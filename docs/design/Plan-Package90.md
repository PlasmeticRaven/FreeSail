# Plan: package 90, the Spanish and Mediterranean ships (the preliminaries' plan)

**Status (2026-11-18).** The implementation plan for package 90, written during the preliminaries.
The lead's note of 2026-11-18, 00:50 UTC (nudge 15), frees research and planning only. The plan
follows the form of `Plan-ShipsWorkflow.md` (the phases, the method, the scale) and of
`Build-Ships.md` (stage 0, the engine's steps, file ownership, each hull's road, the tests,
truths and pins).

**Nothing in it is built.** It changes no file but itself: no code, ship file, generator, scenario
or test, and nothing the suite reads. It ends in a draft scope card for the build (§14), one
page, for the lead to put to the owner. The owner's questions are in
`docs/design/Decisions-Package90-2026-11.md` (**Dec**).

**This is the plan's second version (2026-11-18).** It is revised on the critic's reading of the
six documents it draws on and of its own first version (25 findings, F1 to F25), and on those
documents' second drafts (Phase 2, §3). What each finding changed is listed in "How this version
answers the critic", below the brief.

**Third draft, 2026-11-18, on the owner's answer to question 3** (the lead's note of 04:30 UTC,
nudge 17). The owner agreed nine of Dec's ten questions as picked and re-opened the third: a
vessel with a lateen main tacks and wears as others do, each an ordered evolution, and the change
of the yard round the mast is "preferred but not necessary" (Dec 3 and Part F, verbatim). The
research note of the same day finds no source that says a lateen vessel could not tack
(`Research-LateenGoingAbout-2026-11.md`, **GA**). This draft records the answers (§0) and
corrects the tartane's row of §1.1. It re-plans A1 as four steps, A1a to A1d (§6, §9.1, §10, Eng
§14). It brings into line the brief, what binds, §4's rows 1 to 4 and 16, §5.2 (stage 0L's
practice in place of `wears_only()`), §7.1 (the engine track's new files), §8.0 to §8.3, the cost
(§11), the risks (§12), the lead's rulings (§13.1) and the card (§14).

**What binds, in order:**
1. **The lead's note of 2026-11-18, nudge 15** (`docs/dev/M7-WorkPackages.md`, the last
   paragraphs of the ships session's notes), **and that of 04:30 UTC the same day, nudge 17**:
   the owner's answers to Dec, question 3 re-opened, and its re-plan, documents alone (this third
   draft).
   - What is freed and what is not. What is not freed: code, ship files, the generator, scenarios,
     tests, anything the suite reads.
   - The stopping point: the session's report on the preliminaries.
   - Items 8 and 37 of the list of 79. Item 8 is settled in the polacre's design, Pol-D §5. Item
     37 is reported in the engine note, Eng §1.
   - What has changed on the trunk: package 96's shelves; package 116's wheel, anchor and
     `thresholds:`; packages 115 and 117.
2. **`docs/dev/ScopeCards-BeforeTheGate.md`.**
   - Before any building package, a one-page scope card agreed with the owner.
   - One building package at a time.
   - The owner's gate of milestone 7 before new building, unless the owner says otherwise.
   - "How a package runs, as amended by the owner on 2026-11-16".
3. **The owner's rule on mends** (2026-11-14, `docs/dev/M7-WorkPackages.md` l. 134). Every mend
   ruled from a reading is made at its general cause, is looked for elsewhere, and is tested at
   that level.
4. **Row 90 and the lead's notes to the ships session** of 2026-10-29 and 2026-11-06 (18:00):
   - the five hulls, from the smallest up;
   - B3.1's lateen handling, "worn, not tacked; the yard dipped round the mast", replaced for this
     package by the owner's answer to Dec 3 (2026-11-18): tacked and worn, the yard changed round
     the mast or left;
   - the schooner's-mast rule of B3.4 and its two classing limits;
   - the regency's cruisers as a role;
   - Winfield's metres, and Winfield's pairs of libras and pounds as the book gives them.
5. **The owner's choice of 2026-11-12 for package 90's builds.** This session stays local, for
   research and coordination. One cloud session per hull builds and tests once stage 0 has
   landed, each on its own branch, checked and merged here.
6. **The trunk's standing rules:**
   - no name of a model or its maker in any file;
   - ship files only through the generator, and a generated file only by its tool;
   - pins moved only where measured, old beside new, and passed by someone other than the one who
     moved them;
   - never a test skipped, disabled or quarantined;
   - truths pin states, counts, ticks and bands, never digests.
7. **`Build-Ships.md`:**
   - §5.0's aim, principles and ladder of evidence;
   - §6's postscript, package 81's checklist for a hull's ports and guns;
   - §8's fits and roles;
   - §14.2's guard set and §17's review lenses.

   And `Design-ShipsEngineExtensions.md`, **Ext**: B3.1 the lateen, B3.3 the settee, B3.4 the
   schooner's mast.
8. **`Design-SlaveryAndSuppression.md` §8.** No seat for a player at a regency's cruiser. A
   model's seat only under a brief not yet in the consent documents. Every kind of hull a regency
   sails is open to the player under another flag.

**The documents it draws on:**
- **Eng**: `Design-Package90-Engine.md`.
- **Tar**, **Pol**, **Xeb**, **Dia**, **Con**: the five research notes (`Research-*-2026-11.md`).
- **Tar-D**, **Pol-D**, **Xeb-D**, **Dia-D**, **Con-D**: their designs, each in its second draft
  (`Design-Ship-*.md`).
- **VR-Sp**: `VesselReferences-2026-11-Spanish.md`, Winfield's facts by page in the lead's words.
- **Build**: `Build-Ships.md`.

**Marks.**
- *read*: a document, or the code at 68e769ef.
- *measured*: a figure from a sibling document's scratch probe, cited there. This plan ran no
  suite. For its second version the critic's two runs (the polacre's heave-to by truth 12's own
  measure; the tartane's topsail on a pole main) were run again in scratch and agree; they are
  cited in the hulls' second drafts (Pol-D §5.2, Tar-D §5.1a).
- **JUDGEMENT**: this plan's own reasoning.
- "Plainly:" marks a departure from a draft, a ruling or the brief, with its reason.

Every `file:line` is at 68e769ef, where the package's branch was cut from the trunk.

---

## In brief

- **The five hulls, from the smallest up:** the tartane, the polacre, the xebec, the corvette
  *Diana* and the *Purísima Concepción* three-decker. Each has a research note and a design in
  its second draft. The engine note measured what the engine does with each of them today. What
  the engine does is run or read, each marked so, never guessed (§1).
- **What the engine must be given** is listed in §6:
  - item 37 (A0);
  - the whole lateen tacked and worn, its yard changed round its mast or left, on the owner's
    answer to Dec 3 (A1a to A1d), and in a gale with its row tuned (A8);
  - the words of a rig with no yards (A2);
  - a tiller's words (A3);
  - the boat in tow (A4);
  - a yard's level read from its place on the mast, and the pole mast's quick handing (A5, A6);
  - sweeps that leave a ship a ship (A7);
  - three gun decks (A9);
  - the viewer's whole lateen, pole mast, towed boat and middle-deck words (V1 to V4);
  - the shared data: Spanish names, the corsair's role, a Spanish marines kit (N1 to N3).

  Each step is keyed on something no committed file carries, so that every existing ship sails
  as she does today. The exceptions are each named in the card with what it moves:
  - item 37 (A0), by the road the owner chooses;
  - three older faults the package meets (A2, A3, A5), mended at their cause because the
    owner's rule asks it;
  - three that reach existing ships by their keys: the pole's quick handing reaches the smack's
    topsail (A6) and its drawing her picture (V2), and the viewer's port words move the 74's and
    the 64's "a lower port" (V4).
- **Behaviour-free first.**
  - **Stage 0** lays the hooks, the five module stubs, the keyed registry rows and the inert keys
    (§5.1).
  - **Stage 0L** lays the whole lateen's interfaces once the lead has approved A1's design
    (§5.2).

  Each stage-0 commit is checked by an agent that did not write it.
- **Two roads, after stage 0 and item 37** (§9).
  - **The ship-rigged road:** the *Diana*, then the three-decker. They need little of the engine.
  - **The lateen road:** the engine's steps in one track, with the tartane, the polacre and the
    xebec each built as her steps land.

  Each hull is built in a cloud session of her own, beside the engine track and the viewer's,
  with at most four sessions at once. Each hull ends with a testing report. This session checks
  and merges each branch, and the lead gates each reported hash.
- **The owner decided ten things** (Dec): nine as picked and the third in their own shape, on
  2026-11-18 (§0):
  1. when the build begins, and its order;
  2. item 37's road;
  3. how the lateen ships go about;
  4. the tartane's size, her main's rake and the tréou;
  5. the xebec's size, and the chambequín;
  6. the xebec's sweeps;
  7. the *Diana*'s guns when she was taken;
  8. the three-decker's fits, soldiers and rank;
  9. how a foreign gun's pounds are written;
  10. four questions on the sources.

  The owner is also asked to source Winfield's passages, listed by title and class (Dec, Part D).
- **The cost on the owner's machine** is one fast tier, which is stage 0's base, plus short checks
  at each merge: about three and a half to five and a half hours over the whole package (§11).
  The builders' suites and the lead's whole suites run in the cloud.
- **The card** (§14) covers the whole build, with five stopping points at which the owner can try
  what has landed.

---

## How this version answers the critic

The critic read the five designs, the engine note, this plan and the decisions sheet against their
research notes and sources, and re-ran two probes. Every finding was checked; none was refuted.
Each is mended where it lives and in every document that repeated it.

