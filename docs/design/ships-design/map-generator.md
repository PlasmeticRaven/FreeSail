# Map: the generator, the schema and the ship files (package 75, Phase 3)

The package 75 clone (D:/Projects/FreeSail/FreeSail-pkg-75) at head 6b94731 (the lead's 3421829 merged in: packages 73, 86 and
84's first two steps). Every `file:line` is at that head. Read-only: nothing in the repository
was changed. Marks: **read** (from the code or file), **measured** (a scratch script run from the
tree root, outside the repository), **judgement** (an inference a designer should check). Where no
mark is given, the fact is read.

## 0. Twenty facts to carry into every design

1. One script, `tools/gen_ships.py` (8,490 lines), writes all eight files in `data/ships/`. There is no
   `main()`. The ship list is the `if __name__ == "__main__":` block at `tools/gen_ships.py:8479-8490`.
   `tools/ships/` does not exist, and neither does `tools/__init__.py` (measured).
2. Byte identity: `py tools/gen_ships.py <scratch>` reproduces all eight committed files byte for byte
   at this head on this session's Windows machine (measured with `cmp`). The guard is
   `tests/test_ship_particulars.py:555-581`, which regenerates into `tmp_path` and compares as UTF-8
   text. Its file list (`:565-574`) is explicit, so a new file must be added to it.
3. The generator calls the engine. The rating pass (`Builder.rate_spars`, `tools/gen_ships.py:841-904`)
   loads the document through `freesail.ship.loader.ship_from_dict`, and `fit_magazine` imports
   `freesail.ship.parts` (`:3629`). So a new spar or sail class, a new gun key or a new crew key must
   be accepted by `freesail/ship/schema.py` **before** a generator module writes it. Otherwise
   generation fails.
4. The schema refuses unknown keys in some places and silently drops them in others (measured
   by a probe). It **refuses** them in a gun, a fit, the armament, the quarter bill, the crew section,
   a pump, a boat, an anchor, a sail-room entry and a person role. It **silently drops** them at the
   top level, in `hull`, in a spar, in a sail and in a line. A hull profile written before
   `HullSpec` knows it simply vanishes from the parsed ship.
5. A gun has no `deck` key: `GUN_KEYS` is at `schema.py:202-214`, and the probe was refused with
   "has 'deck', which a gun does not take". The owner's "quarter bill by deck, with a deck key on each
   gun" (Decisions, the 74's answers) is a schema change.
6. `combat/shot.py:116` `lee_port_shut(sill, heel, half_beam)` is defined, but **nothing calls it**
   (measured with grep over `freesail/` and `tests/`). A gun's `height_m` is its sill above the water
   upright (`shot.py:22-24`). The heel at which each existing gun's lee port would shut is given in §3.3.
7. `PEAK_COEFF` (`tools/gen_ships.py:135`) has square, studding, gaff, jibheaded and lug only. A `lateen`
   or `sprit` sail, or a new settee class, raises `KeyError` in `static_kn` (`:434-441`) during the
   rating pass. The curves for lateen and sprit exist in `data/sail_classes.yaml:93` and `:105`.
8. `LONG_GUN_CWT` (`:3577`) has 18, 12, 9, 6, 4 and 3 only, and `CARRONADE_CWT` (`:3578`) has 32, 24, 18
   and 12. There is no long 24- or 32-pounder and no 42-pounder carronade. The 64, the razee and the
   74 need entries.
9. `exercise_allowance` (`:3656-3662`) gives a fourth of the upper deck guns. Its docstring says the
   Regulations give "a third in ships of two or three decks", which the function does not do.
10. `ground_tackle_for` (`:494-565`) always gives two bowers, a sheet and a stream at 200 tons and
    over, and a kedge. The 74's four bowers by Steel would have to be written through
    `Builder.ground_tackle` directly. No ship does that today.
11. A ship is sailable at far detail only if she has a `"plain sail"` group: `polar_of` sets that
    group alone (`freesail/world/ships.py:364-372`). The engine also reads these groups by name:
    "topsails", "courses", "headsails", "jibs", "gaff sails", "storm canvas", "storm staysails",
    "lying-to staysails", "occasional sails" and "all sail" (measured with grep; §1.4).
12. A far vessel's file comes only through the description index: `vessel_from_spec` takes
    `d["file"]` from `DESCRIPTIONS` (`ships.py:1131-1137`, `:1171`). A scenario cannot give a far ship a file
    of its own, so every new file sailed as another sail needs a `DESCRIPTIONS` entry.
13. `size_of_words` and `size_rank_of` match `_SIZE_WORDS` in order (`captains.py:296-305`). There,
    "a ship" means 3, the frigate's rank, so "a ship of the line" ranks as a frigate. The test
    `tests/test_ships.py:101` asserts that `description_key("a ship of the line") is None`. The 74
    moves that assertion, so it must be shown old beside new.
14. Three caches are sized to the eight files (`lru_cache(maxsize=8)`): `file_descriptions`,
    `rig_height_m` and `polar_of` (`ships.py:266`, `:297`, `:423`). With 12 or 13 files they evict.
    That does not change the results, but the pace could move (judgement).
15. Posts and drawn roles come from `data/people/<stem>.yaml` and are read at import
    (`gen_ships.py:3502-3532`). A new file needs a wardroom file. Such a file is hand-written data, not
    generator output. `privateer-schooner.yaml` has none (measured): `wardroom_path` returns None and
    the file borrows the schooner's posts.
16. The marines' detachment is the file's `crew.stations.marines`, with its officer and sergeant drawn
    from it by the wardroom file. The kit is the nation's: `data/nations.yaml` `marines: {kit: ...}`
    leads to `data/marines.yaml`. Nothing about marines is in the generator beyond the station count (§1.9).
17. The id and pair rules: a broadside gun's `(number, side)` must be unique in its fit
    (`schema.py:1664-1670`), and the pair of one number shares one crew (`ship/parts.py:554-559`
    `pair_key`). The frigate numbers straight on across decks: upper deck 1-13, quarterdeck carronades
    14-17, forecastle 18, quarterdeck 9-pounders 19 (`gen_ships.py:3836-3893`).
18. Variants are made by running the ship function again with a flag, then mutating `b.doc` before
    `dump`: `schooner(armed=True)` and `brig(merchant=True)`. A `Builder` cannot be dumped twice,
    because `dump` mutates the document (§1.6).
19. The yards under the bowsprit: a `yard` with `on: bowsprit` and a square sail on it **load**. The
    spar chain is `[spritsail.yard, bowsprit]` (measured with a probe on the frigate). The schema
    refuses nothing there. What the physics, the evolutions and the viewer make of it is the engine
    design's question.
20. Per 84: in the files this map covers, `world.ship` or `CrewedWorld` appears 23 times in `captains.py` and twice in
    `ships.py` (`:1456`, `:1810`), plus one comment at `:503` (measured). It appears 0 times in the
    generator and the schema. `world.ship` is now a property onto `world.own`, the Hull
    (`freesail/world/hulls.py:14-25`, `PER_SHIP_FIELDS` at `:52`). Code written against it should use
    the names the Hull keeps (Design-OneWorld §2.2).

## 1. `tools/gen_ships.py`

### 1.1 Layout (line ranges)

| Lines | What |
|---|---|
| 1-117 | Module docstring: the rules (Luce's masting rules, rope by Luce ch. IV, ratings, brace limits). It says "four reference ship files", which is stale. |
| 119-125 | Imports; `REPO_ROOT` put on `sys.path` so that the engine's loader imports when the script runs as a script. |
| 126-180 | `SIDES`, `FT`, `ROPE_KN_PER_SQ_IN`, `PEAK_COEFF` (135), `SUSTAINED_FRACTION` (144), `DESIGN_WIND_KN` (148-157). |
| 181-390 | Canvas: `FRIGATE_CANVAS` (184), `SCHOONER_CANVAS` (303), `cloth` (348), `storm_cloth` (355), `canvas_note` (364). |
| 391-452 | `ft` (395), `rope_kn` (410), `DesignLoad` (415-431), `static_kn` (434), `design_kn` (444). |
| 453-565 | Ground tackle constants (453-491; `BOWER_CWT_PER_100_TONS` 465) and `ground_tackle_for` (494-565). |
| 568-571 | `quarter` (rope to the quarter inch). |
| 573-1078 | **`class Builder`** (§1.2) and `dump` (933-1078). |
| 1102-1430 | Package 57's staysails between the masts: `stay_sail_cut` (1110), `stay_point` (1142), `staysail_from_cut` (1148), `between_the_masts` (1197). |
| 1433-1463 | `square_sail_lines` (the running rigging of one square sail and its yard). |
| 1473-1513 | `FRIGATE_ROPE` and `FRIGATE_MAST_ROPE_FACTOR`. |
| 1516-2507 | **`frigate()`** (§1.3). 2515-2527: `FRIGATE_RAKE_DEG`, `raked_x` (2519), `SPANKER_*`. |
| 2535-3321 | **`schooner(armed=False)`**: both Speedwell and, with `armed`, the privateer. |
| 3335-3405 | Hold and boats: `hold_for` (3367), `boat_entries` (3378), and their constants (3356-3364). |
| 3407-3474 | Pumps and the notes of 73: `CHAIN_PUMP_*`, `HAND_PUMP_*`, `SMALL_ARMS_NOTE` (3412), `BOARDERS_NOTE` (3417), `PUMPS_NOTE` (3423), `SHOT_PLUGS_NOTE` (3429), `pump_entries` (3437). |
| 3475-3556 | `BOATS_NOTE`, `PEOPLE_DIR` (3502), `wardroom` (3507), the posts tuples (3528-3532), `ration_entries` (3535). |
| 3558-3816 | **Guns** (§1.7): the weights, `gun_crew`, the rounds, `PORT_SILL_M`, `fit_magazine`, `exercise_allowance`, `filling_party`, `MAGAZINE_NOTES`, `FILLING_NOTE`, `broadside_pair`, `chasers`, `pivot_gun`, `swivels`, `spaced`, `QUARTER_BILL_NOTE` (3801), `PRIORITY_NOTE` (3811). |
| 3819-4439 | Armament functions: `frigate_armament` (3819), `cutter_armament` (3985), `privateer_schooner` (4103), `schooner_armament` (4139), `brig_armament` (4289), `merchant_brig_armament` (4372). |
| 4442-4836 | `frigate_crew` (4442), `schooner_crew` (4663). |
| 4839-5795 | `CUTTER_CANVAS` (4839), `CUTTER_ROPE` (4866), **`cutter()`** (4898-5613), `cutter_crew` (5616). |
| 5755-7027 | `BRIG_CANVAS` (5755), **`brig(merchant=False)`** (5798-6646), `merchant_brig` (6649-6714), `merchant_brig_crew` (6717), `brig_crew` (6823). |
| 7001-7818 | `LUGGER_CANVAS` (7001), `LUGGER_TOPSAIL_ROPE` (7021), `LUGGER_POSTS` (7027), **`lugger()`** (7045-7636), `GEAR_NOTE` (7642), `lugger_crew` (7649). |
| 7774-8476 | `SMACK_CANVAS` (7774), `SMACK_ROPE` (7796), `SMACK_POSTS` (7818), **`smack()`** (7821-8398), `smack_crew` (8401). |
| 8479-8490 | The entry point and its ship list (§1.10). |

### 1.2 The Builder API (`tools/gen_ships.py:573-1078`)

`Builder(name, rig, era_notes, hull, hull_notes=None)` (`:574-589`) starts `doc` with `ship`, `hull`,
`spars`, `sails`, `lines`, `groups` and `aliases`, in that order. Every later section is appended
in the order of the calls, and the file's key order is that insertion order (`yaml.safe_dump(...,
sort_keys=False)`, `:936`). So for byte identity, **the call order is part of the file**.

| Method | Line | Writes | Notes in the file |
|---|---|---|---|
| `spar(id, cls, note, **kw)` | 591 | `spars[]`; a `studdingsail_boom` gets `rigged_out: false`. `None` kwargs are dropped. | `notes[id]`, the comment above `- id:` |
| `sail(id, cls, note, **kw)` | 605 | `sails[]` | `notes[id]` |
| `line(id, cls, of, side, rating, note, parts)` | 613 | `lines[]`; `parts` only when above 1 | `notes[id]` |
| `sided(base, cls, of, rating, note)` | 627 | `base.starboard` and `base.larboard` | the note on starboard only |
| `group(name, members)` / `alias(name, target)` | 633 / 636 | `groups`, `aliases` | none |
| `crew(entries)` | 639 | **replaces** `doc["crew"]` from `(path, value, note)`. Paths: `("complement",)`, `("names",)`, `("stations", st)`, `("ratings", r)`, `("posts", post)` (value None), `("idlers_by_trade", trade)`, `("stores", key)`, `("ration", key)` (`ration_entries`, 3535) | `crew_notes[path]` |
| `sail_room(note, entries)` | 657 | `crew.stores.sails` from `(kind, canvas_no, note)`, each at condition 100 | per kind |
| `spare_spars(note, entries)` | 666 | `crew.stores.spare_spars` by class | per class |
| `ground_tackle(note, anchors, chain)` | 676 | `ground_tackle` from 8-tuples `(id, kind, name, weight_kg, cable_fathoms, cable_in, cable_kn, note)` | section and per anchor |
| `hold(capacity_tons, note)` | 700 | `hold` | section |
| `boats(note, entries)` | 706 | `boats[]` from 8-tuples (`boat_entries` makes them) | section and per boat |
| `pumps(note, entries)` | 727 | `pumps[]` from 6-tuples (`pump_entries`) | section and per pump |
| `gear(note, entries)` | 739 | `gear[]` (fishing; package 56) | section and per piece |
| `people(note, entries)` | 752 | `crew.people` from `(role, station, rating, messenger, note)` (`wardroom()` makes them) | per role |
| `armament(note, default, fits)` | 772 | `armament: {default, fits: {name: {source, guns, **magazine}}}` from `(name, source, guns, magazine, note)`, where `guns` is `[(mapping, note)]` | section, fit, gun, magazine keys |
| `quarter_bill(note, trimmers, helm, powder, priority, notes, small_arms, boarders, small_arms_note, boarders_note, filling)` | 799 | `crew.quarter_bill`, keys in the order trimmers, helm, powder, filling (when given), priority, small_arms, boarders | per key; the default notes are `SMALL_ARMS_NOTE` and `BOARDERS_NOTE` |
| `descriptions(entries)` | 923 | `ship.descriptions: {key: {rig, what, note}}` (the far words; §4.1) | none |
| `rate_spars()` | 841 | the second pass, run by `dump`: every `DesignLoad` rating is recomputed from the sails whose spar chain passes through the spar, at its design wind (§1.3) | appends "Rating: ..." to the spar's note |
| `whole_ship_groups()` | 906 | run by `dump`: "lower/topmast/topgallant studdingsails" and alias `sails` -> `all sail` when absent | none |
| `dump(path, header)` | 933 | §1.5 | |

Order constraints (read): `crew()` replaces the whole crew section, so `people`, `spare_spars`,
`sail_room` and `quarter_bill` must come after it. `quarter_bill` also writes into `doc["crew"]`.
Direct writes to `b.doc` are the house way for a variant's last words (`:4109`, `:6656-6657`, `:8325`) and for a rating fixed late (`:7311`, `:7462`).

### 1.3 One ship function end to end (the frigate, `:1516-2507`)

1. **Hull figures** (`:1517-1533`): published dimensions in feet go through `ft()` to metres.
   `lwl`, `beam`, `draught`, a displacement by block coefficient, and `deck_height` (1.8 m).
2. **`b = Builder(...)`** (`:1535-1580`): name, rig word, era notes, the hull dict
   (`length_waterline_m`, `beam_m`, `draught_m`, `displacement_kg`, `gm_m`, `clr_x_m`,
   `lateral_area_m2`, `hull_speed_kn`, `deck_height_m`, `rudder{area_m2, max_angle_deg, rate_deg_s,
   span_m}`), and `hull_notes` keyed by the same names, each written above its line.
3. **Spar geometry in feet** (`:1582-1632`): Luce's ratios give `geom[mast]`, with `above`, `head`,
   the hoists, the yard lengths and the yard heights above the deck. Then the areas and centres
   (`:1634-1672`) and the brace plans (`:1674-1686`).
4. **Per mast** (`:1713-1839`): `b.spar` for the mast (`x_m`, `rake_deg`, `height_m` above the
   deck), the topmast, the topgallant and the royal (`steps_on`, `height_m` = the hoist above the
   cap). Then per level a yard (`on`, `length_m`, `height_m` above the deck, `brace_limit_deg`) and
   its square sail (`area_m2`, `x_m` by `raked_x`, `centre_height_m` above the water, `canvas_no`,
   `cloth_rating_kn`, `reef_bands`, `flying` for royals), with `square_sail_lines` (`:1433`).
   Then the shrouds and topmast backstays by `b.sided`. Ratings are `design_kn(carried,
   DESIGN_WIND_KN[level])` placeholders, finalised by `rate_spars`.
5. **The mizzen** (`:1841-1906`): `mizzen.crossjack.yard` is **bare**, with no sail. The gaff and
   boom spanker follows with its halyards, sheet, outhaul and vangs. This matters for the 74's mizen
   course and the 64's D9(c) sail.
6. **The head** (`:1908-2003`): the bowsprit (outboard `length_m`), `jib_boom` and `flying_jib_boom`
   (`on` the spar inside), the stays (`main.stay`, `bobstay`, `martingale`), and the head sails hanked
   to stays (`stay` role).
7. **The staysails between the masts** (`:2005-2017`): `between_the_masts` (`:1197`) cuts each sail
   by Steel and writes `corners_m`.
8. **Studding sails** (`:2019-2094`): `studdingsail_boom` on its yard, with `side`, and the sail with
   `boom` and `yard` roles.
9. **Storm canvas and occasional sails** (`:2096-2301`): `bent: false`, `in_place_of` (the storm
   mizzen for the spanker), the ringtail on a `ringtail_boom` run out on the driver boom, and the
   save-alls.
10. **Groups and aliases** (`:2303-2424`): the period's words, and the groups the engine reads (§1.4).
11. **The tail, always in this order**: `ground_tackle_for(b, burthen, beam_ft, draught_ft)` (`:2425`),
    `frigate_crew(b)` (crew, people, spare spars, sail room), `frigate_armament(b, deck_height)`
    (armament, quarter bill), `hold_for` (`:2428`), `b.pumps(PUMPS_NOTE, pump_entries(2, 2, names))`
    (`:2429`), `b.boats(BOATS_NOTE, boat_entries(gundeck_ft, True, allowance))` (`:2442`), and
    `b.dump(path, header)` (`:2496-2507`).

The other ships follow the same skeleton.

| File | Function | `Builder` at | Crew | Armament | Tail | Notes |
|---|---|---|---|---|---|---|
| frigate-36 | `frigate` 1516-2507 | 1535 | `frigate_crew` 4442 | `frigate_armament` 3819 | 2425-2507 | no `descriptions` |
| topsail-schooner | `schooner` 2535-3321 | 2572 | `schooner_crew` 4663 | none | 3283-3321 | no `descriptions` |
| privateer-schooner | `schooner(armed=True)` | 2572 | `schooner_crew` | `schooner_armament` 4139, called at 3285-3286 | `privateer_schooner` 4103-4136, called at 3307-3309 | §3.2 |
| cutter | `cutter` 4898-5613 | 4931 | `cutter_crew` 5616 | `cutter_armament` 3985 | 5571-5613 | no `descriptions` |
| brig | `brig` 5798-6646 | 5826 | `brig_crew` 6823 | `brig_armament` 4289 | 6568-6646 | `descriptions` 6614 (two) |
| merchant-brig | `brig(merchant=True)`, which branches at 6569-6571 to `merchant_brig` 6649-6714 | 5826 | `merchant_brig_crew` 6717 | `merchant_brig_armament` 4372 | 6666-6714 | name and era notes rewritten in `b.doc` |
| lugger | `lugger` 7045-7636 | 7065 | `lugger_crew` 7649 | none | 7583-7636, `gear` 7597 | `descriptions` 7571 |
| smack | `smack` 7821-8398 | 7843 | `smack_crew` 8401 | none | 8321-8398, `gear` 8349 | `hold.well_m3` written into `b.doc` at 8324-8325 |

### 1.4 Groups the engine reads by name (measured with grep in `freesail/`)

- "plain sail": `world/ships.py` (the polar), `world/captains.py`, `world/crews.py`, `orders/verbs.py`
  and `agents/tools.py`.
- "topsails": evolutions, orders and captains.
- "courses": `orders/storm.py`, captains and crews.
- "headsails": `orders/storm.py`.
- "jibs": evolutions, navigation, storm and captains.
- "gaff sails": captains.
- "storm canvas": `ship/parts.py`, storm and captains.
- "storm staysails": storm and captains.
- "lying-to staysails": evolutions and storm.
- "occasional sails": `ship/parts.py`.
- "all sail": verbs and tools.

A new ship without these groups loses the behaviour that reads them. Without "plain sail" in
particular, she has no far polar (judgement on `ships.py:364-372` and `:424`).

### 1.5 How a file is written, and how byte identity holds

`dump` (`:933-1078`) runs `whole_ship_groups()` and `rate_spars()`, then
`yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)` (`:936`). A sail's `corners_m`
is collapsed onto one line by a regex keyed to the two-space indent of a sail item (`:938-950`). Then
one pass over the lines inserts the comments:

- `# note` above `- id: X` (spars, sails, lines) from `notes` (`:1069-1071`). This is skipped inside
  boats, gear and pumps.
