# Design: the *Prince de Neufchatel*, the American privateer hermaphrodite brig of 1812-1815 (package 75, Phase 3)

The design for the second ship of package 75 (B2). It was judged from two drafts, one written
for fidelity and one for buildability. The fidelity draft is the base: it measured her hull on
her own lines and read the period's tables on their pages. The buildability draft gave the
engine key's contract, the stage 0b list, the generation checks and the testing report. Every
claim kept was checked against the code at this head and against the notes. Where the drafts
disagreed, or one was wrong, this document says so and gives its reason (the table below). It
is for her builder (B2), the stage-0 agent (her stage 0b), the engine builder (B3, its step
B3.4) and the scenario builder (B6). Its §0, §12 and §17's second list are also for the lead.
Nothing here is built.

**Where.** The clone `D:/Projects/FreeSail/FreeSail-pkg-75`, on the package's branch at 8f30be9: stage
0, stage 0E and B1's stage A committed (614d2d4), the lead's ab9181c merged in (8af6870), the
owner's answers on stage A and the lead's approval of the hull's design recorded. Stage 0H,
SW-2b.1 and B1's refinements were under way in the working tree, uncommitted. `g.hull_form` and
`g.midship_section` are cited from it (`tools/gen_ships.py:691`, `:864` there, "working tree").
Every other `file:line` is at 8f30be9. Paths are from the repository root. A builder re-checks a
line before editing it.

**What binds, in order:**
1. The brief, `docs/dev/M7-WorkPackages.md`, "## Package 75", item 2: "the hermaphrodite brig or
   schooner rig as the sources have her, her long guns and carronades, her large crew for
   prizes ... the rig's peculiarities recorded for the physics' reading (the physics is not
   changed; where her rig needs a sail class the engine lacks, say so for the lead rather than
   approximate silently); her privateer's fits; an American vessel of 1812 under 71's basic
   signals system". Then the lead's notes at its end: the gate on the engine extensions only;
   item 6, the scenario's `nations:` block ruled in and laid in stage 0b, a row not checked
   against James named open; item 7, D10(a)'s key "built by B3 as its fourth step beside
   `under_bowsprit` at places 1 and 3 of §4.2, inert until her file uses it"; item 8, the lead
   merges after each ship; the hull's principles, design and order approved (2026-10-29).
2. `docs/design/Build-Ships.md` (cited **Build**): §13.1 (what is laid for her and what her
   design settles); §2.2-§2.6 as amended by **the owner's direction of 2026-10-29**: the build
   goes on without holding for the owner's own test of the *Indefatigable*, the owner receiving a
   testing report instead, so her window follows B1's merge. That direction was given in the
   session and is not yet written into Build at 8f30be9 (§17, lead item 4). Also §3.3, §4,
   §5.0-§5.3, §5.6, §5.7, §6, §7, §8.1, §9.2, §9.4, §9.5, §12, §14-§16, §19.
3. `docs/design/Decisions-ShipsRound2-2026-10.md`: every decision taken as recommended unless
   answered otherwise. Hers: D10 (a); D11 (a); D15 (a); D21 (a); D22 (a); D23 (a); D24 (a); D29
   (b); D35 (b) limited, as answered; D36 (a); D37 (a); D38 (a); D47 (a); D8 (b) as answered (the
   64's and the bilander's yards only); D27 and D39 taken with the brief (an American vessel of
   1812, her names American).