| # | Finding, in short | Mended in |
|---|---|---|
| F1 | The polacre's heave-to: 1.49 kn was her headway; truth 12's own measure reads 1.65 kn, over its 1.6 | Pol-D decision 8, §5.1, §5.2, P3; Pol §8; Eng §4; §1.1 here. The settlement stands (the driver rule must not reach the mizen); her lever named |
| F2 | A personal path, with the account's name, written out in two notes | Con-D marks; Con §0 |
| F3 | The tartane's own main is a pole, so her topsail is a course today | A5 and A6 before her file (§6, §8.1, §9.1); Tar-D §5.1a, §5.3, §5.4 item 10, T-5; Eng §3; Pol-D §5.4 |
| F4 | A loop in the order: A8 waited on the polacre, the xebec on A8, the polacre on Winfield | A8 tuned on the lateen hulls on the branch then (§4 row 7, §6, §9.1) |
| F5 | The card under-stated what moves in existing ships | In brief; §14's Purpose and Expected to move (A6, V2, V4) |
| F6 | The polacre's one company of 16 for fits of 71 and 80 | Two files (Pol-D decisions 1, 12; §4 row 12; §7.1; §14's eight files; Dec Part E) |
| F7 | The engine note's lateen mizen read by the driver rule | Eng §2.3 item 5, §14; §4 row 4's last column |
| F8 | Willaumez's tacking polacre is a square-rigged one | §4 row 1; Pol-D §17.1 question 3; Pol §4, §10, §12; Dec 3 |
| F9 | Plans not yet read were given rungs | §1.1; Tar-D decision 4, §3; Tar's ladder; Xeb-D decision 3, §3.1; Con-D decision 3, §3.2; Con §2.3 |
| F10 | The xebec of 30 "about 38 m": no source gives it | Xeb-D §18.1; Xeb §2.2; Dec 5 |
| F11 | The soldiers' other way "as Winfield gives them": no breakdown is held | Con-D decision 10, §6.1, §17; Dec 8 |
| F12 | The tartane's size sketch, and "exactly your rig" | Tar-D §16.1; Dec 4 |
| F13 | The tartane's mizen rake and outrigger taken from the watercolour | Tar-D decision 10, §4.2 |
| F14 | The *Diana*'s 1809 drawing: unvetted, "made aboard", the credit shortened | Dia-D §17.1, §17.2; Dia §9; Dec 7, Dec 10 |
| F15 | B3.4's limits handed in a circle, the chebec called the first limit | Pol-D §5.4 (stated once); Xeb §9 item 9; Xeb-D §4.3; §4 row 17 |
| F16 | "a coastguard" and the game named in a ship's words | Tar-D §8, §9, §12 ("a guarda-costa"); Xeb-D §5 |
| F17 | Winfield's "length" labelled "Length overall" in VR-Sp | Con-D §2; Con §2.1 (the *Diana*'s plan the reason, JUDGEMENT) |
| F18 | The polacre's working tonnage misapplied the old measure | Pol-D §2.1 |
| F19 | Unit labels (pieds, inches, pies de Burgos) | Xeb "In short", §0.3; Dia §3.2; Dec Part D C1 |
| F20 | Two of Forfait's ratios disagree with their figures | Tar §2.1; Tar-D decision 11 (to re-read before a constant) |
| F21 | The heritage inventory's rung; "all of this was run" | §1.1; In brief |
| F22 | A7's far-body pace lives in a file no owner was given | §6 A7; §7.1; §14's May change |
| F23 | Two pace measures in different worlds | Con-D §9; Con §7; §1.1 (truth 7-196's world, Eng §7) |
| F24 | The headsails put to the owner, the rake to the lead; the Greenwich sheets treated two ways | Tar-D §16; Tar §9, §11; Dec 4, Dec 10; §4 rows 19-20; §13.1 |
| F25 | "Nothing written in the tree": the probes wrote bytecode caches | Eng §0; Pol-D marks; the other notes' marks ("no tracked file changed") |

---

## 0. The owner's decisions (answered 2026-11-18)

The questions are in Dec, each with the pick first, a plain sketch of what it means in play, and
where the evidence is. The answers are recorded there verbatim (Dec, Part F), and here. **Nine
were agreed as picked** ("I agree with the proposals", the owner, 2026-11-18). **The third was
answered in the owner's own shape**, the row below.

| # | Question | The answer (the pick, unless said) | Evidence |
|---|---|---|---|
| 1 | When the build begins, and in what order | After the gate. Then two roads at once (the ship-rigged and the lateen), one cloud session a hull | §2, §9; Dia-D §0 |
| 2 | Item 37, the generator's copy of the sail-force law | (a) Mend the cause: the generator reads the engine's curves, rounded, and a test holds the two together | Eng §1 |
| 3 | How the lateen ships go about | **The owner's shape, not the pick.** A vessel with a lateen main tacks and wears as other vessels do, each an ordered evolution with her own words, hands and time. Changing the yard round the mast is a part of either that may be done or left: done in stays or in the wear by her practice ("shift" in both by default, the owner's "preferred"); left, she sails the new board on the bad hand until ordered to shift it. The polacre the same with her square main | GA §4; Dec 3; Eng §2.3, §2.4 |
| 4 | The tartane | Forfait's *Humble*; her main raked 3° forward; the tréou carried (her headsails by judgement, as decision 11 leaves them: one jib) | Tar §2, §3; Tar-D §16.1 |
| 5 | The xebec's size, and the chambequín | The small class on *Minorca*'s hull; the chambequín booked | Xeb §2.4, §3.6; Xeb-D §18.1 |
| 6 | The xebec's sweeps | Now, as a fit: sixteen sweeps of three men taken from her company, and she stays a ship | Xeb §4; Xeb-D §6; Eng §5 |
| 7 | The *Diana*'s guns when taken | The owner's three fits kept, and a fourth, "Danish 1807", added from her own papers | Dia §4, §8; Dia-D §17.1 |
| 8 | The three-decker | Two fits on one rebuilt hull, 1797 as the default; about 100 of her 839 as soldiers so that every gun is manned (interim, until Winfield's dotación is read); size rank 5 | Con §3, §4; Con-D §17 |
| 9 | A foreign gun's pounds | As her navy named it (`pounder: 36`), with Winfield's pairs in the note as the book gives them | VR-Sp "Units"; Con §3.3; Dia-D §17.1 |
| 10 | The sources | Hold PB-039; the three-decker's hull from her sister's lines as rebuilt (ZAZ0101 to ZAZ0103, read under the standing Greenwich rule); hold the *Diana*'s 1809 drawing once a museum image with its terms is found and vetted; the Danish draught not sought now | Con §11; Dia §9 |

**Taken as recommended unless the owner says otherwise:** Dec, Part E, a short list with pointers.
It includes:
- no scenario in this card;
- a tiller's words for every tiller-steered hull;
- the obús carried as a carronade;
- the polacre in two files, the trader's and the polacre of war's.

**The answers:** recorded in Dec's Part F (2026-11-18). Winfield's passages (Dec, Part D) are
the owner's to look up; none has come yet. Part E stands as recommended, no word having been given
against it.

---

## 1. What the preliminaries hold

### 1.1 The documents (the first round and the second, done)

| Hull | Research note | Design (second draft) | Her lines, by rung | Her probe today (measured) | Not reached |
|---|---|---|---|---|---|
| Tartane | Tar: Forfait 1788 Table II (p. 134, page image) names two tartanes. The *Humble* (100 tonneaux, 20.38 × 6.61 m, topsail and mizen) is the owner's rig almost exactly. Lescallier, Röding, Steel and Falconer agree on the rig. A heritage inventory of late small craft has the yard changed by a wear "when the weather allows" and long boards on the bad hand avoided (secondary; GA §2.4) | Tar-D: one module, two files (the trader, and the coastguard); her topsail on a pole main, so A5 and A6 before her file | S† once Chapman Pl. LVIII No. 16 is read at step 1; T until then, to read: the plate | Classes as the cutter. Tacks in 89 s with nothing done to either lateen. Wears in 487 s without shifting them. Forereaches hove to at 3.1 kn. `dip` refused. With her topsail on her pole main's head, as her file has it, the topsail is a course and is hauled up hove to | Chapman's plate at a readable size; Monleón's print; the prize papers |
| Polacre | Pol: Steel 1794's two polacre-settees; Forfait's rule for pole masts; O'Scanlan 1831; James's eight armed polacres, among them the Spanish navy's *San Josef* of 1800 | Pol-D: item 8 settled (§5); two files (the trader, and the polacre of war) | T: no polacre's lines or dimensions found; her size waits on Winfield's rows | On a pole main the topsail and topgallant are "courses" to the engine at twelve places. Her lateen mizen hove to is kept drawing: 58.5° off at 1.65 kn by truth 12's own measure, 0.05 kn over its 1.6 (her headway 1.49 kn), her lever the fore lateen's trim. Taken in, she does not heave to at all | Winfield's polacras; Monleón's caption |
| Xebec | Xeb: James gives *África* (1799), *Vives* (1806) and a 22-gun xebec at her sweeps (1801). Niles gives the regency's 18 (1815). Forfait's Table IV (the *Caméléon*) gives her spars | Xeb-D: two files (the King's xebec, and a trader); a new corsair book | S† once Greenwich's *Minorca* (ZAZ4270, 29.49 × 9.30 m) is read at step 1; R or T until then | A point nearer the wind than the brig, but better before the wind than the brig: the opposite of the sources. Tacks in 346 s with the lateens flipped free. A ship given boat's oars becomes a boat | Forfait's Table IV on the page image; *Minorca* measured; Chapman's xebec |
| *Diana* | Dia: her held Spanish plan read to scale. Its table gives Winfield's row and her displacement, 497.2 t. Roos 1957 (rung B) gives her Danish arms and her captain's report | Dia-D: one file; four fits | S: her own plan, rung A | Sails, tacks, wears and heaves to as the frigate does, given GM 1.5. One tack, from 295°, is 164 s, under truth 10's band | Steel's 20-gun column; the Danish draught |
| *Concepción* | Con: her own plan PB-039 (CC BY 4.0), three tiers of 15, 16 and 16 ports; her sister's lines at Greenwich (ZAZ0101); James's *San Josef* as taken | Con-D: one file; two fits | S once ZAZ0101 is read and measured; PB-039 (read on screen) her stand-in, S†, meanwhile | The engine takes a third deck almost everywhere (Eng §6). She tacks quicker than the 74 (181 to 188 s against 237 to 258 s). In truth 7-196's world three of her probe crewed run 72 to 75 ticks a second against three 74s' 79 to 81 (Eng §7) | Her masting, the breakdown of her 839, her gun weights, draught and sill; ZAZ0100 to ZAZ0103 not viewed |

**The engine note**, Eng:
- item 37 measured both ways, on both tiers, through a read redirect in scratch (§1);
- the lateens (§2) and the tartane's topsail (§3);
- the pole mast, cross-referred to Pol-D (§4);
- sweeps (§5), three decks (§6) and the pace (§7);
- the regency's role (§8), the harbour's shelves (§9) and the wheel (§10);
- package 81's checklist (§11);
- **the steps A0 to A9 and V1 to V4 as one design, for the lead's approval before stage 0L (§14)**.

**The lead's two items:**
- **Item 8** is settled in Pol-D §5 by measurement: the pole read from the parts, with no key; the
  lateen mizen kept set hove to, the driver rule never reaching it (with it she forereaches 0.05 kn
  past truth 12's speed, her lever named; without it she does not heave to); a whole lateen worked
  by nothing in stays; B3.4's limits reaching neither her nor any rig of the package. The first
  file with a pole main is the tartane's (Tar-D §5.1a), so A5 and A6 come before it.
- **Item 37** is reported in Eng §1. It is not changed.

### 1.2 Not reached, and wanted before or at the build's step 1

- **Page images and plates, public domain.** None is held in the tree; each is read outside it, as
  package 75's were (`D:/Projects/FreeSail/reference-cache/`, never committed):
  - Chapman's Pl. LVIII No. 16 and Pl. LXII (the tartane);
  - Forfait's Table IV (p. 136) and Forfait's figs. 9, 35, 37 and 38;
  - Lescallier tome II, Pl. XXII fig. 5, Pl. XXI fig. 3 and Pl. XX fig. 1;
  - Röding's figures;
  - Willaumez's CHEBEC and MUDER, and O'Scanlan 1831's JABEQUE, CAPA, POLACRA, TARTANA and MUDER;
  - Steel 1794's 20-gun column and Steel's p. 39 fractions.
- **Greenwich's free 1280-px images**, read and cited by object number and never copied:
  - *Minorca*, ZAZ4270;
  - ZAZ0100 to ZAZ0103, the *San Josef*, under the same rule; the owner chooses whether the
    three-decker's hull is drawn from them (Dec 10).
- **Winfield's passages**, sourced by the owner and asked by title and class (Dec, Part D).
- **The National Archives' prize papers (HCA 32)**, for the tonnage, guns and men of tartanes and
  polacres. Duhamel du Monceau's fishing tartane.

**Where the measuring is done.** A cloud session cannot read `D:/Projects/FreeSail/owner-notes/` or
the image cache. So each hull's measuring tasks are done here (§9.2). Where the source is free,
this can happen during the preliminaries, since it is research and is filed as documents. The
figures go into a measuring note per sheet in `docs/design/ships-design/` (`pages-<sheet>.md`, the
form of the existing `pages-zaz4491.md`) and into the hull's second draft. No image goes into the
tree.

---

## 2. The rules since 15 November, and what they ask of this plan

1. **A one-page scope card agreed with the owner before any building** (§14). This plan and its
   six documents are the card's input. The card's scope is what is built, and it does not grow.
2. **One building package at a time.**
   - Package 90's build is one package. Its stage 0, its engine steps and its five hulls run under
     one card, in parallel sessions inside it.
   - While it runs, nothing else of the ships session builds. The session's list of 79 waits for
     its own cards. The lead has given 21 of its items to other packages' roads.
3. **The owner's gate of milestone 7 before new building, unless the owner says otherwise** (Dec
   1). The pick is to build after the gate. Phase 2's documents and Phase 3's passages fill the
   time until then, so the build can begin the day the gate closes.
4. **How a package runs, as amended on 2026-11-16:**
   - **A few passes are fine.** Each pass is one gathered list. If a step is not converging after a
     few passes, it comes to the owner.
   - **The lead gates the hash a builder has reported, never one that was merely pushed.** This
     session reports a hash only once the builder's own gate on it has finished.
   - **Each reader is told which standard to hold** (§9.2):
     - for a hull, her sources and the ladder;
     - for an engine step, that no committed ship sails otherwise than the card names.

     A reasonable stop for any reader: no new sources beyond the routes named, and the owner's
     answers are not reopened.
   - **Each builder runs the fast tier whole within its container's limit of hours**, never a
     limit it set itself. Each brief says what the limit is.
5. **Every mend is made at its cause.** The cause is named and mended where it lives, it is looked
   for elsewhere, and the test is at that level. This rule turns three faults the package meets
   into mends for every ship with the same cause, not just for package 90's hulls:
   - **A2: the words of a rig with no yards.** Every wear says "brace in the after yards", and
     every tack says "braced up", whatever the rig.
   - **A3: a tiller's words.** Every tiller-steered hull is told its wheel is shot away and is
     repaired with new wheel-ropes.
   - **A5: a yard's level read from its spar's class.** Today it makes the smack's topsail a
     course.

   The card names all three, with what each moves. A reader of a mended hash is asked whether each
   mend is the cause's or only the symptom's.
6. **The standing rules** (What binds, item 6). Two more are specific to this package:
   - a cloud session is given page-cited facts only, never a book's text;
   - an image enters the tree only with its licence vetted (public domain or CC BY), its artist,
     date and namesake vetted, and its README row, on the owner's word (Dec 10).

---

## 3. The phases

Each phase is its own piece of work, so that the lead, and where needed the owner, can read each
result before the next begins.

### Phase 1: research (done)

Five research notes, five first drafts and the engine note (§1). They were written by parallel
agents with no test suite, and their probes ran in scratch. This plan is the synthesis.

### Phase 2: critics and second drafts (documents only, before the report: done 2026-11-18 but for the measuring)

| Piece | What | Standard the reader holds |
|---|---|---|
| A critic per document (six: the five designs and the engine note), as one piece of work in parallel, with no test runs. **Done**: one reading of the six, this plan and the decisions sheet, 25 findings, two probes re-run | It reads the draft against its research note, this plan and the sources it cites. It lists: what is unsourced or mis-marked; what the engine would not do as the draft says (re-run where the draft's probe allows); what this plan's settlements (§4) change; what the second draft must settle (§8's lists) | Fidelity to the sources and the ladder. Buildability against what was measured. Agreement with this plan. A reasonable stop: no new research beyond the routes of §1.2, and no picks reopened that are the owner's |
| A second draft per document | It answers the critic item by item. It takes §4's settlements, cites §6's step names in place of its own, and keeps the owner's questions as Dec puts them. The engine note's second draft becomes the design of A1 to A9 for the lead's approval before stage 0L, as Ext was before 0E. **Done**: each design says so at its head, with its table of the findings it answers; the engine note's §14 is the steps' design | — |
| The measuring of the free sources (§1.2), here | Chapman's plates, Forfait's tables, *Minorca*, Steel's column: the figures marked in a measuring note per sheet | The sheet's own scale checked against its stated dimensions (the package 75 rule). **Not done in this round**: it stays each hull's step 1, here (§8.0), or a short piece of work before the report if the lead wants it first |
| This plan's second version | It is revised on the critics' findings and the second drafts. Its §4 and §13 are brought up to date. **This version** | — |
| The report to the lead | The branch and its documents, and Dec's ten questions with the passages. The session's stopping point (nudge 15) | — |

### Phase 3: the owner's round (human)

- The lead puts Dec and the card to the owner, and the owner sources Winfield's passages.
- The answers are recorded verbatim in Dec, in §0 and in each design's open section.
- The second drafts are then amended inline with the answers and the passages, by hand, not as a
  separate workflow. This is small work, and reshaping work already written needs no workflow (the
  session's practice).
- A passage that changes a hull's size or company moves her draft's figures. Each moved figure is
  recorded old beside new, with the passage cited by page.

### Phase 4: the build (under the card)

Stage 0 here (§5), then the two roads in cloud sessions (§9). Every step is merged into the
package's branch here, and every reported hash is gated by the lead. There are five stopping
points, where the owner can try what has landed (§9.1).

### Phase 5: the close

The integrator, which is this session:
- moves the truths into `tests/test_known_truths.py` by number;
- updates `SLOW_TESTS` in `tests/conftest.py`;
- writes `docs/dev/TuningNotes.md`'s sections for the package, the specification as built, and
  the primer's vessel pages;
- adds the images README's rows, on the owner's word.

A whole-change reading then follows, with the same lenses as `Build-Ships.md` §17 plus one more
(§10.2). The close is one final report to the lead, with the leftovers listed.

---

## 4. Where the drafts disagree, and how this plan settles it

| # | Question | The drafts | Settled here, or for whom | Second draft to change |
|---|---|---|---|---|
| 1 | How a lateen ship goes about | Tar-D, Xeb-D and Eng: worn, not tacked. Pol-D: the polacre tacks and wears, her lateens changed in both (JUDGEMENT: no source read says she could not; Willaumez's text describes a square-rigged polacre, with no lateens, tacking, the plate not viewed) | **Settled by the owner, 2026-11-18 (Dec 3), in their own shape:** every lateen rig tacks and wears as other vessels do, each an ordered evolution; changing the yard is a part of either, done or left. **Plainly:** the second version's "one rule, keyed on the main sail" (a whole-lateen main worn only) is dropped; it came from the brief, not a source (GA §4) | Tar-D, Xeb-D and Pol-D, their going about (third drafts, done) |
| 2 | What `tack ship` does on a lateen main | Tar-D and Xeb-D: answered in words naming the wear. Eng: answered in words, or turned into a wear | **She tacks** (Dec 3, the owner's answer). `tack ship` is never turned into a wear. `put her about` (package 45's road, `data/vocabulary.yaml` l. 238-243) gains one reason to wear: a whole lateen set and the wind over the book's `lateen_tack_kn` (22 kn, Forfait p. 119; JUDGEMENT on the figure), said (A1c; Eng §2.3 item 6). **Plainly:** the second version's "answered in her words, and nothing done" is dropped | Tar-D §5.4 item 3; Xeb-D §5 (done) |
| 3 | The machinery for changing a lateen | Eng and Xeb-D: `dipping` widened to the lateen, the dip's machinery keyed on `dipping` and not on class `lug`. Pol-D: the settee's change machinery | **Proposed: one key, the change as a part of the tack and the wear, and one new evolution for the change by itself.** `dipping` is allowed on a whole lateen, and with it the side state (`lug_side`) and `against_the_mast` (A1a). In the tack and the wear the change runs as the settee's `SetteeChange` does, the yard peaked up and passed round, never lowered: in stays once her head is through the wind, in the wear at "wind aft", by the order's clause or the ship's practice (A1b). By itself it is `change_lateen`, its scripts on the settee's B3.3 model. Which side of the mast the car passes is not agreed (abaft by Willaumez, forward by O'Scanlan; GA §3.3). The lugger's and the settee's paths stay keyed as they are. **The lead rules this** at A1's design (§13.1; Eng §14) | Pol-D §5.3; Xeb-D §5; Tar-D §5.4 item 2; Eng §2.3 items 1-3 (done) |
| 4 | The lateen mizen | Tar-D and Eng: read by the driver's paths. Pol-D (measured): the heave-to's driver rule must not reach it. Taken in hove to, the polacre falls off and the heave-to fails at 600 s | **Worked as a ship's mizen in going about, and kept set hove to.** Hauled aft at helm's a-lee, and as she comes to in the wear; eased at "up helm"; **eased as she pays off on the new board where she has no head sail set** (third draft, measured on the bare xebec: 192 m lost to windward against 1,064, Eng §2.2a). `after_gaff_sails` never takes a whole lateen, and a guard over every file holds it. Each hull's heave-to is measured on her own file against truth 12's band, by its own `knots()`. With the mizen set the polacre probe forereaches 0.05 kn past the band's speed (1.65 kn); her lever is the fore lateen's sheet or trim. If the tartane forereaches past the band, the lever is her great lateen's trim, not the mizen | Tar-D §5.3, §5.4 item 4; Eng §2.3 item 5; Pol-D §5.2 (done) |
| 5 | The pole mast | Pol-D and Eng agree: no key; the pole read from the parts as filed; the furlers on the yard below | **Settled** (A5, A6) | none |
| 6 | Step numbers | Pol-D E1 to E4, Xeb-D E1 to E10 and Tar-D §5.4's items each number differently | **This plan's names (§6) replace them.** The second drafts cite A0 to A9, V1 to V4 and N1 to N3 | all three (done) |
| 7 | When the lateen row is tuned | Pol-D: once, on the tartane's file. Xeb-D: once, on all three hulls' truths together | **Once, at A8, before the xebec's merge, on the truths of the lateen hulls on the branch at that time**: the tartane and the xebec, and the polacre if her Winfield rows have come. A hull that lands after A8 (the polacre, if her rows are late) has her figures measured against the tuned row, old beside new; the row is re-tuned for her only if her truths fail, the lead's to rule. So nothing of the xebec waits on the polacre's rows. The tartane's "a point nearer the wind" passes on the untuned row today (measured on the probe), so she need not wait for A8 | Pol-D §16 item 2; Xeb-D §5, §17 item 4 (done) |
| 8 | A foreign gun's pounds | Dia-D: the nominal pounder. Con-D: English pounds, by Winfield's broadside ratio applied per calibre. Xeb-D: one rule asked for | **The owner's** (Dec 9). The pick is the nominal pounder, with Winfield's pairs in the note as the book gives them. That is the reading that never re-derives the book's ratio, which the lead's rule forbids. If the owner takes the pick, Con-D's decision 9 and its §5.3 table change | Con-D §5.3 |
| 9 | Spanish names | Dia-D, Con-D, Pol-D and Xeb-D each want a `spanish` list | **One shared step, N1**, before the first Spanish people file, keyed on the new people files. Spain's nation row (`names: english`) is unchanged, so no passage with a Spanish ship moves | all four |
| 10 | The obús | Con-D and Dia-D: carried as a carronade by judgement. Eng: the owner's | **Carried as a carronade of its calibre**, with the word "obús" in its words and its note. A kind of its own, with shells, is booked for a gunnery package. This is taken as recommended (Dec, Part E) | none |
| 11 | The helm | Tar-D: a tiller. Xeb-D: a wheel by judgement. Dia-D and Con-D: a wheel. Eng: the helm read from the file | **A hull key `helm: wheel or tiller`** (A3), the words a tiller's, for every tiller-steered hull, under the owner's rule on mends | Tar-D §5.4 item 9 |
| 12 | One company per file | Tar-D and Xeb-D: second files (the coastguard tartane, the merchant xebec). Pol-D's first draft: one file of 16 for fits of 16, 71 and 80 | **Settled:** one class in two roles (`Build-Ships.md` §5.0, principle 10; the lead's ruling (5) of 2026-11-07, that a company belongs to a file, not to a fit): the polacre too, the trader's file (16) and the polacre of war's (71, the corsair's 80 a departure recorded, as the xebec's regency 150 is) | Pol-D decisions 1, 11, 12; §6.1; §7.2; §9 (done) |
| 13 | The xebec's heave-to | Xeb-D: she carries no headsail, so the order is refused in her words until a source is found. Eng's probe kept the brig's headsails | **Xeb-D's.** A lying-to under lateens alone is booked until a source is found (O'Scanlan's CAPA; Bonnefoux and Pâris's CAPE). Both probes are recorded | none |
| 14 | A first rate's rank, and her soldiers | Con-D: rank 5, and 100 soldiers so that every gun is manned. Eng: the owner's | **The owner's** (Dec 8) | — |
| 15 | Scenarios | Tar-D and Con-D give shelf lines and a first scenario. Dia-D gives two. Xeb-D gives hers | **None in this card.** Each ship is offered from the harbour for a bare start, with her fits listed. Each hull's scenarios come in a card of their own after `data/nations.yaml` holds dated wars. Today it holds one year's wars: no war of Britain with Denmark, and nothing for 1808 to 1810 (Dia-D §18 item 4; Con-D §11). Taken as recommended (Dec, Part E) | the scenario sections become "booked" |
| 16 | Truth numbers | T-1 to T-9, P1 to P6, X1 to X9, A to F, 7-NNN-a to e | **Numbered by the lead at the card**, after the last truth at that time (7-635 at 68e769ef) (§10.3) | all five |
| 17 | B3.4's two limits | Pol-D handed them to the xebec's document; Xeb and Xeb-D handed them back and called the chebec's classing the first limit | **Settled:** neither limit reaches the polacre, the chebec (her main the foremost mast with braced yards) or the chambequín (a ship). The limits stay with a schooner's main, recorded; no remedy is built. Stated once in Pol-D §5.4 | Pol-D §5.4; Xeb §9 item 9; Xeb-D §4.3 (done) |
| 18 | The first file with a pole main | Pol-D: the polacre. Tar-D files her topsail yard on her pole main's head | **The tartane.** A5 and A6 come before her file (§6, §9.1); her heave-to is read after A5 | Tar-D §5.1a; Pol-D §5.4; Eng §3 (done) |
| 19 | Whose question: the tartane's headsails and her main's rake | Tar-D's first draft: the headsails to the owner, the rake to the lead | **The headsails by judgement**, as decision 11 says: one jib, the images README's reading of two recorded. **The rake to the owner** (Dec 4): their word "raking" against their watercolour's near-upright main | Tar-D §16; Tar §9, §11 (done) |
| 20 | The Greenwich sheets | Con-D asked the owner's word to view ZAZ0100 to ZAZ0103; this plan read *Minorca*'s ZAZ4270 on the same rule without asking | **Both are read under the standing rule** (cited by object number, never copied). What is the owner's is the three-decker's hull: her sister's lines as rebuilt (ZAZ0101) or her own plan as built (PB-039). *Minorca* is the xebec's only plan, so no choice arises for her (Dec 10) | Con-D §17 question 2; Con §11 (done) |

---

## 5. Stage 0

### 5.1 Stage 0 (one commit, behaviour-free: the card's first step)

Every item below is inert: no file, scenario or path uses it until a builder does. The stage-0
agent works here, after the trunk has been merged in.

**The generator**

1. **The modules.**
   - `SHIP_MODULES` (`tools/gen_ships.py:10399`) gains `"tartane"`, `"polacre"`, `"xebec"`,
     `"diana"` and `"concepcion"`, in that order, after the four.
   - Five stubs `tools/ships/<name>.py`, each `def build(out_dir: str) -> None` that writes
     nothing, with a docstring naming its design.
   - A stub `tools/ships/lateen.py`: a docstring only, saying that it is the whole lateen's cut,
     pure, and that the tartane's builder fills it.
   - **A pin moves:** `MODULE_FILES` in `tests/test_profile.py:502-507` gains the five rows, each
     `[]` (the bilander's precedent), and the hook test's name and docstring say nine modules. It
     is recorded old beside new.
2. **`tools/ships/period.py`** gains the package's units as constants, importing nothing:
   - the pie de Burgos, 0.2786 m (the tree's value from package 39d);
   - Forfait's pied du roi, 0.3248 m;
   - a comment naming Winfield's metres as the game's figures for the book's rows (VR-Sp, "Units").

**The ship's schema** (`freesail/ship/schema.py`, which belongs to the stage-0 agent for the whole
package, as in package 75). Each key below is parsed, refused where it is wrong, and carried by no
file.

3. **`sweeps:`**, a top-level section: `number`, `men_each`, `thrust_n`, `power_w`, `tiring_h`
   (Xeb-D §6's sketch).
   - It is refused on a hull that has `oars:`, and refused with a boat's rig.
   - `ShipSpec.sweeps` defaults to None.
   - A fit's `sweeps:` (a number, or none) is parsed in `armament.fits` and refused where the file
     has no `sweeps:` section.
4. **A boat's `towed`** (`BOAT_KEYS`), a bool defaulting to false. Today it is refused at load
   (Eng §3; no test pins that refusal: to be grepped at the commit).
5. **The hull's `helm`**: `wheel` or `tiller`, defaulting to `wheel`, and read by nothing yet.

**The keyed registries** (`freesail/world/`): inert until a description names them. A grep proves
that no text the game gives a sail holds the new words, as `Build-Ships.md` §3.1 item 24 did.

6. **`SIZE_RANK` and `_SIZE_WORDS`** (`world/captains.py:296-359`):
   - `"tartane": 1`, `"polacre": 2`, `"xebec": 2`, `"corvette": 2`, and `"three-decker"` at the
     rank the owner answers (Dec 8: 5 or 4);
   - the words `("three-decker", …)`, `("first rate", …)`, `("corvette", 2)`, `("ship-sloop", 2)`,
     `("ship sloop", 2)`, `("xebec", 2)`, `("polacre", 2)` and `("tartane", 1)`, each placed before
     any row that matches inside it (`"a ship"`, `"ship of the line"`, `"brig"`).

   A test over the rows proves that every existing description ranks as before.
7. **The men-of-war sets** (`world/regimes.py:197`, `world/squadrons.py:474` and `:1577`) gain
   `"corvette"`, `"three-decker"` and `"xebec"`. `role_of_vessel` (`world/brains.py:245`) takes the
   three as King's ships. The hail words (`orders/signals.py:277`) gain "corvette", "xebec" and
   "three-decker".
8. **Each hull's `DESCRIPTIONS` row lands with her file, from her builder**, not here.
   (`Build-Ships.md` decision 15: a row names a file, and the harbour offers every row.)

**The tests**

9. **`tests/rig_fixtures.py`** gains `xebec_probe()` and `three_decker_probe()`, as Eng §0 built
   them, for tests to come, without touching the lead's two probes.
10. **`tests/test_probes_90.py`** (new):
    - the four probes' classing, measured at this head;
    - no committed file carries `sweeps:`, a towed boat, `helm: tiller`, or a whole lateen with
      `dipping`;
    - each new key's refusals;
    - the five stubs write nothing;
    - every description's rank is unchanged.

### 5.2 Stage 0L (the whole lateen's interfaces, after the lead approves A1's design)

This mirrors package 75's stage 0E. It is laid so that the three lateen hulls' builders can write
their files with the key while A1's behaviour is built (the bilander's file was generated before
B3.3 in the same way).

- **The schema:** `dipping` allowed on a whole lateen (class `lateen` with no `cut_at_mast`). The
  refusal at `schema.py:2363-2364` is narrowed. Its sentence is pinned by no test (grepped: the
  schema alone).
- **The runtime:** `Sail.lug_side` kept for a dipping lateen, a plain class default. The ship's
  practice for the yard, `ship.extra["lateen_practice"]`, is read with its default ("shift" in
  stays and in wearing) and set by nothing. The change evolution's data file is laid with its
  `applies` empty. **Plainly:** the second version's `Ship.wears_only()` is not laid; the owner's
  answer to Dec 3 has every lateen rig tack (A1a to A1d, §6).
- **Guards** in `tests/test_probes_90.py`: no committed file carries the key; each probe with the
  key loads and classes as without it; the refusals for a lateen cut at the mast and for a lug are
  unchanged.

### 5.3 The checks of each stage-0 commit

By an agent that did not write it, here:
- the eighteen files byte-identical, by the two-way byte test;
- the golden classing table, and `tests/test_schooner_mast.py`'s two probes;
- `tests/test_probes_90.py`;
- the fast tier whole once, at stage 0 only, with `--junitxml`. This is **the base** for every
  later step's comparison (the session's rule that tests run once);
- the diff read for any reach beyond §5.1 or §5.2: no behaviour, no pin but the hook test's
  table, no `world.ship` or `CrewedWorld` read beyond the names the Hull keeps, no model or maker
  named.

---

## 6. The engine's steps

Each step has two parts:
- an inert part, laid in §5.1 or §5.2;
- its behaviour, keyed on what no committed file carries, except where named.

Each step is merged alone and measured, old beside new.

| Step | What | Keyed on | Expected to move (to be measured at the ground report) | Before | Owner | The drafts' names |
|---|---|---|---|---|---|---|
| **A0** | Item 37: the generator's peaks read from the engine's curves, rounded to two places; a test holding the two together; the sprit class gaining 1.20 | the generator | 74 `rating_kn` figures in 9 files, regenerated: the studding-sail booms and four ringtail booms. Truth 35's last clause. `test_studding`'s frigate brought up to six points. Five records of "no figure moved" naming the booms. Seven byte pins passing again by the regeneration. Truths 9 and 14 hold (Eng §1.3-§1.4). Only under Dec 2 (a) | any new file being generated | engine track | Eng §1.5 |
| **A1a** | The whole lateen's side and the bad hand: `dipping` on a whole lateen, `lug_side` and `against_the_mast` (the lug's two-thirds, JUDGEMENT; measured 4 to 17 per cent of her speed close-hauled on the probes, Eng §2.2a); `shift the mainsail` by itself (`change` and `dip` its synonyms for a lateen), refused on the good hand, held in a manoeuvre, kept apart from the sail room's "shift … for …", its evolution `change_lateen` (peaked, never lowered; its seconds and hands by the yard's length, JUDGEMENT: Eng §2.4.4); the stern watch's line for a lateen left on the mast; `set_lateen`, `take_in_lateen`, `furl_lateen` and `reef_lateen` sized by the ship's data or `too_few: all hands`; the lateen mizen kept set hove to; the heave-to refused, for a rig with neither head sail nor braced yard, in the xebec's words | `dipping` on a whole lateen | Nothing of the eighteen files (none carries a whole lateen; the 64's and the 74's mizen courses are `cut_at_mast`). The library's count of evolutions by `change_lateen` (`tests/test_agents.py`); the vocabulary's order lists by `shift` for a lateen. The probes' tests are unchanged as filed | the three lateen hulls' files on the branch | engine track | Tar-D §5.4 items 1, 5, 7; Pol-D A1 (its E3); Xeb-D A1 (its E1, E3); Eng §2.3 items 1, 3, 5, 8, §14 |
| **A1b** | Going about with the yard's change a part (the owner's answer to Dec 3): the tack and the wear (and the box-haul and the fill away, as for a settee) change each whole lateen as the settee's `SetteeChange` does, the yard peaked and not lowered, in stays once her head is through the wind, in the wear at "wind aft"; which yards, by the order's clause ("and shift the lateens", "and leave the lateens") or the ship's practice ("shift" in both by default; set by "in stays, leave the lateens" and its kin; shown in the readings); the clause a new modifier kind in `orders/grammar.py`, its words loaded by `orders/vocabulary.py`, and the practice's orders a new verb named in the primer; a lateen left on the bad hand until shifted; the change's seconds in its own file (`tack.yaml`'s and `wear.yaml`'s timings untouched); her words name the lateens; the aftermost lateen hauled aft at helm's a-lee and eased as she pays off where she has no head sail; a foremost lateen before a square main eased with the head sheets and drawn at "let go and haul" | `dipping` on a whole lateen | Nothing of the eighteen files; the settee's and the lugger's guard sets as they are. The vocabulary's order lists (the clause, the practice's orders). The primer's going-about chapter naming the practice's new verb and its reading, so that `tests/test_grammar_book.py`'s two primer tests pass again. No checkpoint name (`lateen_practice` is a plain dict of strings: Eng §2.3). `tests/test_catalogue.py` unmoved by construction | the three lateen hulls' files on the branch | engine track | Tar-D §5.4 items 2-4; Pol-D §5.3; Xeb-D §5 A1; Eng §2.3 items 2-5, §14 |
| **A1c** | The rules captain and `put her about`: package 45's choice wears where a whole lateen is set and the wind is over `lateen_tack_kn` (22 kn), said, and so does the course's judgement for a course across the wind's eye (`judge_course`, the road of `steer`, `shape a course` and the captains' hourly leg), each tacking her regardless where there is no room to wear; `tack ship` never turned into a wear; the captain's practice from the book: in stays the yards left under `lateen_leave_kn` (12 kn) and shifted above it or after a board of `bad_hand_s` (1,800 s) on the bad hand, shifted in wearing, and shifted after the wind has crossed the stern, as a lug is dipped; the three keys under `thresholds:` with their sources (Forfait p. 119; Stratico BISDOSSO; the 2018 inventory), read with these defaults where a book lacks them (JUDGEMENT on every figure) | a whole lateen set | Nothing of the eighteen files (none sets one). The captains' books' threshold counts, if the lead puts the keys in every book (to grep at the build). The captain's trials and `tests/test_captains.py` as a lens | the tartane's merge | engine track | Eng §2.3 item 6, §14 |
| **A1d** | Taken aback, and the bad hand in a breeze: a whole lateen aback loads its yard and mast by `LATEEN_ABACK_LOAD` (about 3.9 on the engine's sustained load: a great yard rated at the lower spars' 55 kn strains aback from about 28 kn and may carry away from about 34, the yard before the mast), and on the bad hand by `LATEEN_BAD_HAND_LOAD` (about 1.5, the yard strained only in a strong gale, about 45 kn; or none, the other way); `take in` begun on a lateen aback over `lateen_tack_kn` waits till she pays off (Forfait p. 119); the strain model as it is (JUDGEMENT on every figure, measured on each hull's file) | a whole lateen with `dipping` | Nothing of the eighteen files. `tests/test_strain.py` as it is. The hulls' own truths (Tar-D T-6 and T-9) | the tartane's merge | engine track | Eng §2.4.3, §14 |
| **A2** | The words of a rig with no yards: the wear's "brace in the after yards" said only where she has after yards; the tack's "braced up on the … tack" only where she has a braced yard (the cause's mend, for every rig) | the rig as filed | The wear's first line and the tack's last line in the lugger's, the cutter's and the smack's recorded passages: words only, old beside new | with A1a and A1b (the same scripts) | engine track | Eng §2.3 item 9; Xeb-D E10 |
| **A3** | The helm's kind: on `helm: tiller`, the hit says the tiller or its ropes are shot away; the relieving tackles hook to the tiller as now; `repair the wheel` is answered as the tiller's repair (a spare tiller shipped, or new tiller ropes rove), its time and hands by judgement. For every tiller-steered hull | `helm: tiller` | The six files whose notes say tiller, regenerated with the key: the cutter, the lugger, the smack, the two schooners and the hermaphrodite brig (read: `data/ships/*.yaml`). Their "no figure moved" records name the key. Their words where a helm is shot away. Truth 7-626 is the first action's, at seed 6: to be measured, and expected not to move if her ship steers by a wheel | the tartane's file | engine track | Tar-D §5.4 item 9; Eng §10 |
| **A4** | The boat in tow: a towed boat manned from alongside, not hoisted out; words. Its drag is left out as small beside the hull's at her speeds (JUDGEMENT, measured against the trawl's form) | a boat's `towed` | nothing (no file tows a boat) | the tartane's file | engine track | Tar-D §5.4 item 8; Eng §3 |
| **A5** | A yard's level read from its order on its lower mast: one predicate `Ship.yard_level(yard)`, read at the twelve places of Pol-D §5.1 (the cause's mend). A square yard over a whole lateen with no braced yard below it counts the lateen yard as the level below (JUDGEMENT, for the lead: the tartane if her tréou is left out, Tar-D §5.1a) | the parts as filed | The smack: her topsail becomes a topsail, not a course, in the heave-to and lie a-try with it set. No pinned passage is expected to move, since her plain sail sets no topsail (measured, Pol-D §15). A guard over every file's yard levels, old beside new | **the tartane's file** (her topsail on a pole main: Tar-D §5.1a) | engine track | Pol-D A5 (its E1) |
| **A6** | The pole mast's quick handing ("amener en paquet"): the upper square sails of a pole lowered together onto the lower yard, furled and reefed from the yard below; the topmast evolutions refused in words. Times by judgement, for the lead | a lower mast carrying yards above its lowest with no topmast (the smack's, the tartane's and the polacre's mains) | The smack gains it for her topsail (to be measured), and the tartane by the same key | **the tartane's file** | engine track | Pol-D A6 (its E2) |
| **A7** | Sweeps: the thrust by package 82's law (`physics/oars.py`), added in the ship's substep; state saved in `ship.extra["sweeps"]`; `out sweeps`, `in sweeps`, `give way`, `easy all` and `lie on your sweeps` where the hull has sweeps; an evolution manning `number × men_each` from the watch, or all hands; the men at the sweeps taken from the sails and the guns; the far body's pace in a calm (`world/ships.py`'s `VESSEL_MIN_SPEED_KN`, l. 98, read at l. 849 and 865). The boat predicates stay a ship's boat's | `sweeps:` | The library's count of evolutions (`tests/test_agents.py`). The vocabulary's order lists. The checkpoint's names list, by its tool | the xebec's fits with sweeps | engine track | Xeb-D A7 (its E4) and §6; Eng §5 |
| **A8** | The lateen in a gale: the reduction shifts storm canvas set `in_place_of` a whole lateen (the xebec's small lateens, the tartane's bouffette) at the topsails' second reef (Luce p. 476's level), in place of reefing. A whole lateen belongs to no "courses" group. **The lateen row tuned** (`data/sail_classes.yaml`) on the truths of the lateen hulls on the branch at the time (§4 row 7) | storm canvas `in_place_of` a whole lateen; the lateen row, which no committed sail reads (the mizen courses use the gaff's curve) | Nothing committed. The lateen hulls' own figures, re-measured old beside new; a hull landing later measured against the tuned row. `PEAK_COEFF["lateen"]` follows the row by A0 (a) | the xebec's merge | engine track | Tar-D §5.4 item 6; Xeb-D A8 (its E5, E6) |
| **A9** | Three decks: `_shut_crews` and `_rob_order` for a middle deck (`crew/quarters.py:418-435`, `:668-687`); "the second deck" and "the third deck" in `orders/gunnery.py`; "the main deck" refused in words on a three-decker, naming her decks | a `middle` deck | nothing (no file has one) | the *Concepción*'s file | **her builder** | Con-D §5.5, §6.3; Eng §6.3 |
| **V1** | The whole lateen drawn: three corners on its yard, slung at a third on the mast's raked line, on its lee side; peaked up its mast while it is changed; against its mast on the bad hand (`client/projection.js:815-816`, `904`, `1506`, `1537`) | as A1 | the pictures of every committed file unchanged (`tests/test_pictures.py`, `tests/test_view_geometry.py`) | the tartane's testing report | viewer | Pol-D E4; Eng §11 |
| **V2** | The pole mast drawn with no doubling; the upper yards drawn down on the lower while lowered | as A6 | the smack's picture with her topsail lowered, the only move | the tartane's report | viewer | Pol-D §13 |
| **V3** | The towed boat drawn astern | as A4 | none | the tartane's report | viewer | Tar-D §10 |
| **V4** | A port's words by the log's "-deck" form ("a middle-deck port") | the deck words | the 74's and the 64's "a lower port" become "a lower-deck port": words, old beside new | the *Concepción*'s report | viewer | Eng §6.2, §13 item 3 |
| **N1** | A `spanish` list in `data/crew/names.yaml`, from a named source, read by the new people files' `names: spanish` | the people file's key | none (Spain's nation row is unchanged) | the first Spanish people file | the *Diana*'s builder, merged alone first | Dia-D §17.1 q6 |
| **N2** | The regency's cruiser: `corsair` in `ROLES` (`world/captains.py:137-150`) and `data/captains/corsair.yaml` on the privateer's and the cruiser's form. Every key sits under `thresholds:` (package 116's road), and its differences are stated at its head with their sources. The people's fate is package 110's, never the book's. No seat for a player at it, and a model's seat refused in words (Design-SlaveryAndSuppression §8) | role `corsair` | The captain files' counts in the audit. The roles' sets (`corsair` among the armed roles, never in `HAND_PEACEFUL_ROLES`) | the polacre's and the xebec's corsair fits | the *Diana*'s builder, merged alone | Pol-D §12; Xeb-D E9; Eng §8 |
| **N3** | A `spanish` marines kit in `data/marines.yaml` (decision 64; the *África*'s 38 soldiers): musket and drill from a source, or the basic kit's, said so | the fit's marines | none | the xebec's King's fit | the *Diana*'s builder | Xeb-D E8 |

**What this plan does not give the engine** (booked, each in §14's "Does not build"):
- the obús as a kind of its own;
- a lying-to under lateens alone;
- the xebec's square sails for running;
- the sweep ports drawn;
- a season key for the regency's cruisers;
- the nations' dated wars.

**Plainly:** Pol-D proposes A5 (its E1) as "its own small step before any pole-masted file". It
reaches twelve readers. It is taken into the engine track after A1 to A4, because it shares A1's
files, and before the tartane, the package's first pole main (the critic's F3).

---

## 7. File ownership

### 7.1 The owners

| Owner | Owns (edits only these) |
|---|---|
| **The stage-0 agent** (here) | Every file of §5.1 and §5.2, at its commit. `freesail/ship/schema.py` for the whole package: a later need goes back to a stage-0 commit, as in package 75 |
| **The engine track** (one cloud session, one builder at a time) | **Code:** `tools/gen_ships.py` after stage 0 (A0 only); `freesail/ship/parts.py` and `ship/graph.py`; `physics/sails.py` and `physics/integrate.py`; `evolutions/scripts.py`, `runner.py`, `trim.py` and `action_scripts.py`; `orders/verbs.py`, `orders/storm.py`, `orders/boat.py` and a new `orders/sweeps.py`; `combat/hits.py` (A3); `world/boats.py` and `world/movement.py` (A7, only so that the boat predicates stay a boat's); `world/ships.py`'s far-body pace, l. 840-870 (A7, `VESSEL_MIN_SPEED_KN` and its readers); **third draft:** `orders/navigation.py`'s `put_about_choice`, `judge_course`'s eye branch and `watch_the_stern` (A1a, A1c); `orders/grammar.py`'s going-about modifiers and `orders/vocabulary.py`'s table for them (A1b); `physics/strain.py` (A1d); `world/captains.py`'s going about and `_across_the_stern`, for a whole lateen alone (A1c); `api/readings.py`'s row for the ship's practice (A1b) |
| | **Docs:** the primer's going-about chapter, `docs/primer/05-going-about.md`, at A1b, naming the practice's new verb and its reading; and at A7 a passage naming the sweeps' orders, in the chapter the builder names. `tests/test_grammar_book.py` asks every verb and reading to be named in the primer (the sweeps' gap older than the third draft) |
| | **Data:** `data/evolutions/` (the new files and those the steps name); `data/vocabulary.yaml`; the lateen row of `data/sail_classes.yaml` (A8); the three lateen keys in `data/captains/`, in the books the lead names (A1c; §13.1) |
| | **Generated:** the committed files that A0 and A3 move, regenerated by the tool |
| | **Tests:** the new files `tests/test_peak_coeff.py`, `test_lateen_whole.py`, `test_rig_words.py`, `test_helm_kind.py`, `test_boat_towed.py`, `test_yard_level.py`, `test_pole_mast.py`, `test_sweeps.py` and `test_lateen_gale.py`; and the pins its steps move, by name (§10.4) |
| **The viewer** (one cloud session; the screenshots taken here) | `client/projection.js`, `client/shipview.js`, `client/style.css`; `tests/test_view_geometry.py`; `tests/test_pictures.py` only for a threshold that moves; the screenshots, kept outside the repository |
| **The tartane's builder** | `tools/ships/tartane.py`; `tools/ships/lateen.py` (the shared cut, **merged alone first**, before the polacre's and the xebec's rigs are written); `data/ships/tartane.yaml` and `coastguard-tartane.yaml` (generated); their people files; `tests/test_tartane.py`; her row of `MODULE_FILES`; in her window, her `DESCRIPTIONS` rows and words |
| **The polacre's builder** | `tools/ships/polacre.py`; `data/ships/polacre.yaml` and `polacre-of-war.yaml`; their people files; `tests/test_polacre.py`; her rows |
| **The xebec's builder** | `tools/ships/xebec.py`; `data/ships/xebec.yaml` and `merchant-xebec.yaml`; their people files; `tests/test_xebec.py`; her rows |
| **The *Diana*'s builder** | N1 to N3, each merged alone before her file: `data/crew/names.yaml`'s `spanish` list; `ROLES` with `data/captains/corsair.yaml` and the roles' sets in `world/regimes.py` and `world/squadrons.py`; `data/marines.yaml`'s Spanish kit; `tests/test_corsair.py`. Then `tools/ships/diana.py`, `data/ships/corvette-20.yaml`, her people file, `tests/test_diana.py`, and her rows |
| **The *Concepción*'s builder** | A9 (`crew/quarters.py`'s two readers, `orders/gunnery.py`'s deck words, `tests/test_three_decks.py`); `tools/ships/concepcion.py`; `data/ships/three-decker.yaml`; her people file; `tests/test_concepcion.py`; her rows |
| **The integrator** (this session) | The merges into the package's branch; the trunk's fetch and merge at each boundary; a file regenerated at a merge, with the reason; Phase 5 (§3) |

**Nobody touches**, after stage 0:
- `core/world.py`, `core/replay.py`, `world/hulls.py`;
- `world/scenarios.py`, `data/scenarios/` and `client/harbour-shelves.yaml` (no scenario in this
  card);
- `data/nations.yaml`;
- the consent files, the books, `BUILD_NAME`;
- any existing ship file, except through the generator, by A0 and A3.

**Plainly:** N2 is no part of the *Diana*'s own work. It is given to her builder because the
ship-rigged road starts first and is the lightest, so the corsair's book is on the branch before
the polacre's and the xebec's fits need it (Dia-D §0 offers her as the hull on which the package's
shared rules are settled first).

### 7.2 Files that pass, and when

A file passes from one owner to the next only at a merge into the package's branch, never while
two owners are open on it.
- **`freesail/world/ships.py`.**
  - Stage 0 holds the keyed rows.
  - The engine track holds its far-body pace (l. 840-870) for A7, at its merge.
  - Each hull's builder then appends her `DESCRIPTIONS` row and words, under a comment naming her,
    in the order of §9.1.
  - The integrator resolves the row-level conflicts at the merge. The rows are independent, and
    the descriptions' tests read the whole table.
- **`freesail/world/captains.py`.** Stage 0 has `SIZE_RANK` and the words. Then the *Diana*'s
  builder takes `ROLES` for N2.
- **`world/regimes.py` and `world/squadrons.py`.** Stage 0, then the *Diana*'s builder for N2.
- **`tools/ships/lateen.py`.** It begins as stage 0's stub. The tartane's builder fills it and
  merges it alone. After that, the integrator holds it, and an extension of it is a small commit
  of its own.
- **`tools/ships/period.py`.** Stage 0 writes it. After that, a hull's builder appends only her own
  constants, at her merge.
- **`crew/quarters.py` and `orders/gunnery.py`.** The *Concepción*'s builder holds them (A9), and
  no other step touches them.
- **`orders/boat.py`.** The engine track holds it (A4, A7).

### 7.3 What every builder runs at the end of a step

At the end of every step, from the tree root:
- `py tools/gen_ships.py <scratch>`;
- a `cmp` of every committed file not meant to change;
- `load_ship` on each new file;
- `tools/check_viewer_guns.py` on each new file.

At the end of the builder's work:
- the fast tier whole on its final tree once, with `--junitxml`, compared test by test with the
  base;
- the slow tier of the files it touched;
- after a mend, only the mended test's file, then the fast tier with its junit (the session's rule
  that tests run once).

---

## 8. The hulls

### 8.0 Every hull's road

| Step | What | Where |
|---|---|---|
| 0 | Her window opens: her branch is cut from the package's branch at the merge that carries her dependencies (§9.1), and her stage-0 rows are read | the cloud |
| 1 | Her measuring tasks: the figures in a measuring note (`docs/design/ships-design/pages-<sheet>.md`) and in her second draft | **here**, from images that stay outside the tree (§1.2) |
| 2 | Her module: particulars as data in their sources' units, converted once; hull blocks, profile and shape keys (`Build-Ships.md` §5.0-§5.3, the pair check); masts, yards and sails mast by mast; the generator's checks raising `ValueError` with a sentence | the cloud |
| 3 | Her guns and ports by package 81's checklist (`check_viewer_guns` clean); fits, magazine and bill; her company, watches and people file; package 116's evolutions met (`let_go_anchor`'s `too_few: all hands`, the relieving tackles, `repair the wheel` or the tiller's); ground tackle, boats, pumps, hold and stores; her `DESCRIPTIONS` row and words by the made-out rule | the cloud |
| 4 | Her tests and her truths, drafted in her own test file; her polar measured and recorded; her handling against her truths | the cloud |
| 5 | The fast tier whole and the slow tier of her files (§7.3); the review lenses (§10.2), and one fixer | the cloud |
| 6 | Her testing report (below) on her branch as text. The branch checked here (§9.2), merged into the package's branch and pushed. The hash reported to the lead | here |

**The testing report**, the owner's form of 2026-10-29 (the bilander's §13.1):
- **The basics:**
  - her particulars against their sources, each clause with its figure, band and source;
  - her polar beside her comparator's;
  - her tack, wear and heave-to at seed 7, with the ticks of each part;
  - the work that is particular to her;
  - her drawn depth and displacement beside the filed ones;
  - what was taken as judgement, in a list.
