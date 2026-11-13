# Design: the viewer's action, from the hull 75 draws (package 81)

The brief is `docs/dev/M7-WorkPackages.md`, "Package 81". This note is its item 1: the standard,
written before the drawing is touched, for the lead to rule on. The owner's rule binds it
(2026-11-07): **ships are added continuously, so this is a procedure, not a picture.** Every gun of
every hull is drawn by one rule from what her file already carries; a new ship is drawn at the same
standard by passing the same checker with no change of code; her builder knows from one checklist
(§9) what her file must give.

Marks as the research notes give them: **read**, the page or its image; **read (OCR)**, the OCR text
under `docs/references/` only; **read (by …)**, another session's reading, cited where it stands;
**judgement**, the design's own, named as such, with what would replace it.

## In brief

- **The data contract (§1).** A gun is drawn when her file gives a profile and the gun's place can
  be resolved from it: a port gun (broadside, bow, stern) by its deck's triple at its own x and its
  deck's `port_size_m`; a swivel on the rail at its x; a pivot on the middle line at its x. The test
  holds every shipped file to it; the viewer draws a hull that lacks it as 75 left her.
- **The one rule (§2).** A port gun stands at the triple of its deck whose x is its own within
  §5.3's 0.01 m. **The triple is a port where the side stands the port's depth above its sill, and a
  place over the rail where it does not** (taken another way from the brief's `OVER_THE_RAIL_M`:
  §2.2). Measured on the files today: 327 guns over eleven fits, every one placed, none by hand (§2.3).
- **The gun's figure (§3)** by kind and calibre from one sourced table: the length by the file's own
  `weight_cwt` against Adye's patterns (pp. 155 and 72, the page images), the bore by the shot.
- **The firing (§4)**: a flash and a plume at each gun whose count of rounds rose, stamped with the
  tick of the snapshot that first shows it (exact at 1x; §4.1), drifting on the apparent wind,
  thinning over the half minute; the recoil in a few frames.
- **The damage (§5)** as `the damage` gives it: the shot holes at their side, place and size; a gun
  dismounted; a spar gone as now. No port stove: the engine has none.
- **The animation road (§6)**: the snapshot redraws the ship; between snapshots a clock
  (`requestAnimationFrame`) draws only a layer of effects and moving guns. 91 reuses it.
- **The engine is not touched.** `action.fired` already names its guns (`data["guns"]`,
  `combat/guns.py:1115`), so item 2's one allowed touch is not needed (§7).
- **The flags (§12)**, the owner's addition to the brief: drawn at their places on the drawn spars by
  one rule of place words, from the snapshot's `flags`; until 76's `colours.yaml` lands, one plain
  ensign at the peak from the nations' table.
- **Questions for the owner's shelf (§11, §12.6)**, none holding the work: each has a judgement in place.

## 0. What stands today (read at the trunk's head, f466051)

- **The files.** Fifteen under `data/ships/`. Eight have both an armament and port triples: the
  brig, the cutter, the frigate-36, the merchant brig, the privateer schooner, the razee, the 64, and
  (triples, no armament) the topsail schooner. The lugger and the smack have profiles and no armament
  in their files; the five boats have profiles and no guns.
