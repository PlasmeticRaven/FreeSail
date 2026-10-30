# Design: the three engine extensions of package 75 (the settee, the lateen class finished, the yards under the bowsprit)

**Status (2026-10-28).** Phase 3 of `Plan-ShipsWorkflow.md`. This is the one design document
for the engine extensions that the lead's go-ahead of 2026-10-28 asks to see before their
builders start (`Decisions-ShipsRound2-2026-10.md` l. 61-65; the brief, `M7-WorkPackages.md`,
"The session's five extensions"). It covers:

1. **the settee**, the bilander's main;
2. **the lateen class finished**, which now carries the mizen course cut at the mast for the
   64 and the 74, with the full lateen kept possible for a later tartane;
3. **the yards under the bowsprit** of the 64, the 74 and the bilander.

Nothing is built. The plain ships' builders do not wait for this document: their files need
only stage 0 (`Build-Ships.md` §3.1; §8 here is stage 0E, laid after the approval). The generator modules, the hull profiles and the ship files are not under
the gate.

**Where.** The clone `D:/Projects/FreeSail/FreeSail-pkg-75` on the package's branch at 6b94731 (the
lead's 3421829 merged: 73, 86, 84's steps 1 and 2). Every `file:line` is at that head. Paths
are from the repository root. A builder re-checks a line before editing it.

**What binds, in order:** the brief (`docs/dev/M7-WorkPackages.md`, the head rules and
"Package 75"); the lead's go-ahead of 2026-10-28; the plan (`docs/design/Plan-ShipsWorkflow.md`,
Phase 3); the owner's answers and the lead's rulings (`Decisions-ShipsRound2-2026-10.md`
l. 1-76, and D1-D5, D8, D9, D13, D42-D46 as answered); the research notes **Eng**, **Bil**,
**Ind** §3 and §5, **Bel** §5 and §13. The physics' equations are not changed; the curves and
the sail classes around them are open.

**Marks.** *read*: the code or the page cited. *read (owner's book)*: the owner's private
copy, cited by figure or page and never quoted. *observed*: seen in a scratch script run from
the tree root with `py`, kept outside the repository in the session's scratch folder
`design/` (`risk/classing_table.py`, `risk/sprit_rule.py`, `risk/half_mizen.py`,
`ext/aback.py`; the first three re-run for this document). *measured*: arithmetic on the
files, the tables or a scratch run. *catalogue*, *secondary*, *memory*, *judgement* as the
notes use them. **Plainly:** marks a choice that departs from a decision, a ruling or the
brief, with the reason. No git was run, no test suite was run, and nothing in the repository
was written but this file.

**The maps.** The code maps cited as *map-engine* and *map-generator*, and the shared-work
draft folded into `Build-Ships.md`, are filed beside this document in `ships-design/`. The
scratch scripts named are not.

---

## In brief

- **The mizen course** of the 64 and the 74 is class `lateen` on a `lateen_yard`, marked by a
  new sail key `cut_at_mast: true`.
  - **In the physics it is the gaff sail** the owner asked for (Bel §13.5): one property,
    `Sail.curve_class`, gives it the gaff's curve and trim at every lookup that now reads the
    class. Measured on the frigate: within 0.03 kn of her spanker at every angle.
  - **In the handling and the drawing it is a sail on a yard:** its own `set_lateen`,
    `take_in_lateen`, `furl_lateen`, `reef_lateen`, `shake_out_lateen` and
    `trim_lateen_sheet`; the yard slung across the mast at its truss, its fore part bare,
    with lifts.
  - **It is the ship's driver:** hauled aft at helm's a-lee, brailed up hove to, brailed at
    "up helm" and hauled out by the wind, taken in at the gale's third reef, set after the
    cast. These are the gaff driver's paths, widened by the key.
  - **The lateen yard is no longer a braced yard** (`Spar.is_yard` true for `yard` alone).
    The period's mizen yard had vangs, not braces.
  - The full lateen (no key) keeps the lateen class's own curve, evolutions and words, for
    the tartane.
- **The yards under the bowsprit** stay class `yard` with square sails, braced by every brace
  order. One predicate, `Ship.under_bowsprit(part)`, is read at nine places: it keeps them out
  of every count of masts and levels, puts them with the head yards, clews their sails up hove
  to, takes them in first when sail is shortened, and puts their windage where they are.
  Observed: the frigate, the brig and the topsail schooner then class exactly as filed.
- **The settee** is a dipping lug with a new key, `settee: true` (D2(a); the brief: "the
  settee follows the lug's class as 43b built it").
  - The key routes it to four evolutions of its own: `set_settee` and `furl_settee` aloft,
    `take_in_settee` (clewed up with the yard aloft), and `dip_settee`. It keeps the lug's
    reef, trim and curve (D42(a), D45(a), D44(a)).
  - **In stays** (D3(b)) it is a ship's mizen until the head yards are swung: hauled aft at
    helm's a-lee, drawing against the mast once through the wind, dipped last. **In wearing**
    (D46(d) rule 4) it is lowered at "up helm" and hoisted on the new lee only once the wind
    has crossed the stern. **Hove to** (D4(a)) her main topsail goes to the mast, through a
    mast key `heave_to_aback: true`, and the settee is clewed up aloft.
  - It is kept off every lugger's path: getting under way, the dip lists, the heave-to's
    lowering, the storm lug.
- **The one rule of the design.** Every change is keyed on something no existing file has:
  the keys `settee`, `cut_at_mast` and `heave_to_aback`, the class `lateen_yard`, or a yard
  rooted at a bowsprit. Measured on the eight files: none has any of them. So no existing pin
  is expected to move (§11).
- **One engine builder** builds it in three steps, the lateen first (the Indefatigable
  first), then the bowsprit yards, then the settee. One viewer builder draws each as it lands.

---

## Decisions taken

| # | Decision | Why, in short |
|---|---|---|
| E1 | The mizen course is **class `lateen` with `cut_at_mast: true`**, on a `lateen_yard` | D9(c) and the lead's ruling ask for "the lateen class finished"; the cut is a key so that the drawing, the handling and the curve can tell it from a whole lateen without reading geometry |
| E2 | **`Sail.curve_class`** is "gaff" for a sail cut at the mast, else its class. The curve, the trim's offset and range, the rating's coefficient and the furled windage are read through it | The owner: "in the physics, a four-sided, loose-footed sail, like the gaff sail" (Bel §13.5). Measured: the lateen curve costs the frigate 0.21 kn at 50°; the gaff's costs 0.03 kn at most (§3.2) |
| E3 | **`Spar.is_yard` is true for `yard` alone** | Falconer 1780, VANGS and BRACE: the mizen yard has vangs in place of braces (Bil §1.2); Lavery I32 gives it lifts, a truss and a bowline, no brace. Its sail is trimmed by the sheet in the physics already (`physics/sails.py:590-596`) |
| E4 | The mizen course is **the driver**, through the gaff driver's paths widened by the key | Steel 1794 II p. 316 (hauled out at helm's a-lee) and pp. 321-322 (hauled up as she bears up, out once the stern is past) (Bil §1.5). These are what the engine already does to the spanker |
| E5 | The lateen class gets **its own six evolution files**, named by class | The engine runs `set_{cls}`, `take_in_{cls}` and the rest by class (`tests/test_evolutions.py:293-330`); the vocabulary already names `set_lateen` and `take_in_lateen` (`data/vocabulary.yaml:1756, 1765`) |
| E6 | **"Furl the mizen" furls it aloft** on its yard (`furl_lateen`) | Falconer 1780, YARD: the woldings of a lateen yard are the steps "to climb to the peek to furl or loose the sail" (Bil §1.1). **Plainly:** a gaff sail keeps package 37l's refusal; a sail laced to a yard is furled on its spar |
| E7 | The yards under the bowsprit stay **class `yard`, braced like any yard**, and leave the classing through **one predicate read at nine places** | Every fault Eng §5 and map-engine §3.2 found comes from the bowsprit being counted as a mast. Observed: the predicate alone restores the filed classing on three ships (§4.2) |
| E8 | **No evolution files, no runtime state and no new station** for the spritsails: the square sail's evolutions, the fore top's topmen by the fallback | Reuse: Lever's topping of the spritsail yard is stood in for by the horizontal brace (Plainly, §4.4) |
| E9 | The settee is **class `lug`, `dipping: true`, `settee: true`** | D2(a); the brief. One key routes it and guards every lug-keyed path; the lugger's file never carries it |
| E10 | **Four settee evolutions**: set and furl aloft, take in clewed up aloft, dip with the yard lowered. Reef, trim, bend, unbend and shift stay the lug's | Lescallier p. 390: set and clewed up as a square sail (Bil §1.2, §1.4); D1(a) the dip; D42(a) the lug's reef |
| E11 | A runtime field **`Sail.yard_lowered`** marks a settee's yard on deck | "In the gear" is a lug lowered on deck but a settee clewed up aloft; the viewer and the evolutions must tell them apart |
| E12 | **In stays (D3(b))** the settee joins the tack's boom sails at helm's a-lee and is dipped **when the head yards' swing ends**; the tack ends only once it is hoisted | Bourdé 1765 p. 87, Steel 1794 II p. 316, Boteler p. 163 (Bil §1.5), carried over by judgement |
| E13 | **In wearing (D46(d) rule 4)** it is lowered at "up helm", passed round, and hoisted on the new lee **when its time is done and the wind is on the new side of the stern** | Steel 1794 II pp. 321-322 (Bil §1.5), carried over by judgement. The gate on the wind is the rule's own words |
| E14 | **Hove to (D4(a))**: a mast key `heave_to_aback: true` names the mast laid aback; the settee is clewed up aloft. Her lie is measured with it so and with it eased, before any truth | D4(a). The engine's own rule eases a brig's driver because brailed she falls off (`scripts.py:2251-2266`); the figures decide whether D4(a)'s words stand (§5.7) |
| E15 | The settee is **one of her courses** (in "courses" and "plain sail"), not her driver | The gale then reefs it at the second reef and takes it in at the third (`orders/storm.py:396-404`); the driver lists would hand it twice and ease it hove to, against D4(a) |
| E16 | **The settee's manoeuvre time stays in code** (`settee_dip_s`, 120 s) | `tests/test_catalogue.py:73-150` pins the `timing` of `tack`, `wear` and `heave_to` exactly (`test_milestone_2_timings_are_unchanged`, 258-266): a key there moves a pin. 43b's `dip_s` is a code default too (`scripts.py:1122`) |
| E17 | **The ropes (D45(a) with (c))**: lifts as `lift`, the peak ropes as `vang`, the heel ropes (the settee's ourses, the mizen yard's bowlines) as `guy`, one unsided `sheet` led to the taffrail | A `brace` takes 0.3 of the sail's pull and is drawn (`sails.py:117, 1438-1466`); a `bowline` may only be of a sail and is hauled by an order (`schema.py:145-165`; `vocabulary.yaml`, `haul: bowline`). `vang`, `guy` and `lift` are read by nothing but the reeving and repair tables |
| E18 | **Stage 0 is inert stubs plus two guards**: the golden classing table of the eight files and in-memory rig fixtures. The wiring is the builder's | The plan's behaviour-free stage 0; the guards let every step prove it moved nothing (§8) |
| E19 | **One engine builder, three ordered steps**: the lateen, the bowsprit yards, the settee | All three edit `evolutions/scripts.py`, `orders/verbs.py` and the vocabulary; the Indefatigable comes first |
| E20 | **Rule 5 is measured before it is pinned.** The tables predict it holds only at small incidences | §5.10. The fallback is D44(c), a `settee` curve row read through `curve_class` |

---

## 1. What binds, and what is left alone

- **The physics' equations are not changed.** `_plate_force` (`physics/sails.py:1079-1132`),
  `compute_sail_forces`'s sums (335-501), `_lateral_offset` (1320-1351), the load fractions
  (115-119) and `data/sail_classes.yaml` are untouched. The physics files gain only these
  readings, each a lookup or a membership, for the lead's gate lens:
  - `_read_rig` reads `SAIL_CLASSES[sail.curve_class]` (580), and the furled windage the same
    (1529);
  - `_square_rigged` (852-866) and the helm's mark (444-448) leave out yards and sails under
    the bowsprit;
  - `_spar_x` (1569-1573) gives a yard under the bowsprit its own `x_m` for its windage.
- **84's names.** Nothing here reads `world.ship` or a `CrewedWorld`. Every change is on the
  `Ship`: the scripts, the trim, the orders, the runner, the API's ship graph, the viewer. The
  one World read on these paths, the captains' storm lug (`world/captains.py:2822-2831`, through
  `_lugs_all`), reads `self.world.ship`, a name the Hull keeps (`Design-OneWorld.md` §2.2;
  `world/hulls.py:52-127`). Tests build worlds with `make_world` and read `w.ship`.
- **The ship files** are written only through `tools/gen_ships.py` and its `tools/ships/`
  modules. The engine extensions add one table entry and one lookup to the generator (§8).
- **D18 and D25 stay open.** Every height this design reads (a yard's `height_m`, a sail's
  `corners_m`) is above the file's deck, as now; the viewer draws the rig from that datum
  (`client/projection.js:275`) whatever D18 settles.
- **The suites** (the brief): the fast tier and the touched files' slow tier on the owner's
  machine; the whole slow tier and the pace tests are the lead's on the build machine.

## 2. The period's handling, in brief

The reference the evolutions and the truths are built against. Each carrying-over to the
engine is marked where it is used.

**The settee** (Bil §1.1-1.5):
- A four-cornered lateen on a yard hung obliquely, the after end peaked about 45° over the
  stern, the fore end about amidships (Falconer 1780, BILANDER; Röding I col. 304). Gwyn's cut,
  slung at a third (D5(a)).
- Its gear: parrel and truss; jeers; a peak lift (the derrick); a peak brace (the English
  vangs); two heel ropes (the ourses, the English bowlines); two tacks, made fast to windward;
  one sheet to the taffrail; clewlines and buntlines "comme pour les voiles quarrées"
  (Lescallier p. 390).
- Set: gaskets cast off aloft, the gear let go, the tack hauled down to windward and the sheet
  aft (judgement on Lescallier p. 390 and Falconer, YARD). Taken in: sheet and tack eased, clewed
  up as a course. Furled on the yard aloft; no source lowers the yard to furl (Bil §1.4).
- Reefed by one band parallel to the foot, a fifth of the leech up (D42(a)).
- Going about: lowered and passed round, as a lug (Röding II col. 581; D1(a)). In stays it is
  kept drawing as a ship's mizen, the ourse braced to leeward as the helm goes down, the yard
  changed last (D3(b)). In wearing a ship's mizen is hauled up as she bears up and hauled out
  once the stern has passed the wind (Steel 1794 II pp. 321-322).