- **Pictures**, at 800 × 600 in the built-in pane and at 960 × 720 for the sheets:
  - abeam to leeward, on the quarter, ahead and astern, furled and under plain sail;
  - her own states;
  - beside her comparator at one scale, and her hull alone beside her comparator's, with her rung
    letters under it;
  - heeled 10°, seen from windward.
- **Her open questions.**

The pictures stay outside the repository.

| Hull | Comparator | Her particular work in the report |
|---|---|---|
| Tartane | the cutter | her tack and her wear, each with her yards shifted and with them left, the time and the ground lost beside the cutter's; the bad hand and `shift the mainsail`; `put her about` in a strong breeze; taken aback in a breeze; hove to; the tréou running; the gale's bouffette; the boat in tow |
| Polacre | the merchant brig | the topsail and topgallant lowered "en paquet"; her tack and her wear with both lateens changed and with them left; hove to with her mizen set |
| Xebec | the brig | her tack and her wear with the three changes, and her mizen eased as she pays off; `out sweeps` in a calm, and the men taken from the guns; the small lateens shifted in a gale; before the wind against the brig |
| *Diana* | the frigate-36 | her captain's case (10 to 11 kn, 2 to 3 points free); her heel against the frigate's; the lee port at 21.8°; her four fits |
| *Concepción* | the seventy-four | beat to quarters by three decks; the robbing; the lee ports by deck; her tack against the 74's; three of her crewed at the pace floor |