- Above a two-space key under `hull:` from `hull_notes` (`:1072-1074`). Only top-level hull keys get
  notes.
- Inside `crew:`: posts, people, sail-room kinds, top keys, `spare_spars` classes, `trimmers`
  stations and second-level keys (`:1049-1068`).
- Inside `armament:`: the section, each fit name matched by `^    ([^ :][^:]*):$`, each gun matched by
  `^      - id: (\S+)$`, and the magazine keys `cartridges|charges|powder_barrels|exercise_charges`
  (`:974-996`).
- `ground_tackle`, `hold`, `boats`, `gear` and `pumps` get their own section and item notes
  (`:997-1048`).

The file is written with `newline="\n"` and `encoding="utf-8"` (`:1076-1078`), as
`header + body + "\n"`. The header is each ship's own literal string (for example `:2498-2506`), and
must contain "Generated by tools/gen_ships.py" (`tests/test_fishing.py:99` reads it for the smack).
Byte identity therefore rests on four things: the call order, the float formatting of the values
(rounded by the caller; `broadside_pair` rounds `x_m` and `height_m` to 0.1 at `:3722-3723`), the
notes' text, and the rating pass. Nothing hashes the files. The guard is the text comparison in
§5.1. The LF rule is also tested for every `.yaml` under `data/` (`tests/test_ship_loader.py:432-455`).

