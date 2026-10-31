# Design: the bilander, a British coasting trader under a settee main (package 75, Phase 3)

The design for the third ship of package 75 to be built (B4). It was judged from two drafts, one
written for fidelity and one for buildability. Every claim kept was checked against the code at
this head, the notes and the held images; where the drafts disagreed, or one was wrong, this
document says so and gives its reason (the table below). It follows the *Indefatigable*'s design
(**Indf**) in shape. It names her stage 0, her files, her truths' measures and her pins, as
`Build-Ships.md` §13 asks, and settles what §13.3 there says her design must settle. It is for
her builder (B4), the stage-0 agent of her window, the engine builder (B3, for what B3.3 must give
her), the viewer builder (B5) and the lead. Nothing here is built.

**What binds, in order:**
1. The brief (`docs/dev/M7-WorkPackages.md`, its head rules and "## Package 75", item 3: the
   British bilander with a settee main, Gwyn's drawing, unarmed by default with an armed merchant
   fit). The lead's notes at its end: the gate's approval of the engine extensions (2026-10-28);
   the order and the merges (item 8: the *Indefatigable*, the *Neufchatel*, the bilander, the 74;
   the lead merges after each ship); stage 0E accepted (2026-10-29); the hull's principles,
   design and order approved (2026-10-29); the rulings on Ext §14 items 3 and 4.
2. `Build-Ships.md`: §13.3; §2.2-§2.6, as changed by **the owner's direction of 2026-10-29**: the
   build goes on without holding for the owner's own test of the *Indefatigable*, the owner
   receiving a "testing report" with the basics and pictures of the important views instead, so
   her window follows B1's merge and then B2's, as each ship is merged; §3.3 (her stage 0d); §4;
   §5.0-§5.3, §5.6, §5.7; §6; §7; §14-§16; §19.
3. `Decisions-ShipsRound2-2026-10.md` (**Dec**): every decision not named in the owner's answers
   taken as recommended. For her: D1 (a); D2 (a); **D3 (b)**; D4 (a); D5 (a); D6 (a) with (e);
   D7 (a); **D8 (b)**; D13 (a); **D14 (c)**; D16 (a); D24 (a); D26 (a) with (b); D40 (a); D41 (a);
   D42 (a); D43 (eight); D44 (a); D45 (a) with (c); **D46 (d) with rule 3 restored**.
4. Her research note, `docs/design/Research-Bilander-2026-10.md` (**Bil**), and the notes it
   cites; **Eng** (`Research-ShipsEngine-2026-10.md`).
5. `Design-ShipsEngineExtensions.md` (**Ext**): the settee (§5, D46 rules 1-5, B3.3, its drawing
   B5.4), the yards under the bowsprit (§4, B3.2), the helpers' contracts (§9.3), the truths
   (§10.3).
6. The owner's private references (`D:/Projects/FreeSail/owner-notes/`): facts by book and page
   only. None of their books is needed for her. The held images there
   (`owner-notes/bilander/rmg/`: Gwyn's 1560-px image and the note's grid crops, Chapman's IA
   leaf 0141) are read for figures; the images never enter the repository.