### 8.1 The tartane (Tar, Tar-D)

- **Her second draft must settle:**
  - **The main's rake.** "Raking" in decision 11; no text gives an angle; the watercolour's main is
    near upright. 3° forward is provisional. The owner's (Dec 4).
  - **Her topsail on a pole main** (Tar-D §5.1a): A5 and A6 before her file, and A5's reading of
    her topsail if the tréou's yard is left out (the lead's).
  - **Her heave-to's lever** (§4 row 4), with the measure to be made on her file.
  - **Chapman's Pl. LVIII No. 16** read at a readable size and her scaling factor (step 1, here).
  - **Her company of ten**, and the coastguard's 34. Both are JUDGEMENT until Winfield's tartanas
    are read.
  - **The bouffette and the tréou's yard.**
  - **The fisherman.** She is a fit with its description booked: it wants a Gulf of Lion
    fishing-grounds file, which is no part of this card.
- **Her files are written** after stage 0L, once `lateen.py` has gone in alone (Dec 3 and Dec 4
  are answered). **They reach the package's branch** once A1a to A6 are merged (A5 and A6 for her
  topsail on a pole main).

  For the record: A0 moves nothing of hers, since she carries no studding sail and her lateen peak
  is 1.25, the engine's 1.246. V1 to V3 are for her report, not her file.