### 1.6 Variants

- **The privateer schooner**: `schooner(out, armed=True)` builds Speedwell in full. It adds
  `schooner_armament(b)` after the crew (`:3285-3286`), then hands off to `privateer_schooner(b, out)`
  (`:3307-3309`), which rewrites `era_notes`, adds `descriptions` and dumps to
  `privateer-schooner.yaml` with its own header (`:4103-4136`).
- **The merchant brig**: `brig(out, merchant=True)` builds the Harpy's hull, rig and ground tackle,
  then branches before the crew (`:6568-6571`) to `merchant_brig` (`:6649-6714`), which renames the
  ship, rewrites the era notes and writes its own crew, armament, hold, pumps, boats and descriptions.
- Each variant is a **second full build**. `dump` mutates `doc`: the ratings become floats and the
  notes gain "Rating: ...". So a Builder is not dumped twice. The precedent for "the razee derived
  from the 64" is therefore a flag on one function, branching before the parts that differ
  (judgement). `DesignLoad.__reduce__` (`:430-431`) lets a `copy.deepcopy(b.doc)` survive (it is
  used at `:851`), but no ship copies a Builder today.

### 1.7 Guns, fits and the quarter bill (packages 70, 72-73 practice, 86)

- **Fits** (70): `b.armament(note, default, [(name, source, guns, magazine, note), ...])` (`:772`).
  The scenario chooses a fit by name (§4.3). Each fit carries its own magazine. Fit names are
  free words; the existing ones are "amazon class 1795", "carronades", "long guns", "long tom",
  "letter of marque", "diligence class 1796" and "merchant".
