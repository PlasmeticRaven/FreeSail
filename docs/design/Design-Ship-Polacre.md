# Design: the polacre, a Mediterranean trader under lateens and a square pole main (package 90, second draft)

**Status: the second draft (2026-11-18)** of her design document, in the form of
`Design-Ship-Bilander.md` and `Design-Ship-Bellerophon.md` (`Plan-ShipsWorkflow.md` §2, Phase 3).
It answers the critic's reading of the first draft item by item ("How this draft answers the
critic", below the decisions), takes the settlements of package 90's plan
(`docs/design/Plan-Package90.md` §4) and cites the plan's step names (§6 there) in place of the
first draft's own: **A5** (the first draft's E1), **A6** (E2), **A1** (E3), **V1** (E4). Package
90's preliminary work only (the lead's note of 2026-11-18, 00:50 UTC, nudge 15):
**nothing here is built**, and the build begins only from a one-page scope card agreed with the
owner (`docs/dev/ScopeCards-BeforeTheGate.md`, "How a package runs, as amended by the owner on
2026-11-16"). It is for the lead's scope card, and later her builder and the viewer's.

**What binds, in order:**
1. The brief: `docs/dev/M7-WorkPackages.md` row 90 and the lead's notes to the ships session of
   2026-10-29, 2026-11-06 (the widening, Winfield's passages, 18:00's rulings on B3.4) and
   2026-11-18 (nudge 15: research and planning only; **item 8 of the list of 79 is hers and is
   settled here, with what the engine does today, run and not guessed**).
2. `docs/design/Build-Ships.md`: §5.0's principles and its ladder; §6's postscript (package 81's
   checklist for ports and guns); §8 (descriptions, fits, roles); the made-out rule (Phase 5,
   2026-11-14).
3. `docs/design/Design-ShipsEngineExtensions.md` (cited **Ext**): §3 (the lateen class; §3.7 the
   whole lateen kept possible), §5 (the settee and its change), B3.4's schooner's mast with its
   two limits (`docs/dev/TuningNotes.md`, "The schooner's mast", "Left, and for whom").
4. Her research note, `docs/design/Research-Polacre-2026-11.md` (cited **Pol**), and
   `VesselReferences-2026-11-Spanish.md` §2 (Winfield pp. 1083-1084 in the lead's words),
   `VesselReferences-2026-10.md` §3.3-§3.4.
5. Packages since 75 that a new hull meets: 96 (the harbour's shelves,
   `client/harbour-shelves.yaml`, a sentence each); 116 (the wheel shot away, the relieving
   tackles, `repair the wheel`; a captain's doctrine read from `thresholds:`); 110's rulings on
   Barbary captivity (`Design-SlaveryAndSuppression.md`, its head and §8.1); package 75's ruling 11
   (a merchantman's working officers).
6. Pictures for the eye only, never a source of points: Monleón's print (Winfield p. 1084, cited,
   not held), Roux's polacres on Commons (Pol §9, not looked at, not held).

**Where.** The worktree `D:/Projects/FreeSail/FreeSail-pkg-90`, on package 90's branch, cut from
the trunk's 68e769ef. Every `file:line` is at that head. Paths are from the repository root.

**Marks.** *read*, *read (OCR)*, *catalogue*, *the lead's words*, *memory, unverified* as Pol uses
them. *observed*: printed by a scratch probe run in this package's scratch
(`scratchpad/p90/polacre/`: `probe_classing.py`, `probe_sail.py`, `probe_pole.py`,
`probe_pole_words.py`, `probe_variants.py`, `probe_mizen_topmast.py`, `probe_polar.py`,
`probe_smack.py`; `py`, the worktree first on `sys.path`, `freesail.__file__` asserted under it;
the scripts are not filed; no tracked file changed, the only things written in the worktree being
Python's git-ignored bytecode caches). **Every speed in knots below is her headway (`dyn.u`), as
the first draft's probes printed it, unless it is marked "by truth 12's measure"**: truth 12 reads
the ship's speed, `knots()`, which is `dyn.speed` (`tests/test_known_truths.py:120-121`, read), a
little more than the headway when she makes leeway (the heave-to's figures re-measured both ways
for this draft, `scratchpad/p90/second/speeds.py`). **JUDGEMENT**: this draft's own.
"Plainly:" marks a departure from the brief, a ruling or a decision, with its reason. Rungs as Pol:
**A** (the period's own plan, rule or text), **B** (a historian's particular), **C** (judgement);
for the hull's lines §5.0's **S**, **S†**, **R**, **T**.

**One sentence.** One module writes two files of one class: a Mediterranean trader of about 200 tons
(JUDGEMENT until Winfield's rows come), three pole masts with no tops, a great lateen on the fore
raked forward, a course, topsail and topgallant on the pole main handed by lowering their yards, a
lateen on the mizen, the jibs on a long bowsprit of one piece; the trader unarmed by default,
with an armed trader's fit, and on the same hull the polacre of war, the Spanish navy's, with the
regency's cruiser as a role; built only after the plan's A5 (a yard's level read from its place on
the mast and not from its spar's class), A6 (the pole mast's quick handing), A1 (the whole lateen
worked in stays and changed round its mast) and V1 (the whole lateen drawn), which package 90's
tartane and xebec share (the tartane A5 and A6 too, her topsail standing on her pole main's
head).

---

## Decisions proposed

| # | Proposal | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/polacre.py`, `build(out_dir)` writing `data/ships/polacre.yaml` (the trader) and `data/ships/polacre-of-war.yaml` (the navy's and the regency's: one class in two roles, the file's name the lead's); the whole lateen's cut in a shared pure module `tools/ships/lateen.py` (the tartane's and the xebec's too) | the per-ship modules' rule (`Plan-ShipsWorkflow.md` §3); a company belongs to a file, not to a fit (the lead's ruling (5) of 2026-11-07; `Build-Ships.md` §5.0 principle 10), and her fits' companies are 16, 71 and 80; one cut for package 90's three lateen hulls |
| 2 | **The rig is Monleón's** (the owner's plan): lateen fore on a pole foremast raked forward; square pole main with course, topsail and topgallant; lateen mizen on a pole; jibs on a long bowsprit of one piece | the owner, 2026-11-06; Falconer's "generally"; Steel's second polacre-settee (Pol §1); question 1 |
| 3 | **The hull a Mediterranean merchantman's of burthen, with a beak**, not the xebec's | Falconer 1780 XEBEC, PROW; Lescallier p. 370 "un Navire Marchand ordinaire"; Pol §5.1; question 2 |
| 4 | **Her size from Winfield's Spanish rows when the owner sends them**; until then about 200 tons by the old measure, LWL about 25 m, beam about 7.3 m, draught about 3.3 m, all JUDGEMENT | no polacre's dimensions found (Pol §5.2); §2 |
| 5 | **Pole masts filed as the smack files her one stick**: a `mast` with every yard on it and no topmast, topgallant or royal mast; no new key | the generator's precedent (`data/ships/smack.yaml` l. 129-166, read); Pol §2 |
| 6 | **Engine step A5: a yard's level read from its order on its lower mast, not from its spar's class**, one predicate read at the twelve places that read it now | observed: a pole main's topsail is a course to the heave-to, the lie a-try, the take-in words and the trim (§5.1) |
| 7 | **Engine step A6: the pole mast's quick handing**, "amener en paquet": the upper square sails of a pole mast lowered together onto the lower yard, quicker than clewing up each on its cap; furled from the yard below | Lescallier p. 371; Röding; Falconer; Steel p. 236; O'Scanlan p. 482 (Pol §2.3) |
| 8 | **Her lateen mizen is kept set hove to, and the heave-to's driver rule does not reach it** | observed: kept, she lies 58.5° off at 1.65 kn by truth 12's measure (1.49 kn of headway), just over its 1.6 kn, so her file's lever is to be measured (§5.2); taken in, she falls off past the beam and the heave-to fails (§5.2) |
| 9 | **Engine step A1: a whole lateen worked in stays** (the mizen hauled out at helm's a-lee as a ship's mizen; the fore eased off as a head sail) **and changed round its mast** (the period's *muder*: the yard peaked up and its heel passed abaft the mast), with a lateen left unchanged lying against its mast | observed: nothing works a whole lateen in stays today (§5.3); Lescallier p. 378, Fincham p. 60, Willaumez MUDER (Pol §4) |
| 10 | **B3.4's limits do not bite her**, nor the chebec's or the chambequín's: her main is her foremost mast with braced yards, pole or not; a square mizen topsail (question 1 (b)) would be filed on the pole mizen and class her square-rigged, never on a mizzen topmast | observed (§5.4) |
| 11 | Fits: in the trader's file **`unarmed`** (default) and **`armed trader`** six long 6-pounders; in the polacre of war's **`spanish navy 1800`** (default) San Josef's fourteen brass guns and **`corsair`** fourteen small guns. Roles `merchant`, `privateer` (on the armed trader), `kings-ship` and `cruiser` (on the navy's), and a new **`corsair`** role for the regency's cruiser with a doctrine book of its own (`data/captains/corsair.yaml`, read from `thresholds:` as package 116 made the cruiser's: question 4) | James (Pol §6); the roles the files use today are nine, none a corsair's (observed); question 4 |
| 12 | Company **sixteen** in the trader's file: master and mate (posts, working officers by ruling 11), boatswain, carpenter, cook, nine seamen, two boys; **seventy-one** in the polacre of war's (the *San Josef*'s 49 seamen and 22 soldiers), the corsair's 80 filed at 71 and recorded as a departure, as the xebec's regency fit's 150 is (Xeb-D §8.1); `names: spanish` (a new list, the plan's N1) | the trader's JUDGEMENT within twelve to twenty (Pol §5.3); James vol. 3 pp. 33, 160 (Pol §6); §7 |
| 13 | Description key `polacre`, rig word **"a polacre"**, size rank 2; the registries gain her words | the made-out rule; §9 |
| 14 | **Engine step V1 (the viewer): a whole lateen drawn as itself**, three corners on its yard, on its lee side, peaked up the mast while it is changed | `client/projection.js` l. 815, 904, 1506, 1537 (read): no whole lateen is drawn as one today; §13 |
| 15 | Truths proposed P1 to P6 (§14); her scenario a shelf line on 79c's water (§11), booked for a card of its own (the plan's §4 row 15) | the plan's form |

---

## How this draft answers the critic

| Finding | What the first draft said | This draft |
|---|---|---|
| F1 (blocker): the heave-to's speed | 1.49 kn, "inside truth 12's band"; the engine note's 1.65 kn put down to a different settle | **Held.** 1.49 kn was her headway (`dyn.u`); truth 12 reads `dyn.speed`, 1.65 kn, over its 1.6 kn (re-measured: 1.65 at +600, +750 and +900 s, headway 1.50, 1.49, 1.49). Mended in decision 8, §5.1, §5.2, P3 and the marks; "the two settles differ" deleted. The settlement stands: the driver rule must not reach the mizen, since taken in she does not heave to at all. The lever for her file is named (§5.2) |
| F3: the first pole main | "she is that file" (§5.4) | **Held.** The tartane's design files her topsail yard on her main's own head (Tar-D §4.1), and on such a main the topsail is a course today (the critic's run, re-run here: "Hauled up the courses", hove to under her fore-and-aft canvas at 3.29 kn). The tartane is the package's first file with a pole main; A5 and A6 come before her file (the plan's §9.1) |
| F6: one company for fits of 16, 71 and 80 | one file, `polacre.yaml`, company sixteen | **Held.** Two files of one class (decisions 1 and 12; §6.1, §7.2, §9): the trader's (16) and the polacre of war's (71), the corsair's 80 a departure as the xebec's regency 150 is |
| F8: Willaumez | "Willaumez draws a polacre tacking" | **Held.** Willaumez's text describes a square-rigged polacre, with no lateens, tacking; the plate was not viewed (Pol §1, §4). The lateen polacre's tack is JUDGEMENT (§17.1 question 3) |
| F15: B3.4's limits | the limits handed to "the xebec's document" | **Held.** Stated once, §5.4: neither limit reaches the polacre, the chebec (her main the foremost mast with yards) or the chambequín (a ship); they stay with a schooner's main, recorded |
| F18: the working tonnage | 86 by 24 ft "gives 172 tons" | **Held.** By the old measure 86 by 24 ft is about 219 tons and 88 by 25 ft about 243; about 200 tons at 3.4 beams is about 81 by 23¾ ft (§2.1) |
| F25: "wrote nothing in the tree" | the marks | **Held.** Reworded: no tracked file changed; bytecode caches only, git-ignored |
| The plan's settlements (Plan §4) | E1 to E4; the lateen row tuned "on the tartane's file" | The plan's names throughout; the row tuned once at A8 on the lateen hulls on the branch then, her figures re-measured old beside new when she lands (§16) |

---

## 0. The road: what waits, and on what

- **Nothing is built before the owner's scope card** (nudge 15). This document, the critic's
  reading and the second draft are the preliminaries; the lead puts a card for the build to the
  owner after the session's report.
- **Her files wait on four engine steps**, each its own small step with its own measure (§12):
  **A5** the yards' level (before the tartane's file, the package's first pole main, the smack
  measured first: §15);
  **A6** the pole mast's quick handing (after A5); **A1** the whole lateen in stays and its change
  (shared with the tartane and the xebec; after the owner's answer to question 3); **V1** the
  whole lateen drawn (the viewer's, with A1). Without A5 her main topsail is a course to six of
  the engine's paths (§5.1); without A1 her lateens tack for nothing and never lie against their
  masts (§5.3).
- **Her size waits on Winfield's rows** (Pol §11 items 1, 2 and 6). Until then the figures of §2
  are JUDGEMENT and her files are not written.
- **Order within package 90** (the plan's §9.1, which keeps the lead's view): the tartane first,
  the smallest and the reference vessel, after A1 to A6; the polacre second, after the tartane's
  file; the xebec third, going ahead of her if her Winfield rows have not come when A6 lands.

---

## 1. The module and the generator

### 1.1 Files (in her window, none now)

| File | What | Kind |
|---|---|---|
| `tools/ships/polacre.py` | her module: `build(out_dir)`, her `Particulars`, her sections in the generator's order | new |
| `tools/ships/lateen.py` | the whole lateen's cut, pure: yard, corners `[tack, peak, clew]` (three-cornered), area and centroid, the slinging at a third on the mast's raked line | new, shared with the tartane and the xebec |
| `data/ships/polacre.yaml` | the trader's file, by the generator only | generated |
| `data/ships/polacre-of-war.yaml` | the polacre of war's file (the navy's and the regency's), the same hull, by the generator only | generated |
| `data/people/polacre.yaml` | the trader's afterguard as people (the master, the mate, a boy to carry the word) | hand-written data |
| `data/people/polacre-of-war.yaml` | the polacre of war's (her commander, a second, a pilot: §7.2) | hand-written data |
| `data/crew/names.yaml` | a `spanish` list (shared by package 90's Spanish hulls) | data |
| `tests/test_polacre.py` | her particulars, her classing, her truths | new |

### 1.2 What she reuses, read only

- The generator's builder (`b.spar`, `b.sail`, `b.line`, groups, aliases, descriptions, fits), the
  smack's one-stick mast (`data/ships/smack.yaml` l. 129-166), the merchant brig's ground tackle,
  boats, pumps and hold rules, `MERCHANT_ROUNDS` for a trader's magazine (`Research-Bilander` §3,
  read there), the lateen evolutions of B3.1 (`set_lateen`, `take_in_lateen`, `furl_lateen`,
  `reef_lateen`, `trim_lateen_sheet`; Ext §3.6).
- `tests/rig_fixtures.py`'s `polacre_probe()` is the lead's classing probe and is **not** her file:
  its figures are round and its masts the brig's (`rig_fixtures.py` l. 232-266, read).

### 1.3 Her particulars as data

In the sources' units, converted once: Winfield's metres for a Spanish row (never the pies as
English feet; the Spanish note's head); Forfait's pieds du roi (0.3248 m) for the rules' examples;
James's English pounds of shot as given. Each figure carries its rung in its note.

---

## 2. The hull blocks

### 2.1 The figures (all JUDGEMENT until a source; the second draft replaces them)

| Key | Working figure | Rung | Basis |
|---|---|---|---|
| Tons burthen | about 200 (170 to 220) | C | `VesselReferences-2026-10.md` §3.4's "about 200 tons" (judgement there); the polacre-ships of James carry ten to sixteen guns (Pol §6) |
| `length_waterline_m` | about 24.5 | C | the tons by the old measure on a length of 3.4 beams (a merchant's proportion, JUDGEMENT). The keel for tonnage is the length less three-fifths of the breadth, as *Minorca*'s own figures show (96 ft 9 in less 18 ft 3 in is 78 ft 6 in: Pol §5.1), and the tons are that keel by the breadth by half the breadth over 94: about 81 ft on deck by 23¾ ft broad gives 200 tons (24.7 × 7.24 m), 86 by 24 ft about 219, 88 by 25 ft about 243. **Plainly:** the first draft's "172" and "190" misapplied the rule |
| `beam_m` | about 7.3 | C | as above |
| `draught_m` | about 3.3 | C | a laden trader of her size (the bilander's 3.51 m at 130 tons, read there, is a deep-laden British coaster's, from Lloyd's: JUDGEMENT on carrying less to her) |
| Displacement | LWL × B × T × Cb 0.52 × 1025 | C | the brig file's method; Cb a merchant's, JUDGEMENT |
| `deck_height_m` | about 1.4 | C | the brig's method |

**Plainly:** no figure above is sourced. The owner's passages (Pol §11 items 1, 2, 6) are asked
for; a Spanish polacra's row, or HMS *Calpe*'s if she was the *San José*, replaces them, its metres
taken as Winfield gives them.

### 2.2 Her datum

The upper deck, as the merchant brig's (D18 (a) of package 75).

---

## 3. The hull profile and her shape (`Build-Ships.md` §5.0-§5.3)

### 3.1 What the sources give, by rung

- **S** (her own lines): none found (Pol §5.1, §11).
- **S†** (a period plan of her type, scaled): none found. The Spanish navy's plans in the
  Biblioteca Virtual de Defensa (a CC BY 4.0 source, as the *Diana*'s) were searched on their first
  page only (Pol §0); a polacra plan there would be S† or S at once.
- **R** (a period rule on her particulars): Chapman's merchant-ship rules for the greatest breadth
  and the heights of breadth (Chapman 1781, the tree's OCR; `Build-Ships.md` §5.0 principle 3's
  example), and Steel 1805's heights of breadth, applied to her particulars.
- **T**: the design's default rule (§5.3 there), with her type's stated differences: **a beak**
  (Falconer PROW: the "pointed cut-water of a polacre, xebeck, or galley", with a grating
  platform), JUDGEMENT on its length; **a merchantman's fuller floor** than the xebec's (Falconer
  XEBEC: the xebec's hull "extremely different"; Steel's PINKS "not sharp in the bottom, as they
  are vessels of burthen"); **a low sheer** with a short raised quarterdeck (JUDGEMENT, to be
  checked against the owner's description of Monleón's print, Pol §11 item 5).

### 3.2 What the drawing must show her to be

Distinct from the merchant brig (her nearest hull in size) by the beak, the three masts and the
forward rake of the fore; distinct from the xebec (package 90's next hull) by her fuller floor, a
higher side and no overhanging stern platform (Falconer XEBEC). Her marks: `stand-in` nowhere,
`rule` for the breadths, `judged` for the beak, the stern and the sheer, each note naming the
source to read.

### 3.3 Carving and paint

None sourced; recorded in words only where the owner's description or a vetted picture gives it
(principle 9).

---

## 4. The rig

### 4.1 The masts: three poles (Pol §2)

| Spar | Filed as | Figures (JUDGEMENT unless said) | Source |
|---|---|---|---|
| `fore.mast` | `mast`, one stick, **raked forward** (`rake_deg` about −8) | shorter than the main (about 0.75 of its height above the deck), short and thick as a lateen mast is | Monleón (the lead's words); Lescallier p. 376 ("gros & courts"); Fincham p. 59; the rake JUDGEMENT, to check on the print |
| `main.mast` | `mast`, one stick carrying the course, topsail and topgallant yards; **no topmast, topgallant or royal mast** | the heel-to-head length by Forfait's rule: the eyes of the rigging at the heights a three-piece main of her size would give them (p. 132), shortened at the pole's head by Lescallier's advice (p. 372); checked against the Levant's rule of four and a fraction breadths (p. 133, the fraction to read) | Forfait pp. 131-133; Lescallier pp. 370-372 (Pol §2.5, §10) |
| `mizzen.mast` | `mast`, one stick, a lateen mast | about 0.6 of the main's height (Fincham's xebec, read there) | Pol §3.3 |
| `bowsprit` | `bowsprit`, **one piece, no jib-boom**, long | about 0.6 of the main's length outboard (JUDGEMENT) | Lescallier p. 370 ("bout de beaupré aussi d'une seule pièce"); Steel p. 236; Monleón "a long bowsprit" (the lead's words) |

- **The diameters** (for the ratings' notes): the main at the deck 1/60 to 1/62 of its length, the
  fore 1/68 (Forfait p. 133); the yards a twentieth (lower) and a fifteenth (upper) thinner than
  the three-piece rig's.
- **The ratings.** A pole mast carries every load of its sails on one spar; its rating by the
  generator's rule from every sail on it (as the smack's mast note does). Lescallier's "excess of
  diameter" is the reason it stands; Winfield's "less able to stand a strong wind" is the reason to
  rate it no higher than the three-piece main's lower mast (JUDGEMENT).
- **No `strike_topmasts`, `send_down_topgallant_masts`**: she has none; the parser already refuses
  in words (observed: "There is no such part as the main topgallant mast in this ship").

### 4.2 The main's yards and square sails

- **Course, topsail, topgallant** (Monleón); no royals, no studding sails (JUDGEMENT: no source of
  the type shows them; Steel's square POLACRES "the same sails as a ship" is the square-rigged
  polacre's).
- Yards by the generator's merchant rules (Steel 1794's merchant tables, as the merchant brig's),
  their diameters reduced by Forfait's twentieth and fifteenth.
- **Footropes on the lower yard only** (Steel p. 236; Falconer says none: Pol §10); the topsail
  and topgallant are loosed and furled from the yard below, their yards lowered for it (Falconer;
  Steel). The engine has no footrope; this is words and times (A6).
- Brace limits the merchant brig's, level for level (JUDGEMENT).

### 4.3 The fore lateen (`fore.lateen` on `fore.lateen_yard`)

- A whole lateen, **no `cut_at_mast`**: three corners (tack at the yard's lower end, the *car*,
  near the stem or the bowsprit's heel; the peak at the *penne*; the clew aft), cut by
  `tools/ships/lateen.py`.
- Its yard slung at a third (Lescallier p. 379; Fincham p. 60), of two spliced pieces (p. 378; the
  file notes it), its length about 0.75 of the waterline (JUDGEMENT under Fincham's xebec, whose
  fore lateen yard is 0.86 of the length: read there).
- Its lines: jeers (`halyard`); **two ourses**, the *ourse à proue* and *à poupe*, at its lower end
  to the weather side (filed as two `guy` lines, as the mizen course's bowlines are, Ext §3.4); a
  **brace** (*oste*) and a **vang** (*van*) at its upper lee end (sided pairs, `brace` and `vang`;
  Ext §3.3 allows a brace on a lateen yard); **one unsided sheet**, aft to leeward; a tack. The
  runners (*haubans à colonne*) are her standing rigging's notes, shifted when the yard is changed
  (Fincham p. 60).
- **One reef** (Lescallier: oblique). The engine's reef band is parallel to the foot (Ext §3.6's
  `reef_lateen`); the area is what it reduces, and its note says the band is oblique in the period
  (JUDGEMENT: no change asked).
- In "plain sail", "all sail", "fore-and-aft sails" and a new group "lateens"; never "courses"
  (the gale's reduction would take it as a course: Ext §3.4's reason for the mizen course).
- Alias "foresail" and "fore lateen"; the Spanish *trinquete*, the Levant's *polacre* for the fore
  lateen (Willaumez POLACRE) in her notes.

### 4.4 The mizen lateen (`mizzen.lateen` on `mizzen.lateen_yard`)

- A whole lateen, smaller: its yard about half the fore lateen yard (JUDGEMENT). **Plainly:**
  Fincham's 0.45 is the xebec's mizen yard against her main yard (read there); the polacre has no
  main lateen, so the fore's is taken as the measure.
- Its lines as the fore's. In "plain sail", "all sail", "fore-and-aft sails", "lateens"; alias
  "mizen".
- **Kept set hove to** (§5.2): never a driver.

### 4.5 Headsails, staysails, storm canvas

- **Jibs on the long bowsprit**: a fore staysail and a jib, on stays from the fore masthead
  (JUDGEMENT: Monleón shows "the jibs"; the count to the owner's eye). **Plainly:** Lescallier p.
  376 gives lateen masts no stays; how a polacre's jib stays clear the fore lateen's yard when it is
  changed is not in any source read (§17, for the lead).
- **A main staysail** on the main stay, her lying-to staysail (JUDGEMENT: the heave-to's and lie
  a-try's staysail; none sourced).
- **Storm canvas**: a storm fore staysail; small lateens for bad weather are the xebec's (Fincham
  p. 60), a later fit (§17).

### 4.6 Groups and aliases

"courses" (`main.course`), "topsails" (`main.topsail`), "topgallants" (`main.topgallant`), "square
sails", "lateens" (new), "fore-and-aft sails", "headsails", "plain sail" (fore lateen, main course,
main topsail, jib, mizen lateen), "all sail", "lying-to staysails", "storm canvas"; "main yards",
"lower yards", "topsail yards", "yards". Aliases: "mainsail" the main course, "foresail" the fore
lateen, "mizen" the mizen lateen.

---

## 5. Item 8, settled: how the engine sails her today, and what it must be given

All on the lead's `polacre_probe()` (the brig with lateens on her fore and on a mizen, her main
course and main topsail kept; `tests/rig_fixtures.py` l. 956-992) and on variants built in memory
from it in scratch: **`pole_main`** (her main made one stick, the main topmast, topgallant and royal
masts taken out and every yard and line on them put on `main.mast`, its height their sum, 27.6 m:
the smack's way), **`pole_tg`** (the same with the brig's main topgallant yard and sail put back:
Monleón's three square sails). B3.4's measure throughout: seed 7, a northerly of 15 kn, no gusts,
heading 292.5° at 5 kn, plain sail set and braced sharp up on the starboard tack, trimmed every two
minutes, settled 2,400 s; each order from a fresh settle (observed).

### 5.1 (a) The pole masts: what the generator and the engine do with one today

**The generator** has no pole mast and needs none: the smack's file is the precedent, "the mast and
topmast in one stick ... No topmast to strike: the topsail yard crosses the mast's own head"
(`data/ships/smack.yaml` l. 129, read), a `mast` with both her yards `on: main.mast`. Of the
committed files the smack alone has yards on a lower mast with no topmast above it (observed, over
every file of `data/ships/`). The generator's "pole" elsewhere is a topmast's pole-head
(`tools/gen_ships.py` l. 3317, 6141, 7098; read). **So she is filed with no new key** (decision 5).

**The engine reads a yard's level from the class of the spar it hangs on** (`mast`, `topmast`,
`topgallant_mast`, `royal_mast`), at twelve places (read):

| Place | What it decides | On a pole main today (observed or read) |
|---|---|---|
| `evolutions/scripts.py:860` `lowest_square_sails` (and through it `standing_sail_on` :605, the heave-to :2898, lie a-try, the box-haul's after courses :5190, back and fill :6014, coming to anchor :7155) | the courses | **the topsail and topgallant are courses** (observed: `['main.course', 'main.topsail', 'main.topgallant']`) |
| `scripts.py:808`, the test at :833 `light_sails_forward_of` | the light sails clewed up hove to | the topgallant is no light sail (read) |
| `scripts.py:5677` `_topsails_on` | lie a-try's topsail | none: **"Could not bring her to: She has no topsail to lie a-try under."** (observed) |
| `scripts.py:7389` `_is_upper_square` | the anchor's "In ... topgallants" | the topgallant is no upper sail (read) |
| `scripts.py:~7995` `_topsails` | the topsails by parent | none (read) |
| `evolutions/trim.py:61, 95, 151, 175, 226` `_LEVELS`, `_level`, `stagger`, `by_level` | each level braced in from the one below (Luce p. 418) | every yard of the pole at level 0: no stagger (read) |
| `orders/verbs.py:525` `_take_in_kind` | the take-in words | **"lower the main topsail": "A course is hauled up, not lowered; say 'haul up the main topsail'"** (observed) |
| `orders/verbs.py:1373` `_level_rank` | "trim the sails" by level | level 0 (read) |
| `physics/sails.py:894` `_yard_level` | the helm's mark, the highest square sail | level 0 (read; not reached on her, being no square-rigged ship) |
| `physics/sails.py:1001` `studding_level` | a studding sail's stall | lower (read; she carries none) |

What that does when she is sailed (observed):

| Order | The brig's masts (the probe) | Her main a pole |
|---|---|---|
| heave to | "Hauled up the courses." "The fore topmast staysail sheet to windward; braced the main topsail aback; helm a-lee." Hove to at 182 s; +600 to +900 s **58.4° to 58.5° off, 1.65 kn by truth 12's measure** (1.49 to 1.50 kn of headway): inside truth 12's 45-65°, **just over its 1.6 kn** | "Hauled up the courses." (the course **and the topsail**) "The fore topmast staysail sheet to windward; helm a-lee." Hove to at 144 s "under her fore-and-aft canvas"; **+600 to +900 s 59.9° to 60.1° off, 2.65 kn by truth 12's measure** (2.61 of headway; over its 1.6 kn) |
| lie a-try (with the topgallant set) | under the main topsail and the staysails at 396 s, 54.9° off, 2.60 kn | **refused**: "She has no topsail to lie a-try under." |
| take in the main topsail | clewed up 64 s, in the gear 112 s | the same, 65 s and 113 s: no difference |
| furl the main topsail | furled 219 s | furled 221 s: no difference |
| shorten sail at 30 kn | "All hands reef the main topsail", reefed at 522 s | the same at 528 s (the group "topsails" names it, so the gale's reduction finds it) |
| send down the topgallant yards | sent down at 568 s | refused, "The topgallant and royal yards are on deck already." (the probe keeps the brig's fore topmasts, which carry no yard; with every mast a pole the refusal says she has none, by reading `scripts.py:3873`) |
| send down the main topgallant mast; strike the main topmast | refused in words | refused in words ("no such part") |
| tack; wear | 164 s; 464 s | 162 s; 478 s |

Found beside it: **the smack's heave-to with her topsail set** hauls the topsail up as a course and
lies under her fore-and-aft canvas, 47.3° off at 2.61 kn by truth 12's measure (2.56 of headway;
observed, `smack.yaml` as committed, the topsail set first), where the fore-and-after's rule means her topsail "to the mast as well if it is
set" (`scripts.py:2819`'s docstring, read). Her topsail is out of her plain sail, so no pinned
passage of hers meets it (by reading; §18).

**What the engine must be given (A5, decision 6).** One predicate, `Ship.yard_level(yard)`: the
rank of a braced yard among the braced yards whose lower mast is its own, by height (0 the lowest,
the course), the yards under the bowsprit apart; read once a ship from the parts as filed and held
beside her as B3.4's memo is (`graph._SCHOONER_YARDS`, not pickled). Every one of the twelve places
reads it in place of the parent's class. **On every committed file but the smack it gives what the
parent's class gives today** (to be proved by the golden classing table and a guard over every file
at A5's step: the levels of every yard of every file, old beside new); on the smack it makes her
topsail level 1, a topsail, which moves her heave-to with that sail set (measured at the step, old
beside new).

**The pole mast's handing (A6, decision 7).** The period's mark of the rig is that the topsail and
topgallant come down together onto the lower yard ("amener en paquet", Lescallier p. 371; Röding),
and are loosed, reefed and furled from the yard below (Falconer; Steel p. 236). Today the engine
does neither: the take-in and the furl are the brig's to the second (observed above). Proposed:
- a pole mast's upper square sails taken in by letting go their halyards together, the yards
  lowered to the lower yard and the sails clewed up there: one evolution for the mast's upper
  sails, its time the lower of a brig's topsail take-in's (60 s clew-up and 45 s settling,
  `take_in_square.yaml`, read) and no settling per yard (JUDGEMENT: no period time found; the
  figure is the builder's to propose and the lead's to rule);
- `furl_square`'s `aloft` step on a pole mast's upper sail shortened (the men on the lower yard, no
  climb to a top; JUDGEMENT on the time), its hands the same topmen;
- `reef_square` on a pole mast's topsail: the yard lowered to the lower yard first (Falconer), the
  rest as now.
Without A6 she handles as a brig with one-piece masts, which is acceptable for a first file only if
the owner says so (§17).

**Against the package's engine note** (`Design-Package90-Engine.md` §4, written beside this draft):
it leans to a key on the mast (a pole) read by the take-in, the furl, the topmast evolutions and
the viewer, and to the square sails handed "from the deck, no men aloft". This draft proposes
instead **no key**: the pole is read from the parts as filed (a lower mast with braced yards above
its lowest and no topmast), as B3.4's rule is read, for B3.4's own reason ("a file that forgets a
key makes her a brig with no word said", the lead's ruling of 2026-11-06); and **men aloft on the
yard below**, not on deck, since Falconer and Steel p. 236 both put them on the lower yard to furl
the topsail and on the topsail yard to furl the topgallant (Pol §2.3). The two readings are for the
critic and the lead.

**What the pole costs her** (read): a pole mast breaks as one spar; every yard on it is its child,
so the strain stream's mast loss takes them all (`physics/strain.py:243`, the masts falling "from the
top down"; the pole is a `mast`, decaying at half the topmasts' ratio there, :247, read). Lescallier's
"the whole mast unrigged" is so by the parts. Whether a pole mast should decay at a topmast's ratio
(she carries her upper sails on it) is a figure for her builder to measure (§16 risk 4).

### 5.2 (b) Her lateen mizen hove to, and the heave-to's driver rule

- **Today it is kept set, as a fore-and-after's sail** (observed): she has one mast with braced
  yards (`_masts_with_yards`, `scripts.py:627`: `['main.mast']`), so the heave-to takes the
  fore-and-after's way (`fore_and_after`, :2819) with the main topsail to the mast; and the
  driver rule (`after_gaff_sails`, :747) gives nothing: it wants two masts with yards (:769, "if
  len(with_yards) < 2: return []") and a sail that `drives_aft` (:219), which a whole lateen does
  not (no `cut_at_mast`). Both lateens stay set at their sheets (25.7° and 25.6°) throughout.
- **Kept, she lies to, forereaching a little past truth 12's speed**: hove to at 182 s, 58.4° to
  58.5° off from +600 to +900 s at **1.65 kn by truth 12's measure** (`knots()`, `dyn.speed`),
  her headway 1.49 to 1.50 kn (observed, B3.4's harness to the letter; the engine note's 1.65 kn in
  its own harness, `Design-Package90-Engine.md` §2.2, is the same measure and agrees). Her angle is
  inside truth 12's 45-65°; her speed is 0.05 kn over its 1.6. **Plainly:** the first draft gave
  the headway as the truth's speed and called her inside the band; she is not, by a little. The
  lever for her own file is the fore lateen's sheet or trim hove to (eased, it draws less; JUDGEMENT,
  to be measured on her file, as the plan's §4 row 4 names the great lateen's trim for the
  tartane), never the mizen: P3's band is a target until it is measured there. **Taken in first** ("take in the mizen", brailed up at 115 s,
  then "heave to"): 68.2° off at +150 s, 88.0° at +300 s, 130.9° at +450 s, and "Could not heave
  to: she would not lie to on the starboard tack, the wind on the starboard quarter, abaft the
  beam" at 600 s (observed). The driver rule exists because a spanker set abaft the backed main
  brought the frigate to with sternway (`after_gaff_sails`' docstring, package 10); her small mizen
  does the reverse, holding her up against the fore lateen's drive.
- **Settled (decision 8): the driver rule does not reach her lateen mizen**, and should not be made
  to: taken in, she does not heave to at all, which is worse than forereaching a twentieth of a knot
  past the band. Her file gives it no `cut_at_mast`; a guard test pins that `after_gaff_sails` takes no whole
  lateen on any file, and her heave-to is truth P3 (§14). If question 1 (b) adds a square mizen
  topsail, she has two masts with yards and the rule's first condition is met, but her lateen is
  still no driver by `drives_aft`: the same result (observed on the variant: `driver: []`, §5.4).
- The period (JUDGEMENT): no polacre's heave-to was read; a ship's mizen kept hauled out while she
  lay to under a main topsail aback was the old practice the driver rule departs from for a big
  spanker (Steel 1794 vol. II p. 330: the balanced mizen hauled out in a gale to keep her to the
  wind, read there: `Research-Bilander-2026-10.md` §1.5).

### 5.3 (c) A whole lateen in stays: hauled aft by nothing, changed by nothing

**Today** (observed, the probe tacked from the settle):
- "Ready about. Helm's a-lee; ease off the head sheets." at 1 s; "Let go and haul. Draw jib; trim
  aft the head sheets." at 51 s; tacked at 164 s, "braced up on the larboard tack"; her way 3.18 kn
  at 30 s, 1.76 kn at 60 s, 0.14 kn at 90 s, **−0.51 kn at 120 s** (sternway, her head 31° off on
  the new tack), the least −0.66 kn.
- **Neither lateen is touched.** Each sheet stays at its angle (fore 25.7°, mizen 25.6°) from
  helm's a-lee to the end; each lateen lies on the old lee side until her head passes the wind
  (−4.9° at 60 s) and on the new lee side after, never backed, never shivering. Worn (464 s) the
  same: they go over at 90 s, the wind aft, set throughout.
- **Why** (read): a whole lateen is no head sail (`head_sails`, :207, wants a jib-headed sail
  forward of the foremost mast), no boom sail (`boom_sails`, :230, takes a gaff on a boom, a lateen
  `cut_at_mast` or a standing lug), and not shifted (`shifted_sails`, :314, wants a sided sheet; the
  lateen's one sheet is unsided). Its one sheet, belayed with no side held, lies to leeward of
  whatever wind comes (`trim.set_sheet_angle`'s docstring; `physics/sails.py:600-606`); and
  `against_the_mast` (:673) is a dipping lug's alone. So the yard is never changed, and leaving it
  unchanged costs nothing.

**Measured in the process only** (`boom_sails` widened by a monkeypatch in scratch; nothing in the
tree changed): the mizen lateen hauled aft at helm's a-lee as a spanker is ("haul aft the mizen
sheet", its sheet to the lateen's 8° floor): **157 s** against 164 s, the least way −0.60 kn; both
lateens hauled aft: 165 s, −0.65 kn (the fore lateen hauled aft holds her head back, as a head sail
hauled aft would). So the mizen worked as a ship's mizen helps her round a little (Steel 1794 vol.
II p. 316, "haul the mizen out while you put the helm a-lee", read there: Ext §2), and the fore is
to be eased as the head sheets are.

**What the engine must be given (A1, decision 9)** (for the owner's question 3 and the lead):
1. **In stays**: a whole lateen on the aftermost lower mast abaft the masts with yards is hauled out
   at helm's a-lee (a `boom_sails` reading for it: Steel II p. 316; "brace the bowline quite to
   leeward", Bourdé p. 87 and Steel II p. 316, read there); a whole lateen on the foremost mast,
   forward of the masts with yards, is eased off with the head sheets at helm's a-lee and drawn at
   "let go and haul" (`head_sails`' reading widened for it). Words only for her where the existing
   lines say "head sheets".
2. **The change round the mast** (*trelucher, muder l'antenne*, Lescallier p. 378; Fincham p. 60;
   Willaumez MUDER): after "let go and haul" (or, wearing, once the wind is aft), each lateen's
   runners cast off, its yard peaked up the mast, its heel passed round abaft the mast, the tack
   hooked on the new weather side and the sheet hauled aft to leeward. On the settee's machinery
   (`SetteeChange`, `scripts.py:394`) with the yard **peaked, not lowered** (Bil §1.5's way (b));
   the hands by the settee's road, `too_few: all hands` where her watch is short (package 75's
   ruling of 2026-11-10). Times JUDGEMENT, to be measured against the settee's.
3. **A lateen not changed lies against its mast**: `against_the_mast` read for a whole lateen whose
   yard is on the weather side of its mast (a `yard_side` beside `lug_side`), at the lug's area
   factor, so that the change has a reason in the physics (Willaumez MUDER: the sail pressed on
   the mast).
4. **"Worn, not tacked"** (the brief): if the owner rules question 3 (b), "tack ship" is refused in
   her words and every going about is a wear with the lateens changed when the wind is aft. If
   (a), she tacks as above.

The package's engine note (`Design-Package90-Engine.md` §2.3) builds the change as a dip, with
`dipping: true` allowed on the lateen class and the yard peaked and passed round, not lowered: the
same act as item 2 here, by the lug's key where this draft names the settee's machinery. One of
the two is built once for the tartane, the polacre and the xebec; the engine note's key is the
smaller change to the schema, the settee's machinery the nearer in its handling of a yard slung on
a mast that carries other yards (the bilander's main). **The plan settles the proposal** (Plan §4
row 3): `dipping` allowed on a whole lateen for its side and its loss against the mast, and a new
`change_lateen` evolution, peaked up and passed round, never lowered, its scripts on the settee's
B3.3 model. The lead rules it at A1's design.

### 5.4 (d) The schooner's-mast rule's two limits, for the file that first carries a pole main

The rule (`Ship.on_schooner_mast`, B3.4; the lead's ruling of 2026-11-06): "An after mast with yards
and no yard on its lower mast handles as a fore-and-after's mast". Its two recorded limits
(`TuningNotes.md` "The schooner's mast", "Left, and for whom"): a schooner with a lower square-sail
yard on her main, and one whose main is a pole mast with its topsail yard on the lower mast, each
classes as a brig. The lead's note gave them to "package 90 and B2, whichever files a pole main
first"; B2 (the *Neufchatel*) filed her main with a topmast, and no committed file has a pole main
among two masts with yards (observed), so **she is that file**. Classed through the golden table's
gates, plain sail set (observed). **Plainly:** the first draft said "she is that file"; the
tartane's design files her topsail yard on her main's own head with no topmast (Tar-D §4.1), so the
tartane is the package's first file with a pole main (one mast with yards, where the limits cannot
bite), and the polacre the first with a pole main among square yards and lateens:

| Rig | Masts with yards | Head; after yards | Square-rigged | Driver | Schooner's mast |
|---|---|---|---|---|---|
| The probe (the brig's masts) | main | main yard, main topsail yard; none | no | none | none |
| Her main a pole | main | the same; none | no | none | none |
| Her fore and main poles | main | the same; none | no | none | none |
| A square mizen topsail on a **pole mizen** (question 1 (b)) | main, mizzen | main's; mizen topsail yard | **yes** | none | none |
| A square mizen topsail on a **mizzen topmast** | main | main's; mizen topsail yard | no | none | **the mizen topsail and its yard** |
| Trial B with its main topsail yard filed on `main.mast` (limit 2, for comparison) | fore, main | fore's three; main topsail yard | yes | **the mainsail** | none |
| Trial A with a lower square-sail yard on her main (limit 1) | fore, main | fore's three; main yard | yes | **the mainsail** | none |

**Settled (decision 10):**
- **In Monleón's rig neither limit bites her.** Her lateen yards are no braced yards (`Spar.is_yard`,
  Ext §3.3), so her main is her foremost mast with braced yards, and "an after mast" never names
  it, pole or not. She is classed as the cutter's and the tartane's one mast with yards, her main's
  yards her head yards, as the rule's author read her (the lead's note of 2026-11-06).
- **A square mizen topsail (Steel's first polacre-settee, question 1 (b)) is classed two ways by
  where its yard is filed**: on a mizzen topmast the rule makes her mizen a schooner's mast and her
  a fore-and-after; on a pole mizen she has two masts with yards and is square-rigged. The second
  is the period's (Forfait p. 130's xebec after mast carries its square sail over the lateen; the
  mizen topsail is handled with the main's yards at "mainsail haul", a ship's way: JUDGEMENT), so
  her file would carry it on the pole mizen, and a guard pins that no file of hers has a mizzen
  topmast.
- **Neither limit reaches the xebec's other rigs either** (stated here once, for the package; the
  xebec's documents agree, Xeb §9 item 9, Xeb-D §4.3): Forfait's Spanish chebec (a square main of
  course and topsail between a lateen fore and a lateen mizen) has her main as her foremost mast with
  braced yards, so "an after mast" never names it; the chambequín, square on all three masts, classes
  as a ship (measured by the xebec's note on the frigate-36's row). **The limits stay with a
  schooner's main** (a lower square-sail yard on it; a pole main with its topsail yard on the lower
  mast) and stay recorded (`TuningNotes.md`, "Left, and for whom"); no file of package 90 meets them,
  so no remedy is built.

### 5.5 Her polar today, for the record

`world.ships.polar_of` (plain sail, 15 kn; observed):

| Off the wind | 40° | 50° | 60° | 70° | 90° | 120° | 150° | 180° | least angle |
|---|---|---|---|---|---|---|---|---|---|
| The brig as filed | 0.10 | 2.62 | 4.26 | 5.88 | 7.83 | 7.55 | 6.32 | 5.73 | 50° |
| The probe | 1.45 | 2.86 | 4.05 | 5.29 | 6.44 | 6.24 | 5.38 | 5.00 | 40° |
| Her main a pole | 1.20 | 2.71 | 3.96 | 5.23 | 6.41 | 6.25 | 5.44 | 5.03 | 40° |

The probe holds way 10° nearer than the brig, by the whole lateen's 8° sheet floor (Ext §3.1) and
the lateen row's curve, which is **untuned** (`docs/dev/TuningNotes.md` l. 127: "Lug, lateen and
sprit scaled to match (untested rigs)"). Lescallier's five points against six (p. 380) and Steel's
"one point nearer" (I p. 237) are the only figures against which it can be tuned (truth P2).

---

## 6. The guns (`Build-Ships.md` §6's postscript, package 81's checklist)

### 6.1 The fits

| Fit | Guns | Men | Source |
|---|---|---|---|
| `unarmed` (default) | none | her sixteen | the trade (Pol §5.3) |
| `armed trader` | six long 6-pounders, three a side in the waist | her sixteen; guns crewed by Falconer's rule for the new ships (D31 (c) of package 75) | James vol. 4 p. 346: a polacre-ship of six long 6-pounders and 20 to 30 men (1808) |
| `spanish navy 1800` (the polacre of war's default) | two long 24-pounders as bow chasers, two long brass 18-pounders as stern-chasers, four 12- and six 4-pounders on the sides (two 12s and three 4s a side), all brass | 49 seamen and 22 soldiers (71), the polacre of war's company | James vol. 3 p. 33: the *San Josef*, "the Spanish national polacre-ship", 1800 |
| `corsair` (the polacre of war's file; the regency's cruiser; question 4) | fourteen small guns, seven a side, "probably 4-pounders" | 71 filed; **80** her own, a departure in the note until the ship's configuration (`Design-Harbour.md`, designed and not built) gives a number, as the xebec's regency fit (Xeb-D §8.1) | James vol. 3 p. 160: a Tripolitan polacre-ship, Dale's cruise |

- **Not proposed now:** the *Virgen del Rosario*'s eight long 12- and two long 24-pounders,
  pierced for twenty, 94 men (James vol. 3 p. 149): a privateer heavier than the navy's own, on a
  hull pierced ten a side; a second privateer fit if the owner wants it.
- **The calibres** are James's English words for Spanish and Barbary guns; Winfield's rows give
  libras beside pounds for the navy's (take Winfield's pairs as given: the Spanish note's head). The
  navy's fit's calibres are to be read against Winfield's row for her if she is the *San José*.
- **Brass**: the *San Josef*'s guns are all brass. The weight table is Adye's (package 81's item 4);
  brass guns' weights for these calibres are to be read before her file (§17, for the lead).

### 6.2 Package 81's checklist, item by item

1. **`hull.profile`** with `rail_m`, `breadth_m` and `decks_m` (the upper deck, the one gun deck):
   §3's work.
2. **`ports_m.upper`**: a triple [x, sill, half-breadth] at every broadside gun's and chaser's own
   `x_m` (within 0.01 m). **One hull for every fit of both files**, so she is pierced for the most any fit
   carries: seven a side (the corsair's) with two bow chase ports and two stern ports (the navy's
   chasers): JUDGEMENT, the lead's to rule (§17), since a trader pierced seven a side is a heavily
   pierced trader (James's *Bella Aurora* of ten guns and the privateer pierced twenty make it
   credible). The armed trader's six stand in the waist's ports; the navy's ten broadside guns in
   five a side.
3. **`port_size_m.upper`**: [width, depth] one size for the deck: a 12-pounder's port (the navy's
   largest broadside gun), JUDGEMENT on its figures until a plan.
4. **Every gun's** `kind`, `pounder`, `place`, `side` (but a pivot), `x_m`, `weight_cwt` (the
   pattern of nearest weight in Adye's tables; a weight from memory listed when more than a tenth
   off), and `deck: upper` for each broadside gun and chaser.
5. Then `python tools/check_viewer_guns.py` on `data/ships/polacre.yaml` and
   `data/ships/polacre-of-war.yaml`, both clean, and its test.

### 6.3 The magazine

A trader's (`MERCHANT_ROUNDS`) for the armed trader; the navy's by package 70's rule for the
navy's fit; the corsair's as the privateer's book gives a privateer (JUDGEMENT).

---

## 7. The company and the people file

### 7.1 In trade: sixteen (decision 12)

| Post or rate | Number | Watch | Note |
|---|---|---|---|
| master (*capitán* or *patrón*) | 1 | larboard (heads it) | a post; a working officer by ruling 11 |
| mate (*piloto*) | 1 | starboard (heads it) | a post; a working officer by ruling 11 |
| boatswain (*contramaestre*) | 1 | larboard | |
| carpenter | 1 | idler | for `repair the wheel` (package 116's evolution wants four able hands of the idlers and afterguard) |
| cook | 1 | idler | |
| seamen | 9 | five and four | |
| boys (*grumetes*, *pajes*) | 2 | one each | |

- **JUDGEMENT within twelve to twenty**: no trading polacre's crew was read (Pol §5.3, §11). The
  Mediterranean manned more heavily than the North Sea (the *Vergine del Carmine*'s nine to sixty
  tons; Forfait's fifteen men for a Dutch ship of 470 tonneaux against the King's thirty for 350:
  read), and the lateens' change wants hands (Winfield's xebec: the square rig's smaller crew).
- **The working officers (ruling 11)**: the master and the mate counted a hand of their own watch
  for deck work only where the watch's whole number is under the work's want; never aloft, for all
  hands, at quarters or for one of the twelve manoeuvres (`Build-Ships.md` the ruling's row, read).
  Their `watch:` in her people file (the master the larboard, the mate the starboard, as the three
  merchantmen's and the bilander's).
- **Her watches** of seven and six (with their posts eight and seven) begin a watch's work on deck;
  the lateen's change and the main topsail's reef want more and call all hands by the settee's road
  (`too_few: all hands`), as a small coaster called for her great sail's work (package 75's ruling
  of 2026-11-10, the lead's judgement there).
- **The wheel** (package 116): every ship has one in the engine; the relieving tackles want six
  ordinary hands of the afterguard and waisters (`relieving_tackles.yaml` l. 35, read), which her
  watch on deck has with its post; `repair the wheel` four able of the idlers and afterguard
  (`repair_wheel.yaml`, read): her carpenter and three of the watch. A trader of her size steering
  by a wheel and not a tiller is JUDGEMENT.

### 7.2 The polacre of war's file: seventy-one

- **The navy's** (`spanish navy 1800`, the file's default): 49 seamen and 22 soldiers or marines
  (James vol. 3 p. 33), the file's company,
  her officers JUDGEMENT (a lieutenant commanding and a second, a pilot; the Spanish navy's ranks
  for a small vessel to be read in Winfield's row); the marines file's Spanish row for the 22.
- **The corsair's**: filed at the file's 71, her own 80 (James vol. 3 p. 160) a departure in the
  note, as the xebec's regency fit's 150 is filed at the King's 113 (Xeb-D §8.1). **Package 110's
  rulings bind** (the owner,
  2026-11-12 and 13): Barbary captivity in its middle form, no player at a corsair's station, a
  model at one only under a brief that says plainly what it is and may do (§8.1 there); her people
  are spoken of as people. Nothing of captivity is the ship's: her role's doctrine says what she
  does with a prize, and package 110 what becomes of the people.

### 7.3 Her people file and names

`data/people/polacre.yaml` in the bilander's form (the master, the mate, a boy to carry the word),
and `data/people/polacre-of-war.yaml` in the brig's (her commander, a second and a pilot, §7.2),
outlines bred in the Spanish coasting and Levant trade (JUDGEMENT; no one named); `names: spanish`, a
new list in `data/crew/names.yaml`, sourced from a period muster or register before it is filled
(§17, for the lead).

---

## 8. Ground tackle, boat, pumps, hold and stores

By the merchant brig's rules at her size (package 34's anchors with hemp cables; package 35's
boats: a long-boat amidships and a small boat; the pumps and hold as hers): rule R by the game's
own rules, JUDGEMENT on their carrying to a Mediterranean hull. **Plainly:** the tartane tows her
boat (the brief); the polacre carries hers on deck (JUDGEMENT: a vessel of her size; no source).

---

## 9. Her description: what is made out, and when (the made-out rule)

The rule (`freesail/world/ships.py` l. 28-36 and 94-104, read): the tops make out a sail's rig at
`RIG_MADE_OUT_NM` (4.0), her colours at `COLOURS_MADE_OUT_NM` (2.0), what she is at `MADE_OUT_NM`
(1.5); a glass sent aloft reaches `GLASS_FACTOR` (1.5) further: 6.0, 3.0 and 2.25 miles. A far
vessel's size is read from what is made out (`captains.size_of_words`, :349).

| Key | rig (at 4 miles; 6 with the glass) | what (at 1.5 miles; 2.25 with the glass) | fit | roles |
|---|---|---|---|---|
| `polacre` | "a polacre" | "a polacre, a Mediterranean trader, deep laden" | `unarmed` | `merchant` |
| `armed polacre` | "a polacre" | "a polacre, an armed trader, three ports a side" | `armed trader` | `merchant`, `privateer` |
| `polacre of war` | "a polacre" | "a polacre of war, five ports a side and chase guns in her bow" | `spanish navy 1800` | `kings-ship`, `cruiser` |
| `corsair polacre` | "a polacre" | "a polacre-ship, a corsair, seven ports a side, her deck crowded with men" | `corsair` | `corsair` |

The first two rows are `polacre.yaml`'s, the last two `polacre-of-war.yaml`'s (decision 1).

- **The rig word, "a polacre"** (JUDGEMENT on the words): what the tops see at the rig's distance
  is the rig's mark, as with the bilander's settee: three masts with **no tops**, the fore raked
  forward under a great lateen, the square sails on the main alone, a lateen on the mizen (Falconer,
  Steel, Lescallier: the rig named on sight). A pole mast's want of tops is what tells her from a
  ship or a barque at the distance where masts are told (JUDGEMENT on what the eye resolves).
- **The registries** (in her window): `_SIZE_WORDS` gains `("polacre", 2)` **before "brig" and "a
  ship"** (so "a polacre-ship" ranks 2 and not a frigate's 3; "polacre brig" not a brig's by
  accident of order: `captains.py:331-346`, read); `SIZE_RANK["polacre"] = 2` (a three-master of a
  brig's size); `lookout._RIG_WORDS["polacre"]` (`lookout.py:314`); `DESCRIPTIONS["polacre"]` and
  `_DESCRIPTION_WORDS`: "a polacre", "polacre", "a polacca", "polacca", "a polacra", "polacra", "a
  polacre-ship", "polacre-ship" (`ships.py:308`). None of these words is in the game's text now
  (grep over `freesail/` and `data/`: "polac" only in three comments, `orders/storm.py:445`,
  `ship/graph.py:228` and `ship/schema.py:611`, and in the tests' fixtures; observed).
- **"Merchant" in the trader's words** makes her a cruiser's weaker mark, and a merchant hull never
  a superior force, as the bilander's (her design §8, read).
- `ship.rig: polacre`, served as the graph's `rig`.

---

## 10. The polar: what her builder measures

Her polar by `polar_of` on her file; the least angle with a knot of way at 15 kn against the
merchant brig's and the tartane's; her speeds at 60°, 90°, 120° and 150°; the same with the main
topgallant set and taken in. The lateen curve is untuned (§5.5): the polar's figures are the
lateen row's until truth P2 pins it, and a tuning of that row is the tartane's package step (the
lateen's first file), measured there and read here.

---

## 11. Where she sails

79c's water (the Strait to Cartagena and the Balearics; the scenarios `mahon`, `morocco`, `bona`
on the trunk name its ports, read: `data/scenarios/`). Her scenario, when the ships' scenarios'
package makes it, wants a line on the harbour's **Trade** shelf (`client/harbour-shelves.yaml`,
id `trade`, read): one sentence, for example "A Spanish polacre working up from Cartagena to Mahon
with oil, the wind ahead." (JUDGEMENT; the scenario's own package writes it).

---

## 12. Interfaces: what the engine must be given, step by step

| Step | What | Files it reaches | Proof that nothing else moves |
|---|---|---|---|
| **A5**, the yards' level | `Ship.yard_level(yard)` read at the twelve places of §5.1 | `ship/graph.py`, `evolutions/scripts.py`, `evolutions/trim.py`, `orders/verbs.py`, `physics/sails.py` | a guard over every file of `data/ships/`: every yard's level old beside new, equal but for the smack's topsail; the golden classing table unmoved; the smack's heave-to and lie a-try measured old beside new with her topsail set |
| **A6**, the pole mast's handing | a pole mast's upper sails lowered "en paquet" onto the lower yard; the furl and reef from the yard below | the take-in and furl evolutions' data and scripts | no committed file has a pole mast with two yards above its lowest but the smack (whose two yards are a square sail and a topsail: she would gain the quick handing of her topsail; measured) |
| **A1**, the whole lateen in stays | §5.3's items 1 to 3; item 4 on the owner's word | `evolutions/scripts.py` (the tack, the wear, a lateen change on the settee's machinery), `physics/sails.py` (`against_the_mast`), new evolution data | no committed file has a whole lateen (the 64's and the 74's mizen courses are `cut_at_mast`: read); the tartane's file is the first to meet it |
| **V1**, the whole lateen drawn | §13 | `client/projection.js` | the drawn pictures of every committed file unchanged |
| Her rows | §9's registries | `world/captains.py`, `world/lookout.py`, `world/ships.py` | no text of the game says "polacre" now |
| Her names | `spanish` in `data/crew/names.yaml` | data | the three lists unchanged |
| The regency's cruiser | a new role `corsair` and its doctrine book `data/captains/corsair.yaml`, every key under `thresholds:` (package 116's road: the cruiser's thirteen prize keys were moved there because the reader reads nothing else), each with its source: boarding early and by numbers (`board_odds`, `board_when`; the Tripolitan's 80 men in a polacre of fourteen small guns, James vol. 3 p. 160), the prize doctrine, the engaging and evading figures; its people's fate package 110's, never the book's | `data/captains/`; `world/brains.py`'s role reading | the existing books unchanged; no file takes the role but hers (and the xebec's, which shares it) |

**The allotment** (the plan's §6 and §9.1): A5 is general (any pole mast) and small, and A6 is
any pole mast's; both come before the tartane's file, whose topsail stands on her pole main's head
(the critic's F3). A1 and V1 are the lateen class's, built on the engine track before the
tartane's file, the first whole lateen.

---

## 13. What the viewer must draw

- **Her fore raked forward**: a negative `rake_deg`, drawn today (`docs/gates/gate-m2.md` l. 103).
- **Her pole masts as single sticks**: the viewer draws an upper mast overlapping the one below by
  `DOUBLING` (`client/projection.js` l. 56, 731, read); a pole draws none, which is the rig's mark.
  No tops are drawn for any ship (read: no top or crosstree platform in the viewer), so nothing is
  to be taken away; the rope ladders are below the 2-px rule (§5.0 principle 2).
- **Her whole lateens, new (V1)**: the viewer draws a whole lateen today either as a four-cornered
  sheet under a yard braced as a square yard and tilted a fixed 0.8 rad (with no corners: l. 904,
  1537) or as a standing lug on its lee side (with four corners: l. 815, 1506), "until the package
  that builds a whole lateen draws it as its own" (l. 815-816). Wanted: a three-cornered sail from
  the yard's lower end to its peak with the clew aft, its yard slung at a third on its mast's raked
  line, on its lee side; drawn peaked up its mast while it is changed; against its mast when not
  changed (A1 item 3).
- **The square sails lowered "en paquet"**: the topsail and topgallant yards drawn down on the
  lower yard while their sails are lowered (A6).
- **The long bowsprit of one piece**, its jibs; the beak; her ports and guns by package 81's rule
  (§6.2), nothing drawn by hand.
- Pictures for the owner's testing report: abeam under plain sail; from ahead (the fore's rake and
  lateen); hove to; with the main's upper sails lowered.

---

## 14. Tests and truths proposed (numbered by the build document)

- **Her tests** (`tests/test_polacre.py`): her particulars against their notes; her classing (her
  main her one mast with yards; her lateens no driver, no boom sail; no file of hers with a mizzen
  topmast); `after_gaff_sails` never takes a whole lateen (a guard over every file).
- **P1, her particulars hold their sources**: her size and masts as their notes say (Winfield's
  metres, Forfait's rule).
- **P2, she lies nearer the wind than a brig of her size**: a knot of way at 15 kn at an angle a
  point or so closer than the merchant brig's (Lescallier p. 380; Steel I p. 237). Observed on the
  probe: 40° against 50° (§5.5). Its band JUDGEMENT, set with the lateen row's tuning.
- **P3, hove to with her main topsail to the mast and her lateens set, she lies within truth 12's
  band**: observed on the probe 58.5° off at 1.65 kn by truth 12's measure (1.49 kn of headway),
  just over the band's speed, so the band is a target until it is measured on her file with its
  lever (§5.2); and the guard that taken in, the mizen's want
  makes her fall off (observed: the heave-to fails at 600 s).
- **P4, "amener en paquet"**: her main topsail and topgallant handed together onto the lower yard
  in less time than the merchant brig takes in both (Lescallier p. 371): after A6.
- **P5, going about costs her the lateens' change**: her tack (or wear, by question 3) against the
  merchant brig's, the change's time and hands said in the log (Lescallier p. 378): after A1.
- **P6, a pole mast lost is a whole mast lost** (Lescallier p. 372): her main carried away takes
  every yard with it, and no topmast is to be fidded (by reading `strain.py`; to be run at her
  build).

---

## 15. Pins her work could move

- **A5**: the smack's heave-to and lie a-try with her topsail set (observed today: her topsail
  hauled up as a course); every other file's levels equal (to be proved). The smack's pinned
  passages do not set her topsail in plain sail (her plain sail is the mainsail, foresail and jib:
  observed), so none is expected to move.
- **A1**: no committed file (no whole lateen); the tartane's and the xebec's own.
- **Her rows**: none (no text says "polacre").

---

## 16. Risks, ranked

1. **Her size and hull rest on judgement** until the owner's Winfield passages come (Pol §11).
   *Mitigation:* no file until then; the figures of §2 are a probe's, not a ship's.
2. **The lateen curve is untuned**, so her windward work is the class curve's (§5.5). *Mitigation:*
   tuned once at A8 on the lateen hulls on the branch at the time, against Lescallier's five points
   (the plan's §4 row 7); P2 here, re-measured old beside new when she lands.
3. **A1 is the largest engine step** (the lateen's change on the settee's machinery, peaked not
   lowered; the physics of a lateen against its mast). *Mitigation:* built once for the three
   lateen hulls; the bilander's settee change is its model and its tests the guard.
4. **A pole mast's strain**: it decays at a lower mast's half ratio though it carries the upper
   sails (`strain.py:247`). *Mitigation:* measured on her file at the build; the owner's word if it
   moves her gale.
5. **A5 touches twelve readers.** *Mitigation:* one predicate, equal on every committed file but
   the smack, proved by a guard of every yard's level.
6. **The jibs' stays and the fore lateen's yard**: unsourced rigging (§4.5). *Mitigation:* the
   owner's eye on Monleón; a lead's ruling.
7. **Package 110's rules for the corsair role** must be met in her role's doctrine and words.
   *Mitigation:* the role's doctrine says only what she does with a ship; package 110 holds the
   people's fate.

---

## 17. Open, for the owner and the lead

### 17.1 For the owner (few and plain; my pick first)

1. **Her rig.** (a) **Monleón's, as you chose: lateen fore raked forward, square pole main with
   course, topsail and topgallant, lateen mizen, jibs on a long bowsprit** (my pick). (b) Steel's
   first polacre-settee, a square mizen topsail over the lateen mizen. (c) The Provençal polacre,
   square on three pole masts, as a later fit.
2. **Her hull and size.** (a) **A Mediterranean merchant hull of about 200 tons with a beak, its
   size from a Spanish polacra in Winfield once you send the rows** (my pick). (b) The xebec-like
   hull of O'Scanlan's 1831 polacra, from the xebec's draught.
3. **Going about.** (a) **She tacks and wears as a brig of her size, her two lateen yards changed
   round their masts in both** (my pick, JUDGEMENT: no source read says she could not, and her
   square main tacks as a brig's; Willaumez's text describes a square-rigged polacre, with no
   lateens, tacking, and the plate was not viewed). (b) The brief's "worn, not tacked": she wears
   only.
4. **Her fits and roles.** (a) **Two files of one hull: the trader's, unarmed (the default) and
   the armed trader, sixteen men; the polacre of war's, the Spanish navy's (San Josef's fourteen
   brass guns and her 71) and the regency's cruiser as a role on the corsair's fourteen small guns,
   her 80 filed at 71 with the departure recorded** (my pick), the privateer a role of the armed
   trader. (b) The trader's file alone, and the navy's later.

**The passages to ask for** (Winfield, *Spanish Warships*; by title and class): the eight
**polacras** of about 1780 to 1818, each with her dimensions and Winfield's metres, tons, guns, men
and fate; whether a **San José** (Fuengirola, 28 October 1800) is among them; the **caption of
Monleón's polacre** on p. 1084 with the Museo Naval's number; any **bergantín-polacra** and
**polacra-goleta** entries. And from Winfield's British volume (1793-1817): **HMS *Calpe* (14)**,
the polacre-sloop of 1801 (was she the *San José*? memory, unverified), and **HMS *Fortune* (10)**,
polacre, 1799. And, in the owner's own words, the hull in Monleón's print (stern, head, ports,
sheer). (Pol §11.)

### 17.2 For the lead

1. A5 as its own small step before the tartane's file, the package's first pole main, the smack's
   heave-to measured old beside new with her topsail set (§5.1, §15); and the second file's name,
   `polacre-of-war.yaml`, with the plan's other file names (Plan §13.1 item 5).
2. A6's times (no period figure found): the builder's proposal, the lead's ruling.
3. A1's design (the plan's proposal, §5.3 above); and whether a lateen left unchanged lies
   against its mast (A1 item 3) at the lug's area factor.
4. Her ports: pierced for the corsair's seven a side on one hull for every fit (§6.2 item 2), or
   the trader's hull plain and the armed fits' ports her fits' own.
5. Brass guns' weights for the navy's fit (§6.1): a source to read before her file.
6. A `spanish` names list (§7.3): its source, shared by package 90's hulls.
7. The jibs' stays against the fore lateen's yard (§4.5): a ruling on the rigging.

---

## 18. Found on the way

1. **A pole mast's upper sails are courses to the engine** (§5.1): any file with a yard above
   another on one lower mast, today the smack. Her heave-to with her topsail set hauls it up and
   she lies under her fore-and-aft canvas at 2.61 kn by truth 12's measure (2.56 kn of headway;
   observed), where her fore-and-after's rule
   means her topsail to the mast. For the lead; A5 mends it.
2. **"lower the main topsail" on a pole main** is answered as for a course, "A course is hauled up,
   not lowered; say 'haul up the main topsail'" (observed; `verbs.py:525`). A5 mends it.
3. **Lie a-try finds no topsail on a pole mast** (observed; `scripts.py:5677`). A5 mends it.
4. **"Send down the topgallant yards"** on the probe with a pole main says "on deck already" (the
   probe's fore keeps the brig's topgallant mast with no yard on it): a probe's artefact, but the
   words would mislead on any rig with a bare topgallant mast (`scripts.py:3882`). For the lead.
5. **Willaumez's text** used here is the owner's private bilander checks' OCR
   (`owner-notes/bilander/rmg/measurements/bilchk/will.txt`); the dictionary is not in the tree.
   If the build cites it, it is filed under `docs/references/` with its row first (the README's
   rule).