- **Her truths:** nine (Tar-D §13, T-1 to T-9; T-9, taken aback in a breeze, the third draft's).
- **Her pins:** none of a committed file. The probe's tests read the probe as filed.

### 8.2 The polacre (Pol, Pol-D)

- **Her second draft must settle:**
  - **Her size** from Winfield's polacras (Dec, Part D, P1). **Her files wait on them**, and her
    figures until then are a probe's, not a ship's (Pol-D §16 risk 1).
  - **Her two files** (Pol-D decision 1): the trader's (16) and the polacre of war's (71, the
    corsair's 80 recorded as a departure); the second file's name the lead's.
  - **Her going about** under Dec 3's answer: as a brig with her main, both lateens shifted or left
    (Pol-D §5.3; Eng §2.4.5).
  - **The step names**, A1, A5, A6 and V1 to V2 in place of her E1 to E4.
  - **The jibs' stays against the fore lateen's yard.** No rigging source covers it; the lead rules.
  - **Her ports:** one hull pierced for the corsair's seven a side for every fit, the ports shut
    and empty in trade; or plain for trade, with the armed fits' own ports. The lead rules; the lean
    is the first, as one hull in its roles.
  - **Brass guns' weights** for the navy's fit, from a source to be read.
- **Her files wait on:**
  - Winfield's rows;
  - A1a to A1d, A5 and A6 (all on the branch before the tartane's file);
  - N2 for her corsair fit.

  V1 and V2 are for her report.
- **Her truths:** six (Pol-D §14).
- **Her pins:** the smack's, from A5 and A6 (theirs, not hers).

### 8.3 The xebec (Xeb, Xeb-D)

- **Her second draft must settle:**
  - **Her size and the chambequín** (Dec 5).
  - **Her sweeps** (Dec 6).
  - ***Minorca* measured** (step 1, here: the 1280-px image kept outside the tree).
  - **Forfait's Table IV** read on the page image before it becomes a constant.
  - **Her suits:** the small lateens shifted in a gale, the square sails booked.
  - **Her heave-to**, refused in words (§4 row 13).
  - **Her wheel** (JUDGEMENT).
  - **Her regency's fit** on N2, under `Design-SlaveryAndSuppression.md` §8. Her file is open to the
    player under Spain's flag, as the rule asks.
- **Her file waits on:**
  - A1a to A1d, and A7;
  - A8 before her merge, since her "worst of all before the wind" truth fails on the untuned row
    today;
  - N2 and N3;
  - (Dec 3, 5 and 6 are answered.)

  Her hull, rig as data, guns and company can be built in her worktree before A1, as the
  bilander's were before the settee.
- **Her truths:** nine (Xeb-D §15).
- **Her pins:**
  - the guards that count the ship files;
  - the library's evolutions and the vocabulary's lists (A7's);
  - the checkpoint's names list.

### 8.4 The *Diana* (Dia, Dia-D)

- **Her second draft must settle:**
  - **Her fits** under Dec 7, and her pounders under Dec 9.
  - **GM 1.5 m** (JUDGEMENT, set from her captain's "stiff").
  - **Her spars** by the frigate's rule (Luce's chain) on her particulars. Chapman and Steel's
    20-gun column are the checks.
  - **The load line, first.** The drawn displacement is integrated to the arrowed line and set
    against the table's 497 t. If it misses by more than 5%, it goes to the lead before anything
    else.
  - **Her one fast tack**, 164 s from 295°, under truth 10's 285-s floor: to be tuned by her helm
    and rudder.
  - **The obús** of her 1817 fit, carried as a carronade.
  - **Her file's name** (`corvette-20.yaml`), and her rank at the rig's distance: the lead's.
- **Her file waits on:**
  - stage 0;
  - A0, since she carries studding sails;
  - N1;
  - Dec 7 and Dec 9.

  Nothing in the engine (Dia-D §9).
- **Her truths:** six (Dia-D §14).
- **Her pins:** the shared guards that range over every file, old beside new (Dia-D §15).

### 8.5 The *Purísima Concepción* (Con, Con-D)

- **Her second draft must settle:**
  - **Dec 8**, Dec 9 (her decision 9 and its §5.3 table, if the owner takes the nominal pounder)
    and Dec 10.
  - **Her lines from ZAZ0101** if the owner chooses her sister's hull (Dec 10), or PB-039 as a
    stand-in.
  - **Her tack**, quicker than the 74's today. Her rudder and helm's lead are tuned to a tack no
    quicker than the 74's and inside Luce's five to ten minutes. If no setting holds both the helm
    and the tack, the band is the lead's.
  - **Her masts** by Steel's rule, scaled 1.15.
  - **Her bill by deck**, with her soldiers under Dec 8.
  - **"The main deck"**, the lead's (§13.1).
- **Her file waits on:**
  - stage 0, A0 and A9 (her own);
  - Winfield's passages C1 and G3, on which her hull blocks and her bill wait, and G2 for her
    pounds by calibre under Dec 9's other way;
  - Dec 10 for her lines (without it, her hull stands at PB-039's stand-in);
  - N1.
- **Her truths:** five (Con-D §14). The pace truth is measured on the build machine.
- **Her pins:** none of another ship's file. A9 is keyed on a middle deck. V4's words move the 74's
  and the 64's port word.

---

## 9. The order, and how the builds run

### 9.1 The order

| Step | Who | What | After | Before | Pins it moves |
|---|---|---|---|---|---|
| S0 | stage-0 agent, here | §5.1 | the card agreed; the trunk merged in | everything | the hook test's table |
| A0 | engine track | item 37 | S0 | any new file generated | §10.4 |
| N1-N3 | the *Diana*'s builder | the shared data, each merged alone | S0 | the first Spanish people file; the corsair fits | the audit's counts (N2) |
| ***Diana*** | her builder | her file | A0, N1 | stopping point 1 | none of another file's |
| **Stopping point 1** | the owner | the first new ship, and item 37's boom ratings | | | |
| 0L | stage-0 agent, here | §5.2 | the lead's approval of A1's design (A1a to A1d) | A1a, and the lateen hulls' files | none (proven) |
| A1a, A1b, A2 | engine track | the whole lateen's side and its going about, the yard's change a part; the words | 0L | the tartane's file on the branch | A2's words; the library's and the vocabulary's counts |
| A1c, A1d | engine track | the rules captain; taken aback and the bad hand in a breeze | A1b (N2's `world/captains.py` merged first) | the tartane's merge | the books' counts, if the keys go into every book |
| A3, A4 | engine track | the helm; the boat in tow | A1b (the same files) | the tartane's file | A3's six files |
| A5, A6 | engine track | the yard's level; the pole | A3, A4 | the tartane's file (her topsail on a pole main) | the smack's |
| V1 to V3 | viewer | the lateen, the pole and the towed boat drawn | A1, A4, A6 | the tartane's report | the smack's picture (V2) |
| **Tartane** | her builder | `lateen.py` alone, then her two files | 0L for her files; A1a to A6 for her merge | the polacre's and the xebec's rigs (`lateen.py`) | none |
| **Stopping point 2** | the owner | the first lateen ship | | | |
| A9, ***Concepción*** | her builder | three decks, and her file | A0, N1, her passages, Dec 10 | stopping point 3 | V4's words |
| V4 | viewer | the middle deck's port words | A9 | her report | the 74's and the 64's port word |
| **Stopping point 3** | the owner | the first three-decker | | | |
| **Polacre** | her builder | her two files | A1a to A1d, A5, A6, N2; Winfield's rows | stopping point 4 | none |
| **Stopping point 4** | the owner | the square main among lateens | | | |
| A7 | engine track | sweeps | A6 | the xebec's sweeps | the counts |
| **Xebec** | her builder | her two files | A1a to A1d, A7, N2, N3 | A8 | the file counts |
| A8 | engine track | the gale; the lateen row tuned | the tartane and the xebec on the branch, and the polacre if she has landed (§4 row 7) | the xebec's merge | the lateen hulls' own figures |
| **Stopping point 5** | the owner | the whole package | | | |
| Phase 5 | integrator | §3 | every merge | the lead's close | — |

**Why this order:**
- **The ship-rigged road** wants least of the engine. The *Diana* is the smallest build of the
  five (Dia-D §0), and her builder settles the shared data first. The three-decker needs only A9,
  her own step, but waits on Winfield's passages for her blocks and her bill.
- **The lateen road** follows the lead's view: the tartane first, as the smallest hull, the
  reference vessel, the first whole lateen and the first pole main (so A1a to A6 come before her);
  then the polacre; then the xebec. Each waits on the
  engine steps that come before her, and the engine track's files are shared, so its steps run one
  at a time.
- **If the polacre's passages have not come** when A6 lands, the xebec goes ahead of her: A7 needs
  only A6, and A8 is tuned on the lateen hulls then on the branch (§4 row 7), so nothing of the
  xebec waits on the polacre. The polacre then follows when her rows arrive, her figures measured
  against the tuned row, old beside new. Her files alone wait on them.
- **At most four sessions run at once:** the engine track, the viewer, and one hull on each road
  (JUDGEMENT). Each reported hash is read independently. More hulls in flight than the lead can
  read would only queue at the readings.

### 9.2 Where each piece runs

- **Here, on the owner's machine:**
  - research, the owner's books and coordination;
  - stage 0 and 0L, built by one agent and checked by another;
  - the measuring of images that stay outside the tree;
  - the merges into the package's branch and their checks;
  - the testing reports' pictures, where a cloud session has no browser pane;
  - the reports to the lead, as notes in `docs/dev/M7-WorkPackages.md`.
- **In the cloud:** the engine track, the viewer, and one session per hull. Each starts from the
  pushed package's branch at a named hash and works on a branch of its own. Each is briefed with:
  - **the rules:** no model or maker named; ship files only through the generator; never a test
    skipped; pins moved old beside new; truths as states, never digests;
  - **its documents:** its design's second draft, this plan, and its row of §7.1 as the files it
    may change;
  - **the stop rule:** a step that needs any other file stops, and says so;
  - **its sources:** facts by page only (it cannot read the owner's notes);
  - **its suite:** the fast tier whole within the container's stated limit of hours.
- **Checking a cloud branch here.** A cloud session sends no report back, so this session reads
  each branch:
  - its diff against its brief's list of files (card 3's path check: one file outside the list,
    and the step goes back or gets more);
  - its junit against the base, test by test;
  - the byte test, the golden classing table, and the guard set of §10.2;
  - its testing report, filed as text on its branch.
- **The merge.**
  - Into the package's branch, never a rebase, and pushed.
  - The hash is reported to the lead.
  - The lead gates that hash, with:
    - an independent reading by a reader of the other tier, told which standard to hold (§2 item
      4);
    - the whole suite in the cloud;
    - a few passes where needed, each one gathered list.
  - The lead merges to the trunk at a stopping point, or hull by hull, as the lead chooses.
- **The trunk** is brought in at each boundary, with `git fetch origin && git merge
  origin/claude/dreamy-darwin-d77nty` on the package's branch, never a rebase, and the guard set
  run after it.

---

## 10. Tests, truths and pins

### 10.1 Each builder's tests

Each builder's tests go in its own new files (§7.1). Its truths are drafted there under their
reserved numbers, and the integrator moves them into `tests/test_known_truths.py` at the close, as
package 75 did. Each test enters through the door the behaviour is met at:
- a ship file loaded as the game loads it;
- an order given as a player gives it;
- the harbour's bare start.

That is the rule package 115's tests were held to, which this plan takes for its own (JUDGEMENT:
a test that builds the state by hand let faults through there).

### 10.2 The guard set every merge runs, and the lenses

**The guard set:**
- the byte test, two-way, and the golden classing table;
- `tests/test_schooner_mast.py` and `tests/test_probes_90.py`;
- `tools/check_viewer_guns.py`'s test;
- **at each of A1a to A1d, A2, A5 and A6:**
  - the lugger's guard set: `tests/test_lug.py`, truth 7b-111, `tests/test_captains.py`'s lug
    cases, the lug cases of `tests/test_view_geometry.py`;
  - the settee's, `tests/test_settee.py`;
  - the going-about set: `test_gale.py`, `test_rig_geometry.py`, `test_staying.py`,
    `test_lying_to.py`, `test_evolutions.py`, `test_captain_trials.py`, `test_catalogue.py`;
  - a trace of the lugger's and the frigate's tack, wear and heave-to at seed 7, before and after
    (a lens, not a test);
  - **at A1b and A7 also**: `tests/test_grammar_book.py`, for the new orders, the clause's parse
    and the primer's naming of them;
  - **at A1c and A1d also**: `tests/test_captains.py` whole, `tests/test_captain_rules.py`,
    `tests/test_standing.py` and `tests/test_strain.py`, since they reach the rules captain's going
    about, the practice's order as a standing order, and the strain;
  - **at A1a to A1d**: the probes' own going about re-measured, old beside new, by Eng §2.2a's
    measure (the tack and the wear, the yard shifted and left, the time and the ground lost).

**The review lenses** on each builder's branch (`Build-Ships.md` §17):
1. sources and fidelity;
2. sailing;
3. the generator;
4. the gun deck;
5. the viewer;
6. the engine's keys, under which no committed file sails otherwise;
7. the World's names, the pace and the checkpoints;
8. **new: the cause's mends.** For A2, A3 and A5, is each the cause's mend, and where else was the
   cause looked for?

### 10.3 The truths

Thirty-five are proposed:
- tartane 9 (T-9, taken aback in a breeze, is the third draft's);
- polacre 6;
- xebec 9;
- *Diana* 6;
- *Concepción* 5.

The lead numbers them at the card, from the first free number at that time (7-636 at 68e769ef),
in the order of §9.1. The engine steps' own behaviour is pinned in their test files, and in the
hulls' truths that state it ("she tacks and wears, her yards shifted round their masts or left";
"she shifts to her small lateens";
"under her sweeps in a calm"; "three gun decks at quarters").

### 10.4 Pins expected to move, by step

Each figure here is to be measured at the ground report. A moved pin is recorded old beside new
and passed by a reader other than the one who moved it.

| Step | Pin | How it moves |
|---|---|---|
| S0 | `tests/test_profile.py`'s `MODULE_FILES` and the hook test's name | five rows of `[]` |
| A0 | 74 boom ratings in 9 files; truth 35's last clause; `test_studding.py`'s frigate at six points; five records of no figure moved (`tests/test_hull_frigate.py:499`, `test_hull_brig.py` twice, `test_hull_schooner.py` twice); seven byte pins | regenerated; re-stated for the intended rating (Eng §1.5); the booms named; passed by the regeneration |
| A1a, A1b | `tests/test_agents.py`'s count of evolutions (`change_lateen`); the vocabulary's order lists (`shift` for a lateen, the clause, the practice's orders); `tests/test_grammar_book.py`'s `test_every_verb_of_the_vocabulary_is_named_in_the_primer` and `test_every_reading_of_the_registry_is_named_in_the_primer` | counts; the lists regenerated by their tools; the two primer tests passing again once chapter 5 names the new verb and reading |
| A1c | the captains' books' threshold counts, if the three keys go into every book (the lead's, §13.1); none if they are read with defaults | counts, grepped at the build |
| A1d | none (keyed on a whole lateen aback) | — |
| A2 | the wear's first line and the tack's last line for the lugger, the cutter and the smack, wherever a recorded passage holds them | words only |
| A3 | six files regenerated with `helm: tiller`; their records of no figure moved; their words where a helm is shot away; truth 7-626 measured | a key line; words |
| A5, A6 | the smack's heave-to and lie a-try with her topsail set; her topsail's take-in | behaviour where her topsail is set; no pinned passage expected |
| A7 | `tests/test_agents.py`'s count of evolutions; the vocabulary's order lists; the checkpoint's names list; `tests/test_grammar_book.py`'s primer test of the verbs | counts; the list regenerated by its tool; the primer test passing again once the sweeps' orders are named |
| N2 | the audit's counts of captain files; the roles' sets | counts |
| V2 | the smack's picture with her topsail lowered | the picture, old beside new |
| V4 | the 74's and the 64's port word in the viewer | words |
| each hull | the guards that count ship files (`tests/test_schooner_mast.py`'s eighteen, truth 7-190's table by file, `tests/test_subtypes.py`'s rows, the harbour's list of files) | eighteen to twenty-six, each named |

The descriptions' caches hold 32 files (Build decision 13), and twenty-six fit within them.

---

## 11. The cost in test runs on the owner's machine

The fast tier takes about 51 minutes here at eight workers, and the slow tier about 54 minutes
(Eng §1.4, measured on a loaded machine).

| When | What runs here | Time here |
|---|---|---|
| Phase 2 and Phase 3 (critics, second drafts, measuring, the owner's round) | nothing | — |
| S0 | the fast tier whole once, with `--junitxml`: **the base** for every later step; the stage-0 guards; the byte test | about 55 minutes |
| 0L | `tests/test_probes_90.py`, and the tests of the schema and the lateen; the base is S0's junit | about 10 minutes |
| Each merge of a cloud branch (about eighteen: A0; N1, N2 and N3; the *Diana*; A1a-A1b-A2; A1c-A1d; A3-A4; A5-A6; V1 to V3; `lateen.py`; the tartane; A9 with the *Concepción*; V4; the polacre; A7; the xebec; A8) | the byte test, the golden classing table, §10.2's guard set for that step's files, and lint. **No tier:** the cloud's fast-tier junit is compared here against the base | 5 to 15 minutes each, A1c-A1d's about half an hour (the captains' and the strain's tests whole): about two and a half to four and a half hours over the package |
| The three-decker's crewed pace | truth 7-196's world with three of her crewed, once, to record a figure (the floor is the build machine's) | about 2 minutes |
| The testing reports' pictures | the viewer in the built-in pane; no suite | minutes each |
| **Total** | **about three and a half to five and a half hours of the owner's machine over the package**, one at a time, and never beside another suite (third draft: half an hour more than the second version's three to five, for A1c-A1d) | |

**In the cloud**, not on the owner's machine:
- each builder's fast tier whole on its final tree, about an hour, plus the slow tier of its
  files;
- the lead's whole suite on each reported hash, and on the trunk at each stopping point;
- a fixer's run: only the slow candidates, then the fast tier with its junit.

**Plainly:** stage 0 could run in the cloud as well, leaving nothing here but the merge checks. It
is placed here because it is the base every cloud branch is cut from, and the lead gates it before
any cloud session opens. If the owner would rather keep the machine free, it moves without
changing anything else in this plan.

**By comparison:** in package 75 every builder's fast and slow tiers ran on this machine, one suite
at a time. About two of B3.4's three hours were suites.

**Scale** (JUDGEMENT, from package 75's record, in `Plan-ShipsWorkflow.md` §5's form):
- **Phase 2:** about fifteen agents: six critics, six second drafts, the measuring and this plan's
  second version. It runs no suite.
- **Phase 4:**
  - seven cloud sessions over the package (the engine track, the viewer and five hulls), at most
    four at once;
  - here, a stage-0 agent and its checker for each of the two stage-0 commits;
  - for each builder's branch, a review by lenses and one fixer.

The research and A1's design are where the effort is best spent. The hulls are mostly the
generator's existing method.

---

## 12. Risks, ranked

1. **A1 is new behaviour on every whole lateen of the package and is the largest step**, larger
   since the owner's answer to Dec 3: four steps in place of one (A1a to A1d), reaching the tack,
   the wear, the rules captain and the strain.
   - *Mitigation:*
     - designed once in the engine note (its third draft, §2.3, §2.4, §14), approved by the lead
       before 0L;
     - keyed on `dipping` on a whole lateen, or on a whole lateen set, which no committed file
       carries;
     - the lugger's and the settee's guard sets, the captains' and the strain's tests at A1c and
       A1d, and the trace (§10.2);
     - the probes tested with the key before any file carries it, their going about re-measured
       by Eng §2.2a's measure.
2. **Every figure of the lateen's going about is judgement**: the bad hand's loss, the change's
   seconds and hands, the captain's three winds, the strain aback. No source gives one (GA §5).
   - *Mitigation:* each is named in Eng §2.4 with its reason, the lead rules them (§13.1), and each
     hull's truths measure them on her own file. The probes already show the trade the owner's
     shape implies (Eng §2.2a: the yard left pays on a short board, the change on a long one),
     so a figure that loses it is seen.
3. **Sources not yet read when a file is built.** The polacre's size, the three-decker's blocks
   and bill, and the tartane's lines (Chapman) depend on them.
   - *Mitigation:* her file waits, or stands at a lower rung and says so (`Build-Ships.md` §5.0,
     principle 3). The passages are asked for now (Dec, Part D).
4. **Many sessions in flight, and the lead's readings.**
   - *Mitigation:*
     - at most four sessions at once;
     - the path check on every branch;
     - each reader told its standard;
     - five stopping points, with the whole suite on the trunk at each.
5. **The lateen row is untuned.** The xebec's "worst before the wind" truth fails today.
   - *Mitigation:* A8 comes before her merge, tuned on three hulls together. With A0 (a), the
     generator's lateen peak follows the row by itself.
6. **The cause's mends reach existing ships** (A2, A3, A5, and by their keys A6, V2 and V4).
   - *Mitigation:* each is named in the card with what it moves. The ground report counts the
     moving pins first, and more than about twenty brings it back to the owner.
7. **The three-decker stays quicker than the 74** (the engine's tack does not slow with size).
   - *Mitigation:* her rudder and helm's lead are tuned. If no setting holds both, the band goes
     to the lead.
8. **The regency's role and package 110's rules.**
   - *Mitigation:* N2's book says only what she does with a ship. The seat is refused in words, and
     the file is open to the player under Spain's flag.
9. **A cloud session cannot read the owner's notes or the image cache.**
   - *Mitigation:* every hull's step 1 is done here, and the briefs hold facts by page.
10. **The trunk moves under the package** while the gate's mends land.
   - *Mitigation:* a fresh merge at each boundary, with the guard set after it.

---

## 13. For the lead

### 13.1 Rulings asked (with this plan's lean)

1. **A1's machinery and its figures** (§4 row 3; Eng §2.3, §2.4, §14, A1a to A1d), on the owner's
   answer to Dec 3:
   - the machinery. The lean: `dipping` widened; the change in the tack and the wear on the
     settee's `SetteeChange`, the yard peaked and not lowered; `change_lateen` for the change by
     itself;
   - which side of the mast the car passes. The lean: abaft (Willaumez), O'Scanlan's forward
     recorded; it changes the drawing only;
   - the bad hand's loss. The lean: the lug's two-thirds, until A8's tuning;
   - the change's time and hands. The lean: 7½ seconds a metre of yard in a manoeuvre, the same in
     stays and in the wear, and one able hand for 2½ metres, at least four;
   - the order's words: the clause "and shift the lateens" or "and leave the lateens", and the
     practice's orders, "shift" in both by default;
   - the rules captain's winds and board: `lateen_tack_kn` 22, `lateen_leave_kn` 12, `bad_hand_s`
     1,800; in every book, or read with defaults and written only in the corsair's and the lateen
     hulls' books. The lean: the second, so that no committed book's count moves;
   - the strain aback and on the bad hand. The lean: `LATEEN_ABACK_LOAD` about 3.9 and
     `LATEEN_BAD_HAND_LOAD` about 1.5 on the engine's sustained load, set on each hull's file to
     the winds Eng §2.4.3 names (28 and 34 kn aback; about 45 kn on the bad hand);
   - the course's judgement wearing a lateen over `lateen_tack_kn` as `put her about` does
     (`judge_course`). The lean: yes, with the tack regardless where there is no room to wear;
2. **A5's reading of a topsail over a whole lateen** with no braced yard below it (the tartane
   if her tréou is left out): the lean, the lateen yard counted as the level below (Tar-D §5.1a).
   (The tartane's main's rake, asked of the lead in the first version, is the owner's: Dec 4.)
3. **A tiller's words and times** (A3), and A6's handing times. The lean: the builder proposes
   them, as JUDGEMENT.
4. **The polacre's ports.** The lean: one hull pierced for every fit. Also the jibs' stays against
   the fore lateen's yard.
5. **The files' names:**
   - `coastguard-tartane.yaml` (its description key `guarda-costa tartane`: Tar-D §9);
   - `polacre-of-war.yaml`;
   - `merchant-xebec.yaml`;
   - `corvette-20.yaml`;
   - `three-decker.yaml`.
6. **The *Diana*'s rank at the rig's distance.** "A ship" ranks her a frigate until she is made
   out. The lean: keep it.
7. **"The main deck" on a three-decker.** The lean: refused, naming her three decks.
8. **The relieving tackles' six hands at a first rate's tiller or wheel.**
9. **The second reef queued on a course already being reefed.** This is item 4 of the lead's notes
   of 2026-11-07, given to "package 90's or 77's, whichever reaches the gale's reduction first".
   A8 reaches it, so the card names it if the lead gives it here.
10. **The truths' numbers**, and the tier of each critic and reader.

### 13.2 Corrections to files this package may not edit (found in the research)

- **`docs/references/images/README.md`:**
  - the tartane's "two headsails" is one reading of the watercolour (Tar §9);
  - J1945 "as taken in 1797": Greenwich dates it 1799 (ZAZ0100), and the lines are ZAZ0101 (Con
    §2.3).
- **`docs/design/VesselReferences-2026-10.md`:**
  - §0: Lescallier's tartane article is pp. 400-401; pp. 394-401 is the chapter on lateen craft;
  - §3.3: Fincham's xebec is Forfait's Table IV by Fincham's own footnote, not a second source.
    Steel's xebec page is p. 237 (OCR p. 297).
- **`VesselReferences-2026-11-Spanish.md` §5 and the images README:** the *Diana* "taken at
  Cartagena with the declaration of war". Roos dates the seizure to 26 September 1809, two years
  after she came in (Dia §1).
- **Truth 7-196's docstring** records 150 ticks a second on 13 November. This machine gives 79 to
  81 in the same world. `tools/pace.py seventy-four` times a fight, not that world (Eng §7).

### 13.3 Older faults found on the way, not built unless the card names them

- **A boat's `out oars` refusal is keyed on the lug** (`orders/boat.py:82-84`). A boat under a
  lateen or a sprit would not be refused (Xeb-D §19).
- **"Send down the topgallant yards" on a bare topgallant mast** says "on deck already" (Pol-D §18
  item 4).
- **The tartane probe's heave-to says "the foresail sheet"** of the cutter's aliased fore staysail
  (Tar-D §17).

The three this package does mend, A2, A3 and A5, are in §2 item 5.

---

## 14. A draft scope card for the build (one page, for the lead to put to the owner)

| Field | |
|---|---|
| **Purpose** | The game gains its five Spanish and Mediterranean ships, from the smallest up: the tartane, the polacre, the xebec, the corvette *Diana* and the *Purísima Concepción* three-decker. Each is sailable from the harbour in her fits and roles, built from her sources by the ladder of evidence, and handled as the period handled her: a lateen tacked and worn, its yard changed round its mast or left on the bad hand (the owner's answer to Dec 3); a pole mast's sails lowered from the deck; a xebec at her sweeps; three gun decks at quarters. No existing ship sails otherwise, except where this card names it: item 37's boom ratings; three older faults mended at their cause; and what reaches existing ships by the new keys: the smack's topsail lowered onto the yard below and drawn so, and the 74's and the 64's port word |
| **Builds** | **(1) Stage 0 and 0L**, behaviour-free (plan §5). |
| | **(2) The engine's steps A0 to A9** (§6): item 37 by the owner's road; the whole lateen tacked and worn, its yard's change a part done or left by the order's words or the ship's practice, the rules captain's choice, and its danger taken aback in a breeze (A1a to A1d); the words of a rig with no yards; a tiller's words; the boat in tow; a yard's level and the pole mast; sweeps; the lateen in a gale, with its row tuned; three decks. |
| | **(3) The viewer's V1 to V4.** |
| | **(4) The shared data N1 to N3:** Spanish names; the regency's cruiser as a role with its doctrine; a Spanish marines kit. |
| | **(5) The five hulls in eight ship files:** the tartane and the coastguard tartane; the polacre and the polacre of war; the xebec and the merchant xebec; `corvette-20`; `three-decker`. Each with her people files, tests, truths and testing report. |
| **Does not build** | Any scenario or shelf line. The fisherman's description, which wants a fishing-grounds file. The chambequín, or the xebec of 30. The xebec's square sails for running, or her lying to under lateens. A polacre with a square mizen topsail. The obús as a kind of its own. A British *San Josef* fit. A seat for a player at a regency's cruiser. The nations' dated wars. The sweep ports drawn. The Danish draught. Anything else of package 77 or of the list of 79 |
| **May change** | **Only these:** stage 0's and 0L's files; `tools/gen_ships.py` (`SHIP_MODULES`, and item 37); the five new modules, `tools/ships/lateen.py` and `period.py`'s constants; the eight new ship files and their people files; existing ship files only by regeneration, under A0 and A3; the engine's files named in plan §7.1, `world/ships.py`'s far-body pace among them, and for A1a to A1d `orders/navigation.py`'s going-about choice, course judgement and stern watch, `orders/grammar.py`'s going-about modifiers and `orders/vocabulary.py`'s table for them, `physics/strain.py`, `world/captains.py`'s going about for a whole lateen and `api/readings.py`'s row for the practice; the rows of `world/ships.py` and `world/captains.py`, and `ROLES`; `data/evolutions/`, `data/vocabulary.yaml`, the lateen row of `data/sail_classes.yaml`, `data/captains/corsair.yaml` and the three lateen keys in the books the lead names, `data/crew/names.yaml` and `data/marines.yaml`; `client/projection.js`, `shipview.js` and `style.css`; the tests of these; the primer's going-about chapter at A1b, and a passage naming the sweeps' orders at A7, for the grammar book's tests; at the close, the notes, the specification as built and the primer's vessel pages. |
| | **A step that needs any other file stops**, and the builder says so before touching it |
| **Expected to move** | Item 37's: truth 35's last clause, `test_studding`'s frigate case, five records naming the booms, and seven byte pins by regeneration. A tiller's key in six files, and their words where a helm is shot away. The wear's and the tack's words for the lugger, the cutter and the smack. The smack's topsail handled as a topsail (A5), lowered onto the yard below and furled from it (A6), and drawn so (V2). The 74's and the 64's "a lower port" in the viewer's words, "a lower-deck port" (V4). The counts that grow by a file, a role or an evolution, the lateen's change and its orders among them (plan §10.4); the primer named for the new orders and the practice's reading, the grammar book's two tests passing again; the captains' books' counts only if the lead puts the lateen keys in every book. |
| | Each is measured old beside new and passed by a reader other than the one who moved it. **Anything else that moves is a stop, not a ruling** |
| **First step, before any code** | A ground report: (a) the trunk merged in, and the grep that no text of the game holds the new rank words; (b) for item 37, the tiller's key, the words and the smack, what moves, run and not guessed, with a count; (c) the tiller-steered files read from their sources. **More than about twenty pinned results moving brings it back to the owner before anything is built** |
| **How the owner tries it** | At five stopping points, from the harbour, each new ship from a bare start: (1) the *Diana* on a reach in a strong breeze, leaning as the frigate does; (2) the tartane: `tack ship`, her great yard shifted round the mast in stays; then `tack ship and leave the lateens`, a board on the bad hand, and `shift the mainsail`; then `wear ship`; (3) the three-decker: `beat to quarters` reports three decks, then `fire the starboard middle deck`; (4) the polacre: `take in the main topsail` lowers it onto the lower yard; (5) the xebec: `out sweeps` in a calm. |
| | With each hull's testing report: figures beside her comparator, and pictures in five views |
| **Size** | Two and a half to three and a half weeks of calendar at this week's pace, set by the readings and the trying, not by the tests. The engine track is about eleven working days of steps: eight in the second version, and about three more for the owner's answer to Dec 3 (A1b's change in the tack and the wear and its orders about one and a half, A1c's rules captain one, A1d's strain a half). Each hull is two to three days, in parallel (JUDGEMENT, from package 75's record). About three and a half to five and a half hours of the owner's machine (plan §11) |
| **Comes after** | The owner's gate of milestone 7, unless the owner says otherwise (Dec 1); the owner's answers (Dec 1 to 10, given 2026-11-18); the second drafts and these third drafts read by the lead, and A1's design (A1a to A1d) approved; for the polacre's files alone, Winfield's polacras |
| **Comes before** | Package 90's scenarios (a card of their own, after the nations' dated wars); any later ship of the session |
| **Who** | **This session, here:** stage 0 and 0L (built by one agent, checked by another), the measuring, the merges and their checks, the reports. |
| | **Cloud sessions:** the engine track, the viewer and one per hull, at most four at once, each on its own branch. Each runs the fast tier whole within its container's limit of hours. |
| | **The lead:** every reported hash read by an independent reader of the other tier, told the standard to hold; the whole suite in the cloud on each reported hash and on the trunk at each stopping point; a few passes where the work needs them |

**The choices in this card that are the owner's:** Dec 1 to 10, answered on 2026-11-18 (nine as
picked, the third in the owner's own shape). And Winfield's passages, which the owner sources
(Dec, Part D).