7. Pictures for the eye: Gwyn's PAG3828 (`docs/references/images/
   bilander-gwyn-c1780-nmm-pag3828.webp`, public domain by age) and the modern PSF line drawing
   (`bilander-line-drawing-psf.webp`), which gives no figure. **Plainly:** Gwyn's drawing is also
   the owner's named source for her (the brief item 3; D5, D6 (e), D7, D14), so its measured
   ratios are used as figures, each marked, at Chapman's scale.

**Where.** The clone `D:/Projects/FreeSail/FreeSail-pkg-75` on the package's branch at 8f30be9.
Every `file:line` is at that head. Stage 0H and B8's SW-2b.1 are under way in that clone's working tree
and not yet committed (`freesail/ship/form.py`, `tests/test_hull_form.py`, and `g.hull_form`,
`g.midship_section`, `g.from_steel_table` in `tools/gen_ships.py`); where this design leans on
them it cites `Build-Ships.md` §3.5 and §5.3 and the names, not lines. A builder re-checks a line
before using it. Paths are from the repository root.

**Marks.** *read*: the page, image or code cited was seen. *read (OCR)*: the text layer only.
*measured*: off an image, with its error, as the notes give it. *measured here*: by this design or
its drafts, arithmetic on the notes' figures, or a reading of the held crops (±10 px a point,
about ±0.3 m at her scale). *read here*: three leaves of Steel 1805 (IA `elementspractice00stee`,
n474, n484 and n488; "No Copyright - United States", as `docs/references/README.md` l. 53 records
the item), fetched by the buildability draft into the new folder
`D:/Projects/FreeSail/reference-cache/steel-1805-collier-brigantine/`, outside the repository,
and the dead flat of p. 26 re-read on n484 by the judge; Folio I's row letters for the collier
(n488) and p. 26's stations in both bodies (n484) re-read on the page images by the check that
followed. *observed*: printed by a scratch probe run
from the tree root with `py` (`scratchpad/designs/bilander/probe_polar.py`, `probe_scaled.py`,
`probe/polar_probe.py`, `probe/figs2.py`, `final/probe_final.py`; the scripts are not filed).
*catalogue*, *secondary*, *memory*, *judgement* as the notes use them. "Plainly:" marks a
departure from a decision, a ruling or the brief, with its reason. Rungs of the hull's ladder are
`Build-Ships.md` §5.0's: **S**, **S†**, **R**, **T**, each line marked `sourced`, `stand-in`,
`rule` or `judged`. Nothing in the repository was changed, no git command wrote, and no test
suite was run.

**One sentence.** One module writes one file: Chapman's bilander of 1768 at the plate's own scale
(70.6 by 19.4 ft, 118-128 tons), drawn as Gwyn's British coaster (raised quarterdeck, round
windowed stern, a figure) on Steel's brig collier's body, rigged to Gwyn's heights with Chapman's
yards, her main a settee cut to Gwyn and slung at a third, unarmed by default with Elizabeth's four
3-pounders as her armed fit. She is built and tested in her own worktree from her window's
opening, after B2's merge, and reaches the package's branch only once the engine's settee (B3.3)
is merged there, because without it her main is a lugger's dipping lug to every path.

---

## How the two drafts were judged

| Question | Taken from | Why, in short |
|---|---|---|
| The base: hull, rig, settee, guns, crew | fidelity | Its hull is drawn as herself: every rail, quarterdeck, wale, stern light and head point measured and marked; its engine-contract findings are right. The buildability draft's core figures failed (the rows below) |
| Her size | fidelity: Chapman unscaled, with a Plainly line | D7 (a) gives 70.6 by 19.4 ft at about 123 tons; 128 tons is "about 130" (D6 (a)). The buildability draft's ×1.02 is the other reading of D6 (a), put to the lead (§17) |
| The datum of Gwyn's heights | fidelity: the waist rail | On the hull crop the masts' feet are drawn at the waist rail (image y 958 against the rail at 961, ±5 px). The buildability draft laid them from the deck, 0.73 m lower on every rig height |
| Displacement, GM, Cb | fidelity (229 t, 0.66 m, 0.50) | D7 (a): "by the brig file's methods". The buildability draft's Cb 0.52 and GM of 0.12 B departed from it with no Plainly line |
| Draught | fidelity's 11.5 ft, the collier's check beside it | Either is judgement on Lloyd's 11 and 12 ft; the collier's 10 ft 9 in at 170 tons is recorded (§2.1) |
| **Her body under the water** | **buildability: Steel 1805's brig collier** | A period table of her type, read here (title, dead flat, Folio I). It raises §5.7's "a trader's body R/T" to S† once transcribed (§3) |
| The stand-in's length ratio | neither: 0.92, recomputed, provisional | The buildability draft's 0.94 was its scaled 72 ft against the collier's 76 ft 11 in; on 70.6 ft it is 0.92. Folio I's row C, read by the sloop's method, suggests about 0.95: settled at step 1 (§3.4) |
| The aft rail | fidelity (3.30 m at the taffrail) | The buildability draft's 2.45 m "judged" contradicts its own swivels on that rail at 3.29 m |
| The settee's cut and corners | fidelity (73.3 m²) | The tack at Gwyn's height, D5 (a)'s third; the crossing height measured and recorded, not used to place the yard (§4.4) |
| **The sheet's lead** | **fidelity** | `trim.py:388` takes a foot of 0.8√A from the tack, so the block falls 4.45 m short of the taffrail and Ext §5.9's reserve branch is triggered. The buildability draft's "a fathom abaft the clew, so not needed" read the corners, which the trim never reads |
| The brig's plain sail | fidelity: 766 m² | `data/ships/brig.yaml`'s "plain sail" sums to 766 m² on 413 t (read here); the buildability draft's 672 was wrong, so the rope factor is 0.70 |
| Staysails between the masts | buildability | No main staysail: its foot would lie across the settee's fore part. The main topmast staysail is bent, out of plain sail, and the lying-to staysail; neither draft's "occasional" is kept, since the code's "occasional sails" start the voyage unbent (§4.5) |
| Brace limits | neither: the brig's level for level | Fore 60°, 62°, 64°; main 62°, 64°, 66° (`brig.yaml`, read here). The fidelity draft's 60° for the dry yard was the frigate's crossjack, which stands on a mizen |
| The spritsail; the rig word; the quarter badge | settled here, not asked | The razee's answer carries (a sail bent, out of plain sail); §13.3 there makes the rig word the design's; principle 9 puts carving in words |
| The armed fit's ports | buildability's owner question | Gwyn draws no port; the choice between ports and an open rail is the owner's (§17) |
| Gun crews | fidelity: Falconer's three | The owner's rule for the new ships' crews (D31 (c); the 74's answers). Two a gun had no Plainly line |
| Rule 2's hand count in 7-198 | fidelity | D46 (d): "by how many hands" |
| The heave-to | buildability | The lead's ruling on Ext §14 item 3: the driver rule first, D4 (a) if the figures say otherwise |
| Rule 5's fallback | buildability | The lead's ruling on Ext §14 item 4: D44 (c)'s `settee` row accepted in advance |
| The order | buildability's hard rule, fidelity's allowance | Her file is not committed to the package's branch before B3.3; she is built and tested in her worktree from her window's opening |
| The hook test's row | buildability | A stage-0 commit immediately before hers, as 9454fd6 came just before 614d2d4; B4 never touches `tests/test_profile.py` |
| The 0H guard | buildability | `tests/test_hull_form.py`'s pickle test fails on any file with shape keys (read here); the fidelity draft missed it |
| The testing report | buildability, as step 6 | The owner's direction of 2026-10-29 |
| The module's shape | buildability | Particulars as data in the sources' units, converted once; section functions in a fixed order; checks raise `ValueError` with a sentence |
| The dry yard's checks | both, relabelled | Chapman's brig rule (fidelity) gives 40.8 ft. The buildability draft's "Steel's crossjack proportion" is not Steel's rule but the 64's crossjack to her mizen topsail yard carried to her by judgement; it agrees at 40.8 ft. Steel p. 40's own rule (the crossjack as the fore topsail yard) would give 30.0 ft and is not taken (§4.1) |
| The polar | both, and this design's own probe | Three probes, the last on this design's own figures (§9) |
| The scenario's nations | buildability's mark | Spain allied to Britain in 1793-95 is memory, unverified until read in James vol. 1 |
| Her name | fidelity's, put to the owner | "Hopewell" was a real Poole bilander's name; whether to reuse it is the owner's taste (§17) |

---

## Decisions taken

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/bilander.py`, `build(out_dir)` writing `data/ships/bilander.yaml`; her cut in her own pure `tools/ships/settee.py`; her spritsail yard through B1's `tools/ships/spritsail_yards.py` | `Build-Ships.md` §3.3, §4.1; Ext §9.3; the lead's names (item 9) |
| 2 | Her particulars as data in the sources' own units (Chapman's Swedish feet, Gwyn's shares of the rail length, Lloyd's feet, Steel's feet and inches), converted once in a frozen `Particulars`; section functions in a fixed order; checks raise `ValueError` with a sentence | Indf §1.4's way: every figure reads as its source gives it |
| 3 | **The hull is Chapman's No. 5 at the plate's own scale:** LWL 21.52 m (70.6 ft), beam 5.91 m (19.4 ft), the waist rail 1.65 m (5.4 ft) above the water | D7 (a). **Plainly:** not scaled by D6 (a)'s "about 2%" to 130 tons (§2.1; for the lead, §17) |
| 4 | Draught 3.51 m (11.5 ft) to the keel's lower edge (D29 (b)'s convention) | D7 (a): Lloyd's 11 and 12 ft for the two bilanders of 130 tons; the mean, judgement. The collier's 10 ft 9 in at 170 tons recorded beside it |
| 5 | Displacement 229 t (Cb 0.50), GM 0.66 m, lateral plane 64.2 m², hull speed 10.3 kn to start, deck 0.92 m | D7 (a): "by the brig file's methods, marked judgement"; D24 (a); D18 (a) |
| 6 | **Her body under the water and her breadths by station: Steel 1805's brig collier of 170 27/94 tons** (Tables p. 26), scaled (lengths 0.92, provisional until step 1 settles the collier's length; sections 0.847), through `g.from_steel_table`; S† once transcribed at step 1, T "to read" until then | `Build-Ships.md` §5.7's next source, read here; §5.0 principles 3, 5, 7 |
| 7 | **Gwyn's sheer on Chapman's waist:** the raised quarterdeck from x −4.0 m rising to 3.30 m at the taffrail; the bow rising to 2.65 m at the stem head; the stern `round` with three lights in one band; the head `figure` | D14 (c); §5.7's row; principle 9 |
| 8 | Masts at Chapman's stations; **heights by Gwyn's shares of the rail length, laid from the waist rail**; yards by Chapman's measured lengths | D6 (a) with (e). **Plainly:** D6 (e) and Bil §2.3 say "above the deck"; Gwyn's masts stand on the drawn waist rail (§1.4) |
| 9 | A **dry yard** (`main.crossjack.yard`) under the main top, 12.44 m; topgallants on both masts; no royals | D40 (a); Chapman's brig rule. The check, by judgement: the 64's crossjack to her mizen topsail yard (Steel p. 49) carried to her. Steel p. 40's rule for a ship's crossjack is not taken (§4.1) |
| 10 | Brace limits the brig's, level for level | The brig is her comparator in 7-197; no source gives hers |
| 11 | **The settee** to D5 (a): head 15.67 m on a yard of 16.59 m at 44°; luff 0.16 of the leech; leech and foot 0.72 of the head; slung at a third on the main mast's raked line; the tack at Gwyn's height; about 73 m² | D5 (a); Ext §5.1's contract |
| 12 | Its lines Lescallier's; one unsided sheet to the taffrail; **B3.3 asked for Ext §5.9's reserve branch from the start**, its block placed one of two ways for the lead to choose (§12.2 item 6) | D45 (a) with (c); the trim's block falls 4.45 m short (§12.2) |
| 13 | `heave_to_aback: true` on the main mast; hove to, the settee by **the lead's ruling** on Ext §14 item 3 | D4 (a) for the mast; the driver rule for the sail unless the figures say otherwise |
| 14 | The settee in "courses", "plain sail" and "all sail", never "gaff sails" | Ext §5.1, E15 |
| 15 | **The spritsail yard crossed, a spritsail bent to it** (`bent: true`), in "spritsails" and "all sail", out of "plain sail" and out of the code's "occasional sails"; no sprit-topsail yard | D8 (b); Ext §4.1's groups; the razee's answer ("an occasional sail", set now and then, out of plain sail) carried to her; settled here (§4.3) |
| 16 | Headsails the jib and the fore topmast staysail (Gwyn); between the masts **the main topmast staysail only**, bent (`bent: true`), out of plain sail, the lying-to staysail; no main staysail | Lescallier pp. 402-403 (the brigantin's staysails, Bil §2.1), Chapman No. 5 the check; the settee's fore part (§4.5) |
| 17 | No studding sails, no royals, no driver | No drawing of her type shows them (Bil §2.6; D40); nothing invented |
| 18 | Fits: **"unarmed"** the default; **"armed merchant"**: four long 3-pounders, two a side in the waist, and four half-pounder swivels on the quarterdeck rail | The brief item 3; D41 (a): Elizabeth's "4-3 P." |
| 19 | The armed fit's ports: two a side in the waist bulwark, sills judged; **the owner's question** (§17) | Gwyn draws no port: the drawing shows her unarmed |
| 20 | The 3-pounders crewed by Falconer (three a gun); a merchant's magazine; "sail before guns" | D31 (c)'s rule for the new ships; the merchant brig's pattern for the rest |
| 21 | Company **eight**: master and mate (posts), two in each top, a boy, a cook; `names: english` | D43; Ext §5.1 and risk 10 |
| 22 | Ground tackle, boat, pumps, hold by the merchant brig's rules; Steel 1794's Navy anchor table the check | Bil §2.7 |
| 23 | Description key `bilander`, rank 1; rig word **"a bilander"**; what "a bilander, a merchantman under a settee main, deep laden"; roles `merchant` | D16 (a); §13.3 there makes the rig word the design's |
| 24 | `ship.name` **Hopewell**, put to the owner | Judgement on a Poole bilander's name (§6.3, §17) |
| 25 | Her stage 0d lays **nothing in code**. One stage-0 commit, the hook test's row, lands immediately before her first commit | §12.1 |
| 26 | **Her file is not committed to the package's branch until B3.3 is merged there**; she is built and tested in her own worktree from her window's opening | Without B3.3 her settee takes the lugger's paths (Eng §4.4; Ext §5.8). **Plainly:** `Build-Ships.md` §2.4 and Ext §9.4 let her file reach the branch after stage 0E, with only her handling truths waiting for B3.3 (§0) |
| 27 | Three truths: 7-197 measured at stage A, 7-198 and 7-199 on B3.3; the heave-to a test | `Build-Ships.md` §15 |
| 28 | **A testing report** to the owner in place of the owner's own test (§13.1) | The owner's direction of 2026-10-29 |
| 29 | Carving and paint in words: the blue stern and red band, the figure and head rails, an oval badge on each quarter, the ensign on its staff | §5.0 principle 9; §19.1 item 17 there |

---

## 0. The gate: what her builder builds at once, what waits

**The gate is passed.** Ext was approved on 2026-10-28. Stage 0E, which lays the settee's keys
(`SailSpec.settee`, `SparSpec.heave_to_aback`, `Sail.yard_lowered`, the runner's `class:
settee`), was accepted on 2026-10-29, and the hull's design was approved the same day. Nothing of
hers waits on a ruling. What waits is work: the engine's settee (B3.3), its drawing (B5.4), the
form's drawing (B5.6), and the 0H guard restated before her first commit (§12.1).

**Her window** opens at the boundary after B2's merge, with the fresh merge of the lead's branch
(`Build-Ships.md` §2.1). By then B1 is whole and merged, with stage 0H, SW-2b.1, B3.1, B3.2, B3.5
and B1's `spritsail_yards.py`, and SW-4 is in (it comes before B2: §2.2 there). **Plainly:** §2.2
and §2.6 there hold B2,
B4 and B7 for the owner's first test of the *Indefatigable*. The owner's direction of 2026-10-29
lifts that hold: the owner receives a testing report of each ship instead (§13.1). Her place third
in the order, and the lead's merge after each ship, stand.

**One hard rule.** Her file is not committed to the package's branch until B3.3 is merged there.
Without B3.3 her settee is class `lug` with `dipping: true` to every path the engine has:
`_lugs_all` (`evolutions/scripts.py:6800`) counts it, so she gets under way as a lugger, which
failed in the trial at 1,842 s (Eng §4.4; Ext §5.8); hove to it is lowered and the fore topsail
backed, and she fell off to 79-87° (Ext §5.7). The harbour lists every file in `data/ships/`
(`ui/harbour.py:382`), the lead merges the package's branch whole, and the owner may test from it.
A file "held from the harbour" on the branch would still sail the lugger's paths. Her module
cannot go without her file either: the generator writes the file whenever the module is in, and
the two-way byte test then demands it. **Plainly:** `Build-Ships.md` §2.4 and Ext §9.4 let her
file reach the branch after stage 0E, with only her handling truths waiting for B3.3 (§2.2's row
B4: "B3.3 (for her handling truths)"). It is held back here because, before B3.3, her settee
takes the lugger's paths on every route the harbour offers (`_lugs_all`, the heave-to's lowering).
Lead item 1 puts the timing to the lead.

**At once, in her own worktree** (forked from the package's branch at her window's opening): §13's
steps 1-4.
- `tools/ships/settee.py` and `tools/ships/bilander.py`, her file complete: hull, profile and shape
  keys, masts, yards, square sails, the settee, the head, the spritsail yard, staysails, groups,
  aliases, both fits, the bill, the company, stores, ground tackle, boat, pumps, hold,
  descriptions;
- `data/people/bilander.yaml`; her rows in `freesail/world/ships.py`;
- `tests/test_bilander.py`: her particulars, her polar, and truth 7-197 whole. Its polar clause
  reads no handling code: `polar_of` trims and sums forces only (`world/ships.py:471-490`).

**On B3.3** (merged into the package's branch and brought into her worktree): §13's step 5. The
heave-to both ways (Ext §5.7); the sheet's block against the taffrail (Ext §5.9); rule 5's measure
on her file (Ext §5.10, B3's there; B4's here, lead item 8); the untried manoeuvres run once on her
file (Ext §5.4); her requests at eight; truths 7-198 and 7-199; her first hour at seed 7. If rule 5
takes D44 (c), B3 adds the `settee` row as a follow-up step before her merge, and her polar,
§9's table and 7-197's rule-1 clause are measured again on it, old beside new (§14). Her commits
then land on the package's branch, the stage-0 commit first (§12.1).

**On B5.4 and B5.6:** §13's step 6, the testing report; reported done; the lead merges.

**If B3.3 lags her stage A,** she is held unmerged in her worktree until it is in. What the lead
does meanwhile with the 74's window (`Build-Ships.md` §2.2: B7 after B4) is §17's lead item 1.

---

## 1. The module and the generator

### 1.1 Files

| Path | What | Owner |
|---|---|---|
| `tools/ships/bilander.py` | the data at the head; `particulars()`; `write(out_dir, p)` and its section functions (§1.4); `build(out_dir)` | B4 (replaces stage 0's stub) |
| `tools/ships/settee.py` | `cut(...)`: the corners to D5 (a), the area and centre; `lines()`: Ext §5.1's lines as ids, classes and sides; its checks. Pure, importing nothing from `gen_ships` | B4 (Ext §9.3) |
| `tools/ships/spritsail_yards.py` | read only: the spritsail yard alone, as the razee takes it | B1 (Ext §9.3; `Build-Ships.md` §4.2) |
| `tools/ships/period.py` | appended: Adye's 3-pounder, once read (§5.3) | stage 0; B4 appends in her window |
| `data/ships/bilander.yaml` | generated only | B4, through the generator |
| `data/people/bilander.yaml` | the master, the mate, the boy as messenger | B4, hand-written data |
| `tests/test_bilander.py` | her tests and her three truths' drafts | B4 |
| `freesail/world/ships.py` | her `DESCRIPTIONS` row and her words, in her window | B4 |
| `docs/design/ships-design/pages-steel-1805-collier.md` | new: the collier's bodies table and folio rows, facts only (§3.6 task 1) | the session's docs commit, from B4's transcription handed over as text (B4 owns no doc: `Build-Ships.md` §4.1) |

Her file's header is its own literal string with "Generated by tools/gen_ships.py" in it, as every
file's is (the phrase `tests/test_fishing.py:99` reads).

### 1.2 The import

Stage 0 laid the hook (`tools/gen_ships.py:8621`, `SHIP_MODULES` naming `bilander` third; the
alias and the loop in its `__main__` block; Indf §1.2, measured there). The module begins `import
gen_ships as g` and `from ships import period, settee, spritsail_yards`, and takes every helper as
`g.<name>`. `g.wardroom("bilander")` is called inside `build()`, never at import, so a missing
people file breaks only her build. `settee.py` and `spritsail_yards.py` import nothing from
`gen_ships`, so no second copy of the generator can arise from them (Ext §9.3).

### 1.3 What B4 reuses, read only, and what is new

**Reused** (`tools/gen_ships.py` at 8f30be9): `Builder` (:650); `ft`, `FT`, `SIDES`, `rope_kn`
(:415), `design_kn` (:449), `DESIGN_WIND_KN`; `cloth` (:353), `canvas_note`, `BRIG_CANVAS` (:5887),
`BRIG_ROPE_SCALE` (:5926), `PEAK_COEFF` (:136); `hull_profile` (:587); `square_sail_lines` (:1533),
`stay_sail_cut` (:1210), `staysail_from_cut` (:1248); `_quad_area_centroid` (:7162); `raked_x`
(:2619), **always with `deck_m=` her own 0.92**; `broadside_pair` (:3837, with `deck=` and
`round_to=0.01`), `swivels` (:3899), `fit_magazine` (:3718), `filling_party` (:3769),
`MERCHANT_ROUNDS`, `SWIVEL_ROUNDS` (:3708-3709), `SWIVEL_CWT` (:3679), `QUARTER_BILL_NOTE`
(:3933), `PRIORITY_NOTE`; `hold_for` (:3467), `boat_entries` (:3478), `pump_entries` (:3537),
`ground_tackle_for` (:499), `ration_entries` (:3635), `wardroom` (:3607); the notes `PUMPS_NOTE`,
`BOATS_NOTE`, `SHOT_PLUGS_NOTE`, `SMALL_ARMS_NOTE`, `BOARDERS_NOTE`. From SW-2b.1 (working tree):
`g.hull_form(hull, notes, *, form, marks, measured=())`, `g.midship_section(...)`,
`g.from_steel_table(rows, *, length_ratio, beam_ratio)`.

**Written anew in the module, on the brig's lines** (`brig()`, :5930, takes no particulars and
dumps itself, so it is not touched): the two masts' loop, the yards, the square sails' cut between
their yards, the head, the main topmast staysail, storm canvas, groups and aliases. The module's
`geom[mast]` uses the brig's keys (`above`, `head`, `t_hoist`, `g_hoist`, `yard`, `topsail_yard`,
`tg_yard`, `yard_h`, `topsail_h`, `tg_h`; :6034-6062), filled from §4, so the copied loops run
unchanged. No royal keys. The settee is written from `settee.cut()`, as the lugger writes its lugs
from its own cut (`lugger()`, :7177). The merchant brig's crew and armament (`merchant_brig_crew`,
:6849; `merchant_brig_armament`, :4504) are the pattern for hers. `between_the_masts` (:1297) is
not called: it writes the main staysail with the topmast staysail (§4.5).

### 1.4 The data, the frame, the shape and the checks

- **Data at the head of the module**, each with its source in a comment, in the source's own
  units: `CHAPMAN_NO5` (Bil §2.4: the waterline, the breadth, the rail, the overall lengths, the
  mast stations and rakes, the mastheads, the yards at twice their drawn length, the bowsprit; in
  Swedish feet, `SW_FOOT = 0.2969` m); `GWYN` (Bil §2.3 and §3.2 below: the rig's heights, the
  sheer, the quarterdeck, the wale, the stern view, the settee's ratios, as shares of the rail
  length); `LLOYDS` (Bil §2.2: the draughts and tons of the bilanders of 120-140 tons, Elizabeth's
  guns); `STEEL_COLLIER` (Steel 1805 Tables p. 26 and its Folio I column, in feet and inches, as
  transcribed at step 1); `D5` (the cut's ratios). `particulars()` converts them once into a frozen
  `Particulars`.
- **The file frame.** x in metres forward of the middle of her load waterline; z above that
  waterline. The waterline's ends are her post and her stem at the water, x = ∓10.76.
- **Gwyn's figures at her scale.** Gwyn's drawing has no scale (Bil §2.3). Its figures are taken
  as shares of the drawing's rail length (stem head to taffrail, 785 px) and laid on Chapman's rail
  length, 23.04 m (75.6 ft), **upward from Chapman's waist rail**, 1.65 m above the water. A Gwyn
  height is `1.65 + share × 23.04`. Two reasons: Gwyn's sea line is freehand; and the drawing's
  "deck" for the rig's heights is its waist rail (the masts' feet at image y 958 against the rail
  at 961, ±5 px, measured here on the hull crop). **Plainly:** D6 (e) and Bil §2.3 say "above the
  deck"; laid from her deck, 0.92 m, every rig height would stand 0.73 m lower. Each such figure's
  note says so, and its line is marked `stand-in` (§3.3).
- **`to_file`, once:** a lower spar's `height_m` is its z less her datum, 0.92 m (§2.2); an upper
  mast's is its hoist above the cap below; `corners_m` heights above the datum; a sail's
  `centre_height_m` and a gun's `height_m` above the water (the file's conventions; Indf §1.4).
- **Rounding:** measured figures rounded once, at the source's precision, before any trigonometry,
  so that a last-bit difference in `math.sin` between machines cannot flip a written figure (Indf
  §16 risk 4); spars and sails as the brig's.
- **The shape.** `build(out_dir)` calls `write(out_dir, particulars())`. `write` builds one
  `Builder` in this order, each a function of `(b, p)`: `hull_block`, `masts_and_yards`,
  `square_sails`, `the_settee`, `the_head` (bowsprit, jib-boom, jib, fore topmast staysail, the
  spritsail yard and its sail), `staysail_and_storm` (the main topmast staysail, the storm
  canvas), `groups_and_aliases`, `armament`, `crew_and_people`,
  `stores`, `tackle_boats_pumps_hold`, `descriptions`; then `b.rate_spars()`, the profile and the
  shape (`g.hull_profile`, `g.hull_form`) as the hull's last key, and `b.dump`.
- **Checks before the file is written**, each `raise ValueError` with a sentence, never `assert`:
  the burthen by the old measure between 118 and 130 tons; the settee's contract (`settee.py`,
  §4.4); the spritsail's foot above the water (the helper's own); the fore course's foot clear of
  the rail at the fore mast; the main topmast staysail's foot clear of the settee's yard; each port
  gun on a triple of its deck to the centimetre.

---

## 2. The hull blocks

### 2.1 The figures

| Field | Figure | Source and mark |
|---|---|---|
| `length_waterline_m` | 21.52 | Chapman 1768 Pl. LXII No. 5: 72.5 Swedish ft, 70.6 English, ±1.5-2 ft where the stem is read (Bil §2.4, measured). S† |
| `beam_m` | 5.91 | No. 5's breadth marks, 19.9 Swedish ft, 19.4 English, ±1.5% (Bil §2.4, measured); taken as extreme (judgement: the marks do not say). S† |
| `draught_m` | 3.51 | 11.5 ft to the keel's lower edge: Lloyd's draught loaded, 12 ft for Elizabeth and 11 ft for the Duke of York of Bristol, both of 130 tons (Bil §2.2, read on the row images); the mean, judgement. The register's key (1781) calls the column the draught loaded and does not say whether it is the mean or the greatest; taken as the deepest wood, D29 (b)'s convention, so that she grounds on it. **The check:** Steel's brig collier of 170 tons draws 10 ft 9 in afore and abaft (Folio I, read here), less than the register's bilanders of 130, which suggests the register's column is the greatest draught deep laden (judgement). Chapman draws no draught |
| `displacement_kg` | 229,000 | LWL × B × T × Cb 0.50 × 1025, the brig file's method (`gen_ships.py:5946-5948`; D7 (a)): 1.8 times her 128 tons burthen (measured here). Cb judgement, the brig's. `g.hull_form` records the drawn displacement beside it, never in its place (§5.0 principle 8) |
| `gm_m` | 0.66 | The brig's method: the frigate's 4 ft 3 in scaled by the breadth (19.4 against 38.3 ft), as the brig's 0.95 is by hers (measured here). Judgement; a deep-laden coaster |
| `clr_x_m` | +0.40 to start | The brig's 0.5 m as a share of her waterline (0.019 L), tuned as the house tunes it: a little weather helm close-hauled and a few degrees on a beam reach in 15 kn (`gen_ships.py:5991-5997`). Recorded as tuned |
| `lateral_area_m2` | 64.2 | LWL × draught × 0.85, the brig's rule (`gen_ships.py:5976`): 21.52 × 3.51 × 0.85 (measured here). The brig rounds hers to tens; hers keeps the tenth, rounded once (§1.4) |
| `hull_speed_kn` | 10.3 | D24 (a): the brig's 11.5 kn by √(70.6 / 88) (measured here). No period speed exists for a bilander (Bil §4) |
| `deck_height_m` | 0.92 | Her upper deck at side at x 0 (D18 (a); `Build-Ships.md` §5.5). Judgement: Chapman's rail less a merchant's waist of about 2 ft 5 in. Steel 1805's coasting sloop floats with her deck 3 ft 0½ in above the water at dead flat (`ships-design/pages-steel-1805-bodies.md` §0, read), the like freeboard. **To check** on the collier's Folio XXXII (deck above the rabbet, the waist) at step 1 |
| `rudder` | area 2.4 m², span 3.2 m, 35°, 3.5°/s | The brig's blade (`gen_ships.py:5979`) by her length and draught (judgement) |
| `profile` | §3 | D14 (c); `Build-Ships.md` §5.1 |

**Her burthen.** (L − 3/5 B) × B × B/2 / 94 on B 19.4 ft gives 118 tons on the waterline's 70.6 ft
and 128 on the taffrail-to-stem-head 75.6 ft (Bil §2.4; measured here). The rule's length lies
between them. 128 is used where the generator reads tons (the anchors, the boat, the hold), as
D6 (a)'s "about 130". Her `era_notes` give both. **Plainly:** D6 (a) says Chapman's figures "scale
by only about 2%" to 130 tons. They are not scaled: a scale factor would be a figure no source
gives, 2% lies inside Chapman's own ±1.5-2 ft, and D7 (a) gives the hull as 70.6 by 19.4 ft. If the
lead reads D6 (a) as the scale, ×1.02 moves every Chapman figure by 2% and the burthen to 125-136
tons (§17, lead item 6).

**The masts** stand at Chapman's stations at the rail (Bil §2.4, measured: "use the rail
positions"): the main 0.41 of the waterline forward of the post, x −1.94 m, raking aft about 2.8°;
the fore 0.148 abaft the stem, x +7.57 m, nearly plumb; 9.51 m apart (31.2 ft; Chapman 31.1). Gwyn's
are within 0.2 m (main) and 0.6 m (fore) of them at her scale (measured here). S†.

### 2.2 Her datum (D18)

D18 stays open for the existing files and the razee. For a new file `Build-Ships.md` §5.5 proposes
(a), the uppermost continuous deck at midships, taken from her profile. Hers is her upper deck,
0.92 m above the water at x 0, which runs flush from the stem to the taffrail under the raised
quarterdeck (§3.2). (c), her quarterdeck, is no working deck at midships, so (a) has no rival, and
nothing of hers waits on the owner's choice for the razee.

---

## 3. The hull profile and her shape (D14 (c); `Build-Ships.md` §5.0-§5.3, §5.7)

### 3.1 What the sources give, by rung

| Feature | Source | Rung |
|---|---|---|
| Length, breadth, waist rail, overhangs, mast stations | Chapman No. 5, to the plate's scale bar (Bil §2.4) | S† (a period plan of her type) |
| The raised quarterdeck, its break and rail; the sheer; the wale's band; the round stern and its three lights; the figure and head rails; a carved badge on each quarter | Gwyn PAG3828 (Bil §2.3; measured here, §3.2) | S for what is drawn; its dimensions at Chapman's scale, so S† |
| The body under the water: the breadths by station, the main breadth, the sections, the midship section, the keel, the floor | **Steel 1805's brig collier of 170 27/94 tons, Tables p. 26** (IA n484, read here: the heading "Bodies of a Brig Collier of 170 27/94 Tons"; the dead flat at 30 ft 0 in abaft FP, the lower and upper heights of breadth 9 ft 7 in and 12 ft 1¼ in, the top-timber line 16 ft 4 in, the main half-breadth 11 ft 3 in); its Folio I column (n488, read here: breadth 22 ft 6 in moulded, 22 ft 11 in extreme; load draught 10 ft 9 in afore and abaft; row C, the stem at the hawse holes, in merchant ships at the wing transom, to the post's aft side, 76 ft 3 in; row B, the range of the deck, blank for the collier) | **S†** once the rows are transcribed at step 1; until then T, "to read: Steel 1805 Tables p. 26" (principle 3) |
| The greatest section's place | Chapman 1781 p. 81, §33 (read (OCR), l. 10096-10123): forward of the middle, for full merchant ships by up to eight times the centre of gravity's distance | R in direction; the collier's table gives the amount once read |

**Why the collier.** `Build-Ships.md` §5.7 names "Steel's brig collier (p. 26) or brigantine (p. 16)"
as her next source. The collier is a trader of two masts, the nearest Steel prints to her in size
and trade; the brigantine "of 10 Guns, 16 Swivels, and 201 Tons" (p. 16, read here) is armed and
finer. Neither is a bilander: no lines of any bilander exist (Bil §6). Scaling the collier to her is
judgement, and every factor goes in the note (principle 7).

### 3.2 Her points (file frame, metres)

Gwyn's figures were measured on the held crops (`PAG3828-crop-hull-grid.png`, `-masts-grid.png`,
`-settee-grid.png`, and a crop of the stern view from the large image), ±10 px a point, about
±0.3 m at her scale; Bil §2.3's own figures where it gives them. B4 re-measures each with a checker
(§3.6). The collier's lines replace the judged points below the water at step 1; the points given
for them here are the fallback, kept only if a row cannot be read.

| Line | Points | Source; mark after step 1 (until then) |
|---|---|---|
| `rail_m` | (−11.52, 3.30), (−8.00, 2.95), (−4.03, 2.49), (−3.93, 1.75), (0.12, 1.65), (4.00, 1.72), (7.57, 1.90), (10.00, 2.30), (11.52, 2.65) | The waist 1.65 (Chapman, 5.3-5.5 ft, S†). Above it Gwyn's rise: the quarterdeck's rail 0.84 m above the waist rail at its break and 1.65 m at the taffrail; the bow 1.00 m at the stem head (measured here). The break about 0.32 of the length from the taffrail, abaft the main shrouds (Bil §2.3). The taffrail and stem head each 2½ ft beyond the water's ends, half Chapman's 5.0 ft of overhang between them (the split judgement until measured, §3.6 task 5). Chapman's own sheer, read roughly on the grid crop, rises 2.7 ft forward and 3.6 ft aft: the check. `stand-in` |
| `breadth_m` | from the collier: the half-breadths at her load line and at the top-timber line by station, lengths × 0.92 (provisional, §3.4), breadths × 0.847. Fallback: (−10.50, 0.30, 1.80), (−8.00, 1.95, 2.35), (−4.00, 2.78, 2.80), (0.50, 2.95, 2.85), (4.00, 2.88, 2.82), (7.50, 2.35, 2.55), (9.80, 1.10, 1.90), (10.60, 0.25, 1.30) | The collier's half-breadth at the water is printed nowhere and is computed from its diagonals at the load line, as the pages note computed the sloop's (§5.2 there). The stern's rail half-breadth between Gwyn's stern view's 1.55 m at the taffrail and 2.05 m at the wale (measured here). `stand-in` (fallback `judged`: a trader's full ends, the greatest section a little forward of the middle, 0.10 m of tumblehome) |
| `keel_m` | level at the collier's depth scaled: (−10.40, −2.77), (9.60, −2.77) | The collier floats level, 10 ft 9 in afore and abaft (Folio I, read here); 10 ft 9 in × 0.847 = 9 ft 1 in. Her file's draught, 3.51 m, is recorded beside it, never moved (principle 7; §3.4). `stand-in` (`judged`) |
| `stem_m` | (10.20, −2.50), (10.60, −1.30), (10.76, 0.00), (11.15, 1.40), (11.52, 2.65) | Below the water the collier's stem, scaled (to read); above it a bluff merchant's stem raking 2½ ft forward to Chapman's stem head (judgement on Chapman's overhang until §3.6 task 5 measures the stem's fore edge). `judged` until both are read; then `stand-in` |
| `stern_m` | (−10.40, −2.77), (−10.62, −1.30), (−10.76, 0.00), (−11.15, 1.20), (−11.40, 2.20), (−11.52, 3.30) | The post raking about 7° to the water (the collier's post below, to read), then the round counter to the taffrail (Gwyn's stern view, at Chapman's overhang). `judged` until read; then `stand-in` |
| `wales_m` | (−10.00, 0.62, 1.20), (−4.00, 0.36, 0.95), (0.12, 0.30, 0.89), (4.00, 0.37, 0.96), (10.00, 0.95, 1.54) | Gwyn's dark band, 0.76 m below the drawing's waist rail to its top and 0.59 m broad (measured here), hung from Chapman's rail and carried along the sheer. The collier's Folio VII (cached right leaf `_0501`) the type's check. `stand-in` |
| `section_m` | the collier's dead flat, scaled by 0.847. Fallback `g.midship_section(half_breadth=2.96, breadth_z=0.0, depth=2.77, deadrise_deg=6.0, bilge_m=1.4, tumblehome_m=0.12, rail_z=1.65)` | The dead flat's main half-breadth 11 ft 3 in moulded, 11 ft 5½ in with the plank, gives 2.96 m, her half-beam; its heights of breadth fall about 0.2 m below to 0.5 m above her water (judgement on the keel's depth below the base, to read on Folio I). Above the water her side is fitted to Chapman's rail (principle 7). `stand-in` (`judged`) |
| `decks_m` | `upper`: (−11.20, 1.45), (−4.00, 1.00), (0.12, 0.92), (4.00, 0.99), (7.57, 1.17), (11.20, 1.85); `quarterdeck`: (−11.20, 2.80), (−4.03, 2.25) | The upper deck the waist rail less 0.73 m along the sheer (judgement; the collier's Folio XXXII the check); the quarterdeck at Gwyn's planksheer, a light rail on stanchions above it (measured here; the deck judgement), raised about 1.25 m above the upper deck at its break. `judged` |
| `ports_m` | `upper`: (1.00, 1.34, 2.92), (4.00, 1.40, 2.86) | The armed fit's two ports a side in the waist (§5.2): sills the deck + 16 in (judgement after the *Raven*'s, Steel 1805 p. lix); half-breadths at the sill from the collier's sections at those stations, scaled (to read; the fallback from `breadth_m`), never from the drawing. `judged` |
| `port_size_m` | `upper`: [0.50, 0.30] | Cut down from the rail, which they must not reach; the brigantine's Folio XXXII (cached `_0551`) the check (§3.6 task 7). `judged` |

**Shape keys** (stage 0H; written through `g.hull_profile` and `g.hull_form`):

| Key | Figure | Source; rung and mark after step 1 (until then) |
|---|---|---|
| `head_m` | (10.90, 0.50), (12.40, 1.80), (13.00, 2.70) | Gwyn's knee and figure, reaching about 1.5 m beyond the stem head (measured here). Chapman's "overall to the head", 83 English ft (Bil §2.4), would put it 2.3 m beyond: the check, recorded. S†, `stand-in` |
| `breadth_line_m` | the collier's upper height of breadth and main half-breadth by station, through `g.from_steel_table(rows, length_ratio=0.92, beam_ratio=0.847)`, the length ratio as §3.4 settles it at step 1 | S†, `stand-in` (not written until read: the default rule draws the main breadth) |
| `sections_m` | the collier's diagonals by station, through the same call | S†, `stand-in` (not written until read) |
| `channel_wales_m` | not written | Gwyn draws channels with deadeyes and no separate channel wale |
| `floor_m` | the collier's rising line and rising half-breadth by station, if transcribed | S†, `stand-in`. Kept by principle 11 ("written wherever a source gives them, drawn or not"); not drawn |
| `rabbet_m` | not written | No siding is read for the collier's keel |
| `form.fullness` | [1, 1] | The default rule, filling only beyond the collier's sections (principle 5). T, `judged` (the design's own rule, principle 3). Fallback, if the collier cannot be read: [1.3, 1.3], a trader's fuller ends, `judged` |
| `form.stern` | `type: round`; `lights_m: [[1.75, 2.75, 3, 1.10]]` | Gwyn's separate stern view: rounded, three oval windows on a blue ground, a red band below (Bil §2.3, read). The band's heights and spread measured here on the stern view (±5 px), scaled to her taffrail's 3.30 m. The type S, `sourced`; the lights S†, `stand-in`. No `transom_hb_m` (refused on a round stern) |
| `form.head` | `figure` | Gwyn: a figurehead with head rails (Bil §2.3, read). S, `sourced` |

**`marks`**, after step 1: `rail_m: stand-in`, `breadth_m: stand-in`, `keel_m: stand-in`,
`stem_m: stand-in`, `stern_m: stand-in`, `wales_m: stand-in`, `section_m: stand-in`, `decks_m:
judged`, `ports_m: judged`, `port_size_m: judged`, `head_m: stand-in`, `breadth_line_m: stand-in`,
`sections_m: stand-in`, `floor_m: stand-in` (if written), `form.fullness: judged`, `form.stern:
sourced`, `form.stern.lights_m: stand-in`, `form.head: sourced`. A line any of whose points stays
unmeasured takes the word of its weakest point (`judged`), and its note names where along the hull
the weak points are (principle 4).

**Her rungs on §5.0's ladder, in one place.** After step 1: **S** for `form.stern`'s type and
`form.head` (Gwyn, needing no scale); **S†** for `rail_m`, `wales_m`, `head_m` and
`form.stern.lights_m` (Gwyn at Chapman's scale), and for `breadth_m`, `keel_m`, `stem_m`,
`stern_m`, `section_m`, `breadth_line_m`, `sections_m` and `floor_m` (the collier scaled, Chapman
above the water); **R** for nothing drawn (Chapman's rule for the greatest section gives only its
direction, which the collier's table then gives as read); **T** for `decks_m`, `ports_m`,
`port_size_m` and `form.fullness` (the default rule). Until step 1 every line under the water is T,
"to read: Steel 1805 Tables p. 26".

**Carving and paint in words** (principle 9; `Build-Ships.md` §19.1 item 17): Gwyn's blue stern
with a red band, the three oval lights and the rudder; the figure and head rails; **an oval carved
badge on each quarter**, a window-like oval in scrollwork (read here on the hull crop; not in Bil
§2.3); the red ensign on a staff at the taffrail. The badge is carving, not a gallery, so it has no
place among the shape keys and none is asked for.

### 3.3 Why Gwyn's lines are `stand-in` and not `sourced`

Gwyn is her own drawing and the owner's named source. But every figure taken from it rests on
Chapman's scale, and a line takes the word of its weakest point (principle 4). So the shape Gwyn
draws is S and its metres are S†. The stern's type and the head's word need no scale, and are
`sourced`.

### 3.4 The stand-in's scale (§5.0 principle 7; measured here)

- **Lengths** by the waterlines: her 70.6 ft against the collier's about 76 ft 11 in between the
  perpendiculars, **0.92, provisional**. The collier's length is judgement on its stations as read
  (the dead flat 30 ft 0 in abaft FP; timber 4 at 38 ft 11 in afore AP, the after body's room
  2 ft 0 in from timber 4 aft; read here on n484). The room from the dead flat to timber 4 is not
  printed: at the fore body's ⊕ to D, 7 ft 7 in over four rooms, the length is about 76 ft 6 in
  (read here). Folio I gives no length between the perpendiculars for her: row B, the range of the
  deck, is blank, and row C (the stem at the hawse holes, in merchant ships at the wing transom, to
  the post's aft side) is 76 ft 3 in (read here on n488). **A conflict, to settle at step 1:** row
  C runs 1 ft 9 in to 2 ft 6 in beyond the length between the perpendiculars on the sloop (52 ft
  0 in against 50 ft 3 in taken) and the cutter (80 ft 6 in against her stations' 78 ft 0 in)
  (`pages-steel-1805-bodies.md` §4, §5.1, §6). By the sloop's method, row C less the stem's
  moulding and the post, the collier's length is about 74 ft and the ratio about 0.95, against
  0.92 from the stations. B4 reads Folio II's stem moulding and Folio IV's post for her (§3.6 task
  1) and says which length is taken. If it is not 76 ft 11 in, the ratio, `breadth_m`'s stations,
  `breadth_line_m`, `sections_m` and the drawn displacement are written again on it, with 0.92's
  figures beside the new in the note (old beside new).
- **Sections** by one factor, her beam against the collier's extreme breadth: 19.4 / 22.92 =
  **0.847**, so the collier's floor, tumblehome and flare keep their angles.
- **Her side above the water** from her own source, Chapman's 1.65 m, and the sheer's rise from
  Gwyn's (her type's drawing wins over the stand-in's).
- **The drawn depth is recorded, never moved:** the collier's 10 ft 9 in × 0.847 = 9 ft 1 in,
  **2.77 m, 0.73 m short of her file's 3.51 m** (0.58 m short of 11 ft, had 11 ft been taken). The
  drawn displacement goes in the notes beside the filed 229 t, and is reported if it falls more
  than 15% short (principle 8).
- **A check, not used:** the collier's top-timber line at the dead flat, 16 ft 4 in above the base,
  stands about 6 ft above its load line (judgement on the keel's depth below the base: about half
  the keel in a merchant ship, by Folio I's note as the pages note reads it, §5.1 there). Scaled, it
  is about 1.57 m above her water, against Chapman's waist rail at 1.65 m.

### 3.5 What the drawing must show her to be

- **Distinguishable** (principle 1; the pair check of `Build-Ships.md` §5.6). She is no class in
  two roles. Her nearest are the brig and the merchant brig; normalised to one length, beam,
  freeboard and draught, she differs by the step of her raised quarterdeck, her round stern with
  three lights and her strong sheer aft. Her waterline of 3.6 beams against *Harpy*'s 3.1 is
  equal by construction once normalised, so it counts only in the one-scale picture beside the
  merchant brig (§13.1). Measured with SW-2b.2's check (`tests/test_profiles.py`, B8's) at her
  first commit if it is in; if her window opens first, B4 measures her against the brig by the
  same method in a scratch script and reports the figure.
- **Her masts sit true:** the drawn hull is her file's length and beam (principle 7).
- **Port triples:** her two judged triples are not in `measured`; their gaps to the drawn side
  are reported by `g.hull_form` (§5.3 there). No triple is written from the drawing.

### 3.6 B4's measuring tasks (step 1)

On the held images and the cached pages, by the research's method (registered grids, a checker),
with scratch scripts outside the repository. The figures go in; the images never do.
1. **Steel 1805's brig collier:** the whole bodies table, Tables p. 26
   (`reference-cache/steel-1805-collier-brigantine/elementspractice00stee_n484_w1600.jpg`),
   transcribed as the pages note transcribed the sloop's (`pages-steel-1805-bodies.md` §3.3), the
   rising line and its half-breadth included; its Folio I column (n488): the length between the
   perpendiculars against its stations and against row C (§3.4's conflict), the keel's depth, the
   load line on the base; the collier's columns of Folio II (the stem moulded and sided) and
   Folio IV (the post and the wing transom), on leaves not yet fetched (new leaves of the same IA
   item, into the same cache folder); the collier's columns of Folios VII (the wale), XXXII (the
   deck above the rabbet, the waist), LI (the stern) and LV (the sheer rail) on the cached right
   leaves (`reference-cache/steel-1805-bodies/elementspractice00stee_0501.jp2`, `_0551`, `_0589`,
   `_0597`); its drawn displacement at its load line, scaled. B4 hands the transcription over as
   text; the session files it as a new note, `docs/design/ships-design/pages-steel-1805-collier.md`,
   facts only, in its docs commit at her stage A (§1.1). B4 owns no doc (`Build-Ships.md` §4.1),
   and the existing pages note keeps its three ships.
2. **Gwyn's rig** (D6 (e)): every height of §4.1's table, as a share of the rail length from the
   waist rail; the fore top and the fore cap, which Bil §2.3 does not give.
3. **Gwyn's hull:** the quarterdeck's break and its rail, the sheer at the bow and the stern, the
   wale's band, the head's reach, the stern view's lights and half-breadths, the side steps' place
   (for the record).
4. **Gwyn's settee:** the tack's height above the rail, and where the drawn yard crosses the main
   mast. Three readings stand: Bil §1.2's 32 px below the top (0.94 m at her scale), about 1.4 m
   (the fidelity draft), and about 67 px (1.97 m; the buildability draft). Each is judgement until
   measured; the measure is recorded beside D5 (a)'s 2.33 m (§4.4), and the cut does not move.
5. **Chapman's No. 5:** the taffrail's and the stem head's x against the waterline's ends (the
   overhang's split); the sheer; the stem's fore edge; the post; the bowsprit's heel; whether a
   quarterdeck rail is drawn; whether a staysail is drawn between the masts.
6. **Adye 1804 p. 155,** the 3-pounder's lengths and weights (IA leaf n178, the page image Ind §6.4
   read), appended to `period.py` with its page.
7. **Steel 1805's brigantine of 10 guns,** Folio XXXII (cached `_0551`): the port's size and its
   sill above the deck, as the check on her waist ports.

Until a point is measured it is written as judgement in its note, never left out.

**The pages' row.** The cache folder `reference-cache/steel-1805-collier-brigantine/` (n474, n484,
n488; the item's rights as for `steel-1805-bodies/`) gets its sentence in
`docs/references/README.md`'s paragraph at l. 53, in the commit that files this design (the lead's
rule of 2026-10-28: nothing filed without its row).

---

## 4. The rig

### 4.1 Masts and yards (D6 (a) with (e))

Heights above the water: Gwyn's shares of the rail length, laid from the waist rail (§1.4). "Bil"
figures are Bil §2.3's; the rest were measured here on the masts crop and are B4's to re-measure.
Yards: Chapman's, at twice the drawn length (Bil §2.4, measured).

| | Fore | Main | Source |
|---|---|---|---|
| Station; rake | +7.57 m; 0° | −1.94 m; 2.8° aft | Chapman (S†) |
| Lower yard | 8.01 m (0.276) | the dry yard 8.40 m (0.293) | measured here |
| Top | 9.23 m (0.329) | 9.71 m (0.35, Bil) | Gwyn |
| Lower cap; `height_m` above 0.92 | 10.77 m (0.396); 9.85 | 11.44 m (0.425); 10.52 | measured here |
| Topsail yard hoisted | 15.01 m (0.580) | 16.23 m (0.633) | measured here |
| Topmast cap; topmast `height_m` | 17.06 m (0.669); 6.29 | 18.26 m (0.721); 6.82 | measured here |
| Topgallant yard | 18.93 m (0.750) | 20.86 m (0.834) | measured here |
| Truck; topgallant mast with its pole | 21.23 m (0.85, Bil); 4.17 | 23.54 m (0.95, Bil); 5.28 | Gwyn |
| Lower yard length | 12.44 m (40.8 ft; 0.578 of the waterline) | the dry yard 12.44 m | Chapman (S†); the dry yard by the Tractat's rule for brigs, the main yard the fore's (Chapman 1781 p. 102, read, Bil §2.4): R |
| Topsail yard | 9.14 m (30.0 ft) | 9.36 m (30.7 ft) | Chapman |
| Topgallant yard | 6.13 m (20.1 ft) | 6.13 m (20.1 ft) | Chapman |

- **The dry yard's length and its checks.** Chapman's brig rule gives 40.8 ft (R, above). The
  check is by judgement: the 64's crossjack to her mizen topsail yard (Steel 1794 p. 49, 57 ft 6 in
  over 43 ft 3 in; Indf §4.2, read there on the page image), carried to her dry yard and her main
  topsail yard, 30.7 ft, gives 40.8 ft (measured here). That analogy is this design's, not a rule
  of Steel's. Steel 1794 I p. 40's own rule for a ship's crossjack is the fore topsail yard's
  length (read on the page image with a checker, `Research-74-2026-10.md` §5.3; the OCR at l.
  4521-4525 is garbled there). For her it would give 30.0 ft. It is **not taken**: a dry yard
  shorter than the main topsail yard above it (30.7 ft) cannot spread that sail's foot, and in a
  ship the fore topsail yard the rule names stands far longer than the mizen topsail yard the
  crossjack spreads (judgement). On No. 5 the main topsail's clews come down about 34 ft apart, and
  Chapman draws no dry yard (Bil §2.4): the drawing's, recorded.
- **No royals and no royal masts** (D40 (a): no drawing has a royal). The topgallant masts carry
  their poles to the trucks. The brig's files file a royal mast; hers do not.
- **The dry yard** is filed as the frigate's crossjack is (`frigate-36.yaml` l. 206-207): a `yard`
  with no sail, braced, spreading the main topsail's foot. Id `main.crossjack.yard`, read as a lower
  yard by `orders/verbs.py`'s `_yard_kind`; aliases "crossjack", "cross-jack yard", "dry yard".
  Steel 1794 I's BRIG article: English brigs carry a crossjack yard and no main yard (OCR l. 24728,
  the lead's reading in D40). "Main yard" is the settee's yard's alias (§4.4), so the dry yard is
  not called so.
- **Gwyn's rig is low** beside Chapman's (the main top 0.35 of the rail length against Chapman's
  0.53: D6 (e); Bil §2.5). Her lower masts are about 4.6 m shorter than No. 5's. That is the
  owner's choice of heights (D6 (e)), and her sail plan follows from it.
- **Brace limits:** the brig's, level for level (`brig.yaml`, read here): the fore yard 60°, the
  fore topsail yard 62°, the fore topgallant yard 64°; the dry yard 62°, the main topsail yard 64°,
  the main topgallant yard 66°. The brig is her comparator in 7-197, so the same limits test her
  sails, not her braces (judgement; no source gives hers). Her fore yard is 2.1 breadths, the
  frigate's ratio (`gen_ships.py:6115-6118`), so the brig's reduction "for a short ship whose lower
  yards are long for her breadth" holds for her too (judgement). The settee's yard is not braced
  (Ext E3: `is_yard` is true for `yard` alone); its trim is its sheet's.
- **Rope:** the brig's (`BRIG_ROPE_SCALE`) by √(her plain sail ÷ the brig's 766 m²), √(380 / 766),
  about 0.70 (measured here; judgement, Indf §4.2's method), so a line's rating grows with the sail
  it works. Spar ratings from the rating pass (`PEAK_COEFF["lug"]` 1.29 for the settee).

### 4.2 The square sails and the head

- **Cut between their yards as the spars stand**, by the brig's rules (`gen_ships.py:6064-6104`: a
  course 0.42 of its yard deep; the upper sails' heads 0.82-0.89 and feet 0.9 of their yards).
  Measured here (±10%): fore course about 58 m², fore topsail 65, fore topgallant 27; main topsail
  74, main topgallant 32. **Canvas** by the brig's table (Steel 1794, by sail); **reefs** as the
  brig's. The fore course's foot stands 2.79 m above the water, 0.89 m clear of the rail at the
  fore mast (checked at generation, §1.4).
- **The main topsail sheets to the dry yard's arms** (Gwyn; Lescallier Pl. XVII fig. 7 and Pl. XXII
  fig. 8; Bil §2.6, read). **Plainly:** so it is wider at the foot than Chapman's drawn sail, whose
  clews come to the top 34 ft apart; D40 (a) takes Gwyn's.
- **Headsails:** the fore topmast staysail and the jib on the jib-boom (Gwyn, read), cut by
  `stay_sail_cut` on her own stays. About 50 m² together by the fidelity draft's estimate (±25%);
  about 63 m² by rough triangles on her stays (measured here). **Their cut decides 7-197's beat's
  margin** (§9). No flying jib, no fore staysail: Gwyn draws neither.
- **Bowsprit:** Chapman's, 28.5 Swedish ft outboard at the stem head (8.46 m), steeved about 29°;
  the jib-boom 15.3 ft beyond the cap (4.54 m) (Bil §2.4, measured). S†. Heavier than the Tractat's
  rule (22.9 ft outboard), recorded in its note. Its heel at the stem head, x +11.52, 1.73 m above
  the datum; its cap about x +18.9, 6.75 m above the water (measured here). Inboard a third of its
  length (the frigate's Luce rule, judgement) unless Chapman's heel measures (§3.6 task 5).

### 4.3 The spritsail yard (D8 (b)): settled, a sail bent

- **The yard** by B1's `spritsail_yards.py`, the spritsail yard alone, as the razee takes it: class
  `yard` on the bowsprit, at the station the module's rule gives near the cap (Steel 1794 I pp.
  196-197), no halyard; braces, lifts, sheets, clewlines and buntlines by `square_sail_lines`; ids
  `spritsail.yard` and `spritsail` (Ext §4.1).
- **Its length:** 9.14 m (30.0 ft), **the fore topsail yard's**, by Steel 1794 I p. 40's rule
  for the Royal Navy, "cross-jack and spritsail yards as the fore topsail yard" (read on the page
  image with a checker, `Research-74-2026-10.md` §5.3). R. The check: Steel p. 49's 64 column has
  the spritsail yard and the fore topsail yard alike at 57 ft 6 in (Indf §4.2, §4.6, read there on
  the page image). A King's rule carried to a trader (judgement).
- **Evidence for the yard:** Steel 1794's Plate 1 (the bilander, read) and Lescallier's bélandre,
  Pl. XXII fig. 8 (read) (Bil §2.6). Gwyn's spar under the bowsprit is the lead's reading only and
  is not counted (D8).
- **The sail is bent** (`bent: true`, so it starts the voyage furled on its yard): square, cut by
  the module's rule to a metre above the water (about 40 m², measured here), in the groups
  "spritsails" and "all sail" (Ext §4.1's two), **never** "plain sail", "courses", "headsails",
  "jibs" or the code's "occasional sails". So the polar, the far ships and every captain's "plain
  sail" never set it. Hove to it is clewed up; `shorten sail` takes it in first (Ext §4.2's places 7
  and 8, B3.2's). Aliases "spritsail", "the spritsail yard". **"Occasional", said:** the owner's
  answer for the razee, "an occasional sail kept out of plain sail" (Dec, the razee's answer to
  D8), is read in the period's sense, a sail set now and then in light fair winds. In the code the
  group "occasional sails" means the sail room's own canvas: its members are written unbent and
  stand outside "all sail" (`gen_ships.py:986-992, 2196-2201` at this head; `parts.py:363`; the
  *Indefatigable*'s module, working tree, the comment on its groups). A bent spritsail in that
  group would mix the two, so it is not put there. **Why it is not asked:** whether a sail is bent
  is hers to settle (Ext §4.1; §13.3 there), the owner's answer for the razee is the same case, and
  the owner judged spritsails "a reasonable thing to try for" (D8). Her polar, her plain sail and
  the captains' handling are the same with the yard bare. If the lead reads the owner's
  "occasional" as the sail room, the sail is written unbent and put in "occasional sails" alone,
  out of "all sail", and nothing else moves.
- **No sprit-topsail yard.** No drawing of her type shows one (Bil §2.6).

### 4.4 The settee (D5 (a); Ext §5.1)

**The cut** (`settee.py`; measured here; heights above her datum, x forward of midships):

| Figure | Value | Source |
|---|---|---|
| Yard (`main.lug_yard`) | 16.59 m: 0.72 of the rail length | Gwyn, 564 px of 785 (Bil §2.3); D5 (a) |
| Head | 15.67 m: 534 px of 785 | Gwyn (Bil §2.3) |
| Head to the horizontal | 44° | Gwyn; Falconer 1780 and Röding I col. 304 about 45° (Bil §1.1) |
| Leech, foot | 11.29 m each, 0.72 of the head | D5 (a) |
| Luff | 1.81 m, 0.16 of the leech | D5 (a); Steel 1794 I p. 136's boat rule 0.20 (Bil §1.3) |
| Tack | x +1.54, 1.03 m (0.30 m above the waist rail, under the throat) | Gwyn's tack just above the rail, 0.57 of the length from the taffrail against Gwyn's 0.58 (measured here); the luff upright under the throat, as the fixture cuts it (`tests/rig_fixtures.py:361-381`) |
| Throat | x +1.54, 2.83 m | |
| Sling, a third along throat→peak | on the main mast's raked line, 6.46 m (7.38 above the water) | D5 (a); Ext §5.1's contract, within 0.1 m |
| Peak | x −9.73, 13.72 m (14.64 above the water) | 1.79 m inside the taffrail, 0.078 of the length; Gwyn about 0.09 ± 0.02 (Bil §2.3) |
| Clew | x −9.66, 2.43 m | where the foot from the tack meets the leech from the peak: 1.86 m inside the taffrail, about at Gwyn's quarterdeck rail, where the drawn clew is (measured here) |
| Area; centre | 73.3 m²; x −5.43, 6.67 m above the water | `_quad_area_centroid` on the corners; the centre above the water (Ext §5.1: the trial's fault mended) |
| Reef bands | 1, a fifth of the leech up, parallel to the foot | D42 (a) |
| Canvas | the brig's mainsail's number | Steel 1794 p. 119 as the brig cites it; a vessel's mainsail of the heavy numbers (Bil §1.3, judgement) |

- **The yard against Gwyn.** Slung at a third with the tack at Gwyn's height, the yard crosses the
  mast 2.33 m below the main top and 1.02 m below the dry yard. Gwyn's drawn crossing is higher
  (three readings, 0.94-1.97 m below the top: §3.6 task 4), with 0.36-0.40 of the yard before the
  mast. **Plainly:** that is D5 (a)'s third against Gwyn's 0.395 (D5 (b) not taken). The measured
  crossing is recorded in her note; the cut stands on D5 (a) and Gwyn's tack.
- **The yard is longer than the head** by 0.92 m, as Gwyn draws it (564 against 534 px), split
  between the two ends (judgement). If the drawing needs the yard to span the head exactly, as the
  fixture's does, B5 says so and the yard is cut to the head, recorded.
- **Against Chapman.** Chapman's settee is 92 m² ±8% on a 12.45-m yard at 35° (Bil §2.4). Gwyn's
  near-triangle on a longer, steeper yard gives 73 m² on her. The sail is the owner's choice (D5
  (a)); the difference is recorded, not tuned away.
- **Lines** (Lescallier p. 390, Pl. XVII fig. 7's letters; Bil §1.2; Ext §5.1): the jeers a
  `halyard` of the yard; the derrick (*martinet*) a `lift`; the peak brace (the English vangs) two
  sided `vang`s; the ourses (the English bowlines) two sided `guy`s; the tacks two sided `tack`s of
  the sail; **one unsided `sheet`** to the taffrail; two clewlines and a buntline. Ratings by
  `rope_kn` on the brig's sizes for the like lines, scaled (§4.1).
- **Roles** `yard` and `mast`; `dipping: true`, `settee: true` (Ext §5.1; the schema refuses the
  key without them, stage 0E). The yard's `height_m` is the sling; its `length_m` the yard's.
- **Groups:** "courses" with the fore course, "plain sail", "all sail"; never "gaff sails" (Ext
  §5.1, E15). **Aliases:** "mainsail", "main sail", "the mainsail", "settee", "the settee" →
  `main.settee`; "main yard", "settee yard", "lateen yard" → `main.lug_yard` (Falconer 1780, YARD:
  "the bilander's main yard", Bil §1.1).
- **`settee.py`'s checks** (Ext §9.3), each a `ValueError` with a sentence: the point a third along
  throat→peak more than 0.1 m off the main mast's raked line at its height; the peak or the clew
  abaft the taffrail; more than one sheet, or a sided one; a corner's ratio more than 0.01 off D5
  (a).
- **No driver and no spanker.** She has no after sail but the settee, and the gale takes it in at the
  third reef through "courses" (Ext §5.8).

### 4.5 Staysails, storm canvas, groups and aliases

- **Between the masts: the main topmast staysail only**, on her main topmast stay, written with
  `g.stay_sail_cut` and `g.staysail_from_cut` as `between_the_masts` writes the brig's, **bent**
  (`bent: true`), out of "plain sail" as the brig's is, its foot above the settee's yard (judgement;
  checked at generation, §1.4). **Its source:** Lescallier pp. 402-403 give the brigantin, of which
  the bilander is a variant, a ship's square sails, "staysails and jibs", but for the main's dry
  yard (Bil §2.1, read (OCR)); which staysail she sets between the masts is judgement. Gwyn draws
  none there (Bil §2.3); Chapman's No. 5 reports "jib and staysails" (Bil §2.6), the check, to be
  read at §3.6 task 5. **No main staysail:** its foot would lie across the settee's fore part, from
  the yard's fore end at 3.75 m above the water to the mast (judgement). No middle or topgallant
  staysails: no drawing shows them.
- **"Lying-to staysails":** the main topmast staysail (judgement; read by `orders/storm.py:75-80`
  and `evolutions/scripts.py:4663`). It must be bent: the lie-to takes a lying-to staysail only
  furled, loosed or in the gear (`scripts.py:4660-4666`), so an unbent one would leave her lying to
  with no staysail. The brig's, the main staysail, is bent and in no occasional group
  (`brig.yaml`'s groups). B4 checks the lie-to with it.
- **Storm canvas:** the fore and main storm staysails, the brig's pattern (judgement). The main one
  should only ever stand in the settee's place: the gale takes the settee in with the topsails'
  third reef (Ext §5.8), and `orders/storm.py`'s `_replaced` takes the after sail in as a storm
  staysail abaft the foremost is set, if B3.3 counts the settee among the after sails there. B4
  checks that order on her file, and B5.4 that the drawing shows the storm staysail under the
  settee's yard aloft; if either fails, the main storm staysail is left out, said. No storm
  trysail: she has no gaff.
- **Groups,** with the names the engine reads: "plain sail" (fore course, fore topsail, fore
  topgallant, main topsail, main topgallant, the settee, the fore topmast staysail, the jib),
  "courses" (the fore course, the settee), "topsails", "topgallants", "headsails", "jibs",
  "staysails" (the fore and main topmast staysails), "staysails between the masts" (the main topmast
  staysail), "storm canvas", "storm staysails", "lying-to staysails", "spritsails" (the spritsail),
  "square sails", "fore-and-aft sails", "all sail" (plain sail with the spritsail and the main
  topmast staysail), and the yard groups: the head yards the fore's and the spritsail yard (B3.2's
  place 2); the after yards the main topsail, topgallant and dry yards. The settee's yard is in no
  yard group.
- **Aliases** in the period's words, the brig's where they fit (`brig.yaml` l. 1758-1788), with
  "mainsail" the settee's and no spanker, gaff or boom; "foresail", "fore yard", "head sails",
  "sails".
- **Mast ids `fore.` and `main.`** (`Build-Ships.md` §4.4).

---

## 5. The guns

### 5.1 The fits

| Fit | Guns | Source |
|---|---|---|
| **"unarmed"** (default) | none | The brief item 3; `armament.default: unarmed` (stage 0; `schema.py:241`) |
| **"armed merchant"** | four long 3-pounders, two a side in the waist (Nos. 1-2), and four half-pounder swivels on the quarterdeck rail, two a side | D41 (a): Elizabeth, 130 tons, "4-3 P.", four 3-pounders of the common construction, Lloyd's 1779 and 1782 (Bil §3, read on the row images). The swivels: no British source counts a bilander's (Bil §3); four is the privateer schooner's provisional figure, judgement |

Her armed fit's note names the register's other bilanders, Kerrison's six 4-pounders and Essex's
two 2-pounders (Bil §3), as the degrees a scenario editor may reason within; neither is a fit.
**Plainly:** the brief's "as the merchant brig's" is read as the pattern of a few small guns, not
the merchant brig's 6-pounders (D41).

### 5.2 Places, ports and heights

- **The 3-pounders** by `g.broadside_pair` at x +4.00 and +1.00, in the waist between the fore
  chains and the main mast (judgement), `deck="upper"`, `round_to=0.01`; then `x_m` and `height_m`
  set to their ports' triples to the centimetre (Indf §5.2's means).
- **Their ports** (§3.2): cut in the waist bulwark, sills the deck + 16 in (0.41 m), 1.34-1.40 m
  above the water (the deck 0.936 m at x +1.00 and 0.99 m at x +4.00 on `decks_m`; measured here),
  0.30 m deep, below the rail (judgement after the *Raven*'s sills, Steel 1805 p. lix). **The ports
  are invented for the fit, not seen:** Gwyn draws none, since the drawing shows her unarmed.
  Package 75 draws no port (81's); 81 would draw these triples on her side in every fit. This is the
  owner's question 1 (§17), with the open-rail way beside it. **Plainly:** `PORT_SILL_M`'s 0.6 m
  (`gen_ships.py:3715`) is not used; her bulwark is lower than that.
- **The swivels** on Gwyn's open quarterdeck rail at x −5.50 and −9.00 (judgement), place `rail`, by
  one call, `g.swivels(4, [-5.50, -9.00], 0.0, deck="quarterdeck", round_to=0.01)`, so that the ids
  run `swivel.1.*` and `swivel.2.*` once (the helper numbers from 1 within a call and takes one
  `height_m` for every gun: `gen_ships.py:3899`). Then each swivel's `height_m` is set to the rail's
  height at its own x on §3.2's `rail_m`, `round(interp(rail_m, gun["x_m"]), 2)`, which is
  `rail_at`'s rule (`freesail/ship/profile.py:41`; `Build-Ships.md` §5.3: swivels take
  `rail_at(profile, x)`), as the 3-pounders' heights are set to their triples (Indf §5.2): 2.66 m at
  x −5.50 and 3.05 m at x −9.00 (measured here), since her quarterdeck rail rises aft. A swivel has
  no port (`Build-Ships.md` §5.1).

### 5.3 Weights, crews and the magazine

| Piece | Weight | Crew | Source |
|---|---|---|---|
| Long 3-pounder | Adye 1804 p. 155, to read (§3.6 task 6); until then the shared table's 7 cwt, from memory (`LONG_GUN_CWT[3]`, `gen_ships.py:3677`) | 3 | Falconer 1780, QUARTERS (`period.FALCONER_CREW[3]`), by the owner's rule for the new ships' crews (D31 (c); the 74's answers) |
| Half-pounder swivel | 0.5 cwt (`SWIVEL_CWT`, read not edited) | 1, from whoever is spare | the house's |

- **Magazine:** `fit_magazine` with `MERCHANT_ROUNDS` (20 round and 4 grape a gun) and
  `SWIVEL_ROUNDS` (40), judgement as the merchant brig's. The charges by `charge_lb`, which reads
  Table No. 29 once SW-1 is in (`Build-Ships.md` §10: the 3-pounder 1 lb, the half-pounder swivel
  2 oz). No exercise allowance: a King's fit only.
- **Filling:** `filling_party` gives one.
- **Broadside by 70's rule:** 6 lb a side and the swivels' 1 lb (measured here); no truth pins it.

### 5.4 The quarter bill (set against the armed fit, as `Build-Ships.md` §9.1 sets an unarmed default's)

| | Figure | Basis |
|---|---|---|
| Men at one side's guns | 6 (two numbers of three) | Falconer |
| Trimmers | fore top 1, main top 1 | the merchant brig's (`gen_ships.py:4549-4552`); the settee's sheet is her trim |
| Helm | 1 | the merchant brig's |
| Powder | 0: the boy and the cook pass | judgement |
| Filling | 1 | `filling_party` |
| Priority | sail before guns | "A merchantman's weapon is her heels" (the merchant brig's, judgement) |
| Small arms; boarders | 2; 3 | the master's chest; a trader does not board (the merchant brig's shares, scaled) |

**Realism:** with eight men, two of them the master and the mate, she cannot man a side's guns, the
helm and the sails together. B4 measures `Quarters.beat` at muster on the armed fit and records
which guns fill; the expected answer is one gun or none, recorded as the period's numbers give it,
not forced.

---

## 6. The company and the people file

### 6.1 Eight (D43)

| Station | Count | Basis |
|---|---|---|
| Posts | 2: the master, the mate | the smack's (`data/people/smack.yaml`); a trader of 130 tons |
| Fore top | 2 | Ext §5.1: the main top two at least, so the fore's alike (judgement) |
| Main top | 2 | Ext §5.1 and risk 10: the settee's loosing and furling aloft are the main top's |
| Afterguard | 1: the boy, the messenger | the smack's and the merchant brig's (judgement) |
| Idlers | 1: the cook | the house's |

- **No forecastle station.** The head sheets and the anchors fall to the fore topmen by the hands'
  ranking, which takes any idle hand after the stations a request prefers (`crew/hands.py:339-344`).
  **Plainly:** a company of eight has no hand to spare for one.
- **Ratings** the merchant brig's (0.70 able, 0.20 ordinary, 0.10 landsmen; judgement).
- **`names: english`** (`data/crew/names.yaml:17`), as the smack's.
- **The settee's requests** are six hands each (Ext §5.3); the short-handed rule begins one with
  half its hands, slower in proportion (`SHORT_HANDED_SHARE`, `crew/hands.py:95`). B4 measures each
  settee request and the square sails' take-in and furl at eight, and records which begin and their
  times (D43; Ext §5.3, §14 items 6-7: the times and hands in TuningNotes with their sources).

### 6.2 The people file (`data/people/bilander.yaml`, hand-written data)

The smack's form: the master (post, the command), the mate (post), the boy (drawn, afterguard,
ordinary, the messenger). The harness's stations: captain the master; officer of the watch the mate;
master the mate. Outlines judgement, bred in the Poole and Newfoundland trade (D26 (b)), naming no
one; a scenario names people by `people:`. Her own test runs `tests/test_wardroom.py:42-57`'s check
on it.

### 6.3 Her name and her notes

`ship.name`: **Hopewell**, the name of a Poole-built bilander (1749) in Lloyd's 1776
(Poole–Sunderland/Memel) and 1779 (Dublin and Poole to Newfoundland) (Bil §2.2, read), taken as a
name of her port and type (judgement). Her note says she is not that vessel (150 tons, built 1749,
lengthened 1756). Whether to reuse a registered vessel's name is put to the
owner (§17). `ship.rig`: "bilander". `era_notes`: an old survivor (D26 (a)); the rig rare by 1769
(Falconer) and "seldom used but by the Dutch" in 1794 (Steel p. 220); the last British bilander
verified in the register 1789 (Bil §2.2); her two burthens (§2.1); her file undated, as the owner
ruled.

---

## 7. Ground tackle, boat, pumps, hold and stores

- **Ground tackle:** `ground_tackle_for(b, 128, 19.4, 11.5)` (`gen_ships.py:499-565`), the merchant
  brig's rule: two bowers of 6.4 cwt by Luce 1866's five to the hundred tons, 9½-in hemp cables, a
  kedge; no sheet or stream under 200 tons (Lever 1808 p. 67, as the generator cites it). **The
  period's check** (read on the held image of Steel 1794 vol. I's anchor table, IA leaf n127): the
  Navy's smallest rows are brigs of 200 tons, three anchors of 12 cwt, and a cutter, three of
  10 cwt; 6 cwt a hundred tons would give her 7.7. **Plainly:** the house rule, later than the era,
  is kept for the two traders alike; Steel's is a King's allowance, heavier than a merchant's
  (judgement); her note gives both. Gwyn's catted anchor (perhaps: Bil §2.3) is a bower.
- **Boat:** one, the long-boat, 18 ft by Luce's rule on 75.6 ft at the small vessel's factor
  (`boat_entries`; measured here), stowed amidships. Gwyn draws no boat (Bil §2.3), which is no
  evidence either way; one boat is judgement.
- **Pumps:** two hand pumps, `pump_entries(0, 2, ...)`, as the merchant brig's.
- **Hold:** `hold_for(b, 128, False, ...)`: 64 tons, half her burthen, the trader's share.
- **Stores** (judgement): water 3 tons (eight men two months at a gallon a day is about 2 tons, and
  some over); provisions 60 days; cordage 80 fathoms; shot plugs 2; a spare topsail yard; the sail
  room a second fore topsail and jib and the storm staysails; the ration `ration_entries(...)` for a
  merchant's articles, which `tests/test_stores.py` asks of every file.

---

## 8. Far description, vessel type and size rank (D16 (a))

**In her file**, through `b.descriptions` in SW-4's form (`Build-Ships.md` §8.1, with `roles`):

| Key | rig | what | roles |
|---|---|---|---|
| `bilander` | "a bilander" | "a bilander, a merchantman under a settee main, deep laden" | `merchant` |

- **"Merchant" in what she is made out to be** (D16 (a)): a cruiser takes her for a weaker mark
  whatever her class (`_weaker`, `world/captains.py:4124-4127`, reads "merchant" in the words), and
  a merchant hull never counts as a superior force (`_overmatched`, `:1857`).
- **The rig word, settled: "a bilander".** The tops make out her rig at `RIG_MADE_OUT_NM`
  (`world/ships.py:97`). Her settee's yard, peaked at 44° high over the stern and the longest spar
  she carries, is the rig's mark, as a lugger's lugs are; the period named the rig on sight
  (Falconer; Steel; Röding I col. 304: it differs from the brig and the snow by its great sail).
  The *Neufchatel*'s word at a distance is "a brig" (D15 (a)) because her rig looks a brig's from
  afar; the bilander's does not. With "a brig" a stranger would rank her 2 until she was made out
  (`size_of_words`, `captains.py:327`, reads "bilander" before "brig", `:315`).
- **No fit word:** her default is unarmed, and a far ship takes a description's fit only where it is
  not her file's default (§8.1 there).
- **Stage 0's registries** hold her already: `SIZE_RANK["bilander"] = 1` and `("bilander", 1)` before
  "brig" in `_SIZE_WORDS` (`world/captains.py:304, 315`); `brains.role_of_vessel` gives her the
  merchant's book by default (`world/brains.py:152-`). Not a man of war.
- **Her rows in `freesail/world/ships.py`, in her window:** `DESCRIPTIONS["bilander"]` (file, rig,
  what) and `_DESCRIPTION_WORDS`: "a bilander", "bilander", "a billander", "billander" (Lloyd's
  key's spelling, "Br, – Billander", Bil §2.2, read). "An armed bilander" and "a merchant bilander"
  resolve by the tail rule (`world/ships.py:281-288`). None of these words is in any text the game
  gives now (grep over `freesail/`, `data/`, `tests/`: "bilander" only in stage 0's registries,
  comments and `tests/test_profile.py`).
- **Vessel type:** `ship.rig: bilander`, served on `/api/ship` as the graph's `rig`.

---

## 9. The polar: what B4 measures and records

**Measure** `polar_of` on her file (`world/ships.py:471-490`): speeds at 8, 15 and 25 kn from 40° to
180°; `closest_deg`; `beat_deg(8)`, `beat_deg(15)` and `beat_deg(25)`; the sailed figure at 90° in
15 kn (speed, heel, helm). Record them in her notes beside these:

**Observed, three probes** (scratch ship files built on the committed `brig_with_settee` fixture,
read by `polar_of`; none is her file):

| Probe | Closest | Beat in 8 / 15 / 25 kn | Best in 8 / 15 / 25 kn | Way to windward in 15 kn at 60° against 70° | Plain sail per t^(2/3) |
|---|---|---|---|---|---|
| The brig, as filed | 50° | 60° / 60° / 60° | 4.57 / 7.92 / 10.97 | (4.26 kn at 60°) | 13.8 |
| **This design's figures**, headsails 50 m² (`final/probe_final.py`) | **50°** | **60° / 60° / 60°** | 3.82 / 6.70 / 9.43 | 1.79 against 1.74 kn: **0.05 kn** | 10.1 |
| The same, headsails 63 m² | 50° | 60° / 60° / 60° | 3.89 / 6.80 / 9.53 | 1.87 against 1.78: 0.09 kn | — |
| The same, headsails 75 m² | 50° | 60° / 60° / 60° | 3.96 / 6.90 / 9.62 | 1.94 against 1.82: 0.12 kn | — |
| The same, headsails 50 m², without the settee | 60° | 70° (15 kn) | — | 1.51 against 1.59: 70° wins | — |
| The same, the settee and headsails alone | 50° | 60° (15 kn) | — | — | — |
| The buildability draft's spars (Chapman ×1.02, heights from the deck, settee 76 m², headsails 75 m²) | 50° | 60° (15 kn) | 4.02 / 6.98 / 9.74 | margin 0.11 kn; 0.002 kn with the brig's headsails scaled down | 10.8 |
| The brig with the settee scaled in length by 1.0 to 0.75 (the fidelity draft) | 50° | 60° (15 kn) | — | 1.84-1.91 against 1.79-1.87 kn, about 2% | about 10.7 |

Read so (judgement on the measures):
- **Rule 1 holds on this design's own figures**, at the bound, by 0.05-0.12 kn of way to windward,
  by the headsails' cut. Her headsails' cut on her own stays decides the margin.
- **The settee is what puts her beside the brig.** Without it, under her square sails and
  headsails, she lies at 60° and beats at 70°. The settee and the headsails alone lie at 50°, a
  point nearer, as the period says lateen sails do (Steel 1794 I p. 237; Lescallier p. 380).
- **She is slower than the brig** by about 1.2 kn in 15 kn: a deep-laden hull under Gwyn's short
  rig, 10.1 m² of plain sail per t^(2/3) against the brig's 13.8. No source gives a bilander's speed
  (Bil §4). Recorded, not tuned up.

**Targets:**
- **Rule 1** (D46; Ext §5.9): `closest_deg` and `beat_deg(15)` no wider than the brig's 50° and 60°
  (truth 7-197). Lateen craft lie a point nearer the wind than square-riggers (Steel 1794 I p. 237;
  Lescallier p. 380: five points against six); with a square fore she would not gain the whole
  point (Bil §4, judgement). So "no wider than the brig" is the claim; "closer" is not pinned.
  `beat_deg(8)` and `beat_deg(25)` are recorded, not pinned.
- **No speed is sourced** for her. Her figures are recorded, not banded.

**The knobs, in this order, each recorded beside its start:**
1. the headsails' cut, only by its sources: her stays as rigged, `stay_sail_cut`'s rule;
2. `clr_x_m` for the helm (no effect on the polar, which has no leeway);
3. `hull_speed_kn` within 9.8-10.8 kn (judgement about D24 (a)'s start, which D24 has tuned by
   truth 1 and her polar).

Never the brace limits without a source. **Realism, not pacing:** if rule 1 fails on her file within
these knobs, B4 reports the figures to the lead and the owner and the clause is not forced. D44 (c)'s
`settee` curve was accepted in advance only for rule 5's failure, so whether it is tried for her
pointing is the lead's (§17, lead item 7).

---

## 10. The lee ports: what her file supplies

- **Unarmed by default,** so she has no line in 7-190 ("every armed file's lowest lee port ... for
  each armed file's default fit").
- **The armed fit's ports** are in her profile (§3.2): sills 1.34-1.40 m above the water,
  half-breadths 2.86-2.92 m. By 70's rule, heel alone (`combat/shot.py:116-120`, `PORT_SHUT_M`
  0.3048 m), the lower shuts at **20.8°**, asin((1.34 − 0.3048) / 2.92) (measured here); with the
  roll, a roll's amplitude sooner (`Build-Ships.md` §7.1). The half-breadth at the sill is the
  triple's, read by SW-5.
- Every port gun's `(x_m, height_m)` equals its triple to the centimetre (the contract, §4.4 there;
  truth 7-185's check). A test in her file checks the armed fit's ports shutting at their heel,
  after SW-5.
- The swivels on the rail have no port.

---

## 11. Where she sails

**Her scenario** (D26 (a) with (b); `Build-Ships.md` §12.2; B6's, after her merge): an old survivor
out of Poole on the passage from Falmouth to Plymouth, on her road home, a summer forenoon early in
1793-1795; a French privateer lugger about (`lugger.yaml` under SW-4's "privateer lugger"
description); a trader in sight. What her file gives B6: the key `bilander`, the file, the fits
("unarmed" the default, "armed merchant"), her date range (undated; the scenario's 1793-95 nearest
the register's evidence, D26), her people file.
- **Her fit there:** B6's scenario names `fit: unarmed` (the schema's word, `UNARMED`,
  `schema.py:241`, which a scenario may name: `ArmamentSpec.fit`, `schema.py:717-723`), as
  `Build-Ships.md` §12.2 has each scenario name its fit. She sails unarmed, a chase; the editor arms
  her with "armed merchant" for a fight. Under D48's third way (the lead's ruling), a command-line
  ship lacking a named fit takes her own default.
- **The table of nations** stands at June 1805 (`data/nations.yaml`). For 1793-95 Britain is at war
  with France and has Spain as an ally (memory, UNVERIFIED until read in James vol. 1). The 1805
  table serves a French lugger; it does not serve a Spanish ship. If B6 names no Spaniard, no
  `nations:` block is needed. If one is carried (stage 0b's, ruled in), its wars cite James by page
  or are marked open (`Build-Ships.md` §12.1; the lead's item 6).

**Built in her own test file, common to any scenario:** she sails her first hour under rules
captains at seed 7 in a world with no named fit (`make_world(7, <her file>, Scenario())`), after
B3.3 (§0), since before it she gets under way as a lugger.

---

## 12. Interfaces

### 12.1 Her stage 0d, exactly

`Build-Ships.md` §3.3 gives her stage 0 "anything beyond stage 0E her design names". **This design
names no new key, hook or registry row.** Her stage 0d is:

1. **At her window's opening** (after B2's merge): the fresh fetch and merge of the lead's branch
   into the package's branch (§2.1 there); the two-way byte test, the golden classing table, the
   0E key probe, and the fast tier if the merge brought code (§3.4 there).
2. **The checks of what she uses**, each shown accepted, by an agent that did not write them:

| Her file writes | Laid by | Checked by |
|---|---|---|
| `settee: true` on a dipping lug with four corners and a mast role | stage 0E (`SailSpec.settee`) | the schema accepting the fixture `brig_with_settee` (`tests/test_rig_classing.py`) |
| `heave_to_aback: true` on `main.mast` | 0E (`SparSpec.heave_to_aback`) | the same fixture |
| `armament.default: unarmed` | stage 0 (`schema.py:241`) | the topsail schooner's load, or a scratch file |
| `deck` on each gun; `hull.profile` with `ports_m`, `port_size_m` | stage 0 (`DECK_WORDS`, `PROFILE_KEYS`) | `tests/test_profile.py` |
| the shape keys; `form.stern.type: round` with `lights_m` and no `transom_hb_m`; `form.head: figure`; `marks` | stage 0H | a scratch profile through the schema; `tests/test_hull_form.py` |
| `g.hull_form`, `g.midship_section`, `g.from_steel_table` | SW-2b.1 | its merge |
| `SIZE_RANK["bilander"]`, the size word | stage 0 (`captains.py:304, 315`) | `tests/test_profile.py:920-936` |
| the stub in `SHIP_MODULES` | stage 0 | writes nothing |

3. **One stage-0 commit,** at the boundary that brings her module (after B3.3's merge):
   `tests/test_profile.py:502-507`, `MODULE_FILES["ships.bilander"]` from `[]` to
   `["bilander.yaml"]`. It lands immediately before her first commit, in the same push, as
   9454fd6 came just before 614d2d4 for B1. Alone it would fail the hook test (the stub writes
   nothing), so the two land together and the hook test runs on the pair. **B4 never touches
   `tests/test_profile.py`.** It is a list, not a pin.

**A precondition, not stage 0d's:** **the 0H guard restated.**
`tests/test_hull_form.py::test_every_ships_spec_round_trips_its_pickle_with_no_shape_key` globs
every ship file and asserts that no pickle carries a shape key (working tree, read here). Her first
commit writes shape keys, so the guard must be restated before it: by B8, who owns
`tests/test_hull_form.py` after 0H (`Build-Ships.md` §4.1), most likely at B1's stage B, which meets
it first (§5.6 there). Named for the lead (§17, lead item 3).

**Plainly:** §3.3 there has the stage-0 agent lay what her design names. Her design names nothing,
so stage 0d is the fresh merge, the checks and the one list's move.

### 12.2 What B3.3 must give her (the contract she relies on; Ext §5)

1. The settee routed to `set_settee`, `take_in_settee`, `furl_settee`, `dip_settee`; reef, trim,
   bend, unbend and shift to the lug's (Ext §5.2-§5.3).
2. Kept off every lugger's path (Ext §5.4): `_lugs_all`, `LugDip`, the heave-to's lowering, the
   storm lug; set after the cast as her after sail; getting under way as a ship.
3. In stays, D3 (b): hauled aft at helm's a-lee, dipped when the head yards' swing ends, the tack
   ended only once it is hoisted (Ext §5.5; `settee_dip_s` 120 s in code).
4. In wearing: lowered at "up helm", hoisted on the new lee once the wind has crossed the stern
   (Ext §5.6).
5. **Hove to, by the lead's ruling on Ext §14 item 3:** the main laid aback by `heave_to_aback`
   (D4 (a)); the settee kept with its sheet eased to `HOVE_TO_DRIVER_APPARENT`
   (`evolutions/scripts.py:1648`), the engine's driver rule, unless the measured figures say
   otherwise, and then clewed up aloft (D4 (a)), with the figures in TuningNotes. B3 measures on
   the fixture and B4 on her file, both ways (Ext §5.7). If her file's figures overturn the
   fixture's, B3 changes the way, keyed on `settee` alone, before her merge.
6. **The sheet's lead (Ext §5.9).** The loose-footed proxy takes a foot of 0.8√A = 6.85 m from the
   tack (`trim.py:278-279, 388`); her cut's foot is 11.29 m, 1.65 times it. The block a fathom abaft
   the proxy's clew then falls at about x −7.1 m, **4.45 m short of the taffrail** (measured here).
   Ext §5.9's trigger ("more than a fathom from it") is met by her figures already, so B3.3 is asked
   to build the reserve branch from the start, keyed on `settee`. **Proposed for B3:** the foot from
   the corners' tack→clew in place of 0.8√A, and the block a fathom abaft the clew and abreast of
   it, as the loose-footed rule has it now (`trim.py:270-279`). On her cut that block stands 0.03 m
   from the taffrail (the clew 1.86 m inside it), so the branch needs no reading of the profile,
   which `Build-Ships.md` §5.6 keeps to the viewer, the lee port and the checks. B4's check proves
   the block within a fathom of the taffrail. **Plainly:** Ext §5.9 (approved) puts the branch's
   block at the taffrail on the centreline. This design keeps the loose-footed rule's block, a
   fathom abaft the clew and abreast of it, so that the trim reads no taffrail from the profile.
   On her cut the two blocks lie within 0.1 m fore and aft and about 1.6 m apart athwartships
   (11.29 m × sin 8°, the foot at the lug's floor; measured here), and B5.4 draws the sheet to the
   centreline (Ext §6.3), so the trim and the drawing differ by that much. The lead chooses between
   Ext's block and this one (§17, lead item 4).
7. The untried manoeuvres (Ext §5.4) run once on her file by B4, since her file comes after B3.3.
   A guard found missing is B3's, keyed on `settee` alone, before her merge.
8. Her drawing (B5.4, Ext §6.3): `lugHoisted` false only while `yard_lowered`; gathered aloft in the
   gear; the sheet to the profile's taffrail; the sling a third along throat→peak.

**For the record, not for B3.3:** the physics' lateral offset for a sail with no boom or gaff takes
half of 0.8√A (`physics/sails.py:1342-1350`), 3.42 m on her settee, where her cut's half-foot is
5.65 m: at a given sheet her centre of effort lies about 40% less far out than her cut puts it. The
physics' equations are not changed (the gate), and the reserve branch does not mend it. Recorded
beside her file, in TuningNotes and for the lead (§17).

### 12.3 What the viewer builder (B5) is asked for

- **B5.1 and B5.6** (`Build-Ships.md` §6): her rail's step at the quarterdeck; the round stern
  closed to the centreline with its band of three lights; the figure on `head_m`; the wale; her
  lower masts' feet on the drawn deck; the bowsprit's heel at the stem head.
- **B5.4** (Ext §6.3): the settee on her corners within 0.1 m when set; gathered under its yard
  aloft in the gear; on deck only while `yard_lowered`; furled aloft; its sheet to the profile's
  taffrail. The dry yard 1.02 m above the settee's sling, drawn without the two crossing.
- **B5.3:** her spritsail under B3.2's drawing (Ext §6.2), its foot above the water in every state.
- **The pictures of the testing report** (§13.1).

### 12.4 What she gives the others

- **To B5 and B8:** a profile in §5.1's form; every port gun on a triple of its deck; every height
  above her water; mast ids `fore.` and `main.`.
- **To B6:** her description key and file, her fits and default, her era note, her people file.
- **To the integrator:** her truths drafted under 7-197 to 7-199 in her own test file, using only
  the names the Hull keeps; her tuning notes as text in her branch's report.

---

## 13. File ownership, and the road

**B4 owns:** `tools/ships/bilander.py`, `tools/ships/settee.py`; `data/ships/bilander.yaml`
(generated); `data/people/bilander.yaml`; `tests/test_bilander.py`; in her window, her rows in
`freesail/world/ships.py` and appends to `tools/ships/period.py`. **B4 never touches:**
`tools/gen_ships.py`; any existing ship file; any doc (the collier's transcription goes to the
session as text, §3.6 task 1); `spritsail_yards.py` unless it lacks the spritsail
yard alone (none expected: the razee takes the same); `freesail/ship/schema.py`; `freesail/` beyond
her `world/ships.py` rows; B3's engine files; `client/*`; `tests/test_profile.py` (stage 0's,
§12.1); `tests/test_hull_form.py` (B8's after 0H); anything under `docs/agents/consent/`. A need goes
back to the stage-0 agent or to B3.

**The road.** Every step ends with `py tools/gen_ships.py <scratch>` from the tree root, a `cmp` of
every committed file against the scratch, and `load_ship` on hers. The fast tier runs once at the
end with the touched files' slow tier, one suite at a time on the owner's machine (`Build-Ships.md`
§2.5).

| Step | What | Proves | Waits on |
|---|---|---|---|
| 0 | Her window opens: the lead's head merged at the boundary; stage 0d's checks (§12.1); her worktree forked | nothing moves (the byte test, the guards) | B2 merged (the owner's direction of 2026-10-29) |
| 1 | The measuring tasks (§3.6), outside the repository; p. 26 transcribed | the profile's, the body's, the rig's and the settee's figures | 0 |
| 2 | In her worktree: `settee.py`; `write()` to the hull, profile and shape keys, masts, yards, square sails, the settee, the head and the spritsail yard, the main topmast staysail, storm canvas, groups, aliases | the file loads, rates and polars; `settee.py`'s checks; `g.hull_form`'s report (drawn displacement and depth; the triple gaps); the pair check | 1; 0H, SW-2b.1, B1's `spritsail_yards.py` (all in at step 0) |
| 3 | Fits, magazine, bill, crew, people file, stores, ground tackle, boat, pumps, hold, descriptions; her `world/ships.py` rows | `Quarters.beat` measured on the armed fit; the wardroom check; the ration; the descriptions resolve | 2 |
| 4 | Her tests; truth 7-197 whole; the polar measured, tuned within §9's knobs, recorded | §14 | 3 |
| 5 | **After B3.3 is merged** (brought into her worktree): the heave-to both ways; the sheet's block; rule 5's measure; the untried manoeuvres; her requests at eight; truths 7-198 and 7-199; her first hour at seed 7. If rule 5 takes D44 (c), B3 adds the settee row as a follow-up step keyed on `settee` (`data/sail_classes.yaml`; `tests/test_sails.py:65-74`, old beside new) before her merge, and her polar, §9's table and 7-197's rule-1 clause are measured again on it, old beside new. Then the stage-0 commit and her commits land on the package's branch | §14; her handling judged by heading and tack a set time after, never by "Tacked" (D13) | B3.3 merged; the 0H guard restated |
| 6 | **The testing report** to the owner (§13.1); the lead's head brought in again; reported done; the lead merges | — | 5; B5.4; B5.6 drawing her file |

### 13.1 The testing report (the owner's direction of 2026-10-29)

In place of holding for the owner's own test, the session sends the owner, with her report:
- **The basics:**
  - her particulars against their sources: 7-197's clauses, each with its figure, band and source;
  - her polar beside the brig's: closest, the beat in 8, 15 and 25 kn, the best in each, the
    speeds at 60° and 90° in 15 kn;
  - her tack and wear at seed 7: the ticks of helm's a-lee, the dip's start and hoist, and when she
    is on the new tack; in the wear, the lowering, the hoist and the wind past the stern;
  - her heave-to's lie both ways at +150 s and +300 s in 15 and 20 kn, and which way B3.3 built;
  - her settee requests at eight: which begin, and their times;
  - `Quarters.beat` on the armed fit;
  - the drawn depth and displacement beside the filed ones;
  - what was taken as judgement, in a list.
- **Pictures in the viewer**, at 800 × 600 in the built-in pane and 960 × 720 for the sheets
  (`Build-Ships.md` §6):
  - abeam to leeward, on the quarter, ahead and astern, furled and under plain sail;
  - the settee set, clewed up aloft (in the gear), lowered in the dip, and furled;
  - the spritsail set;
  - beside the merchant brig at one scale, and the hull alone normalised beside the brig's, with
    her rung letters under it;
  - heeled 10° seen from windward.
- **Her open questions** (§17), if any are still open.

The pictures stay outside the repository, as the owner's sheets do; the figures go into her tuning
notes.

---

## 14. Tests and truths

**Her tests** (`tests/test_bilander.py`; the band form with the source in a comment, as
`tests/test_ship_particulars.py:93-104`):
- the hull block against Chapman and Lloyd's; the profile's points and marks against Chapman, the
  collier and Gwyn; every shape line marked;
- the rig against Gwyn's shares and Chapman's yards (±2%); the settee's cut and contract;
- the spritsail and the main topmast staysail bent, out of "plain sail" and out of "occasional
  sails"; the main topmast staysail the one lying-to staysail;
- the fits (unarmed by default; the armed fit's guns; each port gun on its triple; the swivels on
  the rail);
- the crew of eight with two in the main top; the people file by `test_wardroom.py:42-57`'s check;
- her names resolving (as `test_period_names_resolve`); her description, rank and words; her ration;
  her ground tackle (two bowers, a kedge);
- her polar in `tests/test_ships.py:74-93`'s form with her own measured beam reach ±0.5 kn;
- every settee request begins at her company of eight;
- **the heave-to** (below);
- the sheet's block within a fathom of the taffrail;
- the first hour at seed 7 with no named fit (§11);
- the armed fit's lee ports shutting at their heel, after SW-5.

**The truths** (numbered by `Build-Ships.md` §15), drafted in her test file under their numbers and
moved into `tests/test_known_truths.py` in Phase 5. Each pins states, counts, orders of events,
ticks and bands, never a digest. Each is written against the names the Hull keeps (`world.ship`,
`world.motion`, `world.sea`, `world.clock`), never an `isinstance(..., CrewedWorld)`. Each judges her
by her heading and tack a set time after, never by the "Tacked" line (D13 (a)). Each says that its
rule is carried over from a ship's mizen, the lug or the lateen by judgement (D46). Their ticks are
measured on her file at seed 7 and the bands set from the measure; each docstring gives the
scenario, the source, the figures measured and the machine.

**7-197, her particulars hold their sources, and by the wind she lies as close as a brig** (B4,
measured at step 4, pinned when her commits land; if rule 5 takes D44 (c), the rule-1 clause is
measured again on B3's settee row at step 5, old beside new, before it is pinned):
- LWL 21.5 ± 0.5 m and beam 5.91 ± 0.1 m (Chapman, ±1.5-2 ft and ±1.5%); draught 3.51 ± 0.16 m
  (Lloyd's 11-12 ft); burthen by the old measure 118-130 tons; the waist rail 1.65 ± 0.05 m above the
  water (Chapman 5.3-5.5 ft);
- the settee: luff over leech 0.16 ± 0.02; leech and foot over head 0.72 ± 0.02; the head at 44 ± 1°;
  the yard 0.72 ± 0.02 of the rail length; the point a third along throat→peak on the main mast's
  line within 0.1 m; the peak inside the taffrail by 0.07-0.11 of the rail length (Gwyn 0.09 ±
  0.02, Bil §2.3; hers 0.078);
  `settee` and `dipping` true; one unsided sheet;
- the main top 0.35 ± 0.02, the main truck 0.95 ± 0.03 and the fore truck 0.85 ± 0.03 of the rail
  length above the waist rail (Gwyn, Bil §2.3); the fore yard 12.44 ± 0.2 m, the topsail yards 9.14
  and 9.36 ± 0.2 m (Chapman); a dry yard and no royal (D40);
- the company 8, two in the main top; `heave_to_aback` on the main mast and no other;
- the default fit unarmed; the armed fit four 3-pounders and four half-pounder swivels;
- her description ranks 1 and its what holds "merchant";
- **rule 1:** `polar_of(...).closest_deg <= 50` and `beat_deg(15) <= 60`, the brig's figures at this
  head (Ext §5.9; D46 rule 1; Steel 1794 I p. 237; Lescallier p. 380). On this design's probe: 50 and
  60, the beat by 0.05-0.12 kn of way to windward (§9). If her file does not bear it out within
  §9's knobs, the clause goes to the lead and the owner with the figures; it is not forced.

**7-198, the settee in stays is kept drawing, its ourse to leeward, and dipped last** (B4, on B3.3;
Ext §10.3 item 1; D46 rules 2 and 3; D3 (b)). From close-hauled in 15 and 20 kn:
- at helm's a-lee + 1 tick the settee is set, its sheet within 1° of the lug's 8° floor, and the log
  carries "haul aft the mainsail sheet and brace the ourse to leeward";
- `yard_lowered` is first true at or after the tick the head yards' swing ends;
- it stays true for a band of ticks about `settee_dip_s` (120 s) by her crew factor at eight, and
  `lug_side` passes from the old lee to the new;
- **rule 2 on her own dip** (D46 (d): that the yard is lowered and passed round, "and by how many
  hands"): the hands at the dip, a count of her eight, pinned as measured;
- the tack's end is not before the hoist tick; at a set time after helm's a-lee she is on the new
  tack within a band of close-hauled;
- **rule 5**, as a clause, by the lead's ruling on Ext §14 item 4: Ext §5.10's measure on her file
  (the main mast's `load_kn` a square metre of the settee aback against her main topsail's, at the
  incidences of her own tack and of a two-point shift close-hauled; B3's in Ext, B4's here, lead
  item 8); the case that holds is pinned and named. If neither holds, D44 (c)'s `settee` row is
  accepted in advance: B3 adds it as a follow-up step keyed on `settee` (`data/sail_classes.yaml`;
  `tests/test_sails.py:65-74`, old beside new) before her merge, and the clause follows it. The
  row changes the curve her settee is trimmed and driven by (the polar trims by
  `wanted_sheet_angle(sail.curve_class, awa)`, `world/ships.py:438`), so 7-197's rule-1 clause,
  her polar and §9's table are measured again on it, old beside new.

**7-199, in wearing the settee is lowered as she bears up and hoisted on the new lee once the stern
is past the wind** (B4, on B3.3; Ext §10.3 item 2; D46 rule 4 as reworded): `yard_lowered` true
within a band of ticks after "up helm"; at the hoist tick the wind on the new side of the stern;
she comes to by the wind on the new tack within a band at a set time.

**Not a truth, a test: her heave-to** (D4; `Build-Ships.md` §15; Ext §5.7). No source says how a
bilander lay to (Bil §4). Her lie at +150 s and +300 s in 15 and 20 kn, both ways: the settee kept
with its sheet eased (the driver rule), and clewed up aloft (D4 (a)). The test pins the way B3.3
built under the lead's ruling, within the heave-to's four to seven points
(`data/evolutions/heave_to.yaml:50-51`); the other way's lie is recorded in TuningNotes.

---

## 15. Pins her work could move

- **None of the existing ships'.** The module writes one new file; no shared function or table
  changes; `brig()` is untouched; the eight files stay byte-identical (the two-way byte test).
- **Lists, not pins:** `tests/test_profile.py:502-507`'s `MODULE_FILES` row, `[]` →
  `["bilander.yaml"]`, by the stage-0 agent, old beside new, with the reason (§12.1).
  `tests/test_stores.py` and `tests/test_hull_form.py`'s round-trip test glob every ship file; her
  file passes the first by its ration.
- **The 0H guard** (`tests/test_hull_form.py::test_every_ships_spec_round_trips_its_pickle_with_no_shape_key`,
  working tree) fails on any file that writes shape keys. B1's stage B meets it first and B8
  restates it; her first commit assumes it restated (§12.1).
- **The registries:** new words only; no existing scenario, business table or test names "bilander"
  (grep).
- **The caches** (32, `world/ships.py:294, 343, 470`): her file the twelfth or thirteenth; results
  unchanged.
- **The harbour's glob** (`ui/harbour.py:382`) lists her; its test checks membership only.
- **`tests/test_view_geometry.py:572-602`** (each square sail drawn within 5% of its area): only if
  B5 adds her file to its list; her spritsail's drawn area is checked before then (Ext §11).
- **Not hers, said:** `tests/test_sails.py:65-74` moves only if rule 5 fails and D44 (c)'s row is
  taken (B3's, Ext §5.10), and her own polar and 7-197's rule-1 clause are then measured again on
  it before they are pinned (§14); the lee-port pins are SW-5's (her default is unarmed).

---

## 16. Risks, ranked

1. **Rule 1's margin is thin.** On this design's own figures the beat holds at 60° by 0.05-0.12 kn of
   way to windward over 70°, by the headsails' cut (§9). *Mitigation:* the headsails cut on her
   measured stays; measured at step 2; the knobs only within sources; the clause reported, not
   forced.
2. **Her file is unsafe before B3.3.** Her settee takes the lugger's paths, and getting under way
   failed in the trial. *Mitigation:* not committed to the package's branch before B3.3 (§0); the
   lead's item 1 for the window's timing; the untried manoeuvres run on her file.
3. **The sheet's lead.** The proxy's block falls 4.45 m short of the taffrail (§12.2 item 6).
   *Mitigation:* B3.3 builds Ext §5.9's reserve branch from the start; B4's check proves it.
4. **The physics' lateral offset understates her settee** by about 40% (§12.2). Not changed under
   the gate; recorded beside her file and in TuningNotes.
5. **The heave-to.** Either way may fall off, as the trial's did (79-87° by 300 s). *Mitigation:*
   both lies measured before any pin; a test, not a truth; the lead's ruling decides the way.
6. **Rule 5 may fail** for a settee laid flat aback, as the tables predict (Ext §5.10).
   *Mitigation:* the case that holds is pinned; else D44 (c), accepted in advance, built by B3 as a
   follow-up step before her merge, with her polar and 7-197's rule-1 clause measured again on it.
7. **A company of eight against six-hand settee requests,** ten- and twelve-hand square-sail work,
   and a side of guns. *Mitigation:* two main topmen; every request measured at eight; the times
   recorded; nothing tuned to make her quicker.
8. **Gwyn's freehand ratios at Chapman's scale,** ±10 px (±0.3 m) a point, on every rig height and on
   the quarterdeck; the settee's crossing read three ways. *Mitigation:* B4's re-measure with a
   checker (§3.6); every line marked `stand-in`; the crossing recorded, never used to place the yard.
9. **The collier's rows may read badly** in places: every bodies table's OCR is garbled, though the
   dead flat reads cleanly on the page image. *Mitigation:* the page image read at full
   resolution; a row not read keeps the judged fallback, marked; the rung falls to T on that line.
10. **The drawn depth 0.73 m short of her draught**, and perhaps the drawn displacement more than 15%
    short. Recorded, never moved.
11. **The draught's datum.** Lloyd's column may be the mean or the greatest; ±0.5 ft on her grounding
    and her lateral plane. Recorded, with the collier's check.
12. **The armed fit's ports are invented** (owner's question 1).
13. **The spritsail's foot near the water** off a stem head 2.65 m up. *Mitigation:*
    `spritsail_yards.py` checks every foot above the water at heel 0 (Ext §9.3).
14. **The false "Tacked"** on her brig-like hull (D13). *Mitigation:* every truth judges by heading.
15. **The 74's window held by hers** if B3.3 lags (`Build-Ships.md` §2.2: B7 after B4). *Mitigation:*
    the lead's item 1.
16. **Byte identity on the build machine.** *Mitigation:* rounding at the measured figures.

---

## 17. Open for the owner or the lead

**Answered by the owner (2026-10-29).**
- **The armed fit's guns:** "Looking at the picture again, you're right, there really isn't a
  clear place for guns on it. I'd say that, reasonably, we could put the guns on the
  quarterdeck, or we could make the armed version a subtle variant with cutouts in the gunwale
  somewhere along it for the guns. I'd go with the way that seems more historically accurate
  and reasonable." Taken: **ports cut in her waist** (this design's pick, the owner's "cutouts
  in the gunwale"). The period's traders were "pierced for" their guns, and no source read
  shows a trader's carriage guns firing between the stanchions of a quarterdeck rail; Gwyn
  draws her unpierced, as a trader in peace. The open rail (lead item 10) is not taken.
- **Her name:** "Hopewell is fine." *Hopewell*, as proposed.

**For the owner** (each with this design's pick and what the owner would see):

1. **The armed fit's guns.** The register gives a bilander of her size four 3-pounders, but Gwyn's
   drawing shows no gun ports. Where do the guns go?
   - *Pick:* two small ports a side in her waist, their places and sills judged, shut and unseen
     until package 81 draws ports.
   - *What you would see:* nothing new in this package's pictures. In a fight her two guns a side
     fire through ports, and the lee ports shut at about 21° of heel, like any ship's.
   - *The other way:* the four guns on her raised quarterdeck, firing between the stanchions of its
     open rail. No ports, true to Gwyn's picture; the guns stand higher and never shut. But the game
     has never fought a carriage gun mounted that way, so it would need checking first.
2. **Her name.** This design names her *Hopewell*: a Poole-built bilander (1749) bore that name in
   Lloyd's 1776 (Poole–Sunderland/Memel) and 1779 (Dublin and Poole to Newfoundland). Her notes say
   she is not that vessel (150 tons, built 1749).
   - *Pick:* *Hopewell*.
   - *What you would see:* she is the *Hopewell* in the harbour list, the log and the hails. The
     other way: a common trading name of the period that no bilander in the register bore, chosen
     by judgement as the merchant brig's *Industry* was.

**Settled here, not asked:** the spritsail is bent and kept out of plain sail, set now and then as
the owner's "occasional sail" for the razee means (§4.3; the code's word, lead item 11); the tops
call her "a bilander" once her rig is made out (§8); Gwyn's carved quarter badge is kept in words,
with the rest of her carving and paint (§3.2).

**For the lead:**
1. **Her window against B3.3.** *Pick:* her window opens after B2's merge, and B4 builds her to
   stage A at once in her worktree; her file reaches the package's branch only after B3.3 is merged
   there. If B3.3 lags, she is held unmerged, and the 74's window waits as `Build-Ships.md` §2.2 has
   it. Taking the 74 before her would change the owner's order and needs the owner's word.
2. **The hook test's row.** *Pick:* a stage-0 commit, `MODULE_FILES["ships.bilander"]` `[]` →
   `["bilander.yaml"]`, immediately before her first commit in the same push, as 9454fd6 came just
   before 614d2d4; the hook test passes on the pair. B4 never touches `tests/test_profile.py`.
3. **The 0H guard** (`tests/test_hull_form.py`, the pickle test of every ship file) restated by B8
   before any ship writes shape keys: B1's stage B first, then her first commit.
4. **The settee's sheet branch.** Her cut puts the proxy's block 4.45 m short of the taffrail, which
   meets Ext §5.9's trigger. *Pick:* B3.3 builds the reserve branch from the start, keyed on
   `settee`, as the foot from the corners with the block a fathom abaft the clew and abreast of it
   (no reading of the profile; §12.2 item 6). **Plainly:** Ext §5.9 (approved) puts the block at
   the taffrail on the centreline. On her cut the two blocks lie within 0.1 m fore and aft and
   about 1.6 m apart athwartships, and B5.4 draws the sheet to the centreline. The other way is
   Ext's block, which needs the taffrail's x from somewhere the trim may read. Which block? For
   the record: the physics' lateral offset for a sail with no boom or gaff understates her
   settee's by about 40%; it stays unchanged under the gate, in TuningNotes.
5. **Her body raised from §5.7's "a trader's body R/T" to S†,** Steel 1805's brig collier scaled
   (lengths 0.92, provisional, against about 0.95 by Folio I's row C: settled at step 1, §3.4;
   sections 0.847), once p. 26 is transcribed; **and Gwyn's quarterdeck, sheer, wale, head and
   lights marked stand-in (S†), not §5.7's S,** since their metres rest on Chapman's scale (§3.3);
   the stern's type and the head's word stay sourced (S). Please note both against the approved plan
   hull by hull. The pages are in `reference-cache/steel-1805-collier-brigantine/`, outside the
   repository, public domain; their README sentence comes with this design's commit (§3.6).
6. **D6 (a):** Chapman unscaled at 118-128 tons, with a Plainly line, against the decision's note
   that Chapman's figures "scale by only about 2%" to 130 tons. *Pick:* unscaled (D7 (a) gives 70.6
   by 19.4 ft; 2% lies inside Chapman's error; 128 tons is "about 130"). If the lead reads D6 (a) as
   the scale, ×1.02 moves every figure laid on Chapman's (the hull block, Gwyn's heights and the
   settee at her scale) by 2% in length, 4% in area and 6% in displacement, and the burthen to
   125-136 tons; the method and the marks stay as they are.
7. **Rule 1 if it fails on her file.** D44 (c)'s `settee` curve was accepted in advance only for rule
   5's failure. *Pick:* report the figures first, and change no curve for rule 1 alone unless the
   lead rules otherwise.
8. **B3's work on her file after B3.3's merge.** Ext §5.4, §5.7 and §5.10 have B3 run the untried
   manoeuvres, the heave-to and rule 5's measure (the main mast's `load_kn` with the settee aback)
   on her file, which comes after B3.3. *Pick:* B4 runs them; a guard found missing, a heave-to way
   her figures overturn, or D44 (c)'s `settee` row if rule 5 fails (`data/sail_classes.yaml`;
   `tests/test_sails.py:65-74`, old beside new), is a follow-up B3 step keyed on `settee` alone,
   before her merge. After the row, B4 measures her polar and 7-197's rule-1 clause again on it,
   old beside new.
9. **Names:** the armed fit "armed merchant"; the description key `bilander` and its words (§8); the
   dry yard's id `main.crossjack.yard`.
10. **If the owner takes the open rail** (owner's question 1): a long gun at place `rail` is allowed
    by the schema (`GUN_PLACES`, `schema.py:222`) but has never been used by the gun deck's code.
    Who checks it?
11. **"An occasional sail", for her spritsail and the razee's.** The owner's answer for the razee
    reads "an occasional sail kept out of plain sail"; Indf §4.6 proposed the 64's sprit sails in
    "all sail" and "occasional sails". In the code "occasional sails" is the sail room's canvas,
    written unbent and kept out of "all sail" (§4.3). *Pick:* the period's sense: her spritsail
    bent, in "spritsails" and "all sail", out of "plain sail" and out of "occasional sails" (Ext
    §4.1's groups). The razee's at B1's stage B may want the same reading, so the two agree.

**Kept as decided, said:** D5 (a)'s third against Gwyn's 0.395 (§4.4); Gwyn's heights laid from the
waist rail (§1.4); no studding sails or royals (§4.1, §4.2); Falconer's three to a 3-pounder against
the merchant brig's four to a pair of 6-pounders (§5.3); the house's anchors against Steel's King's
allowance (§7).

---

## 18. Found on the way

1. **Her settee is a lugger's lug to every path until B3.3** (`_lugs_all`,
   `evolutions/scripts.py:6800`): her file must not reach the package's branch before it (§0).
2. **The loose-footed proxy is 0.61 of her cut's foot** (6.85 against 11.29 m), so the trim's block
   falls 4.45 m short of the taffrail and the physics' lateral offset understates hers
   (`trim.py:278-279, 388`; `physics/sails.py:1342-1350`). D45's "the clew about a fathom inside the
   taffrail" holds for the corners (1.86 m) and not for the trim's proxy, which never reads them.
3. **Steel 1805's two "next sources" identified** (read here on the page images): Tables p. 26 is
   "Bodies of a Brig Collier of 170 27/94 Tons"; p. 16 "Bodies of a Brigantine of 10 Guns, 16
   Swivels, and 201 Tons". The collier is the trader; the brigantine is armed and finer.
4. **The collier's Folio I column** (n488, read here, row letters by the pages note's reading of
   Folio I): row B, the range of the deck, blank; row C (the stem at the hawse holes, in merchant
   ships at the wing transom, to the post's aft side) 76 ft 3 in; keel for the tonnage 60 ft 8 in;
   dead flat 30 ft 0 in abaft FP; breadth 22 ft 6 in moulded and 22 ft 11 in extreme; burthen 170;
   load draught 10 ft 9 in afore and abaft. Row C is shorter than her stations' span (about 76 ft
   6 in to 76 ft 11 in), where on the sloop and the cutter it runs 1 ft 9 in to 2 ft 6 in longer
   than the length between the perpendiculars: a conflict for step 1 (§3.4).
5. **The register's bilanders draw more than Steel's larger collier** (11-12 ft at 130 tons against
   10 ft 9 in at 170): Lloyd's column may be the greatest draught deep laden (judgement).
6. **The collier's top-timber line scaled stands about 1.57 m above her water,** against Chapman's
   waist rail at 1.65 m (judgement on the keel's depth): the stand-in and her own source agree on her
   side within about 0.1 m.
7. **Gwyn's "deck" in Bil §2.3's rig ratios is the drawing's waist rail** (image y 958 against the
   rail at 961, ±5 px): the heights are laid from the rail, and Bil §2.3, and D6 (e) after it, should
   say so. For the research note.
8. **Gwyn's waist stands higher than Chapman's at Chapman's length:** Bil's 64-68 px give about
   1.9-2.0 m against 1.65 m. The drawing's vertical scale is not its horizontal, as a freehand
   profile's need not be, so its heights are taken from its rail, not its sea line.
9. **Gwyn, measured here beyond Bil §2.3:** the fore top 0.33 of the rail length above the waist
   rail; the quarterdeck's break about 0.32 of the length from the taffrail; the stern view's three
   lights in one band and the stern's half-breadth 1.55 m at the taffrail and 2.05 m at the wale (at
   her scale); an oval carved badge on each quarter.
10. **The settee's crossing read three ways** (Bil's 32 px, about 48 px, about 67 px below the top):
    a measuring task, not a figure.
11. **The settee is what puts her beside the brig by the wind:** without it this design's probe lies
    at 60° and beats at 70°; the settee and the headsails alone lie at 50°, a point nearer (§9).
12. **Chapman's dry yard and the 64's crossjack proportion agree** on her: 40.8 ft both ways, the
    second the 64's crossjack to her mizen topsail yard (Steel p. 49) carried to her by judgement.
    Steel p. 40's own rule for a ship's crossjack, the fore topsail yard's length, would give her
    30.0 ft, shorter than the main topsail yard the dry yard spreads; not taken (§4.1).
13. **The spritsail yard equals the fore topsail yard** by Steel p. 40's rule (read on the page
    image, `Research-74-2026-10.md` §5.3), and in Steel's 64 column (57 ft 6 in each, p. 49): the
    rule taken for hers.
14. **She is a slow trader by the owner's rig:** about 10.1 m² of plain sail per t^(2/3) against the
    brig's 13.8, the lugger's 19.8 and the cutter's 12.1 (measured on the files).
15. **The brig's main yards brace to 62°, 64° and 66°**, two degrees beyond the fore's
    (`brig.yaml`, read here): the dry yard takes the brig's main yard's 62°, not the frigate's
    crossjack's 60°, which stands on a mizen.
16. **Steel 1794's Navy anchor table ends at the brigs of 200 tons** (three of 12 cwt) and the cutter
    (three of 10 cwt) (read on IA leaf n127): 6 cwt a hundred tons, near the house rule's 5.
17. **Lloyd's key (1781) does not say whether its draught is the mean or the greatest.**