- **Gun helpers**, each returning `[(mapping, note)]` with the note on the first gun only:
  - `broadside_pair(number, kind, pounder, cwt, x_m, height_m, note)` (`:3709-3727`) gives
    `gun.{n}.starboard` and `gun.{n}.larboard`, with `place: broadside`, `number`, `side`,
    `crew = gun_crew(kind, cwt)` and `weight_cwt`.
  - `chasers(place, ...)` (`:3730-3746`) gives `chaser.{bow|stern}.{side}`.
  - `pivot_gun(kind, pounder, cwt, x_m, height_m, arc_deg, note)` (`:3749-3765`) gives id `pivot`,
    `place: pivot`, no side, and `arc_deg: [from, to]` degrees off the bow over either side. Package
    86 made the arc per gun: the schema reads it at `schema.py:1033-1056`, `combat/guns.py:130-152`
    uses it, and `ARC_PIVOT_FROM_DEG`/`ARC_PIVOT_TO_DEG` 60/140 remain the fallback at `:140-141`.
    One pivot a fit, since the id is fixed.
  - `swivels(count, xs_m, height_m, note)` (`:3768-3790`) gives `swivel.{n}.{side}`, `place: rail`,
    crew 1 and `SWIVEL_CWT` 0.5.
  - `spaced(fore_m, aft_m, n)` (`:3793-3798`) gives n positions, forward positive.
- **`gun_crew(kind, cwt)`** (`:3591-3596`): a long gun gets 2 + round(cwt/5); a carronade 3 +
  round(cwt/8); a swivel 1. It is a judgement reading of Douglas, and D31(c) and the 74 answer
  replace it "by the period sources" for the razee and the 74. The merchant brig overrides it in
  place (`g["crew"] = 4`, `:4396-4397`).
- **Weights**: `LONG_GUN_CWT`, `CARRONADE_CWT` and `SWIVEL_CWT` (`:3577-3579`). All are from
  memory and marked UNVERIFIED. The gaps are listed in §0 item 8.
- **Rounds**: `KINGS_ROUNDS` 60/6/6, `HIRED_ROUNDS` 40/6/4, `MERCHANT_ROUNDS` 20/4, `SWIVEL_ROUNDS` 40
  and `BLANK_SHARE` 0.1 (`:3606-3610`).
- **`fit_magazine(guns, rounds_by_kind, exercise_charges=0)`** (`:3618-3653`) returns the keys in
  the file's order: `cartridges{kind:{pounder:n}}`, `charges{kind:{pounder:lb}}` (from
  `ship/parts.py:596` `charge_lb`), `powder_barrels`
  (ceil(`RESERVE_SHARE` 0.5 × filled lb / `BARREL_LB` 100), `parts.py:574`, `:586`),
  `exercise_charges` (only when above 0) and `shot{pounder:{kind:n}}`.
- **`exercise_allowance(upper_deck_guns)`** (`:3656-3662`) is `// 4`, for King's fits only.
  `filling_party(guns)` (`:3665-3669`) is max(1, non-swivel guns // 4), after Falconer's
  QUARTER-GUNNER (folded in by 86).
- **`PORT_SILL_M = 0.6`** (`:3615`): a gun's `height_m` is the deck height plus 0.6, the "sill
  above the water upright", in every King's file. The privateer alone uses a sourced sill (Spider's
  3 ft 5 in, `:4153-4155`).
- **The quarter bill** (`:799-839`): trimmers by station (validated not to exceed the station,
  `schema.py:1672-1679`), helm, powder, `filling` (86's fold-in, written after powder with
  `FILLING_NOTE`), priority ("sail before guns" or "guns before sail"), and `small_arms` and
  `boarders` (73). Every armed file passes `filling=filling_party(<the default fit's guns>)`.
  With no `quarter_bill`, `crew/quarters.py` reckons one from its defaults (helm 2, powder 0,
  `:111-112`, `:160-198`). The gun crews are drawn per `pair_key` in `_gun_order` (broadside and
  pivot first, from forward; `quarters.py:432-434`), and from preferred stations by place
  (`:437-`).

### 1.8 Ground tackle, boats, pumps, hold, stores, wardroom

- `ground_tackle_for(b, burthen, beam_ft, draught_ft)` (`:494-565`): bower cwt = 5 × burthen/100;
  the cable is half an inch per foot of beam; the sheet and stream come at 200 tons and over; the
  kedge is an eighth of the bower. It is called by every ship (`:2425`, `:3283`, `:5571`, `:6568`,
  `:7583`, `:8321`).