4. Her research note, **Neuf** (`docs/design/Research-PrinceDeNeufchatel-2026-10.md`), and the
   texts it cites; **Eng** (`Research-ShipsEngine-2026-10.md`) §3 for her rig in the engine.
   Her module is `tools/ships/neufchatel.py` (stage 0's stub), her file
   `data/ships/hermaphrodite-brig.yaml`, her description key `hermaphrodite brig` at rank 2. Her
   draughts are RMG ZAZ6177 (lines) and ZAZ6179 (sail plan), measured from the museum's 1280-px
   images and never copied (Crown copyright on the photographs: Neuf §0.3).
5. **Ext** (`docs/design/Design-ShipsEngineExtensions.md`): §4.2's places 1 and 3, beside which
   D10(a)'s key is read; §14 item 12. SW-4's pivot rule (Build §9.2) is not hers: she carries no
   pivot (§5.1).
6. The owner's private references (`D:/Projects/FreeSail/owner-notes/`): Winfield 1793-1817
   pp. 335-336 and its photograph of Reed's modern model, cited by page only; none of their
   text is here. The public-domain page images held there (Adye 1804, Steel 1794 vol. I, Fincham
   1843) were read for this design.
7. Pictures for the eye (anecdotal checks of appearance, never a source of points): none held.
   The research names RMG TRO/103/1's watercolour of the boat attack (catalogue only, not online)
   and NHHC USN 902978 (not reached). Reed's model is modern and is used for the eye only.

**Marks.** *read*: the page, the page image or the code cited. *read (OCR)*: an OCR text under
`docs/references/`, not checked against the page image. *measured*: Neuf's figures off the
1280-px sheets. *catalogue*, *secondary*, *memory*, *judgement* as the notes use them. **Measured
here** means one of three things: arithmetic on Neuf's figures; a reading of the held 1280-px
images (ZAZ6177 at 7.05 px/ft, ZAZ6179 at 6.52 px/ft) by the drafts' scratch scripts, with the
research's registration (the after rabbet at the sailing-trim waterline at x 321.6 px; the
waterline the research's fitted line, y = 248.1 + 0.0288 (x − 350); Neuf §2.3), good to about
±2 px, ±0.3 ft; or `polar_of` and the description lookup run on committed files and scratch
stand-ins. The scripts are outside the repository (`scratchpad/designs/neufchatel/`: `probe/`
`crop.py`, `redline.py`, `sills.py`, `ports.py`, `figs.py`, `polars.py`, `standin.py`; `figs.py`
and `probe_polar.py` beside them; `verify/nowave.py` and `verify/closest.py` from the review
pass), run from the tree root with `py`. **Read here** means a page
image held in `owner-notes` read for this design: Adye 1804 pp. 72 and 155 (IA leaves n95, n178),
Steel 1794 vol. I's anchor table and cordage table (IA leaves n127, n117), and Cobb and James in
their OCR. *To read*: a source on file but not yet read for this figure; its line is R or T until
it is (Build §5.0 principle 3). **Plainly:** marks a choice that departs from a decision, a
ruling or the brief, with its reason. No test suite was run. Nothing in the repository was
written.

**One sentence.** One module writes one file: a flush-decked Baltimore privateer on her own lines,
with a brig's square foremast and a schooner's main, a large loose-footed fore gaff sail lapping
the mainmast, eighteen guns and 130 men. She is built whole at once but for her small main
topgallant, which waits behind one module constant for B3.4's key and sails meanwhile without it
(D10(c), the sheet's own fallback), so that she is never handled as a brig.

---

## How the two drafts were judged

| Question | Taken from | Why, in short |
|---|---|---|
| The hull: rail, deck, stem, knee, transom, eleven sills, all measured on ZAZ6177 | fidelity | Measured for the draft and checked here by eye on its strips. The buildability draft's profile was Neuf's rules ("deck + 4 ft", "deck + 1.3 ft") and "to measure" at both ends |
| The frame's join (Neuf's port and mast origin against the after rabbet) | fidelity's figure, buildability's form | Measured at both end ports: 0.85 ft. The buildability draft's 1.5 ft was judgement and would put every port and mast about 0.2 m aft. Kept as one named constant, `POST_AT_DECK_FT` (§1.4) |
| Her stern | fidelity, under a Plainly | Measured: a flat transom raking 31°, 16.1 ft at its corners, no counter, which is §5.1's `raked`. Build §5.7 has "square, about 17 ft", which was Neuf's "not re-measured". A checker re-traces it in task 1 |
| Adye's and Steel's tables | fidelity | The page images are held and were read here. The buildability draft left them "to read" with the generator's memory figures and Luce's rule meanwhile |
| The plank on the end half-breadths and the section's foot | fidelity | 0.14 and 0.16 m with 2 in of plank. The buildability draft's 0.09 and 0.11 lack it |
| GM | fidelity: 2.1, tuned only within 2.0-2.2 | D23(a). The buildability draft widened tuning to 2.4 without a Plainly |
| The main topgallant out of plain sail | fidelity | Her gaff topsail beneath it is a light sail; keeping both out keeps "plain sail" consistent aloft and leaves 7-193 unmoved at the flip |
| D10(a)'s key: its contract | buildability | Places 1 and 3 only, as the lead ruled, with a measure and a report before any further place. The fidelity draft's contract reached places 2 and 5-8 unmarked |
| The key's name | buildability: `schooner_mast` | The fidelity draft's `fore_and_aft` would sit beside `Sail.is_fore_and_aft`, the locals named `fore_and_aft` in `evolutions/scripts.py` and `_set_fore_and_aft`, and invite misreading |
| `MODULE_FILES` in `tests/test_profile.py` | buildability | Her first file fails the hook test without her row (`tests/test_profile.py:502-532`). The fidelity draft missed it |
| The generation checks | buildability | Tonnage, mast spacing, triples, spars against Fincham, sails against ZAZ6179, each raised in words (§1.5) |
| The main topgallant's pole filed as a mast | buildability | `main.topgallant_mast` from the first commit, so that the trim's levels see each yard on its own spar (Indf §4.1) |
| The `nations:` block's rows | buildability | The peace with France read here in James vol. 6 p. 229 (OCR l. 12000-12001). The fidelity draft had it from memory |
| The owner's question on her best speed | buildability | The right realism question: the engine's polar peaks on a reach, her accounts were running |
| The fidelity draft's questions on a second fit and on her date | dropped | D22(a) already gives a second fit only if a scenario asks. Build §12.2 and D27 with the brief leave the year to the design, which settles it (§11) and tells the lead |
| 7-193's form | merged | The buildability draft's speeds at 60° and 70° above the frigate-36's; the fidelity draft's `closest_deg` no wider than hers, the safer form until her file is measured; the angle and the running speeds reported, not pinned |
| 7-192's mast clause | buildability: 13.3 ± 0.3 m apart | Independent of the frame's join. Neuf's "0.105 abaft the middle" assumed the rabbet as origin; after the 0.85-ft join the main stands 0.112 abaft |
| The description | neither as written | No `fit` (Build §8.1: her one fit is her default; the fidelity draft wrote one). Rows for "a hermaphrodite brig" and "an hermaphrodite brig" are needed: probed here, the lookup gives "merchant brig" without them (the buildability draft said the second needed none) |
| The quarter bill | buildability | Helm 1 at a tiller, powder 2, small arms and boarders on the privateer schooner's shares, the trimmers scaled from the brig-sloop's by plain sail. The fidelity draft took the frigate's and Indf's |
| The prize-masters | buildability | One drawn in her people file, the rest among the able seamen: a post is an officer on the quarterdeck who never hauls (`crew/muster.py:179`) and needs an outline |
| The marines and the ratings | fidelity | Sixteen marines on Cobb p. 73's "marine corps"; more landsmen on Cobb p. 39. The buildability draft copied the brig-sloop's twenty |
| A surgeon | neither | The buildability draft's "no surgeon" is wrong: Cobb pp. 75-76 (OCR l. 2964-2999, read here) gives her a surgeon by title, a stranger of little skill (hearsay). The fidelity draft's posts left the surgeon out. The surgeon is a post here |
| The rope | buildability | The brig-sloop's for the fore and the head, the topsail schooner's for the main, each scaled by √(sail on that mast). The fidelity draft scaled the frigate's by one factor |
| The pair check | buildability | Against the topsail and privateer schooners (*Lynx*), now that her stern is `raked` as *Lynx*'s is; run in scratch if SW-2b.2 has not landed |
| The long 6s | buildability: bow chasers through `g.chasers` | The brig-sloop's file has its 6s at the bow (`chaser.bow.*`). Broadside 108 lb by 70's rule; the fidelity draft's 102 lb (one a side on the broadside) is put to the owner in the judgement list only |
| The rail at the masts | buildability's flag, fidelity's figures | The traced rail stands about 7.5 ft above the water at the main and 8.2 ft at the fore, against ZAZ6179's 8.4 ft at both. A measured conflict, given a task |
| The testing report | buildability's specification | Merged into the road's last step (§13). That it holds for her is judgement, put to the lead |
| The colours | buildability | None shown in the last chase (Cobb p. 104, OCR l. 4204, read here); for B6 |

---

## Decisions taken

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/neufchatel.py`: `Particulars`, `particulars()`, `write(out_dir, p)`, `main_topgallant(b, p)`, `build(out_dir)`; one file `data/ships/hermaphrodite-brig.yaml` | The lead's structural decision and name (item 9); Build §3.3 |
| 2 | Her data in her sheets' frame (feet forward of the after rabbet at the sailing-trim waterline, feet above that water), converted once; one frame join, `POST_AT_DECK_FT = 0.85`, measured | Indf §1.4's method; every figure reads as Neuf gives it (§1.4) |
| 3 | Checks raised in words before the file is written | Indf §1.5's rule: `raise ValueError`, never `assert` (§1.5) |
| 4 | Hull: LWL 32.7 m rabbet to rabbet, beam 7.82 m, draught 3.16 m to the false keel, 288 t, lateral plane 102 m², rudder 2.61 m² on 3.58 m | D29(b), D38(a); Winfield pp. 335-336; Neuf §2.4-§2.6, measured |
| 5 | GM 2.1 m, tuned only within 2.0-2.2 | D23(a); Neuf §2.5 |
| 6 | `hull_speed_kn` 12.9 to start, tuned within 12.5-13.9; `clr_x_m` +0.3 to start, tuned against the helm; neither forced | D24(a); realism, not pacing (§9) |
| 7 | `deck_height_m` 1.16 m, her flush deck at side at mid-length; D18 moot for her | Neuf §2.7; Build §5.5 (§2.2) |
| 8 | A profile and her shape keys from her first commit: her stern **raked**, measured; her head a knee | Build §5.0, §5.6, §5.7. **Plainly:** §5.7 has her stern "square, about 17 ft" (§3.5) |
| 9 | Every port gun on its port's measured x and sill, to the centimetre; eleven sills measured, the lowest 4 ft 11 in (1.50 m), shut at 18.2° of heel alone | The brief's sourced sills; Indf decision 9; Build §5.1 (§3.3-§3.4) |
| 10 | Spars and sails from ZAZ6179, the yards doubled; Fincham's Ex. 1 only for spars it does not draw | D37(a); Neuf §1.2, §3.2-§3.3 (§4) |
| 11 | The fore gaff sail to her plan: loose-footed, its clew 2.7-2.9 ft abaft the mainmast, about 154 m², on the topsail schooner's pattern | D21(a); Neuf §1.2 (§4.4) |
| 12 | **The main topgallant (D10):** behind `MAIN_TOPGALLANT`: `"out"` writes nothing (D10(c)); `"keyed"` writes its two light yards and the sail with D10(a)'s key, once B3.4 is merged. Ids final from the first commit. Out of "plain sail" either way | D10(a) as answered; the lead's item 7; Build §13.1's fallback "(c), not (b)" (§0, §4.5) |
| 13 | D10(a)'s key `schooner_mast: true` on `main.mast`, read by B3.4 at Ext §4.2's places 1 and 3 only | The lead's item 7; Cobb p. 38, "her mainmast was rigged as a schooner" (§12.2) |
| 14 | Plain sail: the fore course, topsail and topgallant, the fore gaff sail, the mainsail, the fore staysail and the jib | The brig's and the schooner's patterns together; put to the owner (§17, owner question 2) |
| 15 | Light sails as the owner chose: the fore lower, topmast and topgallant studding sails and the main topmast staysail (its upper foot); no ringtail, no water sail; "the Jack" not built | D35(b) limited; D8(b) as answered (§4.6-§4.7) |
| 16 | One fit, **"as taken 1814"** (default): 16 × 12-pdr carronades (Adye's 5 cwt 3 qr 10 lb) and 2 long 6-pdrs (Adye's 8 ft, 22 cwt); no pivot. Cobb's "nine and eighteen pounders" in the fit's note | D22(a); Winfield pp. 335-336; Adye pp. 72, 155, read here (§5) |
| 17 | The long 6s bow chasers in the foremost port a side; the carronades in the next eight; the two aftmost ports empty | D22's leave; the brig-sloop's precedent; judgement (§5.2) |
| 18 | Crews by Douglas (4 to a carronade) and Falconer (5 to a long 6) | `period.py`; D31(c)'s reading for the new ships (§5.3) |
| 19 | Company 130: posts 12 (a captain, five lieutenants, the sailing master, the surgeon, the boatswain, gunner, carpenter and sailmaker), marines 16, idlers 8, seamen 94; more landsmen than the privateer schooner's | D36(a); Niles vol. VII p. 284; Cobb pp. 39-41, 73, 75-76 (§6.1) |
| 20 | The nine prize-masters: one drawn in her people file, the rest among the able seamen | `crew/muster.py:179`; Cobb p. 40 (§6.1) |
| 21 | Quarter bill on the privateer schooner's shares, trimmers by the brig-sloop's scaled | §6.4 |
| 22 | Her names the `american` list; no nation in her file; the marines' kit the nation's (`basic` for the United States) | D39 with the brief; Build §9.4 (§6.5) |
| 23 | Ground tackle by Steel 1794's row for "14 Guns, 300 Tons": three bowers of 20 cwt, a stream of 7, a kedge of 3 cwt 2 qr; the cordage table's "Sloops" column, five cables of 13½ in and a stream cable of 8 in (the column judgement) | Steel's tables, read here; the house's preference for Steel (D33) (§7) |
| 24 | Description `hermaphrodite brig`, "a brig" at a distance, rank 2, `roles: [privateer]`, no description `fit`; four lookout rows | D15(a); Build §8.1 (§8) |
| 25 | Polar measured and recorded; 7-193 pins her best speed in 25 kn within her accounts' band and her pointing against the frigate-36, the best point's angle reported | The brief item 6; D24(a); put to the owner (§9, §14) |
| 26 | Her scenario **August 1814** in the western Channel, with a `nations:` block of that summer; rows read cited by page, the rest named open | D27 with the brief; Build §12.2; the lead's item 6 (§11) |
| 27 | Her stage 0b: the key's schema (at B3.4's boundary if B3.4 opens first), the `nations:` block (after B6's D48 change to `world/scenarios.py`, Build §4.2), and her `MODULE_FILES` row committed with her first file | Build §3.3; the lead's items 6 and 7 (§12.1). **Plainly:** the key's runtime field and predicate are B3.4's, not stage 0b's (§12.1 item 1) |
| 28 | A testing report for the owner at her merge: pictures of the important views and her figures | The owner's direction of 2026-10-29 for the *Indefatigable*, taken to hold for her by judgement; put to the lead (§13) |

---

## 0. The gate: what her builder builds at once, what waits, behind which stub

**No gate stands on her.** The plain ships wait for nothing gated (Build decision 2; Ext §9.4:
"the *Neufchatel* wait[s] for nothing here"). One piece of her waits for an engine step, ruled in
by the lead: her main topgallant on D10(a)'s key, built by B3 as B3.4 beside `under_bowsprit` at
Ext §4.2's places 1 and 3, inert until her file uses it (the lead's notes, item 7).

**Her window.** By the owner's direction of 2026-10-29 the build no longer holds for the owner's
own test of the *Indefatigable*; the owner receives a testing report instead. So her window opens
at B1's merge, with the fresh merge of the lead's head and her stage 0b (Build §2.1, §3.3).
Build §2.2 also puts SW-4 before her, and SW-4's rows in `freesail/world/ships.py` wait for B1's
window to close and for 84's step 7 (the lead, 2026-10-29). Her own rows in that file are her
last step (§13), so she can be built while SW-4 waits; that departs from Build decision 15 and
is said plainly in §8. Which rows go in first is the lead's (§17, lead item 3). Her stage 0b's
`nations:` block waits, in turn, for B6's D48 change to `world/scenarios.py` (Build §4.2; §12.1).

**Stage A, at once:**
- the module, her people file and her ship file complete in hull, profile with its shape keys,
  masts, yards, sails, lines, groups, aliases, guns, crew, quarter bill, ground tackle, boats,
  pumps, hold, stores and description;
- `MAIN_TOPGALLANT = "out"`: `main_topgallant(b, p)` writes nothing. Its docstring and the main
  topmast's note say the sail is on her plan and comes with B3.4's key. She sails as a
  fore-and-after with a square fore, which is how Cobb has her main ("rigged as a schooner", p.
  38). In the engine she is then trial A's vessel (Eng §3.3). The sail left out is about 28 m²,
  some 3% of her measured canvas (Neuf §3.3);
- every id final from the first commit: `main.topgallant_mast` (the topmast's pole, filed as a
  mast of its own and bare until the flip), `main.topsail.yard` (the lower light yard, which
  carries no sail), `main.topgallant.yard` and `main.topgallant`, so that the flip renames
  nothing and moves no group member but its own.

**If B3.4 is merged before her first commit**, she takes `"keyed"` from that commit and there is
no stage B.

**Stage B, once B3.4 is merged** (and its schema key, §12.1 item 1):
- `MAIN_TOPGALLANT = "keyed"`: `main.mast` takes `schooner_mast: true`; the two light yards and
  the square sail between them are written (§4.5);
- her file regenerated alone. Her classing re-measured: the same row as stage A but for the two
  light yards among the after yards, place 2 being left as it is (her golden row, §14). Her polar
  moves at most by the two light yards' windage, since the sail is out of "plain sail". Her
  rating, balance, tack, wear and heave-to are re-measured. Each figure is shown old beside new.

**If B3.4 slips past her merge.** She goes in at stage A. **Plainly:** that departs from D10(a)
as answered. Her file's note, the tuning notes and spec §27 as built say so, and stage B follows
B3.4 as a small step of her own module, re-measured old beside new. Never D10(b): a yard on her
main without the key makes her a brig to every handling path (Eng §3.3; D10).

What B3.4 must give her is §12.2.

---

## 1. The module and the generator

### 1.1 Files

| Path | What | Owner |
|---|---|---|
| `tools/ships/neufchatel.py` | the data in the sheets' frame, `to_file`, the checks of §1.5, `particulars()`, `write(out_dir, p)`, `main_topgallant(b, p)`, `build(out_dir)` | B2 (the stub is stage 0's: Build §3.1 item 2) |
| `tools/ships/period.py` | her appends: Adye's 12-pdr carronade and long 6s; Steel's row for "14 Guns, 300 Tons" and the sloops' cables; each with its page (§5.3, §7) | B2, appending in her window (Build §4.2) |
| `data/ships/hermaphrodite-brig.yaml` | generated only | B2, through the generator |
| `data/people/hermaphrodite-brig.yaml` | her wardroom file, hand-written data in the frigate-36's form | B2 |
| `tests/test_neufchatel.py` | her tests and her truths 7-192 and 7-193, drafted there | B2 |
| `freesail/world/ships.py` | her `DESCRIPTIONS` row and her `_DESCRIPTION_WORDS` rows | B2, in her window, as her last step |
| `tests/test_profile.py` | `MODULE_FILES["ships.neufchatel"]` | the stage-0 agent, committed with her first file (§12.1 item 3) |

The file's header is its own literal string and contains "Generated by tools/gen_ships.py"
(`tests/test_fishing.py:99` reads the phrase for the smack) and "(tools/ships/neufchatel.py)", as
the razee's does.

### 1.2 The import

As stage 0 laid it and Indf §1.2 measured twice: `SHIP_MODULES` (`tools/gen_ships.py:8621`)
names her module; it begins `import gen_ships as g` and `from ships import period`, takes every
helper as `g.<name>`, and is imported only by the generator's entry block, after the alias.
`g.wardroom("hermaphrodite-brig")` is called inside `build()`, never at import, so a missing people
file breaks only her build.

### 1.3 What B2 reuses, read-only, and what she writes anew

**Reused** (lines in `tools/gen_ships.py` at 8f30be9):
- `Builder` (`:650-1078`) and its methods, among them `ground_tackle` (`:753`) and `descriptions`
  (`:1003`);
- `ft`, `FT`, `SIDES`, `quarter`, `rope_kn` (`:415`), `design_kn` (`:449`), `DESIGN_WIND_KN`;
  `cloth`, `canvas_note`, `SCHOONER_CANVAS` (`:308`), `BRIG_CANVAS` (`:5887`);
- `square_sail_lines` (`:1533`); `stay_sail_cut` (`:1210`), `staysail_from_cut` (`:1248`),
  `between_the_masts` (`:1297`) with `brig=True`;
- `raked_x` (`:2619`), **always with `deck_m=` her datum, 1.16** (its default is the frigate's 1.8);
- `broadside_pair` (`:3837`) and `chasers` (`:3859`), each with `deck="upper"` and `round_to=0.01`;
  `fit_magazine` (`:3718`), `HIRED_ROUNDS` (`:3707`), `filling_party` (`:3769`);
- `hold_for` (`:3467`), `boat_entries` (`:3478`), `pump_entries` (`:3537`), `ration_entries`
  (`:3635`), `wardroom` (`:3607`);
- the shared notes (`MAGAZINE_NOTES`, `FILLING_NOTE`, `QUARTER_BILL_NOTE`, `PRIORITY_NOTE`,
  `PUMPS_NOTE`, `BOATS_NOTE`, `SHOT_PLUGS_NOTE`, `SMALL_ARMS_NOTE`, `BOARDERS_NOTE`, `HORSE_NOTE`);
- `g.hull_profile` (`:587`); from SW-2b.1, `g.hull_form` (working tree `:691`).

**Written anew in the module**, modelled on the house's lines (`schooner()` and `brig()` take no
particulars and dump themselves, so neither is touched):
- the fore's masts, yards, square sails and their lines on the brig's loop (`brig()`, `:5930-`),
  with her heights and lengths, and a royal above as the brig files hers;
- the fore gaff sail on the topsail schooner's (`:2974-3003`: `fore.gaff`, `fore.sail` class `gaff`
  with no boom, sided sheets and a tack), its sheet shifted round the mainmast in stays as hers is
  (`evolutions/scripts.py:298`);
- the main gaff, boom, mainsail with its horse, and the jib-headed gaff topsail on the schooner's
  (`:3005-3070`);
- the head on the brig's (bowsprit, jib-boom, flying jib-boom; three headsails);
- the studding sails on the brig's three pairs (ids, parents and lines, `:6479-6520`);
- storm canvas on the brig's storm staysail (`:6535-6551`) and the schooner's storm trysail and
  storm jib (`:3226-3240`, `:3255-3270`);
- groups and aliases (§4.8).

### 1.4 The data, the frame and the conversion

- **Data at the head of the module, in the sheets' frame**, each figure with its source in a
  comment: x in feet forward of **the after rabbet at the sailing-trim waterline** (ZAZ6177,
  x 321.6 px), z in feet above that waterline at the station. Her lines, ports, sills, rail,
  deck, stem and stern come from ZAZ6177; her spars, sails and their heights from ZAZ6179, whose
  waterline is level (Neuf §1.2). Named blocks: `LWL_HB`, `WL2_HB`, `WL3_HB` (Neuf §2.4),
  `TOP_BREADTH`, `DEAD_FLAT`, `RAIL`, `DECK_AT_SIDE`, `STEM`, `STERN`, `HEAD`, `PORTS`, `SILLS`,
  `SWEEP_PORTS`, `MASTS`, `SPARS`, `HEIGHTS`, `SAILS`, `KEEL`, `RABBET`.
- **The frame's one join, measured here.** Neuf gives the ports and the masts "forward of the post
  at deck height". That origin lies 0.85 ft (6 px) abaft the after rabbet the lines are measured
  from: the aftmost port's centre, read here at x 370.6 px, is 6.95 ft forward of the rabbet and
  7.8 ft by Neuf; the foremost, at 1032.6 px, 100.85 ft and 101.7. So `POST_AT_DECK_FT = 0.85`
  and `x_from_post(ft) = x_m(ft − POST_AT_DECK_FT)`. Every port and mast of Neuf §2.7 goes through
  it. Task 1's checker confirms it on the end ports (§3.7). Neuf's mast fractions (0.105 abaft the
  middle, 0.30 before it) assumed the rabbet as origin; after the join the main stands 0.112 of
  the waterline abaft the middle and the fore 0.295 before it. The masts' spacing, 43.7 ft, does
  not depend on the join.
- **The file frame.** x in metres forward of the middle of the waterline between the rabbets,
  107.3 ft long (D29(b)): `x_m(x_ft) = (x_ft − 53.65) × 0.3048`, so the waterline runs from −16.35
  to +16.35 m. z in metres above her water at the station. Her water slopes 1.63° to her keel
  rabbet (her 33-in drag); the engine has no trim, so a height above the water at its own station
  is what the engine believes, as Indf §1.4 has it.
- **`to_file(p)`, once:** a lower spar's `height_m` is its height above the water less the datum,
  1.16 m; an upper mast's is its vertical hoist above the cap below; `corners_m` heights above the
  datum; a sail's `centre_height_m` and a gun's `height_m` above the water (Indf §1.4; the file's
  conventions). Every height on ZAZ6179 is vertical above its level waterline, which is what the
  viewer reads (`client/projection.js:503-509`).
- **Rounding.** Profile, sills and hull figures to 0.01 m, early, at the measured value; spar and
  sail figures as the house rounds them, so that a last-bit difference in `math.tan` between
  machines cannot flip a written figure (Indf §16, risk 4).

### 1.5 The checks raised before the file is written

With `raise ValueError(...)` and a sentence, never `assert`, which `python -O` strips:
- the Navy's tonnage rule on Winfield's keel for tonnage and extreme breadth (93 ft 8¼ in and 25 ft
  8 in: 93.6875 × 25.6667 × 12.8333 / 94) within a ton of 328 22/94 (Winfield pp. 335-336;
  measured here 328.3, as Neuf §2.1);
- the masts 43.6-43.9 ft apart at the deck (Neuf §2.7; ZAZ6179's 43.9);
- the eleven port triples a side increasing in x, and every gun of the fit on one within 0.01 m;
- each spar the sheet draws within 2 ft of Fincham p. 78's figure where both exist, but the fore
  gaff, the royal yard and the flying jib-boom, which differ and are noted (D37(a)). A guard
  against a mistyped figure, not evidence that Ex. 1 is her (Neuf §3.4);
- each sail as cut on her spars within ±15% of its area measured on ZAZ6179 (Neuf §3.3's ±10-15%).

---

## 2. The hull block

### 2.1 The figures

| Field | Value | Source and mark |
|---|---|---|
| `length_waterline_m` | 32.7 | D29(b): 107.3 ft between the post's and the stem's rabbets at the sailing-trim line (measured, ±0.5 ft: Neuf §2.4). In the note: 110.1 ft over the post's after side and the gripe's fore side; 110 ft 8 in on deck (Winfield pp. 335-336) |
| `beam_m` | 7.82 | 25 ft 8 in extreme (Winfield pp. 335-336; ZAZ6177's table "25-8?", read, tentative). In the note: 25 ft 4 in moulded (table); the waterline 24.47 ft moulded, 24.8 ft outside the plank (measured) |
| `draught_m` | 3.16 | D38(a), D29(b): 10 ft 4½ in mean to the false keel's bottom at the sailing-trim line drawn on her own lines, "Draught of Water when in sailing Trim" (ZAZ6177, read): 11 ft 8¾ in aft, 9 ft 0 in forward (measured, ±0.25 ft); ZAZ6179 gives about 11.8 and 9.25 independently. About 0.5 ft less if the faint line is the keel's bottom (Neuf §2.3) |
| `displacement_kg` | 288,000 | measured at that line, ±10 t (Neuf §2.5). The weight budget for 130 men, 18 guns and stores, about 315 t (judgement), in the note |
| `gm_m` | 2.1 | D23(a): the metacentre 1.59 m above her line (measured, ±0.15 m); Fincham p. 19's class ratios on Ex. 1 give 2.12 m for a brig of 10 guns and 2.40 for one of 18; the weight budget about 2.2 (judgement). Tuned only within 2.0-2.2 |
| `clr_x_m` | +0.3 to start | the geometric centre of the plane the file counts, −0.80 m without the rudder (measured, Neuf §2.6), with the topsail schooner's tuned lead of 3.5% of her waterline ahead of it (her +0.5 m against a geometric centre near −0.4: `schooner()`'s hull note; judgement for the type). Tuned against the helm (§9) and recorded tuned |
| `lateral_area_m2` | 102 | D29(b): 1,100 sq ft to the false keel's bottom, keel, gripe and post counted, the rudder not (measured, ±5%: Neuf §2.6). 97 on the faint line and 105 with the rudder in the note |
| `hull_speed_kn` | 12.9 to start | D24(a): the topsail schooner's 11.5 (on *Lynx*'s hull, the same type) carried by √(107.3/85) = 12.92 (measured here). Tuned within 12.5-13.9 (§9): 12.5 a little under the brig's 11.5 carried by her length (12.7); 13.9 the 1.34√L rule the schooner's own note calls "too generous" for the type (judgement on both bounds) |
| `deck_height_m` | 1.16 | her flush deck at side at mid-length, 3.8 ft above her line (measured, ±0.3 ft: Neuf §2.7; the red line traced here gives 3.75 ft); Build §5.5's rule for a new file |
| `rudder` | area 2.61, span 3.58, 35°, 4.0°/s | the blade below her line, 28.1 sq ft, its span 11.7 ft to the heel (measured, Neuf §2.6); the angle and the rate the topsail schooner's (judgement; no source gives them) |
| `profile` | §3 | Build §5.1; her shape keys from her first commit (Build §5.6) |

**The masts** stand where ZAZ6177 measures them at the deck, through the join of §1.4: main
−3.67 m, fore +9.65 m, 13.32 m apart; rakes 12.4° and 10.3° from the vertical with her water
level (ZAZ6179, measured; D37(a)). Fincham's Ex. 1 (0.11 and 0.3 of the waterline; 33 and 28 in
in 12 ft) in the note.

**Measured here, from those figures:** her righting moment a degree, 288 t × 9.81 × 2.1 m × sin
1°, is about 104 kN·m, against the frigate-36's 283, the brig's 67 and the topsail schooner's 36;
the wetted area the engine reckons, L(1.7T + 0.7B), 354.7 m² against the topsail schooner's 277.6.

### 2.2 The datum (D18)

Her deck is flush fore and aft (Cobb p. 38, "a flush deck fore and aft", read). The uppermost
continuous deck, the deck she was worked from and her one gun deck are one deck, so D18's
options give the same datum, 1.16 m, and nothing of hers waits on the owner's choice. Cobb's
"trunk of the quarter deck" (p. 103) is read as a raised cabin trunk aft, not a deck (judgement).
It is not in the profile, and its note says so. The step of about 0.8 ft in the red line near the
mainmast (Neuf §2.7, unresolved) is not drawn; its note says so too.

---

## 3. The hull profile and her shape

### 3.1 The form

Build §5.1's form, written by `g.hull_profile(rail, breadth, **parts)` alone, which raises the
schema's own sentence at generation, with stage 0H's shape keys through `g.hull_form(hull, notes,
*, form, marks, measured=...)` from her first commit (Build §5.6: "B2, B4 and B7 write their shape
keys from their first commits"). `g.hull_form` checks each measured port triple against the drawn
side within 0.05 m and writes the drawn displacement beside the filed one (working tree `:691`).
Her one deck is `upper` (Build §5.1: a frigate's, a sloop's and a cutter's single gun deck is
`upper`).

### 3.2 Her points (file frame, metres)

| Line | Points | Source and mark |
|---|---|---|
| `rail_m` | (−17.96, 2.88) the taffrail, (−16.41, 2.56), (−12.97, 2.49), (−10.81, 2.42), (−8.64, 2.40), (−6.48, 2.29), (−3.46, 2.29), (−0.69, 2.36), (2.61, 2.37), (6.05, 2.34), (8.21, 2.40), (10.84, 2.57), (12.97, 2.72), (14.92, 2.77), (16.05, 2.78) the rail's fore end | measured here: the top of her side on ZAZ6177 traced by column, the columns of the mast stumps and deck fittings dropped (±0.3 ft). Neuf's check holds: about 4 ft above the deck at side (Neuf §2.7). **Conflict:** the trace stands about 7.5 ft above the water at the main (2.29 m) and 8.2 ft at the fore (2.49 m), where ZAZ6179 gives about 8.4 ft (2.56 m) at both masts. Task 1 settles it with a checker; until then the lines' figure stands, ZAZ6179's in the note |
| `breadth_m` | [x, at the water, at the rail]: (−16.35, 0.14, 2.58), (−13.30, 1.97, 2.80), (−10.26, 2.93, 3.15), (−7.21, 3.34, 3.43), (−4.16, 3.56, 3.61), (−1.11, 3.68, 3.77), (1.94, 3.78, 3.86), (4.98, 3.70, 3.84), (8.03, 3.52, 3.69), (11.08, 2.95, 3.17), (14.13, 1.65, 2.17), (15.09, 1.00, 1.61), (16.35, 0.14, 0.70) | the water: her sailing-trim waterline's half-breadths at 10-ft stations (measured, ±0.1 ft: Neuf §2.4), the ends 0.3 ft at the rabbets; at 15.09 m, a station added for the rail's last reading, the water taken straight between the 100-ft station and the rabbet, as the form draws it between stations (judgement). The rail: her top-breadth half-breadths by distance from the post (measured, not re-measured: Neuf §2.4), through the join, taken as the rail's (judgement: the body plan draws her topsides near upright; task 4). Neuf's last reading, 5.1 ft at 104 ft from the post, stands at 15.09 m. Forward of it nothing is read: at 16.35 m the rail is 0.70, Neuf's trend from 104 ft to the stem's siding at the stem head (judgement), so the bow is not drawn full to the stem; the stern station's rail is Neuf's 2-ft reading carried 1.15 ft aft (its trend gives 0.03 m less, within the reading). Each with 2 in of plank (Neuf §2.5) |
| `keel_m` | (−15.91, −3.58) the post's heel, (14.71, −2.79) where the gripe leaves the keel | the false keel's bottom (D29(b); the scale bar's border, Neuf §2.3), its depths 11 ft 8¾ in aft and 9 ft 0 in forward at the perpendiculars (measured); the post's heel by its after edge's measured rake, 11-12°, produced to that bottom (measured here). Its fore end's x is the gripe's foot, judged (below), so the line is `judged` until task 2 traces it (§3.5) |
| `stem_m` | (14.71, −2.79), (15.14, −1.55), (15.83, −0.75), (16.35, 0.00), (16.70, 0.92), (16.85, 1.79), (16.83, 2.03), (16.65, 2.35) the stem head | measured here on ZAZ6177 at 5×: the curve drawn from the forefoot to where the head rails meet it, then to where the bowsprit's lower edge crosses the bow. The curve meets her water at the rabbet's x (Neuf's 107.3 ft); whether it is the rabbet or the fore edge above the water is task 2. The gripe's foot at the keel's bottom is judged: the lowest traced point is (14.71, −1.80), and the foot is set straight below it on the keel, where the gripe more likely curves aft as it goes down. So the line is `judged` until task 2 traces the forefoot (§3.5) |
| `stern_m` | (−15.91, −3.58), (−16.61, 0.00) the post's after edge at her water, (−17.07, 1.42) the transom's foot, (−17.96, 2.88) the taffrail | measured here: the post's after edge (the hinge line, Neuf §2.6's 12.1°) at her water, 0.85 ft abaft the after rabbet; the transom's face raking 31° from its foot to the taffrail (§3.5) |
| `section_m` | (−2.50, 0.16), (−2.22, 0.60), (−1.87, 1.24), (−1.53, 1.98), (−1.18, 2.63), (−0.84, 3.12), (−0.49, 3.45), (−0.15, 3.67), (0.00, 3.76), (0.55, 3.85) | the dead-flat section, height above the rabbet against half-breadth (measured: Neuf §2.4), z taken from her line at 8.21 ft above the rabbet there, with 2 in of plank: the straight floor rising 27° and the firm bilge. The 8.21 ft is the body plan's height of her line above its base. The profile's rabbet stands 8.6-8.7 ft below her line at that station (Neuf §2.3-§2.4; `rabbet_m`, §3.5), so the section's foot stands 0.13-0.16 m above the profile's rabbet. It is kept in the body plan's own frame, which gives the section's shape against her line, and the difference is in the note (task 1) |
| `decks_m.upper` | (−16.66, 1.52), (−14.25, 1.45), (−12.97, 1.34), (−8.21, 1.24), (−4.74, 1.05), (−3.03, 1.04), (0.00, 1.16), (2.61, 1.17), (8.21, 1.24), (9.86, 1.34), (12.97, 1.58), (15.56, 1.68), (16.05, 1.71) | the deck at side, the red line: Neuf §2.7's five (stern 5.0 ft, lowest at the main 3.4-3.5, mid-length 3.8, the foremast 4.4, the bow 5.6; measured, ±0.3 ft), and between them traced here |
| `ports_m.upper` | §3.3 | x and sill measured here; half-breadth judgement until task 3 |
| `port_size_m.upper` | [0.81, 0.76] | 2 ft 8 in by 2.48 ft (2 ft 6 in to the inch), the eleven's mean (measured here; the depths re-measured in the review pass by `probe/sills.py`; Neuf's 2.7 by 2.4 ft, ±0.3). The end ports are shallower than the deck's one size, 2.18 ft forward and 2.05 ft aft: drawn at the mean, their tops would stand 2-4 cm above the traced rail at x +14.39 and −14.23. The profile's note says so for package 81, which draws the ports |
| `wales_m` | not written until read | task 6; its absence in the note |

Every point not yet re-measured by B2 is written with its mark in the note and never left out
silently (Indf §3.2). The images' figures go in; the images never do.

### 3.3 The sills and the half-breadths

Eleven ports a side, lids drawn, the same on ZAZ6178 (Neuf §2.7); "pierced for 22 guns, and
mounting 18" (*Naval Chronicle* vol. 33 p. 72, read). Each port's x is Neuf's less the join.
Each sill was measured here as the port frame's lower edge in its middle ten columns (sub-pixel
at the half-maximum; ±0.3 ft). Each half-breadth at the sill is the top breadth at the port's
station with 2 in of plank (judgement until task 3 reads the body plan). It is an upper bound,
so a port shuts a little early at most: the safe side, as Indf §3.3's midship fallback is.

From forward:

| No. | x (m) | Sill (ft; m) | Half-breadth (m) | Shut, heel alone | Neuf's check, deck + 1.3 ft (ft) |
|---|---|---|---|---|---|
| 1 | +14.39 | 6.68; 2.04 | 2.03 | 58.7° | 6.66 |
| 2 | +11.58 | 5.97; 1.82 | 3.07 | 29.6° | 6.14 |
| 3 | +8.72 | 5.20; 1.58 | 3.64 | 20.5° | 5.46 |
| 4 | +6.00 | 5.20; 1.58 | 3.81 | 19.6° | 5.27 |
| 5 | +3.05 | 5.06; 1.54 | 3.87 | 18.6° | 5.16 |
| 6 | +0.12 | 4.92; **1.50** | 3.83 | **18.2°** | 5.10 |
| 7 | −2.74 | 4.94; 1.51 | 3.69 | 19.1° | 4.74 |
| 8 | −5.64 | 4.94; 1.51 | 3.53 | 20.0° | 4.91 |
| 9 | −8.56 | 5.09; 1.55 | 3.35 | 21.8° | 5.40 |
| 10 | −11.37 | 5.39; 1.64 | 3.02 | 26.2° | 5.60 |
| 11 | −14.23 | 5.84; 1.78 | 2.72 | 32.8° | 6.07 |

The two measures agree within 0.31 ft: ports 3 and 9 differ by 0.26 and 0.31 ft, the rest by
0.25 ft or less. Neuf §2.7's "about 4.7 to 5.1 ft above the water amidships" holds. The ports'
depths read here run 2.05-2.81 ft, a mean of 2.48 (Neuf's 2.4 ±0.3); the end ports are the
shallowest (§3.2, `port_size_m`). The eleven sills were re-measured in the review pass by
`probe/sills.py` and came out as the table, to the hundredth of a foot.

- **The stern ports.** Two squares at the top of the transom on both body plans (Neuf §2.7, a
  tentative reading; seen again here). No gun stands in them (§5.2), so they are not triples; the
  profile's note records them for package 81.
- **The sweep ports** (D11(a)): eleven a side, one about 4.6 ft abaft each gun port, 0.7-0.85 ft
  square, at their measured x in the note, not in the profile, which has no key for them.

### 3.4 What the sills give (heel alone, 70's rule `combat/shot.py:116-120`, `PORT_SHUT_M` 0.3048 m; measured here)

| Port | Sill | Shut at (half-breadth at the sill) | (half the beam, 3.91 m) |
|---|---|---|---|
| Hers, lowest (No. 6, amidships) | 1.50 m | **18.2°** | 17.8° |
| Hers, the chasers' (No. 1) | 2.04 m | 58.7° | 26.3° |
| The privateer schooner, for comparison (Build §5.4) | 1.04 m | | 11.6° |
| The brig-sloop on Steel's band (Build §5.4) | 1.22-1.52 m | | 12.3-16.4° |

Rounding her lowest sill to 1.5 m moves nothing (1.50 measured). Under the owner's rule the roll's
amplitude adds to the heel (D12(b); Build §7.1). Cobb has her lee guns "most of the time under
water" in the gale chase of 28 December (p. 97, read): with a roll of ten degrees her lee ports
shut at about eight of heel, so the rule and the account agree. Her truths do not pin that chase;
her line in the package's lee-port truth (7-190) comes after the wiring.

### 3.5 Her shape keys, under §5.0's ladder

Build §5.7's row for her, as approved: "S: three waterlines by station; the dead-flat section
(Neuf §2.4) | square, about 17 ft S; knee to read, T meanwhile; counter, wale and transom face to
read (B2) | ZAZ6177". Each line carries its word in `marks`; a line takes the word of its weakest
point (§5.0 principle 4).

| Line | Rung | Word (`marks`) | What it holds |
|---|---|---|---|
| `rail_m`, `decks_m`, `stern_m` | S | `sourced` | her own lines, measured (§3.2); the rail's conflict with ZAZ6179 in its note |
| `keel_m` | S along its length, T at its fore end | `judged` | the false keel's bottom, measured; its fore end at the gripe's foot, judged (§3.2). The weakest point rules (§5.0 principle 4); task 2 lifts it to `sourced`, old beside new |
| `stem_m` | S from (14.71, −1.80) up, T at the foot | `judged` | the curve as drawn; its foot on the keel judged (§3.2). The note names the foot as the weak point and the rabbet or fore edge question (task 2), which lifts it to `sourced`, old beside new |
| `ports_m` | S for x and sill, T for the half-breadth | `judged` | the weakest point rules: the triples' half-breadths are the top breadth at the station until task 3 lifts the line to `sourced` |
| `breadth_m` | S at the water, T at the rail | `judged` | the rail column is the top breadth taken as the rail's, and forward of 104 ft from the post it is judged (§3.2); task 4 lifts it |
| `section_m` | S | `sourced` | the dead flat (Neuf §2.4) |
| `sections_m` | S | `sourced` | ten stations × three waterlines (the sailing-trim line, WL2 2.63 ft and WL3 5.27 ft below it, parallel: Neuf §2.3-§2.4), each with 2 in of plank, 30 points; e.g. at −1.11 m: (−1.61, 2.00), (−0.80, 3.20), (0.00, 3.68); at +14.13 m: (−1.61, 0.36), (−0.80, 1.00), (0.00, 1.65) |
| `head_m` | S | `sourced` | the knee of the head's fore edge, from where the head rails meet the stem, (16.83, 2.03), to its top, (18.94, 2.74), about 7 ft before the stem (measured here) |
| `rabbet_m` (reserved, not drawn) | S | `sourced` | the keel's rabbet from the draughts to it (Neuf §2.3: 10.1 ft below her water at the post, 7.5 ft at the forefoot): (−15.91, −3.08, 0.11), (+0.23, −2.66, 0.11), (+14.71, −2.29, 0.11), the keel sided 0.7-0.8 ft; kept by principle 11. The rabbet is drawn straight and level on the sheet (Neuf §2.3), so the middle point lies on the line through the two ends (8.74 ft below her line). Neuf's 8.63 ft at that station (x 705 px, §2.4's Cb) agrees within 0.11 ft; the body plan's 8.21 ft (`section_m`) is its base height, 0.4-0.5 ft less, and the note says so. Task 1's checker reads the rabbet's depth at the dead flat on the profile |
| `breadth_line_m` | — | not written | the heights of her top breadth by station are not read; the form's default stands in (Build §5.3 step 2) until task 4 reads them |
| `channel_wales_m`, `floor_m` | — | not written | no channel wale is drawn on her sheets; the rising line is not read |
| `form.fullness` | T | `judged` | [1.0, 1.0], the design's default rule, which fills only below WL3, 5.27 ft down, where nothing is drawn but the dead flat (Build §5.3 step 3) |
| `form.stern` | S | `sourced` | `type: raked`; `knuckle_z_m` 1.42; `transom_hb_m` [2.46, 2.41]; `round_up_m` 0.11; no galleries, no lights |
| `form.head` | T | `judged` | `knee`: the knee and its head rails are drawn; a small terminal at its top is not resolved at 1280 px, so no billet, scroll or figure is drawn (§5.0 principle 9: nothing invented) |

**Her stern, measured here.** On the profile the transom's face runs straight from its foot,
4.65 ft above her water just abaft the post's head, to the taffrail, 9.46 ft above her water and
5.26 ft abaft the after rabbet: 31° from the vertical. Below its foot the post and the rudder run
down; there is no overhanging counter. On the body plan the transom is 16.1 ft across at its top
corners and 15.8 ft at its foot, its top arched about 0.35 ft. That is §5.1's `raked`: "a transom
along `stern_m`'s rake, with no counter". **Plainly:** Build §5.7's row, approved by the lead,
gives her stern "square, about 17 ft". The measure corrects it, and the 17 ft (Neuf §2.4, "not
re-measured") is 16.1 ft at the corners. The row is amended at her merge, old beside new (§17,
lead item 8), by the session in a design-record commit, not by B2, and task 1's checker
re-traces the transom before her first commit. Reed's model
shows the same raked transom (Winfield pp. 335-336's photograph, a modern model, for the eye
only).

**Her head.** A light knee, its head rails rising from the stem to about 7 ft before it. Reed's
model cannot settle the terminal at this size either. If a later reading resolves it, the word
changes and nothing in the game's behaviour does (principle 12).

**The gap check.** `g.hull_form(..., measured=...)` names the triples whose half-breadth is
measured. None is until task 3 reads them on the body plan (their x and sills are measured, their
half-breadths judged). Then `measured=("upper",)`, or a port at a time as `("upper", x)`, and each
must lie within 0.05 m of the drawn side at its sill or the generation fails (Build §5.3). Until
then each gap is reported, not raised. The triples' half-breadths and `breadth_m`'s rail column
both come from the top breadth, so they should agree. Where the drawn side misses a triple by
more, B2 reads the body plan (task 3) before any triple or line is moved, and reports the gap. No
triple is ever taken from the drawing (principle 8). The drawn displacement is reported beside
her 288 t; with three measured waterlines it should fall within the 15% the principles allow, and
over it is recorded, never moved.

**The pair check** (Build §5.6). She is not one class in two roles with any file. Her outline must
differ by 4 px or more in one view from every other file, above all the topsail and privateer
schooners (*Lynx*), whose stern is `raked` too (about 45°, 2.25 m), and the brig-sloop. The check
is B8's test (`tests/test_profiles.py`, from SW-2b.2). If SW-2b.2 has not landed when she is
built, B2 runs it in scratch against *Lynx*'s lines (`pages-chapelle-fig17.md` §5.2) and reports.
Expected to pass (judgement): her deadrise 27° against *Lynx*'s about 30°, her 33 in of drag
against "a great deal", her transom twice as wide and less raked, her knee of the head.

### 3.6 Why the stern and the join matter to the lead

Both move figures the lead approved or that Neuf states. The stern changes one word and three
figures of `form` (drawing only, principle 8). The join puts every port and mast 0.26 m abaft
where Neuf's figures would stand if read from the rabbet; the guns stand on the ports, so it moves
no gun from its port. Neither
moves any behaviour of any existing file.

### 3.7 B2's measuring tasks

On the held 1280-px images (`owner-notes/neufchatel/rmg/`), by the research's registration (the
scale bars; the traced waterlines in `ZAZ6177-hydrostatics/`), with scratch scripts outside the
repository. The figures go in; the images never do.
1. **A checker re-traces** the rail, the deck at side, the transom and the taffrail, and the eleven
   sills, by the research's method (its `trace_*.py`), against §3.2-§3.3's readings; confirms the
   join (`POST_AT_DECK_FT`) on the two end ports; settles **the rail at the masts** against
   ZAZ6179's 8.4 ft; and reads the keel rabbet's depth below her line at the dead flat against
   `rabbet_m`'s 8.74 ft and the body plan's 8.21 (§3.5). A difference over 0.3 ft is reported
   before it is written.
2. **The stem**: separate the rabbet from the fore edge above the water. Neuf's 110.1 ft over the
   post and the gripe puts the fore edge up to about 1.95 ft forward of the rabbet at her water;
   no second line was found there at 1280 px. If none is, the drawn curve stands and the note says
   so. Then trace **the gripe down to the false keel's bottom** (the drafts' `probe/forefoot.png`
   holds the place): if traced, `stem_m`'s foot and `keel_m`'s fore end take the traced point and
   both lines go to `sourced`, old beside new.
3. **The half-breadth at each port's sill**, on the body plan at the port's station, the end ports
   first; then `measured=("upper",)` (§3.5).
4. **The top-timber line** (the rail's half-breadth) and **the top breadth's heights** by station,
   from the body plan and the sheer plan: `breadth_m`'s rail column and `breadth_line_m`; and
   **the top breadth forward of 104 ft** from the post, where nothing is read and the 16.35-m
   station's rail is judged (§3.2).
5. **ZAZ6179's headsails** (the fore staysail, jib and flying jib: stays, tacks, heads and areas),
   its **fore topmast and topgallant studding sails**, and **the main topmast staysail's two
   feet**; then Neuf §8's unfinished Fincham sail-area test (the principal sails against
   9,240-9,410 sq ft) and the centre of effort's height against Fincham's 44 ft. Until then her
   plain sail is uncertain by about ±10%.
6. **The main wale**, if ZAZ6177 draws one.
7. **The bowsprit's heel** (where it enters the hull) and the stem head's height, for the
   bowsprit's root.

None of the shape lines waits on these: each is written now with its mark, and a task done raises
its rung (principle 12), old beside new.

---

## 4. The rig

### 4.1 Masts (ZAZ6179, measured, the yards doubled; D37(a))

| | Fore (a brig's) | Main (a schooner's) | Source |
|---|---|---|---|
| x at the deck; rake | +9.65 m; 10.3° | −3.67 m; 12.4° | measured (ZAZ6177 and ZAZ6179; §1.4) |
| Heel below her water | 6.1 ft | 7.4 ft | measured (Neuf §3.2) |
| Lower mast: heel to hounds; head; overall | 58.4; 10.1; 68.5 ft (20.88 m) | 80.5; 8.4; 88.9 ft (27.10 m) | measured, ±1 ft; Fincham Ex. 1 58.4 and 79.6 hounded, in the note |
| Its cap above her water; `height_m` above 1.16 | 61.3 ft (18.68 m) by length and rake; 17.52 | 79.6 ft (24.26 m), read on the sheet (79.4 by length and rake); 23.10 | measured; arithmetic here |
| Top | a top, a brig's foremast | none: crosstrees, "the first landing place" | Cobb p. 91, read |
| Topmast | 34.8 ft (10.61 m): 29.8 to the hounds and a 5.1-ft head | 39.6 ft (12.07 m): 27.5 to the hounds and a 12.1-ft pole, the pole filed as `main.topgallant_mast` | measured |
| Topgallant | with its royal pole in one, 29.6 ft (9.02 m): 19.3 and 10.4, filed as `fore.topgallant_mast` and `fore.royal_mast` | the topmast's pole (above), bare until `"keyed"` crosses its yard | measured (the fore's upper masts not re-measured: Neuf §3.2) |
| Trucks above her water | 110.4 ft | 110.1 ft | measured |

- The main is a pole mast with crosstrees and no top: "her mainmast towering high in one piece,
  with no top as when square rigged, the cross-trees being the first landing place" (Cobb p. 91,
  read). Cobb calls her main topmast the "top-gallantmast" (p. 91); its note says so.
- **Poles filed as masts.** The fore topgallant and its royal pole are one stick, filed as two as
  the frigate files hers; the main topmast and its pole likewise, as `main.topmast` and
  `main.topgallant_mast`, from the first commit. So the engine's levels (`evolutions/trim.py:98-228`)
  see each yard on its own spar (Indf §4.1), and the viewer draws the main topgallant down to its
  lower yard by `yardBelowId` (`client/projection.js:455`). The notes say each is one stick.
- **Hoists** are the vertical heights between caps (`to_file`), the rake's cosine applied.
- **Stays and shrouds:** the fore channel's seven chain plates a side (four shrouds and three
  backstays, judgement) and the main's three (ZAZ6177, measured).
- Mast ids `fore.` and `main.`; she has no mizen. Her rating pass rates every spar from its loads
  (`Builder.rate_spars`, `:918`).

### 4.2 Yards, gaffs, booms, brace limits, rope

| Spar | Length | Height above her water (above the datum) | Source |
|---|---|---|---|
| `fore.yard` | about 65 ft (19.81 m) | 47.2 ft (13.23 m) | measured, doubled, ±1.5 ft; Fincham 63.25 |
| `fore.topsail.yard` | 46.8 ft (14.26 m) | 78.5 ft (22.77 m) | measured; Fincham 46.52 |
| `fore.topgallant.yard` | about 26 ft (7.92 m); the second round 27.5 | 97.7 ft (28.62 m) | measured; Fincham 26.67 |
| `fore.royal.yard` | about 24.5 ft (7.47 m) | 108.1 ft (31.79 m) | measured; Fincham 21.3. Its odd proportion, 0.94 of the topgallant yard, noted, not changed (D37) |
| `fore.gaff` | 32.9 ft (10.03 m), peaked about 27° | jaws 46.9 ft (13.14 m), peak 61.7 | measured; the peak judgement; Fincham 37.1 (D37(a): hers) |
| `main.gaff` | 37.3 ft (11.37 m), peaked 24° | jaws 64.4 ft (18.47 m), peak about 79.5 | measured; Fincham 37.1 |
| `main.boom` | 64.2 ft (19.57 m) | 10.4 ft at the mast (2.01 m), 16.4 at its end | measured; Fincham 64.46. It overhangs the taffrail 19.6 ft (measured) |
| `main.topsail.yard` (keyed only; carries no sail) | 34.4-35 ft (10.58 m) | 95.7 ft (28.01 m) | measured, doubled, ±1.2 ft; Fincham's main topsail yard 36.3 |
| `main.topgallant.yard` (keyed only) | 23.6-25 ft (7.41 m) | 107.5 ft (31.61 m) | measured; Fincham's main topgallant yard 23.22 |
| Studding-sail booms | beyond the fore yardarm 16.1 ft (4.91 m); beyond the topsail yardarm 6.9 ft (2.10 m); the topgallant yard's by the brig's proportion | | measured; judgement for the third |
| Swinging boom (the lower studding sail's foot) | 43.0 ft (13.11 m) | | Fincham p. 78 (not drawn; judgement for hers) |

- **Heights** are the sheet's, not the frigate's rules: the yards stand where ZAZ6179 draws them.
- **Not carried**, in the notes: Fincham's main square-sail yard (48.4 ft: D10(d), not drawn); "the
  Jack" (§4.6).
- **Brace limits:** the brig-sloop's by level (`brig.yaml`: the fore yard 60°, the royal 66°;
  judgement as hers), the main's two light yards 60° and 62° (judgement). B2 checks the fore yard
  against the lee shrouds from her fore channel's chain plates (ZAZ6177, x 817-927 px), as Indf
  §4.2 does. No source gives hers.
- **The horse** for the main sheet: across her transom, 16.1 ft at its top (measured here), its
  span the transom's inside breadth, about 4.6 m (judgement), by `HORSE_NOTE`.
- **Rope**, per mast: the brig-sloop's line sizes (`FRIGATE_ROPE` × `BRIG_ROPE_SCALE` ×
  `BRIG_MAST_ROPE_FACTOR["fore"]`, `:5926-5927`) for the fore and the head, and the topsail
  schooner's inline circumferences for the main and its gaffs (`:2975-3070`), each scaled by
  √(her sail on that mast ÷ theirs) (judgement, as Indf scales the frigate's). So a line's rating
  grows with the sail it works, and truth 9's strain behaves as the brig's and the schooner's.
  Spar ratings from the rating pass.

### 4.3 Sails (ZAZ6179, measured from the corners, ±10-15%)

| Sail | Area | Notes |
|---|---|---|
| `main.sail` | 2,780 sq ft, **258 m²** | luff 55, head 35, leech 65, foot 62 ft; on the boom (re-measured: Neuf §3.3) |
| `fore.course` | 2,000 sq ft, **186 m²** | 33.3 ft deep, its foot 14 ft above her water |
| `fore.topsail` | 1,700 sq ft, **158 m²** | 30.8 ft deep |
| `fore.sail` (the fore gaff sail) | 1,660 sq ft, **154 m²** | §4.4 (re-measured) |
| `fore.topgallant` | 580 sq ft, 54 m² | 18.6 ft deep |
| `main.staysail` | 530-540 sq ft, 50 m² | its head 60 ft above her water (re-measured) |
| `main.gaff_topsail` | 470 sq ft, 44 m² | class `jibheaded` (D10's note; Chapelle pp. 174-175: the American form nearly jib-headed); its 4.3-4.6-ft head spar recorded, not modelled |
| `main.topgallant` (keyed only) | 300 sq ft, 28 m² | §4.5 |
| `fore.royal` | 250 sq ft, 23 m² | set flying, as the brig's royals (judgement) |
| Fore lower studding sail | about 19 by 35 ft, 62 m² | drawn solid (§4.7) |
| `fore.staysail`, `jib`, `flying_jib` | working figures 93, 121 and 56 m² | judgement until task 5: the first two close Fincham's remainder of 2,200-2,400 sq ft for the jib and the fore topmast staysail (Neuf §2.8) |

- **Plain sail** (decision 14) is 810 m² without its two headsails and about 1,024 m² with the
  working figures (measured here; judgement on the headsails). That is about 23.5 m² a
  tonne^(2/3), against the topsail schooner's 17.2, the brig's 13.8 and the frigate-36's 13.5
  (measured here on the committed files). She carries more canvas for her weight than any file in
  the game, and her sources agree: Rankine's rules exceeded (Neuf §3.3); her prize crew blamed "the
  too large size of her masts and spars, in comparison to her hull" (Cobb p. 138, weak).
- **Canvas** by Steel's numbers for sloops and cutters, as the schooner's `SCHOONER_CANVAS`, and
  `BRIG_CANVAS` for the square sails.
- **Cut.** The square sails are their trapezoids on her yards, cut by the brig's method; the
  measured area within ±15% (§1.5).
- **Reefs:** the fore course 2 and the fore gaff sail 2 (Cobb p. 95: "a double reefed foresail";
  which foresail is not said, so both can take two); the fore topsail 3 (the brig's); the mainsail
  3 ("closely reefed", Cobb p. 95; the schooner's 3); the gaff topsail, the topgallants and the
  royal none. **The jib** none: Cobb's jib was "closely reefed" too (p. 95), but no evolution reefs
  a jib (`data/evolutions/` holds `reef_square`, `reef_gaff`, `reef_lug` and `reef_bowsprit` only).
  Her storm jib stands in for the reefed jib (§4.8). By the brief, a rig the engine lacks is
  reported to the lead (§17, lead item 7), not approximated silently.

### 4.4 The fore gaff sail (D21(a))

To her plan, boomless and loose-footed, lapping the main: gaff 32.9 ft, luff about 37.9, leech
about 50.2, foot about 46.6 ft drawn curved; 1,660 sq ft (±10%); its clew 2.7-2.9 ft abaft the
mainmast's line and 12.6 ft above her water; its jaws just below the fore yard (measured: Neuf
§1.2). It is Cobb's "fore-and-aft foresail" (pp. 33-34, 79), under which she lay to in the gale.
- **Built** on the topsail schooner's foresail (`gen_ships.py:2974-3003`): `fore.sail`, class
  `gaff`, roles `mast` and `gaff`, on `fore.mast` and `fore.gaff`, no boom, `corners_m` from the
  measured corners; its centre by the schooner's rule (0.4 of the foot abaft the raked mast), its
  height from its corners; throat and peak halyards, sided sheets and a tack; its sheet shifted
  round the mainmast in stays (`evolutions/scripts.py:298`), as the schooner's is.
- **"Foresail" is the course.** Cobb's men lashed "the foresail, on the windward yard-arm" (pp.
  106-107) and spoke of having "sheeted down the foresail and filled away" (p. 105). So her alias
  "foresail" goes to `fore.course`, as the brig's, not to `fore.sail` as the topsail schooner's
  (`:3362`). The gaff sail takes its own words (§4.8).
- **The viewer** draws every gaff at 35°, where hers peak at about 27° (fore) and 24° (main), and a
  loose foot 1.5 m above the datum (`LOOSE_FOOT_HEIGHT_M`), where hers runs about 2.7-3.8 m above
  her water: the viewer's standard (Eng §6.1, §6.3), recorded, not asked of B5.

### 4.5 The main topgallant (D10)

**The sail on her plan.** Two light square yards on the main topmast's pole: the lower at the
topmast hounds, 95.7 ft above her water, 34.4-35 ft doubled; the upper near the truck, 107.5 ft,
23.6-25 ft; a square sail about 11.8 ft deep between them, about 300 sq ft (ZAZ6179, measured: Neuf
§1.2). Reed's model shows a small square sail at the main masthead (read; a modern model).
Fincham's p. 78 has the two yards as a main topsail yard (36.3 ft) and a main topgallant yard
(23.22 ft), and a main square-sail yard of 48.4 ft beneath, which her plan does not draw (D10(d),
not taken).

**Filed at `"keyed"`:**
- `main.mast` with `schooner_mast: true` (§12.2);
- `main.topsail.yard`, class `yard`, on `main.topmast`, at its measured height and length, carrying
  no sail: the topgallant's sheets go to its arms. It has lifts and braces as a yard's and is
  rated for the topgallant's sheet load. It is filed because her plan draws it and the sail's foot
  is sheeted to it; without it the viewer's `bareFoot` (`projection.js:455-462`) would draw the
  foot from the sail's centre, losing a drawn spar (§5.0 principle 1);
- `main.topgallant.yard`, class `yard`, on `main.topgallant_mast`, with a halyard;
- `main.topgallant`, class `square`, on the upper yard, its foot at the lower yard's arms, no reef
  bands, 28 m², lines by `square_sail_lines`;
- in "all sail", "light sails" and "square sails", its two yards in "main yards" and "after
  yards" (§4.8); never in "plain sail", "topgallants", "topsails" or "courses". Her gaff topsail
  beneath it is a light sail, and a topgallant set above a furled
  gaff topsail by "set the topgallants" would be inconsistent aloft (judgement). So her polar,
  which sets plain sail (`world/ships.py:410-418`), does not count it.

Her hands for it: the fore top's, as for her gaff topsail, by `topmen`'s rule for a mast with no
top (`crew/hands.py:104-108`; she has no `main_top` station). B2 records what `Quarters.beat` and
the evolutions make of it.

### 4.6 The head, and "the Jack"

- **Bowsprit** about 22.4 ft outboard, stem to cap, steeved about 15° (measured: Neuf §1.2; 14.9° on
  ZAZ6177 for the drag; Fincham's 36 in in 12 ft, 14.0°, in the note); housed 9.0 ft (Fincham's
  0.35 of the breadth; judgement for hers). **Jibboom** 38.7 ft heel to end. **Flying jibboom**
  about 11 ft beyond it (±3 ft), its end 57.2 ft ahead of the stem head (measured; Fincham's 15.6
  noted).
- **Headsails:** a fore staysail, a jib and a flying jib (D35: "the three headsails drawn ... the
  count is tentative"). Their stays, tacks and areas are task 5; until read, the working figures of
  §4.3, cut by the schooner's rule on her spars (judgement, marked).
- **"The Jack"** (Neuf §1.2): a spar under the bowsprit near its cap, 14.6-15.0 ft as drawn or 30 if
  halved, the lower studding sail's leech running down to it. Not built: D8(b) as answered named the
  64's and the bilander's yards only, and the engine's yards under the bowsprit are B3.2's for
  those. Its note says what it is and where. The lower studding sail's foot is spread by Fincham's
  swinging boom (§4.2) in the engine's usual way.

### 4.7 Studding sails and light sails (D35(b), limited)

- **The fore lower studding sail**, drawn solid, about 19 ft wide and 35 deep (62 m²), on the fore
  yard's boom (16.1 ft beyond the yardarm) and the swinging boom.
- **The fore topmast studding sail**, drawn dashed, on the topsail yard's boom (6.9 ft beyond); its
  size by the brig's proportions on her spars until task 5 reads the outline (judgement).
- **The fore topgallant studding sail** (the owner's choice; partly made out on ZAZ6179): by the
  brig's proportions on her spars (judgement), task 5.
- Each on the brig's ids, parents and lines, a pair a side. None on the main (none drawn).
- **The main topmast staysail**, "large", its luff on the main topmast stay to the fore topmast
  crosstrees, its leech vertical just forward of the main; its foot drawn dashed at two heights,
  45 and 73 ft above her water. **The upper foot is taken** (judgement): at 73 ft it clears the
  fore gaff sail's peak, 61.7 ft, so both can stand; at 45 ft it would lie over the gaff sail. Both
  are in the note (D35: "the build picks one of the staysail's two drawn feet and marks it"). Cut
  by `stay_sail_cut` and `staysail_from_cut` on her geometry.
- **The main staysail** (50 m², its stay from the main masthead to the foremast near the deck)
  shares the space between the masts with the fore gaff sail; she would set one or the other
  (judgement). It goes in "lying-to staysails", "staysails between the masts" and "all sail", never
  "plain sail". The engine's blanketing (`physics/sails.py:122-124`) does not keep two sails in one
  plane from both drawing; B2 measures what the polar and the heave-to make of it and records it.
- **Not carried:** the ringtail and the water sail of the topsail schooner's pattern. Her sources
  show neither, and the owner limited her light sails (D35(b)).

### 4.8 Storm canvas, groups, aliases

- **Storm canvas** (Cobb, read): in the gale "the top-gallantmasts were housed and the yards on
  deck" (p. 78, OCR l. 3106); she lay to under the fore gaff sail (p. 79), then scudded under
  bare poles at about ten knots (p. 90), then lay to "under her storm-staysail only", "close
  reefed as it was" (p. 91, OCR l. 3647-3648);
  on the 28th she had every yard on deck but the fore and fore topsail yards (p. 93), under a
  double-reefed foresail, a closely reefed mainsail and jib (p. 95). Filed in the sail room
  (`bent: false`): `fore.storm_staysail` (the brig's, `:6535-6551`), `storm_trysail` on the main
  gaff and boom `in_place_of` the mainsail, and `storm_jib` `in_place_of` the jib (the schooner's,
  `:3226-3240`, `:3255-3270`). The evolutions `send_down_topgallant_masts`,
  `send_down_topgallant_yards` and `strike_topmasts` serve the housing.
- **Lying to.** `lie_a_try` lies her under the close-reefed fore topsail and the staysails and keeps
  her gaff sails, as a schooner (`data/evolutions/lie_a_try.yaml`'s head). Cobb's lying to under the
  fore gaff sail alone is recorded, not built: no path lies a vessel to under a gaff foresail, and
  T4 is not pinned.
- **Groups**, with the names the engine reads (map-generator fact 11), on the brig's and the
  schooner's patterns:

| Group | Members |
|---|---|
| "plain sail" | `fore.course`, `fore.topsail`, `fore.topgallant`, `fore.sail`, `main.sail`, `fore.staysail`, `jib` |
| "courses"; "topsails" | `fore.course`; `fore.topsail` |
| "topgallants"; "royals" | `fore.topgallant`; `fore.royal` |
| "square sails" | the fore's four, and `main.topgallant` when keyed |
| "headsails"; "jibs" | `fore.staysail`, `jib`, `flying_jib`; `jib`, `flying_jib` |
| "gaff sails"; "fore-and-aft sails" | `fore.sail`, `main.sail`; those with the headsails, staysails and gaff topsail |
| "staysails between the masts" | `main.staysail`, `main.topmast_staysail` |
| "studdingsails", and by level | the six |
| "light sails" | `fore.royal`, `main.gaff_topsail`, `flying_jib`, `main.topmast_staysail`, the studding sails, `main.topgallant` when keyed |
| "lying-to staysails" | `main.staysail` (the brig's pattern, judgement) |
| "storm canvas"; "storm staysails" | the three; `fore.storm_staysail` |
| "all sail" | every sail but the storm canvas |
| "yards", "fore yards", "head yards", "lower yards", "topsail yards", "topgallant yards", "royal yards" | as the brig's, on the fore |
| "main yards", "after yards" | when keyed only: the two light yards |

  B2 reads which group names the engine reads by name before it files any it does not.
- **Aliases**, in her sources' words: "foresail" and "fore course" → `fore.course`; "fore-and-aft
  foresail", "fore gaff sail" and "gaff foresail" → `fore.sail` (Cobb pp. 33-34, 79); "mainsail"
  and "fore-and-aft mainsail" (Cobb p. 95) → `main.sail`; "gaff topsail" and "main gaff topsail" →
  `main.gaff_topsail`; when keyed, "main topgallant" and "main topgallant sail" → `main.topgallant`.

### 4.9 Her rig's peculiarities, for the physics' reading (the brief)

| Peculiarity | Sail class | In the engine | Said for the lead |
|---|---|---|---|
| A brig's square fore under a schooner's main | `square` on the fore, `gaff` on the main | **yes**: she classes as a fore-and-after (`_masts_with_yards` the fore alone), the topsail schooner's handling with four fore yards (Eng §3.3's trial A) | — |
| The great fore gaff sail lapping the main | `gaff`, loose-footed | **yes**: the topsail schooner's foresail | its overlap with the main staysail (§4.7) |
| The main topgallant on two light yards | `square` | **no**: any yard on the main makes her a brig to every path | D10(a)'s key, B3.4 (§12.2) |
| Hove to, that topgallant stays set abaft the backed fore | `square` | the heave-to clews up light sails forward of the backed yards only (`light_sails_forward_of`, `evolutions/scripts.py:584-609`) | a finding for B3.4's measure (§12.2 item 8) |
| The gaff topsail's small head spar | `jibheaded` | the head spar is not modelled | recorded |
| The jib reefed | `jib` | **no**: no evolution reefs a jib | §17, lead item 7 |
| Lying to under the fore gaff sail | `gaff` | no path lies a vessel to under a gaff foresail | recorded |
| "The Jack" | — | not built (D8) | recorded |
| Sweeps | — | not modelled (D11(a)) | recorded |
| Running in a heavy sea, the frigates gaining as she pitched (Cobb p. 97) | — | **no**: the hull's added resistance acts in a head sea only (`physics/motion.py:111-118`) | recorded, not pinned |

---

## 5. The guns

### 5.1 The fit

| Fit | Guns | Source |
|---|---|---|
| **"as taken 1814"** (the default, and her one fit) | 16 × 12-pdr carronades and 2 long 6-pdrs, 18 in all; no pivot | Winfield pp. 335-336 (the Admiralty's record, undated; most likely as taken, since she was never commissioned: D22(a), judgement). The count agrees with Niles vol. VII p. 284 (18 guns sailing from Boston, 21 December 1814), Cobb p. 39 (eighteen) and *Naval Chronicle* vol. 33 p. 72 ("pierced for 22 guns, and mounting 18"); James vol. 6 p. 237 (OCR l. 12393-12394) gives 18 in October |

- **The name.** "as taken 1814": the record most likely describes her as taken (D22, judgement);
  the house names fits by their year ("ardent class 1784", "as carried 1796").
- **Cobb's calibres in the fit's note.** "The brig mounted eighteen guns, of nine and eighteen
  pounders" (p. 39, read): one witness, 26 years on, and no other source gives them. The note also
  gives 17 guns in October (Niles vol. VII p. 120; Coggeshall p. 241), 14 by her log (Stevens p.
  26), and the 12-lb bags of musket balls of the boat action (Stevens p. 27), which fit 12-pdr
  carronades (judgement). One fit, by D22(a): a second only if a scenario asks for one. No other
  armament is sourced for her, so the scenario editor is offered no other degree (brief item 4).
  `unarmed` is not hers.
- **No pivot.** No source mentions one and none is drawn; none of the three sheets is a deck plan,
  so the absence is weak (Neuf §2.7, §4.1). SW-4's pivot rule (Build §9.2) is not needed.
- **Small arms:** blunderbusses, muskets and boarding pikes (Coggeshall p. 241); her double shot
  with "canister shot and bags of musket balls" (Coggeshall 1861 p. 468; Stevens p. 27), grape to the
  engine. In the note.

### 5.2 Places, numbers and the deck

From forward, each side:

| Port | Gun |
|---|---|
| 1 | long 6-pdr, the bow chaser (`chaser.bow.starboard`, `chaser.bow.larboard`, place `bow`) |
| 2-9 | 12-pdr carronades, Nos. 1-8 |
| 10, 11 | empty |

- **The 6-pounders as bow chasers** (judgement, by D22's leave). The Admiralty's record of her
  reads like a brig-sloop's ("16 × 12-pdr carronades and 2 × 6-pdrs"), and the brig-sloop's file
  stands its two 6s at the bow as chase guns (`brig_armament`, `gen_ships.py:4421-4450`;
  `brig.yaml`'s `chaser.bow.*`). A privateer's long guns are her chase guns, to bring a prize to at
  long shot. No bow port is drawn on her, so they stand in the foremost broadside port, where the
  side is fine (half-breadth 2.03 m) and a gun trains well forward. The other reading, stern chasers
  in the two squares at the transom's top if those are ports (Neuf §2.7, tentative), and the
  broadside reading, one 6 a side among the carronades, are in the owner's judgement list (§17).
- **The empty ports** (judgement): the two aftmost, by the cabin trunk and the tiller under the
  main boom's sweep. "Mounting 18" in 22 ports leaves four empty in all. No source places her guns;
  Cobb's chase has her fire one gun, to leeward, as the signal of surrender (p. 104).
- **Built** with `g.broadside_pair` and `g.chasers`, `deck="upper"` and `round_to=0.01`, each gun's
  `x_m` and `height_m` its port's triple (§3.3) to the centimetre (truth 7-185), then `crew`
  reassigned (§5.3), as Indf §5.2 reassigns it (assigning an existing key keeps the key order).
  Numbered from forward, as the house numbers. One deck, so a deck-aware pair key the 74 may bring
  does not reach her.
- **The stern ports** take no gun (§3.3).

### 5.3 Patterns, weights and crews

| Piece | Pattern and weight | Crew | Source |
|---|---|---|---|
| 12-pdr carronade | 2 ft 2 in, bore 4.52 in, **5 cwt 3 qr 10 lb** (5.84 cwt, 297 kg) | 4 | Adye 1804 p. 72 (read here on the page image, IA leaf n95). Douglas 1829 art. 136 for the crew (`DOUGLAS_CARRONADE_CREW`) |
| Long 6-pdr | **8 ft 0 in, 22 cwt** (1,118 kg) | 5 | Adye 1804 p. 155 (read here, IA leaf n178): the 6-pdr of 8 ft 22 cwt, or of 6 ft 16 cwt 2 qr. The longer taken (judgement: the reach a chase gun is carried for); the shorter in the note. Falconer 1780, QUARTERS (`FALCONER_CREW[6]`) |

- **Her appends to `period.py`**, with their pages: `ADYE_CARRONADE_CWT[12] = 5.84` (5 cwt 3 qr 10
  lb) and `ADYE_LONG_GUN_CWT[6] = {(8, 0): 22.0, (6, 0): 16.5}`. The shared tables give a 12-pdr
  carronade of 6 cwt and a long 6 of 20 cwt (`gen_ships.py:3677-3678`, from memory). They feed the
  eight files and stay as they are (Build decision 11), so no figure of the eight moves.
- **Crews by the period**, as the 64's and the 74's are: one side's guns, a chaser included, take
  37 men (8 × 4 + 5). The generator's own rule (`gun_crew`, `:3691`) gives the 6 six men; the
  period's figure is the one written. The weight enters only the cycle and the dismount (Indf §5.3).

### 5.4 The magazine

- `g.fit_magazine(guns, {"long": HIRED_ROUNDS, "carronade": HIRED_ROUNDS})`: 40 round, 6 grape and
  4 chain a gun, the privateer schooner's allowance (judgement: a private ship of war's magazine
  smaller than a King's). Below she was cleared for prize goods, "except the water and provision
  casks" (Cobb p. 40). The bags of musket balls she fired are grape to the engine.
- **Charges:** the engine's shares give Table No. 29's figures exactly for both her calibres: a
  12-pdr carronade 1 lb (a twelfth), a long 6 2 lb (a third) (Build §10; Adye p. 72 gives the
  carronade's 1 lb too, read here). SW-1's table serves her the same when it lands; nothing is
  overridden.
- **Exercise charges:** none. The Regulations bind King's ships; the privateer schooner has none.
- **Filling:** `filling_party` gives 4 (18 cannon, one to every four: Falconer 1780,
  QUARTER-GUNNER).

### 5.5 Broadside weight by 70's rule (measured here)

`far_ship` counts one side's broadside guns and every gun not on the broadside
(`combat/far.py:97-122`): hers is 8 × 12 + 2 × 6 = **108 lb**. The brig-sloop escorting her
scenario's convoy fires 268 lb by the same rule (eight 32-pdr carronades a side and her two 6-pdr
chasers), and the frigate-36 421 lb (Indf §5.5). She is no match for a frigate's broadside, which
her history bears out: she ran from frigates and fought boats. With the 6s on the broadside, one a
side, the figure would be 102 lb; as stern chasers, 108.

---

## 6. The company, the marines, the quarter bill and the people file

### 6.1 The company, 130 (D36(a))

"From Boston, 18 guns, 130 men" (Niles vol. VII p. 284, 31 December 1814, read); 130 in Collier's
report as reprinted (snippet). Emmons's 127 (p. 190), James's "120 or 130 men" in October (vol. 6
p. 237, OCR l. 12394, read here) and Cobb's 163 "all told" (p. 39) are in the note. Her "large
crew for prizes" (the brief) is this company: about seven men a gun, with nine prize-masters to
take her prizes in. Sending a prize crew away is 74's (`combat/action.py:515`).

| Station | Count | Basis |
|---|---|---|
| Posts | 12 | the captain, five lieutenants (first to fifth), the master (Cobb's "sailing-masters"), the surgeon, the boatswain, the gunner, the carpenter and the sailmaker. "Besides the captain, we had five lieutenants, nine prize-masters, quarter-masters, sailing-masters, boatswains, gunners, carpenters, and sail-makers in profusion" (Cobb p. 40, OCR l. 1448, read here), one of each warrant; the surgeon, Cobb pp. 75-76 (below). Their mates are petty officers in the stations (judgement) |
| Marines | 16 | Cobb was put "with seven others" in the long boat at quarters, with muskets: "the first intimation I had of being drafted into the marine corps" (p. 73, read); Coggeshall counts "officers and marines" (p. 241). At least eight; sixteen is judgement, the long boat's eight and as many forward |
| Idlers | 8 | a cook, a steward (Cobb's "purser's steward", p. 75), two of the carpenter's crew, one of the sailmaker's, a cooper, an armourer (her blunderbusses, muskets and pikes), a servant (judgement) |
| Seamen: forecastle, fore top, afterguard, waisters | 20, 24, 30, 20 (94) | judgement: four fore yards and the studding sails for the fore top; the great mainsail and the gaffs for the afterguard. No main top (Cobb p. 91), as the schooner's |

- **The surgeon.** Cobb has a "doctor" who took the one berth left, "that of surgeon", came aboard
  just before sailing and kept to the cabin until the capture; their skill was doubted aboard and
  their diploma, by hearsay, not their own (pp. 75-76, OCR l. 2964-2999, read here). So she carried a
  surgeon by post. Package 73's sick list then runs as on a ship with one.
- **The nine prize-masters** (Cobb p. 40) are counted among the afterguard's able seamen, one drawn
  by name in her people file (§6.3). Cobb counts them among the officers; as posts they would stand
  on the quarterdeck as officers and never haul (`crew/muster.py:179`), and each post needs an
  outline (`tests/test_wardroom.py:42-57`). Prizes are package 74's, which takes its prize crews
  from her company of 130. Cobb p. 40's list stays in the note and in the owner's judgement list
  (§17).
- **Ratings** 0.35 able, 0.35 ordinary, 0.30 landsmen (judgement). The privateer schooner's are 0.45,
  0.40 and 0.15, a privateer shipping prime seamen. Her December crew was not: the prize money of
  her last cruise "proved an attraction too alluring to be resisted by many, who otherwise never
  would have gone to sea" (Cobb p. 39), and Cobb was a green hand.

### 6.2 The marines

Sixteen, the file's `crew.stations.marines`, a small-arms division at quarters apart from the guns
(§6.4). No marine officer: none is named in any source read. Cobb's "marine corps" were landsmen
with muskets (p. 73), not a detachment as a King's ship's, and the note says so. The kit is the
scenario's nation's (`data/nations.yaml`: the United States' `marines: {kit: basic}`; Build §9.4).

### 6.3 The people file (`data/people/hermaphrodite-brig.yaml`; B2's, hand-written data)

The frigate-36's form (`data/people/frigate-36.yaml`), the posts in order:
- **the stations bound by role:** captain → the captain; officer of the watch → the first
  lieutenant; master → the master;
- **drawn at muster:** a prize-master `{station: afterguard, rating: able}`, a quartermaster (Cobb
  p. 40's "quarter-masters") and a boy `{station: afterguard, rating: landsman}` as the captain's
  messenger;
- **the outlines**, under the owner's question 3 (§17): her December crew's as Cobb gives them,
  in the file's own words and with no names, for Cobb names none:
  - **the captain:** her first lieutenant on her former cruises, given the command when her late
    captain fell ill (p. 40); French by birth and American "for convenience", small of stature,
    came aboard only when all was ready and kept below until the chase (p. 41);
  - **the first lieutenant:** never an angry or profane word, feared for exactness rather than
    temper, knowing each hand's duty and never setting more than a hand can do (p. 41);
  - **the surgeon:** a stranger to all aboard, who kept to the cabin (pp. 75-76);
  - the officers "in profusion", mild in harbour and harsh at sea (pp. 40-41);
  - the rest plain types, traits and histories judgement in the period's words where the sources
    give them (her people "on shares, from the captain down", Cobb p. 39).

**Plainly:** D39's recommendation added that her outlines fix no nationality. The captain's French
birth is her one witness's fact of her last crew, and it suits her under American or French colours
alike. Put to the owner (§17, question 3). If declined, every outline is a plain type with no birth
given. A scenario names Ordronaux or Millin by `people:` (`world/people.py:548-571`).

Her own test file runs `tests/test_wardroom.py:42-57`'s check on her file (no builder edits a
shared test list: Build §4.1).

### 6.4 The quarter bill (set against the default fit)

| | Count | Basis |
|---|---|---|
| Men at one side's guns, the chaser included | 37, all seamen | §5.3 |
| Trimmers: forecastle, fore top, afterguard | 9, 11, 15: **35** | the brig-sloop's 27 (`brig.yaml`'s bill) scaled by her plain sail against the brig's, about 1,024 m² against 766 (measured here, 1.31 to 1.34), split by each mast's work: the head sails, the fore's four yards, the main sheet and the gaffs (judgement) |
| Helm | 1 | a tiller (judgement, as the privateer schooner's) |
| Powder | 2 | two waisters (the privateer schooner's, judgement) |
| Filling | 4 | Falconer's rule (§5.4) |
| Priority | sail before guns | `PRIORITY_NOTE`; the privateer schooner's; her trade was running and chasing |
| Small arms | 26 | her sixteen marines and ten seamen: a fifth of her company, the privateer schooner's share (8 of 40), judgement; Coggeshall p. 241's blunderbusses and muskets |
| Boarders | 85 | about two thirds of her company, the privateer schooner's share (26 of 40: "a privateer's company boards almost whole"), judgement |

- **The marines stand apart from the guns** (judgement): her musketry, and her seamen are enough to
  man one side (37 of 94). Indf §6.4 has the King's marines take the carronades first; hers do not.
- **B2 measures `Quarters.beat` at muster** (`crew/quarters.py:155-242`) on the default fit, and
  records whether every gun crew fills, the trimmers by station and the small-arms division.

### 6.5 Her names and her nation

`crew.names: american` (the brief, with D27 and D39 taken with it). `NAMES_TO_NATION` maps the list
to the United States when a scenario names none (`world/nations.py:40`, `:172`). Her file carries
no nation (plan §0). As D39 says, no names list leaves a file wholly without a nation, since every
list implies a default; a scenario's `nation:` wins. Her company's mixed nations (Cobb p. 42;
Stevens p. 27) are in the note.

---

## 7. Ground tackle, boats, pumps, hold and stores

**Ground tackle** by Steel 1794 vol. I (read here on the page images, IA leaves n127 and n117): the
anchor table's row for "14 Guns, 300 Tons", the nearest to her 328 tons, and the cordage table's
"Sloops" column. The cordage table has no column for 14 guns: it goes from "20 guns" (six bower
cables of 14½ in) to "Sloops" (five of 13½ in). The "Sloops" column is taken for a vessel of 14
guns and about 300 tons (judgement); the "20 guns" column is in the note. Through
`b.ground_tackle(note, anchors, chain=False)` (`:753`):

| Id | Kind | Weight | Cable |
|---|---|---|---|
| `best_bower` | bower | 20 cwt, 1,016 kg | 240 fathoms (two cables) of 13½ in |
| `small_bower` | bower | 20 cwt | 240 fathoms of 13½ in |
| `sheet` | sheet | 20 cwt | 120 fathoms of 13½ in |
| `stream` | stream | 7 cwt, 356 kg | 120 fathoms of 8 in |
| `kedge` | kedge | 3 cwt 2 qr, 178 kg | a hawser of 6¾ in (half the bower cable, the house's rule, judgement) |

Steel's three anchors and five cables, laid two, two and one (judgement: Lever's "three Cables on the
best Bower, two on the small" is a ship of the line's, Indf §7). Her append to `period.py`:
`STEEL_ANCHORS[14]` with the row's figures (3 bowers of 20 cwt, a stream of 7, a kedge of 3.5; 5
bower cables of 13½ in, a stream cable of 8 in) and its pages. Steel's table is the Navy's; no
source gives a privateer's. It is the period's own table on her own tonnage, where the house's rule
(`ground_tackle_for`, Luce 1866) is a later writer's: the house prefers Steel (D33). The rule's
figures for her go in the note beside Steel's.

**The rest:**
- **Boats:** "the long boat, which stood amidships of the deck" (Cobb p. 73, read; damaged by the
  sea of p. 93), and a yawl at the stern (judgement: Reed's model shows a boat there, a modern
  model). By Luce's rule on her length, through `boat_entries`, as the privateer schooner's long
  boat and yawl.
- **Pumps:** "the pumps" (Cobb p. 55, read): two hand pumps, the privateer schooner's (judgement
  for the kind), through `pump_entries`.
- **Hold:** `hold_for(b, 328, False, ...)`, the trader's share, about 164 t: her hold was "cleared
  away underneath the deck, except the water and provision casks" for prize goods (Cobb p. 40). A
  ship of war's share would give 33 t; she was a privateer, built to fill.
- **Stores** (judgement): water a gallon a man a day for two months, about 35 t; provisions three
  months (her 1814 cruise ran from Cherbourg on 4 July to Boston on 15 October: Stevens p. 26; Niles
  vol. VII p. 120); cordage, spare spars and shot plugs as the brig's on her own spars, one plug a
  gun of the fit; the sail room by the schooner's method; `ration_entries` as the privateer
  schooner's, which `tests/test_stores.py:28` asks of every file.

---

## 8. Far description, vessel type, size rank and roles (D15(a))

**In her file**, `b.descriptions(...)` (`:1003`):

| Key | rig | what | roles |
|---|---|---|---|
| `hermaphrodite brig` | "a brig" | "a hermaphrodite brig, a brig's foremast and a schooner's main, long and low, pierced for eleven guns a side" | [privateer] |

Its note: "hermaphrodite rigged" (Niles vol. VII p. 120; Cobb p. 38; Coggeshall p. 241); Rankine
via Chapelle p. 164; "lying low in the water" (Cobb p. 38); "pierced for 22 guns" (*Naval
Chronicle* vol. 33 p. 72); the Admiralty's "American Schooner" (ZAZ6177, ZAZ6179) and Winfield's
"schooner"; her log's "privateer brig" (Stevens p. 26); the tops make out a brig (D15(a)).

- **No `fit`** on the description: her one fit is her file's default, and a far vessel takes a
  description's fit only where it is not the default (Build §8.1).
- **The roles.** `privateer` only, a role of `ROLES` (`world/captains.py:133`) with its book
  (`data/captains/privateer.yaml`). `Builder.descriptions` at 8f30be9 writes `rig`, `what` and
  `note` only, so her module sets `roles` on the mapping after the call, the key
  `file_descriptions` reads (stage 0). Where SW-4 has widened `descriptions` when she is built, she
  passes it there instead; the file's bytes are the same. A far ship of hers sails the privateer's
  book when her scenario gives `role: privateer`, or by her intent (`role_of_vessel`); `brains.py`
  is not hers and is not edited.
- **The vessel type** is `ship.rig: hermaphrodite brig` (Build §3.3), free text served on
  `/api/ship` (`api/queries.py:437`) and read by nothing that branches.
- **Rank 2**, laid (`world/captains.py:286`). Her words hold "brig", which `_SIZE_WORDS` ranks 2
  before "schooner", and `size_of_words` reads only the words before the first comma ("a
  hermaphrodite brig": 2, probed here). None of her words is a man-of-war word (`MAN_OF_WAR_WORDS`,
  `:190-198`).
- **Her rows in `world/ships.py`, in her window** (Build decision 15), her last step (§13 step
  6). **Plainly:** Build decision 15 lands the row with her file. Here it is her window's last
  commit, because Build §4.2 passes `world/ships.py` to SW-4's rows first, and those wait for
  B1's window to close and for 84's step 7 (the lead, 2026-10-29). Her file and her rows still
  land in her one merge. Until the row is in, `description("hermaphrodite brig")` raises
  (`d = dict(DESCRIPTIONS[key])` comes first, `world/ships.py:327-339`), so whatever reads the
  index waits for step 6 (§14). The order is the lead's (§17, lead item 3). The rows:
  - `DESCRIPTIONS["hermaphrodite brig"] = {"file": "data/ships/hermaphrodite-brig.yaml", "rig": "a
    brig", "what": ...}`;
  - `_DESCRIPTION_WORDS`: "a hermaphrodite brig" and "an hermaphrodite brig" (Cobb's own, p. 23),
    "a privateer brig" and "privateer brig" (her log, Stevens p. 26; James vol. 6 p. 237, OCR l.
    12393, "the American privateer brig"), each → `hermaphrodite brig`. The bare key resolves
    itself.
  - **Probed here** with her key patched into `DESCRIPTIONS` in memory: without these rows "a
    hermaphrodite brig", "an hermaphrodite brig", "a privateer brig" and "privateer brig" all give
    "merchant brig", because `description_key` strips the article and then tries the tails shorter
    than the words, so a two-word phrase meets only "brig". "An American hermaphrodite brig" gives
    hers by its tail.
  - **Not** "a brig", which stays the merchant brig's (§18).
- None of her words appears in any existing text but `SIZE_RANK` and `tests/test_profile.py:920`
  (grep over `freesail/`, `data/`, `tests/`), so her rows move no existing ranking or lookup.
- **The privateer schooner stays beside her** (Build §9.5): another hull, of class 1.

---

## 9. The polar: what B2 measures and records

**Measure** `polar_of` on her file (`world/ships.py:471`): the speeds at 8, 15 and 25 kn, 40° to
180°; `closest_deg`; `beat_deg(15)` and `beat_deg(25)`; and the sailed figures at 90° in 15 and 25
kn (speed, heel, helm). Record them beside the frigate-36's, the brig's and the topsail schooner's.
Test it in `tests/test_neufchatel.py` in `tests/test_ships.py:74-93`'s form, with her own figures,
±0.5.

**Measured here on the committed files** (`polars.py`, and again for this design):

| File | Best in 8 / 15 / 25 kn | At | 180° in 25 kn | 60° / 70° in 15 kn; in 25 kn | `closest_deg`; `beat_deg(25)` |
|---|---|---|---|---|---|
| frigate-36 | 4.62 / 8.19 / 11.63 | 90°, 90°, 100° | 9.23 | 4.29 / 6.14; 7.03 / 9.62 | 50; 60 |
| brig | 4.57 / 7.92 / 10.97 | 100° | 8.84 | 4.26 / 5.88; 6.89 / 9.10 | 50; 60 |
| topsail-schooner (and privateer-schooner) | 4.59 / 7.92 / 10.95 | 100°, 90°, 90° | 8.50 | 6.47 / 7.16; 9.43 / 10.17 | 40; 50 |
| razee-44 (stage A) | 4.41 / 7.93 / 11.54 | 90°, 90°, 100° | 9.00 | — | 50; 60 |

**The finding.** Every file's best point lies on a reach, 90-100° off the wind, under plain sail
with no studding sails, and each falls by a fifth or more by 180°. The polar is plain sail, flat
water, no heel. Cobb's 12.5 knots was "running off" in the gale chase (p. 138; T2), above the
polar's top wind of 25 kn, and "running off at the rate of twelve and a half miles per hour" out
of Boston with the yards squared (p. 54; T3, the unit loose: 10.9 kn if statute miles). So **her
accounts' 12.5 knots, which were running, cannot be her polar's best point by its angle.**

**Two stand-ins, measured here** (probes, not her file):

1. The topsail schooner's and the brig's files given her hull block and every sail scaled so that
   their plain sail is 950 m² (`standin.py`). Her best in 25 kn, and her speeds at 60° and 70° in
   15 and 25 kn (the 60° and 70° figures measured in the review pass, `verify/nowave.py` and
   `verify/closest.py`):

| Hull speed | 12.0 | 12.5 | 13.0 | 13.5 | 14.0 |
|---|---|---|---|---|---|
| On the schooner's rig: best in 25 kn | 11.68 | 11.90 | 12.12 | 12.23 | 12.43 |
| its 60° / 70° in 15 kn | 6.89 / 7.55 | 6.92 / 7.61 | 6.94 / 7.67 | 6.96 / 7.72 | 6.98 / 7.76 |
| its 60° / 70° in 25 kn | 10.16 / 10.68 | 10.32 / 10.87 | 10.48 / 11.04 | 10.63 / 11.20 | 10.75 / 11.36 |
| On the brig's rig: best in 25 kn | 11.35 | 11.56 | 11.77 | 11.95 | 12.12 |
| its 60° / 70° in 15 kn | 4.48 / 6.07 | 4.48 / 6.09 | 4.49 / 6.10 | 4.49 / 6.11 | 4.49 / 6.12 |
| its 60° / 70° in 25 kn | 7.23 / 9.38 | 7.26 / 9.47 | 7.29 / 9.55 | 7.32 / 9.63 | 7.34 / 9.70 |

   `closest_deg` was 40 on the schooner's rig at every hull speed and 50 on the brig's.

2. The topsail schooner's file in memory with her hull block, her masts, her measured sails, a fore
   course on a 65-ft yard, the main topgallant's two yards and the headsails at §4.3's working
   figures (`probe_polar.py`; GM 2.0, the masts by the buildability draft's 1.5-ft join, 0.2 m aft
   of this design's; judgement):

| Case (25 kn) | Best | At 150° | At 180° | Closest; at 60° and 70° in 15 kn; in 25 kn |
|---|---|---|---|---|
| `hull_speed_kn` 11.5 | 11.64 kn at 100° | 9.71 | 9.18 | 40°; 6.33, 7.00; 9.28, 10.11 |
| 12.5 | 12.12 at 100° | 9.97 | 9.38 | 40°; 6.40, 7.09; 9.55, 10.42 |
| 13.5 | 12.56 at 100° | 10.18 | 9.54 | 40°; 6.44, 7.15; 9.78, 10.69 |
| 12.5, the fore gaff sail out of plain sail | 11.69 at 100° | 9.68 | 9.09 | 40°; 5.54, 6.40; 8.56, 9.71 |
| 12.5, the fore course out of plain sail | 11.67 at 90° | 9.56 | 9.06 | 40°; 6.46, 7.11; 9.63, 10.41 |
| 12.5, D10(c) (no main topgallant) | 12.03 at 100° | 9.85 | 9.32 | 40°; 6.45, 7.10; 9.61, 10.41 |
| The frigate-36, for comparison | 11.63 at 100° | 10.01 | 9.23 | 50°; 4.29, 6.14; 7.03, 9.62 |

Her own rig lies between the first stand-in's two (a brig's fore, a schooner's main), and the
second, with her own sails, lies near its schooner row. Her best in 25 kn is about 11.4-12.6 kn
across both, at 90-100°, and dead before it about 9.1-9.5 kn.

**Her pointing against the frigate-36, the margins** (measured here). On her own sails (the
second stand-in) she is faster than the frigate at 60° and 70° in both winds: by 2.1 and 0.95 kn
in 15 kn and 2.5 and 0.8 kn in 25 kn at `hull_speed_kn` 12.5. The margin is slimmest at 70° in
25 kn, and with the fore gaff sail out it falls to 0.1 kn there. The brig-rigged stand-in, her
other bracket, is faster at 60° only: at 70° it falls short of the frigate in 15 kn at every hull
speed (6.07-6.12 against 6.14) and in 25 kn below a hull speed of 13.5 (9.38-9.55 against 9.62).
So 7-193's 70° clause holds if her file sails as her own sails did, and fails if she sails nearer
the brig's rig. If her file misses it after tuning within bounds, it is reported, not forced (§14).

**Running at 12.5 knots is out of the engine's reach for her.** With the resistance law's wave term
removed altogether (`physics/hull.py`, `resistance`: the factor 1 + (u / hull speed)⁴), the second
stand-in's run before the wind in 25 kn rises to about 10.2 kn (10.21 on `probe-all-12.5.yaml`,
measured here by `verify/nowave.py`; 9.8-10.2 across the other cases). That is an upper bound,
since her thrust before the wind falls as she gains on it. The same change takes her best point
to 16.2 kn at 100°, so tuning toward 12.5 running would raise her beam reach far past every
account.

**Targets** (D24(a); each judgement, banded on her accounts):
- her best in 25 kn within **11.5-13.0 kn**, wherever the engine puts it (Cobb's 12.5 kn twice; the
  lower edge a knot below for p. 54's loose unit and p. 138's reefed gale; the upper half a knot
  above). The band is fixed only when her file is measured (§13 step 5), and put to the owner (§17,
  question 1). **Plainly:** D24(a) asks that she be tuned to make "about 12.5 kn running". The
  engine cannot give it (above), so the band is set on her best point and the angle is reported.
  The band's floor alone does not rank her above the frigate-36 on a reach (11.63); her accounts do
  not rank her so running either (p. 97: the frigates gained on her running). The clause that ranks
  her is her pointing;
- her `closest_deg` no wider than the frigate-36's 50°, and her speed at 60° and 70° in 15 and 25 kn
  above the frigate-36's (4.29, 6.14; 7.03, 9.62): "we could haul closer upon the wind than the
  enemy", and on the wind she gained to windward of them (Cobb p. 96, T1, her strongest evidence).
  The margins are above: 0.8 kn at 70° in 25 kn on her own sails, and short of the frigate at 70°
  on the brig-rigged stand-in. "At least 10° inside the frigate's" (40°, the schooner's) is
  recorded if measured, not pinned: the brig-rigged stand-in gave 50°;
- **not pinned:** the best point's angle (reported); her speeds at 150° and 180° (reported); the
  frigates gaining on her running in a heavy sea (p. 97: no added resistance in a following sea,
  §4.9); her crew's opinion (T6); her damaged passage (T7); about ten knots scudding under bare poles
  (T4: no polar under bare poles).

**The knobs, in this order:** `hull_speed_kn` within 12.5-13.9; `clr_x_m` for the helm (balanced
close-hauled in 15 kn and a few degrees of weather helm on a beam reach, as the schooner was tuned:
`schooner()`'s hull note; the helm's truths 6 and 17 as Indf tuned the razee); `gm_m` only within
2.0-2.2, against a measured heel; the brace limits only with a source. Each tuned figure is recorded
beside its start. **Realism, not pacing:** if she misses a band at the edge of its knob's bounds, B2
reports it with the figures and does not force it.

**Also measured and recorded, not pinned:** her heel at 90° in 15 and 25 kn under plain sail beside
the frigate-36's (T5: she took in light sails aloft as the wind freshened while the frigates held
theirs, Cobb p. 96); the strain on her lines at 90° in 25 kn under plain sail (truth 9's behaviour);
her tack, wear and heave-to at seed 7 in 15 kn beside trial A's (149 s, 449 s, 50° off at 2.65 kn:
Eng §3.3), at `"out"` and again at `"keyed"`.

---

## 10. The lee ports: what her file supplies

Per broadside gun and chaser, a sourced sill (`height_m`, equal to its port's triple), and per port,
in the profile, the half-breadth at the sill (§3.3). B8's wiring reads them (Build §7): the dip is
the heel to the gun's side plus the roll's amplitude; a port shuts at a foot above the water and
reopens six inches clear. Her lowest shuts at 18.2° of heel alone (§3.4); she has one deck and one
band, 18-22° amidships. Her roll is her own through `world.motion` (`Firer.roll_deg`); a crewed
ship's roll stays nought until 84 gives each hull her sea (Build §7.1), so her truth line is sailed
as the player's ship. Her lines in 7-190 come after L3.

---

## 11. Where she sails

### 11.1 Her scenario (B6's; D27 and D39 taken with the brief)

Build §12.2: an American privateer of 1814 in the western Channel, a convoy of four under a
brig-sloop working up from the Lizard (plan §3; package 72's convoy; Neuf §5.1).

**The year and the month: August 1814, settled here.** D27 with the brief and Build §12.2 leave the
year to her design. She was in the Channel and the Irish Sea in August and September 1814, taking
many prizes (Niles vol. VII p. 120), and on 21 August sank a brig by broadside in the Irish Channel
(Niles vol. VIII p. 111). Her spring cruise of 1814 off the French coast (prizes into Havre in
April: Niles vol. VI pp. 150, 368) would need Britain and France at war until the spring's peace,
with rows not yet read. The choice is told to the lead (§17, lead item 6), not put to the owner.

**What B6 needs of her:**
- her file and description key, `hermaphrodite brig`; her fit unnamed (her one fit is her default);
- `nation: united-states` on her ship; the role `privateer` for a far ship of her description;
- the scenario's `nations:` block (§11.2), since `data/nations.yaml` stands at June 1805 with the
  United States at peace and issuing no letters (`as_of: 1805-06-01`; `letters_of_marque: false`);
- her colours: in the last chase "the brig carried no colours, nor showed any emblem of the country
  she hailed from" (Cobb p. 104, OCR l. 4204, read here); her signals root the United States',
  `{root: basic, system: basic}`, the brief's "71's basic signals system";
- her date range for any scenario, 1813 to December 1814 (built 1812-13; taken 28 December 1814:
  Winfield pp. 335-336); her wardroom file;
- the drivers' command-line ship: D48's third way (the lead's item 3, B6's) gives a ship lacking a
  scenario's named fit her own default; hers names none.

### 11.2 The scenario's `nations:` block (Build §12.1; ruled in, laid in her stage 0b)

The block replaces the table's wars and letters for that World, so every war in force is listed and
every peace is an absence. The rows her scenario needs, with what has been read for them:

| Row | Figure | Source and mark |
|---|---|---|
| `as_of` | August 1814 (the day B6's) | her Channel cruise (Niles vol. VII p. 120; vol. VIII p. 111) |
| War: Britain and the United States | since 1812-06-18 | James vol. 5 p. 253 ("the three years that followed, the 18th of June, 1812"; OCR l. 13043) and p. 360 (the war "declared by the United States"; OCR l. 18514): read (OCR) here |
| Britain and France | at peace: the treaty "signed at Paris on the 30th of May, 1814" | James vol. 6 p. 229 (OCR l. 12000-12001): read (OCR) here |
| The war's end, beyond her scenario | the treaty signed at Ghent on 24 December 1814, ratified at Washington on 18 February 1815 | James vol. 6 p. 236 (OCR l. 12349-12351): read (OCR) here; her capture on 28 December falls inside the war |
| Letters of marque | the United States against Britain; Britain against the United States | from memory: **open**, her scenario's notes say so, as the lead ruled |
| Spain, Denmark, the Netherlands (the Batavian Republic's successor), Portugal | at peace with Britain by August 1814 | from memory: **open**, each row's comment saying it is not checked against James |

The block's form and reading are Build §12.1's: the loader validates the ids as `nation:` is
(`world/scenarios.py:390-401`), and the World replaces the table's wars and letters with the
scenario's where it loads the table (`core/world.py:747-754`). Inert while no scenario carries it.
None of these dates is in `data/nations.yaml` yet.

### 11.3 What is built with her, common to any scenario

Her file with its fit, her description and role, her people file, and a test that she sails under
rules captains at seed 7 in a world with no named fit (`make_world(7, <her file>, Scenario())`), as
Indf §11.2's. The scenario file itself is B6's, on `first-action.yaml`'s shape.

---

## 12. Interfaces

### 12.1 Her stage 0b (behaviour-free; each item checked to change nothing)

At the opening of her window, after the fresh merge of the lead's head (Build §2.1, §3.3), the
stage-0 agent lays, each item checked by an agent that did not write it (Build §3.4):

1. **D10(a)'s key in the schema** (`freesail/ship/schema.py`, the stage-0 agent's for the whole
   package: Build §4.1), on the pattern stage 0E laid for `heave_to_aback`:
   - `SparSpec.schooner_mast: bool | None = None` beside `heave_to_aback` (`schema.py:471`), left out
     of the checkpoint's state while None (the pattern at `:474-478`);
   - parsed by `_schooner_mast(s, where, source)` in `_parse_spar` (`:1586-`), `true` or refused in
     words, as `_heave_to_aback` (`:1681-1690`);
   - refused in `validate` (beside `:1943`), in words: on a spar that is not a lower mast ("only a
     lower mast takes 'schooner_mast'"); on a mast that carries a yard on it ("a schooner's mast
     carries no lower yard; 'main.yard' is on it"); on every mast that carries yards ("one mast with
     yards stays a square-rigged mast: her head yards are its");
   - a fixture `schooner_with_main_topgallant()` in `tests/rig_fixtures.py` (the topsail schooner in
     memory with a fore course and the two main light yards, Eng §3.3's trials) loading with the
     key; in `tests/test_rig_classing.py`, the guards that no file carries `schooner_mast` and the
     three refusals.

   **When:** at B3.4's boundary if B3.4 opens before her window ("a later need goes back to a
   stage-0 commit": Build §4.1), so that B3.4 builds on a key that loads; else at her window's
   opening. Inert: no file carries the key, and the runtime field and its readers are B3.4's (§12.2).

   **Plainly:** Build §3.3 lays the key in the schema and in `Spar`, as stage 0E laid
   `Spar.heave_to_aback` and `Ship.under_bowsprit` inert. Here the runtime field
   (`Spar.schooner_mast`) and the predicate (`Ship.on_schooner_mast`) are B3.4's, because Build
   §4.2 passes `ship/parts.py` and `ship/graph.py` to B3 after 0E and no stage-0 commit reopens
   them. Nothing reads either before B3.4. Lead item 1.
2. **The scenario's `nations:` block** (Build §12.1, the lead's item 6): `world/scenarios.py` reads
   `nations: {as_of, wars, letters_of_marque, source}` and validates the ids as `nation:` is
   (`:390-401`); `core/world.py` replaces the table's wars and letters with the scenario's where it
   loads the table (`:747-754`). Inert while no scenario carries it. Her rows are §11.2's, B6's to
   write.

   **When:** Build §4.2 passes `world/scenarios.py` to B6 first, for D48's third way (ruled in:
   the lead's notes, the gate's item 3), merged before stage 0b, and only then to stage 0b. At
   8f30be9 that change is not in (`tests/test_scenarios_75.py` does not exist). So item 2 waits for
   B6's D48 change to be merged, or for the lead's word that item 2 goes first and B6 merges onto
   it (§17, lead item 4). Items 1 and 3 do not wait on it.
3. **`MODULE_FILES["ships.neufchatel"] = ["hermaphrodite-brig.yaml"]`** in `tests/test_profile.py`
   (`:502-507`). The hook test asserts that each built module writes its own files and a stub none
   (`:525-532`), so this row is committed directly before her first-file commit at the same
   boundary, the test run on the pair, as 9454fd6 was before B1's stage A (614d2d4).

Nothing else: her `DESCRIPTIONS` and `_DESCRIPTION_WORDS` rows are hers (Build decision 15);
`SIZE_RANK` is laid; `names: american` and the United States' basic marines' kit exist; no pivot
needs SW-4's rule.

**Already laid, nothing more needed:** her module stub and `SHIP_MODULES` name; her size rank;
`DECK_WORDS`'s `upper`; the profile and gun `deck` keys (stage 0); the shape keys (0H); the
description's `fit` and `roles` read (stage 0 item 22); the two-way byte test.

**The checks** (Build §3.4): the eight files and the *Indefatigable*'s two byte-identical (the two-way
byte test, `tests/test_ship_particulars.py:555-`); the golden classing table
(`tests/test_rig_classing.py`); the key's three refusals in words and the fixture loading; every
pickle byte-identical; every existing scenario loading and round-tripping as before (no `nations:`
block in any); the fast tier green; the diff read for any reach beyond its list, any `world.ship` or
`CrewedWorld` read the Hull does not keep, any model or vendor name.

### 12.2 What B3.4 gives her (the engine's fourth step; the lead's item 7)

The lead's ruling: "D10(a)'s key for the *Neufchatel*'s main topgallant: yes, built by B3 as its
fourth step beside `under_bowsprit` at places 1 and 3 of §4.2, inert until her file uses it."
Proposed form, for the lead (§17, lead item 1):
1. **The runtime field** `Spar.schooner_mast: bool = False` (`ship/parts.py`, beside
   `heave_to_aback` at `:219`), copied from the spec (beside `:256`) and left out of the pickle while
   false (the pattern at `:222-226`).
2. **The predicate** `Ship.on_schooner_mast(part) -> bool` (`ship/graph.py`, beside `under_bowsprit`
   at `:183`): true for a spar of class `yard` whose `mast_of` carries `schooner_mast`, and for a
   square sail whose yard is one; a dict lookup on the chain memo.
3. **Place 1, `_masts_with_yards`** (`evolutions/scripts.py:472-478`): a yard on a schooner's mast
   does not make its mast one with yards. So her head yards are the fore's, and
   `after_square_yards` (`:494-501`), `yards_to_back` (`:504-523`), `yards_to_back_set`,
   `after_gaff_sails` (`:553-581`, its `with_yards` at `:570`), `_boom_mainsails` (`:6747`), the
   heave-to's fore-and-after test and the getting-under-way's take her as a fore-and-after with
   yards on her fore.
4. **Place 3, `_square_rigged`** (`physics/sails.py:852-866`): such a yard is not counted, so the
   helm's mark and the gale's reduction (`orders/storm.py:382-384`) take her as a fore-and-after and
   keep her reefed mainsail, as she kept it on 28 December (Cobb p. 95). The cache is kept as it is.
5. **Left as they are** (read; judgement: right for a light yard worked by its own braces):
   - `working_yards` (`scripts.py:466-469`) keeps her main yards, so the brace orders, "trim sails"
     and the polar's trim (`world/ships.py:421-438`) brace them;
   - `head_and_after_yards` (place 2, `:481-491`) puts them in the after list, so they swing at
     "mainsail haul" in stays, follow the wind in the wear, and are kept full and braced up hove to;
   - `light_sails_forward_of` (place 7, `:584-609`), `trim`'s levels (places 5 and 6) and "shorten
     sail" (place 8) are untouched.
6. **The physics is unchanged**: the main topgallant's force is a square sail's at its own `x_m` and
   centre height; `_spar_x` unchanged.
7. **Tests** in B3.4's own file (`tests/test_schooner_mast.py`): the golden classing table unmoved;
   the fixture classed as trial A with the key and as trial B without it; the predicate false on
   every yard of every committed file; the pickle without the field as before.
8. **The measure** (a trace, the lens check): the fixture's tack, wear and heave-to at seed 7 in 15
   kn with the key, against trial A's 149 s, 449 s and 50° off, and the log's words. Two findings
   are to be measured, not assumed:
   - the swing at "mainsail haul" on a schooner's main (place 2 left), its time and its log line;
   - hove to, her main topgallant stays set abaft the backed fore, since the heave-to clews up light
     sails forward of the backed yards only (place 7). In her gale the light yards were on deck
     (Cobb p. 78), so it does not bear on her accounts; but a set topgallant abaft the backed fore
     may lie her a point closer. If the swing costs more than a tenth on trial A's tack, or the
     topgallant moves the heave-to beyond truth 12's band, or a word does not suit a schooner's
     main, **B3.4 reports it to the lead with the figures before adding any place, never silently.**
9. **The guard set** at the step (Build §14.2) and the pace: the predicate runs in manoeuvres and once
   into the cached `_square_rigged`, nothing a tick.

**Her golden row** (§14) at `"keyed"`: `_masts_with_yards` the fore alone; not square-rigged; head
yards the four fore yards; after yards the two main light yards; `yards_to_back` the fore's;
`after_gaff_sails` none (fewer than two masts with yards).

### 12.3 What the viewer builder (B5) is asked

- Nothing new. Her profile, raked transom, knee and ports are drawn by B5.1's and B5.6's builders as
  built for every file (Build §6).
- Her rig with today's classes: the fore course before the fore mast and the gaff sail abaft it (the
  brig-sloop's main course and spanker the precedent); the main topgallant down to its dry yard
  (`yardBelowId`); the lifts on every yard (B5.1).
- **Recorded, not asked:** the gaffs at 35° and the loose foot at 1.5 m above the datum (§4.4); the
  overlap of the fore gaff sail with the main staysail.
- The testing report's pictures (§13), by B5's sheet tooling (`FreeSailApp.picture` in
  `client/app.js`, or the same drawing rendered headless outside the repository).

### 12.4 What B6 is given

Her description key and file; her fit and its default; her date range, 1813 to December 1814; her
wardroom file; her colours and signals root; the `nations:` block's rows and their marks (§11).

---

## 13. File ownership, and the road

**B2 owns:** `tools/ships/neufchatel.py`; `data/ships/hermaphrodite-brig.yaml` (generated) and
`data/people/hermaphrodite-brig.yaml`; `tests/test_neufchatel.py`; in her window, her `DESCRIPTIONS`
and `_DESCRIPTION_WORDS` rows in `freesail/world/ships.py`, the one edit she makes under
`freesail/`, and appends to `tools/ships/period.py`. **B2 never touches:** `tools/gen_ships.py`;
`freesail/ship/schema.py` and `tests/test_profile.py`, `tests/rig_fixtures.py`,
`tests/test_rig_classing.py` (the stage-0 agent's, §12.1); B3's files (`ship/parts.py`,
`ship/graph.py`, `evolutions/`, `physics/sails.py`, `orders/`); `client/`; `combat/`; the eight
files and the *Indefatigable*'s two, `privateer-schooner.yaml` among them; `tests/test_ships.py` and
the other shared test lists; anything under `docs/agents/consent/`. Her truths are drafted in her
test file and moved in Phase 5; her tuning notes are text in her branch's report (Build decision 23).

**Her window** opens at B1's merge: the lead merges the *Indefatigable* whole, and by the owner's
direction of 2026-10-29 the build goes on without holding for the owner's own test. It opens with the
fresh merge of the lead's head and her stage 0b, and closes with her merge.

**The road.** Every step ends with `py tools/gen_ships.py <scratch>` from the tree root, a `cmp` of
every committed file against the scratch, and `load_ship` on hers. The fast tier runs once at the
end, with the slow tier of the files touched (Build §2.5; one suite at a time on the owner's
machine); the whole suite is the lead's.

| Step | What | Proves | Waits on |
|---|---|---|---|
| 0 | The fresh merge of the lead's head; her stage 0b, items 1 (if not laid at B3.4's boundary) and 2 (§12.1) | nothing changes (§12.1's checks) | B1's merge; for item 2, B6's D48 change to `world/scenarios.py` merged (Build §4.2), or the lead's word that item 2 goes first and B6 merges onto it (§17, lead item 4) |
| 1 | The measuring tasks (§3.7), scratch scripts outside the repository, with a checker | the rail, the transom, the sills, the join; the end ports' half-breadths; the headsails | — |
| 2 | The module: data, frame, the checks of §1.5, the hull block, the profile and shape keys, the masts, yards and square sails, the fore gaff sail, the main, the head; `MAIN_TOPGALLANT = "out"` unless B3.4 is in. Stage 0b's item 3 committed directly before it | her file loads, rates and polars; the gaps reported (asserted for each measured triple); her classing a fore-and-after with four fore yards | 0, 1 |
| 3 | Staysails, studding sails, storm canvas, groups, aliases | every group the engine reads by name exists | 2 |
| 4 | The fit, the magazine, the quarter bill, the crew, the people file, stores, sail room, ground tackle, boats, pumps, hold; the description with its roles; `period.py`'s appends | `Quarters.beat` fills every gun crew; the round trip at seed 7 | 2-3 |
| 5 | Tests and truths but those that read the index; the polar measured, tuned within bounds, recorded; heel, helm, strain, tack, wear and heave-to measured; the pair check (in scratch if SW-2b.2 is not in) | §14, 7-192 with its description clause read from her file, 7-193 | 4 |
| 6 | Her `DESCRIPTIONS` row and words in `world/ships.py`; the index's tests (§14); 7-192's index clause | her description resolves through the index; her four phrases give her key; rank 2; "a brig" unchanged | 5; SW-4's rows merged, or the lead's order (§17, lead item 3) |
| 7 | **After B3.4 merges:** `MAIN_TOPGALLANT = "keyed"`, her file regenerated, re-measured | old beside new: her classing (the golden row), polar, 7-193's measures, rating, balance, tack, wear, heave-to | B3.4 and its schema key |
| 8 | The lead's head in again before reporting (the lead's notes, "stage 0 read", item 2); **her testing report** to the owner; reported done; the lead merges | — | 5, 6 (and 7 if B3.4 is in) |

**Her testing report** (the owner's direction of 2026-10-29 for the *Indefatigable*, taken to hold for
her by judgement: §17, lead item 4), at step 8:
- **pictures** at 960 × 720 (Build §6's sheets): abeam to leeward, ahead, astern, on the quarter at
  135°, and heeled 10° seen from windward; under plain sail and furled; the hull alone beside the
  topsail schooner and the brig-sloop at one scale, and the same three hulls normalised to one
  length, beam and freeboard so that only the lines differ (Build §6's sheets; there her raked
  transom and knee are told from *Lynx*'s); the page's panel at 800 × 600 once; her rung letters
  under her;
- **her figures:** her particulars beside their sources (§2.1); her polar beside the frigate-36's, the
  brig-sloop's and the topsail schooner's, with the best point's angle and her running speeds; her
  heel at 90°; her tack, wear and heave-to beside trial A's; her shut heels; her broadside by 70's
  rule; each tuned figure beside its start;
- **what is not done or not measured**, plainly: D10's flip if B3.4 is not in; any task of §3.7 left
  open; any band missed; the pair check's result and how it was run.

---

## 14. Tests and truths

**Her tests** (`tests/test_neufchatel.py`), in the band form with the source in a comment
(`tests/test_ship_particulars.py:93-104`'s form):
- her hull block against ZAZ6177 and Winfield; her profile's points, sills and half-breadths against
  §3.2-§3.3; eleven port triples a side, increasing in x; every port gun on a triple of `upper` within
  0.01 m, naming its deck; her stern `raked`, her head `knee`, a mark on every shape line;
- her spars against ZAZ6179 (masts ±1 ft, yards ±1.5 ft, booms and gaffs ±0.7 ft) and Fincham where
  taken; her sails against ZAZ6179's areas (±15%); the fore gaff sail's clew abaft the mainmast's line
  by 0.8-0.9 m (±0.3);
- her fit, guns, crews and filling against Winfield, Adye, Douglas and Falconer; her company, posts,
  marines and people file against Niles and Cobb (`tests/test_wardroom.py:42-57`'s check); her ground
  tackle against Steel's row;
- her description in her file, at step 5: `file_descriptions(<her file>)["hermaphrodite brig"]`
  gives rig "a brig", her `what`, the roles `[privateer]` and no `fit`; `SIZE_RANK` 2 and
  `size_of_words` of her rig words 2;
- her description through the index, at step 6 with her rows (§8): `description("hermaphrodite
  brig")` names her file with those words; `description_key("a hermaphrodite brig")`, `("an
  hermaphrodite brig")`, `("a privateer brig")` and `("privateer brig")` give `hermaphrodite brig`;
  `("a brig")` still gives `merchant brig`. Before her rows these give "merchant brig" or raise
  (probed here, §8), so they cannot run at step 5;
- her names resolving (`test_period_names_resolve`'s form on her phrases,
  `tests/test_ship_particulars.py:470-552`);
- **her golden row:** `_masts_with_yards` the fore alone; not square-rigged; head yards the four fore
  yards; `yards_to_back` the fore's; `after_gaff_sails` none; after yards none at `"out"`, the two main
  light yards at `"keyed"` (§12.2);
- `MAIN_TOPGALLANT`: `"out"` gives no yard on the main; `"keyed"` (after B3.4) gives her main's two yards
  on a schooner's mast;
- her polar in `tests/test_ships.py:74-93`'s form with her own figures, ±0.5;
- the round trip under rules captains at seed 7 with no named fit (§11.3).

**Truths** (Build §15: 7-192 and 7-193 reserved for her). States, counts, ticks and bands only, never a
digest (decision 26). Written against the names the Hull keeps where a world is made (`world.ship`,
`world.motion`, `world.sea`, `world.clock`), never `isinstance(..., CrewedWorld)`. Both are
arithmetic on her file (`load_spec`, `file_descriptions`, `description`, `polar_of`: "the same
on every machine", `world/ships.py:471-474`), so neither depends on the machine.

1. **7-192: the *Prince de Neufchatel*'s particulars hold their sources.** Pinned at step 5 but
   for its index clause, which is added at step 6 with her rows (§8, §13).
   - Her file loads; `ship.rig` "hermaphrodite brig"; LWL 32.7 ± 0.2 m (107.3 ft between the rabbets,
     ZAZ6177); beam 7.82 ± 0.05 m (25 ft 8 in, Winfield pp. 335-336); draught 3.16 ± 0.08 m (10.36 ft
     mean to the false keel); displacement 288 ± 10 t at her sailing trim; lateral area 102 ± 5 m².
   - Her masts 13.3 ± 0.3 m apart at the deck (43.7 ft, Neuf §2.7), raking 12.4 ± 0.7° and 10.3 ±
     0.7°; four square yards on the fore and a boomless gaff sail; a gaff mainsail on a boom of 19.6 ±
     0.3 m (64.2 ft); the fore yard 19.8 ± 0.5 m (65 ft).
   - Eleven port triples a side; every gun on one within 0.01 m; her lowest sill 1.50 ± 0.09 m (4 ft 11
     in, measured ±0.3 ft), tightened to ±0.03 m once task 1's checker confirms it.
   - Her default fit 16 × 12-pdr carronades and 2 long 6-pdrs, 18 pieces, 108 lb by 70's rule; her
     complement 130, with a captain and five lieutenants among her posts (Cobb p. 40); the names
     `american`.
   - **Her rig read as Cobb's** (p. 38): she classes as one mast with yards, not square-rigged, her
     main a schooner's.
   - At step 5, the description her file carries (`file_descriptions`): `hermaphrodite brig`, "a
     brig" at a distance, roles `[privateer]`, no fit; size rank 2 (`SIZE_RANK`, laid).
   - At step 6, the index clause: `description("hermaphrodite brig")` gives her file and those
     words, and "a hermaphrodite brig" names her (`description_key`).
2. **7-193: her polar's best point, from her accounts.** Pinned at step 5 on what the file bears,
   re-measured at step 7, old beside new.
   - Her best speed in 25 kn of wind within the band of her accounts: proposed 11.5-13.0 kn (Cobb pp.
     54, 138), fixed when her file is measured and as the owner answers question 1;
   - her `closest_deg` no wider than the frigate-36's, and her speed at 60° and 70° in 15 and 25 kn above
     the frigate-36's (Cobb p. 96, T1). The margins are §9's: 0.8 kn at 70° in 25 kn on her own
     sails, none on the brig-rigged stand-in, so the 70° clause is the one most likely to be
     reported rather than pinned;
   - its docstring gives the best point's angle and her speeds at 150° and 180°, as measured, as
     figures reported and not pinned.

   **Pinned only where §9's measure bears it out after tuning within its bounds; else reported, not
   forced** (the owner's rule for the razee, 2026-10-29: left to tuning, neither ship presumed at
   fault). **Plainly:** the brief names "the Prince de Neufchatel's polar's best point". The truth pins
   its speed and its wind, and reports its angle: her accounts' point of sailing was running, and the
   engine's polar peaks at 90-100° for every file measured (§9). Put to the owner (§17, question 1) and
   the lead (lead item 5).

Her lee ports shutting (18.2°, heel alone) are a line of the package's lee-port truth (7-190), after
L3. Her file's byte identity is the package's generator truth (7-185). Her scenario's round trip is
B6's test, not a truth (Build decision 27).

---

## 15. Pins her work could move

- **None of the existing ships' passages.** The module writes a new file only; no shared function or
  table changes; `brig()`, `schooner()` and `privateer_schooner()` are untouched.
- **Lists, not pins:** `tests/test_profile.py`'s `MODULE_FILES` row, stage 0b's, with her first file.
  No other list: the byte test is two-way; her names, her wardroom check, her golden row and her
  polar test run in her own file. Rank 2 is laid and already asserted (`tests/test_profile.py:920`).
- **The registries:** new keys and words only; "a brig" unchanged; no scenario, business table or test
  names her words (grep).
- **The caches** (32) hold her file beside the others. **The harbour's glob** (`ui/harbour.py:382`)
  lists her (membership only).
- **Stage 0b:** nothing (§12.1's checks). **B3.4:** nothing existing; no file carries the key until
  hers (the golden table).
- **The `nations:` block:** nothing; no scenario carries it until B6's.
- **Within the package:** her flip moves her own file's bytes, classing (the after yards), rating,
  balance and handling, and her 7-193 measures by at most the light yards' windage, each old beside
  new.
- **Not hers:** the lee-port wiring's combat pins (B8's).

---

## 16. Risks, ranked

1. **Her polar's best point against her running accounts** (§9). The truth pins the speed and reports
   the angle. If the owner wants her running speed honoured, that is the polar's shape for every file,
   an engine matter, not hers. Her pointing at 70° is the slimmest clause: 0.8 kn over the frigate in
   25 kn on her own sails, short of it on the brig-rigged stand-in.
2. **The most canvas for her weight in the game** (about 23.5 m² a tonne^(2/3) against 13.5-17.2):
   heel, the strain on her lines (truth 9's behaviour) and the rating pass. Her lines are scaled per
   mast from the brig's and the schooner's and may part early in a breeze; B2 measures the strain at
   90° in 25 kn. GM held within 2.0-2.2; her sources agree she was heavily sparred (T5, T7).
3. **B3.4 after her merge.** She ships at stage A, D10(c), 3% of her canvas left out, **Plainly** said;
   stage B follows, re-measured old beside new. Never D10(b).
4. **Her main yards in the after list** (place 2 left as it is), and her main topgallant set hove to
   abaft the backed fore (place 7): "mainsail haul" logged on a schooner's main, the swing's time, the
   heave-to's angle. B3.4 measures and reports before adding any place (§12.2 item 8).
5. **Her profile read at 1280 px** (±0.3 ft): the rail at the masts against ZAZ6179 (0.9 ft at the
   main), the stem's rabbet or fore edge (up to 2 ft at the water), the gripe's foot (judged), the
   rabbet's depth at the dead flat (0.4-0.5 ft between the profile and the body plan), the rail
   column of `breadth_m` taken from the top breadth, the end ports' half-breadths, the transom. Each
   is marked; the gap check guards the triples; tasks 1-4 raise them.
6. **Her stern against the approved §5.7 row**: measured `raked` where the row says `square`. Re-traced
   by a checker before her first commit, and the row amended old beside new.
7. **The headsails unmeasured** until task 5: her plain sail ±10%; 7-193's band holds across the
   stand-ins' cases.
8. **Both foresails in plain sail**: no file carries a large fore gaff sail beside a fore course (trial
   A's course had the schooner's smaller gaff sail); the blanketing between them; the tack's shift of
   the gaff sail round the main with the course set. Measured at step 5.
9. **Two sails in one space** between her masts (the fore gaff sail and the main staysail): the physics
   lets both draw. Mitigated by the groups (the main staysail never in plain sail) and the main topmast
   staysail's upper foot; B2 measures and records.
10. **The order with SW-4** for `world/ships.py` while SW-4's rows wait on 84's step 7 (§17, lead item
    3).
11. **The keel's bottom** (D29(b)): the scale bar's border, as Neuf takes it. On the faint line instead,
    the draught falls 0.5 ft and the lateral plane 5% (Neuf §2.3).
12. **Her balance:** a great mainsail on a long boom over the stern and a loose fore gaff sail lapping
    the main. `clr_x_m` tuned against the helm and recorded tuned.
13. **The `nations:` block** carries rows not yet read (the letters of marque, the minor powers'
    peaces); named open, not carried as checked.
14. **The quarter bill's judgement figures** (trimmers, small arms, boarders) and the guns' places
    (the 6s at the bow, Adye's 8-ft 6-pdr, the two aftmost ports empty): `Quarters.beat` measures the
    first; the owner's eye the second.
15. **The pair check before SW-2b.2 lands:** run in scratch against *Lynx*'s lines, and re-run when the
    test lands.
16. **Byte identity on the build machine** (Indf risk 4): the module rounds early.
17. **The far ship's length** (package 74's, booked): `combat/far.py:111` reads every far ship's length
    as 0.0, hers too.
18. **A scenario naming her "a brig"** gets the merchant brig's file (§18); B6 names her by her key.

---

## 17. Open for the owner or the lead

**Answered by the owner (2026-10-29).**
- **Her best speed:** "Agreed, don't worry about tuning for best speed running." Held to her
  accounts' band wherever the engine puts it, as proposed; not tuned for running.
- **The fore course and the fore gaff sail together in plain sail:** "Reasonable to start."
  Both, as proposed, open to a later look once she sails.
- **Her officers from Cobb's account:** "Fine by me." As proposed.
- **Her judgement figures:** "Agreed." As proposed.

**For the owner** (each with this design's pick and what the owner would see):

1. **Her best speed.** The engine makes every ship fastest with the wind just abaft the beam, and
   slower running before it. Cobb's 12.5 knots was running. *Pick:* hold her best speed in a strong
   breeze (25 kn of wind) to 11.5-13 knots wherever the engine puts it, about 100° off the wind. Do
   not tune her to make 12.5 knots dead before the wind. *What you would see:* in a strong breeze she
   makes about 12 knots on a reach with the wind just abaft the beam, and about 9.5 knots dead
   before it. On a reach she is a little faster than the frigate-36 (11.6) and the brig-sloop
   (11.0). Close-hauled she points at least as close as the frigate, and is much faster at 60° off
   the wind and faster at 70° (about 6.4 and 7.1 knots in a moderate breeze, against the frigate's
   4.3 and 6.1). Those figures are from a stand-in with her own sails; with a brig's rig the gain at
   70° vanishes, so her own file decides it. No tuning can make her 12.5 knots dead before the
   wind: even with the hull's wave-making resistance taken away she makes only about 10.2.
   Trying would make her far faster on a reach than any account.
2. **Under plain sail, does she set the fore course and the great fore gaff sail together?** *Pick:
   both.* Her sail plan draws both, and Cobb has both at work. *What you would see:* in the viewer
   under plain sail she shows the square course before the foremast and the big gaff sail abaft it at
   once, about 1,020 m² in all. The gaff sail is worth about 0.9 knots at 60° off the wind and 0.4 at
   her best. Without the course she would look and sail more like a schooner on a wind, setting the
   course only when running.
3. **Her officers' character sketches from Cobb's account of her December 1814 crew?** *Pick: yes.*
   *What you would see:* her captain reads as Cobb describes them: small, French-born, "an American
   for convenience", seldom on deck until the chase. Her first lieutenant is mild and exacting, her
   surgeon a stranger who keeps to the cabin, and her officers are "in profusion". Names are drawn
   from the American list. Otherwise the sketches are plain types with no birth given, as the
   decisions sheet recommended for her.
4. **Her judgement figures, put to you as the 64's were.** *Pick: accept as proposed.* Sixteen marines
   (Cobb's eight in the long boat, and as many forward); GM 2.1 m; the two long 6s as bow chasers in
   the foremost ports (broadside 108 lb; 102 lb if they stood one a side among the carronades, 108
   as stern chasers in the two squares at the transom's top, if those are ports); Adye's 8-ft 6-pdr
   over the 6-ft; her two aftmost ports empty; the nine prize-masters, one drawn by name and the rest
   among her able seamen; three landsmen in ten; the main topmast staysail on its upper foot; the main
   staysail and the main topgallant out of plain sail; Steel's anchors for a ship of 14 guns and 300
   tons, and his sloops' cables; the hold at a trader's share; three months' provisions and two
   months' water; a long boat and a yawl; two hand pumps. *What you would see:* at quarters,
   sixteen men with muskets stand on deck apart from the guns while seamen man the guns. In a chase she fires her two long 6s ahead. Under plain sail she
   carries about a third more canvas for her weight than the topsail schooner, which fits her prize
   crew's complaint that her masts and spars were too large.

**For the lead:**

1. **D10(a)'s key** (§12.1 item 1, §12.2). Proposed: one mast key, `schooner_mast: true` on her main
   ("an opt-in key whose yards the handling ignores"), read through `Ship.on_schooner_mast` at Ext
   §4.2's places 1 and 3 only; place 2 left, so her main yards are after yards that swing at "mainsail
   haul" and are braced by every brace order; the two findings of §12.2 item 8 measured and reported
   to you before any further place. The schema key laid by a stage-0 commit, at B3.4's boundary if
   B3.4 opens first; the runtime field and the predicate B3.4's. **Plainly:** Build §3.3 lays the
   key in the schema and `Spar`; here `Spar.schooner_mast` and `Ship.on_schooner_mast` are B3.4's,
   because Build §4.2 passes `ship/parts.py` and `ship/graph.py` to B3 after 0E and no stage-0
   commit reopens them; nothing reads either before B3.4 (§12.1 item 1). And B3.4's place: right
   after B3.5, before the settee (B3.3), since her window comes before the bilander's, so that her file takes
   D10(a) from its first commit; else she goes in on D10(c) and flips when B3.4 lands, old beside new.
2. **Stage 0b's `MODULE_FILES` row** in `tests/test_profile.py`: committed directly before her
   first-file commit at the same boundary, as 9454fd6 was before 614d2d4.
3. **`world/ships.py`'s order.** Her rows come after SW-4's, which wait for B1's merge and 84's step 7.
   Proposed: if 84's step 7 holds SW-4's rows back when she is otherwise done, hers go in first in her
   window and SW-4's follow. Both are new keys and words only, and neither touches the other's rows.
   **Plainly:** Build decision 15 lands the row with her file; here it waits for SW-4's rows
   (Build §4.2; your ruling of 2026-10-29), so it is her last step, in the same merge as her file.
   Her tests and the clause of 7-192 that read the index move to that step with it (§13, §14).
4. **Her window and her testing report.** By the owner's direction of 2026-10-29 her window opens at
   B1's merge without the owner's test. Proposed: the direction holds for her too, by judgement; she is
   reported done with a testing report of her own (§13), and you merge her on it. The order: B1's
   merge, then SW-4's rows (or hers first, item 3), then her stage 0b. Her stage 0b's item 2 (the
   `nations:` block in `world/scenarios.py`) also waits for B6's D48 change to that file to be
   merged (Build §4.2), which is not in at 8f30be9; or, by your word, item 2 goes first and B6
   merges onto it. Build §2.2's B2 row ("the owner's test") and §2.6's "Held until the test" need
   the direction written in, by the session in a design-record commit at her window's opening (as
   8f30be9 recorded the owner's answers), not by B2.
5. **7-193's form:** her best speed in 25 kn within her accounts' band and her pointing against the
   frigate-36 pinned, the best point's angle and her running speeds reported (§14), since the engine's
   polar peaks at 90-100° for every file and her accounts were running. The pointing clause's margin
   at 70° is slim (0.8 kn in 25 kn on her own sails, none on a brig's rig: §9), and is reported, not
   forced, if her file misses it. Does that meet the brief's "polar's best point"?
6. **Her scenario's date and the `nations:` block** (§11). August 1814 is settled by this design
   (D27 with the brief; Build §12.2). Read (OCR) and cited by page: the war from 18 June 1812 (James
   vol. 5 pp. 253, 360) and the peace with France of 30 May 1814 (vol. 6 p. 229). Open in her
   scenario's notes, as you ruled: the letters of marque and the peaces of Spain, Denmark, the
   Netherlands and Portugal.
7. **The jib's reef** (Cobb p. 95): no evolution reefs a jib; her jib is filed without reef bands and a
   storm jib stands in. Reported under the brief's "a rig the engine lacks", for a later package.
8. **Her stern** (§3.5): measured `raked`, 16.1 ft, no counter, where Build §5.7's approved row says
   "square, about 17 ft". Proposed: the row amended at her merge, old beside new, after task 1's
   checker re-traces it, by the session in a design-record commit, not by B2 (Build-Ships.md is no
   builder's: Build §4.1).
9. **Names:** the fit "as taken 1814"; her description words "a hermaphrodite brig", "an
   hermaphrodite brig", "a privateer brig" and "privateer brig" (§8).

---

## 18. Found on the way

1. **Her stern is raked, not square:** a flat transom raking about 31° from the vertical, from 4.65 ft
   above her water to the taffrail at 9.46 ft, 16.1 ft across at its top, with no counter (measured
   here). Build §5.7 has "square, about 17 ft".
2. **Neuf's ports and masts are measured from a point 0.85 ft abaft the after rabbet** the waterline
   is measured from (measured here at both end ports), so Neuf's mast fractions assumed the wrong
   origin: the main stands 0.112 of the waterline abaft the middle, not 0.105.
3. **The eleven sills, measured here**, agree with Neuf's "deck plus 1.3 ft" within 0.31 ft (ports 3
   and 9 at 0.26 and 0.31; the rest within 0.25); the lowest is 4 ft 11 in amidships, shut at 18.2°
   of heel alone.
4. **The rail at the masts:** ZAZ6177's traced rail gives about 7.5 ft above the water at the main and
   8.2 ft at the fore, against ZAZ6179's 8.4 ft at both.
5. **Every file's polar peaks at 90-100° off the wind** and falls by a fifth or more by 180° (measured
   here on the frigate-36, the brig, the topsail schooner, the razee and the 64). No running account
   can be a polar's best point by its angle.
6. **Before the wind in 25 kn she cannot pass about 10.2 kn** even with the wave term of the resistance
   removed (10.21 measured here on `probe-all-12.5.yaml`, the wave factor divided out:
   `verify/nowave.py`).
7. **"A brig" names the merchant brig** (`world/ships.py:236`), and **two-word descriptions resolve
   only through a row of their own**: `description_key` strips the article and then tries tails
   shorter than the words, so "a hermaphrodite brig" meets only "brig" (probed here). Three-word
   phrases resolve by their tail ("an American hermaphrodite brig" gives hers).
8. **She carried a surgeon**: Cobb pp. 75-76 (OCR l. 2964-2999) has a "doctor" in the berth "of
   surgeon", a stranger of little skill by hearsay. The buildability draft's "no surgeon" was wrong.
9. **Cobb's "foresail" is the course** (pp. 105-107: the lashing on the weather yard-arm), so her alias
   differs from the topsail schooner's. "Foresail" means two sails in the house.
10. **No evolution reefs a jib**, though Cobb's was "closely reefed" (p. 95).
11. **Hove to, a light yard abaft the backed yards stays set**: the heave-to keeps every other working
    yard full and braced up and clews up light sails only forward of the backed yards
    (`evolutions/scripts.py:584-609`), so her main topgallant would stand while she lies to.
12. **The hull's added resistance acts only in a head sea** (`physics/motion.py:111-118`), so the
    frigates gaining on her as she pitched running before a heavy sea (Cobb p. 97) cannot be
    reproduced.
13. **Cobb p. 73:** a long boat stowed amidships, and landsmen "drafted into the marine corps" with
    muskets at quarters, eight of them in the long boat.
14. **Cobb p. 104:** she showed no colours throughout the last chase, and fired one gun, to leeward, as
    the signal of her surrender.
15. **Steel's tables have a row for "14 Guns, 300 Tons"** (three bowers of 20 cwt, a stream of 7, a kedge
    of 3 cwt 2 qr) and a "Sloops" column of five bower cables of 13½ in and a stream cable of 8 in
    (read here).
16. **Adye p. 72's 12-pdr carronade is 5 cwt 3 qr 10 lb** and p. 155's long 6s 22 cwt (8 ft) and 16 cwt
    2 qr (6 ft) (read here); the shared tables' 6 and 20 cwt, from memory, are heavier.
17. **James gives the nations block's dates by page:** the war from 18 June 1812 (vol. 5 pp. 253, 360),
    the peace with France signed at Paris on 30 May 1814 (vol. 6 p. 229), the treaty of Ghent of 24
    December 1814, ratified 18 February 1815 (vol. 6 p. 236); read (OCR) here. None is in
    `data/nations.yaml` yet.
18. **`tests/test_profile.py`'s `MODULE_FILES`** needs her row in the commit pair that first writes her
    file, or the hook test fails.
19. **The main staysail and the fore gaff sail share one space** between her masts on her plan; the main
    topmast staysail's two drawn feet are one below and one above the fore gaff's peak.
20. **D18 is moot for her:** a flush deck gives one datum under every option.
21. **Her knee of the head reaches about 7 ft before the stem** at the head rails (measured here); the
    terminal at its top is not resolved at 1280 px.
22. **Her plain sail per tonne^(2/3) is the package's largest**: about 23.5 against the topsail
    schooner's 17.2, the brig-sloop's 13.8 and the frigate-36's 13.5, the prize crew's judgement of her
    spars (Cobb p. 138) in figures.
