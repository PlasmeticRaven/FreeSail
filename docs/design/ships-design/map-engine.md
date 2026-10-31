# Map: the engine and the viewer where the ship designs touch them (head 6b94731)

Phase 3 of `Plan-ShipsWorkflow.md`, a reference for the designers of package 75. It maps the
code on the package's branch at 6b94731 (the lead's 3421829 merged: 73, 86, 84's steps 1 and 2) where
the five ships and the three engine extensions (the settee, the lateen class finished with the
mizen course cut at the mast, the yards under the bowsprit) meet it. Every line number is at this
head. Paths are from the repository root.

**Marks.** *read*: the code at the line cited. *observed*: seen in a scratch script run from the
tree root with `py`, kept outside the repository in the same scratch directory as this map (`sills.py`,
`sprit.py`, `lateen.py`). *measured*: arithmetic on the files or the tables. *judgement*: mine, for the
designers to weigh. No test suite was run.

---

## 1. The sail physics (`freesail/physics/sails.py`, 1,588 lines)

### 1.1 The loop

- `compute_sail_forces(ship, wind, dt)` (335-501) runs every substep. It reads the deck's
  apparent wind at `deck_height_m + WIND_EYE_HEIGHT_M` (1.5 m; 138, 349), then for each driving
  sail: the wind at its own `centre_height_m` (`_FlowField.at`, 715-799; shear 805-812), the area
  after reefs, holes, heel (`cos heel`) and blanketing, a flat plate's lift and drag
  (`_plate_force`, 1079-1132), the loads (`_apply_loads`, 1490-1522). Sums go to the hull as
  thrust, side force, heel moment (`f_stb * centre_height_m`) and yaw about `clr_x_m` (425-429).
  Read.
- The rig is read once a tick and held for the four substeps (`_read_rig`, 575-659; `hold_rig`,
  `release_rig`, 556-562; the `_Drawing` record, 508-529). Anything that changes a sail's
  class-dependent figures mid-tick would break that contract. Read.
- `ship.extra["luff_angle"]` is the area-weighted mean of the driving sails' luff angles
  (431-442); the helm's "full and by" reads it (`physics/hull.py:461`). Read.
- **Heights.** `Sail.centre_height_m` and `Sail.x_m` are above the **water** and from midships.
  `Spar.height_m` is above the **deck** (`_spar_centre_height` adds `deck_height_m`, 1560-1566;
  the viewer the same, `projection.js:22-24`). The Eng note's trial settee mixed the two (Eng
  §4.4). Read.

### 1.2 How a class is modelled

A class is one row of `data/sail_classes.yaml` loaded into `SailClass` (sails.py:181-218): tables
of lift and drag by angle of attack, a luff angle, a reef factor, a furled windage, and (studding
only) a stall. `coefficients()` (199-212) interpolates and applies a hauled bowline's gain.
`peak_alpha` (214-218) is the angle of the greatest lift. The equations are the same for every
class; only the table and the way the chord is found differ. Read.

| Class | yaml lines | Peak lift (α), drag there | Luff | Reef | Furled | Its chord comes from | `TRIM_OFFSET` / `TRIM_RANGE` (trim.py:256-269) | `PEAK_COEFF` (gen_ships.py:135) / measured \|(C_L,C_D)\| |
|---|---|---|---|---|---|---|---|---|
| square | 35-53 | 1.12 (40°), 0.50 | 18° | 0.20 | 0.04 | its yard's brace (`square_chord`, 584-589) | none (braced) | 1.23 / 1.227 |
| gaff | 55-66 | 1.25 (30°), 0.32 | 10° | 0.25 | 0.06 | its sheet (590-596) | 25° / 18-85° | 1.29 / 1.290 |
| jibheaded | 68-79 | 1.30 (28°), 0.24 | 12° | 0.30 | 0.03 | its sheet | 28° / 15-60° | 1.32 / 1.322 |
| lug | 81-91 | 1.20 (35°), 0.46 | 18° | 0.25 | 0.06 | its sheet; ×2/3 against the mast | 25° / 8-85° | 1.29 / 1.285 |
| lateen | 93-103 | 1.15 (35°), 0.48 | 18° | 0.25 | 0.08 | its sheet | 25° / 8-85° | **missing** / 1.246 |
| sprit | 105-114 | 1.05 (30°), 0.34 | 18° | 0.25 | 0.06 | its sheet | 25° / 8-85° | **missing** / 1.104 |
| studding | 116-151 | 1.35 (35°), 0.50 | 18° | 0 | 0 | its parent yard's brace; a sideless one its gaff sail's sheet | none | 1.25 / **1.440** |

Measured: the last column's second figure is the hypotenuse of the table's lift and drag at its
peak, the rule `PEAK_COEFF`'s comment states (gen_ships.py:133-134).

- **Square family** (`SQUARE_FAMILY = {square, studding}`, 142): the chord is the yard, at
  `π/2 − brace_angle` from the centreline, with the drive normal through the after face
  (584-589; `_chord`, 1059-1076). Wind on the fore face beyond the luff angle is "backed"
  (1112-1114). Bowlines (161-172, 1135-1187), goose-winging (149-150, 375-376) and the helm's mark
  (444-448, 883-917) are square-only. Read.
- **Fore-and-aft** (`Sail.is_fore_and_aft`: gaff, jibheaded, lug, lateen, sprit; `ship/parts.py:366-367`):
  the angle is a reading of the sheet (`trim.refresh_reading`, trim.py:472-477), the side is the
  sheet's side, a sheet to windward stands it aback (`held`, 1113-1114), every sheet let fly flogs
  (399-407), wind on the lee face collapses it (1115-1116). Read.
- **What no class reads.** The slope of a yard, a gaff's peak, `corners_m`, the yard's brace for a
  fore-and-aft sail. The only geometry a fore-and-aft sail gives the physics is its area, `x_m`,
  `centre_height_m`, the length of its boom or gaff (`_lateral_offset`, 1320-1351; else
  0.8√A), and its height for blanketing (1.2√A, 1354-1360). Read.