- `boat_entries(length_ft, ship_of_war, allowance)` (`:3378-3393`): the launch is 2.6√length (×0.8
  for a non-ship-of-war). Each entry is `(id, kind, name, of_launch, note)`. Oars are one a thwart per
  3 ft, the crew is oars + 1, and the tons follow Luce's weight rule. `BOAT_KINDS` are at
  `schema.py:687`.
- `pump_entries(chain, hand, names)` (`:3437-3472`): pumps `pump.chain.{n}` (80 t/h, 4 hands) and
  `pump.hand.{n}` (15 t/h, 2 hands). The frigate has 2+2, the brig 1+2, the schooner, privateer,
  cutter and merchant brig 0+2, and the lugger and smack 0+1.
- `hold_for(b, burthen, ship_of_war, note)` (`:3367-3375`): 0.1 of the burthen for a ship of war and
  0.5 for a trader.
- Stores are written through `b.crew` paths: `water_tons`, `provisions_days`, `spare_spars` (then
  `b.spare_spars`), `cordage_fathoms` and `shot_plugs` (73, with `SHOT_PLUGS_NOTE`). The sail room
  comes through `b.sail_room`, and the ration through `ration_entries(whose)` (`:3535-3554`; table
  `navy`, a gallon).
- `wardroom(stem)` (`:3507-3525`) reads `data/people/<stem>.yaml` and returns the posts (entries with
  `post`) and the drawn roles (entries with `drawn: {station, rating}`). The module constants are at
  `:3528-3532`, `:7027` and `:7818`. `tests/test_wardroom.py:42-57` proves the file and the wardroom
  agree, for the four first files (`:19-24`).

### 1.9 The marines and their kit (package 73)

- **The detachment** is `crew.stations.marines` (frigate 40, `:4484-4488`; brig 20, `:6852-6856`).
  The other six files have none. The marines count in the complement (§2.4). The officer and the
  sergeant are `crew.people` entries drawn `{station: marines, rating: marine}` from the wardroom file
  (`data/people/frigate-36.yaml:207-234`, `data/people/brig.yaml:122-134`). `rating: marine` is
  allowed by `PERSON_RATINGS` (`schema.py:294`).