- **A gun** (`schema.GunSpec`, `ship/parts.py:518` `Gun`): `id`, `kind` (long, carronade, swivel),
  `pounder`, `place` (broadside, bow, stern, rail, pivot), `number`, `side`, `x_m`, `height_m` (the
  port's sill since 75's hull step, §5.3), `crew`, `weight_cwt`, `arc_deg` (a pivot's), `deck`. Its
  state as a part: `cast_loose`, `loaded`, `run_out`, `primed`, `train_deg` (set by the engine for a
  pivot only, `combat/guns.py:535`), `elevation_deg` (never set), `dismounted`, `fired` (rounds,
  monotone). Its words: `Gun.name` ("No. 3 starboard gun", "the starboard bow chaser") and
  `Gun.kind_words` ("long 18-pounder", "32-pounder carronade"), both in-world already.
- **The ports.** `hull.profile.ports_m` (one side's triples, x, sill, half-breadth, by deck) and
  `port_size_m` (width, depth, by deck); read through `ship/profile.py`. The lee ports' rule
  (`combat/ports.py`, Build-Ships.md §7) keeps the shut guns' ids in `Battery._shut`, which `the guns`
  serves as `ports_shut` (`api/action_readings.py:207`).
- **The damage.** `the damage` (`api/action_readings.py:249`) serves `holes`, each `{tick, side,
  x_m, z_m, diameter_m, pounder}` and `plugged` once plugged (`combat/hits.py:185-193`; `z_m`
  against the waterline upright, negative below), `dismounted` (gun ids), `spars` carried away.
  There is no port stove anywhere in the engine (grep: `stove` is a boat's, `hits.py:225`).
- **The viewer.** `client/projection.js` builds a skeleton from `/api/ship`'s graph and the
  snapshot, projects it (`project`), and `shipview.js` paints it; `app.js` redraws at each snapshot
  (every tick at 1x, every 10 at 10x, every 60 above: `ui/server.py:182`). The frame is the full rig
  swung as far as it swings plus the hull (`fullRigFrame`), so no state rescales the view. No gun,
  port or hole is drawn; `PORT_BANDS` draws each deck's strake from the sill up the port's depth.
- **The survey** (`tools/check_viewer_guns.py`'s first form, run in scratch on f466051): every gun of
  every fit against its deck's triples, the gap from each triple's sill to the rail at its x, and the
  port's depth. Its figures stand in §2.3.

## 1. The data contract

A hull is drawn with her guns and ports when her file gives:

| What | Where in the file | Why |
|---|---|---|
| the profile | `hull.profile` with `rail_m` and `breadth_m` (the schema's own requirement) | the side the ports are cut in, the rail a gun fires over |
| the decks | `hull.profile.decks_m`, each deck a gun stands on | the carriage's foot; a pivot's foot |
| the ports | `hull.profile.ports_m.<deck>`: a triple at every port gun's own x, x within 0.01 m | the port, by rule 2 |
| the ports' sizes | `hull.profile.port_size_m.<deck>`, for every deck with ports | the port's opening; the test of a port against the rail (§2.2) |
| the guns | `armament.fits.<fit>.guns`: each gun's `kind`, `pounder`, `place`, `side` (but a pivot), `x_m`, `weight_cwt`, and `deck` for a port gun | the figure (§3), the place (§2) |

**Taken another way from the brief's (a):** the brief asks a deck of every gun. A swivel and a pivot
have no port (`Build-Ships.md` §5.1: "A pivot and a rail gun have no port"), and no file gives them a
deck (the cutter's eight swivels, the privateer's four and her long tom: the survey). They are placed
by the rail and the deck at their x (§2.4), as §5.3 already places their heights (`rail_at`). So the
contract asks a deck of a port gun only.

**Per gun, not per hull.** A gun whose place cannot be resolved is not drawn and the checker says
why; her other guns and her ports are drawn. The viewer never draws a gun it cannot place, and a hull
whose file gives no profile is drawn exactly as 75 left her. The *test* is stricter than the viewer:
every file under `data/ships/` with an armament must place every gun (§8), so a ship added without
the contract fails until her file gives it. The viewer's leniency serves a hand-written file and the
tests' fixtures; the test's strictness is the standard.

## 2. The one rule of placing

### 2.1 A port gun (broadside, bow, stern)

1. **Its triple** is its deck's triple whose x is nearest its own, within 0.01 m (§5.3, truth
   7-185). None within 0.01 m: the gun is refused ("no port of the upper deck at 13.8 m"), a finding
   for the ships session through the lead, never placed by hand.
2. **Its port**, from the triple and its deck's `port_size_m` [w, d]: a rectangle on the drawn side,
   centred fore and aft on the triple's x, its lower edge on the sill, w wide and d deep, its edges
   parallel to the deck at that x ("The lower and upper edges of the ports are always parallel to the
   deck": Falconer 1780, PORTS, read (OCR), `falconer/…ocr.txt:13783-13789`); on the side's surface
   (the drawn half-breadth at each corner's height, from the served stations: `drawnSideAt`), on her
   side and mirrored on the other where she carries the gun's pair.
3. **A port or over the rail** (§2.2): a port where the side stands at least the port's depth above
   the sill, less `PORT_FIT_M` (0.05 m, the §5.2 tolerance a drawn side keeps to a triple); over the
   rail where it does not. A port whose depth reaches above the rail within `PORT_FIT_M` is cut to the
   rail (the 64's foremost quarterdeck port, at −5.88 m, 0.02 m; the frigate's long 9s, 0.00).
4. **In a port**, the gun's axis stands at the port's middle (sill + d/2), level (Falconer, as above:
   the guns "when levelled in their carriages, are all equally high above" the sill; the middle is
   judgement), square to the side at its x for a broadside gun; a chaser is trained toward its end by
   `CHASE_TRAIN_DEG` (30°, judgement, question 5). Its muzzle stands by its state (§3.3).
5. **Over the rail**, there is no port: the gun stands on its carriage or slide on its deck, its axis
   `RAIL_CLEAR_M` above the rail at its x beyond the muzzle's half-diameter (0.05 m, judgement), the
   same muzzle rule. The triple's sill and half-breadth still give its place across the deck.

### 2.2 Over the rail: the side's own test, not a constant from the tools

The brief has it: "a triple within `OVER_THE_RAIL_M` of the rail at its x is a gun over the rail".
`OVER_THE_RAIL_M` (0.05 m) is the 64's generator's convention (`tools/ships/indefatigable.py:241`):
on a deck "whose rail stands less than a port's sill above it" the sill is written 2 in under the
rail. Its function (`open_deck_sill`, :1163-1168) writes the lesser of the deck and 0.41 m, and the
rail less 0.05 m. So **where the rail stands only a little above the deck and 0.41 m, the sill is
written at the deck and 0.41 m, short of the rail by more than 0.05 m, and the deck still draws no
port.** The survey finds one such triple: the 64's foremost forecastle triple at 18.41 m, 0.07 m
under the rail, where the fit of 1784 carries a long 9 a side. By the constant it is a port, whose
0.69 m depth would stand 0.62 m above the rail.

The rule taken: **a triple is a port where the side stands the port's depth above its sill (within
0.05 m), and a gun's place over the rail where it does not.** It is one test of the file's own data
(the triple, the rail, the deck's port size), it holds every place `OVER_THE_RAIL_M` gives (each
0.04-0.05 m under the rail against a depth of 0.69-0.71 m), it places the 64's forecastle 9-pounder
over the rail as her sheet has it, and it needs no constant from a ship's module in the viewer or
the server. The checker names each triple it puts over the rail that is not at `OVER_THE_RAIL_M`
(today the one), for the ships session to keep or to write 2 in under the rail. **For the lead to
rule:** the brief's constant instead, under which that gun is refused and the test fails on
`sixty-four.yaml` until the ships session rewrites the triple.

### 2.3 The eight files by the rule (the survey, f466051)

| File | Fit | Guns | In a port | Over the rail | On the rail | Pivot | Refused | Empty ports a side |
|---|---|---|---|---|---|---|---|---|
| brig | diligence class 1796 | 18 | 18 | 0 | 0 | 0 | 0 | upper 1 |
| cutter | carronades | 6 | 6 | 0 | 0 | 0 | 0 | upper 4 |
| cutter | long guns | 14 | 6 | 0 | 8 (swivels) | 0 | 0 | upper 4 |
| frigate-36 | amazon class 1795 | 40 | 36 | 4 (pair 18 and the bow chasers, on the forecastle) | 0 | 0 | 0 | none |
| merchant brig | merchant | 4 | 4 | 0 | 0 | 0 | 0 | upper 8 |
| privateer schooner | long tom | 9 | 4 | 0 | 4 (swivels) | 1 | 0 | upper 6 |
| privateer schooner | letter of marque | 10 | 6 | 0 | 4 (swivels) | 0 | 0 | upper 5 |
| razee | as razeed 1795 | 44 | 44 | 0 | 0 | 0 | 0 | forecastle 1 |
| razee | as carried 1796 | 46 | 46 | 0 | 0 | 0 | 0 | none |
| sixty-four | ardent class 1784 | 64 | 62 | 2 (the forecastle 9s, §2.2) | 0 | 0 | 0 | quarterdeck 1 |
| sixty-four | ardent class 1794 | 72 | 62 | 10 (the forecastle's 24-pounder carronades and 9s, the roundhouse's six 18-pounder carronades) | 0 | 0 | 0 | quarterdeck 1 |

327 guns over eleven fits, every one placed by the rule and none refused (the prototype of the
checker, run in scratch on f466051 with `PORT_FIT_M` 0.05 m). The topsail schooner has eight triples a
side and no armament: drawn as eight empty ports a side. A triple over the rail with no gun of the fit
(the 64's roundhouse in the fit of 1784) is no port and draws nothing. The checker's own output
replaces this table in the tuning notes at item 4.

**Found on the way, for the ships session through the lead:**
- **The frigate's quarterdeck carries two sizes of port and the file one.** Her sheet has carronade
  ports of 3 ft by 2 ft 11½ in and gun ports of 2 ft 3 in by 2 ft 4 in (`pages-zaz2587.md` §7.2);
  `port_size_m` is by deck, so her file gives the gun ports' [0.69, 0.71] to the carronades too
  (`frigate-36.yaml` :75-79 and its note). Drawn at the deck's size until the schema gives a size by
  port; a key by port is the ships session's and the schema's, not this package's.
- **No port stove** exists in the engine (§5).

### 2.4 A swivel and a pivot

- **A swivel** (`place: rail`) stands on its yoke on the rail at its x and side (`rail_at`, the
  drawn rail's half-breadth there), its axis `SWIVEL_YOKE_M` above the rail (0.15 m, judgement),
  trained square to the side. It is drawn whatever its state; loaded or not shows in its words.
- **A pivot** (`place: pivot`) stands on the middle line at its x, its slide on the deck at that x
  (`deck_at`), its axis above the rail at its x by §2.1's over-the-rail height (it fires over the
  rail: `Proposal-PivotGun.md` §4.4), trained by its `train_deg` (served; nought, fore and aft, when
  secured). Its arc is not drawn.
- **Taken another way from the brief's (b):** "a chaser at the bow or the stern and a pivot gun at its
  place by the same rule on the stem's or the taffrail's line". The files give every chaser a triple
  of its deck at its own x (§5.1: "A chaser's port is a triple of its deck at the chaser's x"), in the
  side, so a chaser is placed by rule 2.1 as a broadside gun is, at its triple; the stem's and the
  taffrail's lines carry no data of a chase port. A pivot is on the middle line, not on the stem's.

### 2.5 The ports

Every triple of every deck is a port of the hull, drawn on both sides whatever the fit (a ship's
ports are cut once; the fits differ in what stands in them), except a triple over the rail (§2.2),
which is no port and draws nothing without its gun.

- **A lid** on every port (judgement, question 2: which decks had hanging lids, which half-ports),
  hinged at its upper edge (Falconer, PORTS: "hanging-doors, called the port-lids … fastened by
  hinges to their upper-edges"; Steel 1805, PORT-LIDS, `steel-1805…ocr.txt:4061`, read (OCR)).
- **Open** while its gun is cast loose and the sea is not at its sill; the lid raised outboard
  `LID_OPEN_DEG` (70° from the side, judgement, question 2). **Shut** while its gun is secured, while
  the lee ports' rule has it shut (`ports_shut`), and for an empty port (judgement: an empty port
  is kept shut). "To lee down when the cannon are drawn into the ship" (Falconer) is the rule's
  ground: a gun run in by the sea has its lid let down.
- **Drawn** as a dark opening on the side's face, sorted a hair outboard of its strip as the wales are
  (`DEPTH_TIE`), seen only from outside (`outward`); the lid a plank-coloured plate, flush when shut,
  standing out when open. `PORT_BANDS` stays.

## 3. The gun's figure by kind and calibre

### 3.1 The table

One table, in `freesail/api/viewer_guns.py` beside its sources, the figure the same for every gun of
that kind, calibre and weight on every ship. **The length is read from the file's own `weight_cwt`
against the patterns Adye prints for that calibre: the pattern of nearest weight.** So no new key is
asked of a file, and a gun of a new weight draws at its pattern's length.

| Kind, pounder | Patterns: length (ft in) at weight (cwt) | Source | Files' weights today |
|---|---|---|---|
| long 42 | 10 0 at 67; 9 6 at 65 | Adye p. 155, read here (R1) | (none) |
| long 32 | 10 0 at 58; 9 6 at 55 | Adye 1804 p. 155, IA leaf n178, read (by the ships sessions: `tools/ships/period.py:16-29`; Research-Indefatigable-2026-10.md §6.4) | (the 74, to come) |
| long 24 | 10 0 at 52; 9 6 at 49½; 9 0 at 47½ | the same | razee, 64: 49.5 |
| long 18 | 9 6 at 42; 9 0 at 40 | the same | frigate 42 (her note's "9 ft" is the comment's only: `Decisions-ShipsRound2-2026-10.md` l. 536); 64 |
| long 12 | 9 6 at 34; 9 0 at 32; 8 6 at 31½; 7 6 at 29¼ | the same | razee 34 |
| long 9 | 7 6 at 24½; 7 0 at 23 | the same | frigate, 64: 26 (from memory, `gen_ships.py:4195`) → 7 6 |
| long 6 | 8 0 at 22; 6 0 at 16½ | Adye p. 155, read by the Neufchatel's design (`Design-Ship-PrinceDeNeufchatel.md:836`) | brig, merchant brig, privateer 20 (from memory) → 8 0 |
| long 4, long 3 | 4: 6 0 at 12¼; 5 6 at 11¼. 3: 4 6 at 7¼ | Adye p. 155, IA leaf n178, read here (R1, 2026-11-07): the 4-pounder of 6 ft printed "22 1", read 12 cwt 1 qr by its own column of metal to the pound of shot (343 lb × 4 = 12¼ cwt; 22¼ would be 623) | cutter's 3s 7 → 4 6 |
| carronade 68, 42, 32 | 68: 5 2 at 36 or 4 0 at 29; 42: 4 3½ at 22¼; 32: 4 0½ at 17⅛ (17 cwt 14 lb) | Adye p. 72, IA leaf n95, read (by the ships sessions, as above; and here, R2) | 32: frigate, brig 17 |
| carronade 24, 18 | 24: 3 7½ at 13 or 3 0 at 11 cwt 2 qr 25 lb; 18: 3 3 at 9 or 2 4 at 8 cwt 1 qr 25 lb | the same (`period.py:31-37`) | 64: 18 and 24; razee 42 |
| carronade 12 | 2 2 at 5 cwt 3 qr 10 lb | Adye p. 72, read by the Neufchatel's design (`:835`), and here | cutter, privateer 6 |
| swivel ½ | to read (R5) | (judgement until read: 3 ft) | cutter, privateer |

- **The bore**: a carronade's as Adye prints it (p. 72: 68, 8.05 in; 42, 6.84; 32, 6.35; 24, 5.68;
  18, 5.16; 12, 4.52; read); a long gun's the shot's diameter (`combat/hits.py:106`
  `shot_diameter_m`, the gunner's rule, Douglas) and its windage (Adye pp. 255-257, R2, to read). **The outside**: a long gun tapers from the base ring,
  `BREECH_CALIBRES` of the bore across, to the muzzle's swell, `MUZZLE_CALIBRES` (judgement, 3.4 and
  2.2, until Caruana's Blomefield dimensions, question 3); a carronade is a short thick tube,
  `CARRONADE_CALIBRES` 2.6 across to its cup (judgement, question 3). The trunnions at 3/7 of a long
  gun's length from the base ring (judgement, question 3), at the middle of a carronade's.
- **The carriage**: a long gun's truck carriage a plain box under the barrel from the deck to the
  axis, `CARRIAGE_SHARE` 0.45 of the gun's length (judgement, question 1); a carronade's slide a beam
  from the port inboard 1.6 of its length (judgement, question 1); a pivot's slide twice its gun's
  length (judgement); a swivel's yoke a post. **Visible first** (`Build-Ships.md` §5.0 principle 2):
  at the owner's 960 × 720 sheet (9-35 px a metre) a long 18 of 9 ft 6 in is 26-101 px long and
  its breech (3.4 of a 5.3 in bore, 0.46 m) 4-16 px across, so the taper and the carriage earn their place; the trunnions, the cascabel, the
  quoin, the trucks and the tackles do not, and are not drawn.

### 3.2 Where the files' weights are from memory

The frigate's and the 64's long 9s (26 cwt), the brigs' and the privateer's long 6s (20 cwt), the
cutter's long 3s (7) and the files' 12-pounder carronades (6) are the generator's table from memory
(`gen_ships.py:4188-4196`), against Adye's 24½, 22 and 5¾. The rule draws each at the pattern of
nearest weight, so they draw at Adye's lengths (the 9s at 7 ft 6 in, 6% off; the 6s at 8 ft, 9% off);
no file's figure moves. The checker lists every gun whose weight stands more than 10% off its
pattern's: none today. The table holds Adye's patterns only; the 74's forecastle 9 of 8 ft 6 in and
27½ cwt (Lavery Tables 17-18, by `Design-Ship-Bellerophon.md:886`) is appended by her builder when
her file lands, and until then a gun of a weight no pattern gives draws at the nearest and is listed.

### 3.3 The muzzle by state

| The engine's state | Drawn | Ground |
|---|---|---|
| secured (not cast loose) | housed: the muzzle `HOUSED_INBOARD_M` (0.1 m) inside the side, the lid shut | judgement; Falconer, the lids let down when the guns are drawn in |
| cast loose, run in (loading, or run in by the sea) | the muzzle inboard by `RECOIL_SHARE` of its length (a long gun 0.4, a carronade 0.15: judgement) | the room to sponge and load; Adye p. 230 (IA leaf n253, read) gives the free recoil on a level platform, 11 ft for the 32 and the 24 and 10 ft 6 in for the 18 at a third's charge, longer than the gun: aboard the breeching stopped it short (question 1). A carronade is served "with taught breechings", which Douglas's note calls a non-recoil principle (art. 136, p. 163, read (OCR), l. 7631-7640), so it is drawn coming in little |
| run out | the muzzle outboard of the side by `OUT_SHARE` of its length: long 0.33, carronade 0.25 (judgement, question 1) | the carriage against the side: "run out the gun square to the breast of the port" (Douglas 1829 art. 134, pp. 161-162, read (OCR), l. 7560-7585) |
| dismounted | the barrel off its carriage, on the deck at its port, tipped 15° (judgement) | `the damage`'s `dismounted` |

## 4. The firing

### 4.1 What fired, and when

The snapshot serves each gun's `fired` (rounds, never falling). The viewer compares it with the
last snapshot's: a gun whose count rose fired since then, once a round. **Each round is stamped with
the tick of the snapshot that first shows it**: exact at 1x, where the snapshot comes every tick
(`ui/server.py:182`), within ten ticks at 10x and sixty above. At 60x the plume's half minute is
half a second, so the minute is what the eye can see; at 10x a broadside fired as the guns bear is
drawn flashing together where it rippled over ten seconds. **Plainly, for the lead:** to stamp each
round with its own tick needs the tick kept on the minute's volleys (`Volley` in `combat/guns.py`,
a key of the battery's), which is 74's and the battery's, and outside item 2's one touch; it is not
taken. The first snapshot after the page connects shows no firing (it has nothing to compare).

### 4.2 The flash, the plume and the recoil

- **The flash** at the muzzle, `FLASH_S` 0.15 s, a star of the bore × `FLASH_CALIBRES` (6,
  judgement), drawn bright.
- **The plume** from the muzzle: thrown out along the barrel `THROW_M` × (charge/6 lb)^⅓ (4 m at an
  18-pounder's 6 lb, judgement), growing over `PLUME_GROW_S` (2.5 s) to `PLUME_RADIUS_M` ×
  (charge/6 lb)^⅓ (3 m, judgement), drifting with the apparent wind (the snapshot's
  `wind.apparent_angle` and `apparent_speed`: in the ship's own frame, where the viewer stands, the
  smoke goes with the apparent wind, `windVector`), widening slowly and thinning to nothing over
  `PLUME_LIFE_S` (30 s). The charge is the gun's own (`parts.charge_lb`, Table No. 29). The figures
  are judgement, to be held against the period's words (R3: Douglas 1829 p. 218, "the smoke in which
  the hulls of the contending vessels are usually enveloped") and a modern source on black powder's
  smoke (R6).
- **In the air, not in the hull:** the muzzle's point is heeled with her; the plume's drift is not.
- **The recoil**: at the round's stamp the barrel runs in from its run-out to its run-in place over
  `RECOIL_S` (0.4 s, judgement; Adye p. 230 for the distance, R2) and stays there until the engine
  runs it out again; run out again between snapshots is drawn over `RUN_OUT_S` (2 s) from the
  snapshot that says it. **Taken another way from the brief's "in and back":** the gun comes back
  out when the crew runs it out, which the engine says, not by itself.
- **None at a gun that did not fire**, and none at a gun in dumb show (its count does not rise).

## 5. The damage, at the viewer's present honesty

- **A shot hole** where `the damage` puts it: its side, `x_m`, `z_m` against the waterline upright,
  `diameter_m` (the shot's), on the drawn side at that height; dark while open, the plug's colour once
  plugged. Below the water it is hidden by the sea as the hull is, and shows when her heel lifts it.
- **A gun dismounted**: §3.3.
- **A spar gone**: as the viewer already drops it.
- **Not drawn, because the readings do not say it:** a port stove (none in the engine), splinters,
  a beaten-in side, a gun's own damage short of dismounting.
- **Found on the way, for the lead (73's):** a hole above the water is made at 0.3 to 1.8 m
  (`hits.py:184`) whatever her side's height, and the cutter's rail stands about 1.5 m above her
  water: a hole above her rail would be drawn on nothing. The viewer draws it at the rail less its
  own radius, and the checker's test of a hole says so; the engine's figure is 73's.

## 6. The animation road (made once; 91's light and air reuse it)

1. **The snapshot** redraws the ship as today (`drawShip`: `buildSkeleton`, `project`, `render`),
   now with the guns, the ports and the holes in the skeleton.
2. **The clock**: `Projection.clockAt(snap, arrivedMs, nowMs)`, pure: the game's time now, the
   snapshot's tick plus the real seconds since it came times the compression while the clock runs
   (held while it is held), never beyond the next snapshot's tick.
3. **The effects**: `Projection.effects(graph, snap, firings, t, facing, heel)`, pure, returns the
   flash, plume and recoil figures alive at t, projected, each with its depth. Effects are **not in
   the frame** (the frame is the ship's; a plume drifting off the picture leaves it, as smoke does);
   a gun's run-out reach is in the frame (`fullRigFrame` gains every gun's muzzle run out and its lid
   open), so no state of the guns rescales the view.
4. **The loop** (`app.js`): `requestAnimationFrame` runs only while an effect is alive or a gun is
   moving, and stops itself; each frame redraws only the effects' layer (two groups, behind the hull
   and before it, by depth against her middle) and moves the moving guns' nodes. The base scene is not
   rebuilt between snapshots.
5. **For 91**: the clock, the effects' two layers and the loop are the road. A sky's light or a
   moving cloud is an effect with no stamp.

**Pace:** the viewer runs on no tick's path. The snapshot gains a list of the guns' states and the
holes; the graph (once, at hello) the guns' places and the ports. Both are measured on the 64 (72
guns) in the server's test for their cost against the snapshot as it is.

## 7. The data served (item 2), and the engine untouched

- **`freesail/api/viewer_guns.py`** (new, pure): the rule of §2 and the table of §3 over a ship's
  spec and fit; the checker and `queries.py` both read it, so the test checks the very placing the
  viewer is served.
- **`/api/ship`** (`queries.ship_graph`) gains `guns` (each gun's id, name and kind words, place,
  side, deck, x, the way it is placed (`port`, `over the rail`, `rail`, `pivot`) and its numbers: the
  triple, the axis height, the train; the figure's length, bore, breech and muzzle; or, refused, why)
  and `ports` (each deck's triples with the port's size, whether over the rail, and the gun ids that
  stand in each by side).
- **The snapshot** (`queries.snapshot`) gains `guns`: for each gun its state (`secured`, `run in`,
  `run out`, `dismounted`), `loaded`, `shut` (its port shut by the sea), `fired`, and a pivot's
  `train_deg`; and `damage`: the holes as `the damage` gives them. Read through the readings registry
  where a reading gives it (`the guns`' `ports_shut`, `the damage`'s `holes` and `dismounted`) and
  from the parts where it does not (each gun's own state, as the snapshot reads each sail's).
- **The snapshot's `flags`** (§12.1), from `freesail/api/viewer_flags.py` (new, pure).
- **`action.fired`** already names its guns (`data["guns"]`, `combat/guns.py:1115`): no engine file
  is touched. Nothing of the physics, the evolutions or the ship files is written; no pin moves.

## 8. The checker (item 4)

`tools/check_viewer_guns.py [files]` prints, for every file under `data/ships/` (or those named): her
contract (what she gives and lacks), and for each fit each gun's place by §2 or why not; each port
with its guns or "empty"; the triples put over the rail not at `OVER_THE_RAIL_M`; each port cut to
the rail; each gun whose weight stands more than 10% off its pattern's; and that every port lies on
her drawn side between her stem's and her stern's closures, below her rail and above her drawn depth.
Its exit is non-zero on any refusal. `tests/test_viewer_guns.py` runs it parametrized over the files
(a file added later is checked by it with no change), and on a file written to a temporary directory
with the contract and a made-up fit (truth 7-443).

## 9. The ship builder's checklist (for `Build-Ships.md` §6's postscript)

For her guns to be drawn, a ship's file gives:
1. `hull.profile` with `rail_m`, `breadth_m` and `decks_m` (each deck a gun stands on);
2. `ports_m.<deck>`: a triple [x, sill, half-breadth] at every port gun's own `x_m` (within 0.01 m),
   the sill her sheet's at that x and the half-breadth her side's at the sill; for a gun over the
   rail, the sill 2 in under the rail (`OVER_THE_RAIL_M`) or anywhere less than the port's depth
   under it;
3. `port_size_m.<deck>`: [width, depth] for every deck with ports;
4. for every gun: `kind`, `pounder`, `place`, `side` (but a pivot), `x_m`, `weight_cwt`, and `deck`
   for a broadside gun and a chaser;
5. then runs `python tools/check_viewer_guns.py data/ships/<her>.yaml` and the test; nothing is drawn
   by hand for any ship.

## 10. The truths (item 5), 7-436 to 7-443, and the flags' 7-444 and 7-445 (§12)

| Truth | Pins |
|---|---|
| 7-436 | every gun of every file with the contract placed: on its deck's triple within 0.01 m in a port, or over the rail by §2.2, or on the rail, or a pivot; no refusal; the checker clean; each gun's figure the same on every ship for its kind, calibre and weight, its length its pattern's |
| 7-437 | the frigate's forecastle guns (pair 18, the bow chasers) over the rail and through no port; her upper-deck guns in ports of the upper deck's size |
| 7-438 | the 64's forecastle 9-pounders of 1784 over the rail by the side's test (§2.2; as the lead rules) |
| 7-439 | a lee port the engine shuts by the roll is served shut in the next snapshot and its gun run in; drawn with its lid down |
| 7-440 | a broadside fired: a flash at each gun that fired in that minute and at no other; the plume to leeward of the apparent wind |
| 7-441 | the frame's bounds equal with every gun secured, every gun run out with its lid open, every plume alive, a hole in her side and every flag flying; the snapshot's new fields' cost measured; the replay's digests the same by both roads (nothing of the world is written) |
| 7-442 | a hull without the contract (the in-test document with no profile) draws no gun and no port, her figures as before point for point |
| 7-443 | a ship file written to a test's temporary directory with the contract and a made-up fit passes the checker with no change of code; the same file with one gun's x off its triple is refused, and says why |
| 7-444, 7-445 | the flags, as the brief words them (§12.5) |

The Node tests in `tests/test_view_geometry.py` beside them: each port on the drawn side within 1 cm;
each port gun's muzzle outboard by its state; nothing below the drawn depth; the frame across states;
the hover words in-world (no build's word).

## 11. The research plan, and the questions for the owner's shelf

### 11.1 The plan (for the builder, beside the work; each reading recorded with its mark)

- **R1. Adye 1804 p. 155** (IA leaf n178): the rows the ships sessions did not take (the long 6s, 4s,
  3s, the 9 of 7 ft, the 12s' four lengths as a check). *Done 2026-11-07, read: §3.1's rows; every
  row the files use is now read on the page.* The page image fetched through the proxy into
  a new directory, read as an image, its rows cited by page; the OCR loses the columns.
- **R2. Adye p. 72** (leaf n95) as a check of the carronades; **p. 230**, recoil (`adye…ocr.txt:636`
  the index); *both read 2026-11-07 on their images (§3.1, §3.3)*; **pp. 255-257**, the shot's and the windage's diameters (l. 22869-23000).
- **R3. Douglas 1829**: the exercise, arts. 122-135 (running out and in, housing, the breechings'
  length) and the carronade on its slide, art. 136 ff. (l. 7151-7645); the smoke, art. 175 p. 218
  (l. 9612-9625) and p. 280 (l. 11795-11805). *Read (OCR) 2026-11-07 for arts. 134 and 136 (§3.3);
  the smoke's passages say it envelops the hulls and covers a ship's manoeuvre, and give no figure.*
- **R4. Falconer 1780, PORTS** (l. 13783-13789) and **Steel 1805, HALF-PORTS and PORT-LIDS** (l.
  3052-3053, 4061): the lids, read (OCR); the page images where the OCR is unsure.
- **R5. The swivel**: Adye's and Falconer's SWIVEL entries for the half-pounder's length. *Searched
  2026-11-07 (OCR, every spelling): neither gives one; question 4 stands, 3 ft by judgement.*
- **R6. Secondary, read and cited, never copied:** public museum records of surviving Blomefield
  guns and carronades (the outside diameters, to check §3.1's calibres); a modern source on black
  powder's combustion products (the share that is smoke). Searched through the proxy; each cited by
  title and page or address, its figures given in this note's own words.
- **R7. Visible first**: each figure measured at 960 × 720 and 800 × 600 on every armed file before
  it is kept (§5.0 principle 2).

### 11.2 The questions for the owner's own references (through the lead; the answers as figures with
their citation, never copied text; none holds the work)

1. **Lavery, *The Arming and Fitting of English Ships of War***: the truck carriage's length and the
   height of its trunnions above the deck by calibre; the carronade's slide's length; and how far a
   gun's muzzle stood outboard of the side when run out, or the breeching's length from which it
   follows. *(In place: §3.1's carriage and §3.3's `OUT_SHARE`, judgement.)*
2. **Lavery**: which decks' ports had hanging lids, and which half-ports or none (a frigate's
   quarterdeck and forecastle; a sloop's and a cutter's ports; the 64's upper deck); and how far a
   lid was hauled up when open. *(In place: a lid on every port, opened 70°.)*
3. **Caruana, *The History of English Sea Ordnance*, vol. II**: Blomefield's long gun's diameter at
   the base ring and at the muzzle's swell, in calibres, and where the trunnions stand; the
   carronade's outside diameter and its cup. *(In place: 3.4 and 2.2 calibres, the trunnions at 3/7;
   the carronade 2.6.)*
4. **Lavery or Caruana**: the half-pounder swivel's length and its yoke's height on the rail.
   *(In place: 3 ft; 0.15 m.)*
5. **Lavery**: how far a bow or stern chaser could be trained toward its end through a chase port.
   *(In place: 30°.)*
6. **Winfield**: nothing is asked of him for this package; the ports by class are the ships
   session's.

## 12. The flags drawn at their places (the brief's item 7, the owner's addition of 2026-11-07)

### 12.1 What 81 reads, and what it serves until 76's file exists

- **The snapshot's `flags`**: a list, each `{place, name, words, drawing}`: the place word (§12.2),
  the flag's name in the nation's file, its words for the hover ("British colours, the red ensign";
  "the ensign union down"), and its drawing, a short list of coloured rectangles and lines in the
  flag's proportion, as 76's `colours.yaml` gives it. The viewer draws whatever is there, at its
  place, by the rule; a place word it does not know draws nothing and the server's test says so.
- **Until 76's file exists for a root** (the trunk as it stands): the server serves, from the
  player's ship's colours (71's `Colours`, `world/signals.py:470`) and `data/nations.yaml`, **one
  plain ensign at the peak** while her colours show (`shown`, `false`, `distress`), the nation shown
  (the other's under false colours), its words `Colours.words` as the lookout reads them, its drawing
  a single field in the proportion 1:2 (judgement) coloured by the first colour the nation's `flag`
  word names ("the red ensign" red; "the white ensign with the arms" white; a word naming none, the
  plain cloth's colour), **nothing** under `none` and `struck`, and the drawing turned over under
  `distress` (the union down; a plain field shows it only in its words). The flag of truce (74's
  cartel): the trunk's colours have no such state (`COLOURS_STATES`, `world/signals.py:71`: shown,
  none, false, struck, distress; no cartel in the engine), so the fallback serves a plain white
  field at the peak the moment the locker holds one, by whatever word 74 or 76 gives it, and the test
  pins it on a locker given in the test. `signals.py` is read, never written.
- **Where the code stands:** the fallback in `freesail/api/viewer_flags.py` (new, pure), read by
  `queries.snapshot`; 76's locker list read through the same function when it exists, so the
  meeting of the two packages is one function's first line.

### 12.2 The place words, and the one rule that puts each on a drawn spar

The masts are the graph's root spars of class `mast`, named by their ids' first word (`fore`,
`main`, `mizzen` or `mizen`); a ship of one mast has that mast as her main. A mast's **truck** is the
top of the highest spar stepped on it as drawn (a struck topmast's lower head, a housed one's), a
**masthead** of a named mast piece its top; the **peak** is the outer end of the aftmost mast's gaff.

| Place word | Drawn at | Where the ship lacks it |
|---|---|---|
| `peak` | the aftmost gaff's peak, on its halyard's line | `staff` |
| `staff` | the ensign staff: the taffrail's middle, `ENSIGN_STAFF_M` (2.5 m, judgement) above it, raked aft 15° | (every profiled hull has one) |
| `main truck`, `fore truck`, `mizen truck` | that mast's truck | the main for a ship of one mast; else not drawn, said |
| `main topgallant masthead` (and the others by mast and piece) | that piece's head | its mast's truck |
| `jackstaff` | the bowsprit's cap end, `JACKSTAFF_M` (1.5 m, judgement) above it | not drawn, said |
| `main rigging` (and the fore's, the mizen's) | halfway up that mast's weather shrouds, lashed flat to them | not drawn, said |
| `main yardarm` (the lower yard's), `fore topsail yardarm` (a named yard's) | package 102: that yard's weather arm as drawn | not drawn |

The words are 81's, offered to 76 through the lead for `colours.yaml`'s `where`, so that one shape
serves both packages; **for the lead to carry to 76.**

### 12.3 The drawing

Stiff, as the brief has it: the cloth a flat quadrilateral with its hoist along its halyard at the
place, its fly to leeward of the apparent wind (`windVector`), drooped `FLAG_DROOP_DEG` (15°,
judgement) below the level; a pendant a long tapering streamer the same way; each in its drawing's
rectangles and lines; the waving is 91's, on §6's road. Package 102 (step 1): the drawing's
polygons (`polys`) drawn with the rest in the drawing's order; a `swallowtail` flag drawn with the
notch taken out of its fly, each part cut in two at the middle by the notch's two edges (the cut
`cut` of the fly, a third where the drawing gives none, judgement off the plates); a `triangle`
tapered to a point at the middle of its fly.

**The signals flying (package 102, step 3).** The snapshot's `hoists` (the player's own ship's
alone; no other ship's signals are served, the owner's ruling of 2026-11-11): each `{place, key,
words, flags}`, its place word (the order's, 'make the signal No. 16 at the fore'; the private
table's, 'at the fore yardarm'; else `main topgallant masthead`, judgement), the lookout's words
for it, its flags uppermost first, each `{name, words, drawing}` with `drawing.kind` `flag` or
`pendant`. Drawn down its halyard from its place, each flag one hoist and `SIGNAL_GAP_M` (0.15 m)
under the one above; a signal flag's fly `SIGNAL_FLY_OF_BEAM` (0.3) of her beam, a signal
pendant's `SIGNAL_PENDANT_OF_BEAM` (0.6), each hoist by its proportion (judgement). Gone with the
next snapshot after it comes down. The frame is not widened for them: a hoist at a yardarm of
the schooners and the hermaphrodite brig reaches up to a quarter of a metre beyond it. **Sizes** (judgement, question 7): an
ensign's fly half her beam, a jack's half the ensign's, a pendant's length 0.6 of her main yard,
the hoist by the drawing's proportion. In the painter's order a flag sorts at its own middle as a
sail does. In the frame (§6): every place word's point the ship has, with the largest flag's fly
swung every way about it, so that a flag hoisted, struck or doubled leaves the bounds as they were.

### 12.4 Hover words

The flag's `words` as served (in-world, the lookout's own words), and its place: "British colours,
the red ensign, at the peak".

### 12.5 The truths

7-444 and 7-445 as the brief words them: each flag within 0.1 m of its place's point in the
projection when the locker says it flies; the bounds unmoved; struck draws none, false colours the
other nation's, the cartel's white once 76 serves it, and a hull whose nation has no
`colours.yaml` draws the plain ensign of §12.1. Until 76's file lands, the truths run on the
fallback; their rows for the pendant, the broad pendant, the jack and the doubled ensigns run on a
locker list given in the test, so that they pin 81's placing and not 76's data.

### 12.6 The question it adds for the owner's shelf

7. **The flags' sizes** by rate (an ensign's fly against the ship's beam or her main yard; a
   pendant's length): Lavery, or the Admiralty's flag tables if the shelf has them. *(In place:
   §12.3's judgement.)*

## 13. What this package does not build

The light and the air and the flags' waving (91, which reuses §6); 76's `colours.yaml` and the locker's
list of what flies where (76's); a three-dimensional ship or damage beyond the present
honesty (M8); any ship file's triples or port sizes (the ships session's); a key of port size by
port (the schema's); the guns' mechanics (70's, 77's); a tick on each volley (§4.1, the battery's).

## Postscript: as built (2026-11-07)

The lead approved the note on 2026-11-07 with seven rulings: §2.2's side's test (truth 7-438 pins
it); §1's deck asked of port guns only; §2.4's chasers at their own triples; §1's per gun with the
test strict; §4.1's stamp at the first snapshot (a tick on each volley booked to package 77); no
engine touch; §12.2's place words carried to 76, and the flag of truce's word ruled for all three
packages: 74 adds the state `truce` to `COLOURS_STATES`, "a flag of truce", and the fallback serves
the white under it (pinned on a locker given the state).

**Built as the note has it**, and these taken another way or found, each measured in the tuning
notes, "Package 81":
- **The snapshot reads where the ship keeps the state, never through the two readings** (§7 said
  through the registry). `the guns` and `the damage` make the battery and the damage keeper on
  first asking (`battery_of`, `damage_of`), and `signals.locker_of` a locker: served in every
  snapshot they would write the world. So `queries._action_entries` reads `ship.extra`'s battery
  (its shut ports), damage keeper (its holes) and locker (its colours) where they are, the same
  state the readings read, and makes none; a fight with a snapshot every tick gives the same log
  digest as without (truth 7-441).
- **A hull with no profile draws and frames nothing of the action**, its flags too: the first form
  gave her the flags' frame, which moved `test_view_geometry`'s pin of her frame (5.59 m to 5.46);
  the brief's rule is that she draws as 75 left her, so the pin stands.
- **The flags' frame** is each place's own flags drooped as drawn (first written, the pendant's reach
  at every place and a drop of it straight down, 2 to 9 m on every hull): nothing on the frigate,
  the razee, the 64 and the schooners, 0.20 m on the brigs, 1.2 to 1.9 m on the boats and the smack,
  2.9 m on the cutter and 5.0 m on the lugger; the peak held swung every way about its gaff's
  throat, since the gaff swings with its sheet (first written, the frame moved 0.19 m on the cutter
  and the smack between states).
- **A port cut to the rail follows the rail down** where it steps within the port's width: the 64's
  foremost quarterdeck port, at her breast, whose forward top corner stood above the drawn rail.
- **A port on her drawn side, not at its triple's half-breadth:** the razee's and the 64's drawn
  sides stand up to 0.17 m off some triples (the gaps §5.3 records and never moves); the port is
  drawn on the side as drawn.
- **The smoke and the flash face the viewer**: a plume drawn in the ship's plane read as a flat coin
  seen from the bow; each is a disc (the flash a star) about its point's projection, the plume's
  foot held at the sea. **Each barrel has its muzzle's face**, so a gun run out towards the viewer
  shows.
- **The served `charge_lb`** sizes each gun's plume by the cube root of its powder (Table No. 29's,
  `parts.charge_lb`). *Since package 75's SW-1 (2026-11-09): the gun's own charge is its fit's
  `charges` (`parts.filed_charge_lb`, `viewer_guns.served(..., charges)`, which `ship_graph` passes
  from the ship's fit), as its magazine fills it: Table No. 29's in the new ships, the shares as
  filed in the eight files of the packages before 75 (the lead's rule, Build-Ships.md §10), and a
  fit without charges the shares.*
- **The words**: a port, its lid, a hole, a gun, a flag each say themselves in the ship's words
  ("No. 3 starboard gun, a long 18-pounder: run out"; "an upper-deck port, shut, the sea at its
  sill"; "a shot hole through the side to larboard"; "British colours, the red ensign, at the
  peak"), and the primer's chapters 22 and 23 say what the picture shows.
- **The hook for 77**: `Volley` (`combat/guns.py`) keeps no tick, so a round is stamped with the
  first snapshot's tick (`Projection.firingsBetween`); a tick on each volley served beside
  `action.fired`'s guns would let `firingsBetween` stamp each round at its own.

**Not built**, as §13 has it; and the owner's shelf's seven answers wait to replace §3's, §2.5's and
§12.3's judgements by cited figures, each a constant at the top of `viewer_guns.py` or of
`projection.js`'s action section.
