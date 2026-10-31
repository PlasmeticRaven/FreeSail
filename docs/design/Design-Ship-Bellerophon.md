# Design: HMS *Bellerophon*, the Arrogant-class 74 of 1786 on the Bellona-class draughts (package 75, Phase 3)

The design for the fourth and last ship of package 75 (B7). It was judged from two drafts, one
written for fidelity and one for buildability, as the *Indefatigable*'s was, and every figure
kept was checked against the notes, the code at this head and the page images or OCR texts
named. Where the drafts disagreed, or one was wrong, this document says so and gives its reason
(the table below). It is for her builder (B7), for the stage-0 agent who lays her stage 0c, and
for the lead, who allots the engine files her bill by deck reaches (§12.3, §17.2). Nothing here
is built.

**Status (2026-10-29).** Written by the plan's Phase 3 method (`Build-Ships.md` §13 head: "Each
is designed before her build ... from her note and the answers ... names her stage 0, her files,
her truths' measures and her pins"). It settles every item of `Build-Ships.md` §13.2, or says
plainly why one stays open (§17).

**What binds, in order:**
1. The brief (`docs/dev/M7-WorkPackages.md`, "## Package 75", item 3: "a 74 ... her lower deck's
   32-pounders and their ports' sills against the heel ..., her people some 590, her quarter
   bill by deck, her marines; her sail plan and spars; her polar; the pace of a 74 crewed
   measured against the floors"; item 6, her truths) and the lead's notes at its end: the order
   and the merges (item 8 of the gate's rulings: the *Indefatigable*, the *Prince de
   Neufchatel*, the bilander, the 74; the lead merges after each ship, and a window closes with
   its merge); the approval of the hull's design (2026-10-29); SW-1 beside the pilot.
2. `docs/design/Build-Ships.md` (cited **Build**): §13.2 above all; §2.2-§2.6, read with the
   owner's direction of 2026-10-29 (below); §3.3; §4; §5.0-§5.3 and §5.7; §6; §7; §14-§16; §19.
3. `docs/design/Decisions-ShipsRound2-2026-10.md`: the 74's answers (2026-10-28) and the driver as
   the owner chose it (Steel's driver boomsail); the answers in full in her note's §13.1 (cited
   "answer N").
4. Her research note, `docs/design/Research-74-2026-10.md` (cited **Bel**), and the notes it cites.
5. `docs/design/Design-ShipsEngineExtensions.md` (cited **Ext**): §3 (the mizen course cut at the
   mast), §4 (the yards under the bowsprit), §9.3 (the helpers' contracts), §17 (the driver, "the
   74's by the same function").
6. `docs/design/Design-Ship-Indefatigable.md` (cited **Indf**): the model in shape and method.
7. The owner's private references (`D:/Projects/FreeSail/owner-notes/`): facts cited by book and
   page, never their text. Lavery's *The 74-Gun Ship Bellona* (1985) is cited "Lavery p. N" and
   marked *read (owner's book)*.
8. Pictures for the eye only, never a source of points: Thomas Luny's *H.M.S. Bellerophon lying
   at anchor off Berry Head, Torbay, 6 August 1815* (painted 1827; Commons, public domain): two
   tiers of stern lights in a decorated frame, a quarter gallery; Chalon's *Bellerophon* at
   Plymouth, 1815 (RMG BHC3227, in the research's cache); Pocock's sketch of 1794 (PAD8704).

**The owner's direction of 2026-10-29.** The build goes on without holding for the owner's own
test of the *Indefatigable*. The owner receives a testing report instead: the basics, with
pictures of the important views. So each ship's window follows the last ship's merge, in the
order the lead ruled, and her window ends with her own testing report (§13.1). **Plainly:**
`Build-Ships.md` §2.6 still reads "Held for the owner's first test", and its "Held until the
test" line names SW-2, B2, B4, B7 and B6. The session records the direction there before B2's
window opens (§17.2 item 6).

**Code** is cited as file:line at the package branch's head 8f30be9. The clone's working tree
also holds uncommitted work of B1's and of stage 0H and SW-2b.1 (`freesail/ship/form.py`,
`g.hull_form`); this design reads that only as the contracts `Build-Ships.md` §3.5 and §5.3 give,
never by its lines. By her window the tree will have moved through B1's stage B, SW-1, SW-2,
SW-4, SW-5, B2 and B4, so her builder re-reads every line before an edit. Paths are from the
repository root.

**Marks.** *read*: the page, image or code cited. *read (OCR)*: a text layer under
`docs/references/`. *read (page image)*. *read (owner's book)*. *measured*: off a held image by
the research, or arithmetic on its measured figures. *observed*: an engine run in this design's
scratch. *judgement*, *secondary*, *catalogue* as the notes use them; no memory is used.
"Measured here" means arithmetic by this design's scratch scripts, outside the repository
(`scratchpad/designs/bellerophon/figs.py`, `probe/figs.py` and `probe/mend_figs.py`), and
"observed here" the polar probe (`scratchpad/designs/bellerophon/final/probe_polar.py`) and the
frigate's drift off the Lizard (`probe/heave_probe.py`, `probe/heave_probe2.py`), each run with `py`
from the tree root. "Plainly:" marks a departure from a decision, a ruling or the brief, with its reason. No git
write was made, no test suite was run, and nothing in the repository was changed.

**One sentence.** One module writes one file on the final rig, since every engine piece she uses
is merged before her window opens; her water is the line where her drawn lowest port stands the
*Bellona*'s reported 5 ft 2 in clear, so the hull the viewer draws and the hull that floats are
one; her guns stand on their measured ports, each deck named; and her bill by deck is the gun's
`deck` word and one inert bill key, read by two small keyed changes in the quarters and the gun
orders.

---

## How the two drafts were judged

| Question | Taken from | Why, in short |
|---|---|---|
| The skeleton: narrow ownership, a small stage 0c, the fallback flips kept, the general tack rule apart | buildability | The lead's lens: B7 takes `crew/quarters.py`, which is hers (Build §4.1), and `orders/gunnery.py`, which no one owns and which this design names; no B3 or B8 file unless the lead allots it. The flips are the fallback Build §2.4 and Ext §17.8 foresee |
| Her water, the Channel line | both (one reading); buildability's definition | The drawn lowest sill (L7, 5.44 ft above WL1) at exactly 5 ft 2 in: WL1 + 0.273 ft. The fidelity draft's mean of L7 and L8 (0.278 ft) rounds every sill alike |
| The shut heel of the lowest port | buildability's 10.35° | The file's sill, 1.57 m to the centimetre, on 7.04 m. The fidelity draft's 10.38° was the unrounded sill |
| GM, the main mast's place | corrected | 4 ft 5⁷⁄₁₀ in is 1.364 m, so 1.36 (the fidelity draft gave 1.37); 74.79 ft from AP is −2.81 m (it gave −2.80) |
| The displacement band's citation | corrected | Bel §3.2.5 prints 2,530-2,600 t at WL1. The buildability draft cited its own conversion of the tons of 35 (2,515-2,584 t) to Bel. Both conversions are given (§2.1) |
| The topgallant masts | fidelity: Steel p. 42's long pole-head, put to the owner for both ships | The OCR (vol. I l. 2934-2942, 4701-4702) bears the reading: a pole-head is set up from the stop, a long one two-thirds of the length to it |
| The mizen topgallant mast | buildability (Steel's 24-6 × 0.973) | The rule for a mast Table 10 lacks; the room table re-measured on it here |
| The mizen course's tack | neither: 9 ft above the quarterdeck, where I32's throat (about 42 ft above it) less Steel's 11-yard fore leech puts it | The fidelity draft's 6 ft 6 in (Steel's general "within 6 or 7 feet"; B1's `MIZEN_TACK_ABOVE_DECK_FT = 6.5`) ends the course's level foot inside her judged poop, and leaves her driver failing both of Ext §17.2's checks (§4.5, §4.6). The buildability draft's "3 ft, as the 64's" was stale |
| The driver's boom | neither, corrected | Both drafts took Ext §17.2's jaws (2.7 m above the quarterdeck, measured on I32's 42-ft throat) beside a course whose throat stood 2½ ft lower. The throat is the course's, so Steel's fore leech puts the jaws at the course's tack. On I32's throat the boom must be raised about 5¼ ft to clear the judged poop by 6 ft; task 5 measures the poop before the cut (§4.6) |
| The fits | buildability's (the 1812 fit of 78 pieces), with fidelity's forecastle 9s of 8 ft 6 in | The owner chose the *Bellona*'s list of 78. The fidelity draft mounted 76, leaving out two 12-pdr carronades by judgement under "Plainly" alone |
| The fits' names | buildability | The "ardent class 1784" precedent |
| The guns' numbers | buildability's (on across decks), with fidelity's numbering by deck offered to the lead as an option, corrected | The option needs an explicit key, gun ids re-keyed by deck, and the quarters' parse sites taught (§5.2) |
| The company | fidelity's posts (16) and idlers (44) | The buildability draft dropped the chaplain because `IDLER_TRADES` has no place for one; posts are free strings (`PostSpec`, `schema.py:557`). The idlers follow the 64's form (servants among them) |
| The marines' division | fidelity's `marines` bill key, keyed on her bill alone | The brief names her marines; B1's `BEAT_MEASURED` shows no division forming on the 64 or the razee |
| `told_off` | neither | A key that makes one ship follow a general practice the frigate would not is inconsistent. The tack's rule is general, B7.c, on the lead's word |
| The bill by deck's reach | buildability | `crew/quarters.py` and `orders/gunnery.py` meet answer 9. "A deck run in" (`combat/guns.py`, B8's) is not needed for it |
| A King's frigate meeting her | fidelity's question to the owner; buildability's cruiser test kept either way | A doctrine choice is the owner's |
| The flag | buildability (the scenario's `people:`), with fidelity's `commodore` role | A fit holds only guns and stores |
| Her description's words | fidelity | "a two-decker" names the 64 as well |
| 7-195 | buildability's knife-edge rule; fidelity's sailing clause only without gusts and with margin | Answer 8 says "or in gusts at 24 kn" |
| 7-196 | buildability's; the crewed clause named `..._holds_the_crewed_floor` and marked `pace` by hand, as truth 7-138 is, in a world off the Lizard | Build §13.2; truth 88's own place is 30 miles from the station its 74s would keep (§14.4) |
| The testing report | fidelity's content on buildability's frame | The owner asked for the basics and the important views |
| The research's scratch 74 | buildability's finding, re-run here | It no longer loads under 86's magazine by kind; without its armament its polar is unchanged (observed here) |

---

## Decisions taken

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/bellerophon.py`, `build(out_dir)` writing `data/ships/seventy-four.yaml`; her people `data/people/seventy-four.yaml` | Stage 0's stub and name (Build §3.3; the lead's item 9). One file, one rig (Bel §13.5) |
| 2 | **No stage A and stage B.** She is built once, on the final rig. B3.1, B3.2, B3.5, their drawings and B1's `mizen_yard.py` and `spritsail_yards.py` are merged before her window opens. Three flips kept as the fallback | The order (Build §2.2: B7 after B4). Build §2.4 and Ext §17.8 foresee the fallback (§0) |
| 3 | Her module imports nothing from `tools/ships/indefatigable.py`; it takes `g`, `period`, `mizen_yard` and `spritsail_yards`, and copies B1's patterns | An import would tie her bytes to another ship's module, whose window is closed |
| 4 | **Her water is the Channel line**, WL1 + 0.273 ft (0.083 m), parallel to WL1, where her drawn lowest sill stands the *Bellona*'s reported 5 ft 2 in. Draught, displacement, lateral plane and profile all at that line; the report's draughts recorded | Answers 5 and 6 (§2.2). Put to the owner (§17.1 item 1) |
| 5 | Hull: LWL 51.2 m, beam 14.25 m, draught 6.46 m to K, displacement 2,600 t, GM 1.36 m, lateral plane 330 m², deck height 3.16 m | §2.1 |
| 6 | D18 does not bite: (a) and (c) are both her upper deck | As the 64 (Indf §2.2) |
| 7 | The profile with every shape key from her first commit, each line marked on §5.0's ladder; the triples' half-breadth outside the plank | Build §5.1, §5.6, §5.7; Indf §3.3's convention (§3) |
| 8 | Masts and yards: *Dragon*'s (Lavery p. 19, Table 10), her class's own; Steel 1794 p. 49's 74 column where Table 10 lacks a spar, a mast scaled 0.973 and a yard 1.00 | The ladder (S before R); Bel §13.4 |
| 9 | **Topgallant masts with Steel's long pole-head set up above their listed length**; the topgallants and royals cut to the spars so read | Steel 1794 vol. I pp. 41-42 (§4.2). Put to the owner for both ships (§17.1 item 2) |
| 10 | Sails: Steel's table IV, 74 column, unscaled; Lavery's Table 15 (1773) the check | Her yards are Steel's within 1% (Bel §13.4) |
| 11 | The mizen course on its lateen yard through `mizen_yard.py`; the yard 86 ft 6 in; the tack 9 ft above the quarterdeck, under I32's throat | Ext §2, §3.4, §17.2; Bel §13.5 (§4.5) |
| 12 | Steel's driver boomsail through `mizen_yard.driver()`, unscaled; its boom 70 ft 6 in; its jaws set by her measured poop and taffrail | Ext §17.2, §17.8 (§4.6) |
| 13 | Spritsail and sprit-topsail yards through `spritsail_yards.py`, out of "plain sail" | D8 (b); Ext §4.1 |
| 14 | Three fits: "arrogant class 1793" (74 pieces), **"arrogant class 1795"** (82, the default), "as the bellona 1812" (78) | Answer 3 as revised (Bel §13.5); names for the lead |
| 15 | Guns numbered on across decks from forward, the lower deck first; each gun's `deck` named; a place keeps its number in every fit. Numbering by deck offered to the lead as B7.d, for both two-deckers together | `(number, side)` unique in a fit; `pair_key` (`ship/parts.py:621`) (§5.2) |
| 16 | Patterns and crews by the sources: long 32 of 9 ft 6 in and 55 cwt (13), long 18 of 9 ft and 40 cwt (42 in 1812) (9), long 12s of 1812 (7), long 9s of 7 ft 6 in and 8 ft 6 in (6), carronades (4) | Answer 12; Adye; Lavery pp. 21-22 |
| 17 | Charges from SW-1's Table No. 29; exercise 9; filling 18 | Build §10; the Regulations p. 165 |
| 18 | Company 590: posts 16, marines 111, idlers 44, seamen 419 | Answers 10-11; the 1807 table (Bel §4.3) |
| 19 | **The bill by deck (answer 9), B7.b:** the bill's new `marines` key keeps her marines' division; divisions, robbing and orders by deck read the gun's `deck`; officers by deck in her people file | §6.4 |
| 20 | The tack at quarters (answer 17): reasoned here; built as B7.c only on the lead's word, since it moves every ship and truth 7-136 | §6.7 |
| 21 | The rear-admiral's flag: the scenario's `people:`, not her file | `FIT_KEYS` holds guns and stores only (§6.6). Put to the owner |
| 22 | Ground tackle: four bowers of 67 cwt, a stream of 16, a kedge of 8; seven 22-in cables of 100 fathoms. Boats: Lavery's six of about 1800 | Answer 13; Lavery pp. 15-16 |
| 23 | Description `seventy-four`, "a ship", rank 4; "a ship of the line" names her; three assertions moved, old beside new | Build §13.2 (§8) |
| 24 | A lone King's frigate keeps away from her by a rank-4 rule, if the owner takes it (B7.e); a cruiser keeping away is tested either way | Bel §7.2; Maitland p. 78 (§8.3) |
| 25 | Her stage 0c lays one key, `marines` on the quarter bill; and the numbering key only if the lead takes B7.d. Her module writes each into her file after the generator's own call | §12.1 |
| 26 | Her polar measured, tuned only within bands, recorded; no polar truth | Bel §13.2 (§9) |
| 27 | Truths 7-194, 7-195 and 7-196 as §14 measures them | Build §15 |
| 28 | Her window ends with the owner's testing report | The owner's direction of 2026-10-29 (§13.1) |

---

## 0. The gate, the order, and what waits

**No gate of her own.** The lead's gate stood on the engine extensions, approved with Ext §17's
addendum. Every engine piece she uses is built and merged before her window opens:

| Piece | Built by | Before her window? | If it slips |
|---|---|---|---|
| The lateen cut at the mast (B3.1) | B3 | yes: B1's stage B needs it | `MIZEN_COURSE = "stand-in"` (B1's stage-A course, Indf §4.4) |
| The yards under the bowsprit (B3.2) | B3 | yes: B1's stage B | `BOWSPRIT_YARDS = False` |
| The driver (B3.5) and its drawing (B5.5) | B3, B5 | yes: B1's stage B | `DRIVER = False` (Ext §17.8's B7 row) |
| `mizen_yard.py` (the course and `driver()`), `spritsail_yards.py` | B1 at stage B | yes: B1 merged whole | the same flips |
| The settee (B3.3) | B3 | yes: B4 waits on it | nothing of hers |
| Stage 0H, SW-2b.1 (`g.hull_form` and kin) | stage-0 agent, B8 | yes | her shape keys wait; her profile does not |
| SW-1, Table No. 29 | B8 | yes (Build §2.2) | her long 32's charge would be the share's 10 lb 11 oz; she waits rather than override |
| SW-2 with SW-2b.2, then SW-5 L2 and L3 (the lee port) | B8 | yes (Build §2.2: B7 after SW-5) | 7-195 waits; her file does not (§17.2 item 7) |
| SW-4 (a description's `fit` and `roles`) | B8 | yes | her description's `roles` wait |
| B5's drawings (B5.1-B5.3, B5.5, B5.6) | B5 | yes | her testing report's pictures wait |

**Plainly:** her module keeps the three flips (`MIZEN_COURSE`, `BOWSPRIT_YARDS`, `DRIVER`), each
"gated" or `True` by default, so that a late piece costs one constant and the change back is one
regeneration, old beside new, as the 64's stage B is. They are the fallback Build §2.4 and Ext
§17.8 foresee ("if either is missing, her file goes without it"), not a stage A of hers.

**Her window** opens after B4's merge (the lead's order, item 8) with the fresh merge of the
lead's head (Build §2.1), and closes with her merge. Under the owner's direction nothing in it
waits on an owner's test. It ends with her testing report (§13.1).

**What waits within her window** (each on someone's word, none on another builder's code):
- 7-195, on SW-5 L3 (§14.3);
- 7-196's clause alone, on the lead's measurement on the build machine (§14.4);
- B7.c (the tack at quarters) and B7.d (numbering by deck), on the lead's word (§6.7, §5.2);
- B7.e (the rank-4 rule), on the owner's answer and the lead's allotment (§8.3);
- the poop, the stern's face and the head as sourced lines, on Lavery's pages if the owner
  photographs them (§17.1 item 6); until then they are judged and marked so.

---

## 1. The module and the generator

### 1.1 Files

| Path | What | Owner |
|---|---|---|
| `tools/ships/bellerophon.py` | her data in the drawings' frame, the conversion, `write(out_dir)`, `build(out_dir)`, the checks of §1.5 | B7 |
| `tools/ships/period.py` | appends only: Steel's and Lavery's anchors for the 74 (`STEEL_ANCHORS[74]`), the 590 column (`REGULATIONS_COLUMNS[74]`), the 1812 patterns and the long 9 of 8 ft 6 in (§5.3) | B7 in her window (Build §4.2) |
| `data/ships/seventy-four.yaml` | generated only | B7, through the generator |
| `data/people/seventy-four.yaml` | her wardroom file, hand-written data in `data/people/sixty-four.yaml`'s form | B7 |
| `tests/test_bellerophon.py` | her tests and her truths drafted under 7-194 to 7-196 | B7 |

Her file's header is its own literal string and holds "Generated by tools/gen_ships.py", as
every file's does.

### 1.2 The import

Stage 0 laid the hook (`tools/gen_ships.py:8621`, `SHIP_MODULES = ("indefatigable",
"neufchatel", "bilander", "bellerophon")`, with the alias and the loop in the `__main__` block,
as Indf §1.2 measured). Her module begins `import gen_ships as g` and `from ships import period,
mizen_yard, spritsail_yards`, and calls `g.wardroom("seventy-four")` inside `build()`, never at
import. `mizen_yard` and `spritsail_yards` are pure and import nothing from `gen_ships` (Ext §9.3),
so no second copy of the generator arises. She runs last of the four.

### 1.3 What she reuses, and what she writes anew

**Reused through `g`** (lines at 8f30be9): `Builder` (`:650`) with its `descriptions` (`:1003`)
and `ground_tackle` (`:753`); `cloth` (`:353`), `rope_kn` (`:415`), `design_kn` (`:449`);
`FRIGATE_CANVAS` (`:189`); `staysail_from_cut` (`:1248`), `between_the_masts` (`:1297`),
`square_sail_lines` (`:1533`), `raked_x` (`:2619`, always with her own `deck_m=`); `hold_for`
(`:3467`), `pump_entries` (`:3537`), `wardroom` (`:3607`), `ration_entries` (`:3635`);
`KINGS_ROUNDS` (`:3706`), `fit_magazine` (`:3718`), `exercise_allowance` (`:3756`),
`broadside_pair` (`:3837`) with `deck=` and `round_to=0.01`; `_quad_area_centroid` (`:7162`);
`g.hull_profile` (`:587`); and from SW-2b.1 `g.hull_form`.

**Reused as modules:** `mizen_yard.py` (the course and the driver, Ext §9.3, §17.2) and
`spritsail_yards.py` (Ext §4.1), each pure, each asserting its geometry. If either needs an
extension for her (the driver's jaws, §4.6), B7 takes the file in her window (Build §4.2) and
re-runs B1's byte test on the 64's file.

**Written anew, after B1's patterns:** the mast and yard loop, the square sails, the head, the
staysails, the studding sails, the storm and occasional canvas, the groups and aliases, the fits,
the company, the quarter bill, the sail room and the stores. **Plainly:** that copies much of
B1's module. Copying keeps her bytes her own and touches no closed window; the duplication is
reported for a later shared module (§18 item 11).

### 1.4 The data, the frame and the conversion

- **The drawings' frame.** Positions in feet forward of AP (ZAZ1357's red dashed after
  perpendicular); heights in feet above WL1 (its top green waterline) or above K (the strip's top
  border, 0.59 ft under the main keel's lower edge), as Bel §3 gives every measure. One table at
  the module's head per measured line, each figure with its source in a comment.
- **The file frame.** x in metres forward of the mid-perpendicular, 84 ft before AP:
  `x_m = (ft − 84.0) × 0.3048`, as Bel's metres already are. z in metres above **the Channel
  line**: `z_m = (ft_above_WL1 − CHANNEL_FT) × 0.3048`, with `CHANNEL_FT = 5.44 − 62/12 =
  0.2733` (§2.2).
- **No trim.** The Channel line runs parallel to WL1, which keeps its drawn drag of 1.72 ft over
  the 168 ft. The engine has no trim, so a height above the water at its own station is what the
  engine believes, as for the 64. The reports' trim (1 ft 4 in by the stern in 1763, 1 ft 6 in in
  1783) would move the end sills by 5 cm at most (measured here), within the measured lines'
  uncertainty at the ends. Recorded.
- **To the file, once.** A spar's `height_m` and a sail's `corners_m` above the datum (her upper
  deck at midships, 3.16 m); a sail's `centre_height_m` and a gun's `height_m` above the water
  (the file's conventions; Indf §1.4).
- **Rounding** early, at the measured figure: 0.01 m for the hull, profile and sills; spars and
  sails as the frigate's (Indf §1.4; Indf §16 item 4).

### 1.5 The checks raised before her file is written

With `raise ValueError(...)` and a sentence, never `assert`:
- the lowest lower-deck sill 1.57 ± 0.01 m (5 ft 2 in, the report), and its triple's
  half-breadth within 0.03 m of 7.04 m;
- the displacement within Bel's H1 band, 2,490-2,900 t;
- every broadside gun of every fit on a triple of its deck to the centimetre, its deck named
  (Build §4.4);
- every measured port triple within 0.05 m of the drawn side (`g.hull_form`, `measured=`);
- the pieces of each fit 74, 82 and 78, and the broadsides by 70's rule 781, 867 and 938 lb;
- the company's sum 590, the marines 111, the idlers by trade summing to the idlers, the bill's
  `marines` no more than the marines;
- the driver's boom clear of the poop deck by the head room of §4.6 and above the taffrail, its
  four corners within 10% of Steel's area and its after leech within Steel's band (Ext §17.2);
- the mizen course's tack and throat on the mast's line, its clew clear of the poop deck at its x
  (§4.5), and the spritsails' feet above the water (the helpers' own assertions, Ext §9.3, §17.2).

---

## 2. The hull blocks

### 2.1 The figures

| Field | Figure | Source and mark |
|---|---|---|
| `length_waterline_m` | 51.2 | 168 ft between the perpendiculars, the length on the gun deck (ZAZ1357's table, read; 167.97 ft measured, Bel §3.2.1); D29 (b)'s rule, as the 64's. At WL1 the post's after face stands 0.85 ft abaft AP and the stem proper meets the water at 168.2-169.0 ft (measured, Bel §3.2.6). In the note: 51.5-51.8 m post to stem proper, 52.8 m to the knee's outer sweep |
| `beam_m` | 14.25 | 46 ft 9 in extreme, the design's and the Arrogants' contract (ZAZ1357's table, read; ZAZ1070, read; answer 4). 46 ft 1 in moulded (measured, Bel §3.2.4). In the note: *Elephant* as built 46 ft 11½ in (tentative); Charnock's 47 ft 4 in not supported (Bel §3.6) |
| `draught_m` | 6.46 | 21 ft 2½ in mean to K at the Channel line: WL1's 20.93 ft and the 0.27 ft (measured, figs.py). 6.74 m aft and 6.21 m forward to K; 6.29 m mean to the main keel. In the note: the 1763 report's Channel draughts 21 ft 6 in and 22 ft 10 in, mean 22 ft 2 in (Lavery p. 9); the *Audacious*'s 21 ft 0 in (Steel 1805 p. 212) |
| `displacement_kg` | 2,600,000 | Judgement within the measured band at her line. Bel §3.2.5 gives the drawn lines with plank and appendages at WL1 as 2,475-2,543 tons of 35 cu ft, which it prints as 2,530-2,600 t. The slice to the Channel line is 3.3 in at 16.0 tons an inch, 52-53 tons of 35 (measured here). So 2,528-2,596 tons of 35, which is 2,568-2,638 t at 2,240 lb a ton (measured here), or 2,583-2,653 t on Bel's printed tonnes. In the note: the *Audacious* 2,821 t (Steel 1805 p. 212); the report's draughts about 2,770-2,830 t (Bel §13.2) |
| `gm_m` | 1.36 | *Bombay Castle*, a Slade 74 of like size: 4 ft 5⁷⁄₁₀ in, "certainly stiff enough" (Steel 1805 p. 141, page image; Bel §3.2.5). KM about 7.8 m above K (measured, ±0.2 m) |
| `clr_x_m` | +5.5 to start | The measured centroid of the plane the file counts (to K, no rudder: 0.46-0.57 m abaft the mid-perpendicular, Bel §3.2.6), with the 64's tuned lead of 11.8% of her waterline ahead of it (`sixty-four.yaml`'s note): judgement. Tuned against the helm's truths (6 and 17) and the *Bellona*'s easy steering and weatherly helm (Lavery p. 9); recorded as tuned. The scratch 74 needed +6.5 on the frigate's rig (Bel §7.4) |
| `lateral_area_m2` | 330 | 3,503 sq ft below WL1 to K (measured, Bel §3.2.6) and 4.3 m² for the slice (measured here); the rudder left out, as the frigate's and the 64's |
| `hull_speed_kn` | 12.0 to start | No period figure. Judgement, tuned within 11.5-13.0 toward the owner's first goal of about 11 kn best (answer 14; §9). The scratch 74 at 12.0 makes 10.93 kn in 25 kn at the Channel line (observed here) |
| `deck_height_m` | 3.16 | Her upper deck at midships: the mean of the drawn top and middle lines, 10.77 and 10.52 ft above WL1 (measured, Bel §3.3; the checker's depth-in-hold test lands between them), 10.37 ft above the Channel line. ±0.1 m on which line is the surface (measuring task 8) |
| `rudder` | area 9.82 m², span 6.67 m, 35°, 3.0°/s | 104.8 sq ft and 21.6 ft below WL1 (measured, Bel §3.2.6), with the slice over its 3.4-ft breadth at the line (measured here); the angle and rate the frigate-36's (judgement) |
| `profile` | §3 | Build §5.1 and stage 0H's keys |

**The masts** stand where ZAZ1357 measures them at the upper deck, the fore moved by the Arrogant
alteration noted on ZAZ1359 "for the Bellerophon" among others (read; Bel §5.2): fore +19.84 m
(150.27 ft less 1 ft 2 in), upright; main −2.81 m (74.79 ft), raked 1.44°; mizen −17.43 m
(26.80 ft), raked 2.91°. The main stands about 1 ft further aft against the fore on ZAZ1359 and
1361F than on ZAZ1357 (Bel §5.2, §9); the sheer draught's, measured with her sills, is taken and
the other is in the note.

### 2.2 The foot between the drawing and the ship (Build §13.2; Bel §13.2)

**The facts.**
- On ZAZ1357 the midship lower sills (L7, L8) stand 5.44 and 5.45 ft above WL1, 26.38 ft above K
  (measured, two readers; Bel §3.1).
- The *Bellona*, the drawing's own ship, reported 5 ft 2 in to her lowest gun-deck port at her best
  Channel draught, 21 ft 6 in afore and 22 ft 10 in abaft (1763; Lavery p. 9, Table 2, read
  (owner's book)). In 1783 she gave 4 ft 8 in at her foreign-service draught, 21 ft 9 in and 23 ft.
- Three trial 74s at sea agree: *Brunswick* 5 ft 4 in at a mean of 20 ft 11½ in; *Bedford* 5 ft 2½ in
  at 21 ft 9½ in; *Bombay Castle* 5 ft 1½ in at 21 ft 10¾ in (*Collection* 1800 p. 11 and Steel 1805
  p. 140, page images; Bel §13.2).
- At the report's mean of 22 ft 2 in to K, the drawn sill would stand about 4.2 ft above the water;
  to the main keel, about 3.6 ft (measured, figs.py). The gap is 1.0-1.6 ft.

**Three ways:**

| | (a) The Channel line (taken) | (b) The report's draught on the drawn hull | (c) The report's draught, ports raised |
|---|---|---|---|
| Her water | where the drawn lowest sill stands 5 ft 2 in: WL1 + 0.273 ft | 22 ft 2 in mean on the drawn keel | 22 ft 2 in mean |
| Her lowest sill | 1.57 m, the report's | 1.28 m or 1.10 m | 1.57 m |
| Her lowest port shuts at | 10.35° (outside the plank) | about 8.0° or 6.5° (8.1° or 6.6° on the moulded side) | 10.35° |
| The drawing | the measured lines as drawn | as drawn | every port moved up about a foot, which no source draws |
| `draught_m` | 6.46 m, 0.3-0.5 m under the report's | 6.76-6.93 m | the same as (b) |
| What is recorded | the report's draughts beside the file's | the sill against the report | the move |

**Taken: (a).** The owner set the sill at sea (answer 5 as revised) and asked that the hull the
viewer draws and the hull that floats be one (answer 6). Build §5.1 sets every profile height
"above the file's waterline, taken as the load line its sill source states". (a) meets all three:
the freeboard, the figure the brief's truth reads, is the period's own for this hull, and the
gap sits in the draught's figure, which the engine reads for her resistance, her grounding and
the heel's lever. (b) contradicts the owner's sill. (c) invents a hull no draught shows.

**The foot that is left** is in the draught: the report's mean stands about a foot deeper than
the drawing gives at the same freeboard. Its causes stay open in her notes: the draughts' datum
(Steel's "underside of the keel" names neither keel: Bel §3.2.1), a deeper false keel as built,
or the ship as built standing higher on her keel than the 1758 drawing (ZAZ1142, the Arrogant
draught of 1759, has its sills 0.4-0.5 ft and its waterline 0.6 ft higher: Bel §3.1). No figure
moves to close it. **Plainly:** in shoal water she grounds about a foot later than the report's
draught would have her. Put to the owner (§17.1 item 1).

**What it costs.** The polar loses 0.04-0.06 kn at each best point between WL1 and the Channel
line (observed here, §9). Her displacement moves only her heel and inertia (Bel §3.5).

### 2.3 Which deck is the datum (D18)

Her upper deck is continuous from stern to stem; her quarterdeck and forecastle stand above it,
joined by gangways over the waist (Bel §3.3, §3.4). It is the 64's arrangement, so D18's (a) "the
uppermost continuous deck" and (c) "the deck she was worked from" are the same deck for her, as
Indf §2.2 found for the 64: 3.16 m above her water. Whatever the owner chooses for the razee, her
datum does not change.

---

## 3. The hull profile and her shape (Build §5.0-§5.3, §5.7)

### 3.1 The form

Build §5.1, written by `g.hull_profile` with every point key, then `g.hull_form` with `form`,
`marks` and `measured=` (SW-2b.1), from her first commit (Build §5.6: "B2, B4 and B7 write their
shape keys from their first commits"). Every z above the Channel line; x from the
mid-perpendicular. Her deck words are `DECK_WORDS`: `lower`, `upper`, `quarterdeck`,
`forecastle` and `roundhouse` (the poop, §3.5).

### 3.2 Her points, by line

| Key | Points (file frame, metres) | Source | Mark |
|---|---|---|---|
| `keel_m` | (−25.49, −6.74) at the post's heel to (+22.46, −6.24) at the main keel's square fore end, 157.7 ft | K, the bottom of the second drawn band, as the 64's (measured, Bel §3.2.1-§3.2.2, §3.2.6) | `sourced` |
| `stem_m` | below water, the outer fore edge: (+22.86, −6.06) the forefoot; (+23.76, −5.84), (+24.16, −5.54), (+24.73, −4.62), (+25.51, −3.10), (+26.18, −1.58), (+26.53, −0.97), (+26.90, −0.08); above it the stem proper to the stem head, **to measure** | Bel §3.2.6 (both readers within 0.3 ft). The outer line to 172.5 ft is the knee or gripe, drawn red at 15-18 ft of depth (identification open) | `judged` until task 2 |
| `head_m` | the knee of the head's fore edge, from where it leaves the stem to its top | below the water measured (Bel §3.2.6); above it **to measure** on 1357F | `judged` until task 2 |
| `stern_m` | the post: (−25.49, −6.74), (−25.86, −0.08), raking 3.2°; the counter's knuckle **to measure** (5.8 ft or 7.5-7.9 ft above WL1: two readings disagree); the taffrail (−28.04, 8.48) | Bel §3.2.6, §3.3 | `judged` until task 1 |
| `rail_m` | (−28.04, 8.48) the taffrail, (−25.60, 8.18), (−22.56, 7.81), (−19.51, 7.63), (−16.46, 7.51), (−13.41, 6.99), the drift (−13.35, 6.70), (−7.32, 6.35), (−4.88, 6.23), the breast (−3.05, 5.81), the waist (0.00, 4.82), (+9.45, 4.95), the forecastle (+12.50, 5.71), (+17.07, 5.89), (+20.12, 6.20), (+23.16, 6.42), ending at the beakhead bulkhead | Bel §3.3, "the top of the side" (the checker within 0.2 ft at five of six stations; tentative on which line is the rail); the bulkhead from *Dragon*'s upper deck (1362F, Bel §3.4) | `sourced` |
| `breadth_m` | at Bel §3.2.3's stations from 10 to 150 ft and at 135, 145 and 155 ft, where WL1 is read: the half-breadth at the water (WL1's with 4½ in of plank; the 0.27 ft moves it under 0.02 ft amidships) and at the rail (the top-timber line, **to measure**). WL1 at 160 ft is not resolved (under 13.7 ft), so that station waits for task 3 | Bel §3.2.3; 1357F's half-breadth plan | `judged` until task 3 |
| `wales_m` | the main wale at 81 ft from 0.18 m below the line to 1.12 m above it; along the length **to trace** | Bel §3.3 (the checker at 81 ft) | `judged` until task 3 |
| `section_m` | the midship section, plank on: the floor rising 0.3-0.4 ft from 3 to 8 ft out, the bilge from 9 to 17 ft, dead flat 22.95 ft from 17 to 23.5 ft above the keel, the tumblehome to 21.4 ft at 28 ft; above 28 ft to the rail **to trace**, carried on to the rail's half-breadth by judgement until then | Bel §3.2.4 (`hull/` traces in owner-notes) | `judged` until task 3 traces it above 28 ft (its points to 28 ft sourced, named so in the note); then `sourced`, old beside new |
| `decks_m` | lower 1.47 aft, 0.95 at midships, 1.60 at 165 ft; upper 3.65, 3.16, 3.80; quarterdeck 5.78 aft to 5.32 at 60 ft and its breast at 78-80 ft; forecastle about 5.43 from 121 to 162 ft; roundhouse §3.5 | Bel §3.3 (both readers within 0.03 ft; the surface the mean of the top and middle lines, ±0.1 m) | `judged` (the poop) until task 5 |
| `ports_m` | §3.3 | Bel §3.3 | `judged` (the forecastle's and the poop's places) until tasks 5 and 6 |
| `port_size_m` | lower 1.04 × 0.82 (3 ft 4¾ in by 2 ft 8½ in); upper 0.84 × 0.80; quarterdeck 0.79 × 0.71; forecastle as the quarterdeck's, for its two ports on *Dragon*'s plan; none for the roundhouse, whose triples are guns over the rail, not ports (§3.3; the schema takes a deck's ports without a size: `_profile_by_deck`, `schema.py:1555-1583` at 8f30be9) | Bel §3.3 | `judged` (the forecastle's) |

A line takes the word of its weakest point (§5.0 principle 4), and its note names the source by
sheet and the weak points by station. Until a point marked "to measure" is measured, the module
writes it as judgement in its note, never leaving it out silently.

### 3.3 The ports and their sills (at the Channel line)

**The lower deck:** fourteen a side, centres and sills measured on 1357F (Bel §3.3, both readers;
*Dragon*'s gun-deck plan within 0.1 ft at L7-L9). From aft, with the shut heel by 70's rule
(`combat/shot.py:116-120`, `PORT_SHUT_M` 0.3048 m) on the midship half-breadth with plank, 7.04 m
(measured here):

| Port | x (m) | Sill (m) | Shut (°) | Port | x (m) | Sill (m) | Shut (°) |
|---|---|---|---|---|---|---|---|
| L1 | −21.88 | 1.97 | 13.68 | L8 | +1.49 | 1.58 | 10.44 |
| L2 | −18.59 | 1.86 | 12.76 | L9 | +4.81 | 1.61 | 10.68 |
| L3 | −15.31 | 1.77 | 12.01 | L10 | +8.11 | 1.67 | 11.18 |
| L4 | −12.01 | 1.69 | 11.35 | L11 | +11.40 | 1.75 | 11.85 |
| L5 | −8.71 | 1.65 | 11.02 | L12 | +14.69 | 1.85 | 12.68 |
| L6 | −5.41 | 1.61 | 10.68 | L13 | +17.98 | 1.97 | 13.68 |
| **L7** | **−2.15** | **1.57** | **10.35** | L14 | +21.29 | 2.09 | 14.69 |

The guns are numbered from forward (§5.2), so L14 carries the lower deck's pair No. 1 and L7 its
pair No. 8.

- **The upper deck:** fourteen a side, the red altered positions taken as fitted (Bel §3.3): x
  −23.38, −20.12, −16.82, −13.53, −10.24, −6.95, −3.47 (tentative), −0.12, +3.26, +6.58, +9.88,
  +13.17, +16.46, +19.96 m; sills 4.03, 3.90, 3.79, 3.71, 3.64, 3.60, 3.57, **3.56**, 3.60, 3.64,
  3.72, 3.82, 3.94, 4.08 m (Bel's feet above WL1 less the 0.273 ft: measured here).
- **The quarterdeck:** seven a side at ZAZ1357's places (Q1-Q2 black, Q3-Q7 red), from aft: x
  −22.95, −19.96, −17.01, −14.20, −11.43, −8.50, −5.55 m; sills 6.06, 5.94, 5.84, 5.76, 5.70,
  5.64, 5.60 m. *Dragon*'s plan puts them 0.46-0.65 ft further forward (the checker); her file takes
  ZAZ1357's, whose sills are read, and the note gives both.
- **The forecastle:** two a side on *Dragon*'s plan at about +16.76 and +21.03 m (139 and 153 ft;
  ±1.5 ft, one reader). ZAZ1357 draws timberheads there and no port. Their sills are the
  forecastle deck at the port and the quarterdeck's measured height of sill above its own deck
  (about 1.0 ft over the drawn line: judgement) until task 6 measures them.
- **The carronades' places over the rail:** the 1795 fit's forecastle carronade at about 128 ft (x
  +13.41), and the poop's three places a side (§3.5). Each triple stands 2 in under the rail, so
  the gun's height is the rail's and it fires over it (the 64's convention, `OVER_THE_RAIL_M`;
  judgement). No source draws a port there. The triples are kept, since a broadside gun stands on
  one (Build §4.4), but her profile's note names them gun places over the rail, not ports, and the
  roundhouse is given no port size (§3.2). Package 81 draws the ports from the triples and
  `port_size_m` (Build §5.1), so a line for 81's design goes to the lead: a triple within
  `OVER_THE_RAIL_M` of the rail at its x is a gun place, not drawn as a port (§17.2 item 14).

### 3.4 The half-breadth at the sill, and the shut heels

- **At the midship lower sill** the side stands 22.70-22.76 ft from the middle line, moulded, on
  the body plan (measured, both readers; Bel §3.2.4). With 4½ in of plank, as the 64's (Indf
  §3.3; Steel's 5-in plank less judgement): **23.10 ft, 7.04 m**. The port's outer sill is outside
  the plank, and it is the outer sill that meets the water as she heels (judgement), so the
  triple carries 7.04 m.
- **At the other ports** B7 measures the half-breadth at each sill's height at the port's own
  station on 1357F's body plan (task 4). Until then the midship figure stands, which shuts an
  end port a little early: the safe side.
- **The upper deck's** sills stand above the section's measured 28 ft, on the tumblehome:
  about 6.3-6.5 m (judgement on 21.4 ft at 28 ft above the keel) until measured, which shuts the
  lowest at about 30-31°.

**What the sills give** (heel alone, `lee_port_shut`; measured here):

| Port | Sill | On 7.04 m (outside the plank, the file's) | On 22.7 ft moulded (the brief's) | On half the beam |
|---|---|---|---|---|
| L7, the lowest | 1.57 m | **10.35°** | 10.54° | 10.23° |
| The report's 5 ft 2 in exactly | 1.575 m | 10.39° | 10.58° | 10.27° |
| The end ports, on the midship figure | 1.97 m aft, 2.09 m forward | 13.68°, 14.69° | | |
| At WL1 as drawn (no rise) | 1.66 m | 11.1° | 11.3° | |
| At the 1783 report's foreign-service 4 ft 8 in | 1.42 m | 9.1° | 9.3° | |
| The upper deck, lowest | 3.56 m | about 30-31° on its own side | | |

**Plainly:** the brief's truth 7-195 reads "5 ft 2 in at Channel draught on 22.7 ft: shut at 10.6°
heel alone" (Build §15). Answer 7 takes the half-breadth "as the side's half-breadth at the sill,
from the same hull profile", and the profile's triples are outside the plank, as the 64's are
(her lowest port shuts at 10.6° on 6.67 m with plank, Indf §3.4). So her file gives 10.35°, a
quarter of a degree sooner than the brief's figure, which is the same sill on the moulded side.
Truth 7-195's band holds both (§14.3), and the trial 74s at sea shut at 10.15-10.7° (Bel §3.1).
Put to the owner within §17.1 item 1, and the truth's wording to the lead (§17.2 item 11).

### 3.5 The poop (the `roundhouse` deck)

- **What is drawn.** ZAZ1357 draws two tiers of quarter-gallery windows and the top rail rising
  from the drift scroll (40.2 ft from AP, 22.4 ft above WL1) to the taffrail. *Dragon*'s
  quarterdeck plan labels the captain's cabin from the stern to about 12 ft and the coach to about
  23 ft. No sheet read draws the poop deck (Bel §3.3).
- **What the file takes.** A poop over the cabin and the coach, from the taffrail to about 23 ft
  from AP (judgement on Bel §3.3's 23-25 ft), its deck at the side 1 ft 3 in under the rail (the
  64's roundhouse rule, measured there on ZAZ1280; judgement for her). Marked `judged`; task 5
  measures it on ZAZ1359 (the coach and the cabin's beams).
- **The word.** The deck word is `roundhouse`, the word the 64's file gives the same deck. The
  period called it the poop ("four poop carronades": James vol. 1 p. 265; Falconer, QUARTERS;
  Cumby p. 723). Her gun notes say so, the orders take "poop" for it (§6.4), and no deck word is
  added to `DECK_WORDS`.
- **What it bounds.** The 1795 fit's six carronades stand on it (§5.1), the mizen course's foot
  reaches over it to its clew (§4.5), and the driver's boom crosses it (§4.6). If Lavery's deck
  drawings are photographed (§17.1 item 6), its length and height become `sourced`.

### 3.6 Her shape keys under §5.0's ladder (each line's rung)

The rungs are §5.0's: **S** her own lines, her class's or a sister's; **S†** a period plan of her
type, scaled; **R** a named period rule on her own particulars; **T** judgement. The mark is the
line's weakest point. "After the tasks" is what B7's measuring (§3.7) is expected to raise it to.

| Line | Rung and mark (first commit) | After the tasks | What it is | Source; next |
|---|---|---|---|---|
| `sections_m` | **S**, `sourced` | — | WL1-WL5 at the sixteen stations from 10 to 160 ft, 79 points with the plank (WL1 at 160 ft is not resolved, so that station has WL2-WL5), each station low to high from WL5 up, z less 0.083 m. WL1 at 135, 145 and 155 ft goes into `breadth_m`'s water half-breadths at those x's (§3.2), where one point to a station is the form: in `sections_m` a station of one point is refused (Build §5.2) | Bel §3.2.3 (two readers, the checker's WL1) |
| `breadth_line_m` | **R**, `rule`: 21.82 ft at 40, 21.75 at 140, 19.43 at 150 read (S); the heights and the rest by Steel's rule for the heights of breadth (OCR l. 15190-15194) | **S** | the main breadth by station | 1357F's sheer and half-breadth plans (task 3) |
| `channel_wales_m` | **S** at midships, 2.54 to 3.33 m (8.6-11.2 ft above WL1, the researcher's, not re-measured); `judged` along the length | **S** | the channel wale between the lower port tops and the upper sills | task 3 |
| `head_m` | **T**, `judged` | **S** | the knee of the head above the water | 1357F (task 2) |
| `floor_m` | reserved; written only if the rising line is read | — | kept as found (principle 11) | 1357F |
| `rabbet_m` | reserved; written only when task 3 reads its height and siding on 1357F; not drawn | **S** | kept as found (principle 11). The research reads only its extent, about 100 to 154 ft (Bel §3.2.1), which stays in the note until then | 1357F (task 3) |
| `form.fullness` | **T**, `judged`: `[1, 1]`, the design's default rule | — | it fills only beyond the stations `sections_m` carries (abaft 10 ft and forward of 160 ft) | — |
| `form.stern` | **S** for its type: `square` (ZAZ1357's sheer, read); `knuckle_z_m` open; `transom_hb_m` **T**: so `judged` | **S** | the square stern over a counter | 1357F and ZAZ1359 (task 1); *Elephant*'s stern on ZAZ1247's front (1280 px, tentative) |
| `form.stern.round_up_m` | **T**, `judged`, by Steel's sheer-draught method (1805 pp. 250-251) | **S** | the transom's round-up | 1357F's body plan (task 1) |
| `form.stern.galleries_m` | **S**, `sourced`: two tiers from 8.5 ft abaft to 3.7 ft before AP (x −28.19 to −24.48), the lower at 4.33-5.31 m, the upper at 6.53-7.41 m | — | the quarter galleries, drawn on both quarters | ZAZ1357 (Bel §3.3, one reader ±0.3 ft) |
| `form.stern.lights_m` | **T**, `judged`: two bands at the galleries' tiers, the wardroom's and the captain's, placed by Steel's method | **S†** `stand-in` (Steel 1805's 74, Folio LI, cached); **S** if Lavery pp. 54-57 are photographed | the stern lights, plain marks | task 11; §17.1 item 6 |
| `form.head` | **T**, `judged`: `figure` | **S** if Lavery's decoration drawings come | her type certainly carried one (principle 9); carving later (Build §18) | §17.1 item 6 |
| the point lines of §3.2 | as §3.2 | as there | — | — |

- **Pictures for the eye.** Luny's painting shows two tiers of stern lights in a decorated frame
  and a quarter gallery; Chalon's shows her starboard side in 1815, with a gaff where her file
  carries the lateen yard (§4.5). Both are compared by eye with B5.6's drawing of her file; no
  point is taken from either.
- **The measured triples** she names in `measured=` are the lower deck's fourteen, the upper
  deck's fourteen and the quarterdeck's seven, once task 4 has taken their half-breadths at their
  own stations. `g.hull_form` raises for any of them more than 0.05 m off the drawn side. A triple
  still on the midship figure is reported, not asserted. **No triple is ever written from the
  drawing** (principle 8).
- **The drawn displacement** beside the filed 2,600 t, and the drawn depth beside the 6.46 m, go
  into her notes by `g.hull_form`.
- **The pair check** (Build §5.6): she is no class in two roles, so her outlines must differ from
  every other file's by 4 px or more in one view. The 64 is the nearest hull. They differ in her
  much flatter floor (2-3° of deadrise against the 64's 7-9°: Bel §3.2.4), her poop, her
  galleries' heights and her proportions. Measured at her build.

### 3.7 B7's measuring tasks

On the held images (`owner-notes/seventyfour/rmg/`: 1357F, 1359F, 1361F-1363F at full resolution)
by the research's method (its registration and scripts in `owner-notes/seventyfour/measurements/
hull/` and `hullcheck/`), with scratch scripts outside the repository. The figures go into the
module with their marks; the images and the traces stay in owner-notes.
1. **The stern:** the counter's knuckle (5.8 ft or 7.5-7.9 ft above WL1), the transom's
   half-breadths at the taffrail and the knuckle, the round-up, and the taffrail's height again,
   on 1357F and ZAZ1359.
2. **The head:** the stem proper's fore edge separated from the outer line, the stem above the
   water to its head, and the knee of the head (`head_m`), on 1357F.
3. **The breadths and the wales:** the top-timber line and the main-breadth line by station, with
   the heights of breadth on the sheer plan; the section above 28 ft; WL1 at 160 ft; the main and
   channel wales along the length; the rabbets at the line, for the waterline's own length; the
   keel's rabbet, its height and half-siding along its extent (`rabbet_m`).
4. **The ports' half-breadths:** the side at each lower, upper and quarterdeck sill's height, at the
   port's own station, on the body plan.
5. **The poop:** its deck and its rail on ZAZ1359 (the coach and the cabin's beams), with the
   beams' round-up at the middle line, the forecastle rail against its deck; the mizen course's
   clew against the poop (§4.5), **and then the driver's jaws** (§4.6), before the driver is cut.
6. **The forecastle ports** on 1363F at full resolution, and any chase port on *Elephant*'s
   as-built decks (J2938) and her building decks (ZAZ1065-1069, 1280 px).
7. **The bowsprit:** its heel and steeve against the stem head, on 1357F and 1359F, for
   `spritsail_yards.py` (the 64's 27°, ±2°, until measured).
8. **The decks' surface:** which red line is each deck's surface, on 1359F's limber strake and
   1357F's body plan (±0.35 ft today).
9. **The pumps** on *Dragon*'s gun-deck plan (1361F: chain pumps either side of the main mast at
   about 70.4 and 77.2 ft), counted.
10. **The braces** (§4.3): each yard's limit against the lee rigging, from Lavery's leads and her
    channels; and Steel's 74 rigging lists (vol. II pp. 37, 39-40, held) for the lines' sizes where
    legible (Ext §17.9 item 3).
11. **The stern lights:** Steel 1805's 74 on Folio LI (cached), as `stand-in`.

---

## 4. The rig

### 4.1 Masts

*Dragon*'s masts and yards (Lavery p. 19, Table 10; an NMM draught, Ch 7/19, of the class's own
time, about 1760: Lavery p. 23), read (owner's book). Steel 1794 vol. I p. 49's 74 column is
headed 1,799 tons, *Valiant*'s burthen (Bel §5.1; which ship it was drawn for is open, a
*Valiant*-size 74 or his 176-ft example), a larger ship than hers; *Dragon*'s masts run 0.97-0.98
of it and her yards 0.99-1.01 (Bel §13.4). So a mast Table 10 lacks takes Steel's length × 0.973, and a yard
Steel's × 1.00 (judgement).

| | Main | Fore | Mizen | Source |
|---|---|---|---|---|
| x; rake | −2.81 m; 1.44° | +19.84 m; upright | −17.43 m; 2.91° | measured (Bel §5.2); §2.1 |
| Heel above the keel's top | 5.11 ft (the shoulder) | 5.5-6.3 ft (5.9 taken) | 7.8-7.9 ft (the tenon's end) | measured (Bel §5.2) |
| Lower mast; head | 108-0; 15-0 | 95-8; 13-3½ | 93-6; 10-4¾ | Table 10, the main read as 36 yards (below); heads by Steel's rule (p. 42: 5 in a yard the main and fore, 4 in the mizen) |
| Masthead above her water; above the datum | 28.59 m; 25.43 m | 25.30 m; 22.14 m | 24.85 m; 21.69 m | measured here |
| Topmast; head | 64-10; 7-2½ | 57-9; 6-5 | 47-8; 4-7½ | Table 10; heads 4 in a yard, the mizen topmast 3½ (Steel p. 42) |
| Topgallant mast, its listed length | 33-0 | 28-10 | 23-10 | Table 10; the mizen's Steel's 24-6 × 0.973 (Table 10 has none; the mizen topgallant came in only in 1770: Lavery I23) |
| Long pole-head above the stop | 19-10 | 17-4 | 14-4 | Steel p. 42 (§4.2) |
| Bowsprit; jib-boom | 66-0 × 34⅛ in; 48-0 × 14⅛ in | | | Table 10 (its "flying jib boom" row taken as the jib-boom; judgement) |

- **The main mast.** Table 10 prints 30 yards (90 ft), shorter than its fore and mizen. Lavery's
  mast drawings measure the main 1.125 times the fore, 107 ft 7 in on Table 10's fore (measured on
  the owner's photographs, Bel §13.5), and Steel's rule on her design gives 107 ft 4½ in (p. 39,
  read). Read as 36 yards: 108 ft (judgement on a misprint; the three agree within 8 in).
- **Heels** on the keelson as ZAZ1359 measures them; **lower yards** slung 2 ft below the hounds,
  **topsail yards** to the topmast hounds, the rest by the frigate's rules, as Indf §4.2.

### 4.2 The topgallant masts: Steel's long pole-head (read here)

**Steel's words** (1794 vol. I pp. 41-42, read on the page image and in the OCR,
`docs/references/steel/steel-1794-rigging-and-seamanship-vol1-ocr.txt` l. 2934-2942 and
4701-4702). Topgallant masts "have commonly pole heads, either stump, common, or long". "A stump
pole-head is the length of a square head"; the common and long pole-heads are "set up from the
stop", a long one "two-thirds the length to the stop". The fractional table gives "Long pole-heads
to topgallant-masts" two-thirds of the length to the stop, when the square head's 3½ inches a yard
is taken out of the whole length.

**The reading** (judgement on those words): the table's topgallant length is the mast with a square
head of 3½ in a yard. A pole-head takes the square head's place and is set up from the stop. So a
stick with a long pole-head rises above the listed length: on her main topgallant, 33 ft less a
3 ft 2½ in square head is 29 ft 9½ in to the stop, and a pole of 19 ft 10 in above it. The 64's
design read a common pole of seven-eighteenths within the listed length (`indefatigable.py:342`,
`POLE_OF_TOPGALLANT = 7.0 / 18.0`), and on that reading Steel's spar and sail tables disagreed above
the topmast caps (Indf §4.3).

**What it gives** (the frigate's rules for the yards' heights, as the 64's; measured here):

| | Room on the long pole-head | Steel's table IV depth | Room on the 64's reading |
|---|---|---|---|
| Main topgallant; royal | 27.9; 20.8 ft | 30; 22½ ft | 18.2; 13.8 ft |
| Fore topgallant; royal | 24.3; 18.0 ft | 26¼; 20¼ ft | 15.9; 11.9 ft |
| Mizen topgallant; royal | 20.1; 14.7 ft | 21¾; 16½ ft | 13.2; 9.7 ft |

On this reading table IV's topgallants and royals hang within 7-11% of their depths, where the 64's
reading cuts them by about two-fifths. The 1773 establishment, which had no royals, gave the main
topgallant the same 10 yards of depth on the same 33-ft mast (Lavery pp. 19, 21, Tables 10 and 15),
which fits only if the topgallant's room is near its listed length.

**The file:** the owner's rule for the 64, "the spars rule" (Build §19.1 item 5, answered), on her
spars read so: each topgallant and royal cut between its yards, about 89-93% of Steel's depth,
Steel's cloths kept, Steel's areas in the note. **Plainly:** this reads the page the 64's design
read otherwise. Until the owner and the lead together rule on it, the 74 and the 64 read the same
Steel page two ways, and both files' notes say so. It is put to the owner for both ships (§17.1
item 2). The 64's file is B1's: if the owner says yes, it moves in B1's stage B if her window is
still open, else in a step the lead allots, old beside new (§17.2 item 8). If the owner says no,
her topgallants and royals are cut on the 64's reading, about 60% of Steel's depth.

### 4.3 Yards, studding-sail booms, braces and rope

- **Yards** (Table 10): main 96-8, main topsail 70-6, main topgallant 45-10; fore 84-4, fore topsail
  61-6, fore topgallant 40-0; cross-jack 61-6, mizen topsail 46-1; the mizen (lateen) yard 86-6 ×
  15⅜ in; spritsail 61-6 × 12¾ in, sprit topsail 40-0 × 8½ in (the yards on the bowsprit's and the
  jib-boom's rows, Bel §13.4's reading). Steel's column for the rest: the mizen topgallant yard
  31-6; the royal yards 35-0, 31-0, 23-0 (royals on all three masts: *Majestic* at the Nile, Bel
  §5.6). **Plainly:** Ext §4.1's file contract states the 74's spritsail yard 62 ft 0 in
  (18.90 m) and sprit-topsail yard 40 ft 6 in (12.34 m), which are Steel's column. Her class's
  Table 10 gives 61-6 and 40-0 (Bel §13.4), and her class's list rules, S before R, as for every
  spar of hers; `spritsail_yards.py` takes the length as given, and Steel's go in the note.
- **Heights** by the frigate's rules, as the 64's: the main topsail's 19¾ yards hang in 59.6 ft of
  room, the fore's 17½ in 53.3 and the mizen's 13⅞ in 45.0 (measured here): they fit.
- **Studding-sail booms** by Steel's p. 40 rules on her own yards: the lower boom five-ninths of the
  main yard, 53-8; the topmast booms half the lower yards, 48-4 and 42-2; the topgallant booms half
  the topsail yards, 35-3 and 30-9 (Steel's printed 53-9, 48-6, 42-6, 35-0 and 31-0 in the note).
- **Brace limits:** the frigate-36's (Fincham 1843 art. 102: main 64°, fore 62°, cross-jack 60°, two
  degrees more a level aloft), as the owner accepted them for the 64 ("Reasonable": the lee topmast
  backstays eased when the yards were braced sharp up; Indf §17, 2026-10-29). Answer 14 asks that a
  74's be looked for, so B7 computes each yard's limit against the lee rigging (task 10) from
  Lavery's leads (I24-I26: the fore braces aft to the main stays; the main brace to the quarter;
  the main topmast and topgallant braces to the mizen mast; the cross-jack brace to the aftermost
  main shroud; the mizen topsail and topgallant braces forward to the main mast; Bel §13.5) and her
  channels (main 39-74 ft at 17.2 ft above WL1, fore 119-148 at 16.8, mizen 11-24 at 19.8; Bel §3.3).
  The figures are recorded beside the frigate's; a limit changes only on the owner's word. The
  scratch 74 found these limits set her pointing (Bel §7.4).
- **Rope:** `FRIGATE_ROPE` scaled by √(her plain sail ÷ the frigate's 1,584 m²), 1.19 on 2,226 m²
  (measured here; judgement, as the 64's). Spar ratings from the rating pass.

### 4.4 Sails

Steel's table IV, 74 column (Bel §5.6, read on both copies' page images), at 22½ in a cloth; ±10%
the four-sided, ±25% the four-sided staysails; **unscaled**. **Plainly:** Bel §5.1 scaled Steel's
areas by 0.914-0.949 for a 168-ft ship. The class's own yards are Steel's within 1% (Bel §13.4),
and the 1773 establishment gave a 74 sails as large or larger (Lavery p. 21, Table 15), so a sail
cut to her yards is Steel's.

| Sail | Steel's cloths and depth | Area, m² | 1773 (Lavery p. 21), m² |
|---|---|---|---|
| Main course; fore course | 46/48/15¾; 40/38/13 | 387; 265 | 412; 279 |
| Main, fore, mizen topsails | 30/47/19¾; 26/41/17½; 20½/30/13⅞ | 397; 306; 183 | 408; 316; 195 |
| Main, fore, mizen topgallants | cut to the spars (§4.2) | 126; 95; 63 (Steel's 136, 103, 68) | 136, 103 |
| Main, fore, mizen royals | cut to the spars | 70; 53; 33 (Steel's 76, 60, 37) | none in 1773 |
| Mizen course (§4.5) | 16/17; leeches 11 and 21 yd | 138 | |
| Driver (§4.6) | 25½/32½; leeches 11 and 24 yd | 265 by Steel's rule; 281 the four corners | the 1773 driver, not built |
| Sprit course; sprit topsail | 29/29/8; 18½/29½/10 | 121; 125 | |
| Jib; fore topmast staysail; fore staysail | 0/26/25; 0/21/17½; 0/22/13 | 170; 96; 75 | |
| Main, main topmast, middle, main topgallant staysails | 0/31/15¾; and Steel's | 128; 228; 150; 118 | |
| Mizen, mizen topmast staysails | 20½/22½; 19/20 | 126; 107 | |
| Studding sails: fore lower; main and fore topmast; main and fore topgallant | Steel's | 141; 211, 155; 70, 58 | |

- **Plain sail** (courses, topsails, topgallants, the fore topmast staysail, the jib, the mizen
  course): **2,226 m²** (measured here), against the frigate's 1,584 and the 64's 1,826. Per
  displacement to the two-thirds power: 11.8, against the frigate's 13.5 and the 64's 10.9.
- **Staysails between the masts** by `between_the_masts` on her geometry, cut to Steel's table IV
  figures within the bands, as the owner agreed for the 64 (Indf §17, 2026-10-29). Steel's 74 column
  has no mizen topgallant staysail; none is built. The middle staysail is in the establishment of
  30 July 1773 (Lavery p. 21, Table 15: 24 and 24 cloths), though Lavery's note on I31 dates it
  after 1773 (Bel §13.5): hers is Steel's of 1794, whichever stands.
- **One jib**, Steel's "Jib Flying", on the jib-boom. *Majestic* lost a flying jib and a jib at the
  Nile (NRS vol. 2 p. 65, page image; Bel §5.6): a second jib in 1798 whose figures no table gives.
  Recorded, not built.
- **Reefs** by Steel (Bel §5.6): two in each course; four in the main topsail, three in the fore and
  mizen topsails; one in the mizen course a fifth up its mast leech; two diagonal in the spritsail
  (Ext §4.1); none in the driver.
- **Royals** set flying (Steel 1794 vol. I p. 214, as the frigate's file cites it).
- **Studding sails:** the frigate-36's set at Steel's cloths. Steel's main lower studding sail
  (184 m²) against one pair of lower booms is recorded and not built, as the 64's.
- **Canvas** by Steel's numbers for a 74 where `FRIGATE_CANVAS` lies in Steel's range.

### 4.5 The mizen course on its yard (answers 2 and 3 as revised; Ext §3)

- **The yard** `mizzen.yard`: class `lateen_yard`, 86 ft 6 in × 15⅜ in (26.37 m; Table 10; Steel's
  84-0 in the note), slung at its truss with about 0.48 of it forward of the mast and bare (Lavery
  I32, measured by eye on the owner's photograph: Ext §2); no `brace_limit_deg`; lines by Ext §3.4
  (the jeers, the lifts and Steel's derrick, two vangs, two bowlines as guys; no brace).
- **The sail** `mizzen.course`: class `lateen`, `cut_at_mast: true`, roles `yard` and `mast`, cut
  by `mizen_yard.py` from Steel's cloths and leeches (16 and 17 cloths; fore leech 11 yd, after
  leech 21 yd): about 138 m², its head rising 30 ft over 30 ft (Ext §2's table, measured there).
- **Its tack** 9 ft above her quarterdeck at the mizen, so that the throat stands where Lavery's
  I32 draws it, about 42 ft above the deck (measured by eye on the owner's photograph: Ext §2,
  §17.1), with Steel's 11-yard fore leech below it. The quarterdeck there stands 5.58 m above her
  water (18.6 ft above WL1, interpolated between 19.24 ft aft and 17.72 ft at 60 ft: measured
  here), so the tack stands 8.32 m above her water (27.6 ft above WL1) and the throat about 15.2 m
  above the datum. Ext §17.2's figures for her driver were measured on this throat.
- **Plainly:** Steel has the fore leech "attached to the mizen-mast within 6 or 7 feet of the deck"
  (OCR l. 11441-11442), a rule for every ship, and B1's 64 takes 6 ft 6 in
  (`MIZEN_TACK_ABOVE_DECK_FT = 6.5`, `indefatigable.py:398`). The drawing of her class's mizen is
  taken before his general words, for two reasons on her own profile (measured here,
  `probe/mend_figs.py`, the poop judged as §3.5). Cut by B1's rule, the foot level at the tack
  and 9.71 m long (Ext §2), the course's clew lands 5 ft abaft AP: at 6 ft 6 in it stands about
  1.4 ft inside her judged poop deck there, at 9 ft about 1.1 ft clear of it. And the driver,
  whose throat is the course's (Ext §17.2), cannot be cut within Ext §17.2's checks under the
  lower throat (§4.6). Steel's 6 ft 6 in and the 2½ ft between go in the note; task 5's poop
  checks the clew again (§1.5). The course's corners are physics: the higher tack lifts its centre
  by 0.76 m, recorded in her polar notes.
- One reef band; canvas No. 2; one unsided sheet to the taffrail, one tack; the storm mizzen
  `in_place_of` it.
- **Groups:** "plain sail", "all sail", "fore-and-aft sails"; never "courses" (Ext §3.4).
- **The rig's date.** One file, one rig (Bel §13.5). Chalon's painting shows her with a gaff in
  1815, and no "mizen yard" appears in her logs after 1794 (Bel §5.4). In the 1815 scenario she
  carries the earlier spar; the owner accepts that (answer 15).

### 4.6 The driver (Ext §17; the owner's choice)

By `mizen_yard.driver(...)` with her figures, under its two rules (the course filed before the
driver; no driver unless the course is cut at the mast):
- **The sail** `mizzen.driver`: class `lateen`, `cut_at_mast: true`, roles `yard`, `mast` and
  `boom`; `in_place_of: mizzen.course`; `bent: false` (the sail room); "occasional sails" alone;
  canvas No. 5; no reef band. Steel's 25½ and 32½ cloths, fore leech 11 yd and after leech 24 yd
  (Bel §5.6): 265 m² by Steel's rule, 281 m² on the four corners at Steel's fore leech (+6%: Ext §17.2,
  measured there), **unscaled**, for §4.4's reason (Ext §17.2 left the scaling "her design's call").
- **The boom** `mizzen.boom`: by Steel's p. 40 rule her own main topsail yard's length and fore
  topsail yard's diameter, 70 ft 6 in × 12¾ in (21.49 m). Ext's 70 ft 0 in × 13 in was Steel's
  column's yard. Level; the clew about 7 m beyond the taffrail.
- **The driver yard** is not filed (Ext §17.2): her fore topgallant yard's 40 ft 0 in by Steel's
  rule bounds the peak, no more than two-thirds of it beyond the mizen yard's peak.
- **Aliases:** "driver", "spanker", "driver boomsail"; "driver boom", "spanker boom".

**The jaws' height, set by her measured poop (task 5).** Ext §17.2 fixes the boom's height first,
clear of the quarterdeck rail, the roundhouse and the taffrail, and cuts the sail to it. The
driver's throat is the course's, and its fore leech at Steel's 11 yards is the course's too, so
Steel's leech puts her jaws at the course's tack: 9 ft (2.74 m) above her quarterdeck at the
mizen, 27.6 ft above WL1 (§4.5), as Ext §17.2 found on I32 (about 2.7 m). Against her profile
(measured, Bel §3.3, ±0.2 ft on the rails; the poop judged, §3.5; measured here):
- the taffrail stands 28.1 ft above WL1, so a level boom at Steel's leech passes about 6 in under
  its top;
- the judged poop deck stands 1 ft 3 in under its rail, 23.9-26.8 ft above WL1 from its break to
  the taffrail, so the boom would stand only about ¾-3¾ ft above the deck, over the 1795 fit's
  six poop carronades.

So: **B7 measures the poop in task 5 before the driver is cut**, then sets the jaws so that the
boom clears the poop deck by head room over its whole length (6 ft, judgement: room for the poop's
people and its carronades' crews to work beneath it) and clears the taffrail. On the judged poop
that puts the jaws 32.8 ft above WL1: 5¼ ft (1.60 m) above Steel's leech, 14¼ ft above the
quarterdeck at the mizen and 4¾ ft above the taffrail. The fore leech then shortens by as much, to
8.46 m. Raising a level boom with the head fixed takes about a strip of the foot's 18.57 m off the
sail: the four corners about 251 m², 5% under Steel's 265 m² (arithmetic here on Ext §17.2's
figures; re-measured by B7). The after leech shortens by about as much, from its 22.73 m to about
21.13 m, and must stay within Steel's band of 2 to 4 yards deeper than the course's (21.03-22.86 m:
Ext §17.2), which holds for a raise up to 1.70 m. The margin is 0.10 m, and it is narrow: a poop
measured higher, or the beams' round-up at the middle line where the boom passes, can take it.
If the four corners fail 10% of Steel's area, or the after leech its band, B7 reports it to the
lead rather than force the cut (Ext §17.2's rule), with the measured figures and three ways: less
head room (5 ft gives a raise of 1.29 m, the after leech 21.44 m and the corners about 257 m²), a
driver cut more than 10% under Steel's area, or `DRIVER = False` (§17.2 item 13). If
`mizen_yard.driver()` cannot take her jaws, B7 extends it in her window (§1.3).

*Under Steel's 6 ft 6 in tack* (rejected, §4.5) the same arithmetic gives: the boom at Steel's
leech 3 ft under the taffrail's top and through the judged poop deck aft of about 6 ft before AP;
a raise of 2.36 m (7¾ ft) for the 6 ft of head room; the after leech about 20.4 m, under Steel's
band; the four corners about 237 m², 10.6% under Steel's area. Both of Ext §17.2's checks fail
(measured here, `probe/mend_figs.py`).

**Plainly:** the sail's corners are physics, so the jaws move the driver's area and centre; each is
recorded in her polar notes with the driver bent. The boom over the poop is otherwise drawing.

**The period:** the driver was bent beside the course and brailed; the game shifts one for the other
in about fifteen minutes by the file's times, seventeen at the 64's company, its boom going out with it (Ext §17.3, §17.11). *Vanguard*, an Arrogant, "Set driver" at the Nile (NRS vol. 2
p. 53): §9's check S7 is taken with the driver bent. The 1773 driver hung abaft a set course (Lavery
Table 15) is not built (the lead's ruling, Ext §14 item 10).

### 4.7 The head, and the yards under the bowsprit (D8 (b); Ext §4)

- Bowsprit 66-0 and jib-boom 48-0 (Table 10); the steeve and heel by task 7, the 64's 27° (±2°) the
  fallback (judgement); `x_m` at the stem head.
- **The spritsail yard** `spritsail.yard`, 61-6 × 12¾ in, slung under the bowsprit near the cap,
  with no halyard; **the sprit-topsail yard** `sprit_topsail.yard`, 40-0 × 8½ in, on the jib-boom
  near its end, its halyard standing for the traveller's outhauler; both by `spritsail_yards.py`
  from the steeve and length, each foot above the water (its assertion). Lines by
  `square_sail_lines`; the guys as `guy` lines (Ext §4.1).
- **Sails:** the sprit course (121 m²) and the sprit topsail (125 m²), Steel's; group "spritsails"
  and "all sail", never "plain sail" (Ext §4.1; the owner's acceptance).
- **Their brace limits** by the leads to the fore stay and the fore top (Lavery I30): the angle at
  which each brace's lead meets the yard, measured on her spars (judgement), reported.
- **The period:** at the Nile she wore clear of *L'Orient* "setting her spritsail" (James vol. 2
  p. 180, read (OCR); Bel §5.5).

### 4.8 Storm and occasional sails, groups, aliases

As the 64's at her stage B (Indf §4.7): the storm mizzen `in_place_of` the course; the storm
staysails; the driver among the occasional sails; no ringtail (the boom carries the driver, and no
source gives a 74's ringtail: judgement). The frigate-36's groups with "spritsails" added, the
names the engine reads. Aliases "mizen", "mizzen", "mizen course", "mizzen course" →
`mizzen.course`; "mizen yard" → `mizzen.yard`; "spritsail", "sprit topsail". Mast ids `fore.`,
`main.`, `mizzen.` (two z's: `crew/hands.py:104-108`).

---

## 5. The guns

### 5.1 The fits

| Fit | Lower | Upper | Quarterdeck | Forecastle | Roundhouse (poop) | Pieces | Broadside (70's rule) | Source |
|---|---|---|---|---|---|---|---|---|
| "arrogant class 1793" | 28 long 32 | 28 long 18 (40 cwt) | 14 long 9 (7 ft 6 in) | 4 long 9 (8 ft 6 in) | — | 74 | 781 lb | James vol. 1, Abstract No. 1 (page image; Bel §4.1); ZAZ0890's armament block (read); Lavery p. 21, Table 18 (the *Bellona*'s guns of 1761: 14 nines of 7½ ft and 4 of 8½ ft, the longer the forecastle's: judgement; the 8½-ft nines depart from answer 12's pattern, §5.3) |
| **"arrogant class 1795"** (default) | as 1793 | as 1793 | as 1793 | as 1793, and 2 × 32-pdr carronades over the rail | 6 × 18-pdr carronades | 82 | 867 lb | the Admiralty Order of 19 November 1794 as James tabulates the small 74s (vol. 1 p. 256 and Abstract No. 3, page images) |
| "as the bellona 1812" | 28 long 32 | 28 long 18 (42 cwt) | 6 long 12 (7 ft 6 in) at Q5-Q7; 8 × 32-pdr carronades at Q1-Q4 | 2 long 12 (9 ft) at the after ports; 2 × 32-pdr carronades at the fore ports | 2 × 18-pdr and 2 × 12-pdr carronades | 78 | 938 lb | Lavery p. 22, Table 19 (the *Bellona* at Chatham, 6 January 1812; TNA ADM 160/54 by Lavery p. 23), read (owner's book); the places by the order of 17 March 1797 (James vol. 2 pp. 119-120, read (OCR)) |

- **The default** is the owner's (answer 3: "1795-1805 (82, the default)"). James tabulates six poop
  carronades of 18 pounds for the class; *Bellerophon* threw "four poop carronades" overboard in
  June 1795, calibre not given (vol. 1 pp. 265-266), so she carried at least four. Six are taken,
  the order's figure; the four in the note.
- **The 1795 places:** the forecastle carronade at about 128 ft, between the forecastle's breast and
  its first port (judgement; the 64's at 127.9 ft); the poop's three a side at about 4, 12 and 20 ft
  from AP (judgement on a poop of about 23 ft, §3.5).
- **The 1812 places:** long guns in the wake of the main and fore shrouds, carronades elsewhere, by
  the 1797 order, on the measured channels (judgement): the long 12s at Q5-Q7 (46.5-65.8 ft from AP,
  in the main channel's 39-74 ft) and at the forecastle's after port (139 ft, in the fore channel's
  119-148). **Plainly:** the list leaves four long guns a side, so Q2, in the wake of the mizen
  shrouds (18.5 ft, in the mizen channel's 11-24), takes a carronade against the order's letter
  (judgement: the main and fore shrouds' ports first). Maitland's *Bellerophon* of 1815 had long 9s
  at the shrouds, not 12s (Maitland 1826 p. 79, read (OCR)): in the note.
- **The 1812 poop.** Table 19 lists two 12-pdr carronades among the 78 pieces. Their place on the
  poop beside the two 18s is judgement: Table 19 names their founder (HCo), and Lavery's Table 17
  dates 12-pdr carronades in a 74's establishment to 1793 and 1812. Another reading, the boats'
  guns, is in the note (judgement). The owner's 78 is kept.
- **Not her fits:** the *Bellona*'s 12-pdr poop carronades of 1793 (she is not on James's list);
  the *Mars* fit.
- **No chasers.** No chase or stern port is drawn on the deck plans of 1759 (Bel §3.4). Task 6
  reads *Elephant*'s as-built decks; if they show bow ports, a pair of forecastle guns is filed as
  chasers in the fits that carry them, the broadsides re-measured.

### 5.2 Places, numbers and the deck

- **Built** with `g.broadside_pair(..., deck=<word>, round_to=0.01)` at each port's own measured x
  and sill, so each gun lands on its triple to the centimetre (Build §5.3; Indf §5.2's reassignment
  is not needed with `round_to`).
- **Numbered on across decks from forward, the lower deck first:** lower 1-14, upper 15-28,
  quarterdeck 29-35, forecastle 36-37, the 1795 forecastle carronade 38, the roundhouse 39-41. A
  place keeps its number in every fit; a fit that leaves a place empty leaves a gap. So her lower
  deck's pairs run from No. 1 forward, as the period's deck numbering began; the period's single
  guns 2n−1 and 2n are her pair n. Cumby's junior lieutenant "commanded the seven foremost guns on
  each side of the lower deck" (p. 721): her pairs 1-7, the period's Nos. 1-14.
- **The deck word** on every gun: `lower`, `upper`, `quarterdeck`, `forecastle`, `roundhouse`.
- **Plainly:** the period numbered each deck from No. 1: "No. 1 being the foremost gun on the
  larboard side; and No. 2 the foremost on the starboard side on each deck" (the Regulations, 1808
  printing, the Gunner, p. 215, OCR l. 12760-12763). The Regulations number single guns; the engine's crew
  serves a gun and its opposite as one pair (Falconer, QUARTERS; Glascock 1836 vol. II p. 234),
  and the game names a gun by number and side. So a pair keeps one number, as the eight files'
  pairs do. Her upper deck runs 15-28 where the period's ran 1-14.

**Numbering by deck: the option Indf §5.2 handed to her design** ("Renumbering from No. 1 on each
deck waits for a deck-aware pair key, the 74's design to propose, and both files then take it
alike"). It is offered to the lead as step B7.d. What it needs, each keyed so no other file moves:
1. **An explicit key**, never inferred from repeated numbers: `numbering: by deck` in the file's
   `armament` (`ARMAMENT_KEYS`, `ArmamentSpec.numbering: str | None = None`, left out of the pickle
   while None), laid inert in stage 0c (§12.1 item 2). Under it every broadside gun of every fit
   must name a deck and `(deck, number, side)` is unique; without it `(number, side)` is unique as
   now (`schema.py`, validate, :2104-2110). After SW-2 every file names its decks, so only an explicit
   key keeps the eight under the stronger check.
2. **Gun ids re-keyed by deck.** `g.broadside_pair` writes `gun.{number}.{side}` (`gen_ships.py:3837`),
   so by-deck numbers would collide across decks, and B7 may not edit the generator. Her module
   re-keys each id after the call, to `gun.{deck}.{number}.{side}`, as Indf reassigned keys after it.
3. **`Gun.by_deck`**, a plain class default `False`, left out of the pickle while false (stage 0c),
   set from the armament's key where the ship builds her guns (`ship/graph.py`, B3's).
4. **`Gun.pair_key`** (`parts.py:621-626`) `gun:<deck>:<n>` when `by_deck`, else `gun:<n>` as now;
   **`Gun.name`** (`parts.py:589-601`) "No. 3 starboard gun of the lower deck" when `by_deck`.
5. **The quarters' parse sites taught the key** (`crew/quarters.py:349-350` `_guns_words`, `:447`
   `_preferred_stations`, `:467` `_rob_order`): each tests `isdigit()` on the key's tail today, so
   `gun:lower:3` would be taken for a chaser in stations, robbing and words. Under the key the tail's
   last part is the number and its middle the deck.
6. **The orders:** a number with its deck ("No. 3 starboard on the lower deck", "the lower deck's
   No. 3"); a bare number refused in words on a ship numbered by deck ("She has a No. 3 on each
   deck: name the deck.").
7. **Both two-deckers together.** The 64 and the razee renumbered by deck in the same step, a few
   lines of `indefatigable.py` (B1's, window closed), their bytes and gun names moving old beside
   new, any of B1's tests that name a gun by id moved with them. **Pick:** B7.d at the end of her
   window, on the lead's word, with both two-deckers; if the lead declines the 64's renumbering, both
   wait for a later package together, so that the two two-deckers never number two ways.

### 5.3 Patterns, weights and crews (answer 12)

| Piece | Pattern and weight | Crew | Source |
|---|---|---|---|
| Long 32 | 9 ft 6 in, 55 cwt | 13 | Adye 1804 p. 155 (`period.SEVENTY_FOUR_PATTERNS`); Lavery Table 17, 1760-1812; Table 19's 55-56 cwt |
| Long 18 (1793, 1795) | 9 ft 0 in, 40 cwt | 9 | Adye p. 155; Lavery Table 17, 1761 |
| Long 18 (1812) | 9 ft 0 in, 42 cwt | 9 | Lavery Table 17's type of 1812, which Adye lacks (his 9-ft 18-pdr is 40 cwt); Table 19's 28 weigh 41⅛-42⅞, mean 42.0 (measured here) |
| Long 12 (1812) | 9 ft 0 in, 34 cwt; 7 ft 6 in, 29 cwt | 7 | Lavery Table 17, 1812; appended to `period.py` |
| Long 9 | 7 ft 6 in, 24½ cwt (quarterdeck); 8 ft 6 in, 27½ cwt (forecastle, 1793 and 1795) | 6 | Adye p. 155; Lavery Tables 17-18, 1761 (Table 17 gives the longer 27½ cwt, Table 18 prints 27); the 8 ft 6 in appended to `period.py` |
| 32-pdr carronade | 4 ft 0½ in, 17⅛ cwt | 4 | Adye p. 72 (`period.ADYE_CARRONADE_CWT`); Table 19's 17¼-18 cwt in the note |
| 18-pdr carronade | 3 ft 3 in, 9 cwt | 4 | Adye p. 72 |
| 12-pdr carronade | 6 cwt | 4 | Lavery Table 17; appended to `period.py` |

- **The rule for a weight** (judgement): a piece takes its pattern's weight, Adye's where he gives
  one (p. 155 for the long guns, p. 72 for the carronades), else Lavery's Table 17 for its date.
  The fits differ by pattern, never by the founders' scatter. Table 19's weighed pieces of 1812 go
  in the note: the long 32s 55¼-56¾ cwt (mean 55.8), the 32-pdr carronades 17¼-18 (mean 17.65),
  the 18-pdr carronades 9¾ and 10⅛, the 12-pdr carronades 6.56-6.60 (measured here). The long 18
  of 1812 is no exception: Table 17 lists a 9-ft 18-pdr of 42 cwt as a type of 1812, beside the
  40-cwt gun of 1761.
- **Plainly:** so "as the bellona 1812" keeps Adye's carronade weights and Table 17's 6 cwt, 3-10%
  under the *Bellona*'s own pieces of 1812. A gun's weight enters the chance that a shot dismounts
  it (`combat/hits.py:241-242`), so her 1812 carronades are dismounted a little more readily than
  her own pieces would have been. Recorded, not tuned.
- **Plainly:** answer 12 set the 9-pdr's pattern at 7 ft 6 in and 24½ cwt (Bel G4: 23-24½). The
  *Bellona*'s own list of 1761 (Lavery p. 21, Table 18) puts four of 8 ft 6 in on her forecastle,
  and her class's list is taken before the pattern for the 1793 and 1795 fits' four forecastle
  nines: 27½ cwt by Table 17, where Table 18 prints 27.

Crews by Falconer 1780 (QUARTERS) and Douglas 1829 (art. 136): `period.FALCONER_CREW`,
`DOUGLAS_CARRONADE_CREW`. One side's guns take **362** men in the 1793 fit, **378** in 1795 and
**364** in 1812 (measured here; Bel §4.5's 378). A long gun's phases scale by its weight against
42 cwt, never above one (`combat/guns.py`), so her 32s serve at the 18s' pace in the engine.

### 5.4 The magazine, the charges, exercise and filling

- **`fit_magazine`** with `KINGS_ROUNDS` (judgement, as every King's file). The Ordnance's
  allowance a gun is open (Bel §10 item 8).
- **Charges** from Table No. 29 through `charge_lb` once SW-1 has filled `CHARGE_TABLE_LB` (read on
  the page image, Build §10): the long 32 10 lb 10 oz (the share gives 10 lb 11 oz), the 18 6 lb,
  the 12 4 lb, the 9 3 lb; carronades 32-pdr 2 lb 10 oz, 18-pdr 1 lb 8 oz, 12-pdr 1 lb. Under the
  lead's rule the table serves the new ships alone if a figure of the eight would move (the lead's
  notes, stage 0 read, item 1). No override in her module.
- **Exercise:** `g.exercise_allowance(28, decks=2)` = 9, a third of her upper deck's 28 eighteens
  (the Regulations, the Gunner, Art. XXI, OCR l. 13122-13144), with `period.TWO_DECKS_EXERCISE_NOTE`.
- **Filling:** the bill's `filling: 18`, the 590 column's quarter gunners (the Regulations 1808
  printing p. 165 and leaves 455-460, page images; Bel §4.3). Falconer's rule, a quarter gunner to
  every four cannon, gives 18 on the 1793 establishment's 74 pieces and 20 on the default's 82
  (`g.filling_party`): the carronades were never rated cannon. Lavery's 1766 allowance says one to
  every four guns (p. 17). The note says so.

### 5.5 Broadside weight by 70's rule (measured here)

`far_ship` counts one side's broadside guns and every chaser (`combat/far.py:104-108`); she has none.

| Fit | Broadside | Against the frigate-36's 421 lb |
|---|---|---|
| arrogant class 1793 | 781 lb (James's 781) | 1.86 |
| arrogant class 1795 | 867 lb (James's 867) | 2.06 |
| as the bellona 1812 | 938 lb | 2.23 |

Recorded and pinned in 7-194; the brief's broadside truth is the razee's (7-188).

### 5.6 Later armaments, as data for the scenario editor

The degrees the sources allow (brief item 4; Build §8.1): on the quarterdeck and forecastle, a long
9 or 12 in the wake of the shrouds and a 32-pdr carronade elsewhere, the long guns within four (at
most six) of those established (the 1797 order); on the poop none to six carronades; the two gun
decks' 56 fixed. The form the editor reads is SW-4's.

---

## 6. The company, the marines, the quarter bill by deck and the people file

### 6.1 The company, 590 (answer 10)

On the Regulations' table of 31 December 1806, the 590 column (1808 printing p. 165 and leaves
455-460, page images, read row by row; Bel §4.3), in the 64's form:

| Station | Count | Basis |
|---|---|---|
| Posts | 16 | the column's first row, 14 (captain, five lieutenants, master, second master, surgeon, carpenter, boatswain, gunner, purser, chaplain), and the sailmaker and the master-at-arms, posts in the frigate's and the 64's files |
| Marines | 111 | §6.2 |
| Idlers | 44 | the column's rows by trade: carpenter's crew 11 (the carpenter's mate and crew of eight, the caulker and the caulker's mate); sailmaker's crew 4 (the mate, two crew, the ropemaker); cooper 1 (paid but not numbered; judgement); armourer 3 (the armourer and two mates); cook 2 (the cook and the cook's mate); steward 3 (the steward, the steward's mate, a gunroom steward: judgement); servant 14 (the third-class boys, who replaced the officers' servants in 1794: James vol. 1 pp. 256-257, page image; judgement, as the 64's servants); surgeon's mate 2 (the assistant surgeons); clerk 2 (the clerk and the schoolmaster); master-at-arms's party 2 (the ship's corporals) |
| Seamen | 419 | forecastle 65, fore top 55, main top 69, mizzen top 32, afterguard 115, waisters 83: the frigate-36's shares (judgement, as Indf §6.2); the column's petty officers, mates, midshipmen and first- and second-class boys among them |

- Ratings 0.30 able, 0.40 ordinary, 0.30 landsmen, the frigate-36's (judgement). The *Bellona*'s
  company in 1761 (Lavery p. 17, Table 7) is recorded.
- **The posts are free strings** (`PostSpec`, `schema.py:557`), so the second master and the chaplain
  are posts as written. B7 checks that the two posts the frigate's file lacks draw at muster as the
  others do (the wardroom, `tests/test_wardroom.py:42-57`'s check on her people file), or files them
  as drawn people if not, and says so.
- **Widows' men** (fictitious names, Bel §4.3) are counted as men, so the file's 590 is 4 over
  James's net 586. More hands may be signed on in the game (answer 10).
- **"Three times the frigate's":** the sources give 590 against the frigate's 264, 2.2 times
  (Bel §9). The brief's words are a figure of speech the sources do not bear; her notes say so.

### 6.2 The marines, 111 (answer 11)

- **Officers and NCOs:** the 1807 column's eleven (a captain, three lieutenants, three serjeants, two
  corporals, two drummers).
- **Privates: 100.** In March 1803 the *Mars* embarked "100 rank and file" and the *Spartiate* "a
  captain and 100 marines" (*Naval Chronicle* vol. IX p. 245, page image; Bel §4.4), within her
  dates. The *Bellona* carried 90 privates in 1761 (Lavery p. 17, Table 7); her share of 1761 at 590
  would give 101 in all (measured here). Answer 11's band is 100-110; 100 is taken, the dated
  figure at the foot of it.
- **Their kit** is the nation's (`data/nations.yaml`; Build §9.4).
- **Soldiers in their place** in 1794-95 (James vol. 1 p. 155 n. 1) and the 1803 shape are notes: a
  file carries one company. TNA's Trafalgar Ancestors stays the owner's leave, unused here: it
  changes no figure of a file of one company.

### 6.3 The quarter bill (set against the default fit, "arrogant class 1795")

| Key | Figure | Basis |
|---|---|---|
| Men at one side's guns | 378, of whom 16 at the four carronades (one forecastle, three poop) | Falconer and Douglas (§5.3) |
| `marines` (new: §12.1 item 1; written by her module after the generator's `b.quarter_bill(...)`, §12.1) | **95**: the 111 less the carronades' 16, kept in their division at the beat | Falconer, QUARTERS: the marines "generally quartered on the poop and forecastle, or gangway", at the great guns only in distant cannonading; *Bellerophon*'s marines on her poop on 1 June 1794 (the Molloy minutes, read (OCR); Bel §4.4) |
| `trimmers` | forecastle 10, fore top 13, main top 15, mizzen top 7, afterguard 10: **55** | what her seamen leave when one side's long guns and the wheel are manned, 419 − 362 − 2, split by the frigate's trimmer shares (8, 10, 12, 6, 8 of 44), as Indf §6.4 |
| `helm` | 2 | the frigate's (judgement) |
| `powder` | 0 | the idlers pass, the fourteen boys among them (Falconer's "often a boy to bring powder") |
| `filling` | 18 | §5.4 |
| `priority` | sail before guns | as every King's file |
| `small_arms` | 46 | the frigate's share of her seamen (20 of 182; judgement, as Indf §6.4). Falconer's 80 for a third rate of 70 and 100 for one of 80, and the Regulations' 100 seamen trained to muskets for a 74 (p. 142, page image), in the note |
| `boarders` | 105 | a quarter of the seamen (`BOARDERS_NOTE`) |

**At the beat** (`Quarters.beat`, `crew/quarters.py:155-242`) the trimmers and the helm are taken
first by the bill, then the gun crews forward first (`_gun_order`, :432), each from its preferred
stations (`_preferred_stations`, :437-460), which list the marines before the topmen. So on the 64
and the razee no marines' division forms (B1's `BEAT_MEASURED`, `indefatigable.py:2961`), and on her
the marines would go to the long guns while topmen stood idle. Under her bill's `marines` key (read
by B7.b, §6.4 item 1) the beat keeps that many marines for their division before the gun crews draw,
and the long guns' lists leave the marines out while the carronades keep them first. Then
(arithmetic here, measured at her build): the trimmers 55 and the helm 2 come first; the long guns'
362 are exactly the seamen left; the carronades take the other 16 marines; every crew fills, and the
division stands at 95. On the 1812 fit (28 at the carronades) the carronades take the 16 and twelve
seamen beside them, and the trimmers gain the seamen the long guns leave. On the 1793 fit the
division is the whole 111. **B7 measures the beat at muster on each fit**, before and after B7.b, and
records every crew filled, the marines at the guns and in their division, and the trimmers, as B1's
test does.

### 6.4 The bill by deck (answer 9): what is built, B7.b

The owner asked for "a deck key on each gun, with orders, divisions, stations and robbing by deck,
and two lieutenants on each gun deck". The key is stage 0's (`GUN_KEYS`, `schema.py:224-237`;
`Gun.deck`, `ship/parts.py`), read by nothing yet. Step B7.b makes it read, in two files, with the
least reach, each change keyed:

1. **The marines' division** (`crew/quarters.py`, `Quarters.beat`): §6.3, keyed on the bill's
   `marines` alone, which only her file carries.
2. **Divisions by deck** (`_beat_lines` :374 and `describe` :399): `GunCrew` gains `deck: str | None
   = None`, a plain default so an old pickle reads it, copied from its guns. On a ship whose
   broadside guns stand on both the `lower` and the `upper` deck (two gun decks), the beat adds one
   line a deck: "The lower deck: fourteen gun crews, 182 men." No line on a ship of one gun deck.
3. **Stations by deck:** unchanged. The forward, waist and after thirds of `_preferred_stations`
   already hold on each deck, and no period source quarters the parts of the ship by deck (Glascock
   1836 vol. II pp. 231-234 quarters them by part of the ship; Bel §4.5). **Plainly:** the owner's
   "stations by deck" is met by the thirds on each deck, and her notes say so.
4. **Robbing by deck** (`lend` :295, `_rob_order` :463): after the swivels and the chasers, first the
   lower-deck crews whose gun on the engaged side is shut (`Battery._shut`, `combat/guns.py:287`,
   SW-5's, read in `lend` from `ship.extra["battery"]` as the runner reads it,
   `evolutions/runner.py:1146-1148`), then the other decks' crews from the end that bears least,
   then the lower deck's from the end that bears least. The sort key gains a leading term that is
   constant on a ship with no `lower` deck, so its order there is as today. The reasons (judgement):
   a shut port's crew cannot fight, as the *Jupiter* and the *Blenheim* fought with their upper tiers
   (Bel §6.1); the lower deck's 32s are half her weight of metal and a deck further from the braces.
   The words name the deck: "from the lower deck, Nos. 4 to 10, their ports shut" (`_guns_words`,
   :347). Put to the owner (§17.1 item 5).
5. **Orders by deck** (`orders/gunnery.py`, `_guns_named` :592): "the lower deck", "the lower-deck
   guns", "the upper deck", "the main deck" (Cumby's "the main and lower decks", pp. 723-724), "the
   quarterdeck guns", "the forecastle guns", "the poop" and "the poop carronades" (to
   `roundhouse`), each with a side or without, name that deck's broadside guns. "The lower deck"
   and "the upper deck" are literal. "The gun deck" names the lowest deck that carries broadside
   guns: `lower` on a two-decker (*Dragon*'s plans title her lower deck so: Bel §3.4), `upper` on a
   ship of one gun deck (the razee's gun deck is `upper`, and a frigate's: Build §5.1; Indf §3.1).
   So "fire the starboard lower deck" fires them through the named-gun path (`_fire_words`, :545),
   and the director's and the world orders' slots that read `guns_named` (`world/orders.py:1825,
   2324`) take a deck. Words that named no gun before were
   refused; no test pins that refusal (grep over `tests/` for "upper deck", "lower deck", "main
   deck", "poop" at her window).
6. **Fire by divisions** (`combat/guns.py:842`) splits the guns at midships, which gives her lower
   deck seven and seven, Cumby's seven foremost exactly, and her upper deck six forward and eight
   aft (its eighth port stands 0.12 m abaft midships), the *Caesar*'s eight after guns. Left as it
   is; the officers' commands are in her people file (§6.5).

**What it reaches.** Every file names its decks once SW-2 lands (Build §5.3), so a rule keyed on any
deck word would reach the eight. Item 1 is keyed on her bill, item 2 on two gun decks, item 4 on a
`lower` deck, and item 5 adds words where there were none. The razee (one gun deck, `upper`) and the
eight move nothing but item 5's new words. **The 64**, a two-decker with a `lower` deck, gains the
deck lines and the robbing order. None of B1's tests pins either (`tests/test_indefatigable.py` pins
the beat's counts and 7-188's interval, neither of which robs), and her report shows both old beside
new. The two two-deckers then answer to one bill by deck, as the period's did. If the lead prefers
the 64 untouched, items 2 and 4 are keyed on her bill's `marines` key instead (§17.2 item 2).

**Not built:** "run in the lower deck" (a deck kept run in behind shut ports: Douglas arts. 150-152)
reaches `combat/guns.py`, B8's after stage 0. It is booked for the gunnery's later package.

### 6.5 The officers by deck

After the *Caesar* of 1794 (the Molloy minutes, read (OCR)) and Cumby's *Bellerophon* (Bel §4.5;
answer 9): the captain, the first lieutenant, the master and the captain of marines on the
quarterdeck; the second lieutenant with the upper deck's after guns and the fourth with its
foremost; the third lieutenant commanding the lower deck with its after guns, and the fifth, the
junior, "who commanded the seven foremost guns on each side of the lower deck" (Cumby p. 721); the
forecastle under the boatswain or a master's mate (judgement: a 74 of five lieutenants has none to
spare, Bel §4.5); the lieutenants of marines, a signal midshipman and the captain's clerk on the
poop. They are written in her people file's briefs, as the 64's are (`data/people/sixty-four.yaml`:
"the lower deck's twenty-four-pounders at quarters"). No engine reads an officer at the guns
(`Quarters.beat` leaves the quarterdeck's people out, :162), so no key.

### 6.6 The rear-admiral's flag (answer 10)

James adds "the customary supernumeraries" to a flagship's crew, "15 for every one of the four
rear-admirals" (vol. 1 p. 156, OCR l. 12961-12963), so *Bellerophon* bore 609 under Pasley's flag on
1 June 1794 (Bel §4.3). A fit changes only the guns and their stores (`FIT_KEYS`, `schema.py:242`),
and a file holds one company, so the flag is neither a fit nor a file key: a flag flies in a
scenario's year, not in a ship's build. **Taken:** a scenario that hoists a flag in her lists the
rear-admiral, and those of their retinue the story needs, in its existing `people:`
(`world/scenarios.py:55, 402-407`: "people beyond the muster's posts"); where she leads a squadron,
her role is `commodore` (her description's `roles`, SW-4's form, §8.1). Her file and her muster are
untouched; her note records James's rule. **Plainly:** the decision sheet's summary says "as a fit";
answer 10 left fit or role to the design within the schema, and neither holds men. The other way,
15 men added to her muster when a flag is hoisted, needs a crew key in stage 0c and world code to
read it. Put to the owner (§17.1 item 4).

### 6.7 The tack at quarters (answer 17): reasoned

**Today.** At quarters under "sail before guns", an all-hands manoeuvre takes half of every gun crew
(`TOLD_OFF_SHARE`, `crew/quarters.py:70`; `_rob_the_guns`, `evolutions/runner.py:1131-1170`), even when
the trimmers suffice: "if got.outcome == hands.ENOUGH and not want.all_hands: return got" (:1145).
The research's tack lent 189 hands and took 1.21 times the cleared tack at 292.5° (Bel §7.4).

**The period.** The sail trimmers are named in the station bill and leave the guns when called
(Douglas 1829 art. 120; Luce 1884 ch. XX). In the *Caesar* the small-arms men on the poop hauled the
braces, and some were later broken off to the guns (Molloy, read (OCR)). Douglas has the disengaged
side's lower-deck guns secured and their crews crossing (arts. 150-152). Marines were not to be
obliged to go aloft (the Regulations p. 422, read (OCR)), but hauled on deck. Nothing has half of
every crew leave its gun for a tack when hands enough stand elsewhere. The owner's lean agrees.

**The rule.** An all-hands manoeuvre at quarters is worked first by the trimmers and, for the work on
deck, the marines' division (never aloft), and takes from the guns, by the robbing order of §6.4,
only what its party wants beyond them. The party is the hands the same manoeuvre takes at sea in one
watch (judgement: the engine's own measure of "enough"). Under "guns before sail" nothing is lent,
as now. One condition in `_rob_the_guns` and a party for an all-hands request at quarters.

**Why it is a step of its own.** It changes every ship's tack at quarters, and truth 7-136 ("a tack
with the guns served is slower by exactly the hands it takes") with it. A key on her bill alone
would make one ship follow a practice that was every ship's. So it is **B7.c**, after her file and
her truths, only on the lead's word, its own commit, with 7-136 and the frigate's and the 64's tacks
at quarters old beside new and the move bisected to it; else it goes to the gunnery's later package
(§17.2 item 4). Meanwhile B7 records her own tack at quarters (cleared, sail before guns, guns before
sail) from 290°, 292.5° and 295° in truth 7-136's world, beside the scratch's (Bel §7.4).

### 6.8 The people file (B7's, hand-written data)

`data/people/seventy-four.yaml` in `sixty-four.yaml`'s form: the sixteen posts in order; the drawn
roles (the column's three master's mates; a midshipman as the captain's messenger; the captain, a
lieutenant and a serjeant of marines, `{station: marines, rating: marine}`); the harness's stations
bound by role as the 64's (the second and third lieutenants keep the watches). The outlines name no
one: the file serves 1786 to 1815, and a scenario names Hope, Pasley, Darby, Cooke, Loring, Cumby or
Maitland by `people:`. The briefs carry §6.5. Her test runs `tests/test_wardroom.py:42-57`'s check on
it.

---

## 7. Ground tackle, boats, pumps, hold and stores

**Ground tackle** (answer 13), written through `b.ground_tackle(note, anchors, chain=False)`, never
`ground_tackle_for`, whose rule gives a 74 two bowers and overstates them by 14-20% (Bel §5.7):

| Id | Kind | Weight | Cable | Source |
|---|---|---|---|---|
| `best_bower` | bower | 67 cwt (3,404 kg) | three cables of 22 in | Steel 1794 vol. I, the "Smaller 74 Guns" column (page image, Bel §5.7); Lavery p. 15, Table 4, about 1800 |
| `small_bower` | bower | 67 cwt | two cables | the same |
| `sheet` | sheet | 67 cwt | one | the same |
| `spare_anchor` | sheet | 67 cwt | one | the same; Steel's shank painters for four (vol. II p. 39); kind `sheet` as the 64's |
| `stream` | stream | 16 cwt (813 kg) | 13½ in | Table 4; Steel's 12½ in in the note |
| `kedge` | kedge | 8 cwt (406 kg) | a hawser of 11 in | half the bower cable, the house rule (judgement) |

Seven bower cables of 22 in and **100 fathoms** (Table 4, after NMM SPB 15), laid three, two, one and
one as Lever's Channel service (Lever 1808 p. 67, as the generator cites it); rated by `rope_kn`.
**Plainly:** the 64 took Falconer's 120 fathoms a cable; her class's own list gives 100, and it is
taken. Steel 1805's 71 cwt for all 74s goes in the note (one file, one ground tackle: Bel §13.5), with
the viols and the messenger, which the schema has no key for. Appended to `period.STEEL_ANCHORS` as the
74's row with both sources.

**Boats** (Lavery p. 16, Table 5, about 1800): a launch of 31 ft, pinnaces of 32 and 28 ft, two cutters
of 25 ft and one of 18 ft. Each line is written from its sourced length by the generator's own factors
(breadth, oars, weight), since `boat_entries` (`:3478`) takes Luce's lengths. The larger pinnace does
the barge's work (judgement, Bel §13.4).

**The rest:**
- **Pumps:** chain pumps either side of the main mast (*Dragon*'s gun deck, 1361F, read: Bel §3.4),
  two until task 9 counts them, and two hand pumps (judgement, as the 64's): `pump_entries(2, 2, ...)`.
  The well round the main mast (ZAZ1360, read).
- **Hold:** `hold_for(b, 1604, True, ...)` on the design's burthen (ZAZ1070's contract column).
- **Stores** (judgement, the 64's method): water at the frigate's 100 t for 264, carried to 590,
  223 t; provisions 120 days; cordage by the 64's method; shot plugs one a gun of the default fit
  (82). Steel's 80 "as fitted for sea with six months' provision" carried 620 tons of provisions and
  water for 700 men (pp. 197-198, read (OCR)), about 523 tons for 590: the period's check, in the
  note. The spare spars and the sail room by the frigate's method on her own spars and sails, the
  driver's spare among them (Ext §17.2); `ration_entries("a King's ship")`.

---

## 8. Far description, vessel type and size rank

### 8.1 Her description

| Key | rig | what | note |
|---|---|---|---|
| `seventy-four` | "a ship" | "a seventy-four, a ship of the line, fourteen ports a tier" | a third rate (Falconer, RATES); James's small class of 74s, under 1,700 tons (vol. 1 p. 451 note M*, read (OCR)); what the glass makes out, her two tiers of fourteen (Bel §3.3) |

Written in her file's `ship.descriptions` by `b.descriptions(...)`, with SW-4's `roles` (`kings-ship`,
`commodore`, as the frigate's: Build §8.2) and no `fit`, her default serving. `size_of_words` reads
the head, "a seventy-four": rank 4 (laid by stage 0). The 64's "a sixty-four, a ship of the line of
two tiers of ports" stays hers; the two differ in what the glass counts.

### 8.2 Her rows and words in `freesail/world/ships.py` (in her window)

- `DESCRIPTIONS["seventy-four"]` (`world/ships.py:165-220`): her file, rig and what.
- `_DESCRIPTION_WORDS` (`:221-266`): "a seventy-four", "seventy-four", "a 74", "a seventy-four gun
  ship", "a ship of the line", "ship of the line", "a line-of-battle ship", "line-of-battle ship",
  "a line of battle ship" → `seventy-four`.
- **Not taken:** "a two-decker", "two-decker" and "a third rate", which name the 64 as well
  (judgement). The size word "two-decker" stays stage 0's, at rank 4.
- **Laid by stage 0** (read): `SIZE_RANK["seventy-four"] = 4` and `_SIZE_WORDS`'s "seventy-four",
  "ship of the line", "two-decker" at 4 after "razee" and "sixty-four" (`world/captains.py:302,
  312-314`); the man-of-war sets (`world/regimes.py:161`; `world/squadrons.py:473, 1529`);
  `role_of_vessel` giving `kings-ship` (`world/brains.py:175`).

**The three assertions** (Build §16.1), each moved old beside new, its intent kept (words that name
no file are refused, now by a ship the game still lacks):

| Where | Old | New |
|---|---|---|
| `tests/test_ships.py:99` | `description_key("a ship of the line") is None` | `== "seventy-four"`, and the refusal kept as `description_key("a first rate") is None` |
| `tests/test_ships.py:188` | `put(w, "ship of the line", ...)` raises "no description" | `put(w, "first rate", ...)` raises it |
| `tests/test_world_orders.py:98` | `'ship: a ship of the line "Victory" of Britain ...'` refused, "no description" | `'ship: a first rate "Victory" of Britain ...'`, the *Victory* being one |

"A first rate" names no description: `description_key`'s tail search reaches "rate", which is in no
row or word list (read). If a later package adds a first rate, these three move again.

### 8.3 King's frigates and a ship of the line (Build §13.2; Bel §7.2)

- **Today:** `kings-ship.yaml` and `commodore.yaml` set `stranger_hostile_nm` to 0 ("a King's ship
  hauls off from nobody", `kings-ship.yaml:77`), so a King's frigate, British or French, runs down to
  engage a 74; only the cruiser and the trading roles keep away from a bigger class (`_overmatched`,
  `world/captains.py:1857-1873`). The privateer cutter *Renard* evaded the scratch 74 (observed, Bel
  §7.2).
- **The period:** Maitland "scarcely considered three frigates a match for one line-of-battle ship"
  (p. 78, read (OCR)); a 74 lacking stability "may be as easily taken by a thirty-eight-gun frigate"
  (Steel 1805 p. 124, page image), the exception the period names. Pellew's *Indefatigable* and the
  *Amazon* engaged the *Droits de l'Homme* in a gale that kept her lower ports shut (James vol. 2
  pp. 12-19): two frigates, a lee shore and a sea.
- **The rule offered (B7.e, if the owner takes it):** a lone King's ship of rank 3 or less hauls off
  from an enemy of rank 4 made out within two leagues. A knob `line_of_battle_nm` (6 nm, judgement on
  Maitland) in `kings-ship.yaml` and `commodore.yaml`, read by `_overmatched` for that case alone,
  with `overmatched` transitions in the King's ship's book as in the cruiser's. A ship in a set (72's
  squadrons) is left to her commander's book, unchanged. It applies to the 64 as well, a rank-4 ship.
  The *Droits*' case, a sea that shuts a 74's lower tier, is a later refinement.
- **Its reach:** no existing scenario or test puts a frigate against a rank-4 ship, so no pin moves;
  the 64's scenario tests (Indf §11; B6's) are re-run. The files: `world/captains.py` (B7's in her
  window if her design takes the rule: Build §4.1, §4.2) and the two doctrine books, which have no
  listed owner (§17.2 item 10).
- **Either way:** her tests pin that a cruiser frigate keeps away from her (the cruiser's book as it
  stands). Without the rule they record that a King's frigate engages her, and her scenario's French
  frigates are kept in the road by B6's intent, not by doctrine. Put to the owner (§17.1 item 3).

---

## 9. The polar: what B7 measures and records

**Observed here** (`final/probe_polar.py`, the research's scratch 74, the frigate's rig on her
particulars, Bel §7.4, rebuilt at this head without its armament, §18 item 1):

| | Best at 8 / 15 / 25 kn | `closest_deg` | `beat_deg(15)` |
|---|---|---|---|
| The scratch 74 at WL1 (6.20 m, 2,521 t, 318 m²) | 4.48 / 7.83 / 10.99 | 50 | 60 |
| The scratch 74 at the Channel line (6.46 m, 2,620 t, 330 m²) | 4.44 / 7.77 / 10.93 | 50 | 60 |
| The frigate-36 | 4.62 / 8.19 / 11.63 | 50 | 60 |
| The 64 (the clone's tree, 2026-10-29) | 4.25 / 7.59 / 10.92 | 50 | 60 |
| The razee (the same) | 4.41 / 7.93 / 11.54 | 50 | 60 |

At the Channel line the scratch makes 9.22 kn at 70° and 6.67 kn at 60° in 25 kn (static).

**B7 measures** `polar_of` on her file (`world/ships.py:471`): the speeds at 8, 15 and 25 kn from 40°
to 180°; `closest_deg`; `beat_deg(15)`; and the sailed figure at 90° in 15 kn (speed, heel, helm).
She is tested in `tests/test_ships.py:74-93`'s form in her own file, with her own measured beam
reach, ±0.5.

**Targets, bands on the sources** (each judgement on the words):
- her best in 25 kn about 11 kn, within 10.5-12: the owner's first goal (answer 14); the *Bellona*
  made 11-12 kn from a point or two abaft the beam to the bowline as wind and sea allowed (1763), and
  10-12 before the wind (1783) (Lavery p. 9, Table 2);
- below the frigate-36's best in 25 kn (answer 14);
- 7-8.5 kn at 90-100° in 15 kn (Bel E1);
- *Vanguard*'s 4¾-5½ kn a point abaft the beam in a moderate breeze under courses, topsails and the
  driver (NRS vol. 2 p. 53, Bel S7): a sailed check with her driver bent (Ext §17.7), ±1 kn;
- under reefed topsails 6-9 kn (Bel §13.2);
- `closest_deg` within a step of the frigate's while her brace limits are the frigate's (§4.3).

**The close-hauled gap** (Build §13.2). The reports give 9 kn, often 10, close-hauled in a topgallant
gale and smooth water, and 8-8½ in a topsail gale; the scratch made 4.6 kn at 66° in 15 kn and 7.6 kn
in 24 kn (Bel §7.4). The words "close-hauled" and "topgallant gale" are wide, and a captain's figure
is their ship's best. The frigate's file may share the gap (Bel §13.2). **Compared and recorded, not
forced:** no knob of hers closes it without moving the physics' equations, which the brief forbids.
The owner's answer for the razee against the frigate (2026-10-29: "We'll rely on tuning ...", neither
presumed the one at fault) is taken for her the same way, and the gap goes to the lead (§17.2
item 12).

**The knobs, in this order:** `hull_speed_kn` within 11.5-13.0 (13.0 adds 0.14-0.27 kn: Bel §7.4);
`clr_x_m` for the helm (truths 6 and 17; the *Bellona* steered easily, wore and stayed quickly and
was weatherly: Lavery p. 9), tuned with the spritsails and the driver set and unset, each recorded;
the brace limits only with a source and the owner's word. Each tuned figure is recorded beside its
start. Realism, not pacing.

**Her handling, in her tests** (not a truth): her classing as the 64's at stage B (Ext §10.3 item 4's
form); the mizen yard never braced; the course hauled aft at helm's a-lee and brailed hove to; the
spritsails clewed up hove to; she lies to within truth 12's band, as the *Bellona* lay to best under
the mainsail and mizen staysail (Table 2); the driver's shift and back and its paths (Ext §17.7's cases
on her file).

---

## 10. The lee ports: what her file supplies

- Per broadside gun, its port's sill as `height_m` (to the centimetre, equal to its triple) and its
  `deck`; per port, in the profile, the side's half-breadth at the sill (§3.3, §3.4).
- SW-5 reads them (`ports.update`; `half_breadth_at_sill(profile, deck, x)`; Build §7): the dip is
  the heel plus the roll's amplitude; a port shuts when its sill lowered stands within `PORT_SHUT_M`
  of the water, and reopens six inches clear of that (`PORT_REOPEN_M`, 0.15 m). Her roll is her own,
  `Firer.roll_deg` from `world.motion` (Build §7.1).
- **Her shut heels:** the lowest lower-deck port at 10.35° heel alone (10.58° on the moulded 22.7 ft);
  the end ports 13.7-14.7° on the midship figure, later once task 4 measures them; the upper deck about
  30-31°; each a roll's amplitude sooner (answer 7). Once shut, the lowest reopens below 9.1°.
- **In ordinary sailing** (answer 8, the baseline accepted): close-hauled under plain sail the
  scratch 74's midship lee port shut at 28-30 kn of wind on the drawn line's 11.3° (Bel §7.4); on
  her file's 10.35° it would shut at about 27-28½ kn (interpolated here on Bel §7.4's heels), and in
  the gusts at 24 kn. B7 re-measures it on her file and records it (§14.3).
- **The period's own cases** are swell and rolling, not steady heel (*Blenheim*, *Monarch*, the
  *Droits de l'Homme*: Bel §6.1). L3's roll brings them within the rule's reach. A crewed ship's roll
  stays nought until 84 gives each hull her sea (Build §7.1), so a truth on the roll uses the player's
  ship.

---

## 11. Where she sails

- **Her scenario is B6's** (Build §12): Basque Roads, 13-15 July 1815 (answer 15; Bel §8.3 (a); Maitland
  1826, read (OCR)), biscay-north, on her one file with her late fit, "as the bellona 1812". **Plainly:**
  she carries the lateen mizen yard of the one rig where Chalon's 1815 painting shows a gaff (Bel
  §5.4); the owner accepts it (Bel §13.5).
- **What B6 needs from her:** the description `seventy-four`, her file, her fits and default, her date
  range (1786-1815), her people file. **What the scenario needs beyond her** (B6's design): the French
  frigates *Méduse* and *Saale* as the frigate-36 under French colours, with an intent that keeps the
  road (a King's frigate engages anything today, §8.3); the brig as the *Épervier*; her at anchor ready
  to slip (Maitland pp. 39-40); the wind "blowing right in" on the 15th. A command-line ship lacking
  the scenario's fit takes her default (D48's third way, the lead's ruling).
- **Built with her file:** a test that she sails under rules captains at seed 7 in a world with no
  named fit (`make_world(7, "data/ships/seventy-four.yaml", Scenario())`) and round-trips.
- **Elsewhere:** a far 74 in any scenario by "a seventy-four" or "a ship of the line", a King's ship by
  doctrine. Off Brest 1804-05 and Cornwallis's Retreat stay later options (Bel §8.3 (b), (c)). D25 (d),
  the *Droits de l'Homme*, waits for the *Téméraire*-class 74: her file under French colours would be
  wrong in guns, people, mizen and the low tier itself (Bel §8.4).

---

## 12. Interfaces

### 12.1 Her stage 0c, exactly

Laid by the stage-0 agent at the opening of her window, after the fresh merge and after B3's merges,
checked as Build §3.4 by an agent that did not write it. Build §3.3's table names what her stage 0
*may* add (the bill-by-deck keys, any `DECK_WORDS` word, the flag's place); her design needs one key,
and a second only on the lead's word:

| # | What | Where | Inert because |
|---|---|---|---|
| 1 | `"marines"` appended to `QUARTER_BILL_KEYS`; `QuarterBillSpec.marines: int \| None = None`, a plain default; read as a whole number; refused in words below nought or above the file's marines (`stations["marines"]`); a `QuarterBillSpec.__getstate__` leaving it out while None | `freesail/ship/schema.py` (`QUARTER_BILL_KEYS` :256, `QuarterBillSpec` :612 at 8f30be9) | no file carries it until her step 4; nothing reads it until B7.b; every pickle of the eight, the 64 and the razee byte-identical |
| 2 | **Only if the lead takes B7.d (§5.2):** `"numbering"` appended to `ARMAMENT_KEYS`; `ArmamentSpec.numbering: str \| None = None` ("by deck"), left out of the pickle while None; under "by deck", every broadside gun of every fit names a deck and `(deck, number, side)` is unique, the refusal naming the deck; else `(number, side)` as now; `Gun.by_deck: bool = False`, a plain class default, left out of `Gun.__getstate__` while false, set by nothing | `schema.py` (`ARMAMENT_KEYS` :251, `ArmamentSpec` :711, validate :2104-2110); `freesail/ship/parts.py` (`Gun`, :548-), which is B3's after 0E (Build §4.2), so this one class default is laid after B3's merge, on the lead's allotment, checked as Build §3.4 | no file carries the key; the eight keep `(number, side)` whatever decks they name after SW-2 |
| 3 | No deck word | — | her poop is `roundhouse`, as the 64's (§3.5) |
| 4 | Nothing for the flag | — | the scenario's existing `people:` (§6.6) |

**Who writes the keys into her file.** `Builder.quarter_bill` (`gen_ships.py:876-916` at 8f30be9)
builds its mapping from its own parameters and takes no `marines`, and B7 never edits the
generator (Build §4.1). So her module sets `b.doc["crew"]["quarter_bill"]["marines"] = 95` and its
note `b.crew_notes[("quarter_bill", "marines")]` after its call to `b.quarter_bill(...)`, as B1's
module reassigns the filling's note after the same call (`indefatigable.py`, `quarter_bill`, :3034
at 8f30be9; Indf §5.2's reassign-after-the-call pattern). The key lands last in the bill, where
stage 0c appends it to `QUARTER_BILL_KEYS`, and the dump writes its note as it writes the bill's
other keys' (the crew block's four-space keys, `gen_ships.py:1151-1153`). Under B7.d the same:
`b.doc["armament"]["numbering"] = "by deck"` after `b.armament(...)`, its words in the section's
note. The generator stays untouched.

**The checks:** the two-way byte test; the golden classing table; the fast tier; every kept save
loads; every pickle of the eight, the 64 and the razee byte-identical to the head before; a diff
read for any reach beyond the list. **Plainly:** if the owner chooses the flag on her muster (§17.1
item 4), stage 0c also lays one optional crew key, inert and left out of the pickle while empty.

### 12.2 What she takes from others (the contracts she assumes)

| Provider | What |
|---|---|
| Stage 0 | the hook and alias; `period.py`; `g.broadside_pair(..., deck=, round_to=)`, `g.exercise_allowance(n, decks=2)`, `g.hull_profile`; `DECK_WORDS`; the registries; `Sail.curve_class`; `ports.update`'s hook |
| Stage 0E, the driver's stage 0, B3.1, B3.2, B3.5 | `cut_at_mast`, `lateen_yard` out of the braced yards, `under_bowsprit`, the driver's boom on a lateen cut at the mast and its rivalry with the storm mizzen; the behaviour on the keys (Ext §3, §4, §17) |
| B1 at stage B | `mizen_yard.py` (the course and `driver()`) and `spritsail_yards.py`, pure, asserting their geometry (Ext §9.3, §17.2) |
| Stage 0H, SW-2b.1 | the shape keys and their refusals; `form.py`; `g.hull_form(hull, notes, *, form, marks, measured=())` |
| SW-1 | `charge_lb` reading Table No. 29 for every calibre of hers |
| SW-4 | a description's `fit` and `roles` written in her file and read |
| SW-5 (L2, L3) | `ports.update` by Build §7.1's rule; `Battery._shut`, the shut port guns' ids; the roll's read path |
| B5 | her hull drawn from her profile and shape (B5.1, B5.6); her mizen yard, spritsails and driver (B5.2, B5.3, B5.5); the owner's sheets and her pictures |
| B6 | the scenario; D48's third way |
| The lead | the merges; the whole suite in the cloud; the pace on the build machine; the allotments of §12.3 |

### 12.3 What her work reaches beyond her module (for the lead's allotment)

| File | Change | Owner today | Keyed on | Step |
|---|---|---|---|---|
| `freesail/crew/quarters.py` | the `marines` key at the beat; `GunCrew.deck`; the deck lines; robbing by deck; the deck in the words | B7's (Build §4.1) | her bill's `marines`; two gun decks; a `lower` deck | B7.b |
| `freesail/orders/gunnery.py` | the deck words in `_guns_named` | no owner after stage 0; named here (Build §4.1: "the orders her design names") | deck words, newly accepted | B7.b |
| `freesail/evolutions/runner.py` | the tack's rule at quarters | B3 | every ship | B7.c, only on the lead's word |
| `freesail/ship/graph.py` | `Gun.by_deck` set from the armament's `numbering` | B3 | the numbering key | B7.d, only on the lead's word |
| `freesail/ship/parts.py` | `pair_key` and `name` by deck | B3 | `by_deck` | B7.d |
| `freesail/crew/quarters.py` | the parse sites taught `gun:<deck>:<n>` | B7's | `by_deck`'s key form | B7.d |
| `freesail/orders/gunnery.py` | a number with its deck; a bare number refused on a ship numbered by deck | as above | `by_deck` | B7.d |
| `tools/ships/indefatigable.py` | the 64 and the razee renumbered by deck | B1 (window closed) | — | B7.d, with the lead's word on the 64 |
| `freesail/world/captains.py`; `data/captains/kings-ship.yaml`, `commodore.yaml` | the rank-4 rule | B7 if taken (Build §4.1); the two books have no listed owner | rank 4 met by a lone rank 3 or less | B7.e, if the owner takes it |
| `tools/ships/mizen_yard.py` | an extension for the driver's jaws, only if her poop needs one | B1, then B7 in her window (Build §4.2) | her call only | step 2 |

`freesail/combat/guns.py` is not taken (§6.4, "not built").

### 12.4 What she gives

- **To B5 and B8:** a profile in Build §5.1's form with her shape keys and marks; every port gun on a
  triple of its deck to the centimetre, its deck named; every height above her water; the mast ids
  `fore.`, `main.`, `mizzen.`.
- **To B6:** her description key and file, her three fits and default, her date range, her people file.
- **To B5, for the owner's sheets and her testing report:** her five views (§13.1).
- **To the integrator:** her truths drafted in `tests/test_bellerophon.py` under 7-194 to 7-196, written
  against the names the Hull keeps (`world.ship`, `world.motion`, `world.sea`, `world.clock`), never
  `isinstance(..., CrewedWorld)`; her tuning notes as text in her branch's report.

### 12.5 Each engine change checked to change nothing it should not

| Change | Check |
|---|---|
| B7.b, the `marines` key at the beat | the eight's, the 64's and the razee's beats byte for byte at seed 7 (a test over every file without the key) |
| B7.b, the deck lines | every one-gun-deck file's beat lines byte for byte at seed 7; the 64's old beside new |
| B7.b, robbing by deck | the order unchanged on every ship without a `lower` deck (a test over the eight and the razee); the 64's old beside new |
| B7.b, the deck words | every phrase `guns_named` answered before answers the same (the tests' own phrases, re-run); "fire the gun deck" names the razee's and the frigate-36's `upper` guns and her `lower` guns |
| `GunCrew.deck` | an old `Quarters` pickled without it loads (the kept saves, the fast tier) |
| B7.c | truth 7-136 and the tacks at quarters old beside new, bisected to the one commit |
| B7.d | every pair key, gun name and order of the eight unchanged (no file carries the key); the 64's and the razee's old beside new |
| B7.e | no pinned scenario puts a frigate against rank 4 (grep); the 64's scenario tests re-run |

---

## 13. File ownership, and the road

**B7 owns** (Build §4.1): `tools/ships/bellerophon.py`; `data/ships/seventy-four.yaml` (generated);
`data/people/seventy-four.yaml`; `tests/test_bellerophon.py`; `tools/pace.py` (her mode); in her
window, her rows in `freesail/world/ships.py`, the three assertions (`tests/test_ships.py:99`, `:188`;
`tests/test_world_orders.py:98`), appends to `tools/ships/period.py`, and `freesail/crew/quarters.py`.
**Named here for the lead:** `freesail/orders/gunnery.py` (no owner after stage 0); and, only as
§12.3 allots them, `freesail/evolutions/runner.py` (B7.c), `ship/graph.py`, `ship/parts.py` and
`tools/ships/indefatigable.py` (B7.d), `world/captains.py` and the two doctrine books (B7.e),
`tools/ships/mizen_yard.py` (the driver's jaws).

**B7 never touches:** `tools/gen_ships.py`; `freesail/ship/schema.py` (stage 0c's); the eight existing
files; the 64's and the razee's files and module but as B7.d on the lead's word; `freesail/physics/`,
`freesail/combat/`, `client/`; anything under `docs/agents/consent/`.

**Each step ends** with `py tools/gen_ships.py <scratch>` from the tree root, a `cmp` of every committed
file against the scratch, and `load_ship` on hers. The fast tier once at the end, with the slow tier of
the files touched (Build §2.5); one suite at a time on the owner's machine.

| Step | What | Proves | Waits on |
|---|---|---|---|
| 0 | The fresh merge of the lead's head; stage 0c (§12.1) and its checks | nothing changes (bytes, pickles, the fast tier) | B4's merge; §0's pieces; the lead's word on B7.d for item 2 |
| 1 | The measuring tasks (§3.7), scratch scripts outside the repository | the profile's open points, the ports' half-breadths, the poop, the braces' geometry | 0 |
| 2 | Her data and `write()`: the hull, the profile and shape keys with marks, the masts, the yards, the square sails, the head with the spritsail yards, the mizen yard and course, the driver and its boom (the jaws by task 5); groups | her file loads, rates and polars; §1.5's checks; her measured triples within 0.05 m of the drawn side | 1 |
| 3 | Staysails, studding sails, storm and occasional canvas, aliases | every group the engine reads by name exists; the driver's shift and back on her file | 2 |
| 4 | Fits, magazine, company, people file, quarter bill (with `marines`), stores, sail room, ground tackle, boats, pumps, hold; her description rows and words; the three assertions | §1.5's checks; the beat measured at muster on each fit; the three moved, old beside new | 2-3 |
| 5 | Her tests; 7-194; her polar measured, tuned within bands, recorded; her tack at quarters recorded | §14 | 4 |
| 6 | B7.b (§6.4) with its tests and §12.5's checks; the beat re-measured; 7-195 once L3 is in; 7-196 and `tools/pace.py`'s mode | §14; nothing of a one-gun-deck file moves; the 64's old beside new | 5; SW-5 L3 |
| 7 | **Only on the word given:** B7.c (the tack), B7.d (numbering by deck, both two-deckers), B7.e (the rank-4 rule), each its own commit, bisected | §12.5 | 6; the lead (and the owner for B7.e) |
| 8 | The lead's head brought in; her report; **the owner's testing report** (§13.1) | — | 6 (7 if taken); B5.6's drawing of her file |

### 13.1 The owner's testing report (the direction of 2026-10-29)

In place of the owner's own test, a few pages, the basics and the important views:
- **Her particulars against their sources**, in one table: the hull, the sills, the spars, the fits
  and broadsides, the company and the marines, the ground tackle and the boats, each with its source
  and mark.
- **Pictures** from B5's sheets, at one scale and normalised, beside the 64 and the frigate-36, each
  with its rung letters:
  - five views: abeam, ahead, astern, on the quarter at 135°, and heeled 10° from windward;
  - furled, and under plain sail;
  - her mizen course set, the driver shifted in, the spritsails set;
  - heeled 11° to leeward, past her 10.35°, from ahead and abeam: her lower wale and sheer at the
    water, with B5's port bands if the owner keeps them, and beside the picture the figures (each
    lower sill's height at that heel, the ports the rule shuts, the guns' counts) and the log's
    line "The lee lower-deck ports are shut". Package 75 draws no port and no gun; 81 will draw
    the ports;
  - the page's panel at the built-in 800 × 600 window, as a player sees her.
- **Figures:** her polar beside the frigate's, the 64's and the razee's, and against the *Bellona*'s
  reports; her shut heels and the wind at which she shuts her lee lower ports close-hauled; the beat at
  muster on each fit (the marines' division, the trimmers); her tack at quarters, and B7.c's old beside
  new if taken; her pace crewed and alone; her broadsides.
- **What a player would notice:** a deck named in an order ("fire the starboard lower deck"); her lee
  lower ports shut in a near-gale and her eighteen-pounders still firing; the hands for a brace taken
  from the idle lower deck; her driver shifted for the mizen course.
- **What was taken another way:** each "Plainly" of this document, one line each, and what the owner
  is asked (§17.1).

---

## 14. Tests and truths

### 14.1 Her tests (`tests/test_bellerophon.py`)

Band form, the source in a comment, as `tests/test_ship_particulars.py:93-104`: her hull, profile and
sills against the measured lines; her shape keys' marks, and her measured triples within 0.05 m of the
drawn side; her spars against Table 10 and Steel; her sails against table IV (±10%) and Table 15; her
guns, fits, crews, exercise and filling; her company, posts and marines against the 590 column and her
people file (`tests/test_wardroom.py:42-57`'s check); her ground tackle and boats; her descriptions,
rank and words; her period names resolving (`test_period_names_resolve`'s form); her polar in
`tests/test_ships.py:74-93`'s form; her handling (§9); the beat at muster on each fit; B7.b's cases and
§12.5's checks; a far 74 met by a cruiser-role frigate, who keeps away, and by a King's frigate, who
engages unless B7.e is built (recorded as the engine's today); her checkpoint at quarters under
`test_checkpoint`'s 2 MB bound (the scratch's 1,220 KB raw, Bel §7.5); the round trip under rules
captains at seed 7 with no fit named.

**Her truths** (Build §15) are drafted here under their numbers and moved into
`tests/test_known_truths.py` in Phase 5 (Build §4.4). Each pins states, counts, ticks and bands, never a
digest; its docstring gives the scenario, the source, the figures measured at seed 7 and the machine.

### 14.2 Truth 7-194: her particulars hold their sources (pinned at once, step 5)

Her file loads, and:
- beam 14.25 ± 0.05 m (46 ft 9 in, ZAZ1357's table); waterline 51.2 ± 0.3 m (168 ft); draught 6.46 ±
  0.10 m to K;
- displacement within 2,490-2,900 t (Bel H1) and within 2,560-2,660 t (the measured lines at her
  line, either conversion: §2.1); GM 1.2-1.5 m;
- her lowest lower-deck sill 1.57 ± 0.01 m above her water (5 ft 2 in, Lavery p. 9), with the
  half-breadth at it 6.90-7.09 m (6.92 m moulded, 7.04 m with the plank);
- ports a side 14, 14, 7 and 2 (Bel H3); the lower ports 1.04 × 0.82 m;
- the main mast within 107 ft 4½ in-108 ft (Steel's rule; Lavery), the mizen yard 86 ft 6 in ± 1%;
- 28 long 32-pdrs of 55 cwt on the lower deck in every fit; 74, 82 and 78 pieces; broadsides by 70's
  rule 781 and 867 lb (James) and 938 lb;
- crews 13, 9, 7, 6 and 4 (Falconer; Douglas);
- complement 590 (the 1807 column), five lieutenants, marines 111 of whom eleven officers and NCOs;
  filling 18; exercise 9;
- four bowers of 67 cwt, a stream of 16, a kedge of 8, seven 22-in cables (Steel; Lavery p. 15); six
  boats (Lavery p. 16);
- `description_key("a ship of the line") == "seventy-four"`, rank 4.

### 14.3 Truth 7-195: her lower-deck ports shut at the heel the sources give (step 6, after L3)

In truth 7-190's form (B8's, at L3), with her file as the player's ship, no sea unless set:
- **The rule:** the lowest lee lower-deck port by `shot.lee_port_shut` on its triple (L7, at
  x −2.15 m, which carries the lower deck's pair No. 8 from forward; the truth finds the port by
  its triple, the least sill, never by number): open at 9.9° of heel and shut at 10.9°, heel
  alone; its threshold within 10.2-10.7° (10.35° the file's side with the plank; 10.58° the
  source's 5 ft 2 in on the moulded 22.7 ft, the brief's 10.6°).
- **The battery:** in a world heeled to a set angle, raised from upright (so the six-inch reopening
  margin does not bite), with her guns run out, `Battery._shut` holds her lee lower-deck guns in the
  counts the rule gives, at heels **at least 0.3° from every port's threshold**. B7 computes the
  thresholds of all the lower ports on the final file and picks the pinned heels between them; on the
  midship figure: none at 10.0°, nine at 12.35°, eleven at 13.2°, thirteen at 14.2°, all fourteen at
  15.2° (measured here). No upper-deck gun shut below 25°; the weather side open.
- **The reopening:** once shut at 10.9°, still shut at 9.9° on the way down, and open at 8.6° (it
  reopens below 9.1°, six inches clear).
- **A roll's amplitude sooner:** with a roll of 4° set on `world.motion`, the lowest lee port open at
  5.8° of heel and shut at 6.9°, raised from upright.
- **The log:** "The lee lower-deck ports are shut" once at the change.
- **In ordinary sailing** (answer 8): close-hauled under plain sail, no book, in a steady wind with no
  gusts, her lee lower ports open at 24 kn and shut at 32 kn. Pinned only if her tuned file holds each
  with a degree of heel's margin from her 10.35°; else that clause is recorded, not pinned. On Bel
  §7.4's heels the scratch stood 2.2° under 10.35° at 24 kn and 4.4° over it at 32 kn at 2,521 t, and
  3.1° and 2.9° at 2,821 t (measured here); Bel's 1.9° (P3) was against the drawn line's 11.29°.
  Answer 8's "or in gusts at 24 kn" is recorded beside it, measured with the gusts on.

**The knife-edges:** her L7 and L8 shut 0.08° apart (10.353° and 10.436° on the file's sills), L6
and L9 together at 10.68°, and between 11.35° and 11.85° no heel stands 0.3° clear of every
threshold; so no count is pinned near them. The frigate's lee ports open at her shut heel is
7-190's clause (Bel §6.1, P5), not hers. The docstring says plainly
that the period's own cases are swell and rolling, which the roll clause serves and steady heel does
not.

### 14.4 Truth 7-196: a 74 crewed holds the floors (routed as a pace test)

- **Crewed** (`test_truth_7_196_a_seventy_four_crewed_holds_the_crewed_floor`, marked
  `@pytest.mark.pace` by hand as truths 88 and 7-138 are, `tests/conftest.py:490-500`): truth 88's
  form (`tests/test_crews.py:187-211`) in a world where the 74s keep their places, since truth 88's
  own form empties the cap (Bel §7.5).
  - **Its place differs from truth 88's.** Truth 88's frigate lies at 49° 30' N 5° 30' W
    (`world_at(49.5, -5.5)`), about 30 miles from the Lizard (49.959° N 5.207° W,
    `data/charts/features/channel-west.yaml`; measured here): 74s keeping a station off the Lizard
    from there would sail for it and pass the 6-mile demotion within the 4,000 ticks.
  - **Her world:** the frigate put about three miles south of the Lizard (49° 54' N 5° 12.6' W to
    start; B7 settles the place by measurement), her plain sail set and, once it is set, hove to.
    Truth 88's "heave to" at its first tick is refused ("No sail is set on the mainsail to lay
    aback"), and its frigate sails on at 2-3 kn (observed here, as Bel §7.5 found). Three 74s of her
    file `put` 1-3 miles from her with "keep the station off the Lizard within 2 miles"; a thousand
    ticks to settle.
  - **Asserted** at the end of each timed thousand: `crewed_ids` at `CREWED_CAP`, and every 74
    within `CREWED_NM` (4 miles) of her; the best of three at least `CREWED_FLOOR_TICKS_S` (60;
    `world/crews.py:93`).
  - **Observed here** (`probe/heave_probe2.py`): hove to there once her sail is set, the frigate
    drifts north-westward about 2 miles in 4,000 ticks and stays 2.6-2.8 miles from the Lizard.
  - The docstring says why the place differs from truth 88's. Estimated 106-147 ticks a second on
    the build machine (Bel §7.5). Pinned at step 6.
- **Alone** (`test_truth_7_196_the_seventy_four_ticks_at_the_build_machines_floor`): truth 51's form
  with her file in the frigate's place, at least `BUILD_MACHINE_FLOOR` (500;
  `tests/test_known_truths.py:2162`). Estimated 500-620 on the build machine before her spritsails,
  lateen and driver add sail physics (Bel §7.5). Drafted beside the crewed clause; **pinned only if
  the lead's measurement at her merge leaves a tenth's margin (550 or more), else recorded and
  reported. No floor is lowered** (§17.2 item 5).
- **`tools/pace.py`** gains `py tools/pace.py seventy-four`: alone, and with three 74s crewed, printing
  ticks a second with the load. Measured on the owner's machine to record a figure only (Build §2.5).

**Not truths:** her polar (no pinned point until the close-hauled gap is compared); her tack at
quarters (recorded); her scenario's round trip and first hour (B6's tests).

---

## 15. Pins her work could move

- **None of the existing ships' passages.** Her module writes one new file; no shared function or table
  of the generator changes.
- **The three assertions,** named: `tests/test_ships.py:99`, `:188`; `tests/test_world_orders.py:98`
  (§8.2), old beside new.
- **B7.b:** the 64's beat lines (a deck line each) and her robbing order (the upper works before the
  lower deck), pinned by none of B1's tests, shown old beside new in her report; nothing of a
  one-gun-deck file but the deck words newly accepted ("fire the upper deck" or "fire the gun deck"
  on the frigate after SW-2); no test asserts their refusal (grep at her window).
- **B7.c, only on the lead's word:** truth 7-136 and every ship's tack at quarters, bisected to the one
  commit.
- **B7.d, only on the lead's word:** the 64's and the razee's bytes, gun ids and gun names, and any of
  B1's tests that name a gun by id; their truths pin counts, not names.
- **B7.e, only if the owner takes it:** no pinned scenario puts a frigate against rank 4; the 64's
  scenario tests re-run.
- **The registries:** new rows and words only; no existing scenario, business table or test names
  "seventy-four" (grep over `data/`, `freesail/`, `tests/`: only stage 0's rows and the people files'
  histories).
- **The caches** (`maxsize=32`): thirteen files after her, results unchanged.
- **The harbour's glob** lists her file; its test checks membership only.
- **The checkpoint:** her file adds no field; `GunCrew.deck` and the stage-0c fields are plain defaults
  left out of the pickle while empty.
- **Not hers:** the lee ports' combat pins (SW-5's); the far fight's length (package 74's).

---

## 16. Risks, ranked

1. **Her window opens last, on the longest chain.** B4's merge (after B3.3) and SW-5 L3 (after SW-2 and
   L2) must both be in. *Mitigation:* the owner's direction lifts the hold that kept SW-2 behind the
   owner's test; her file and 7-194 do not wait on SW-5 (step 6 alone does).
2. **The close-hauled gap** (§9), probably the frigate's too. *Mitigation:* compared and recorded; tuned
   only within bands; not forced; to the lead.
3. **The foot** (§2.2): her draught a foot under the report's, her displacement under the *Audacious*'s
   2,821 t. *Mitigation:* the sill, which the truth reads, is the report's to the hundredth of a foot;
   the draught's datum recorded as open; displacement moves only heel and inertia; put to the owner.
4. **The driver's boom over the poop** (§4.5, §4.6): the poop judged; the jaws raised about 5¼ ft
   above Steel's leech on I32's throat, the after leech then 0.10 m inside Steel's band. Under Steel's
   6 ft 6 in tack both of Ext §17.2's checks fail. *Mitigation:* the tack at I32's throat; task 5
   before the cut; the 10% check and the after leech's band re-measured; reported to the lead with
   the three ways if they fail (§17.2 item 13).
5. **Knife-edged thresholds** (§14.3). *Mitigation:* counts pinned only at heels 0.3° or more from every
   threshold, computed on the final file; heels raised from upright.
6. **Pace alone** at 500-620 against 500, lowered by her extra sail physics. *Mitigation:* the crewed
   clause pinned; the alone clause only with the lead's margin.
7. **B7.b's reach.** Every file names its decks after SW-2. *Mitigation:* each change keyed (her bill;
   two gun decks; a `lower` deck); §12.5's tests over every one-gun-deck file; the 64's old beside new.
8. **The bill at 590 with the marines kept:** the long guns' crews are exactly the seamen left (§6.3),
   so a sick list or casualties leave crews short at once. *Mitigation:* `marines_to_guns`
   (`quarters.py:137-153`) moves the division to the guns, the carronades first, as losses mount, as in
   the *Caesar* in 1794; measured.
9. **The long pole-head** (§4.2) rests on a reading of Steel's words, and departs from the 64's.
   *Mitigation:* the page image and the OCR held; put to the owner for both ships; either way her
   topgallants and royals fit their spars.
10. **The main mast** rests on reading a misprint (§4.1). *Mitigation:* three figures within 8 in.
11. **Unmeasured points** (the knuckle, the transom, the head, the poop, the top-timber line, the wales
    along the length, the ports' half-breadths at the ends, the forecastle's ports one reader's, the
    upper deck's seventh port tentative): each `judged` until §3.7's tasks are done. The midship figure
    shuts the end ports early, on the safe side.
12. **The deck lines' surface** (±0.35 ft) moves her datum and decks by up to 0.1 m, not her sills, which
    are measured directly. *Mitigation:* task 8.
13. **Duplication with B1's module;** a fix in one is not in the other. *Mitigation:* reported for a
    shared module (§18 item 11).
14. **A King's frigate engages her** unless B7.e is built. In her scenario the French frigates would
    sortie. *Mitigation:* B6's intent; the owner's answer.
15. **The 1815 rig:** the lateen yard where Chalon shows a gaff; accepted by the owner.
16. **Byte identity on the build machine** (Indf §16 item 4). *Mitigation:* rounding at the measured
    figures.
17. **"A first rate"** becomes a description in a later package: the three assertions move again.

---

## 17. Open for the owner or the lead

### 17.0 Answered by the owner (2026-10-29)

- **Where she floats:** "Agreed." As proposed: the line where her drawn lowest port stands the
  report's 5 ft 2 in clear.
- **Topgallants and royals by Steel p. 42's long pole-heads, for her and the 64:** "Agreed."
  For both ships: the 64's file is regenerated at B1's stage B, old beside new
  (Design-Ship-Indefatigable.md §17, lead item 8).
- **A frigate on her own keeps away from her:** "Agreed." The rank-4 rule as proposed (§8.3);
  its files go to the lead (lead item 10).
- **The rear-admiral's flag:** "The rear-admiral and his people should at least be in the ship
  file so that they may have models stationed as them." **This replaces the design's pick.**
  The flag party (the rear-admiral, their flag lieutenant and secretary, and their servants, by
  the period's establishment for a rear-admiral's retinue: to read) is written into her files
  with their stations (the quarterdeck and the admiral's cabin), inert until a scenario hoists
  the flag; while no flag flies they are not aboard and her 590 is unchanged. The key that
  carries them (in her people file or a `flag` block under her crew) is laid in her stage 0c,
  inert, left out of the pickle while empty; the world code that brings them aboard when the
  flag is hoisted is for the lead to place (lead item 15).
- **Robbing the guns by deck:** "Agreed." As proposed.
- **Lavery's drawings:** the owner sent photographs of section D, Decoration (2026-10-29):
  D1 the stern's decorations and D2 the quarter galleries (both 1/96); D6 the plan of the screen
  bulkhead, quarter galleries and stern rail (1/96); D7 and D8 the head from the side and the
  front (1/96); D9 the head from above and below (1/96); D10 the head from below and D11 the
  figurehead (no scale). Kept privately in `owner-notes/bellerophon/lavery-decoration/`, cited
  by figure (pages to confirm), never copied. Her stern (two tiers of lights: the wardroom's
  below, the screen bulkhead's open gallery above with its breast rail, the foot space rail
  between), her quarter galleries (two tiers of lights, the drop below), and her head (knee,
  cheeks, three rails, cathead, figurehead, beakhead bulkhead) are measured from them at 1/96
  in place of Steel's general rule, and marked sourced (her class's own drawings). Carving and
  paint stay in words.

### 17.1 For the owner (few, plain; each with the design's pick)

1. **Where she floats.** The 1758 drawing and the *Bellona*'s 1763 report differ by about a foot.
   *Pick:* at the line where her drawn lowest port stands the report's 5 ft 2 in clear. Her draught is
   then 21 ft 2½ in, a foot under the report's 22 ft 2 in, which stays in her notes, and the drawn hull
   and the floating hull are one. Her lowest lee port shuts at 10.35° of heel, measured to the outside
   of the planking as the 64's are; the brief's 10.6° is the same sill on the moulded side.
   *What you would see:* in the viewer her midship lower ports a little over five feet above the
   water, the hull as ZAZ1357 draws it; heeled a little over 10° the lee lower ports shut; at Basque
   Roads she can stand into water about a foot shallower than the report's draught would allow before
   she touches.
2. **Her topgallants and royals, and the 64's.** Steel's p. 42 reads as a long pole-head rising above
   the listed topgallant mast, room for the topgallant and royal of Steel's sail table. Take that for her,
   and for the 64 too? *Pick:* yes, for both ships (your "spars rule" kept, the spars read this way).
   *What you would see:* her topgallant sails about half as deep again as the 64's present reading
   would cut them, and her royals higher; the 64 the same once her file is regenerated; each ship a
   little quicker in light airs.
3. **A frigate on her own meeting her.** Should a King's frigate on her own, British or French, keep
   away from an enemy ship of the line rather than run down to engage her? *Pick:* yes, unless the
   frigate sails in a squadron. *What you would see:* a French frigate on her own sighting the
   *Bellerophon* turns away and makes sail; in Basque Roads, a frigate coming out from under Aix on
   her own keeps her distance. A frigate meeting the 64 would be treated the same.
4. **The rear-admiral's flag.** A fit can carry only guns and stores. *Pick:* a scenario that hoists a
   flag lists the rear-admiral, and any of their people the story needs, as people aboard beyond her
   muster; her ship file is unchanged. The other way adds 15 men to her muster when a flag is hoisted,
   which needs a new key and world code. *What you would see:* in a scenario of 1794, Rear-Admiral
   Pasley aboard, berthed aft and on the quarterdeck in action; her 590 at the guns and the sails as in
   every other scenario.
5. **Robbing the guns by deck.** When sail work at quarters is short of hands, which guns' crews go
   first? *Pick:* first the lower-deck crews whose guns on the engaged side are shut by the sea; then
   the upper deck's, the quarterdeck's and the forecastle's from the end that bears least; the lower
   deck's last. *What you would see:* engaging to leeward close-hauled in a near-gale, "brace sharp up"
   takes its hands from the idle lower deck, the log says "from the lower deck, Nos. 4 to 10, their
   ports shut", and the eighteen-pounders above keep firing.
6. **Lavery's drawings of the poop, the stern and the head.** May the session have photographs of the
   deck drawings and the decoration drawings (p. 50 onward and pp. 54-57)? *Pick:* yes. *What you would
   see:* her poop, stern windows, quarter galleries and figurehead drawn from her class's own drawings,
   instead of placed by Steel's general rule and marked as judgement.

### 17.2 For the lead

1. **Her stage 0c** (§12.1): one key, `marines` on the quarter bill, inert and left out of the pickle
   while None; the numbering key and `Gun.by_deck` only if item 3 is taken. Should the 64 and the razee
   take the same `marines` key, so a marines' division forms at their beat? Their `BEAT_MEASURED` note
   leaves it to you.
2. **B7.b's files and keying** (§6.4): `crew/quarters.py` (hers) and `orders/gunnery.py` (no owner after
   stage 0; named here). The deck lines on two gun decks and robbing on a `lower` deck, so the 64's beat
   lines and robbing order move, pinned by none of B1's tests, shown old beside new. *Pick:* so keyed,
   the two two-deckers alike; else keyed on her bill alone and the 64 untouched.
3. **Numbering by deck** (§5.2, the option Indf §5.2 handed to her design): an explicit `numbering: by
   deck` key in stage 0c; her ids re-keyed by her module; `pair_key` and `name` in `parts.py` and
   `graph.py` (B3's) after B3's merge; the quarters' parse sites; deck-qualified numbers in the orders;
   the 64 and the razee renumbered in `indefatigable.py`. `parts.py` is B3's after 0E (Build §4.2),
   so stage 0c's one class default there (`Gun.by_deck`) is laid after B3's merge, on your
   allotment, checked as Build §3.4. *Pick:* B7.d at the end of her window, both two-deckers
   together; else both wait for a later package, and she is numbered on across decks.
4. **The tack at quarters** (answer 17; §6.7): the rule reasoned moves truth 7-136 and every ship's tack
   at quarters. *Pick:* B7.c at the end of her window, its own commit, bisected, on your word; else
   booked to the gunnery's later package.
5. **7-196's clause alone:** pinned only if your build machine measures 550 or more at her merge
   (estimated 500-620 before her spritsails and driver); else recorded, never a lowered floor. Agreed?
6. **The order under the owner's direction of 2026-10-29:** B1 is no longer held for the owner's test (a
   testing report instead), so SW-2 with SW-2b.2 follow B1's merge, SW-5 L2 and L3 behind them, and the
   order B2, B4, B7 stands. Confirm; the session records it in Build §2.6 before B2's window opens.
7. **If SW-5 L3 is not merged when her file is ready:** hold her window for it (Build §2.2's order), or
   pin 7-195's rule clause at once and add its battery clauses at L3? *Pick:* hold her window.
8. **The 64 under Steel p. 42,** if the owner takes §17.1 item 2: the 64's bytes, polar and light-air
   figures move, old beside new. In B1's stage B if her window is still open; else a step you allot.
9. **Her fits' names:** "arrogant class 1793", "arrogant class 1795" (the default), "as the bellona
   1812". Accept or rename.
10. **If the owner takes the rank-4 rule** (§8.3): `world/captains.py` (B7's by Build §4.1) and
    `data/captains/kings-ship.yaml` and `commodore.yaml`, which have no listed owner, as B7.e; the 64's
    scenario tests re-run. Who owns the two books?
11. **Truth 7-195's text:** 10.35° on the profile's half-breadth outside the planking, with the brief's
    10.6° on 22.7 ft moulded recorded beside it, the band 10.2-10.7° holding both.
12. **The close-hauled gap** against the *Bellona*'s reports (9-10 kn against the engine's about 7½),
    which the frigate's file likely shares: book it to a later package of the physics?
13. **The mizen course's tack, and the driver's jaws** (§4.5, §4.6). Her tack at 9 ft above the
    quarterdeck, under I32's throat, against Steel's general 6 or 7 ft and the 64's 6 ft 6 in: at
    6 ft 6 in her course's clew ends inside her judged poop and her driver fails both of Ext §17.2's
    checks. On I32's throat both hold, the after leech by 0.10 m. If the measured poop breaks a
    check: less head room (to 5 ft), a driver cut more than 10% under Steel's area, or `DRIVER =
    False`? *Pick:* less head room, to 5 ft; past that, a report to you with the figures, her file
    built with `DRIVER = False` until you rule.
    The 64 cuts her course at 6 ft 6 in: on her file at 8f30be9 its level foot ends about 0.14 m
    under her roundhouse deck at the side (§18 item 19). The same clew check for B1's stage B?
14. **Package 81's boundary: gun places over the rail** (§3.3). Her forecastle carronade of 1795 and
    her poop's carronades stand on triples 2 in under the rail, as the 64's forecastle carronade and
    roundhouse guns do; no source draws a port there. Her roundhouse is given no port size, but her
    forecastle's two real ports give that deck one. Pass a line to 81's design: a triple within
    `OVER_THE_RAIL_M` of the rail at its x is a gun place over the rail, not drawn as a port?

---

15. **The flag party aboard** (the owner's answer, §17.0): the key laid inert in stage 0c, and
    the world code that brings the rear-admiral and their people aboard, with their stations,
    when a scenario hoists the flag. Whose package, and whether 75 builds it beside her?

## 18. Found on the way

1. **The research's scratch 74 no longer loads at this head.** 86's magazine by kind refuses its
   calibre-keyed cartridges (`schema.py`, `_parse_fit`). Without its armament its static polar is the
   research's to the hundredth (4.48, 7.83, 10.99 kn), so the engine's polar has not moved since
   bc10297 (observed here).
2. **At the Channel line the polar loses 0.04-0.06 kn** at each best point (observed here).
3. **Steel 1794 vol. I pp. 41-42 set a long pole-head up from the stop, above the topgallant mast's
   listed length** (OCR l. 2934-2942, 4701-4702; page image). On that reading Steel's spar and sail tables
   agree above the topmast caps within 7-11% for the 74, and for the 64, whose design read the pole
   within the length (§4.2).
4. **The 1773 establishment gave the main topgallant the same 10 yards on the same 33-ft mast**
   (Lavery pp. 19, 21), with no royal: consistent with the reading above.
5. **The Regulations number single guns on each deck,** No. 1 the foremost to larboard and No. 2 the
   foremost to starboard (p. 215, OCR l. 12760-12763); the game's pairs keep one number to a gun and its
   opposite. Numbered on across decks from the lower deck, her lower deck's pairs run from No. 1
   forward as the period's numbering began; the period's single guns 2n−1 and 2n are her pair n.
6. **The marines' division never forms at the beat** on any file: the beat takes the marines to the long
   guns before the topmen (`_preferred_stations`); the 64 and the razee measured it. Her bill's key
   keeps hers.
7. **"Fire by divisions", split at midships, gives her lower deck Cumby's seven and seven** without
   change.
8. **Falconer's quarter gunner to every four cannon gives the 590 column's 18 exactly on the 1793
   establishment,** and 20 on the 1795 fit's 82: the carronades were not rated cannon.
9. **James's customary supernumeraries:** 15 for each of the four rear-admirals, 25 for a full admiral,
   50 for the commander-in-chief (vol. 1 p. 156, OCR l. 12961-12963).
10. **Every file names its decks after SW-2** (Build §5.3), so any deck-keyed rule reaches the eight
    unless keyed on the `lower` deck, on two gun decks or on an explicit key.
11. **A shared two-decker module.** Her module and B1's share the mast loop, the sails, the canvas, the
    company and the bill. A later package could lift them into `tools/ships/two_decker.py`, the 64's,
    the razee's and her files regenerated byte for byte as its proof.
12. **Steel's fore leech puts the driver's jaws at the course's tack,** since the two share the throat
    and the 11-yard leech (Ext §17.2). Under Steel's 6 ft 6 in tack the level boom would stand 3 ft under
    her taffrail's top and run into her judged poop aft of about 6 ft before AP, and after the raise both
    of Ext §17.2's checks would fail (the after leech about 20.4 m, the corners about 237 m², 10.6% under
    Steel's). Under I32's throat the boom stands about 6 in under the taffrail's top and ¾-3¾ ft above
    the judged poop deck, and both checks hold after a raise of 1.60 m, narrowly (§4.5, §4.6).
13. **Her lower thresholds are dense:** L7 10.35° and L8 10.44°; L6 and L9 both 10.68°; a pinned count
    needs heels chosen between them.
14. **Lavery's cables are 100 fathoms** for a 74 of about 1800, where the 64 took Falconer's 120.
15. **`SHIP_MODULES` runs the bilander before her** (`tools/gen_ships.py:8621`), where Build §3.1 item 1
    lists her third. Harmless: each module writes its own file.
16. ***Dragon*'s yards are Steel's 74 column within 1%** (Bel §13.4), so her sails' widths are Steel's
    cloths unscaled, and her driver's area Steel's 265 m², not the research's 243 m² scaled.
17. **The posts are free strings** (`PostSpec`), so the 590 column's second master and chaplain stand as
    posts; `IDLER_TRADES` bounds only the idlers.
18. **"A first rate" names no description,** and the *Victory* was one: the words for the moved refusals.
19. **The 64's mizen course and her roundhouse.** On `sixty-four.yaml` at 8f30be9 the course's tack
    stands 6 ft 6 in above her quarterdeck and its level foot ends at its clew (x −25.35 m) 7.45 m above
    her water, about 0.14 m under her roundhouse deck at the side there (7.59 m, interpolated on her
    `decks_m`; measured here on her file). B1's stage B cuts the lateen course from the same tack
    (`mizen_course_cut`). For B1 and the lead: the clew check of §1.5 (§17.2 item 13).
20. **Truth 88's frigate never heaves to.** Its "heave to" at the first tick is refused, the plain sail
    not yet set, and she sails on at 2-3 kn; ordered once the sail is set (900 ticks), it is carried out
    (observed here; Bel §7.5 found the refusal). Her 7-196 heaves to after the sail is set (§14.4).