- **The kit** is the nation's. `data/nations.yaml` gives `marines: {kit: british}` (britain, `:48`)
  and `{kit: french}` (france, `:84`). Spain (`:122`), the Batavian Republic (`:156`), the United
  States (`:189`), Portugal (`:224`), Denmark (`:257`) and Morocco (`:295`) have `{kit: basic}`. The
  kits themselves are in `data/marines.yaml` (`kits:` british, french, basic, and `small_arms:` the
  company's arms). The lookup is `Nations.marines_kit_of` (`freesail/world/nations.py:149-158`).
  The readers are `combat/small_arms.py:1-12` and `:134-146` (`marines_of`: the quarters' marines
  division, else the station's fit men) and `combat/boarding.py`.
- **At quarters**, `crew/quarters.py:116-150` sends the marines to their muskets from the
  carronades and back again.
- The generator writes nothing of the kit. A ship of a new nation, such as the Neufchatel under
  United States colours, takes the basic kit unless `data/nations.yaml` says otherwise.

### 1.10 The entry point, and where `tools/ships/` would hook in

`tools/gen_ships.py:8479-8490` takes `out = sys.argv[1]` (else `data/ships`), runs `os.makedirs`, then
calls `frigate(out)`, `schooner(out)`, `schooner(out, armed=True)`, `cutter(out)`, `brig(out)`,
`brig(out, merchant=True)`, `lugger(out)` and `smack(out)`, and prints "written to ..." to stderr.
The byte-identity test runs exactly this (`sys.executable tools/gen_ships.py <tmp>`, cwd the root).

The plan's per-ship modules (`Plan-ShipsWorkflow.md:111-114`) would be called after `smack(out)`
(judgement). These facts bear on the import:

- When run as a script, `sys.path[0]` is `tools/`, so `import ships.indefatigable` resolves to
  `tools/ships/` (a namespace package needs no `__init__.py`). `REPO_ROOT` is also on `sys.path`
  (`:122-125`), so `tools.ships.x` resolves too. No other top-level `ships` or `tools` module exists
  on the path (measured with `find_spec`). `freesail.agents.tools` is a submodule and does not collide.
- The script runs as `__main__`. A module that does `from gen_ships import Builder, design_kn` loads
  a **second copy** of the generator as module `gen_ships`. It imports cleanly, in 0.16 s here
  (measured), and reruns the module-level `wardroom()` reads. That is harmless
  only if the module takes **all** of `Builder`, `design_kn` and `DesignLoad` from the same copy.
  `rate_spars` tests `isinstance(rating, DesignLoad)` (`:853`, `:883`). A `DesignLoad` from the other
  copy would skip the rating and reach `yaml.safe_dump` as a float subclass, which SafeDumper
  refuses (judgement). Either pass the generator's namespace in (`build(out, g)`), or have
  `__main__` import itself as `gen_ships` first. The choice is the build document's.
- Each module needs its own wardroom file, its own canvas and rope tables (or the frigate's, scaled),
  and its own header. It must also be added to the test's list (§5.1).

## 2. `freesail/ship/schema.py` (1,978 lines)

### 2.1 What a file may carry (`parse_ship`, `:741-787`)

`ship.name` is required. Also read are `ship.rig` (default "unspecified"; display only, at
`api/queries.py:391` and `client/app.js:125`) and `ship.era_notes`. `ship.descriptions` is **not**
parsed here; `world/ships.file_descriptions` reads it from the YAML. The other sections are:

- `hull` (required)
- `spars`, `sails`, `lines`, `groups`, `aliases`
- `crew`, `ground_tackle`, `hold`, `boats`, `gear`, `armament` and `pumps`, each optional, with None
  or an empty list when absent

There is no `masts` key: a mast is a spar of class `mast`. Unknown keys are dropped silently at the
top level, in the hull, a spar, a sail and a line (measured; §0 item 4).

### 2.2 The hull and the conventions

`HullSpec` (`:345-356`): `length_waterline_m`, `beam_m`, `draught_m`, `displacement_kg`, `gm_m`
(all required), plus `clr_x_m` 0, `lateral_area_m2`, `hull_speed_kn`, `deck_height_m` 1.5 and
`rudder` (`RudderSpec` `:334-342`: `area_m2` 2.0, `max_angle_deg` 35, `rate_deg_s` 4.0, `span_m`).
These are parsed at `:1245-1267`, and unknown keys are ignored.

Conventions (`docs/TechnicalSpec-M0-M2.md:195-255`, and the frigate's code):

- `x_m` is forward of midships, positive.
- `deck_height_m` is the freeboard at midships.
- A mast's `height_m` is its head above the deck. A stepped mast's `height_m` is its hoist above the
  cap below. A yard's `height_m` is above the deck. Compare `frigate-36.yaml:45-99` with
  `gen_ships.py:1609-1614`.
- A sail's `centre_height_m` is above the waterline.
- A sail's `corners_m` is `[x, height above the deck]` (`:410-415`).
- A gun's `height_m` is its sill or muzzle above the water upright (`:538-548`).

### 2.3 Spars and sails

- `SPAR_CLASSES` (`:68-86`): mast, topmast, topgallant_mast, royal_mast, bowsprit, jib_boom,
  flying_jib_boom, yard, gaff, boom, studdingsail_boom, lug_yard, **lateen_yard** (`:82`) and sprit.
  `ROOT_SPAR_CLASSES` are mast and bowsprit (`:88`). `YARD_LIKE_CLASSES` are yard, lug_yard and
  **lateen_yard** (`:91`); braces are allowed only on these (`:1608-1612`).
- `SAIL_CLASSES` (`:93`): square, gaff, jibheaded, lug, **lateen**, sprit and studding.
  - Required roles (`:96-106`): square needs `yard`→yard; gaff needs `mast` and `gaff`; lug needs
    `yard`→lug_yard; **lateen needs `yard`→lateen_yard** (`:102`); sprit needs `mast` and `sprit`;
    studding needs `boom`→studdingsail_boom|boom.
  - Optional roles (`:107-116`): gaff `boom`; jibheaded `stay`|`mast`|`halyard_spar`; lug `mast`;
    **lateen `mast`→mast** (`:115`); studding `yard`.
  - `DEFAULT_SPAR_RATING_KN["lateen_yard"] = 60.0` (`:246`).
  - No file uses lateen or sprit (measured). The class exists only in the schema and the curves.
- `SparSpec` (`:359-389`) adds `x_m`, `height_m`, `length_m`, `on`|`steps_on`, `side`,
  `brace_limit_deg`, `rake_deg` (masts only, within ±30, `:1524-1533`), `rating_kn`, `rigged_out`
  (studding boom or running bowsprit), `running` and `housed_length_m` (bowsprit, 32b), and
  `horse_m` (32e).
- `SailSpec` (`:392-425`) adds `area_m2`, `x_m` and `centre_height_m` (required), `reef_bands`,
  `side`, roles, `cloth_rating_kn`, `canvas_no` 1-9, `bent`, `in_place_of`, `dipping` (lug only),
  `flying` (never with reefs), `sheeted_to` (lug only) and `corners_m` (3 or 4 pairs).
- `LINE_CLASSES` (`:119-140`) and `LINE_TARGET_KINDS` (`:145-165`): a stay, shroud or backstay is
  `of` a spar. A jibheaded sail's `stay` must name a standing line (`:1699-1705`).

### 2.4 The crew section (`_parse_crew`, `:1788-1956`)

- Allowed keys (`:1792-1806`): complement, names, stations, ratings, posts, idlers_by_trade, stores,
  people (35), ration (54) and quarter_bill (70). Anything else is refused.
- `CREW_STATIONS` (`:278-287`): forecastle, fore_top, main_top, mizzen_top, afterguard, waisters,
  marines and idlers. The first six are seamen. There is no deck station; a 74 has the same eight.
- The ratings are able, ordinary and landsman, and must sum to 1.
- **stations + len(posts) == complement**, or the file is refused (`:1866-1872`).
- `idlers_by_trade` must sum to `stations.idlers` (`:1880-1884`). The trades are `IDLER_TRADES`
  (`:298-309`).
- `STORE_KEYS` (`:312-320`) include `shot_plugs` (73). A sail-room entry is
  `{kind, canvas_no, condition}`, and its `kind` must be a sail of the ship (`:1639-1646`).
- `people` entries: role, station, rating (`PERSON_RATINGS`), messenger.
- `QUARTER_BILL_KEYS` (`:229`): trimmers, helm, powder, priority, **small_arms**, **boarders**
  (both 73) and **filling** (practice and resupply, folded in by 86). `PRIORITIES` (`:230`). The
  dataclass is at `:495-515`. `filling: None` means it is reckoned from the guns (`combat/filling.py:66`).

### 2.5 The armament (`:825-1056`)

- `ARMAMENT_KEYS` are default and fits (`:224`). `default` must be one of the fits.
  `ArmamentSpec.fit(name)` (`:590-596`) refuses an unknown name in words.
- `FIT_KEYS` (`:215-223`): source, guns, cartridges, charges, powder_barrels, exercise_charges and
  shot. Anything else is refused, so "a rear-admiral's flag as a fit" is not a fit key.
- `cartridges` and `charges` are keyed by kind then calibre. Cartridges keyed by calibre alone are
  still accepted where one kind has the calibre (`:868-890`, `:939-965`). Every calibre in the
  magazine must belong to a gun of the fit.
- `GUN_KEYS` (`:202-214`): id, kind, pounder, place, number, side, x_m, height_m, crew, weight_cwt
  and arc_deg.
  - `GUN_KINDS` are long, carronade and swivel. `GUN_PLACES` are broadside, bow, stern, rail and
    pivot (`:199-200`).
  - A broadside gun needs a number and a side. A pivot gun has no side. Only a pivot gun takes
    `arc_deg` (0 ≤ from < to ≤ 180).
- `GunSpec` (`:538-560`) and `FitSpec` (`:563-580`).
- `validate` (`:1648-1670`): a gun's id must not be any part's id, must be unique in its fit, and
  `(number, side)` must be unique in the fit.

### 2.6 What `validate` refuses (`:1488-1679`)

- Duplicate ids across spars, sails and lines.
- A spar with both `on` and `steps_on`, or a non-root spar with neither, or an unknown parent, or a
  cycle.
- A studding boom without a side, unless it stands on a boom or gaff.
- `rake_deg` on a non-mast, or beyond ±30.
- Sail role rules (required, optional and unknown roles; the spar class of each role).
- A studding sail without a side.
- `sheeted_to` that is not another lug. `in_place_of` that is not another sail.
- A jibheaded sail with neither a stay nor a mast.
- A line `of` an unknown part or the wrong kind; a brace on a non-yard.
- A group member that is not a part; a group or alias named as a part; an alias pointing nowhere.
- A sail-room kind that is not a sail.
- The gun rules above.
- Trimmers exceeding their station.

Missing ratings are filled from the defaults, with a warning.

### 2.7 Where a hull profile would go (no key exists)

The data path is five places, all read:

1. `HullSpec` (`schema.py:345-356`) and `_parse_hull` (`:1245-1267`), with a new optional field.
   Without it the key is dropped silently (measured).
2. The generator's hull dict in each `Builder(...)` call (for example `gen_ships.py:1542-1553`),
   with its note in `hull_notes` (one note above the key; `dump` notes only two-space hull keys,
   `:1072-1074`).
3. `freesail/api/queries.py:380-406` `ship_graph`, whose `hull` dict lists the seven principal
   figures by name. A profile must be added there to reach the viewer.
4. `client/projection.js:1413-1445` `hullFigures(hull)`: today a generic lens deck from L, B and
   `deck_height_m` with a fixed sheer (`z = F*(1 + 0.12t² + 0.1t)`, 14 stations, the bow at +0.06L,
   the stern at −0.02L, the sides to −0.8 m). It feeds `buildSkeleton` (`:273-`) and
   `client/shipview.js:58-60`.
5. The tests that read the drawing: `tests/test_view_geometry.py` (`:446-470`, the cutter's hull
   ends; `:630`, `:778` deck heights) and `tests/test_pictures.py`.

PyYAML lays a nested list under `hull` out as `    sheer_m:\n    - - -20.0\n      - 2.1` (measured).
The `corners_m` one-line regex (`gen_ships.py:938-950`) does not match it. A profile written as
pairs needs its own collapsing regex, or the multi-line form accepted as it is (judgement). The
same profile gives the lee-port sill and half-breadth (the owner's rule, Bel §13), through
`lee_port_shut` (`combat/shot.py:116`), which is not yet called.

## 3. `data/ships/*.yaml` (all measured from the files)

### 3.1 The eight files

| File (lines) | Ship, rig | Hull: LWL × beam × draught (m), displacement, deck | Masts at `x_m` (rake) | Spars / sails / lines | Company (marines) | Fits (default first) | Quarter bill (trimmers; helm, powder, filling; small arms, boarders) | Other |
|---|---|---|---|---|---|---|---|---|
| frigate-36 (3,094) | Amazon, ship | 41.8 × 11.7 × 4.6, 1,270 t, 1.8 | fore 14.0 (1.5), main −2.0 (2.5), mizzen −16.0 (4.5) | 40 / 38 (6 unbent) / 268 | 264 (40) | "amazon class 1795": 26 long 18 at 2.4; 10 carr 32, 2 long 9 broadside and 2 long 9 bow, all at 4.5 | fc 8, ft 10, mt 12, mzt 6, ag 8; 2, 0, 10; 20, 60 | QD INCORRECT against Winfield p. 143, kept by the owner's ruling (`gen_ships.py:3819-3834`); exercise 6, 77 barrels; 5 anchors (2,370 kg, 19 in); 6 boats; pumps 2+2 |
| topsail-schooner (948) | Speedwell, topsail-schooner | 25.9 × 7.3 × 3.3, 211 t, 0.9 | fore 7.8, main −2.6 (both 11.3) | 15 / 14 (4) / 85 | 40 (0) | none | none | 5 anchors (570 kg); long-boat and yawl; no `descriptions` |
| privateer-schooner (1,228) | Speedwell, topsail-schooner | as the schooner | as the schooner | as the schooner | 40 (0) | "long tom": long 12 pivot at 1.7, arc [60, 140]; 4 carr 12 at 1.0; 4 swivels at 1.7. "letter of marque": 6 long 6 at 1.0; 4 swivels | fc 4, ft 3, ag 4; 1, 2, 1; 8, 26 | §3.2 |
| cutter (1,049) | Sherbourne, cutter | 15.2 × 5.8 × 2.6, 106 t, 0.9 | main 1.5 (5.2); running bowsprit | 9 / 9 (2) / 70 | 30 (0) | "carronades": 6 carr 12 at 1.5 (exercise 1). "long guns": 6 long 3 at 1.5; 8 swivels at 1.7 | fc 4, ag 4; 1, 2, 1; 6, 20 | 3 anchors; boat and punt; pumps 0+2 |
| brig (2,242) | Harpy, brig | 26.8 × 8.6 × 3.5, 413 t, 1.5 | fore 8.9 (1.2), main −3.9 (4.0) | 31 / 29 (3) / 200 | 121 (20) | "diligence class 1796": 16 carr 32 broadside, 2 long 6 bow, all at 2.1 | fc 6, ft 6, mt 7, ag 8; 2, 0, 4; 8, 30 | `descriptions`: brig-sloop and merchant brig; 5 anchors (800 kg); pumps 1+2 |
| merchant-brig (2,016) | Industry, brig | as the brig | as the brig | as the brig | 16 (0), `names: american` | "merchant": 4 long 6 at 2.1, crew 4 by override | ft 1, mt 1; 1, 0, 1; 2, 6 | hold 158 t; long-boat and jolly boat |
| lugger (681) | Éclair, lugger | 16.8 × 6.2 × 2.1, 101 t, 1.0 | fore 6.6, main −0.7, `mizen` −8.7 (9.5) | 11 (5 `lug_yard`) / 9 (6 lug, 2 unbent) / 52 | 30 (0), `names: french` | none | none | gear: drift nets and lines; `mizen.*` ids, where the frigate has `mizzen.*` |
| smack (627) | Culloden, smack | 12.2 × 4.3 × 1.9, 46 t, 0.75 | main 1.8 (2.4) | 6 / 7 (2) / 53 | 8 (0) | none | none | `hold.well_m3` 9.1; gear: trawl, lines and seine |

Every file carries `ground_tackle` (hemp, `chain: false`), `crew` with a ration (navy, 1 gal) and
stores including `shot_plugs`, `hold`, `pumps` and `boats`. The id patterns, read from the frigate:

- Masts: `fore.mast`, `fore.topmast`, `fore.topgallant_mast`, `fore.royal_mast`.
- Yards: `fore.yard` (the lower), `fore.{topsail|topgallant|royal}.yard`, `mizzen.crossjack.yard`.
- The mizzen's spars: `mizzen.gaff`, `mizzen.boom`.
- The head: `bowsprit`, `jib_boom`, `flying_jib_boom`.
- Sails: `fore.course`, `fore.topsail`, ..., `mizzen.spanker`, `jib`, `flying_jib`,
  `fore.topmast_staysail`, `main.staysail`, `middle_staysail`, and
  `fore.topmast.studdingsail.starboard`.
- Lines: `{yard}.brace.{side}`, `{sail}.sheet.{side}`, `{mast}.shrouds.{side}`, `main.stay`,
  `bobstay`, `martingale`.

### 3.2 `privateer-schooner.yaml`

The file is PROVISIONAL: "the owner's ask of 2026-10-25, ahead of package 75". Package 86 folded
in the per-gun pivot arc and the filling party. The file is Speedwell's hull, rig, company and boats
**exactly**, plus `armament`, `crew.quarter_bill`, new `era_notes` and `ship.descriptions` with one
key, "privateer schooner". `tests/test_ships.py:146-158` proves that equality by popping those four
and comparing the documents. It is made by `schooner(out, armed=True)`, then `schooner_armament`
(`gen_ships.py:4139-4286`; the default fit is "long tom", whose arc comes from the owner's ruling and
`docs/design/Proposal-PivotGun.md` §3), then `privateer_schooner` (`:4103-4136`). It has no wardroom
file of its own. In the index it is the `DESCRIPTIONS` key "privateer schooner" (`world/ships.py:174-180`)
with `SIZE_RANK` 1. The brief (item 5) wants its arc sourced and its fits from the type's records.
The Neufchatel is a different, new file.

### 3.3 Gun heights and the heel at which a lee port would shut (measured)

The heel solves `height_m − (beam/2)·sin(heel) = 0.3048` (`PORT_SHUT_M`, `shot.py:65`):

- frigate: upper deck 18s at 2.4 m shut at 21.0°; quarterdeck and forecastle at 4.5 m at 45.8°.
- brig and merchant brig, at 2.1 m: 24.7°.
- cutter: the guns at 1.5 m at 24.3°; the swivels at 1.7 m at 28.8°.
- privateer: carronades and long 6s at 1.0 m at 11.0° (the generator's comment says "about 12",
  `:4153-4155`); the pivot and swivels at 1.7 m at 22.5°.

Today's heights are the deck plus `PORT_SILL_M` (judgement, `:3612-3615`), except the privateer's.
Wiring the lee ports moves nothing until `lee_port_shut` is called. Once it is, every armed file's
heights become the inputs whose combat pins may move (the brief: old beside new, proof by bisection).

## 4. The world's side

### 4.1 `freesail/world/ships.py` (1,826 lines)

- `DESCRIPTIONS` (`:163-204`), keyed by description, each `{file, rig, what}`: frigate,
  schooner, privateer schooner, cutter, brig-sloop, merchant brig (both point at `brig.yaml`),
  lugger and smack. `_DESCRIPTION_WORDS` (`:205-242`) maps the lookout's or a scenario's words to a
  key. `description_key` (`:244-264`) tries the exact key, then the words, then the longest tail.
- `file_descriptions(ship_file)` (`:266-279`, cache 8) reads `ship.descriptions` from the YAML.
  `description(key)` (`:286-295`) lets the file's own `rig` and `what` override the index.
- `SHADOW_FILES` (`:283`): a player's file that no description sails ("merchant-brig.yaml").
  `Vessels.player_shadow` (`:1445-1508`) finds the player's description by file name. A file with
  none and no shadow entry is "a ship" (`:1473`).
- `rig_height_m` (`:297-308`) gives the horizon from the masthead. `_rigged_for_plain_sail`
  (`:364-372`) and `polar_of` (`:423-450`, cache 8) draw the far polar.
- `Vessel` (`:452-`): `kind` is the rig word, plus `ship_file`, `description`, `what` and `fit`
  (`:520-524`, "" for the default). `vessel_from_spec` (`:1126-1190`) builds one from a scenario's
  `ships:` entry. `fit` is read at `:1184`.
- `_size_of(v)` (`:1789-1797`) reads `SIZE_RANK` by description, or else by file.

### 4.2 `freesail/world/captains.py` (4,313 lines) and `data/captains/`

- `ROLES` (`:133-141`): kings-ship, merchant, packet, commodore, cruiser, fisherman, privateer.
  `INTENT_KINDS` (`:145`). `MAN_OF_WAR_WORDS` (`:190-198`) already include "ship of the line".
- `SIZE_RANK` (`:286-295`): frigate 3; brig-sloop and merchant brig 2; schooner, privateer
  schooner, cutter and lugger 1; smack 0. `_SIZE_WORDS` (`:296-305`) is ordered, with "a ship" at 3.
- `size_of_words` (`:308`), `size_rank_of` (`:318`), and `size_of_file` (`:334`, the player's class
  by her file through `DESCRIPTIONS`; used at `:1497`). Also `brains.py:93`.
- `load_doctrine(role)` (`:904-911`) reads `data/captains/<role>.yaml`. `role_for` (`:914-926`):
  a station intent gives privateer if it is for prizes, else kings-ship; a letter gives packet; a
  convoy gives commodore; home, passage or free gives kings-ship if `_is_kings_ship`; otherwise
  merchant. `_is_kings_ship` (`:929-`) reads the wardroom file's binding of the captain's station
  through `world.ship.spec.source`.
- `data/captains/` holds the seven role files: commodore (261 lines), cruiser (264), fisherman (132),
  kings-ship (290), merchant (264, whose head documents the form), packet (238) and privateer (297).
  It also holds `hail.yaml` (163), which is the hail's tables read by `freesail/world/hail.py`, not
  a role. The brief's sub-types (the armed Indiaman, the revenue and hired cutters, the packet) are
  fits plus roles. A new role needs a file here **and** an entry in `ROLES`.

### 4.3 How a scenario names a file and a fit

- The player's ship: `ship: {file: data/ships/<f>.yaml, fit: <name>}` (`world/scenarios.py:19-24`,
  `:328-331`, `:699`). `Scenario.fit` is at `core/world.py:240-244`, and it is None for the file's
  default. `Ship(spec, fit)` (`ship/graph.py:30-45`) calls `ArmamentSpec.fit(fit)`, and the guns come
  from that fit. `load_ship(path, fit)` is at `ship/loader.py:37`.
- Another sail: `ships: [{id, description, name, nation, fit, position, goal, intent, colours}]`,
  for example `data/scenarios/first-action.yaml:63-66`. Its file comes from the description (§0
  item 12). The fit is carried on `Vessel.fit` into the far fight (`combat/far.py:98-103`) and the
  crewed action (`combat/action.py:466`).
- In use (measured): `fit: carronades` in `first-action.yaml:41` and `leak.yaml:35`, and
  `fit: long guns` for the Renard (`first-action.yaml:64`). Scenarios name these files: frigate 20,
  topsail-schooner 10, cutter 6, brig 2, merchant-brig 1, lugger 1 and smack 1. The privateer
  schooner sails as a description (`convoy-six.yaml`).

## 5. The tests that pin ship files

### 5.1 `tests/test_ship_particulars.py` (593 lines)

- Fixtures by file (`:28-73`).
- Particulars are written as **bands with the source in a comment**. For example
  `test_frigate_hull_is_an_amazon_class_frigate` (`:93-104`):
  `assert 11.4 <= h.beam_m <= 12.0  # 38 ft 4 in extreme breadth`.
- Per ship:
  - the frigate's hull, sail area, spars, centres, ratings and head stays (`:93-217`);
  - the schooner (`:220-269`), the cutter (`:272-327`), the brig (`:330-381`), the lugger
    (`:384-441`) and the smack (`:444-544`).
- `test_period_names_resolve` (parametrized by file, `:475-552`).
- **`test_generator_reproduces_the_committed_files`** (`:555-581`). The file list is at `:565-574`.
- The path test (`:584-593`).

### 5.2 `tests/test_ships.py` (869 lines; package 36's far vessels)

- The polar from the file against the measured beam reaches (frigate 8.0, schooner 7.9, cutter 7.3,
  brig 7.7, ±0.5; `:74-93`).
- The descriptions (`:96-104`, including the `"a ship of the line" is None` assertion at `:101`).
- The privateer is the schooner armed (`:107-158`).

The rest is goals, the lookout and steering.

### 5.3 `tests/test_known_truths.py` (10,455 lines; 198 test functions, measured)

- **The last truth at this head is 7-184**, `test_truth_7_184_the_leak_scenario_mans_the_pumps_at_a_foot_and_left_alone_loses_stiffness`,
  at `:10426`. Package 75 owns 7-185 to 7-199.
- A truth is `def test_truth_7_NNN_<the claim in words>():`. Its docstring gives the scenario, the
  source, and the figures measured at seed 7, and says where they were measured (the owner's
  machine or the build machine). Digests are recorded, not pinned (decision 26; for example 7-161 at
  `:9229-9260`).
- The ship constants are at `:90-91`, `:5046`, `:6176`, `:7897-7898` and `:9176` (`PRIVATEER`).
- The brief's truths of this kind (each ship's particulars against her sources within the test's
  bands) follow `test_ship_particulars.py`'s band form.

### 5.4 Other tests a new file meets

- `tests/test_stores.py:28` globs **every** `data/ships/*.yaml` (the ration block, `:42-70`).
- `tests/test_ship_loader.py:432-455` checks LF in every `.yaml`.
- `tests/test_wardroom.py:19-24` and `:42-57` check the wardroom against four files.
- `tests/test_anchor.py:59` is parametrized over four files.
- `tests/test_captains.py:111` runs every doctrine book on the four ships.
- `tests/test_fishing.py:99` reads the generator's header text.
- `tests/test_view_geometry.py` and `tests/test_pictures.py` cover the viewer.
- No other test runs the generator (measured with grep: the other mentions of `gen_ships` in
  `test_anchor`, `test_fishing`, `test_magazine`, `test_places`, `test_scenarios` and
  `test_view_geometry` are in words).