**The mizen course on its yard** (Lavery 1985 I31-I32, read (owner's book); Bel §5.4, §5.6,
§13.5; Ind §3.1, §5):
- Four-sided, its head laced to the yard abaft the mast, its luff laced to the mast, its foot
  loose with one sheet to the taffrail, a tack line to the deck forward of the mast, brails and
  one reef band a fifth of the mast leech from the foot.
- The yard slung at a truss, held by lifts with a fiddle block, a bowline at its fore end to
  the aftermost main shroud; it runs on forward of the mast with no sail there. Steel's 74 rigs
  it with jeers, derrick, vang pendants and falls, bowlines, a truss and brails (1794 II p. 37).
- "Haul the mizen out while you put the helm a-lee ... brace the bowline quite to leeward";
  the yard is not changed (Steel 1794 II p. 316, Bil §1.5). In wearing it is hauled up as she
  bears up and hauled out by the wind (pp. 321-322; Lever 1808, OCR l. 9726-9727, "the Mizen is
  hauled out" with the wind on the new quarter).
- The cut from Steel's sail table (Ind §5; Bel §5.6), measured (arithmetic, 22½ in to a cloth):

  | | Luff / after leech | Cloths head / foot | Head rise over run | Foot | Area | Yard | Fore part |
  |---|---|---|---|---|---|---|---|
  | The 64 | 9¼ / 17¼ yd | 14½ / 15½ | 24 ft over 27.2 ft (41°) | 8.86 m | 104 m² | 77 ft 0 in (Ind §3.1) | about 0.53 |
  | The 74 | 11 / 21 yd | 16 / 17 | 30 ft over 30 ft (45°) | 9.71 m | 138 m² | 84 ft 0 in Steel, 86 ft 6 in *Dragon* (Bel §5.3, §13.4) | about 0.50 |

  I32's yard lies at about 42° with about 0.48 of it forward of the mast (measured by eye on
  the owner's photograph, ±10 px a point).

**The spritsail and the sprit topsail** (Steel 1794 I pp. 196-197; Lever 1808, OCR
l. 7236-7372 and 9378-9966; Lavery I27-I30, read (owner's book)):
- The spritsail yard slung under the bowsprit near the cap, across the ship; the sprit-topsail
  yard under the jib-boom on a traveller drawn out toward its end, its clews sheeted to the
  spritsail yard's arms.
- The braces lead to the fore stay and up to the fore top; the spritsail sheets lead aft along
  the side to a sheave abaft the foremost fore shroud (I30).
- Set large and before the wind, with the royals and studding sails (Lever l. 9778-9780); taken
  in early as it freshens (l. 9962-9966). By the wind the yard is topped up by the lee brace and
  the sail reefed or taken in (l. 7271-7274). At "mainsail haul" the yard is topped the
  contrary way (l. 9386); wearing, topped with the new lee brace (l. 9724-9725).
- "Most essential, to wear a Ship, should any Accident happen to the Foremast" (l. 7241-7243);
  the *Bellerophon* at the Nile, "setting her spritsail, wore clear" (James vol. 2 p. 180; Bel
  §5.5).

---

## 3. The lateen class finished: the mizen course cut at the mast

### 3.1 The class, the key and the curve

- **The key.** `SailSpec.cut_at_mast: bool = False` (`ship/schema.py:392-425`, parsed in
  `_parse_sail` beside `dipping`, 1388-1392) and `Sail.cut_at_mast` (`ship/parts.py:252-325`,
  copied in `from_spec`, 304-325). Refused unless the sail is class `lateen`, names a `mast`
  role (optional today for a lateen, `schema.py:115`) and gives four `corners_m`.
- **The curve.** A property `Sail.curve_class -> str`: `"gaff"` when `cut_at_mast`, else
  `self.cls`. Every lookup that reads a sail's curve or trim by its class reads it instead:

  | Lookup | Where |
  |---|---|
  | the curve driving the sail | `physics/sails.py:580` |
  | the furled windage | `physics/sails.py:1529` |
  | the sheet's floor and ceiling | `evolutions/trim.py:376` |
  | the wanted sheet angle | `evolutions/scripts.py:277, 1833, 2330, 5268`; `orders/verbs.py:1218, 1916`; `world/ships.py:391` |
  | the served reef factor | `api/queries.py:334` |
  | the readings' luff | `api/readings.py:873` |
  | the rating's coefficient | `tools/gen_ships.py:869` (the entry's class, read by `static_kn` at 440) |

  `orders/verbs.py:1101` and `world/ships.py:386` read the class of a sail on an `is_yard`
  spar, which a lateen sail no longer has (§3.3); they stay.
- **Why lateen with a key.** Bel §13.5 left this document a choice between "the lateen class
  with its fore part cut away" and "a gaff sail hung from a yard". The class is lateen because
  D9(c) and the lead's ruling ask for the lateen class finished, with the mizen course as its
  user, and because its handling and drawing are a yard's. The curve is the gaff's because the
  owner wants the physics of a loose-footed gaff sail, and the lateen row is untuned
  (`docs/dev/TuningNotes.md:127`).
- **Plainly:** D9(c)'s "its curve" is met for the cut sail by the gaff's curve. The lateen
  row itself stays untuned; no ship of this package sails a whole lateen to tune it against.
- **The full lateen** (no key) reads the lateen row, the lateen's 8-85° trim and
  `PEAK_COEFF["lateen"]`, a new entry of 1.25 (measured: the hypotenuse of the row's 1.15 and
  0.48 at its 35° peak is 1.246, the rule `gen_ships.py:133-134` states).

### 3.2 What the physics makes of it (measured)

Observed (`risk/half_mizen.py`): the frigate's spanker replaced in memory by a lateen sail of
the same area, `x_m` and centre on a 16-m `lateen_yard`, `is_yard` narrowed; plain sail; the
polar's balanced speed (`world/ships.py:394-420`) in 15 kn:

| Off the wind | 50° | 60° | 90° | 120° | 150° |
|---|---|---|---|---|---|
| The spanker as filed | 2.21 | 4.29 | 8.19 | 7.86 | 6.53 |
| Cut at the mast, the lateen's curve and trim | 2.00 | 4.17 | 8.11 | 7.76 | 6.55 |
| Cut at the mast, the gaff's curve and trim | 2.18 | 4.28 | 8.18 | 7.86 | 6.54 |

With the yard out of the braced yards the frigate's classing was as filed: three masts with
yards, four head yards and eight after, the main backed, square-rigged; the yard's brace 0.

- **Its lateral offset** is 0.5 × 0.8√A × sin(sheet), since it has no boom or gaff role
  (`sails.py:1342-1350`). Against Steel's cut that foot is 8.16 m for 8.86 m on the 64 and
  9.40 m for 9.71 m on the 74 (measured, 3-8% short). Kept.
- **Its pull** goes through its yard to the mizzen mast (`ship/graph.py:348-358`). Its sheet
  takes 0.6 of it, its jeers 0.5 (`sails.py:1490-1522`). It has no brace to load.

### 3.3 The yard out of the braced yards

- `Spar.is_yard` (`ship/parts.py:243-248`) becomes `return self.cls == "yard"`. The
  docstring gains the reason: a lateen yard has vangs in place of braces and a bowline at its
  heel (Falconer 1780, VANGS and BRACE; Lavery I32), and its sail is trimmed by the sheet.
- Every reader of the gate then leaves a lateen yard alone (read):
  - the brace orders by name: `orders/verbs.py:1553-1574` refuses it. The hint at 1561 gains
    `lateen_yard` beside `gaff` and `boom`: "the lateen sail on it is not braced; it is
    trimmed with its sheet and vangs";
  - `trim sails` (`verbs.py:1001-1135`) and the polar's trim (`world/ships.py:375-391`);
  - `working_yards` (`scripts.py:466-469`) and with it every manoeuvre's classing;
  - `_square_rigged` (`sails.py:852-866`);
  - the standing runtime's contrary sets (`standing/runtime.py:168-172, 791`) and the
    promotion's trim (`world/crews.py:390`);
  - `resolve.kind_of` (`orders/resolve.py:621`), which now calls it "lateen yard".
- `lateen_yard` stays in `YARD_LIKE_CLASSES` (`schema.py:91`), so the yard work evolutions
  (sending down, swaying up, a spare shifted: `scripts.py:3617-3632`) still take it.
- **No schema refusal of a brace on a lateen yard.** A tartane's lateen yard has a peak brace
  (Lescallier p. 379; Steel's xebec, I p. 237; Bil §1.4). The contract (§3.4) says the mizen
  yard files none.
- `combat/hits.py:509-524` `_spar_weight` gains `"lateen_yard": 2.0`, a yard's exposure aloft,
  as `lug_yard` has (judgement). Today it falls to the default 1.0.
- **What it changes.** The 64 and the 74 keep their cross-jack, mizen topsail and topgallant
  yards on the mizzen, so their classing is the frigate's (observed, §3.2). A tartane with
  lateen yards alone becomes a fore-and-after, as she was. No existing file has a lateen yard
  (measured), and no test reads one as a braced yard (read: `grep is_yard tests/`).

### 3.4 The file contract (the 64's and the 74's modules)

- **The yard.** Class `lateen_yard`, on the mizzen mast, an id beginning `mizzen.` with two
  z's (`mizzen.yard`; the frigate's cross-jack is `mizzen.crossjack.yard`, so the id is free).
  The `mizzen.` prefix gives the evolutions the mizzen top's topmen (`runner.py:1048-1056`;
  `crew/hands.py:104-108`).
  - `height_m` the truss above the deck; `length_m` the ship design's (§2's table); no
    `brace_limit_deg`.
- **The sail.** Class `lateen`, `cut_at_mast: true`, roles `yard` (the mizen yard) and `mast`
  (the mizzen mast), an id the ship design chooses (`mizzen.course` suggested: Steel's
  "mizen course", Lavery's "mizzen course").
  - `corners_m` `[tack, throat, peak, clew]`, heights above the deck: the tack and the throat
    on the mast's raked line at their heights, within 0.1 m; the head along the yard's slope;
    the clew loose. Cut from Steel's cloths and leeches (§2).
  - `area_m2` and `x_m` from the corners by the lugger's `_quad_area_centroid`
    (`gen_ships.py:7030`); `centre_height_m` the centroid's height **plus the deck height**
    (a sail's centre is above the water: `physics/sails.py:349, 358`; the scratch settee's fault, Eng
    §4.4).
  - `reef_bands: 1` (Steel: one band a fifth of the mast leech from the foot; Bel §5.6).
- **Its lines** (Steel 1794 II p. 37; Lavery I32):
  - the jeers, a `halyard` of the yard;
  - the lifts and Steel's derrick, `lift` lines of the yard;
  - the vangs, two sided `vang` lines of the yard;
  - the bowlines at the heel, two sided `guy` lines of the yard;
  - **one unsided `sheet`** of the sail, to the taffrail;
  - one `tack` of the sail, the tack line forward of the mast;
  - **no brace and no brails.** The engine has no brail line; the spanker files none and
    `take_in_gaff`'s brailing reads no line.
- **Groups.** In the groups the frigate files her spanker in ("plain sail", "all sail",
  "fore-and-aft sails"), never in "courses": the gale would otherwise reduce it as a course as
  well as a driver (`orders/storm.py:396-411`).
- **The generator asserts** the corners on the mast and the head on the yard's line as it
  writes them (§9.3), so a bad file cannot be written.

### 3.5 The handling: the driver's paths

One predicate is read where the code now says `sl.cls == "gaff"` for the driver:
`drives_aft(sl) = sl.cls == "gaff" or sl.cut_at_mast`.

| Path | Where (read) | Today | Gains | The period |
|---|---|---|---|---|
| `boom_sails`: hauled aft at helm's a-lee and held, hauled to windward if she hangs, eased on a miss, worked lying to, drawn on the new tack and in the fill-away | `scripts.py:217-233`; callers 306, 323, 1044, 1072, 1606, 1717, 2250, 2291, 2509, 2553, 2643; `orders/navigation.py:831` | a gaff on a boom; a standing lug | `or sl.cut_at_mast` | Steel 1794 II p. 316: hauled out as the helm goes a-lee, "trimmed as it will remain" |
| `after_gaff_sails`, the driver: brailed up hove to with the main aback; brailed at "up helm" and hauled out by the wind; reduced at the gale's third reef; replaced by storm staysails; handled lying a-try, scudding and coming to anchor | `scripts.py:553-581`; callers 1442, 1475, 2251, 4645, 4785, 4801, 4886, 6131; `orders/storm.py:100, 409` | gaff | `drives_aft` | Steel 1794 II pp. 321-322; the *Bellona* lay to under the mainsail and mizen staysail (Lavery p. 9; Bel §13.2) |
| `_after_sail`, the box-haul's "Up mainsail and spanker!" | `scripts.py:4225-4238` | gaff | `drives_aft` | Luce's order, carried over (judgement) |
| `after_gaff_sails_all`, set after the cast | `scripts.py:7354-7365` | gaff | `drives_aft`, and a settee (§5.8) | Steel 1794 II, getting under way (Bil §1.5) |

- `ship.mast_of(sail)` of the course is the mizzen mast through its yard (`graph.py:174-182`),
  so "the aftermost lower mast" holds.
- With one unsided sheet the course is never in `shifted_sails` (`scripts.py:298-315`).
- **The words.** The two log lines that name the spanker by word (`scripts.py:7265` "set the
  spanker"; 6135 "brail up the spanker") say "spanker" only when every driver is a gaff sail,
  and name the sail otherwise ("set the mizen"). The box-haul's words already name the sail
  (`part_name`, 4310-4312, 4385-4400).
- **At helm's a-lee** a sail cut at the mast adds "brace the bowline to leeward" to the words
  (Steel 1794 II p. 316): words for a line no order works (D45(a)). The frigate's and the
  brig's words do not change.

### 3.6 Evolutions and words

| Verb | Evolution (new data) | Steps (s) and crew | Basis |
|---|---|---|---|
| set | `set_lateen` (`vocabulary.yaml:1756` names it already) | Furled: cast off the gaskets and clear away the brails, 60. In the gear: let go the brails, 15. Haul out the sheet and haul down the tack, 30, which sets it, the sheet at `wanted_sheet(sail)`. **No hoist**: the yard stands. 10 ordinary, afterguard and topmen | Steel 1794 II p. 316 ("haul the mizen out"); Lavery I32; `set_gaff`'s times (judgement) |
| take in | `take_in_lateen` (`vocabulary.yaml:1765`) | Brail up, 90, to the gear. 8 ordinary, afterguard | Steel 1794 II p. 37 (brails at the peak, middle, throat and foot); `take_in_gaff`'s time |
| furl | `furl_lateen` | Brail up, 90, if set; furl on the yard, 120, `aloft: true`. 8 ordinary, afterguard and topmen | Falconer 1780, YARD; `furl_gaff`'s times |
| reef, shake out | `reef_lateen`, `shake_out_lateen` | Ease the sheet and brail in, 30; tie (cast off) the points along the foot band, 120 (90); haul out, 30. 10 able (ordinary), afterguard | Steel's one band a fifth of the mast leech up (Bel §5.6). The times are this row's own (judgement): the yard is not lowered, so there is no settling and no hoist. (B3.1 found that `reef_gaff`'s less its settling would be 240 s, and `shake_out_gaff`'s 180, against these 180 and 150; the files cite this row) |
| trim | `trim_lateen_sheet` | As `trim_gaff_sheet`: script `trim_sheet`, 0.4 s/m², 20-120 s, 6 ordinary afterguard | the sheet to the horse at the taffrail (Steel p. 208; Lavery I32) |
| bend, unbend, shift | `bend_sail`, `unbend_sail`, `shift_sail` (`applies_to: sail`) | vocabulary rows for `lateen` | — |

- **`wanted_sheet(sail)`**, one new function in the runner's expression environment
  (`runner.py:660-686`): `trim.wanted_sheet_angle(sail.curve_class, dyn.apparent_wind_angle)`.
  So one `set_lateen` file sets a cut sail to the gaff's 18-85° and a whole lateen to 8-85°.
- **The vocabulary** (`data/vocabulary.yaml:1749-1886`): `furl: lateen: furl_lateen`,
  `reef: lateen: reef_lateen`, `shake out: lateen: shake_out_lateen`, `trim: lateen:
  trim_lateen_sheet` (today `trim_gaff_sheet`, which refuses it: Eng §4.5, observed), and the
  bend, unbend and shift rows. `take_in_words: lateen` becomes `[brail up, brail in, clew up,
  haul up, lower]` (today `[lower]`, 1885; the whole lateen is clewed up "comme les autres
  voiles", Lescallier p. 379).
- **`HANDING_EVOLUTIONS`** (`scripts.py:419-431`) gains `take_in_lateen` and `furl_lateen`.
- The sprit rows (`vocabulary.yaml:1757, 1766`, which name files that do not exist) are left
  as they are (§16).

### 3.7 The full lateen kept possible

The tartane's lateen (Bel §13.5) is not built here. Nothing here blocks it:
- the narrowed `is_yard` is right for her, and a peak brace stays allowed (§3.3);
- without `cut_at_mast` her lateen is no boom sail and no driver;
- `set_lateen`, `take_in_lateen`, `furl_lateen`, `reef_lateen` and `trim_lateen_sheet` serve
  her, at her own curve and floor through `curve_class`;
- the viewer draws a lateen with four corners and no key by `lugCut` as a standing sail on its
  lee side (§6.1), and one with no corners as now.

Her package chooses how she goes about: the dip, by widening the schema's lug-only `dipping`
(`schema.py:1390-1392`), the dip's machinery keying on `dipping` as `against_the_mast` already
does (`sails.py:662-670`); or Willaumez's *muder* as an evolution of its own (Bil §1.5, way
(b)). Her curve is tuned then.

---

## 4. The yards under the bowsprit (D8(b))

### 4.1 The file contract (the 64's, the 74's and the bilander's modules)

- **The spritsail yard.** Class `yard`, on the bowsprit (`spritsail.yard` on `bowsprit`).
  - `x_m` its station under the bowsprit near the cap (Steel 1794 I pp. 196-197; Lavery I30),
    `height_m` above the deck at that station, below the bowsprit's line, both from the
    bowsprit's steeve and length (the 64's steeves about 27°: Ind §3.1).
  - `length_m`: the 64's 57 ft 6 in (17.53 m), the 74's 62 ft 0 in (18.90 m) (Ind §3.1; Bel
    §5.3). `brace_limit_deg` by judgement from the braces' leads to the fore stay and the fore
    top (Lavery I30; Bel §13.1, answer 14).
  - **No halyard.** It hangs in slings, and a course "has no halyard": `set_square`'s hoist is
    then skipped (`runner.py:803-806`; `data/evolutions/set_square.yaml:44-47`).
- **The sprit-topsail yard.** Class `yard`, on the jib-boom, at its station near the
  jib-boom's end, higher than the spritsail yard; the 64's 34 ft 6 in (10.52 m), the 74's
  40 ft 6 in (12.34 m). A `halyard` of the yard stands for the traveller's outhauler: the sail
  is "drawn out toward the extremity of the boom ... as any other topsail yard is hoisted"
  (Falconer 1780, SPRITSAIL-TOPSAIL; Lavery I29/2's halyard and traveller).
- **Lines** by `square_sail_lines` (`gen_ships.py:1433-1463`): sided braces, lifts, sided
  sheets, clewlines and buntlines; the guys (Lavery I28) as `guy` lines of the yard.
- **The sails.** Class `square`. Steel's two diagonal reef bands in the spritsail may be filed
  as `reef_bands: 2` and are reefed as any square sail's; the sprit topsail has none (Lever
  l. 7354-7356). The 64's spritsail 102 m² and sprit topsail 103 m²; the 74's 121 and 125 m²
  (Ind §5; Bel §5.6).
- **Groups.** Their own group ("spritsails", which the engine does not read) and "all sail",
  where the studding sails are. **Never** "plain sail", "courses", "topsails", "headsails" or
  "jibs", each of which the engine reads by name (map-generator fact 11). Out of "plain sail",
  the polar and the far ships never set them (`world/ships.py:364-372`). Recommended; the ship
  designs' call.
- **The bilander** crosses a spritsail yard (Steel's Plate 1; Lescallier Pl. XXII fig. 8).
  Whether a sail is bent to it is her design's (D8(b)); a bare yard is handled the same way.

### 4.2 The rule: one predicate, nine places

`Ship.under_bowsprit(part) -> bool` (`ship/graph.py`, beside `mast_of`, 174-182): true for a
spar of class `yard` whose `mast_of` is a bowsprit, and for a square sail whose yard is one.
**Not** for a jib: a jib's chain also roots at the bowsprit, so the predicate names yards and
their square sails only. It reads the chain memo, a dict lookup.

| # | Place | Where (read) | Change |
|---|---|---|---|
| 1 | `_masts_with_yards` | `scripts.py:472-478` | leaves out a yard under the bowsprit |
| 2 | `head_and_after_yards` | `scripts.py:481-491` | the foremost mast chosen from the real masts; the yards under the bowsprit added to the head yards; the after yards never take them |
| 3 | `_square_rigged` (cached, gate 3) | `sails.py:852-866` | leaves them out |
| 4 | the helm's mark | `sails.py:444-448` | a sail under the bowsprit is not among the lifts; its `_yard_level` would be 0, a course's (`sails.py:869-881`) |
| 5 | `stagger`, `by_level`, `eased_lowest` | `evolutions/trim.py:98-228` | a yard under the bowsprit is not grouped as a mast; it keeps its own target |
| 6 | `trim sails`' lowest-yard judgement | `orders/verbs.py:1108-1117` | the bowsprit's lowest yard does not decide whether she is on a wind |
| 7 | `light_sails_forward_of` | `scripts.py:584-609` | adds the set square sails under the bowsprit, so hove to (2281) and backing and filling (4886) they are clewed up |
| 8 | `shorten sail`'s first lines | `orders/__init__.py:362-369`; `orders/storm.py:312-321` as the pattern | a new `bowsprit_sail_lines(ship)`, put first as `flying_topsail_lines` is: "take in the spritsail" for each set sail under the bowsprit (Lever l. 9962-9966, with the royals) |
| 9 | `_spar_x` | `sails.py:1569-1573` | a yard under the bowsprit gives its own `x_m`, so its windage acts where its sail does |

**Left as they are** (read; judgement: right):
- `working_yards` keeps them: they are braced by name, by "brace sharp up", "square the
  yards" and "trim sails", and by the polar's trim, within their limits.
- `after_square_yards`, `yards_to_back` and `yards_to_back_set` (`scripts.py:494-550`) take
  their masts from place 1, so never the bowsprit; `lowest_square_sails` (618-626) wants a yard
  whose parent is a mast, so a spritsail is no course.
- `_adjacent_refusals` (`verbs.py:1501-1550`) pairs the two sprit yards as yards of one
  "mast": right, since the sprit topsail's clews are at the spritsail yard's arms (Steel;
  Falconer).

**Observed** (`risk/sprit_rule.py`, re-run: a spritsail yard on the bowsprit and a
sprit-topsail yard on the jib-boom added in memory, with square sails; the rule applied by
places 1 and 3, the stagger fed from them):

| File | As filed | With the yards, no rule | With the yards and the rule |
|---|---|---|---|
| frigate-36 | square-rigged; head the four fore yards; 8 after; backs the main; stagger +2.0° | head the two sprit yards; 12 after; stagger None | as filed, every field |
| topsail-schooner | not square-rigged; head the fore topsail and topgallant yards | **square-rigged**; head the sprit yards | as filed, every field |
| brig | square-rigged; head the four fore yards; 4 after; stagger +2.0° | head the sprit yards; 8 after ("mainsail haul" swings the fore yards); stagger None | as filed, every field |

Place 2's addition (the sprit yards among the head yards) changes no classing field; it puts
them in the head swing.

**As built (B3.2, 2026-10-29).**
- **The head field** counts the head yards on the masts. `head_and_after_yards` returns the
  sprit yards in its head list, so read whole it gives 6 head yards on the fixture, not the
  frigate's 4. The tests (`tests/test_bowsprit_yards.py`, the moved `tests/test_lateen.py`)
  count 4 on the masts and 8 after, with the two sprit yards asserted beside them, and every
  other field as filed. B1's truth 7-189 ("her classing as the frigate's row") reads it the
  same way.
- **"Square the yards"** and every order that names a file group ("the yards", "the head
  yards") brace only the yards the file lists in that group. §4.1's contract lists the sprit
  yards in "spritsails" and "all sail" alone, so these orders leave them; they are braced by
  name, by "brace sharp up" and by "trim sails". Whether the 64's and the 74's files list them
  in "yards" and "head yards" too is a file choice for B1 and B7, with no engine change; for
  the lead.
- **The heave-to's line** lists the light sails clewed up with commas when one of them is under
  the bowsprit ("Clewed up the fore topgallant, the spritsail and the sprit topsail."); every
  other ship keeps its words as before.
- **Shortening sail** takes the sprit sails in first, outermost first, and never reefs them
  (`orders/storm.bowsprit_sail_lines`). The order between the two is judgement: Lever gives
  none.
- **The helm's mark** reads the predicate once a tick, held in the tick's `_Drawing` with the
  sail's curve (B3.1's precedent).

### 4.3 Handling

- **Tacking.** At "let go and haul" the yards under the bowsprit swing with the head yards
  (`scripts.py:1176-1205`), each to its own sharp-up target (place 5). Lever has the spritsail
  yard topped the contrary way at "mainsail haul" (l. 9386); the horizontal swing stands
  in for the topping (Plainly, §4.4).
- **Wearing.** They follow the wind with the head yards (`follow_wind`, `scripts.py:1520-1522`),
  as Lever's spritsail is kept set and braced until she comes to (l. 9722-9725).
- **Heaving to.** They are among the yards kept full and braced up for the tack (`self.full`,
  `scripts.py:2221`), and their sails are clewed up with the light head sails (place 7;
  Luce 1866 ch. XXVI, "settle down the top-gallant sails and royals, or clew them up", as the
  code cites at 584-590). Left set, a spritsail pays her head off. The log: "Clewed up the fore
  topgallant, the spritsail and the sprit topsail." Judgement on carrying the rule to them.
- **The gale and shortening sail.** Taken in first (place 8). Never among the courses or the
  topsails, so the gale's reduction never reefs them (`storm.py:370-411`).
- **The physics** is unchanged. The force is a square sail's at its own `x_m` and
  `centre_height_m` (`sails.py:584-589`). The load goes through the yard to the bowsprit, and
  the generator's rating pass rates the bowsprit for it (`gen_ships.py:841-901`). By the wind it
  draws aback: braced to 45° at 60° off it gave −0.12 kN (Eng §5, observed), as the period
  topped and reefed it or took it in. Large, its pull far forward pays her head off, as the
  *Bellerophon* used it at the Nile.
- **Evolutions.** `set_square`, `take_in_square`, `furl_square`, `reef_square`,
  `shake_out_square` and `brace`, unchanged. `set_square`'s hoist is skipped for the spritsail
  (no halyard) and works the sprit topsail's traveller.
- **Hands.** `topmen` resolves the bowsprit, which has no top, to every top in turn, the fore
  first (`crew/hands.py:104-108, 202-220`); `set_square`'s list then names the forecastle.
- **Plainly:** Luce 1884 has the forecastle men "loose and furl the head-sails" (OCR
  l. 21605-21607). Mapping the bowsprit to the forecastle would reorder the hands of every jib's
  `bend_sail`, `reeve_line` and `shift_sail`, whose crews put `topmen` first, and could move
  pins. Left for a later package.

### 4.4 What is not modelled

- **The topping of the spritsail yard** by the lee brace (Lever l. 7271-7274, 9386,
  9724-9725): the yard is braced horizontally and drawn so. **Plainly:** a stand-in, chosen over
  a runtime topped state and an evolution of its own, because the engine reads no yard's slope.
- **The sprit-topsail yard's run along the jib-boom**: drawn at its file station.
- **Steel's diagonal reef bands**: reefed as any square sail.
- **The spritsail yard got fore and aft in a gale** (Lever l. 10554-10576).

Each is noted in the ship files' comments by their modules.

---

## 5. The settee

### 5.1 The file contract (the bilander's module)

- **The yard.** A `lug_yard` on the main mast, its id beginning `main.` so that its topmen are
  the main top's (`runner.py:1048-1056`).
- **The sail.** Class `lug`, `dipping: true`, `settee: true`, roles `yard` (the lug yard) and
  `mast` (the main mast).
  - `corners_m` `[tack, throat, peak, clew]`, heights above the deck, cut to Gwyn's
    proportions (D5(a): luff 0.16 of the leech, leech and foot 0.72 of the head, yard 44°;
    Bil §2.3). **The point a third along throat→peak stands on the main mast's raked line at
    its height, within 0.1 m.** That is the point `lugCut` pivots and shifts to the mast
    (`client/projection.js:365-393`), so the drawing lies on the file's corners and the
    physics' `x_m` with no sling field (Eng §6.3). The peak inside the taffrail (D5(a)).
  - `area_m2` and `x_m` from the corners (`_quad_area_centroid`, `gen_ships.py:7030`);
    `centre_height_m` the centroid **plus the deck height** (the scratch settee's two faults,
    Eng §4.4).
  - `reef_bands: 1` (D42(a)).
- **Its lines** (Lescallier p. 390, the letters of Pl. XVII fig. 7; Bil §1.2):
  - the jeers, a `halyard` of the yard;
  - the derrick (the martinet, o), a `lift` of the yard;
  - the peak brace (*bras*, t; the English vangs), two sided `vang` lines of the yard;
  - the ourses (q; the English bowlines), two sided `guy` lines of the yard;
  - the tacks (r, r), two sided `tack` lines of the sail;
  - **one unsided `sheet`** (s), to the taffrail;
  - clewlines and buntlines of the sail.

  With one unsided sheet the settee stays out of `shifted_sails` (`scripts.py:298-315`) and
  lies to leeward wherever its yard hangs (`evolutions/trim.py:420-463`), as the lugger's lugs'
  single sheets do.
- **Groups.** "courses" (with the fore course), "plain sail", "all sail". Never "gaff sails".
- **The main mast laid aback.** `heave_to_aback: true` on the main mast (§5.7).
- **Hands.** Her eight (D43) should give the main top at least two men, or `topmen` falls to
  the fore top for the loosing and furling aloft (`hands.py:202-220`).

### 5.2 One key, and how it routes

| Piece | Where | Change |
|---|---|---|
| Schema | `SailSpec` (`schema.py:392-425`); parsed beside `dipping` (1388-1392) | `settee: bool = False`. Refused unless class `lug`, `dipping: true`, four `corners_m` and a `mast` role; never with `sheeted_to` or `flying`. Unknown sail keys are dropped silently today (map-generator fact 4), so without the field the key would vanish |
| Runtime | `Sail` (`parts.py:252-300`), `from_spec` (304-325) | `settee: bool = False`, copied; `yard_lowered: bool = False`, runtime only. Plain class defaults, so old checkpoints load |
| Routing | `evolution_key` (`orders/verbs.py:419-422`) | `"settee"` when the sail is a settee and the verb's mapping has a `settee` row; then `"flying"`; then the class. So reef, shake out, trim, bend, unbend and shift fall to the lug's rows |
| Applies | `Runner._check_applies` (`evolutions/runner.py:565-602`) | `class: settee` accepts a sail with `settee` true, as `class: flying` accepts a flying sail (581-582) |
| Furl | `FURLED_AS_TAKEN_IN` (`verbs.py:416`); the furl mapping's merge (321-328) | unchanged: the furl row `settee: furl_settee` is found before the lug's folded take-in |
| Take-in words | `_take_in_kind` (`verbs.py:517-524`); `vocabulary.yaml:1876-1886` | kind `"settee"`, words `[clew up, haul up]`. "Lower the mainsail" is refused: "a settee sail is clewed up, not lowered" |
| Handing | `HANDING_EVOLUTIONS` (`scripts.py:419-431`) | gains `take_in_settee` and `furl_settee` |
| Vocabulary | `vocabulary.yaml:1749-1786` | `settee:` rows under `set`, `take in`, `furl` and `dip` only |

### 5.3 Its evolutions (new data files)

Times are judgement, each from the engine's like work; no period timing was found.

| Evolution | Steps (s) | Crew | Basis |
|---|---|---|---|
| `set_settee` | Furled: lay aloft and loose, 90, `aloft: true`. In the gear: let go the clewlines and buntlines, 20. On deck (`yard_lowered`): hoist, 60, via `halyard_of(sail)`, which clears `yard_lowered` and sets `lug_side` to `lee_side()`. Then haul down the tack to windward and the sheet aft, 45: set, the sheet at `wanted_sheet(sail)` (8-85°). A yard with no side yet is hoisted on the lee side; one aloft keeps its side | 6 ordinary; topmen, afterguard, forecastle | Lescallier p. 390; Falconer, YARD. `set_square`'s loose and let-go, `dip_lug`'s hoist |
| `take_in_settee` | Ease the sheet and tack and clew up, 60: in the gear, **the yard aloft** | 6 ordinary; afterguard, forecastle | Lescallier p. 390 and pp. 221-228; `take_in_square`'s clewing up |
| `furl_settee` | Clew up, 60, if set; furl on the yard, 150, `aloft: true`. A yard on deck is furled there and hoisted, 60 | 6 ordinary; topmen, afterguard | Falconer, YARD (the woldings the steps to the peak); `furl_square`'s furl. "No source says the yard was lowered to furl" (Bil §1.4) |
| `dip_settee` | Preconditions `dip_lug`'s and `sail.settee`. Lower, 30: in the gear, `yard_lowered` true. Pass round abaft the mast, 75: `lug_side` to `lee_side()`. Hoist, 75, via `halyard_of(sail)`: set, `yard_lowered` false | 6 able; forecastle, afterguard | D1(a); Röding II col. 581. `dip_lug`'s 30/60/60 lengthened for a yard of 15-17 m against the lugger's 10.3 m (`lugger.yaml:74-79`) (judgement) |
| `reef_lug`, `shake_out_lug`, `trim_lug_sheet` | unchanged | unchanged | D42(a); D45(a) |

**Plainly:** `dip_settee` is its own file. Adding `yard_lowered` to `dip_lug.yaml` would serve
too, but it would edit the lugger's file for no gain of hers.

The short-handed rule begins a request with half its hands, slower in proportion
(`SHORT_HANDED_SHARE`, `hands.py:95`). Every settee request is six, which a company of eight
meets with a watch on deck of four (D43; B4 checks each starts).

### 5.4 Every lug-keyed path, and the settee there

Two helpers in `scripts.py`: `lugger_lugs(ship)`, the set dipping lugs that are not settees,
and `settees(ship)`, the set settees.

| Path | Where (read) | The lugger | The settee |
|---|---|---|---|
| `boom_sails` | `scripts.py:217-233` | her standing mizen | out (it dips); joins the tack's boom sails at helm's a-lee only (§5.5) |
| `shifted_sails` | 298-315 | — | out: one unsided sheet |
| `dipping_lugs` | 327-333 | fore and main | **in**, unchanged: the stern watch reads it |
| `LugDip` | 336-404 | dips all her dipping lugs | `self.ids` from `lugger_lugs`: for a ship with no settee, today's set exactly. The settee has `SetteeChange` (§5.5) |
| Tack | 1054-1229 | lowered at helm's a-lee, dipped through the wind | D3(b), §5.5 |
| Wear | 1460-1610 | dipped as the wind comes aft | rule 4, §5.6 |
| Heave to | 2241-2249 | lowered | clewed up aloft, §5.7 |
| Rounding to | 6070-6077 | lowered | in the gear, which for a settee is clewed up aloft; no change (§5.8) |
| `_set_fore_and_aft` | 6786-6797 | `lug_side` to the lee | unchanged |
| `_lugs_all`; getting under way as a lugger; the start words | 6800-6804; 6925; 6835-6837 | her dipping lugs | **leaves out a settee**: she gets under way as a ship (Eng §4.4's failure removed) |
| `_standing_lugs_all` | 6807-6820 | her mizen | out (it dips) |
| `after_gaff_sails_all` | 7354-7365 | — | **adds a settee**: set after the cast as her after sail, on the lee side |
| The stern watch | `orders/navigation.py:778-845` | reports lugs against their masts | reports it in the singular words that exist (820-825): right under D1(a) |
| The captains' storm lug | `world/captains.py:2822-2831` | the taille-vent | `_lugs_all` is empty, so she lies a-try |
| The gale | `orders/storm.py:396-404` | — | through "courses": reefed at the second reef (`reef_lug`), taken in at the third (`take_in_settee`) |
| `against_the_mast` | `sails.py:662-670`; `runner.py:655-658` | 2/3 of the area | kept: on one board it lies against the mast until dipped |
| `FURLED_AS_TAKEN_IN` | `verbs.py:416` | "furl" takes a lug in | furled aloft by its own row |

**The untried manoeuvres**: box-haul, wear short round, box off, lie a-try, scud, back and
fill, fill away, come to anchor, furl all, loose sails to dry. B3 runs each once on the
bilander's file and on the fixture, and records what the settee does. A guard is added only
where one misbehaves, keyed on `settee` alone.

### 5.5 Going about: the tack under D3(b)

`SetteeChange` (new, in `scripts.py` beside `LugDip`): the set settees' ids, a side, the time
left, `lowered`, `done`. `lower()` puts each in the gear with `yard_lowered` true and returns
the words; `change(side, seconds)` lowers if not lowered and starts the time;
`advance(dt, factor, awa, may_hoist=True)` hoists when the time is done and `may_hoist`, sets
`lug_side`, clears `yard_lowered`, draws the sheet as `LugDip.advance` does and logs in the
singular. `TackScript` gains `settee_change: SetteeChange | None = None` as a class default
beside `dip` (`scripts.py:962-970`).

1. **Ready about; helm's a-lee** (`_ready_about`, 1054-1086).
   - `self.booms` is `boom_sails(ship)` plus the set settees, so the settee's sheet is hauled
     aft to its floor with the spanker's pattern (`sheets_to`, 1075).
   - `LugDip(ship)` takes the lugger's lugs only, so the settee is not lowered.
   - The words: "Ready about. Helm's a-lee; ease off the head sheets; haul aft the mainsail
     sheet and brace the ourse to leeward." The ourse is a line no order works (D45(a)); the
     words are Bourdé's and Steel's.
2. **Hung in stays** (`_hang`, 1302-1322): as a boom sail, its sheet is held over to windward,
   and it pushes her stern away (Luce 1866, carried over by judgement).
3. **Through the wind** (1119-1128): the lugger's dip starts; the settee is not dipped. Its
   single sheet lies it to the new lee (`trim.py:452-463`) while its yard hangs on the old
   side: against the mast, at 2/3, drawing (`sails.py:662-670`).
4. **Let go and haul** (1176-1205): the head yards swing; `_draw_on_new_tack` trims its sheet
   with the boom sails (1293-1300).
5. **The head yards swung** (the phase becomes "steady", 1206-1208): `settee_change.change(new
   lee, settee_dip_s)`, `settee_dip_s` read by `timing_value("settee_dip_s", 120.0)`, absent
   from `tack.yaml`. "Dip the mainsail: lower the yard, pass it round abaft the mast and shift
   the tack to the weather bow."
6. **Hoisted on the new lee** when the time is done, by the crew factor: "Dipped the mainsail;
   hoisted on the starboard side, to leeward of the mast."
7. **She is tacked** when steady and the settee is up: `_lugs_down` (1088-1090) is true while
   either the lugger's dip or the settee's change is pending (1116, 1226).

`advance` is called beside `self.dip.advance` (1110-1111). A miss comes only before she is
through (the checks live under `if not self.through`, 1129), so the change never meets
`_miss_stays`; there the settee's sheet is eased off with the boom sails (1339-1341).

**The moment.** D3(b) says "dipped last, after the head yards are swung". The change begins
when the head yards' swing ends, not at "let go and haul", so the after sail helps her round
until her head sails fill on the new tack (Boteler p. 163, "set in the lee braces fore and aft;
shift the mizen"). Open for the owner to confirm (§14).

The time, 120 s, is the lugger's in-manoeuvre 90 s (`timing_value("dip_s", 90.0)`, 1122)
lengthened for the longer yard (judgement); the dip order's own 180 s is `dip_settee`'s.

### 5.6 Wearing (D46(d), rule 4 as reworded)

- **"Up helm"** (`_up_helm`, 1460-1501): `settee_change.lower()` beside the driver's brailing,
  and `change(new lee, settee_dip_s)` started at once. The words: "Stand by to wear ship. Up
  helm; lower the mainsail; brace in the after yards."
- **Hoisted on the new lee** (in `tick`, beside `self.dip.advance`, 1544-1545) when the time is
  done **and** `self.sign * wind_rel(ship, wind) < 0`, the wind on the new side of the stern:
  "Hoisted the mainsail on the starboard side, to leeward of the mast; the wind is past the
  stern."
- `holds()` (1441-1443) gains the settee's id while the change is pending; the wear finishes
  only when it is done (1604).
- The lugger's dip at "wind aft" (1532-1543) is unchanged; a settee lowered at "up helm" is not
  set there, so `LugDip` would not take it in any case.
- **The difference from the lugger.** 43b's lugs keep drawing until the wind is aft; only a
  settee comes down at "up helm", which is D46(d)'s wording. The gate on the wind is stricter
  than a time alone: Steel's mizen is hauled out "as soon as the stern has passed the wind".

### 5.7 Heaving to (D4(a))

- **The mast laid aback.** `SparSpec.heave_to_aback: bool | None` (`schema.py:359-389`, parsed
  in `_parse_spar`, 1270-1301) and `Spar.heave_to_aback: bool = False` (`parts.py:170-200`),
  refused on any spar not of class `mast` and on a second mast. `yards_to_back`
  (`scripts.py:504-523`) returns that mast's working yards first, when it has any; else the most
  square sail, as now. `yards_to_back_set` (526-550) and the captains (`captains.py:2624`) follow
  it. The bilander's main topsail goes "to the mast", the rule the code cites (Luce 1866 ch.
  XXVI). Unknown spar keys are dropped silently today, so the field is needed.
- **The settee.** In `HeaveToScript.begin` (2240-2249) the lowering takes `lugger_lugs`; the
  set settees go in the gear with `yard_lowered` false: clewed up aloft, D4(a). The log's list
  says "clewed up the mainsail" for a settee and keeps "lowered ..." for a lug.
- **The engine's driver rule.** The engine keeps a brig's driver set with its sheet eased when
  the backed yards are on her aftermost mast with yards, because brailed up she falls off to a
  run (2251-2266, package 32e). The bilander's backed main is her aftermost mast with yards, so
  with the settee clewed up nothing abaft is full. In the trial (Eng §4.4) the fore topsail was
  backed and she fell off to 79-87° by 300 s; the brig lies 63-64° off.
- **Measured before any pin.** B3 on the fixture and B4 on her file measure her lie at +150 s
  and +300 s in 15 and 20 kn: with the settee clewed up (D4(a)), and with it kept and its sheet
  eased to `HOVE_TO_DRIVER_APPARENT` (`scripts.py:1648`) as the brig's spanker. If D4(a)'s lie
  stays within the heave-to's four to seven points (`heave_to.yaml:50-51`), it stands. If not,
  both figures go to the lead and the owner; no truth pins the heave-to before that.

### 5.8 Getting under way, rounding to, the gale

- **Getting under way.** With `_lugs_all` leaving out settees, she takes the ship's path:
  loosing aloft, casting with the head yards (`scripts.py:6918-6930`). After the cast
  `after_gaff_sails_all` sets the settee on the lee side (`_set_fore_and_aft`, 7257), and the
  words name it ("set the mainsail", 7265). The trial's lugger path failed at 1,842 s, and its
  standing settee never set (Eng §4.4).
- **Rounding to** (6070-6077): put in the gear with the square sails, which for a settee is
  clewed up aloft. B3 checks that she rounds to and brings up. If she does not, the settee is
  kept to bring her up as the spanker is and clewed up at "brought up" beside the driver
  (6131-6136), keyed on `settee`.
- **The gale.** Through "courses" (§5.1): one reef with the topsails' second reef, taken in
  with their third (`storm.py:396-404`; Luce 1884 p. 476's order for a ship's courses, carried
  to her great sail by judgement). She is square-rigged by her fore and main yards, so the rule
  reaches her (`storm.py:382-384`).

### 5.9 The physics: curve, mast and sheet

- **Nothing in the physics changes.** The curve is the lug's (D44(a); `sail_classes.yaml:81-91`),
  the cut against the mast 2/3 (`sails.py:135, 662-670`), the trim 8-85° (`trim.py:266`), the
  lateral offset 0.5 × 0.8√A × sin(sheet) (`sails.py:1342-1350`). For the polar it lies clear
  of the mast (`lug_side` None, `sails.py:666`).
- **The sheet to the taffrail (D45(c)).** The loose-footed geometry takes a foot of 0.8√A and
  a block a fathom abaft the clew at the floor angle (`trim.py:270-279, 386-391`). D45 has B4
  check that this block falls near the taffrail. **If it falls more than a fathom from it**, B3
  adds a settee branch in `sheet_geometry` (371-395): the foot from the corners' tack→clew, the
  block at the taffrail on the centreline. About ten lines, keyed on `settee`, held in reserve.
- **Rule 1** (a point nearer the wind than square sails: Steel 1794 I p. 237; Lescallier p. 380)
  is read off her polar. Measured at this head: the brig's `closest_deg` is 50° and her
  `beat_deg(15)` 60°, 4.26 kn at 60° in 15 kn (`world/ships.py:337-348, 423-447`).

### 5.10 Rule 5 against the tables (measured)

Rule 5: "aback, the settee presses the mast harder than a square sail does" (D46; Fincham 1843
p. 59). Aback, a square sail and a held fore-and-aft sail meet the same plate equation at their
class's coefficients (`sails.py:1079-1132`). The resultant per unit area (`ext/aback.py`):

| Incidence | Square | Lug | Lug ÷ square | Lug against the mast (×2/3) ÷ square |
|---|---|---|---|---|
| 25° | 0.474 | 1.041 | 2.20 | 1.46 |
| 30° | 0.836 | 1.223 | 1.46 | 0.98 |
| 35° | 1.096 | 1.285 | 1.17 | 0.78 |
| 40° | 1.227 | 1.208 | 0.98 | 0.66 |
| 45° | 1.226 | 1.145 | 0.93 | 0.62 |
| 60° | 1.192 | 1.110 | 0.93 | 0.62 |
| 75° | 1.208 | 1.176 | 0.97 | 0.65 |

So under D44(a) rule 5 holds for a settee taken aback near its trim (a shift of a point or two
close-hauled), clear of the mast below about 39° and against it below about 30°, and fails for
one laid flat aback. The design:
1. B3 measures the main mast's `load_kn` per square metre of sail aback, the settee against
   her main topsail, at the incidences of her own tack (§5.5, step 2) and of a two-point shift
   close-hauled.
2. The truth pins the case that holds, saying which.
3. If neither holds, it goes to the lead and the owner with the fallback, D44(c): a `settee`
   row in `data/sail_classes.yaml` read through `curve_class` ("settee" for a settee). It changes
   no equation and no existing ship, and moves `tests/test_sails.py:65-74` (the set of curves),
   shown old beside new.

---

## 6. The drawing (`client/projection.js`; B5)

Every branch below is reached only by a new key, a `lateen_yard` with a sail cut at the mast, or
a yard under the bowsprit, so no existing ship draws differently.

### 6.1 The mizen course and its yard

- **The yard.** A new branch before the yard branch (575-617) for a `lateen_yard` whose sail is
  cut at the mast:
  - the truss at the mast (`xAt`) at deck plus the throat's height;
  - the peak swung about the mast's vertical by the sail's sheet angle to the sheet's side
    (`sheetDirection`, 164, as the gaff's is at 620-625), at the corners' run and rise;
  - the bare fore part on the same line forward of the mast by the rest of `length_m`, so it
    lies to windward as the after part lies to leeward.

  The fixed 0.8-rad tilt on a braced yard (612-616) remains only for a lateen yard with no
  such sail.
- **The sail.** The corners `[tack, throat, peak, clew]` swung about the mast the same way, in a
  branch beside the gaff's (1087-1119), which returns early without a `gaff` role (1089). The
  reef raises the foot as the gaff's does. In the gear: the gaff's brailed shape gathered to the
  mast and up under the yard (1111-1118). Furled: a bundle along the yard's after part.
- **The lifts**, alone of any ship's lifts: a `lift` of a lateen yard is drawn faint, from the
  yard's after part to the mizzen top, at the braces' opacity (1292-). The owner's one rig has
  the yard "with lifts and brails" (Bel §13.5). **Plainly:** no other lifts are drawn, since
  drawing them everywhere would change every picture.
- **The sheet** from the clew to the taffrail on the centreline.
- **A whole lateen with four corners** is drawn by `lugCut` as a standing sail on its lee side
  (`lugSideSign`, 346-353) until the tartane's change exists; one without corners as now
  (1066-1071).
- `SWINGING` (61) holds `lateen_yard` already; the fixed frame (`fullRigFrame`, 1383-1414) must
  reach the fore part's swing. A view-geometry case pins the bounds equal across states.

**As built (B5.2, 2026-10-29): the departures, each judgement.**
- The course and yard swing whole about the mast's **raked** line, not its vertical. The
  frigate's mizzen rakes 4.5°, so a vertical axis would carry the luff off the mast. The
  corners' heights shift a little at large sheet angles (on the fixture the peak rises up to
  about 0.6 m swung abeam).
- The lifts' feet are on the yard's after part: the two side lifts at 0.45 and 0.55 of it, so
  that they are not drawn on one line, and the derrick at two-thirds (Steel 1794 I p. 207: the
  derrick between the slings and the peak).
- In the gear the sheet is drawn from the clew brailed in on the bundle, not from the set clew.
  Every other sail in the gear keeps its sheet from its set clew, as before.
- A whole lateen with corners, drawn as a lug, lies on deck in the gear or furled, as a lowered
  lug does, until the tartane's package draws its own. No file carries one.
- The frame reaches the yard's swing at the heights of its two ends and of the tack and clew
  (`r.heights`), so the course stays inside it when she heels.

### 6.2 The yards under the bowsprit

- **The yard's place.** A yard whose parent is a bowsprit or jib-boom stands at its own served
  `x_m` (`api/queries.py:316-330`) at deck plus `height_m` (605). Today it stands at the
  bowsprit's heel, where the trial's spritsail hung with its foot two metres under the water
  (Eng §5). No slinging offset (only for a mast parent, 606-607).
- **The spritsail.** `squareCut` (990-1029) unchanged: with no yard below it hangs its area
  over its spread. The generator checks its foot stands above the water at heel 0 (§9.3).
- **The sprit topsail.** `yardBelowId` (432-446) finds the spritsail yard below on the same
  chain, so its clews go to the spritsail yard's arms. The drawn area is the trapezoid between
  the two yards' heights, which may fall short of the file's area (risk 9).
- **Braces** of a yard under the bowsprit lead up to the fore top (the fore mast's head less a
  metre), not level aft (1294-1302): Lavery I30's leads. **Sheets** lead aft to the side abaft
  the fore mast at deck height, not abreast the clew forward of the stem (1316-1322): I30's
  sheave in the side.

**As built (B5.3, 2026-10-29), with the lead's ruling of the same day.**
- **The bowsprit stands from the stem head.** With a profile, its heel at the stem head (or the
  rail there, if lower) as B5.1 had it, and the whole spar at the file's length up to its end's
  height above the datum; the jib-boom from its end, as before. The file serves no steeve, so
  the drawing takes the one that carries the length from the stem head to the end's height:
  32.8° on the 64 against her module's 27°, because the module roots the spar at the
  knighthead's cap, 1.24 m above the profile's stem head (Indf §3.5 item 9). Her end is drawn
  0.19 m short of the module's (1.97 m at B5.1). Without a profile, nothing changes.
- **What follows for the 64 and the razee** (B1's stage B): laying the file's bowsprit root on
  the stem head, where 1407F draws it, makes the drawn steeve her 27° with no viewer change.
  Until then the fore staysail's tack, drawn from its corners, stands about 0.6 m clear of
  the drawn bowsprit (0.04 m at B5.1).
- **The draw order and the frame.** A yard under the bowsprit and its sail are sorted at their
  own middle, not carried forward by the rake correction. The frame reaches such a yard's
  swing every way (16 points about its slings), so the view does not rescale as it is braced.
- **Judgements:** the spritsail's sheets to the side a metre abaft the fore mast at the deck
  datum; the braces to the fore mast's head less a metre, 0.3 m to their own side; the lifts to
  the head of the spar each yard hangs on. A yard filed with no `x_m` (served as 0.0) is drawn
  at its spar's x.
- **Risk 9 measured** on the 64's stood spars at the fixture's stations: the yards' heights
  differ by 4.4 m against a slant of 8.9 m, so Steel's 103 m² sprit topsail cut by the
  heights' trapezoid would be drawn at about 58 m². Before her file joins the area test, either
  the cut places the yards so that the trapezoid holds the area, or `squareCut` takes the gap
  along the slant for a yard under the bowsprit (B1 and B5, at her stage B).

### 6.3 The settee

- **`lugHoisted`** (355-358): for a settee, hoisted unless `yard_lowered`, so the yard is on deck
  only during a dip.
- **In the gear, not lowered**: the sail gathered under its yard aloft (`gathered`, 868-884).
  **Furled**: a bundle along the yard aloft. **Lowered**: on deck, as a lug.
- **The sheet** (1309-1315): from the clew to the taffrail on the centreline at rail height, in
  place of the lee rail a metre abaft (D45(c)). The stern is the hull profile's taffrail when
  the shared work's profile lands (`profileHullFigures`), else −0.52 L.
- **The sling** stays a third along throat→peak (D5(a)), which the corners' contract puts on
  the mast (§5.1).
- The vangs, ourses and derrick are not drawn, to the current standard.

### 6.4 What is served

`api/queries.py`: `settee` and `cut_at_mast` in the sail's entry (`_sail_entry`, 333-353), and
`yard_lowered` in the snapshot's sail (264-279), **each only when true**. Every existing ship's
served graph and snapshot stay as they are.

### 6.5 The pictures' tests

- `tests/test_pictures.py` (thresholds `BLANK_STD` 8.0, `DARK_LEVEL` 110, `DARK_FRACTION`
  0.001, 57-59) and every existing `tests/test_view_geometry.py` case draw as today.
- New view-geometry cases on the fixtures, then on the files:
  - the mizen yard's truss at the mast, its fore part forward of the mast and to windward, the
    frame equal across states;
  - the course brailed to the mast and furled along the yard;
  - each yard under the bowsprit at its station, every sail's foot above the water in every
    state, the sprit topsail's clews at the spritsail yard's arms within 0.1 m;
  - the settee on its corners within 0.1 m when set, gathered aloft in the gear, on deck below
    deck + 1.0 m only while `yard_lowered` (as the lug's at 763-781), its sheet at the taffrail.
- Screenshots of each state for the owner (the plan's human check after B5's first ones).

---

## 7. Everything new, in one place

| Kind | Item | Where | Inert on the eight files because |
|---|---|---|---|
| Schema keys | `SailSpec.settee`, `SailSpec.cut_at_mast`, `SparSpec.heave_to_aback` | `schema.py:359-425, 1270-1301, 1364-1424` | no file carries them (measured) |
| Runtime fields | `Sail.settee`, `Sail.cut_at_mast`, `Sail.yard_lowered`, `Spar.heave_to_aback` (class defaults) | `parts.py:170-325` | false by default |
| Property | `Sail.curve_class` | `parts.py` | equals `cls` for every sail without the key |
| Gate | `Spar.is_yard` narrowed to `yard` | `parts.py:243-248` | no file has a `lateen_yard` |
| Predicate | `Ship.under_bowsprit(part)` | `ship/graph.py` | no file has a yard rooted at a bowsprit (measured) |
| Helpers | `drives_aft`, `lugger_lugs`, `settees`, `SetteeChange`, `bowsprit_sail_lines` | `scripts.py`, `orders/storm.py` | each gives today's answer with no key, class or such yard |
| Runner | `class: settee`; `wanted_sheet(sail)` in the expressions | `runner.py:565-602, 660-686` | used only by new files |
| Routing | `evolution_key` reads `settee` | `verbs.py:419-422` | no settee |
| Evolutions, new | `set_settee`, `take_in_settee`, `furl_settee`, `dip_settee`, `set_lateen`, `take_in_lateen`, `furl_lateen`, `reef_lateen`, `shake_out_lateen`, `trim_lateen_sheet` | `data/evolutions/` | apply to no existing sail |
| Vocabulary | settee and lateen rows; `take_in_words` for both | `vocabulary.yaml:1749-1886` | classes and keys no file has |
| Tables | `PEAK_COEFF["lateen"] = 1.25`; `_spar_weight["lateen_yard"] = 2.0` | `gen_ships.py:135`; `combat/hits.py:509-524` | indexed only by key |
| Served fields | `settee`, `cut_at_mast`, `yard_lowered`, only when true | `api/queries.py:264-279, 333-353` | absent otherwise |
| Viewer branches | §6 | `client/projection.js` | keyed on the same |

No new sail class, spar class, line class, station or physics term.

---

## 8. Stage 0: the interfaces (before the worktrees fork)

Each item is inert: no file, scenario or path uses it until a builder does. It lets the ship
builders write the new keys and generate their files while B3 builds the behaviour.

*Settled by `Build-Ships.md` (§3, decisions 4 and 22):* these items are laid as **stage 0E**,
after the lead approves this document and before B3 starts. Item 3, the property's first form
(`curve_class` returning `cls`) and the `curve_class` lookups at `world/ships.py:391`,
`api/queries.py:334` and `api/readings.py:873` go into the package's first stage 0, where they
are inert, because those files have other owners; 0E widens the property for a sail cut at the
mast.

1. **Schema** (`ship/schema.py`): `SailSpec.settee` and `SailSpec.cut_at_mast` with their
   refusals (§3.1, §5.2), parsed in `_parse_sail` (1364-1424); `SparSpec.heave_to_aback`, parsed
   in `_parse_spar` (1270-1301), refused off a lower mast and on a second mast (in `validate`,
   1488-).
2. **Runtime** (`ship/parts.py`): `Sail.settee`, `Sail.cut_at_mast`, `Sail.yard_lowered`,
   `Spar.heave_to_aback`, plain class defaults, the first two and the last copied in
   `from_spec`; the property `Sail.curve_class`.
3. **Generator** (`tools/gen_ships.py`): `PEAK_COEFF["lateen"] = 1.25` (135); the rating pass's
   entry reads `sail.curve_class` (869). A module that writes a cut lateen then generates and
   rates at the gaff's 1.29 from its first commit.
4. **The predicate** `Ship.under_bowsprit(part)` (`ship/graph.py`), defined, not called.
5. **Runner** (`evolutions/runner.py`): `class: settee` in `_check_applies` (565-602);
   `wanted_sheet(sail)` in the expression functions (660-686). No evolution uses them yet.
6. **Served fields** (`api/queries.py`): `settee`, `cut_at_mast`, `yard_lowered`, only when
   true, so B5 can draw from the fixtures.
7. **Fixtures** `tests/rig_fixtures.py`, built in memory from the committed files on the
   pattern of `tests/messages_api.py`:
   - `frigate_with_mizen_yard()`: the frigate's spanker replaced by a lateen cut at the mast on
     a `lateen_yard`, with a spritsail yard on the bowsprit and a sprit-topsail yard on the
     jib-boom, each with a square sail;
   - `brig_with_settee()`: the brig hull with a settee cut to D5(a)'s proportions, the dry main
     yard and main topsail, `heave_to_aback` on the main (Eng §4.4's variant with its two faults
     corrected).
8. **The guards** `tests/test_rig_classing.py`:
   - the golden classing table of the eight files (§10.1), measured at this head;
   - a probe that no file carries `settee`, `cut_at_mast`, `heave_to_aback`, a `lateen_yard` or a
     yard rooted at a bowsprit;
   - the schema's refusals of the three keys, and that each fixture loads.

**Checks**, by an agent that did not write it: the eight files byte-identical
(`tests/test_ship_particulars.py:555-581`); the fast tier green; the guards green.

**Plainly:** the golden table and the fixtures are tests, not behaviour. They are laid in stage
0 so that each of B3's steps proves against the same table that it moved nothing.

---

## 9. Build order, ownership, contracts

### 9.1 The engine builder (B3), three steps in this order

Each step is committed, reviewed by its lenses and merged before the next. All three edit
`evolutions/scripts.py`, `orders/verbs.py` and the vocabulary, so they are not run in parallel.

1. **B3.1, the lateen** (§3), for the 64 first:
   - `parts.py` (`is_yard`); the nine `curve_class` lookups in its own files (§3.1; the other
     four are stage 0's: `Build-Ships.md` §3.1);
   - `scripts.py` (`drives_aft` in `boom_sails`, `after_gaff_sails`, `_after_sail`,
     `after_gaff_sails_all`; the words at 6135 and 7265; `HANDING_EVOLUTIONS`);
   - `verbs.py` (1561's hint); `combat/hits.py`;
   - the six lateen data files and the vocabulary rows;
   - `tests/test_lateen.py`.
2. **B3.2, the yards under the bowsprit** (§4): the nine places of §4.2 in `scripts.py`,
   `trim.py`, `verbs.py`, `orders/storm.py`, `orders/__init__.py` and `physics/sails.py`;
   `tests/test_bowsprit_yards.py`. Then the pace measured (§10.4), since the helm's mark is a
   per-substep path.
3. **B3.3, the settee** (§5): `verbs.py` (routing, take-in words); `scripts.py` (`lugger_lugs`,
   `settees`, `SetteeChange`, the tack, the wear, the heave-to, `_lugs_all`,
   `after_gaff_sails_all`, `yards_to_back`); the four settee data files and the vocabulary;
   `tests/test_settee.py`.

*Since (2026-10-28):* B3.4 is D10(a)'s key (`Build-Ships.md` decision 34), and **B3.5, the
driver**, taken by the owner and the lead (§17.9 item 1): `_in_each_others_place` in `scripts.py` and
`_in_its_place` in `orders/storm.py`; `tests/test_driver.py`. It follows B3.1 at a step
boundary, as these (§17.8).

### 9.2 The viewer builder (B5)

Draws §6 after each of B3's steps lands, from the fixtures first and the files when they
exist, and owns the new `tests/test_view_geometry.py` cases. **The same builder should draw the
hull profile** (the shared work's drawing), since both work inside `buildSkeleton`
(`projection.js:273-1377`): the profile edits the lower masts' feet and the bowsprit's heel
(501-533), the rig branches here the yards, sails and lines (542-640, 1043-1344). Two builders
there would collide.

### 9.3 The ship builders' contracts

The ship builders own their `tools/ships/` modules and their `data/people/` files; no ship
builder edits an engine file (a need goes back to the stage-0 agent). Three small helper
modules hold the cuts, each pure (numbers in, dicts out) and **importing nothing from
`gen_ships`**, so the second copy of the generator (map-generator §1.10) never arises from them:

| Module | Written by | Gives | Asserts at generation |
|---|---|---|---|
| `tools/ships/mizen_yard.py` | B1 (the 64), imported by the 74's builder | the yard, the course cut at the mast from Steel's cloths and leeches, the lines of §3.4 | the tack and throat on the mast's raked line within 0.1 m; the head along the yard; the area within 10% of Steel's (Ind §5) |
| `tools/ships/spritsail_yards.py` | B1, imported by the 74's builder and B4 | the two yards at their stations from the bowsprit's steeve and length, their sails and lines (§4.1) | each yard's height above the deck below the bowsprit's line; the sprit-topsail yard above the spritsail yard; every foot above the water |
| `tools/ships/settee.py` | B4 | the settee's corners to D5(a), its area and centre, the lines of §5.1 | the third along throat→peak on the main mast's line within 0.1 m; the peak inside the taffrail; one unsided sheet |

Every contract: heights above the deck in `corners_m` and `height_m`, centres above the water;
`mizzen.` and `main.` ids; no brace on a lateen yard; the settee in "courses" and never in
"gaff sails"; the spritsails out of "plain sail".

### 9.4 Who waits for whom

- The razee (a gaff mizen by 1796: Ind §3.3) and the *Neufchatel* wait for nothing here.
- The 64's and the 74's files generate after stage 0 on their stand-ins; their mizen yards and
  spritsail yards after stage 0E (§8). Their handling tests and truth wait for B3.1 and B3.2.
- The bilander's file generates after stage 0E, which lays the settee's keys. Her handling
  truths wait for B3.3.

---

## 10. Tests and truths

### 10.1 The guard set

**The golden classing table** (observed, `risk/classing_table.py` re-run; plain sail set), which
`tests/test_rig_classing.py` holds:

| File | Masts with yards | Head / after | Backed | Square-rigged | Stagger | Driver | Boom sails | Lugger's dipping lugs |
|---|---|---|---|---|---|---|---|---|
| frigate-36 | fore, main, mizzen | 4 / 8 | main | yes | +2.0° | mizzen.spanker | mizzen.spanker | — |
| brig | fore, main | 4 / 4 | main | yes | +2.0° | main.spanker | main.spanker | — |
| merchant-brig | fore, main | 4 / 4 | main | yes | +2.0° | main.spanker | main.spanker | — |
| cutter | main | 3 / 0 | main | no | — | — | main.sail | — |
| topsail-schooner | fore | 2 / 0 | fore | no | — | — | main.sail | — |
| privateer-schooner | fore | 2 / 0 | fore | no | — | — | main.sail | — |
| smack | main | 2 / 0 | main | no | — | — | main.sail | — |
| lugger | none | 0 / 0 | — | no | — | — | mizen.lug | fore.lug, main.lug |

**Beyond the fast tier**, each step runs:
- *the lugger's*: `tests/test_lug.py`; truth 7b-111 (`test_known_truths.py:6186`) and her
  getting under way (7256-); `test_captains.py:583-588`; the lug cases of
  `test_view_geometry.py` (728-826);
- *the classing's*: `test_rig_classing.py`; `test_gale.py`, `test_rig_geometry.py`,
  `test_staying.py`, `test_lying_to.py`, `test_evolutions.py`, `test_captain_trials.py`, and the
  truths that tack, wear or heave to the frigate and the brig;
- *the catalogue's*: `test_catalogue.py` (the pinned timings, the crew lines, the aloft flags);
- *the generator's*: `test_ship_particulars.py:555-581`;
- *a trace*, a lens check rather than a test: the lugger's tack and wear and the frigate's tack
  and heave-to at seed 7, their log lines and ticks compared before and after each step.

### 10.2 The engine's tests (B3)

On the fixtures, then on the files when they land.

- **`tests/test_lateen.py`** (B3.1):
  - no order braces the lateen yard: "brace the mizen yard" refused with the vangs' words;
    "square the yards", "brace sharp up", "trim sails", the polar's trim and the promotion's
    trim leave it at 0;
  - the course's sheet within the gaff's 18-85° by every route: set, trim, `trim sails`,
    `draw_sheets`, the hove-to driver, the polar;
  - hauled aft at helm's a-lee; brailed up hove to; brailed at "up helm" and hauled out by the
    wind; taken in at the gale's third reef; set after the cast;
  - each lateen evolution runs to its end; "furl the mizen" furls it aloft; "brail up the
    mizen" is accepted;
  - a whole lateen (no key) loads, sets, brails and furls on the lateen's floor, and is no
    driver and no boom sail;
  - the rating pass rates a cut lateen at 1.29;
  - the classing of the fixture equals the frigate's row of §10.1.
- **`tests/test_bowsprit_yards.py`** (B3.2):
  - with the yards added, every field of the frigate's, the brig's and the topsail schooner's
    rows equals the row as filed;
  - the head yards include them, and "mainsail haul" swings the main and mizzen yards only;
  - hove to their sails are clewed up; `shorten sail` takes them in first;
  - the helm's mark is never a sail under the bowsprit;
  - the polar is unchanged with them out of "plain sail";
  - set at 150° off in 15 kn their thrust is ahead;
  - `under_bowsprit` is false for every jib.
- **`tests/test_settee.py`** (B3.3):
  - the routing: set, take in, furl and dip to the settee's files; reef, trim, bend, unbend and
    shift to the lug's; "lower the mainsail" refused with "clew up";
  - clewed up aloft keeps `yard_lowered` false; only a dip sets it;
  - she is no lugger: `_lugs_all` empty, the ship's start words, no storm lug;
  - getting under way, the settee set after the cast;
  - the gale: reefed at the second reef, taken in at the third;
  - the untried manoeuvres each run to an end or refuse in words;
  - every settee request begins with her company of eight;
  - the lugger's every path gives the same log lines and ticks (the trace).

### 10.3 The truth candidates (numbered by the build document within 7-185 to 7-199)

*Numbered by `Build-Ships.md` §15:* item 1 is 7-198, with item 3's rule 5 as its clause if the
measure holds; item 2 is 7-199; item 3's rule 1 is a clause of the bilander's particulars,
7-197; item 4 is 7-189, the *Indefatigable*'s, at her stage B.

Each is measured on B4's or B1's file at seed 7, never on the trial's scratch vessels (D46).
Each pins states, counts, orders of events, ticks and bands, never a digest. Each judges her by
her heading and tack a set time after, never by the "Tacked" line (D13(a)). Each says that its
rule is carried over from a ship's mizen, the lug or the lateen by judgement.

1. **The settee in stays is kept drawing, its ourse to leeward, and dipped last** (D46 rules 2
   and 3; D3(b)). From close-hauled in 15 and 20 kn:
   - at helm's a-lee + 1 tick the settee is set, its sheet within 1° of its floor, and the log
     carries "haul aft the mainsail sheet and brace the ourse to leeward";
   - `yard_lowered` is first true at or after the tick the head yards' swing ends;
   - it stays true for a band of ticks about `settee_dip_s` by her crew factor, and `lug_side`
     passes from the old lee to the new;
   - the tack's end is not before the hoist tick;
   - at a set time after helm's a-lee she is on the new tack within a band of close-hauled.
2. **In wearing the settee is lowered as she bears up and hoisted on the new lee once the stern
   is past the wind** (rule 4 as reworded): `yard_lowered` true within a band of ticks after "up
   helm"; at the hoist tick the wind is on the new side of the stern; she comes to by the wind
   on the new tack within a band at a set time.
3. **By the wind she lies as close as a brig, and aback the settee bears on its mast as the
   tables allow** (rules 1 and 5): her polar's `closest_deg` and `beat_deg(15)` no wider than
   the brig's 50° and 60°; rule 5's case per §5.10, or this half of the truth goes to the lead.
4. *(Offered to the Indefatigable's share.)* **The 64 handles as a ship with her mizen yard and
   her spritsails**: her classing as the frigate's row; "mainsail haul" swings the main and
   mizzen yards only; the mizen yard never braced; the mizen course hauled aft at helm's a-lee
   and brailed up hove to; the spritsails clewed up hove to; she lies to within truth 12's band.

The bilander's heave-to (D4(a)) is a test, not a truth: no source says how a bilander lay to
(Bil §4).

### 10.4 Pace and checkpoints

- The per-tick additions: one `curve_class` read a sail in `_read_rig`, the driving sails' curve
  and the idle sails' furled windage (held for the tick's four substeps; B3.1's review), one predicate per square sail in the helm's mark, one clause in
  `boom_sails`. The settee's change runs only in a manoeuvre.
- Measured with `tools/pace.py` alone and crewed, before and after B3.1 and B3.2, the runs
  alternated (Eng §2.7's first-world artifact). The floors stand: `BUILD_MACHINE_FLOOR` 500
  (`tests/test_known_truths.py:2143-2162`), `CREWED_FLOOR_TICKS_S` 60 (`world/crews.py:88-91`).
  The pace tests are the lead's on the build machine.
- **Measured after B3.2 (2026-10-29), on the owner's machine**, 90eb601 against the tree, three
  alternated pairs, ticks a second: the frigate alone 481/477/474 against 475/469/489; crewed
  with 1 ship 262/242/241 against 227/237/241, 3 ships 164/148/147 against 141/147/148, 6 ships
  64/65/65 against 62/64/65, 12 ships 37/37/38 against 36/37/37. `compute_sail_forces` about
  472 µs a call against 476-487. Within the runs' noise; the predicate cost about 0.5% a tick
  before it was held once a tick, a quarter of the calls since. Below the floors on both
  trees, as this machine always is: the build machine's figures are the lead's.
- Every new field has a class default, as package 37m's script fields have
  (`scripts.py:962-970`), so an old checkpoint loads.

---

## 11. Pins expected to move, and the proof

**None.** Every change is keyed on a key, class or root that none of the eight files carries
(§7's last column; the probe of §8 item 8). The two refactors that run on existing paths:
- `LugDip`'s ids from `lugger_lugs`: for a ship with no settee, today's set;
- the heave-to's lowering from `lugger_lugs` and its word list: for no settee, today's.

**The proof**: the byte-identity test; the golden classing table; the lugger's guard set and the
trace; the fast tier and the touched files' slow tier on the final tree.

**Two moves that could come, each shown old beside new with the reason and a bisection if they
do:**
- `tests/test_sails.py:65-74` (the set of curves), only if rule 5 fails and a `settee` row is
  added (§5.10);
- `tests/test_view_geometry.py:572-602` (each square sail drawn to its file's area within 5%),
  only if the new files are added to its list and the sprit topsail's trapezoid falls short
  (risk 9). The remedy is the drawing's or the cut's, never a sail left out of the test.

**Moved at B3.1 (2026-10-29), not foreseen:** `tests/test_agents.py:1873`, the library's count
of evolutions in its contents, 98 → 104. Cause: §3.6's six lateen files, served in every ship's
catalogue as the lug's six have been since package 43b. A count of data files, not behaviour;
moved old beside new by the session in its own commit, as package 86 moved it
(`docs/dev/M7-WorkPackages.md:381`), for the lead's ruling at the merge. B3.3's four settee
files take it to 108.

---

## 12. Review lenses

1. **The gate.** `physics/` holds only the lookups and memberships of §1; no `_plate_force`
   line, curve row or load fraction changes.
2. **The lugger.** Every path of §5.4 walked with the lugger and the bilander; her guard set and
   trace unchanged.
3. **Classing.** For each new rig, every place of §4.2 printed beside the rule; for the eight
   files, the golden table.
4. **Sailing.** D46's truths; the 64's and the 74's mizen in stays, hove to and wearing against
   the *Bellona*'s reports (Bel §13.2: wears and stays quickly; lies to under the mainsail and
   mizen staysail); the spritsail large and by the wind against Lever.
5. **Sources and words.** Every new time, crew and step marked as sourced or judgement; the
   period's words: "haul out the mizen", "brail up", "clew up", "dip", "ourse", "vangs",
   "spritsail"; singular words for one settee; each Plainly justified. Private books give facts
   and figure numbers only.
6. **The viewer.** Drawing against physics (the settee's corners, the mizen yard's side, the sprit
   sails' feet); screenshots in each state at three facings; the pictures' thresholds unmoved.
7. **84's names, pace and checkpoints.** No `world.ship` or `CrewedWorld` in the diff; the pace
   measured; an old checkpoint loads.

---

## 13. Risks, ranked

1. **A lug-keyed path missed** for the settee (Eng risk 1). Getting under way failed outright in
   the trial. *Mitigation*: §5.4's table; the untried manoeuvres run once each; every guard keyed
   on `settee` alone, so the lugger cannot move.
2. **D4(a)'s lie.** With the settee clewed up and her main aback she may fall off as the trial
   did (79-87° by 300 s). *Mitigation*: measured both ways before any pin (§5.7).
3. **Rule 5 fails as the tables predict** for a settee laid flat aback (§5.10). *Mitigation*:
   measured first; the fallback is the lead's and the owner's.
4. **A `curve_class` lookup missed** gives the mizen course the lateen's 8° floor on one path and
   the gaff's 18° on another. *Mitigation*: the nine in B3.1's commit, the other four in stage 0, where they are
   inert; a test of every route.
5. **A classing place missed** for the yards under the bowsprit: the brig's "mainsail haul"
   swings her fore yards, or the schooner heaves to as a square-rigger. *Mitigation*: the golden
   table on the three fixtures; the 64's truth.
6. **The mizen course untuned as a driver.** Hauled aft at helm's a-lee at the gaff's 18° floor
   with no boom, on two ships no truth yet covers. *Mitigation*: the sailing lens against the
   *Bellona*'s report that she stayed quickly (Bel §13.2); the 64's truth.
7. **Drawing and physics disagree** if a module cuts corners off the mast. *Mitigation*: the
   helpers' assertions (§9.3) and the view tests.
8. **The settee's sheet** on a 0.8√A foot may lead well short of the taffrail (D45(c)).
   *Mitigation*: B4's check; the reserve branch (§5.9).
9. **The sprit topsail's drawn area** between yards whose heights differ less than its depth
   (the 64's sail is 9 yards deep: Ind §5). *Mitigation*: the cut places the yards so the
   trapezoid holds the area, or B5 draws it along the slant; checked before the files join the
   view test's list.
10. **The company of eight** against six-hand requests at a dip (D43). *Mitigation*: B4 gives her
    a main-top pair and measures the dip at her company.
11. **The false "Tacked"** on her brig-like hull (D13). *Mitigation*: every truth judges by
    heading.
12. **`projection.js`** shared by the hull's drawing and the three rig drawings. *Mitigation*:
    one viewer builder (§9.2).
13. **The spritsails set by a captain's "make all sail" by the wind** draw aback (−0.12 kN at 60°
    off). *Mitigation*: out of "plain sail"; taken in first when sail is shortened; noted for the
    captains' lens.

---

## 14. Open for the owner or the lead

1. **The mizen course's class** (E1, E2): class lateen cut at the mast, reading the gaff's curve
   through `curve_class`, against a gaff sail hung from a lateen yard. Bel §13.5 left it to this
   document. The lead's gate.
2. **The physics' readings** (§1): `curve_class` at thirteen lookups; `_square_rigged`, the
   helm's mark and `_spar_x` leaving out the yards under the bowsprit. The lead to confirm they
   sit within "the physics' equations are not changed".
3. **D4(a)'s settee clewed up when hove to**, against the engine's driver rule, if the figures
   differ (§5.7).
4. **Rule 5**: which case is pinned; if neither holds, a `settee` curve row (D44(c)) or the rule
   recorded as measured with no truth (§5.10).
5. **"Furl the mizen" furls it aloft** (E6), while a gaff sail keeps package 37l's refusal.
6. **D3(b)'s timing**: the dip begins when the head yards' swing ends (§5.5).
7. **The settee's times and hands**, all judgement: 120 s in a manoeuvre, `dip_settee`'s 180 s,
   requests of six.
8. **The spritsails** out of "plain sail" and taken in first; their topping, traveller and
   diagonal reefs not modelled; the fore top's men, not the forecastle's, at their yards (§4.3,
   §4.4).
9. **The lifts drawn on a lateen yard only** (§6.1).
10. **The 74's driver** of 1773, set abaft the mizen course without a boom (Lavery Table 15; Bel
    §13.5): no engine path hangs a sail from another sail's yard (`graph.py:85-92` returns a
    yard's first sail; `_gaff_host` needs a boom, `sails.py:947-961`). The 74's design leaves it
    out or asks for it. *Reopened by the owner (2026-10-28), who asked for the driver
    (`Build-Ships.md` §19.1 item 13):* §17 proposes Steel's driver boomsail of 1794 for the 64
    and the 74, bent on a boom in the mizen course's place, rather than the 1773 sail that item
    describes. The owner chose it for both (2026-10-28; §17.9 item 1); it waits on the lead's read.
11. **The truths' share**: three numbers for the settee (D46(d) with rule 3), and the 64's offered
    to the Indefatigable's (§10.3).
12. **D10(a)'s key** for the *Neufchatel*'s main topgallant ("yards the handling ignores") would
    sit beside `under_bowsprit` at places 1 and 3 of §4.2; it is her design's.
13. **The tartane's full lateen**, dipped or changed by *muder*, and its curve, in a later
    package (§3.7).
14. **D18 and D25** stay open; nothing here depends on them.

---

## 15. What was taken from each draft

Three drafts were judged: reuse first, fidelity first, and risk and test first.

- **The mizen course's class.** The risk draft's lateen with a key and the gaff's curve, over the
  reuse draft's lateen curve and the fidelity draft's gaff sail on a yard. The fidelity draft
  departs from D9(c) and the ruling's "lateen class finished"; the reuse draft from the owner's
  "in the physics like the gaff sail". The measurement decides between curves (§3.2).
- **The lateen's evolutions.** Their own class-named files (risk) over widening the gaff's files
  with a list `applies_to` (reuse): the engine's and the vocabulary's names are by class.
  "Furl the mizen" aloft (risk) over the gaff's refusal (reuse, fidelity): Falconer's woldings.
- **No schema refusal of a brace on a lateen yard** (against the risk draft): a tartane's lateen
  yard has a peak brace.
- **The yards under the bowsprit.** The reuse draft's predicate with the yards among the head
  yards, and the square evolutions reused; the risk draft's added places (`trim sails`' lowest
  yard, `_spar_x`); the fidelity draft's spritsail evolutions and topped state not taken (a
  runtime state and six files for what a horizontal brace stands in for). `shorten sail`'s first
  line is new here.
- **`TOP_OF_MAST`** left as it is (reuse) rather than mapped to the fore top (risk): the fallback
  already gives the fore top first, so the mapping changes nothing.
- **The settee.** All three take D2(a). `dip_settee` of its own and `yard_lowered` (risk) over
  editing `dip_lug` (reuse, fidelity). The time in code (risk) over a key in `tack.yaml`
  (fidelity), which `test_catalogue.py` pins. A course in the gale (reuse, fidelity) over a
  driver (risk). The heave-to's mast key (risk) over a group of yards (reuse) and a ship-level
  block (fidelity): D4(a) names the mast. D4(a)'s clewing up kept (reuse, fidelity) with the
  risk draft's measure-both. The wear's hoist gated on the wind past the stern (new, stricter than
  the reuse draft's time alone).
- **The ropes.** Heel ropes as `guy` (reuse, risk) over `vang` (fidelity).
- **Stage 0.** Inert stubs (reuse, fidelity, and the plan) with the risk draft's golden table and
  fixtures; the classing and curve wiring left to B3's steps, not stage 0 (against the risk
  draft).
- **Builders.** One engine builder in three steps (reuse, fidelity) over three in parallel (risk).
- **Rule 5** measured first (reuse); the period handling of §2 and the cut arithmetic (fidelity).

---

## 16. Found on the way

1. `data/vocabulary.yaml:1757, 1766` map set and take in on a sprit sail to files that do not
   exist, and `trim: sprit` (1859) to `trim_gaff_sheet`, which refuses it. No ship of this
   package carries a sprit sail; left, and `PEAK_COEFF` gains no "sprit" entry here.
2. `orders/verbs.py:1572-1573` returns the spar of any brace line without checking `is_yard`. The
   lugger's lug topsail yards carry braces (`lugger.yaml`), so a check there would change her
   answers. Left.
3. `evolutions/repair_scripts.py:59` `SLING_SPAR_CLASSES` lacks `lateen_yard` and `lug_yard`, so
   "rig preventers to the slings" passes over the mizen yard. No source found for slinging it.
4. A spritsail yard on the topsail schooner at this head would put her foresail in
   `after_gaff_sails_all` and set it after the cast as a ship's spanker (Eng §5's classing, read
   through 7354-7365). §4.2 removes it.
5. `PEAK_COEFF["studding"]` is 1.25 against the curve's 1.44 (map-engine §10). Not this package's
   to change silently.
6. (B3.1) `physics/strain.py:631` says a yard carried away "in the slings" only for `is_yard`.
   The lateen yard, out of `is_yard` now (§3.3), carries away without the words, though it is
   slung. No existing file has a lateen yard. For the lead under the gate: a membership
   (`spar.is_yard or spar.cls == "lateen_yard"`), or accepted as it stands.
7. (B3.1) At tick 0 the served `ship.tack` is "starboard" whatever the wind: `ShipDynamics.tack`
   reads the apparent wind, which is 0 until the first tick. A page drawing the first snapshot
   puts the fore-and-aft sails to larboard until then. Not this package's.
8. (B3.1) `set_lateen` checks no boom. The driver on its boom (§17.3), set by it, gains
   `not wrecked(spar_of_role(sail, boom))` at B3.5, with its case in `tests/test_driver.py`.
9. (B3.2) "Brace the spritsail yard aback" answers that the spritsail and sprit topsail are
   "to the mast" (`orders/verbs.py:802-806`), though no mast carries them. Outside §4.2's nine
   places; for the lead.
10. (B3.2) Nothing refuses a yard under the bowsprit filed without `x_m`: it defaults to 0.0,
    and place 9 puts its windage amidships. §4.1's contract and B1's helper give it; a refusal
    in `schema.py` is stage 0's, if wanted.
11. (B5.3) Older than this package: the frame's four directions let the view rescale between
    tacks at the diagonal facings, through the swing of booms, gaffs and the ringtail boom, on
    nine of the ten files (worst 2.4-5.0 m of bounds; the same on 90eb601's and the tree's
    `projection.js`). The yards under the bowsprit take sixteen points; the rest is B5's, later.

---

## 17. Addendum (2026-10-28): the driver of the 64 and the 74

**Why.** The owner asked for the occasional driver of the 64 and the 74 (`Build-Ships.md` §19.1
item 13), which §14 item 10 had left out. The lead's ruling (`docs/dev/M7-WorkPackages.md`, the
notes from the lead, "stage 0 read", item 4) asks for this addendum and reads it with the gate's
lens: the physics' ranges byte-identical, the sail's curve an existing class's, `_gaff_host`'s
new host a membership and not an equation, and the frigate's polar re-measured equal. Stage 0E
and B1 do not wait on it.

**Marks** as at the head of this document. The scratch scripts are kept outside the repository
in the session's scratch folder `stage0e/` (`driver_geom.py`, `driver_cut.py`,
`driver_polar.py`, `driver_polar2.py`, and for the four-cornered cut `mend17/driver_four.py`
and `mend17/driver_polar4.py`). They were run from the tree root at 5326e24, with stage
0E's edits in the working tree; no file of the eight reaches those edits. Nothing is built.
The *Indefatigable*'s design (`Design-Ship-Indefatigable.md`) is **Indf**. Lever 1808 is read
in its 1827 printing (`docs/references/README.md`).

**In brief.**
- **The sail.** Chosen by the owner for both ships (2026-10-28; §17.9 item 1): Steel's
  **driver boomsail** of 1794, "the driver or spanker" (§17.1). It is a four-sided sail. Its
  luff is on the mizzen mast, its head runs along the mizen yard's line and on past the
  yard's peak on Steel's small driver yard, and its foot is on a boom over the stern. It is
  not the 1773 driver, which hung from the peak on its own yard abaft a set course, and which
  the owner's item describes.
- **Beside the course, or in its place.** For these ships the period bent the driver beside
  the mizen course, the course brailed up while the driver drew (§17.3). The model bends it
  in the course's place instead, one shifted for the other in a thirteen-minute shift, by
  choice (§17.3).
- **The model.** The driver is class `lateen` with `cut_at_mast: true`, the course's own
  class and key. Its roles are `yard`, `mast` and a new optional `boom`. It is filed
  `in_place_of: mizzen.course` and starts in the sail room. A `boom` spar is added on the
  mizzen mast. This is the storm trysail's pattern (a sail bent to the same spars in the
  working sail's place), not the ringtail's.
- **The engine.**
  - Nothing in `freesail/physics/` or `data/sail_classes.yaml` changes, not even a lookup:
    every physics path reads the boom by its role (§17.4).
  - `_gaff_host` is not touched, since the driver is no ringtail.
  - One schema allowance: a lateen cut at the mast may name a boom.
  - One handling membership: two sails bent in one place are rivals, so the storm mizzen and
    the driver are never bent together.
- **Observed.** The frigate's spanker, re-filed in memory as the driver's model, gives her
  polar and her sails' yaw moment equal at every angle (§17.5).
- **Who.** Once the lead has read this (the owner has chosen the sail), the stage-0 agent
  lays the allowance. B3 adds one small step after B3.1, and B5 draws the sail. B1 writes it
  into `mizen_yard.py` behind a flip of its own at the 64's stage B, and B7 imports it
  (§17.8).

### 17.1 Which sail, from the evidence

Two sails go by the name:
- **(a) The older driver.** An oblong sail on its own yard, hoisted to the mizen peak "when
  the wind is very fair". Its lower corners are spread on a pole over the lee quarter or the
  taffrail. Sources: Falconer 1780, DRIVER, OCR l. 6843-6846; Röding 1794 vol. I, OCR
  l. 72694-72718; Lever 1808, OCR l. 8264-8270, as the merchant service's way. It hangs abaft
  the course, which stays set.
- **(b) Steel's driver boomsail.** Quadrilateral, "occasionally hoisted to the mizen-yard or
  gaff, in light fair winds" (Steel 1794 vol. I, DRIVER BOOMSAIL, OCR l. 13816-13843).
  - Its fore leech is laced to the mizen mast, its head to the yard or gaff, and its foot is
    on a boom fore and aft.
  - The fore leech is as deep as the mizen course's, and the after leech two to four yards
    deeper.
  - The driver yard "expands the head of the driver without the peek of the gaff" (l. 20863).
  - It is bent "as a temporary matter" by four or five pair of halyards to the yard or gaff,
    its tack to the eye-bolt in the throat of the boom and its sheet through the boom's outer
    end; or "instead of the mizen, it bends exactly the same, only the foot of the sail is
    extended on the boom" (l. 24523-24538). Both ways spread the foot on the boom. That the
    first leaves the mizen bent beside it is judgement, with Lever's plate key (§17.3).

**For the owner, plainly.** The driver is a large four-sided sail on the aftermost mast. Its
front edge is laced to the mast, its top edge hangs along the slanting mizen yard and runs on
past the yard's end on a short extra yard, and its bottom edge is stretched along a long pole,
the boom, that reaches out over the stern. In these ships' day it was bent beside the mizen
course, which was brailed up while the driver drew. In the game it lives in the sail room and
is shifted for the mizen course, about thirteen minutes' work, when the wind is fair and
moderate, giving her about twice the sail aft. Shifting one for the other is the game's choice,
so that only one after sail is ever bent (§17.3). It comes in before it blows hard or when the
wind is right astern.

**The evidence, by date** (the session's research of 2026-10-28; the marks as found):

| Date | Source | Which sail |
|---|---|---|
| 1773 | Lavery 1985, Table 15 (p. 21): 19 and 27 cloths, 21 yd deep, canvas sort 6, 483 yd of canvas, listed after the steering sails. 483 = 23 × 21, a uniform depth, so it was cut as a studding sail is (measured); the same table's mizen course does not check so. On I32 the throat stands about 42 ft above the deck, so a 63-ft leech could not hang at the mast below it (measured): it hung from the peak. I31 does not draw it | (a); read (owner's book), measured |
| 1780, 1794 | Falconer, DRIVER (and OCR l. 2897-2900, 15944-15946, 20452-20453); Röding: rather a studding sail, set before the wind at the head of the mizen yard or gaff, its sheet on a spar over the quarter gallery | (a); read |
| 1794 | Steel's Table IV cuts the 64's and the 74's drivers (the two columns read) to the DRIVER BOOMSAIL rule: the 64's fore leech 9½ yd against her mizen's 9¼, after leech 20 against 17¼ (Ind §5); the 74's 11 against 11, 24 against 21 (Bel §5.6). Elsewhere drivers are boom-and-gaff sails (OCR l. 9800-9801) and the "driver boom sail" of the mizen mast (l. 9960). The rigging runs from the mizen yard, used "in ships above 50 guns" (l. 23039-23041), to the "DRIVER or SPANKER-BOOM" (l. 23103-23118) | (b); read, Table IV from the page images, not re-read here |
| 1794-98 | "Spanker" and "driver" are one sail (Steel l. 24523; Lever l. 8272). *Orion* (74), 1 June 1794: "Mizen yard shot in two in the slings" and her spanker boom wounded, a lateen yard and a boom together (Jackson, *Logs* vol. 1, OCR l. 8189-8196). *Audacious* (74) set the spanker in fresh breezes (l. 7221-7231). *Alexander*'s spanker boom shot away, November 1794 (James vol. 1, OCR l. 15786). *Lancaster* (64), 11 October 1797: cross-jack yard and spanker boom shot away (Jackson vol. 1, l. 21330-21331, 21351). *Agamemnon* (64), 13 March 1795, in a chase on or near a wind: "the driver and after-sails to be braced up and shivered" (Nicolas vol. 2, OCR l. 3193, 3212-3213, 32041; on a wind is judgement). At the Nile (Jackson vol. 2): *Vanguard* "Set driver" in moderate breezes, then set the mainsail and hauled to the wind (l. 2700-2702; her point of sailing before is not given); *Goliath*'s driver cut away (l. 606-608); *Majestic* lost "one mizen" and "one driver" with her main and mizen masts (l. 3683-3688; both bent is judgement); *Culloden* brailed her spanker (l. 4063-4064) | (b); read |
| 1808 | Lever gives the merchant sail of (a), then "The DRIVER or SPANKER is now cut Mainsail Fashion: and, in this case, it is spread by a Boom". It "acts as a large Mizen", the after part of its head bent to a yard because the gaff will not spread it (OCR l. 8272-8285). The plate key reads "The Driver or Spanker with the Mizen brailed up" (l. 6276-6277) | (b); read |

**Against (b):**
- Steel's p. 49 spar columns give the 64 and the 74 a driver boom of "0 0" (Ind §3.1; Bel
  §5.3-§5.4). The driver yard is not in that table, only in the p. 40 rule (as the fore
  topgallant yard).
- Steel's vol. II rigging lists rig a boomless driver: two pair of halyards, two sheets, two
  tacks and a downhauler (the 74's at OCR l. 23831-23833, the 64's at l. 24844-24847). But the
  same lists rig a lateen mizen yard for the 38 and the 50/44 (l. 26904, 26935-26944, 25832),
  whose spar columns carry a gaff and a driver boom. So the lists read as an older pattern and
  weigh little (judgement).
- Steel's plate of a 20-gun ship groups its driver with the square sails (vol. I, l. 23657,
  23730-23732, 23773). The plate itself has not been seen.

**The verdict:**
- **The 64 of her dates, 1784-1794** (her file is the 64 of 1784, rigged by Steel's tables of
  1794, with the fits "ardent class 1784" and "ardent class 1794": Indf, "Decisions taken",
  10 and 16): **(b), low confidence.**
  - For: Table IV's cut of her own column, and the 74s' booms of 1794 beside their lateen
    mizen yards (*Orion*, *Alexander*).
  - Against: Steel's 64 column has no boom ("0 0"), and Steel's 64 rigging list rigs the boomless
    driver above (vol. II, OCR l. 24844-24847). No source
    names the *Indefatigable*'s own driver (Ind §5). For 1784 nothing was found either way
    between Falconer's (a) of 1780 and Steel's (b) of 1794.
  - After her dates: *Agamemnon*'s driver (1795) and *Lancaster*'s boom (1797) bear only on a
    64 sailing later, as D48(a) may sail her in the razee's scenario (1795-1797 among D25's
    dates; Indf §11). They are recorded, not counted for her.
- **The 74 of 1798: (b), good confidence.**
  - For: the same table, *Orion*'s yard and boom together in 1794, the Nile's logs, and Bel
    §5.4's own transitional rig, the lateen mizen yard with a boomed driver beside it.
  - Against: Lavery's table of 1773, 25 years earlier, and Steel's "0 0".
- **One model serves both**, cut from each ship's Steel figures by one helper (§17.2).
- **(a) is not proposed.** It is the 1773 establishment's driver and the older or merchant
  practice. What it would take is recorded in §17.4.

**Plainly:** this departs from what the owner's leave carried on b562bae: sail (a), "a
ringtail-like sail on a pole over the taffrail, hosted by the mizen course" (`Build-Ships.md`
§19.1 item 13; the decision sheet's "The 74's driver"). The owner asked for the driver, and for
these ships' dates the evidence leans to (b), for the 64 weakly. Lever gives (a) as the
merchant service's way, beside the driver "now cut Mainsail Fashion". It departs too from that
item's "The mizen course itself stays her after sail": as modelled, the course is unbent while
the driver is bent (§17.3). *The owner chose (b) for both on 2026-10-28, with these departures
before them (§17.9 item 1).*

### 17.2 The file contract (the 64's and the 74's modules)

**The sail** `mizzen.driver`:
- **Class and keys.** Class `lateen`, `cut_at_mast: true`. Roles `yard: mizzen.yard`,
  `mast: mizzen.mast` and `boom: mizzen.boom`. `in_place_of: mizzen.course`.
- **In the sail room.** `bent: false`, so it starts the voyage in the sail room as the storm
  canvas and the occasional sails do (`Sail.from_spec`). The room's list holds one spare of
  its kind and canvas, under "The occasional sails".
- **Corners.** `corners_m` are `[tack, throat, peak, clew]`, heights above the deck, cut after
  the boom's height is fixed (below):
  - the throat is the course's (the same nock under the same truss), and the tack is below
    it on the mast's raked line, both within 0.1 m;
  - the tack is at the boom's jaws, so the fore leech follows from the boom's height, and the
    clew is along the boom at Steel's foot cloths;
  - the peak is on the mizen yard's line at Steel's head cloths, abaft and above the yard's
    peak: the head runs straight along the yard and on along the driver yard, whose inner
    part lies along the mizen yard's after end (Lever l. 8282-8285: the outer halyards at the
    gaff's end, bent to the yard "about one-third from the inner Arm").
- **Area and centre.** `area_m2`, `x_m` and `centre_height_m` come from the four corners, as
  the course's do (§3.4: the centroid's height plus the deck height).
- **Reefs.** `reef_bands: 0`: Steel names no reef band in the driver, and `_sail_check`
  (`orders/verbs.py`) refuses "reef" on a sail with none.
- **Canvas.** `canvas_no` 5 (Steel: "No. 5 or 6", l. 13819), and `cloth_rating_kn` by
  `cloth(area, 5)`.
- **Groups.** "occasional sails" alone, as the frigate's ringtail.
  - Never "plain sail": `_rigged_for_plain_sail` (`world/ships.py`) sets every sail of that
    group, bent or not, so the polar would draw the course and the driver together.
  - Not "courses", which the gale reads, nor "all sail" (`Builder.whole_ship_groups`: the
    occasional sails are not set with the rest).
- **Aliases.** "driver", "spanker" and "driver boomsail" name `mizzen.driver`; "driver boom"
  and "spanker boom" name `mizzen.boom`. The course keeps "mizen" and its kin (Indf §4.7).

**Its figures.** Areas are by Steel's rule: mean cloths by mean depth, at 22½ in to a cloth
(vol. I, OCR l. 10891-10897). The four corners are measured on the research's geometry
(`mend17/driver_four.py`, after `driver_geom.py`), the mast upright, the boom level, the 74's
yard as I32 lies; the 64's jaws 2.4 m above her quarterdeck and the 74's at Steel's fore leech
(the boom's height, below).

| | The 64 | The 74 |
|---|---|---|
| Cloths, head / foot | 22½ / 29 (Ind §5) | 25½ / 32½ (Bel §5.6) |
| Fore / after leech, Steel's | 9½ / 20 yd (8.69 / 18.29 m) | 11 / 24 yd (10.06 / 21.95 m) |
| Fore / after leech, as cut | 6.98 / 18.71 m: the fore leech 1.71 m short, the after leech within Steel's "2 to 4 yards deeper" than the course's (17.60-19.43 m) | 10.06 / 22.73 m, within the same rule (21.03-22.86 m) |
| Area, Steel's rule | 198.5 m² | 265.2 m²; Bel's scaling for her 168 ft (×0.915, judgement) gives 242.7, her design's call as for all her sails |
| Area, the four corners | 197 m² (−1%) | 281 m² (+6%) |
| Centre | 8.55 m abaft the mast, 14.51 m above the water | 9.43 m abaft the mast |
| Against her mizen course | 3.8 m further aft, 1.9 m higher; after sail 104 → 198 m² | 3.9 m aft, 0.9 m higher; 138 → 265 m² |
| The foot | 16.57 m, the clew about 7 m beyond the taffrail (the mast 31 ft 4 in to 31 ft 11 in before it: Ind §3.3) | 18.57 m, about 7 m beyond the taffrail (I32: about 37½ ft abaft the mast) |
| The head | 17.15 m on the yard's line, the peak 6.09 m beyond the yard's peak; the driver yard's inner arm 4.4 m inside it, 0.42 of the driver yard | 19.08 m, 5.39 m beyond; the inner arm 6.95 m inside, 0.56 |
| Canvas | No. 5 | No. 5 |

**The boom** `mizzen.boom`:
- **Class and place.** Class `boom`, `on: mizzen.mast`.
- **Length.** By Steel's p. 40 rule, the main topsail yard's length: 65 ft 4 in × 12⅛ in
  (19.91 m) for the 64 (Indf §4.5, read for the razee's boom), and 70 ft 0 in × 13 in
  (21.34 m) for the 74 (Bel §5.3). The foot is then 0.83 and 0.87 of the boom, as the
  frigate's spanker foot is 0.9 of hers.
  - **Plainly:** Steel's p. 49 column gives both ships "0 0". The rule is the only figure.
    *Orion*'s and *Alexander*'s booms of 1794 are the evidence that 74s carried one beside a
    lateen mizen yard; *Lancaster*'s of 1797 is the only 64's, after her dates (§17.1).
- **Height, fixed first.** The boom lies level, its jaws on the mast, clear of the
  quarterdeck rail, the roundhouse and the taffrail; `height_m` is the jaws, and the sail's
  tack is cut to them.
  - Steel's fore leech would put the 64's jaws about 0.7 m above her quarterdeck at the mizen
    (measured: the throat 14.85 m above the water, less 8.69 m, against the quarterdeck's
    5.47 m), below a rail of 4 ft 6 in (the razee's quarterdeck rail, Indf §3.2). The 64's own
    rails, roundhouse and taffrail are still "to measure" there.
  - Until they are measured, her jaws stand 2.4 m above her quarterdeck, as the frigate's
    boom stands above her deck (`frigate-36.yaml`, `mizzen.boom`) (judgement). Her fore leech
    is then 6.98 m against Steel's 8.69; that shortfall is the cost (§17.9 risk 4).
  - The four corners hold the 10% check from the jaws at the rail (212 m², +7%) to about
    3.6 m above her quarterdeck (179 m², −10%) (measured, `driver_four.py`). If the profile
    wants them higher, B1 reports it to the lead rather than force the cut.
  - The 74's fore leech puts her jaws about 2.7 m above her quarterdeck (I32: the throat about
    42 ft above it), at or above the frigate's height; her poop is B7's to measure.
- **Horse.** `horse_m` as the frigate's (`HORSE_NOTE`). Steel's guy pendants lead to "the
  horse within the taffarel" (l. 23118-23121), and the sheet's geometry reads it
  (`evolutions/trim.py`, `sheet_geometry`).
- **Rating.** `rating_kn` is `design_kn([(area, centre, "gaff")], DESIGN_WIND_KN["gaff"])`,
  as the frigate's spanker boom.
  - The rating pass loads nothing on a boom whose only sail starts unbent
    (`Builder.rate_spars`: "keep the rating from the sails the script named for it").
  - The physics loads no boom: `_load_path` follows `_principal_spar`, the yard first.
- **Its own lines.** Steel's topping lifts and guy pendants (l. 23103-23121) are named in its
  note, not filed as lines, as the frigate files none on her spanker boom (E17: such lines are
  read by nothing but the reeving and repair tables).

**The driver yard is not filed as a spar.**
- Its figures are Steel's p. 40 rule: 34 ft 6 in × 7 in (10.52 m) for the 64 and 40 ft 6 in ×
  8¼ in (12.34 m) for the 74 (Ind §3.1; Bel §5.3).
- **Why not filed.** It went aloft with the sail and came down with it ("hoisted by haliards",
  l. 20863). A spar in the file stands for the whole voyage, catches wind and is drawn
  whether the driver is bent or in the sail room.
- **What it bounds.** The generator asserts the peak no more than two-thirds of the driver
  yard beyond the mizen yard's peak, since Lever's outer halyards are bent at a third of it.
  Its inner part lies along the mizen yard's after end (4.4 m on the 64, 7.0 m on the 74), so
  the viewer draws the head beyond the yard's peak as the driver yard and the rest as the
  mizen yard (§17.6).

**The mizen yard** keeps the course's contract (§3.4) and its rating, which the rating pass takes
from the course, the bent sail.
- **The driver's pull on it.** The driver pulls about 1.9 times as hard as the course in the
  same wind (198.5 against 104 m²; 265 against 138). A yard rated for the course at a design
  wind W therefore carries the driver to about 0.72 W: about 32 kn for 45 (measured, the pull
  as the area by the wind's square; judgement that the centre's 0.9-1.9 m changes it little).
- **No rating moves.** Steel's "light fair winds" sit well inside that limit.

**Its lines** are from Steel 1794 vol. I, "THE DRIVER or SPANKER SAIL" (OCR l. 24523-24545).
- **Sizes.** From Steel's vol. II lists:
  - the 74's halyards as Bel §5.4 read them on the page image;
  - the rest from the OCR, which B1 and B7 read again on the page images.
- **Ratings.** Each line is rated by `rope_kn` of Steel's size, as the ringtail's are rated
  by theirs.
- **The lines:**
  - **one `halyard`** of the sail, for Steel's "four or five pair of haliards" and the throat
    halyards (Lever's outer, middle, inner and throat halyards). The engine reads one
    `halyard_of(sail)`. The 64's is 3 in, the 74's 3½ in;
  - **one `tack`** of the sail, "set tight with a luff-tackle" to the throat of the boom:
    3 in;
  - **one unsided `sheet`**, `parts: 2`, rove through the boom's end to the clew, with its
    luff tackle to the taffrail. Steel's one line does the outhauler's work too. The 64's is
    3 in (judgement: her size is not legible in the OCR), the 74's 3½ in, each
    `rope_kn(size, 2)` as the frigate's spanker sheet;
  - **one `downhaul`** of the sail, "through a block made fast to the middle of the
    driver-yard": 2 in.
- **What follows from them.** With one unsided sheet the driver never joins `shifted_sails`.
  With no brace it loads none. Its working sheet carries the boomed share of its pull
  (`_sheet_load_kn`).

**The storm mizzen** stays `in_place_of: mizzen.course` (Indf §4.7). The course keeps every key of
§3.4.

**The generator asserts**, in `driver(...)` as it writes them (§9.3's rule):
- the throat at the course's throat, and the tack on the mast's raked line at the boom's jaws,
  within 0.1 m;
- the foot on the boom's line, with the clew within the boom's length;
- the peak on the mizen yard's line within 0.1 m, abaft and above the yard's peak by no more
  than two-thirds of the driver yard;
- the four corners' area within 10% of Steel's rule. Measured (`driver_four.py`): 197 m² on
  the 64 (−1%) and 281 m² on the 74 (+6%). At Steel's own fore leech the 64's cut overshoots,
  222 m² (+12%), its boom below her rail;
- the boom clear of the rail and the roundhouse as her profile gives them, and its end above
  the taffrail.

**The modules.**
- `tools/ships/mizen_yard.py` (B1's, pure, importing nothing from `gen_ships`) gains
  `driver(...)`. It writes the sail, the boom and the lines from the ship's Steel figures, the
  boom's height, the course's corners and the mast's line, each with Steel's size or figure
  and no rating.
- The ship's module applies the ratings through `g` (`import gen_ships as g`, Indf §1.2): the
  boom's `g.design_kn`, the cloth's `g.cloth(area, 5)`, each line's `g.rope_kn`, and the
  horse's note `g.HORSE_NOTE`.
- `tools/ships/indefatigable.py` gains a third stage-B flip, `DRIVER = False`, beside
  `MIZEN_COURSE` and `BOWSPRIT_YARDS`, so that the driver is a change of its own, measured old
  beside new by itself (taken at her stage B: `Build-Ships.md` §2.6). Each flip
  regenerates `sixty-four.yaml` alone.
  - The module refuses `DRIVER = True` unless `MIZEN_COURSE == "gated"`: a lateen's yard must
    be a `lateen_yard` (`ship/schema.py`), which the stand-in's gaff-class yard is not.
  - The course is filed before the driver, so that `sail_of(mizzen.yard)` (`ship/graph.py`,
    the first sail filed on the yard) stays the course.
- The 74's module calls the same function with her figures, under the same two rules.

### 17.3 The handling: the period, and the engine's paths

**The period:**
- **Two ways of bending it.** Steel gives both, each with its foot on the boom: the tack to
  "the eye-bolt in the throat of the boom", the sheet through "the outer end of the boom"
  (l. 24523-24538). They differ in how the head is bent and what becomes of the mizen:
  - bent "as a temporary matter" by four or five pair of halyards to the yard or gaff, beside
    the mizen, which is brailed up while the driver is set (the mizen left bent: Lever's plate
    key, "The Driver or Spanker with the Mizen brailed up", l. 6276-6277; *Majestic*'s two
    sails lost at the Nile; judgement from these);
  - or bent to the mast, yard or gaff "instead of the mizen", "exactly the same".
- **For these ships** the evidence is of the first way: Lever's plate, *Majestic*, and Bel
  §5.4's transitional rig, the lateen mizen yard with a boomed driver beside it. The second
  is Steel's alternative, and *Venus*, below, is a frigate with a gaff mizen.
- **Shifted at sea.** *Venus*, a frigate, in fresh gales in 1794 "Split the spanker, unbent
  it, and bent the mizen" (Jackson vol. 1, OCR l. 11064-11076).
- **Setting it.** Lever: "The Spanker is set like a lower Studding Sail, by hauling out the
  Sheet Rope to the Boom End hoisting on the outer Halliards, then the inner and Throat ones,
  and hauling the Tack forwards" (OCR l. 9904-9906).
- **Taking it in.** It comes in when the wind is right aft, because "it will not stand well,
  or if it did, being so far aft, it would cause the Ship to steer wild" (l. 9930-9938).
- **When it was set.** Steel's article says light fair winds. The logs set it in moderate and
  fresh breezes: *Vanguard* before she hauled to the wind, *Audacious* before she tacked in a
  chase, *Agamemnon* in a chase on or near a wind (the points of sailing are judgement).

**The engine takes Steel's second way, through `in_place_of`, by choice (below).** The times
and steps are the course's and the storm mizzen's, all judgement (§3.6).
**Not modelled:** Lever's hoist (the outer halyards, then the inner and the throat) and Steel's
downhauler on the driver yard. `set_lateen` has no hoist and `take_in_lateen` brails, as for
the course; the driver's halyard is read only when parted (the set refused, the sail dropped
into the gear), and its downhaul by no step.

| Order | What runs | Note |
|---|---|---|
| "shift the mizen for the driver" | `shift_sail` (`ShiftScript`). A drawing course is brailed up (90 s), unbent (180), sent down while the driver is swayed up (150), the driver bent (240) and set (120): 780 s by the hands' factor. A course brailed or furled is shifted where it hangs, and the driver left furled | the storm mizzen's way ("shift the spanker for the storm mizzen") |
| "shift the driver for the mizen" | the same, back | *Venus*'s shift |
| "bend the driver" with the course bent | refused by `_SailWork._rival`: "The mizen is bent in the driver's place; unbend it first, or shift the mizen for the driver." | existing words |
| "set the driver" while it is in the sail room | refused by `_sail_check` (`orders/verbs.py`): "the driver is unbent; there is no sail on the yard. Bend one first", untrue while the course is on the yard; "bend the driver" then gives the shift's words above | accepted as they stand: the frigate gives the same for her storm mizzen today, and a words-only fix would change hers (§17.10 item 4) |
| "set plain sail", "make all sail" with the driver bent | every sail of the group but the after sail: the course is reported unbent ("Not done: the mizen is unbent; there is no sail on the yard ..."), and the driver, in "occasional sails" alone, is not set | accepted: the frigate does the same with her storm mizzen bent. The driver is set by name |
| set, take in (brail up), furl, trim | `set_lateen`, `take_in_lateen`, `furl_lateen` (aloft on the yard) and `trim_lateen_sheet`, by class (B3.1, §3.6) | the sheet within the gaff's 18-85° by `wanted_sheet(sail)` |
| reef | refused: no reef band | Steel names none |
| in stays, wearing, hove to, the gale, the cast | the driver's paths by `drives_aft` (§3.5): hauled aft at helm's a-lee, brailed at "up helm" and hauled out by the wind, brailed up hove to, taken in at the gale's third reef, set after the cast | as the course; the log names it "the driver" |
| "shift the driver for the storm mizzen" | allowed by §17.4's one-place rule; the storm mizzen is never bent beside the driver | without the rule both could be bent |

**Plainly:** the brailed way, both sails bent with the mizen brailed while the driver is set, is
not modelled, though it is the way the evidence gives for these ships. The course is unbent while
the driver is bent, against `Build-Ships.md` §19.1 item 13's "The mizen course itself stays her
after sail".
- **Why.** The engine's one refusal (a sail is bent only while no sail in its place is bent)
  keeps one after sail of the place bent on every path that sets sail without asking. Those
  paths are the polar's "plain sail"; `_set_fore_and_aft` after the cast, which sets only a
  furled, loosed or brailed sail and never an unbent one; the gale; and the captains. Both
  sails bent would need a new exclusion on each of those paths, each a place to miss.
- **What is lost.** The shift's thirteen minutes against brailing the course and setting the
  driver, and the brailed course's windage while the driver draws.
- **Open** for the owner, should they want it later (§17.9 item 2); they chose (b) with the
  shift explained.

**Not modelled:** Lever's rule to take the driver in before the wind. The engine does not
make her steer wild under it: at 150° off it adds only 11 kN m of yaw on the frigate (§17.5).
The player's officers are not told the rule. The captains never bend an occasional sail.

### 17.4 The engine change, exactly

**`freesail/physics/` and `data/sail_classes.yaml`: nothing changes**, not even a lookup. Every
physics path the driver takes, read:

| Path | Where (read) | What it reads for the driver | Change |
|---|---|---|---|
| its curve and reef factor | `_read_rig` (`physics/sails.py`) | `SAIL_CLASSES[sail.curve_class]`, the gaff's (B3.1's lookup, §3.1) | none here |
| its side and angle | `_read_rig` → `yard_trim.refresh_reading` | a fore-and-aft sail (`Sail.is_fore_and_aft` holds `lateen`), by its sheet | none |
| its chord | `_chord_angle`, `_chord` | `sail.sheet_angle`: not of the square family, not in a gaff's plane | none |
| its lateral offset | `_lateral_offset` | the length of `ship.spar_of_role(sail, "boom")`, as for every fore-and-aft sail with a boom | none |
| its sheet's load | `_sheet_load_kn` → `trim.sheet_geometry` | the boomed geometry from the boom's length, horse and height, by role | none (B3.1 reads the floor through `curve_class`) |
| its loads | `_load_path`, `_apply_loads` | `spar_chain` from `_principal_spar`, the yard first: the mizen yard and the mast | none |
| its windage furled | `_sail_windage_area` | the class's furled windage (B3.1's `curve_class` lookup); unbent, none | none here |
| a ringtail's host | `_gaff_host` | not reached: the driver is no studding sail. Were a ringtail ever run out on its boom, the driver would already be found as its host (a fore-and-aft sail naming the boom) | none |
| a sideless studding sail | `_in_gaff_plane`, `_trim_yard`, `studding_level`, `studding_stall`; `set_studding.yaml`'s host precondition | not reached | none |

**Against the lead's lens:**
1. *The physics' ranges byte-identical.* The whole of `freesail/physics/` and
   `data/sail_classes.yaml` is untouched by the driver's commits: a diff of them shows nothing.
   That covers more than `_plate_force`, `compute_sail_forces`'s sums, `_lateral_offset` and
   the load fractions.
2. *The sail's curve an existing class's.* The gaff's, through `Sail.curve_class` for a sail
   cut at the mast (stage 0E).
3. *`_gaff_host`'s new host.* None is needed. Sail (a) would have needed one (below).
4. *The frigate's polar re-measured equal.* See §17.5 and §17.7.

**The changes**, each keyed on something no file of the eight has:
1. **Schema** (`ship/schema.py`, the stage-0 agent's).
   - `SAIL_OPTIONAL_ROLES["lateen"]` gains `"boom": frozenset({"boom"})`.
   - `validate` refuses a boom on a lateen that is not cut at the mast: "sail 'X' is a whole
     lateen and names a boom; only a lateen cut at the mast (a driver) is spread on a boom."
     The tartane's whole lateen has none.
   - Inert: no file of the eight has a lateen (measured: the 0E probe).
   - No runtime field, so no `__getstate__`.
2. **One place, one sail** (`evolutions/scripts.py`, B3).
   - `_in_each_others_place(a, b)` is also true when both name one place:
     `a.in_place_of is not None and a.in_place_of == b.in_place_of`.
   - It is read by `_SailWork._rival` (bending and shifting) and by `ShiftScript.check` (the
     order's "for"). So "bend the storm mizzen" with the driver bent is refused, and "shift
     the driver for the storm mizzen" is allowed.
   - `orders/storm.py`'s `_in_its_place` calls the same rule, in place of its own copy.
   - It is a membership: which bent sail holds a place.
   - Inert on the eight (measured): their thirteen `in_place_of` keys name each place once per
     file.

**Nothing else.** Each of these was read and needs no change:
- **The driver's paths.** `drives_aft` (B3.1) takes the driver by `cut_at_mast`, and with it
  `boom_sails`, `after_gaff_sails`, `_after_sail` and `after_gaff_sails_all`.
- **Unbent sails.** `after_gaff_sails_all` lists the driver unbent too, as it lists the brig's
  unbent storm trysail today, and `_set_fore_and_aft` sets neither.
- **Ratings.** `Builder.rate_spars` leaves an unbent sail out, so the course's ratings stand.
- **The yard's sail.** `sail_of(mizzen.yard)` returns the first sail naming the yard, the
  course, even while the driver is bent.
  - It is read for words (`_sail_hint`) and for the sail in hand of a spar evolution on the
    mizen yard (`sails_in_hand`).
  - The lugger's taille-vent on her main lug's yard, and the schooners' storm trysails on the
    main gaff, live with the same today.
- **The unbent refusal.** `_sail_check`'s "is unbent; there is no sail on the yard" answers
  "take in the mizen" while the driver is bent. It is true of the course, and the frigate
  gives the same words for her spanker with the storm mizzen bent. Left (§17.10).
- **The API.** The served graph's roles and stage 0E's `cut_at_mast` carry the driver; nothing
  new is served.

**What sail (a) would have needed**, kept for a later ship of the 1770s or a merchantman:
- a studding-class sail with no side, on a pole over the taffrail;
- the schema to let a sideless pole stand where there is no boom or gaff (`_on_fore_and_aft`,
  `FORE_AND_AFT_SPAR_CLASSES`);
- `_gaff_host` to find a sail cut at the mast as the host of a pole on its mast, a membership;
- `set_studding.yaml`'s host precondition, which reads the sails of the pole's parent;
- the viewer's ringtail branch, which finds its host by class `gaff` or `sprit` alone.

### 17.5 What the physics makes of it (observed)

**The method** is §3.2's (`driver_polar.py`, `driver_polar2.py`; row 4 `driver_polar4.py`):
- the frigate in memory under plain sail, with the polar's balanced speed in 15 kn
  (`world/ships.py`, `_balanced_speed_ms`);
- and the sails' yaw moment there, in kN m, where + turns her head toward a wind on her
  starboard bow (weather helm);
- the lateen read with the gaff's curve and trim by patching the class tables, as §3.2 did,
  since B3.1's `curve_class` lookups are not built yet; `is_yard` narrowed.

Speed (kn) / yaw (kN m):

| Row | 50° | 60° | 90° | 120° | 150° |
|---|---|---|---|---|---|
| 1. The spanker as filed | 2.21 / −45 | 4.29 / −15 | 8.19 / 102 | 7.86 / 89 | 6.53 / −31 |
| 2. The course cut at the mast at the spanker's area and place, on a 16-m lateen yard beside her gaff (§3.2's third row) | 2.18 / −43 | 4.28 / −13 | 8.18 / 102 | 7.86 / 86 | 6.54 / −34 |
| 3. Row 2 on the spanker's boom: the driver's model | 2.18 / −41 | 4.28 / −10 | 8.18 / 107 | 7.86 / 92 | 6.54 / −30 |
| 3′. Row 3 with the gaff taken out and the lateen yard at its length and height | **2.21 / −45** | **4.29 / −15** | **8.19 / 102** | **7.86 / 89** | **6.53 / −31** |
| 4. Row 2 cut to the 64's course's proportions of her driver (§17.2's four corners): 87 m², 3.10 m abaft the mast against 5.60, 1.92 m lower | 1.92 / −112 | 4.11 / −92 | 8.04 / 32 | 7.64 / 62 | 6.45 / −41 |

- **Row 3′ equals row 1 at every angle, in speed and in yaw.** To the physics, the driver's
  model (a lateen cut at the mast, read with the gaff's curve, spread on a boom) is the
  frigate's spanker. Row 3 differs from row 1 only by the windage of the extra lateen yard
  that the in-memory rig adds beside her gaff (§3.2's 0.03 kn); row 2 also by its lateral
  offset, 0.8√A for a sail that names no boom.
- **The boom moves the yaw, not the speed** (row 3 against row 2). The lateral offset becomes
  half the boom's length by the sheet's sine, in place of 0.8√A's.
- **What the shift does** (row 3 against row 4, the frigate's spanker standing for a driver):
  - speed: 0.26 kn more at 50°, 0.17 at 60°, 0.14 at 90°, 0.22 at 120° and 0.09 at 150°;
  - yaw: 71-82 kN m more toward the wind from 50° to 90°, 30 at 120° and 11 at 150°;
  - so more sail, further aft, makes her faster and gives her more weather helm by the wind.
- **On the 64 and the 74** the after sail nearly doubles, and its centre goes 3.8-3.9 m aft and
  0.9-1.9 m up (§17.2). B1 and B7 measure their own polars and balance at the flip, old beside
  new. Nothing is pinned from the frigate.
- **The lateral offset reads the boom's whole length.** That is 19.91 m against a foot of
  16.57 m on the 64, a fifth long, as the frigate's offset reads her whole boom against a foot
  of 0.9 of it. Kept: it is the frigate's convention, and needs no physics change.

### 17.6 The drawing (`client/projection.js`; B5)

Every change is reached only by a lateen cut at the mast that names a boom, so no existing ship
draws differently.
- **The boom's swing.** `sheetAngleOf(sparId)` returns the sheet angle of the first gaff or
  sprit sail on the spar. It also takes a lateen cut at the mast that is not unbent (a
  membership). With the driver in the sail room the boom lies amidships, as a boom with no
  sail does now.
- **The sail**, in §6.1's branch for a sail cut at the mast:
  - with `roles.boom`, the tack is at the boom's jaws and the clew along the boom (`Bm.a`,
    `Bm.b`, as the gaff branch's `Bm`);
  - the head runs straight from the throat along the yard's line to the sail's peak (§17.2's
    four corners); beyond the yard's peak it is drawn as Steel's driver yard, a spar line
    drawn with the sail, whose inner part lies along the mizen yard and is drawn as it;
  - no reef; in the gear it is brailed to the mast as the course is; furled, it is a bundle
    along the yard's after part.
- **The yard.** §6.1 swings the mizen yard by its sail's sheet and lays it at "the corners' run
  and rise".
  - `sailOnYard` already returns a yard's bent sail (`bent[0] || on[0]`).
  - The yard's own line is taken from the course's corners whichever sail is bent: the sail
    cut at the mast with no boom, served whether bent or not. So the yard never moves when
    the driver is shifted.
- **The sheet** runs from the boom's end to the taffrail on the centreline, as §6.1's does.
- **The pictures.**
  - `tests/test_pictures.py`'s thresholds and every existing `tests/test_view_geometry.py` case
    stay as they are.
  - New cases on the fixture: the driver on its corners within 0.1 m; the foot along the boom;
    the yard's line equal with the course bent and with the driver bent; the boom swung to the
    sheet's side; the frame (`fullRigFrame`) holding the boom's swing beyond the taffrail.
  - Screenshots of each state for the owner.

### 17.7 Tests, truths, pins

- **The guard set** (§10.1) is unchanged. The 0E probe gains "a lateen naming a boom" among
  the things no file of the eight carries.
- **`tests/test_driver.py`** (B3, on the fixture `frigate_with_driver()` alone; the 64's file
  carries no driver until B1's flip):
  - "shift the mizen for the driver" and back each run to their end. The room holds the
    course's canvas while the driver is bent;
  - "bend the driver" is refused while the course is bent. "bend the storm mizzen" is refused
    while the driver is bent, with words naming the driver. "shift the driver for the storm
    mizzen" runs;
  - bent, the driver is her driver: hauled aft at helm's a-lee, brailed up hove to, brailed at
    "up helm" and hauled out by the wind, taken in at the gale's third reef, and set after the
    cast. Unbent, none of those paths touches it, and the cast sets the course;
  - its sheet stays within the gaff's 18-85° by every route (set, trim, `trim sails`,
    `draw_sheets`, the polar), and its sheet geometry is the boomed one;
  - "reef the driver" is refused;
  - the words of §17.3: "set the driver" in the sail room, and "set plain sail" and "make all
    sail" with the driver bent, each as the table has them;
  - **the frigate's polar row.** `frigate-36.yaml`'s balanced speed at 50, 60, 90, 120 and 150°
    in 15 kn equals §3.2's first row (2.21, 4.29, 8.19, 7.86, 6.53) on the final tree;
  - **row 3′ as a test.** The frigate's spanker re-filed in memory as a lateen cut at the mast,
    on a lateen yard in the gaff's place and on her boom, with no patch (B3.1's lookups read
    `curve_class`). Speed and yaw equal row 1 at the five angles, within 0.01 kn and 1 kN m.
- **The 64's own cases** (B1's, in `tests/test_indefatigable.py`, at the `DRIVER` flip): the
  shift and back, the two refusals and the paths by `drives_aft` above, run on
  `sixty-four.yaml`; the generator's assertions of §17.2 on her figures.
- **The schema's refusal** (the stage-0 commit's test): a whole lateen naming a boom is refused
  in words, and a lateen cut at the mast naming one loads with the role.
- **The 0E pickling guard** holds as it is: the driver adds no field.
- **Truth 7-230**, allotted by the lead (2026-10-29): row 3′'s equality and the shift's thirteen
  minutes, in `tests/test_driver.py`. As first proposed, B1 measures it at stage
  B with `DRIVER = True`. *The 64 shifts her mizen for the driver, and the driver draws as her
  after sail.* What it pins:
  - the shift's phases, and its ticks in a band at her company;
  - with the driver bent and set, her polar above the course's from 90° to 150° in 10 kn,
    Steel's "light fair winds". Measured first, and pinned only if it holds; else reported;
  - the driver hauled aft at helm's a-lee and brailed up hove to.

  Its sources: Steel l. 13819-13821 and 24536-24538, and *Venus*'s shift.
- **The 74's polar point S7** (*Vanguard*, 1798, "under courses, topsails and driver": Bel §6.3)
  is measured with the driver bent in the course's place, and her truth says so. It is one of
  B7's numbers, not a new one.
- **Pins.**
  - None move on the eight: every change is keyed on a role, a key or a shared place no file
    of the eight has.
  - The 64's own figures move at the `DRIVER` flip by the boom and the spare alone, since the
    driver starts unbent: the boom's windage; the boom among the spars a shot aloft can carry
    away (`combat/hits.py`, `_rigging_hit`, a boom weighted 1.5 by `_spar_weight`); and the
    sail room's count with the driver's spare (`spare_sails`, the muster line). B1 re-measures
    each, shown old beside new in her review and her tuning notes.
  - The same holds for the 74 in her window.

### 17.8 Who builds what, and when

| Who | What | When |
|---|---|---|
| The stage-0 agent | One commit, checked as `Build-Ships.md` §3.4: the schema's `boom` role for a lateen cut at the mast, and its refusal; `frigate_with_driver()` in `tests/rig_fixtures.py`; the probe's line; the refusal's test. The fixture is the 0E fixture (`frigate_with_mizen_yard()`) with the frigate's `mizzen.boom` put back, lengthened to the 64's 19.91 m and set where it hangs the 64's driver from the fixture's truss as §17.2 cuts it (the fore leech 6.98 m below `MIZEN_TRUSS_M`, so the jaws about 4.5 m above her deck: judgement), and the 64's driver on its four corners filed after the course, `in_place_of` it, unbent, with a bent variant for the drawing. The storm mizzen stays `in_place_of` the course, so the one-place rule has its case; the ringtail and its boom stay out, as the 64 carries none (Indf §4.7), so `_gaff_host` is not reached | after the lead's approval (2026-10-29; the owner chose the sail, §17.9 item 1), and after stage 0E (2ead5f0). §17.4's list for (a) is where a later design of (a) would start |
| B3, step B3.5 (the driver) | `_in_each_others_place` widened, and `_in_its_place` calling it; `tests/test_driver.py`. Nothing in `physics/` | after B3.1 (it needs `drives_aft`, the `curve_class` lookups and the six lateen evolutions) and after the stage-0 commit, at the engine builder's next step boundary |
| B5 | §17.6, with or after §6.1's mizen yard, from the fixture | after B3.5 lands |
| B1 | `driver(...)` in `tools/ships/mizen_yard.py`; `DRIVER` in `indefatigable.py`, flipped after B3.5 and B5's drawing; the sail room's spare, the aliases and the group; the 64's cases in `tests/test_indefatigable.py`; truth 7-230 if allotted | at her stage B, as its third flip, in her own window (`Build-Ships.md` §2.6): her stage B waits for B3.5 and B5's drawing, so that the owner's first test is of the whole ship. Her stage A does not wait on it. If they are not in by the package's merge, she ships without it, as `Build-Ships.md` §2.4 has it for the stand-ins |
| B7 | the 74's driver by the same function, with her figures and her scaling | in her window, after B3.5 and B5's drawing; if either is missing, her file goes without it, as the 64's |

**What stage 0 and stage 0E already hold for it:**
- `SailSpec.cut_at_mast` and `Sail.cut_at_mast`, with their refusals and their pickling;
- `Sail.curve_class`, which gives the gaff's for a sail cut at the mast;
- stage 0's `curve_class` lookups: the polar's trim in `world/ships.py`, `api/queries.py`,
  `api/readings.py`, and the rating pass in `gen_ships.py`, so the driver rates at the gaff's
  1.29;
- `wanted_sheet(sail)` in the runner;
- the served `cut_at_mast`;
- `frigate_with_mizen_yard()` and the 0E guards.

From before the package: `in_place_of`, the sail room, `shift_sail`, `bend_sail` and
`unbend_sail`.

**Nothing here waits for B1's first steps.** Nothing of B1's stage A, and nothing of stage 0E,
waits for it.

### 17.9 Risks, ranked, and what stays open

**Risks:**
1. **The 64's verdict is of low confidence.** For her dates Steel's own tables split: Table IV
   cuts a boomsail, while the 64 column has no boom and the 64 list rigs a boomless driver. No
   source names her own driver, and the 64s' evidence (*Agamemnon*, *Lancaster*) is later.
   *Mitigation:* the owner chose it knowing the evidence is weak (item 1 below); its own flip; left off, her stage B is as §3
   has it.
2. **The brailed way is not modelled** (Steel's first way; Lever's plate; *Majestic*'s two
   sails), though it is the evidence's way for these ships. A player who wants the driver pays
   a thirteen-minute shift, and the course is unbent meanwhile. *Mitigation:* the one refusal
   guards every path; the cost is recorded in the tuning notes; the way is left open.
3. **The light canvas.**
   - The driver is No. 5 against the course's No. 2, so it reaches its cloth's rating in less
     wind, and the gale takes it in only at the third reef.
   - Once it is taken in, she has no after sail until it is shifted back.
   - *Mitigation:* B1 measures the wind at which it blows out, set and drawing, and records it
     beside Steel's "light fair winds" and the logs' fresh breezes.
4. **The boom over the rail, the taffrail and the roundhouse**, all unmeasured on the 64
   (Indf §3.2). *Mitigation:* the boom's height fixed first, from her profile, 2.4 m above her
   quarterdeck until measured (judgement). The cost is her fore leech, 6.98 m against Steel's
   8.69 at that height; the area check holds the four corners to jaws about 3.6 m up, and
   above that B1 reports to the lead.
5. **The offset from the boom's whole length** overstates the driver's yaw by about a fifth on
   the 64. *Mitigation:* the frigate's convention; measured at the flip; no physics change.
6. **`sail_of` names the course while the driver is bent**, in words and in a spar evolution's
   sail in hand. *Mitigation:* the lugger's and the schooners' precedent. B3.5 runs "send down
   the mizen yard" with the driver bent and records the words.
7. **The yard drawn from the course's corners** would move if a module cut the two sails'
   throats apart. *Mitigation:* the generator's throat assertion, and the view test's equal
   yard line.

**Open, for the owner or the lead:**
1. **Which sail each ship carries** (answered): (b), proposed for both (for the 64 on weak evidence),
   departing from the (a) carried on b562bae (§17.1), and, as modelled, from that item's "The
   mizen course itself stays her after sail" (§17.3). *The owner's answer (2026-10-28): (b) for
   both, chosen with the two sails drawn side by side and the shift explained, as the simpler.*
   *Approved by the lead (2026-10-29, the notes in `docs/dev/M7-WorkPackages.md`).*
2. **`in_place_of` against the brailed way** (§17.3). If the owner wants both sails bent, it is a
   new exclusion on each path that sets sail, and a design of its own.
3. **The research's uncertainties.**
   - The boom's length, by Steel's rule against Steel's "0 0" column.
   - The Table IV figures, read earlier from the page images and not re-read here; the 64's
     ¼-yd departure from Steel's rule may be a misreading.
   - *Agamemnon*'s driver, inferred from its use, not described; *Majestic*'s two sails bent
     and the logs' points of sailing, inferred.
   - The 64's rails, roundhouse and taffrail, and so her boom's height and fore leech.
   - Whether *Culloden*'s "spanker" was her mizen course under another name.
   - What Steel's 20-gun plate shows.
4. **The lines' sizes**, from the OCR of Steel's vol. II lists but for the 74's halyards. B1 and
   B7 read the page images.
5. **Truth 7-230**: allotted to the driver by the lead (2026-10-29).
6. **Sail (a)**, kept possible as §17.4 says. The 1773 rig is no file's.
7. **The decision sheet's "The 74's driver"** (`Decisions-ShipsRound2-2026-10.md`) still
   describes (a) as carried. This addendum does not edit it.

### 17.10 Found on the way

1. `client/projection.js`'s `sheetAngleOf` and the ringtail branch's host lookup find a sail by
   class `gaff` or `sprit` alone. A sail cut at the mast is added where it is a boom's sail
   (§17.6).
2. `world/ships.py`'s `_rigged_for_plain_sail` sets every sail of "plain sail", bent or not. A
   file that put an occasional sail there would draw both sails of one place in its polar. No
   file does; every occasional sail is kept out of "plain sail".
3. `after_gaff_sails_all` lists unbent gaff sails (the brig's storm trysail). Harmless, since
   `_set_fore_and_aft` sets none.
4. `_sail_check`'s refusal for an unbent sail ("there is no sail on the yard") is untrue when
   another sail is bent in its place, as for the frigate's spanker with the storm mizzen bent. A
   words-only fix would change the frigate's words in that state, so it is left.
5. A ringtail on a driver boom would already find the driver as its host (`_gaff_host` reads the
   fore-and-aft sail naming the boom). The 64 carries none (Indf §4.7).