- **Loads.** The sail's chain of spars from its principal spar (graph.py:348-358: `yard`, `gaff`,
  `boom`, `sprit`, `mast`, `halyard_spar`, in that order) carries the whole pull; sheets 0.6 (or a
  boomed sail's lever, 1469-1487), halyards 0.5, braces 0.3 (`BRACE_LOAD_FRACTION`, 117), a stay
  1.0 (115-119, 1438-1522). The braces are those of `ship.yard_of(sail)`: a lug yard's or a lateen
  yard's braces, if the file gives any, take 0.3 of the pull. Read.

### 1.3 How a yard's brace and a gaff's peak enter

- **Brace.** `Spar.brace_angle` (parts.py:179; radians from square, + for the starboard tack) is
  set only by the evolutions and the orders (`brace`, `trim sails`, the manoeuvres); the limit is
  `brace_limit` (177) from the file's `brace_limit_deg`, eased by the catharpins
  (`rigged_brace_limit`, 191-192). It enters the physics only for the square family. A studding
  sail takes its parent yard's (`_trim_yard`, 925-938). Read.
- **Gaff peak.** No field. The generator uses a peak in its own arithmetic and notes (the
  frigate's spanker "peaked 40 degrees", gen_ships.py:1899; the cutter and schooner 27°; the lug
  25°, 7114) to place `x_m` and `centre_height_m`; the physics never sees it; the viewer draws every
  gaff at 35° (§5.3). Read.

### 1.4 The dormant lateen class: where it stands

Confirmed at this head, with the Eng note's lines corrected:

| Piece | Where (this head) | State |
|---|---|---|
| Sail class and its yard role `lateen_yard`, optional `mast` | `ship/schema.py:93, 101, 115` | present |
| `lateen_yard` a spar class, yard-like, 60 kN default | `schema.py:67-84, 91, 246` | present |
| `Spar.is_yard` true for `lateen_yard` (a braced yard) | `ship/parts.py:243-248` (Eng: 238-243) | present: see §3 |
| Curve, never tuned (`TuningNotes.md:127`, "untested rigs") | `sail_classes.yaml:93-103` | present |
| Trim offset and range (8-85°, as the lug's) | `evolutions/trim.py:260, 267` | present |
| `SPAR_WORK["lateen_yard"] = 2.0` (sending down, swaying up, shifting a spare: a yard's work) | `evolutions/scripts.py:3617-3632`, line 3623 | present |
| `set`, `take in`, `trim` words map to `set_lateen`, `take_in_lateen`, `trim_gaff_sheet` | `data/vocabulary.yaml:1756, 1765, 1858` (Eng: 1577, 1586, 1679) | the first two files do not exist: "There is no such evolution" (`runner.py:313`); the third is `applies_to: {class: gaff}` and is refused by `_check_applies` (`runner.py:565-602`) |
| `take_in_words` lateen: [lower] | `vocabulary.yaml:1885` | present |
| `dipping` and `sheeted_to` refused on anything but a lug | `schema.py:1388-1392, 1401-1405` (Eng: 1292-1293, 1303) | blocks the dip |
| `PEAK_COEFF["lateen"]` | `tools/gen_ships.py:135` | **missing**: `static_kn` indexes `PEAK_COEFF[cls]` (440) for every sail on a rated spar in `rate_spars` (841-901), so a lateen or sprit sail on any spar rated by `design_kn` raises a KeyError at generation (read; the failure judgement on a dict lookup) |
| Viewer | `client/projection.js:612-616, 1043-1071` | a rectangle under the yard, the yard braced and tilted a fixed 0.8 rad; `corners_m` ignored (§5.3) |

Observed (`lateen.py`: the frigate's spanker replaced in memory by a lateen sail of the same area
on a `lateen_yard` on the mizzen mast, plain sail set):
- the lateen yard is in `working_yards` and `after_square_yards`; the sail is fore-and-aft and is
  in none of `boom_sails`, `after_gaff_sails` or `shifted_sails` (so a tack neither hauls its sheet
  aft nor shifts it, and a heave-to never brails it);
- the polar's trim braces the yard (to its 60° limit at 60° and 90° off the wind) while the sail
  draws by its sheet (23°, 37°, 64° off the centreline at 60°, 90°, 120°): the physics computes,
  and the yard's brace means nothing to the force.

### 1.5 The polar (`freesail/world/ships.py`)

- `polar_of(ship_file)` (423-447, `lru_cache(maxsize=8)`): the file's `plain sail` group set
  (`_rigged_for_plain_sail`, 364-372), at each angle of `POLAR_ANGLES_DEG` (40 to 180 by 10) and
  wind of `POLAR_WINDS_KN` (8, 15, 25) (130-131), the speed where thrust balances
  `hull.resistance` by 14 bisections (`_balanced_speed_ms`, 394-420), no heel and no leeway.
  `closest_deg`: the first angle with a knot of way in 15 kn. Read.
- `_trim_for` (375-391): every `is_yard` spar braced to its sail's `peak_alpha` within its limit,
  every fore-and-aft sail's sheet to `wanted_sheet_angle(cls)` (trim.py:284-288, which indexes
  `TRIM_RANGE[cls]`: a class not in it raises). Read.
- `Polar.beat_deg` (337-348): the angle under 90° with the best speed × cos(angle), from
  `closest_deg`. Used by the far vessels (`ships.py:682`) and signals (`signals.py:1227, 1238`).
  Read.
- Three caches of eight (`file_descriptions` 266, `rig_height_m` 297, `polar_of` 423): eight
  files at this head, twelve or more after 75; a cost, not a fault (Eng risk 12). Read.
- The "Neufchatel's best point" truth and the 74's "about 11 kn best" are read off this table.

### 1.6 The mizen course cut at the mast: what each route meets at this head

The owner's one rig (Bel §13.5): a four-sided, loose-footed sail laced to the mizen yard abaft the
mast and to the mast, with brails and a reef band; the yard slung across the mast at its truss,
with lifts, its fore part bare. The same sail for the 64 (D9(c)). Read off the code:

| | As class `gaff`, the yard filed as a `gaff` spar | As class `lateen`, on a `lateen_yard` |
|---|---|---|
| Schema | roles `mast` (mast or topmast) and `gaff` (class `gaff`) required, `boom` optional (`schema.py:98, 108`) | role `yard` (`lateen_yard`) required, `mast` optional (101, 115) |
| Physics | a loose-footed fore-and-aft sail by its sheet; lateral offset from the gaff's length (1342-1350) | the same by its sheet; lateral offset from 0.8√A (no boom or gaff) |
| Classification | not `is_yard`: no brace, not in any gate (§3) | `is_yard`: braced by every brace order and by `trim sails`, counted at every gate (§3.3) |
| Manoeuvres | the driver (`after_gaff_sails`, 553-581): brailed up hove to, taken in at the gale's third reef (`storm.py:409-411`); not a boom sail, so not hauled aft in stays | in none of the manoeuvres' lists (observed, §1.4) |
| Evolutions and words | `set_gaff`, `take_in_gaff` (brail up), `furl_gaff`, `reef_gaff`, `shake_out_gaff`, `trim_gaff_sheet`; "brail up" among its take-in words (`vocabulary.yaml:1881`) | none exist; the words lead to refusals (§1.4) |
| Generator | `PEAK_COEFF["gaff"]` present | `PEAK_COEFF["lateen"]` missing: the rating pass raises |
| Viewer | the spar from the mast's throat aft at a fixed 35°, swung by the sheet; the sail from throat, peak and a loose clew 1.5 m above the deck (620-625, 1087-1119); no fore part, no lifts | the yard across the ship, braced and tilted 0.8 rad; the sail a rectangle below it (§5.3) |

Neither draws the yard's bare fore part or its lifts. Plainly: the table is the code's, not a
recommendation; the choice is the one design document's (Bel §13.5).

---

## 2. The lug and the paths keyed to it (package 43b)

### 2.1 Data and physics

- `SailSpec.dipping`, `sheeted_to`, `corners_m` (`schema.py:405-424`); `Sail.dipping`,
  `lug_side` (`parts.py:267-273`), `flying`, `sheeted_to`, `corners_m` (274-280). `corners_m` is
  accepted on any class (`_corners`, 1427-1446) but only the lug's and the staysails' are drawn.
  Read.
- `Spar.is_yard` excludes `lug_yard`: a lug yard is not braced, has no lifts, and is trimmed by
  the sheet (`parts.py:243-248`). Read.
- `against_the_mast(sail, side_sign)` (sails.py:662-670): a `dipping` sail whose `lug_side` is
  not the side its sheet holds it on. Its area is cut to `LUG_AGAINST_MAST_AREA` = 2/3 (135),
  and a lug topsail's with its host (600-606). A second copy keyed the same way is the
  evolutions' expression helper (`runner.py:655-658`, beside `lee_side()`, 650-653). Both key on
  `dipping`, not on class. Read.

### 2.2 The evolutions (data/evolutions/)

| Evolution | applies_to | Steps (s) | Crew | Notes |
|---|---|---|---|---|
| `set_lug` | lug | cast off stops 30 (furled) or clear away 10 (in the gear); hoist 75 | 6 ordinary, forecastle + afterguard | the hoist sets `lug_side` to `lee_side()` and the sheet to \|awa\|−25° clamped 8-85° (line 34) |
| `take_in_lug` | lug | lower 30 (in the gear: "yard on deck"); stow 60 (furled, `lug_side` none) | 6 ordinary, forecastle + afterguard | a lug is never furled aloft |
| `dip_lug` | lug | lower 30; shift 60 (`lug_side` to lee); hoist 60 | 6 able, forecastle + afterguard | refused for a standing lug, and done when already to leeward |
| `trim_lug_sheet` | lug | 0.4 s/m², 20-120 s (script `trim_sheet`) | 6 ordinary, afterguard | |
| `reef_lug` / `shake_out_lug` | lug | settle 30/20, reef 120 / shake out 90, hoist 45 | 6 able / ordinary, forecastle + afterguard | |
| `take_in_square` | square | clew up 60 (in the gear); settle halyards 45 | 10 ordinary, topmen + afterguard + waisters | the pattern for a settee clewed up aloft |
| `furl_square` | square | clew up 60; furl 150 aloft | 12 ordinary, topmen + forecastle + afterguard | |
| `set_square` | square | loose 90 aloft; let go gear 20; sheet home 60; hoist 120; haul aboard 30 | 12 ordinary, topmen + forecastle + afterguard | |
| `take_in_gaff` | gaff | brail up 90 (in the gear) | 8 ordinary, afterguard | the only brail in the evolutions |
| `furl_gaff` | gaff | brail up 90; furl 120 aloft | 8 ordinary, afterguard + topmen | |
| `set_gaff` | gaff | clear away 60 or let go brails 15; hoist 120; haul out 30 | 10 ordinary, afterguard + topmen | sheet \|awa\|−25° clamped 18-85° |

Read. An evolution is found by the sail's class exactly (`orders/verbs.py:419-422`,
`evolution_key`: "flying" is the only override) and checked by `_check_applies`
(`runner.py:565-602`; `applies_to: {class: yard}` accepts any of `YARD_LIKE_CLASSES`, 589-593).
"furl" on a lug, jib, studding sail or flying sail means take in (`FURLED_AS_TAKEN_IN`,
`verbs.py:416`): wrong for a settee furled aloft. A brace on a lug yard loads but no order works
it: `_yard_for` refuses any spar not `is_yard` (`verbs.py:1553-1574`). Read.

### 2.3 Manoeuvres and other paths keyed to the lug

| Path | Where | What it does |
|---|---|---|
| `boom_sails` | `scripts.py:217-233` | a gaff with a boom, **or a lug neither dipping nor `sheeted_to`**: hauled aft at helm's a-lee and held (1071-1080) |
| `shifted_sails` | 298-315 | fore-and-aft sails with a sided sheet, not head or boom sails: shifted over in tack and wear |
| `dipping_lugs`, `LugDip` | 327-333, 336-404 | lowered at "helm's a-lee" (`_ready_about`, 1081-1085), dipped to the old weather side once through the wind (1118-1124, `dip_s` default 90 s), hoisted to leeward when the time is done (`advance`, 379-404); the tack cannot finish while a lug is down (`_lugs_down`, 1088-1090; 1112-1117; 1220-1227) |
| Wear | 1532-1545 | dipped as the wind comes aft, "Lowered the … to dip them" (1538) |
| Heave to | 2241-2249 | dipping lugs lowered as courses are hauled up; boom sails sheeted flat |
| Rounding to (come to anchor) | 6070-6077 | square, jib-headed and dipping or `sheeted_to` lugs to the gear |
| `_set_fore_and_aft` | 6786-6797 | a dipping lug's `lug_side` set to the tack's lee |
| `_lugs_all` / `_standing_lugs_all` | 6800-6804 / 6807-6820 | **dipping** lugs only / the aftermost standing lug not named "topsail" |
| Getting under way as a lugger | 6925 (`self.lugger = bool(_lugs_all(ship))`), 6963-6974, 7086-7089, 7115-7118, 7225-7230; words 6825-6837 | any **dipping** lug sends a ship down the lugger's path (no hand aloft, the first lug hoisted); a standing (non-dipping) lug does not |
| `after_gaff_sails_all` | 7354-7365 | gaff only: a standing settee is never set after the cast |
| `after_gaff_sails` (the driver) | 553-581 | gaff only, on the aftermost lower mast with yards when two masts have yards; brailed up hove to; reduced in a gale (`orders/storm.py:381-411`, square-rigged ships only, `_square_rigged` at 382-384) |
| Navigation's watch on the stern | `orders/navigation.py:778-845` (`watch_the_stern`; 809-814) | reports a dipping lug against its mast once the wind crosses the stern |
| The captains' storm lug | `world/captains.py:2822-2831` (called 2677) | `_lugs_all` and a sail with id `taille_vent`; reads `self.world.ship` |

Read. The log's plural words ("shift the tacks to the weather bow", 1124; "to leeward of the
masts", 399-400; "dip them", 1538) are the lugger's.

**D3(b) against the tack as built.** A ship's mizen in stays is `boom_sails`' work: hauled aft at
helm's a-lee (1072-1080) and let draw on the new tack once her head is through and hung (1125-1128).
A dipping lug is instead lowered at helm's a-lee (1082-1085) and dipped once through (1118-1124).
A settee kept drawing through stays and dipped last is therefore a new path in `TackScript`
(901-) and the wear (1532-1545); no order works an ourse (vang) or a lug yard's brace (§2.2). Read.

### 2.4 The trim limits and the sheet

- `TRIM_OFFSET` (trim.py:256-262) and `TRIM_RANGE` (263-269), quoted in §1.2. The floor is how
  flat the sheet hauls the sail; a new class must be added to both or `wanted_sheet_angle`
  (284-288) and `sheet_geometry` (371-395; it falls back to the gaff's range) misbehave. Read.
- `SheetGeometry` (291-368): a boomed sail swings about the mast on a horse
  (`horse_m`, default a quarter of the boom); a loose-footed sail's clew swings on a foot of
  0.8√A (`LOOSE_FOOTED_FOOT_FACTOR`, 278) to a block a fathom abaft (279). No lead to the taffrail
  exists. `read_sheet` (420-463) is the one truth of the trim; `set_sheet_angle` (497-543) is how
  every order and evolution works it. Read.

### 2.5 Stations and hands

- An evolution names its crew as `crew: {hands, rating, stations: [...]}`. The words are the
  `CREW_STATIONS` (`schema.py:278-287`: forecastle, fore_top, main_top, mizzen_top, afterguard,
  waisters, marines, idlers), `topmen` and `all hands` (`crew/hands.py:93-99`). Read.
- `topmen` resolves through the subject's mast id prefix (`runner._subject_mast`, 1048-1056:
  `mast.id.split(".")[0]`) and `TOP_OF_MAST` {fore, main, mizzen} (`hands.py:104-108`); an
  unlisted prefix (the lugger's `mizen.`, a spritsail yard's `bowsprit`) falls back to every top
  in order (202-220). New mizen masts must be `mizzen.` (two z) to get the mizzen top. Read.
- Marines haul (the `brace` evolution's crew includes them, `brace.yaml:37`) but never go aloft;
  a man hurt at light duty neither (`can_work`, `hands.py:231-238`). Steps marked `aloft: true`
  slow with the roll (`runner._crew_factor`, 1058-1064, reading `ship.extra["motion"]`, 355-360).
  Read.
- At quarters, sail work takes the trimmers first and robs the guns by the bill's priority
  (`crew/quarters.py`, `lend`, 295-345). Read.

---

## 3. How a ship is classed by her yards

### 3.1 The three gates

1. **`Spar.is_yard`** (`ship/parts.py:243-248`): `yard` and `lateen_yard`. Every brace order,
   `trim sails`, the polar's trim, the standing runtime's contrary-order sets
   (`standing/runtime.py:168-172, 791`), the promotion's trim (`world/crews.py:390`) and
   `orders/resolve.py:621` read it. Read.
2. **`working_yards`** (`evolutions/scripts.py:466-469`): `is_yard`, not wrecked, not sent down.
   Every manoeuvre's classification builds on it: `_masts_with_yards` (472-478),
   `head_and_after_yards` (481-491: head = the foremost "mast" by `x_m`), `after_square_yards`
   (494-501), `yards_to_back` (504-523: the mast with the most square area), `yards_to_back_set`
   (526-550), `after_gaff_sails` (553-581), `lowest_square_sails` (618-626: yards whose parent is
   class `mast`), `_boom_mainsails` (6747-6756), the getting-under-way's fore-and-after test
   (`len(_masts_with_yards) < 2`, 7115), and `captains.py:2624` through `yards_to_back`. Read.
3. **`physics.sails._square_rigged`** (852-866): `is_yard` spars on two masts or more, **cached in
   `ship.extra["sails.square_rigged"]`**, bypassing `working_yards`. It decides the helm's mark
   (444-448) and the gale's reduction (`orders/storm.py:382-384`). Read.

`ship.mast_of(part)` (`ship/graph.py:174-182`) returns the root of the spar chain: "the lower
mast (or bowsprit)". A yard `on` the bowsprit or the jib-boom is therefore a "mast" with yards to
every gate. The schema accepts such a yard: its only checks are that the parent exists and a root
is a mast or bowsprit (`schema.py:1507-1520`). `trim.stagger`, `by_level` and `eased_lowest`
(trim.py:98-228) group yards by `mast_of` and the parent's class as level. Read.

### 3.2 What a yard under the bowsprit trips (observed, `sprit.py`)

A spritsail yard (`yard`, on `bowsprit`, brace limit 45°) and a square sail of 45 m² added in
memory:

| Ship | As filed | With the spritsail yard |
|---|---|---|
| frigate-36 | head yards the four fore yards; stagger head the fore mast, diff +2.0° | head yards **the spritsail yard alone**; the fore yards become after yards (12); **stagger head the bowsprit, diff None: no after-yard stagger at all** (no level shared with the bowsprit); `yards_to_back` and `after_square_yards` unchanged; spritsail not among `lowest_square_sails`; `_yard_level` 0 (a course) |
| topsail-schooner | **not** square-rigged; head yards fore topsail and topgallant | **square-rigged** (bowsprit + fore); head yards the spritsail yard; the fore yards after yards |
| brig | head yards the four fore yards | head yards the spritsail yard; "Mainsail haul" would swing the fore yards with the main |

So for the 64 and the bilander a bowsprit-rooted yard must be taken out of `working_yards` and
`_square_rigged` (or each consumer taught its place) and given its own rule for the heave-to and
the trim; and its hands have no top (`TOP_OF_MAST` has no bowsprit). Eng §5's other findings
(force computed as a course's, loaded through the bowsprit, braced to its limit by `brace sharp
up`, thrust slightly negative at 60° off) were not re-run here. Judgement on the remedy.

### 3.3 What a `lateen_yard` or a dry yard trips

- A `lateen_yard` is a braced yard to all three gates: braced by every brace order and by
  `trim sails` (`verbs._trim`, 1078-1108, which braces it to its sail's `peak_alpha`), counted in
  `_masts_with_yards`, `after_square_yards` (observed, §1.4), and paired in `stagger` at level
  `mast` with the crossjack (`stagger` keeps the first yard of each mast and level, trim.py:129).
  On the 64 and the 74 the mizzen already carries the crossjack, so the classification does not
  change; the handling of the yard itself is wrong for a sail trimmed by its sheet. Read; observed.
- A dry yard (the Neufchatel's main yard, the bilander's main yard) makes its mast a mast with
  yards: the Neufchatel becomes square-rigged on two masts (Eng §3.3). D10(a)'s opt-in key "whose
  yards the handling ignores" would have to be read at gate 2 **and** gate 3 (gate 3 does not
  use `working_yards`), and at gate 1's consumers that brace all yards. Judgement.

---

## 4. The lee port and the gunnery

### 4.1 `lee_port_shut` is still unwired

- `combat/shot.py:116-120`: `lowered = sill − half_beam × sin|heel|`, shut when
  `lowered ≤ PORT_SHUT_M` (0.3048 m, 65). Exported (45-57). **No caller in `freesail/`, `tools/`
  or `tests/` at this head**: neither 70, 73 nor 86 wired it (grep; `TuningNotes.md:10074`
  "defined and never called"). Read.
- Its docstring takes the sill at the gun's `height_m` upright (22-24). The generator writes
  `height_m = deck_height + PORT_SILL_M` (0.6 m, `gen_ships.py:3612-3615`; 3833-3834, 3993,
  4293), except the privateer schooner's sourced 3 ft 5 in (4152-4155). Read.

### 4.2 Where heel and roll reach the guns

- `combat/action.py`: `tick_action(world)` (66-127) reads `world.ship`, builds the mark
  (`target_of`, 130-180) and the firer (`_firer(world, ship)`, **212-223**; the task's
  "firer_state" is this function). `Firer` (`guns.py:204-215`): `heel_deg` from
  `ship.dyn.heel`, `roll_deg` from `world.motion` (0 when the world keeps no sea),
  `sea_height_m`, `weather_factor`, **`half_beam_m = beam_m / 2`** (221), heading, position. Read.
- `guns.py`: `_is_lee` (1032-1040: the side she heels to; a pivot by its training); the quoin laid
  against the heel and `effective_elevation` (886-893; `shot.py:110-113`); the scatter
  `steadiness(roll_deg, sea, on_roll)` (898; `shot.py:123-129`); the service rate's
  `seaway_factor(roll_deg)` (522). The mark's heel shows her bottom (`hits._heel_toward_gun`,
  476-482). Read.
- `physics/motion.py`: `Motion.roll_deg` is an **amplitude** (degrees each side), relaxed toward a
  driven oscillator's target (`_train`, `targets`, `tick`: 260-313); the roll period from beam and the floating GM
  (`Particulars.of`, 151-166). It exists only when the World keeps a sea (`core/world.py:643-655`);
  it is also kept on `ship.extra["motion"]` (655), which the runner reads (`runner.py:359`). Read.

### 4.3 Where a wiring goes, and what it moves

- The natural gate is the battery's choice of guns that fire: the single guns (`Battery._fire`,
  `guns.py:788-793`) and the `ready` list (803-810), beside `bears` (753-771) and `_side_fires`.
  A shut port should also stop a lee gun being run out (`wants_work`, 331-340). Judgement.
- Under the owner's rule (heel with the roll's amplitude; sill and half-breadth from the hull
  profile, D12(b)), the inputs not yet in the engine are the sill per gun (or per deck) and the
  half-breadth at the gun's `x_m`. Today `Firer.half_beam_m` is the beam over two. Read.
- **No hull profile exists at this head.** `HullSpec` (`schema.py:344-356`) carries LWL, beam,
  draught, displacement, GM, CLR, lateral area, hull speed, deck height and the rudder; no field
  for a profile, sheer, wale, sill or deck exists in the schema, the generator or the viewer
  (grep). The profile is a new key under `hull` (the brief: "only where a new figure needs a
  key"), written by the generator and served by `ship_graph` for the viewer. Read; judgement on
  the place.
- **Measured** (`sills.py`, sill = the lowest broadside `height_m`, half-breadth = beam/2, heel
  alone): ports shut at frigate-36 21.0°, brig and merchant-brig 24.7°, cutter 24.3° (both fits),
  privateer-schooner 11.0° (both fits); the lugger, smack and topsail schooner carry no guns. The
  roll's amplitude lowers each threshold by itself. These agree with the Eng note's checker
  (Eng §2.6).
- **The pins.** Any combat truth whose firing ship heels (with the roll) past her threshold with
  her lee battery engaged: candidates are the first action's cutters (`first-action.yaml`,
  truths 7-1xx), the frigate's actions, and the privateer schooner's (`tests/test_known_truths.py`
  9176 on; `test_pivot_gun.py`, `test_practice*.py`, `test_magazine.py`, `test_ordnance.py`). Which
  move is not known without running; the ruling asks for each old beside new, with the reason and
  a bisection. Judgement.

### 4.4 The gun keys and the quarter bill by deck

- `GunSpec` (`schema.py:537-559`) has no deck. `Gun.pair_key` is `gun:{number}` for a broadside
  gun, else `gun:{id}` (`parts.py:553-559`); `broadside_pair` writes `gun.N.side`
  (`gen_ships.py:3709`). Two decks numbered 1 to N each would share crews: number on, or add a
  deck key (the brief allows a schema key "where a new figure needs a key"). Read.
- `Quarters.beat` (`crew/quarters.py:155-242`) draws gun crews by station from the gun's `x_m`
  (`_preferred_stations`, 437-460: forward of L/6 the forecastle, abaft −L/6 the afterguard, the
  waisters between, carronades to the marines first). Nothing reads a deck. Read.

---

## 5. The viewer (`client/projection.js`, 1,598 lines; `shipview.js`, `app.js`)

### 5.1 The pipeline

`/api/ship` serves `queries.ship_graph(ship)` (`freesail/api/queries.py:380-406`): the hull's
LWL, beam, draught, `deck_height_m`, displacement, GM, CLR; each spar (316-330: class, x, height,
length, parent, side, brace, limit, rake, rating, rigged_out); each sail (333-353: class, roles,
area, x, centre, reefs, sheet angle, dipping, flying, `sheeted_to`, `corners_m`); the lines.
**No guns, ports, decks or profile are served.** `buildSkeleton(graph, snapshot)` (273-1377) makes
3-D figures in ship coordinates; `project(skeleton, facing, heel)` (1484-1523) heels them about
the waterline (no roll) and projects orthographically; `shipview.js` renders SVG (hull classes at
58-60; colours `style.css:13-26, 149-158`). Facing: leeward by default, `?facing=`, `[` `]`
(`app.js:4-8, 74`); pictures 960 × 720 (`app.js:158, 189-258`). Read.

### 5.2 The hull: one generic lens

`hullFigures(hull)` (1416-1448), added to the figures at 1374 and to the fixed frame at
1407-1409: stern at −0.52 L, bow at +0.56 L, half-breadth B/2·(1−|t|^2.2)^0.55, transom 0.28 B,
deck at F(1 + 0.12t² + 0.1t) with F = `deck_height_m`, sides down to −0.8 m; figures `deck`,
`side` (starboard, larboard), `transom`. Only LWL, beam and `deck_height_m` vary; draught is unused.
No ports, wales, head, galleries, guns. The same `deck = hull.deck_height_m || 1.5` (275) is the
datum of **every spar's height and every `corners_m` height** (e.g. 506-508, 580, 621-629, 381, 1132-1134).
Read. So D18's choice (whether the file's deck height stays the spars' datum when the sides come
from the profile) touches the physics (`sails.py:349, 1562`; `physics/hull.py:391`;
`world/lookout.py:215`; `api/readings.py:382`) and every spar of the drawing. Read; judgement.

### 5.3 Spars and sails by class

| Part | How it is drawn (read) |
|---|---|
| Lower mast | at `x_m`, raked; upper masts continue its line with a 12% doubling (`DOUBLING`, 51; 501-527) |
| Bowsprit, jib-booms | from the bowsprit's `x_m` at deck level, rising to `height_m` at the tip (528-544) |
| `lug_yard` with a cut | from `lugCut` (365-393; 538-554): the corners swung about slings a third along throat→peak, shifted so the slings meet the mast, on `lug_side` (`lugSideSign`, 346-353: a standing lug lies to leeward of the tack), on deck when lowered |
| `yard`, `lateen_yard`, `lug_yard` without a cut | at the parent's x and `deck + height_m`, braced by the snapshot's `brace_angle`; a square yard slung 0.05 B before a mast (`YARD_BEFORE_MAST_OF_BEAM`, 113; 605); **tilted a fixed 0.8 rad (lateen) or 0.35 rad (lug) up toward its after end** (612-616); hoisting on the cap by state (580-603) |
| Yard on the bowsprit | `parent.x` is the bowsprit's `x_m` (its heel at the stem; no `xAt`), z = deck + `height_m`, athwartships, braced; no slinging offset (only for a mast parent) (605-607) |
| Gaff | throat at the mast, **peaked a fixed 35°** (`GAFF_PEAK_ANGLE`, 44; 620-625), swung by its sail's sheet |
| Boom | from the mast at its height, swung by the sheet (627-631) |
| Sprit | from deck + 1.0 m at a fixed 0.9 rad (632-637) |
| Square sail | `squareCut` (990-1029): head on its yard, clews at 0.9 of the yard below; with none below, 0.9 of its own yard wide and area/width deep (1024-1028); over a bare yard by `bareFoot` (455-462) |
| Lug sail | from `lugCut` (1052-1065), cut in pieces at its mast |
| **Lateen sail** | **from its yard's two ends, a rectangle area/L deep hanging below** (1066-1071); `corners_m` ignored |
| Gaff and sprit sails | throat, peak, clew, tack; loose-footed clew placed from the area, the foot 1.5 m above the deck (`LOOSE_FOOT_HEIGHT_M`, 45; 1087-1119); brailed in the gear as a narrow shape along the luff (1112-1118) |
| Jib-headed | along the stay or from `corners_m` (1120-1225) |
| Studding, ringtail, water sail | 1226-1267 |
| Lines | braces, sheets, hauled bowlines only (1292-1344); a lug's sheet from its clew to the lee rail a metre abaft (1309-1315); a lateen's sheets as a square sail's, to the yard below or the rail (1316-1322) |
| Draw order | far to near by the sail's centre; ties by kind, then `SAIL_CLASS_RANK` (66; 1524-1550) |

Consequences (read): a lateen sail is drawn by its yard's **brace** while the physics trims it by
its **sheet**, so the two disagree on every tack; a lateen yard braced square is drawn across the
ship tilted 46°; a spritsail with no yard below hangs area/(0.9 L) deep from a yard at the stem
(Eng §5 saw its foot under the water on the brig).

### 5.4 The pictures' tests and their thresholds

- `tests/test_pictures.py` (411 lines; skipped without Playwright, its browser or Pillow): the
  frigate in `lesson-falmouth.yaml`, the chart and the ship's view through the API door (228) and
  the MCP bridge (356). A picture passes when the standard deviation of the RGB mean exceeds
  `BLANK_STD` = 8.0 and more than `DARK_FRACTION` = 0.001 of the pixels are under
  `DARK_LEVEL` = 110 (57-59, 186-200). The hull side (#4a3d31, mean 61) and the spars (#3b3128)
  are the dark pixels; the sea (#5f7d8c, mean 120) is not. Read; measured (the means).
- `tests/test_view_geometry.py` (892 lines, Node): the tests that read the hull or the deck datum
  are the fixed frame (181-203, 620-658: bounds equal across states of one ship, the hull points
  included), the cutter from her file (445-478: `sk.hull`, boom end abaft −L/2, bowsprit tip past
  L/2 + 8 m), a yard at its hoist (`file_z = deck_height_m + height_m`, 630), the lowered lug
  (`< deck + 1.0`, 778-781), the square sails' areas within 5% (572-602). `test_server.py:220-221`
  checks the client files are served. Read.
- A drawn profile changes the frame and the dark pixels of every ship; the equalities compare
  states of one ship and stand; the absolute thresholds would move only if the hull's figures
  change their kinds or the deck datum moves. Judgement.

---

## 6. The quarter bill and stations after 73 and 86

- `QUARTER_BILL_KEYS` = trimmers, helm, powder, priority, small_arms, boarders, filling
  (`schema.py:229`); `QuarterBillSpec` (494-514: `small_arms` and `boarders` 73's, `filling`
  practice and resupply's, None reckoned); parsed at 1059-1092; written by
  `Builder.quarter_bill(note, trimmers, helm, powder, priority, notes, small_arms, boarders,
  small_arms_note, boarders_note, filling)` (`gen_ships.py:799-839`). Read.
- Files with a bill (observed by loading): brig, cutter, frigate-36, merchant-brig,
  privateer-schooner (all seven keys); none on lugger, smack, topsail-schooner (no fits either;
  brief item 5). Marines in `stations`: frigate 40, brig 20, others none.
- `Quarters.beat` (`crew/quarters.py:155-242`) assigns, in order: the carpenter's crew and
  surgeon's mates by trade; the trimmers by station; the helm (able afterguard); the gun crews
  forward first by `_preferred_stations`; the powder (landsmen, then any, then every idler); the
  marines' division; the rest as trimmers. `marines_to_arms` / `marines_to_guns` (117-153, 73's)
  move fit marines between the carronades and their muskets. `small_arms_count`, `boarders_count`
  (`combat/small_arms.py:151-176`). Marines' kit by nation `data/nations.yaml:45-48` etc. Read.
- **The filling party** (`combat/filling.py`): `filling_of` (61-71: the bill's `filling`, else one
  to every four cannon, `CANNON_A_FILLER`); `fillers` (74-96): at quarters the first `filling` fit,
  idle men of the powder division, **read, never moved**; out of quarters the bill's number while
  the idlers are up, nobody by night. **The fillers are not posts at this head**: the gunner, the
  gunner's crew and the quarter gunners as real posts that compete for hands are 77's unless 75
  takes them first (brief, `M7-WorkPackages.md:1649-1653`; `filling.py:14-17`). Posts today are
  `PostSpec(post, name)` (`schema.py:439-444`) kept as `crew.posts` (`crew/model.py:225-231`). Read.

---

## 7. The World and the Hull (84's steps 1 and 2 at this head)

### 7.1 The names a builder uses

- **Two classes named `Hull`.** `freesail.ship.parts.Hull` (1793) is the physics hull a `Ship`
  carries (`ship.hull.spec`, `.gm_m`, `.length`, `.hull_speed`). `freesail.world.hulls.Hull` (184)
  is 84's: one ship's share of a World. Read.
- `world/hulls.py:52-127` `PER_SHIP_FIELDS`: `ship`, `origin`, `_position`, `lookout`, `ground`,
  `tide_state`, `glass`, `conditions`, `sea`, `motion`, `wind`, `wind_record`, `sun`, `navigation`,
  `log`, `places`, `people`, `stations`, `papers`, `hold`, `purse`, `stores`, `ports`, `fishery`,
  `needs`, `water`, `ship_lost`, `health`, `standing`, `captain`, `agents`, `agent_journals`,
  `player_seat` and private bookkeeping. Each is a field of the Hull and, on the World, a
  delegating property to `world.own` (installed at `core/world.py:2138-2144`). Read.
- `hulls.py:131-154` `SHARED_FIELDS`: `seed`, `scenario`, `clock`, `rng`, `chart`, `tide`,
  `systems`, `weather`, `nations`, `registry`, `vessels`, `squadrons`, `business`, `world_orders`,
  `marks_of_interest`, `director_*`, `journal`, `inputs`, `station_acts`, `compression`: exposed on
  the Hull under the same names (304-306). Read.
- The Hull's own reads (221-302): `name`, `ship_x`/`ship_y` (and `_km`), `position`,
  `tide_height_m`, `at_anchor`, `heading_deg`, `company`, `aboard`; it forwards `record`, `submit`,
  `readings`, `daylight` to the World. Read.

**For builders** (the lead's note; judgement on the form): write new code against an object that
may be a World or a Hull and read only these names (`x.ship`, `x.motion`, `x.sea`, `x.position`,
`x.clock`, `x.rng`, `x.record(...)`); never test `isinstance(..., CrewedWorld)`; where a ship-level
handle exists prefer it (`ship.extra["motion"]`, as `runner.py:359` reads the roll;
`ship.extra.get("crew")`, `quarters_of(ship)`). Code a 75 builder is likely to touch that reads
World names today: `combat/action.py:66-127, 212-223` (`world.ship`, `world.motion`,
`world.sea`, `world.position`, `world.clock`, `world.rng`), `world/captains.py:2620-2627, 2822-2831`
(`self.world.ship`), `api/queries.py:419-475` (`world.ship`). All of these names are kept by the
Hull, so they need no change for 84. The generator and the ship files are untouched by 84 (OneWorld
§3.5: "75 waits for nothing").

### 7.2 What steps 1 and 2 changed (Design-OneWorld.md:1390-1535)

- `World.own` is a `Hull` made first in `World.__init__` (`core/world.py:463-469`); its id is the
  vessel's for a crewed ship's World and `hulls.own_id()` (175-181) for the player's. Methods
  (`tick`, `record`, `submit`, the `_tick_*`) stay on the World until step 6. Read.
- `World.__setstate__` (861-) lifts an old checkpoint's per-ship fields into a Hull
  (`hulls.lift_old_state`, 309-325). Read.
- One `people.Registry` (`world/people.py:504-`) on `world.registry`, shared by a crewed ship's
  World with its parent (`core/world.py:477`); `People` is one hull's company as a view; persons
  gain `hull` and `home` (`aboard` a bool property over `hull`, 422-430); things gain `hull`;
  hearing by spot (`world/hearing.py:62, 111`); `find_anywhere` (`people.py:1021`). Read.
- **Still standing**: `CrewedWorld` (`world/crews.py:166`) with its own Hull under its vessel's id;
  `CREWED_CAP` 3 and `CREWED_FLOOR_TICKS_S` 60.0 (`crews.py:88-91`); the World's log is the
  player's. Steps 3 onward are built from the head after 86's merge, alongside 75. Read.

---

## 8. Pace

- **Floors.** `BUILD_MACHINE_FLOOR` = `BUILD_MACHINE_MEASURED` 1000 × `BUILD_MACHINE_MARGIN` 0.5 =
  **500** ticks a second (`tests/test_known_truths.py:2143-2162`; the owner's budget 3000 at an
  assumed ratio 2.0 is not asserted). `CREWED_FLOOR_TICKS_S` = **60.0** with the cap of three full
  (`world/crews.py:88-91`). Read.
- **The pace tests**: truth 51 (`test_known_truths.py:2165-2181`), 2656, 2749, 3431, 4580 (against
  500); 7-138 (8311-8334, two crewed cutters in action), 7-151 (8811-), 7-159 (9104-9139, 500),
  7-160 (9142-9160, the crewed floor under the cap); truth 88 (`tests/test_crews.py:182-206`).
  Each is the best of three runs of a thousand ticks after a thousand to settle. Read.
- **Routing.** `tests/conftest.py:490-500` (`_is_pace`) marks a test `pace` and `slow` when it
  carries `@pytest.mark.pace` or its name ends `holds_truth_51s_floor` or
  `ticks_at_the_build_machines_floor`; the lead's whole-suite workflow runs them alone after the
  shards. A new 74 pace truth must be so marked or so named, or it will run in the fast tier on a
  loaded machine. Read; judgement.
- **`tools/pace.py`** (144 lines): modes `alone` (the frigate in the station trial),
  `far` (the merchant passage's dozen), `crewed --ships N` (the frigate with N of the twelve in
  `SHIPS`, four files only, 31-45), `squadrons` (the convoy of six at caps 0, default, 12),
  `--profile`. `measure` is truth 51's form (62-78). A 74 needs a file in `SHIPS` or a mode of
  her own. Read.
- Eng §2.7 measured a muster of 491 at 2-8% slower a tick than 264; the 74's 590 has not been
  measured.

---

## 9. The Eng note at this head: corrections

| Eng says | At 6b94731 |
|---|---|
| `is_yard` `parts.py:238-243`; dipping 262-268; `is_fore_and_aft` 360-362 | 243-248; 267-273; 366-367 |
| `against_the_mast` `sails.py:657-664` | 662-670 (a second copy in `runner.py:655-658`) |
| dipping refused `schema.py:1292-1293`; `sheeted_to` 1303; corners 414-419; stations 277-286; spar roots 1409-1446 | 1388-1392; 1401-1405; 419-424; 278-287; 1507-1520 |
| vocabulary 1570-1680 (lateen 1577, 1586, 1679) | 1749-1886 (1756, 1765, 1858; take-in words 1885) |
| captains 2639-2648, 2783-2792 | 2620-2627 (`yards_to_back`), 2822-2831 (`_lugger_storm_lug`, called 2677) |
| `lugger()` 6809, peak 6877, `_quad_area_centroid` 6794-6806 | 7045, 7114, 7030- |
| `gun_crew` 3449-3455; `exercise_allowance` 3514-3520; `broadside_pair` 3567; `pivot_gun` 3607-3620 | 3591; 3656; 3709; 3749 |
| "Takes the lugger's path whenever any lug exists" (§4.6) | only a **dipping** lug (`_lugs_all`, 6800-6804); the trial agrees (the standing settee got under way) |
| `PEAK_COEFF["lateen"]` needed (§4.7) | and without it the generator's rating pass raises on any lateen or sprit sail (`gen_ships.py:440`) |
| Lines in `sails.py` 575-617, 1047-1056, 1320-1360, 1552-1576; `trim.py:256-269`; `projection.js` | unchanged |

---

## 10. Found on the way

1. `PEAK_COEFF["studding"]` is 1.25; the studding curve's peak gives 1.44 (measured). It rates
   only the studding-sail booms (`rate_spars` keeps studding sails for those alone, 886-888);
   changing it moves every file with studding sails. Not 75's to change silently. Judgement.
2. `stagger` with a bowsprit as the head "mast" silently drops the after yards' stagger and the
   log's difference (observed, §3.2).
3. A lateen yard's braces would carry 0.3 of the sail's pull though the sail is trimmed by its
   sheet (`_load_path`, 1438-1466). Read.
4. `world.motion` is None when the World keeps no sea; `_firer` then reads a roll of 0
   (`action.py:218`). A lee-port rule with the roll must not assume a sea. Read.
5. `lee_port_shut` takes `heel_deg`; `Firer.heel_deg` is signed (+ starboard) and `_is_lee` decides
   the side; the function itself takes the absolute heel. Read.
