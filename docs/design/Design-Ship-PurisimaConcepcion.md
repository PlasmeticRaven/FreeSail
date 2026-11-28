# Design: the *Purísima Concepción* class three-decker of the Spanish navy (package 90, second draft)

**Revised 2026-11-20 on her measuring, the owner's choice of her source and the lead's rulings of
that day (14:10 UTC, nudge 30, item 4).** Her step 1 measured her own plan, PB-039, at the library's
full size (12,932 × 4,574 px, 39.75 px a pie), and her sister's sheets at Greenwich, ZAZ0100 to
ZAZ0103, at the 1,280 px the museum serves. The measuring is set down in
`docs/design/ships-design/pages-concepcion.md` (**Pages**). The owner chose her source the same day:
asked "Draw her hull from PB-039 instead?", in place of their Dec 10 choice of the *San Josef*'s sheets,
they answered "Use PB-039 (Recommended)" (Dec Part F). The lead ruled on the measuring the same day.
Old beside new, each where it falls:
- **her source** (decisions 3 and 4, §0, §3.2, §16, §17 question 2): her lines from ZAZ0101 (rung S,
  a sister's) with PB-039 scaled her stand-in (S†) meanwhile, become **PB-039, her own plan as built
  (BVD record 1026905), unscaled: rung S, her own lines**. ZAZ0100 to ZAZ0103 stay as the comparison;
  they settle her sixteenth lower pair, the aftmost (§3.3).
- **her load line** (ruling 1; §2): a level line at 7.5 m to K (JUDGEMENT) becomes **the line as
  traced** on PB-039, 8.02 m to K at the post's after face, 7.94 m at the middle and 7.65 m at the
  stem's fore face, a drag of 0.37 m. The straight fit (8.17, 7.92 and 7.67 m, a drag of 0.50 m) is
  recorded beside it, with the doubt about the photograph: the other waterlines leave their straight
  fits aft unevenly (Pages §12.1). `draught_m`: 7.5 → **7.94**.
- **`displacement_kg`** (ruling 2; decision 4, §2): 4,200,000 (JUDGEMENT on a level 7.5 m line, the
  *Diana*'s cause) → **4,440,000**, about 4,440 t, the body as drawn, outside the plank, at the line as
  drawn; the range 4,421 to 4,473 t, the plank's 3 to 4 pulgadas JUDGEMENT. Every other figure of
  her file is reckoned to that line: her draught, her breadth at the water, her lateral area and her
  KM (Pages §12.1). Winfield's 5,167 t is recorded beside it: read as toneladas of 2,000 libras, about
  4,762 t, most likely reckoned level near her after draught (JUDGEMENT; the book's own mark on the
  figure, the owner's p. 407, would settle it: Pages §12.5).
- **her length** (ruling 3; decision 4, §2, §3.2): `length_waterline_m` 61.30 (Winfield's rebuilt
  eslora) → **61.26**, PB-039's from the post's after face to the stem's fore face on her line (219.8
  pies; 220.0 outside them at the lower deck). The lengthening of her lines by 1.029 is dropped: it
  came from the research note's "about 214 pies", read short of the stem, and would count the rebuild
  twice. Whether her eslora is between the rabbets (215.5 pies) or outside (220) stays open.
  `hull_speed_kn` stays 13.1 (13.13 on 61.26 m against 13.13 on 61.30: computed).
- **`deck_height_m`** (ruling 4; §2): "about 5.2 m" → **ruled 5.99 m** (the lead's nudge 33, 2026-11-20): by the seventy-four's method, the mean of the lines her sheet draws for that deck, above her line as traced; this note's upper line's 6.06 m recorded beside it. 6.06 m was first ruled on the
  condition that it is the same deck by the same method as the 74's 3.16 m and the 64's 3.22 m (the
  upper deck in the waist). It is the same deck by its place, but not the same method in one
  particular: the 74's is the mean of the top and middle red lines her sheet draws for the deck, where
  Pages took the upper of PB-039's pair. By the 74's method she stands 6.00 to 6.01 m (5.98 to 6.00
  above the line as traced). Not filed (Pages §5.3).
- **accepted as measured** (ruling 5):
  - the ports (§3.3, §3.4): the lower 1.04 × 0.83 m (the 74's, interim) → **1.01 × 0.93 m**, its sills
    (not known) → **1.89 to 2.48 m, 1.91 m amidships**; the middle and upper 0.84 × 0.80 m (interim) →
    **0.91 × 0.76 m** and **0.80 × 0.67 m**; 15, 16 and 16 a side on PB-039 and 16, 16 and 16 on
    ZAZ0100, the sixteenth lower pair's place (the aftmost, JUDGEMENT) → **the aftmost, read**;
  - the lee port (§10): waiting on tasks 2 and 5 → **13.3°** at the midship port;
  - the rudder (§2): "from ZAZ0101's sheer (task 4)" → **13.3 m², a span of 8.29 m**;
  - the lateral plane (§2, a new row): **475.2 m²** to K and the knee, the rudder left out, by the
    drawn hulls' method, D29 (b); about 473.5 m² reckoned to the line as traced (computed, Pages
    §12.1);
  - the decks (§3.2), the stern's lights on PB-039 (§13) and the masts' places (§4.1): measured
    (Pages §5.3, §5.5, §5.7), the masts at **x −18.94, −3.47 and +23.37 m**.
- **found besides** (Pages): PB-039 is a full body plan of eighteen sections with a half-breadth plan,
  not a section only (§19); ZAZ0100 gives the quarterdeck six ports a side and the poop three, the
  forecastle's not made out (decision 5, §3.3); her five truths' range, 7-735 to 7-739 (§14; Plan
  §10.3).
- **for the lead** (§18 items 7 to 10): `deck_height_m`; her `draught_m` at the middle of a bent line;
  the length's convention by D29 (b), as the *Diana*'s; the breadth's factor of the old stand-in rule.

**Revised 2026-11-19 on Winfield's passages sent by the owner, and the owner's answers of that
day.** The units (Winfield et al. 2023, pp. 41-46), the complements of 1788 (p. 1446 and the two
pages following) and of the Regulation of 16 October 1803, and the ordinance of 1803's guns by deck
came, set down in `VesselReferences-2026-11-Spanish.md` §7, §15 and §16. The class's own pages
(C1) were not sent; by the owner's word, what they would have given is filled from other research
or judgement. This revision carries, each figure old beside new:
- **her company by the regulations** (decision 10, §6.1, §6.3, §14, §17 question 3): for the 1797
  fit the 1788 regulation's **877** (was her own 839, kept in the note), of whom **225 soldiers, 168
  infantry and 57 infantry-artillery** (was about 100, interim JUDGEMENT); for the 1809 fit the 1803
  regulation's **1,015**, of whom **275**, recorded as a departure since a company is the file's;
  whether the engine's rule then leaves crews empty, measured at her build and for the lead;
- **her guns by deck by her own record** (pp. 406-410), **the ordinance of 1803's 118 noted** beside
  her 116 (two more 48-pounder obuses on the quarterdeck), and its note that she carried 18-pounders
  in her third battery (§5.1);
- **her calibres by the book's libra** (0.4608 kg, one ratio, 1.0159, for every calibre): the other
  way's English figures move from the broadside pairs' ratio to it, a 36 from 38.85 to 36.57 lb, and
  the 36's interim weight from 66.8 to 62.9 cwt (decision 9, §5.3); **the guns' weights by calibre
  are still to come** from other research (the period's Spanish artillery treatises, for example)
  or JUDGEMENT;
- **her length's label**: the eslora, on the lowest planked deck over both overhangs (§2); the
  figure does not move.

The second draft (2026-11-18) of the design for package 90's fifth hull, the Spanish navy's
*Purísima Concepción* class, the game's first ship of three gun decks. By the plan's method
(`Plan-ShipsWorkflow.md` §2, Phase 3) it answers the critic's reading of the first draft item by
item ("How this draft answers the critic", below the decisions) and takes the settlements of
package 90's plan (`docs/design/Plan-Package90.md` §4, its step names in §6: A9 is hers). It is for
the lead and, through the lead's scope card, the owner. **Nothing here is
built**, and nothing may be until a scope card for the build is agreed with the owner
(`docs/dev/ScopeCards-BeforeTheGate.md`, "How a package runs, as amended on 2026-11-16"; the
lead's note of 2026-11-18, nudge 15).

**What binds, in order:**
1. The lead's note of 2026-11-18, 00:50 UTC (row 90's last paragraph in `docs/dev/M7-WorkPackages.md`):
   the preliminaries only; documents alone; the build from a scope card agreed with the owner.
2. Row 90 and the notes to the ships session of 2026-10-29 and 2026-11-06 (18:00 and later): the
   first three-decker, "three gun decks, a first rate's complement and her stations, the great
   ship's handling"; the 1797 fit of 112 for St Vincent and the 1803 fit of 116 for the war's
   scenarios; Winfield's metres for the game's constants; the book's pairs of libras and pounds as it
   gives them.
3. `docs/design/Build-Ships.md` (cited **Build**): §5.0's principles and ladder; §6's postscript,
   package 81's checklist for ports and guns; §8, fits and roles; §13.2's list of what a ship's
   design settles (the 74's, the nearest kin).
4. Her research note, `docs/design/Research-PurisimaConcepcion-2026-11.md` (cited **Res**), and
   `docs/design/VesselReferences-2026-11-Spanish.md` §4 (cited **VR-Sp**, Winfield via the lead).
5. The 74's design, `docs/design/Design-Ship-Bellerophon.md` (cited **Bel-D**): her bill by deck
   (§6.4, B7.b as built), her numbering by deck (§5.2, B7.d as built), her made-out words (§8 and
   the lead's ruling 17 of 2026-11-12), her lateen mizen and yards under the bowsprit (§4).
6. `docs/design/Design-ShipsEngineExtensions.md` (cited **Ext**): §3 (B3.1, the lateen cut at the
   mast) and the schooner's-mast rule (B3.4, `Ship.on_schooner_mast`), which she meets only to be
   classed a ship.
7. The engine's note for package 90, `docs/design/Design-Package90-Engine.md` (cited **Eng**):
   its §6 on three gun decks and the obús, read beside this draft's own probes.
8. Package 116 (the wheel shot away, `repair the wheel`, the cruiser's doctrine read from
   `thresholds:`) and package 96 (`client/harbour-shelves.yaml`, a sentence a scenario).

**Marks** as Res's: *read*, *read (OCR)*, *read on screen*, *catalogue*, *via Winfield*,
*measured*, *observed*, *judgement* (in capitals, **JUDGEMENT**, where a figure of hers rests on it
alone). **2026-11-20:** *measured* also off PB-039 at the library's full size (39.75 px a pie) and
the Greenwich sheets at 1,280 px (Pages, its marks). The rungs are the lead's: **A** the original
plans, **B** a historian's particular, **C** judgement; **rule** for a named period rule applied to
her own particulars (§5.0's R). "Plainly:" marks a departure from a ruling, a precedent or a
source, with its reason. "Observed here" means a run of this draft's scratch scripts (Res §7;
`scratchpad/p90/concepcion/`, the session's scratch, not filed), each with `py`, the pkg-90 tree
first on `sys.path`, `freesail.__file__` asserted under it; no tracked file of the tree was changed
(Python's git-ignored bytecode caches aside) and no git write made.

**One sentence.** One module writes one file of the rebuilt hull for both her fits: her lines her
sister's at Greenwich checked on her own plan at Madrid (since 2026-11-20, her lines her own plan's,
PB-039, by the owner's choice, her sister's the comparison), her three tiers of sixteen ports on the
74's machinery for decks (which already takes a middle deck), Winfield's two establishments to the
libra, a company of 839 split so that every gun is manned (since 2026-11-19, her company by the
regulations of 1788 and 1803, her soldiers their infantry and infantry-artillery), her rig by
Steel's rule until a Spanish one is read, and her own words, rank and polar so that she is made out, feared and sailed as a
first rate.

---

## Decisions proposed

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/concepcion.py`, `build(out_dir)` writing `data/ships/three-decker.yaml` (her name *Purísima Concepción*); her people `data/people/three-decker.yaml` | The 74's form (Bel-D decision 1): a file by her type, a name by her ship |
| 2 | **One hull, as rebuilt (1786 to 1793), for both fits**; the as-built hull of 94 is no fit | Both her fits are after the rebuild (VR-Sp §4); the game's era is 1792 to 1820 (`Plan-ShipsWorkflow.md` §0) |
| 3 | **Her lines from ZAZ0101** (her sister *San Josef* as fitted at Plymouth, 1:48, 1801: body, sheer, half-breadth), rung A (§5.0's S, a sister's lines) **once it is read at step 1** (not viewed yet: Res §0.3); until then **PB-039** (her own plan as built, 1779, read on screen) scaled to her rebuilt length stands as her stand-in, S†, and checks ZAZ0101 after | The rebuilt form is the one she sailed; PB-039 is before the rebuild (Res §2.3, §2.4); a source on file but unread is no rung (§5.0 principle 3). **2026-11-20, the owner's answer** ("Use PB-039 (Recommended)", to "Draw her hull from PB-039 instead?"): **her lines PB-039's, her own plan as built, unscaled, rung S**; ZAZ0101 read at 1,280 px only, the comparison (Pages §1.2, §11) |
| 4 | Hull blocks: length 61.30 m (Winfield, rebuilt), extreme breadth 16.54 m (James, the *San Josef*), draught and displacement measured at her water; interim 7.5 m and 4,200 t, **JUDGEMENT**; Winfield's 5,167 t recorded beside. **2026-11-20 (the lead's rulings 1 to 3):** length 61.30 → **61.26 m** (PB-039); draught 7.5 → **7.94 m** to K at the middle of the line as traced; displacement 4,200 → **about 4,440 t** (4,421 to 4,473 t outside the plank); Winfield's 5,167 t beside it, about 4,762 t as toneladas of 2,000 libras | §2 |
| 5 | **Three tiers of sixteen ports a side** (lower, middle, upper), the lower's sixteenth pair empty in Spanish service; the quarterdeck's and forecastle's ports as ZAZ0103 and ZAZ0100 show them. **2026-11-20:** ZAZ0100 draws 16, 16 and 16 a side, the sixteenth lower pair the aftmost; the quarterdeck 6 a side, the poop 3 small ones; no forecastle port made out at 1,280 px, and ZAZ0103's plans do not show the ports at that size (Pages §11.3) | Res §2.4 (PB-039's 15, 16, 16 as built); VR-Sp §4 (the sixteenth pair cut in 1791) |
| 6 | **Guns numbered by deck** (`numbering: by deck`), each deck from No. 1 forward, the 74's B7.d | Built and measured on her scratch file (observed here); the period numbered each deck (Bel-D §5.2) |
| 7 | **Two fits**: "concepcion 1797" (112, the default) and "concepcion 1809" (116, the 1803 alteration) | VR-Sp §4; each sums to Winfield's broadside in libras exactly (observed here) |
| 8 | **The obús carried as a carronade** of its calibre, its words and note saying obús | The engine refuses an `obus` kind and takes a 48-pounder carronade (Eng §6.3); a new kind is engine work beyond her file (§5.4) |
| 9 | **A gun's `pounder` as her navy named it** (`pounder: 36`), Winfield's pairs of libras and pounds in the note as the book gives them, never a ratio re-derived from them: **the owner's (Dec 9)**, this the pick; the other way, the English weight in the file with the words from a separate key, set beside it in §5.3. **2026-11-19:** the book's libra, 0.4608 kg (pp. 41-46), gives the other way's figures, one ratio for every calibre (§5.3); the pick, settled, is unchanged | The lead's rule (VR-Sp "Units": take the pairs as given); the plan's §4 row 8. **Plainly:** the first draft filed each calibre by Winfield's broadside ratio, which re-derives the book's ratio per calibre |
| 10 | Company 839: posts 18, idlers 60, **her soldiers 100, the bill keeping 60 as small arms**, seamen 661: every gun of one side manned at the beat (observed here). **Interim** until Winfield's dotación by kind (Dec Part D, G3) is read. **Revised 2026-11-19, G3 read: her company by the regulations**, the file's the 1797 default's by that of 1788, **877** (was 839), of whom **225 soldiers** (168 infantry, 57 infantry-artillery; was 100); the 1809 fit's by that of 1803, **1,015** of whom **275**, a departure recorded in its note (a company being the file's), or a second file if the lead prefers; the rest split onto the game's stations at her build (JUDGEMENT). Her crews under the engine's rule are measured then, and go to the lead if any stands empty (§6.1) | Winfield et al. 2023, p. 1446 and the table of the Regulation of 16 October 1803 (VR-Sp §15); VR-Sp §4 (her own 839, not broken down); the marines never serve a long gun in the engine (Bel-D §6.3), so about 160 soldiers, the 74's share (JUDGEMENT), leave four crews unmanned (observed here; §6) |
| 11 | Masts by Steel's rule on her own particulars (the main mast half her lower deck and extreme breadth), the rest by the 74's proportions scaled 1.15, **rule and JUDGEMENT**, until a Spanish rule or PB-078 is read | Res §5 |
| 12 | The mizen course on a lateen yard cut at the mast (B3.1) in both fits; the spritsail and sprit topsail yards as the 74's; **no driver** | The 74's machinery; no Spanish source either way (Res §5); the driver is the owner's British choice (Bel-D §4.6) |
| 13 | Her words: description `three-decker`; at the rig's distance the tops make out **"a three-decker"**; the glass **"a three-decker, sixteen ports a tier"**; how she is rigged, "a ship" | Package 75's made-out rule, the lead's ruling 17 (Bel-D §8) |
| 14 | **Size rank 5**, a class above the 74's 4, `LINE_OF_BATTLE_RANK` unchanged | The owner's (§17 item 1) |
| 15 | Roles: `kings-ship` and `commodore` (a flagship); her nation the scenario's; a British fit "as the san josef 1801" booked, not drawn | Build §8.2; Bel-D §8 |
| 16 | Her polar given her own length and canvas so that she sails between the 74 and the frigate (observed here: 8.01 kn abeam in 15 kn against 7.87 and 8.19); her tack slowed to no quicker than the 74's by her rudder and her helm's lead | Res §6 (Brenton, James); §9 |
| 17 | Truths 7-NNN-a to e (§14), numbered by the lead at the scope card | Build §15's form |
| 18 | Her first scenario: Cape St Vincent, 14 February 1797, on the Actions shelf, a sentence (§11): **booked** for a card of its own after the nations' dated wars, not in the build's card (the plan's §4 row 15); she is offered from the harbour for a bare start | Package 96; Res §8 |

---

## How this draft answers the critic

| Finding | What the first draft said | This draft |
|---|---|---|
| F2 (blocker): a personal path | the scratch folder written out in full, with the account's name | **Held.** `scratchpad/p90/concepcion/`, the session's scratch, not filed, as the other notes write it (the marks; Res §0) |
| F9: rungs before reading | ZAZ0101 "A (S)" though not viewed | **Held.** S once ZAZ0101 is read at step 1; PB-039, read on screen, her stand-in (S†) until then (decision 3, §3.2) |
| F11: the soldiers' other way | "file the soldiers as Winfield gives them" | **Held.** Winfield gives the 839 unbroken; the other way is about 160 soldiers by the 74's share (JUDGEMENT) with the engine's rule changed. The pick of 100 is interim until G3's dotación is read (decision 10, §6.1, §17 question 3) |
| F17: which length | "not said in VR-Sp"; filed as the length on the gun deck | **Held.** VR-Sp labels it "Length overall"; the *Diana*'s plan, where Winfield's 124 pies measure as the gun deck from post to stem (Dia §2.2-§2.3), is the reason to read it as the eslora on the gun deck, JUDGEMENT; C1 stays asked (§2) |
| F23: the pace | "three crewed at the first thousand and two after", 0.96 | **Held.** Her p5c.py ran a world of its own (three of the file added as patrolling vessels off the Lizard), not truth 7-196's; in truth 7-196's own world the engine note measured three three-decker probes at 72 to 75 against three 74s' 79 to 81, all three crewed throughout (Eng §7): about 0.92 (§9) |
| The plan's settlements | the pounder by Winfield's ratio per calibre; a first scenario | the nominal pounder as the pick, the owner's (decision 9, §5.3; Plan §4 row 8); no scenario in the card (decision 18; Plan §4 row 15); A9 hers (Plan §6) |

---

## 0. The gate, the order, and what waits

**No build until the owner's scope card.** The order inside package 90 is the plan's (§9.1): on
the ship-rigged road the *Diana* first and she second, beside the lateen road; A9 (three decks) is
her own step, built by her builder. Her build would want, in
this order and each on its own word:

| Piece | Whose | Before her file? |
|---|---|---|
| The owner's answers to §17 | the owner | yes |
| Winfield's passages (Res §11) | the owner's books | the hull blocks and the bill wait on items 1 and 2; nothing else does. **Received 2026-11-19, in part:** the bill by the regulations (§6.1) and the libra (§5.3); the class's pages (item 1) not sent, so her draught, sills and rudder are measured on ZAZ0101 or judged, and the keel's and the rebuilt length's digits stand as printed. **Nothing waits on Winfield now**. **2026-11-20:** her draught, sills and rudder measured on PB-039 at step 1 (Pages); her length PB-039's 61.26 m by the lead's ruling 3, Winfield's printed 61.30 beside it |
| PB-039 held in the tree (CC BY 4.0), and the choice of her hull: her sister's ZAZ0101 as rebuilt, or PB-039 as built (Dec 10; the sheets themselves read under the standing Greenwich rule) | the owner | her hull's lines (§3.2) wait on it. **Answered 2026-11-20:** PB-039, her own plan ("Use PB-039 (Recommended)"), the Greenwich sheets the comparison. Dec 10's first part, PB-039 held in the tree, stands as agreed and was not done at step 1 (her image is kept outside the tree: Pages §1.1) |
| Her words and rank in `world/ships.py` and `world/captains.py` (§8) | her builder, the lead allotting `world/` | with her file |
| "The second deck", "the third deck" in `orders/gunnery.py` (§5.5) | the gunnery's owner, or her builder on the lead's allotment | no: words only |
| The obús as a kind of its own | a later gunnery package | no: carried as a carronade meanwhile |
| A Spanish names list (`data/crew/names.yaml` has English, American and French) | her builder or the *Diana*'s | with her people file |

Nothing of her moves another ship's file, truth or pin (§15).

---

## 1. The module and the generator

### 1.1 Files

- `tools/ships/concepcion.py` (new): `build(out_dir)`; imports `gen_ships` as `g`, `period`,
  `mizen_yard`, `spritsail_yards`; nothing from `bellerophon.py` (Bel-D decision 3: an import
  would tie her bytes to another ship's module).
- `data/ships/three-decker.yaml` (generated).
- `data/people/three-decker.yaml` (hand-written data, as the 74's).
- `tests/test_concepcion.py` (new).
- Rows in `freesail/world/ships.py` and `freesail/world/captains.py` (§8), and the words of §5.5.

### 1.2 What she reuses, read only

The 74's machinery throughout: `g.broadside_pair(..., deck=<word>, round_to=0.01)` and the re-keying
of ids by deck after it (`gun.middle.3.starboard`: Bel-D §5.2, B7.d as built); `numbering: by
deck`; `g.hull_profile` with `decks_m`, `ports_m` and `port_size_m` for each of her six decks
(`schema.DECK_WORDS` already holds `middle`: `freesail/ship/schema.py:339`); `mizen_yard.py` (the
course cut at the mast); `spritsail_yards.py`; `g.fit_magazine`; `g.exercise_allowance(n,
decks=3)` (the Regulations' "a ship of two or three decks": Eng §6.2).

### 1.3 What is new in her module

Her own lists (no shared constant changes): her decks (`GUN_DECKS` as the 74's module keeps its
own, `tools/ships/bellerophon.py:2499`, Eng §6.2); her calibres in libras and their English pounds
(§5.3); her patterns' weights and crews (§5.3); her company's split (§6).

---

## 2. The hull blocks

| Key | Figure | Source, rung |
|---|---|---|
| `length_waterline_m` | **61.30** → **61.26** (2026-11-20) | Winfield's rebuilt length (via Winfield, p. 407; B), filed by the 74's convention of the length on the gun deck (Bel-D §2.1). VR-Sp labels Winfield's figure "Length overall"; the *Diana*'s plan, where Winfield's 124 pies measure as her gun deck from post to stem (Dia §2.2-§2.3), is the reason to read it as the *eslora* on the gun deck (JUDGEMENT), the owner's passage C1 asked. **2026-11-19:** the book defines its length (Winfield et al. 2023, pp. 41-46; VR-Sp §7): the *eslora*, on the lowest planked deck over both overhangs, neither the length overall nor the British gun deck's between the rabbets; for her the lower gun deck (JUDGEMENT); VR-Sp §4 relabelled. The figure filed does not move. **Plainly:** the book's pies give 61.43 m (220 pies 6 pulgadas × 0.2786); its metres are taken by the lead's rule, the owner's re-reading of p. 407 settling the digit (Res §2.1). James's 59.21 m for the *San Josef* (Res §2.2) is the check; ZAZ0101's scale measures it (task 1). **Revised, the lead's ruling 3: PB-039's 61.26 m**, from the post's after face (x 3,131 px) to the stem's fore face (x 11,870) on her line, 219.8 pies; 220.0 pies (61.30 m) outside them at the lower deck, 215.5 pies (60.06 m) between the rabbets there (Pages §5.1, measured). The lengthening of the lines by 1.029 is dropped (§3.2). Whether her eslora is between the rabbets or outside stays open; VR-Sp §7's definition (the lowest planked deck, both overhangs included) and the *Diana*'s plan read it outside, by which PB-039 draws about the rebuilt figure (220.0 pies against 220 pies 6 pulgadas: Pages §5.1): recorded, not settled. ZAZ0101 and ZAZ0100 draw the *San Josef* 59.71 m post to stem (Pages §11.2): the comparison. **Plainly:** D29 (b) files the drawn hulls' length rabbet to rabbet at the load line; hers, as the *Diana*'s, is post to stem by the ruling (§18 item 9). A, her own plan |
| `beam_m` | **16.54** | James's extreme breadth of the *San Josef* (vol. 2 p. 59, read (OCR); B). **Plainly:** not Winfield's 16.25 m, the book's *manga* being read as inside the plank (Res §2.2, JUDGEMENT); the file's beam is the extreme, as the 74's 46 ft 9 in is. If the owner's passage says the *manga* is extreme, 16.25. **2026-11-19:** the book's *manga* is the greatest beam at mid-length, the plank not said (pp. 41-46): the condition is not met in so many words, and 16.54 stands (JUDGEMENT). **2026-11-20:** unchanged; beside it PB-039's moulded breadth at her line, 16.34 m amidships, its body plan's frame 58.25 pies (the as-built manga 58 pies 0), and ZAZ0101's 16.23 m (Pages §4.5, §6, §11.2) |
| `draught_m` | **7.5**, to K, **JUDGEMENT** → **7.94** (2026-11-20) | Not found (Res §2.6). The 74's draught to K over her depth in hold (6.46 m on 19 ft 9 in: 1.07) on James's 7.44 m gives 8.0; on a Spanish ship built to carry her lower battery higher (James vol. 1 pp. 29 to 30) less (judgement). Measured on ZAZ0101 at her water (task 2). **Revised, the lead's ruling 1: her load line is the line as traced on PB-039**, 8.02 m to K at the post's after face, **7.94 m at the middle**, 7.65 m at the stem's fore face, a drag of 0.37 m (Pages §12.1, measured); the straight fit L0, the top of seven ruled waterlines inclined 0.47° to the keel, 8.17, 7.92 and 7.67 m (a drag of 0.50 m), recorded beside it, with the doubt about the photograph (the other waterlines leave their straight fits aft unevenly). To the keel's lower edge 7.65 m at the middle on the straight fit. The level 7.5 m was the *Diana*'s cause (Pages §4.4). K a false keel's lower edge (JUDGEMENT), as the drawn hulls file theirs (D29 (b)). The middle is taken, not the mean of the bent line's two ends, 7.84 m (JUDGEMENT; §18 item 8). ZAZ0101's waterlines are inclined 0.45° to its keel, its load line not identified at 1,280 px (Pages §11.2). A |
| `displacement_kg` | **4,200,000**, **JUDGEMENT** → **4,440,000** (2026-11-20) | Her length, breadth and draught at the 74's block (Res §2.5). Measured off ZAZ0101's sections at her water (task 3); Winfield's 5,167 t in the note and in truth 7-NNN-a's record. The scratch file at 5,167 t heels 0.5° less close-hauled and tacks the same (observed here). **Revised, the lead's ruling 2: the body as drawn, outside the plank, at the line as drawn**: about 4,440 t, the range 4,421 to 4,473 t (the line as traced and the straight fit, each outside 3 to 4 pulgadas of plank), the plank's thickness **JUDGEMENT**, no scantling source being read for her (Pages §4.3, §4.5, §12.1; computed, ±2%). Moulded with the keel, 4,327 to 4,349 t. Every other figure of her file is reckoned to that line: her draught, her breadth at the water, her lateral area and her KM. **Beside it, in her source note:** Winfield's 5,167 t (p. 407), read as toneladas of 2,000 libras (921.6 kg, the *Diana*'s table's unit), is about **4,762 t**, most likely reckoned level near her after draught (JUDGEMENT); as metric tonnes it would need a line 0.8 to 0.9 m above her drawn one, in the wale's band, drawn nowhere on the sheet. The book's own mark on the figure, the owner's p. 407, would settle its unit (Pages §12). The old 4,200 t was her body at a judged level 7.5 m (Pages §4.4: 4,080 to 4,110 t there). A, her own plan |
| `gm_m` | **1.5**, **JUDGEMENT** | The 74's 1.36 m (*Bombay Castle*, Bel-D §2.1) raised for a broad ship (James vol. 1 pp. 29 to 30: Spain built her ships broader than any other nation's, for safety); tuned within a band against the 74's heel |
| `deck_height_m` | her **upper deck** at midships, about 5.2 m, measured → **5.99 m** (ruled, nudge 33, 2026-11-20: the 74's method above her traced line; 6.06 by the note's upper line recorded) | D18 (Bel-D §2.3): the deck of the waist, the third; read for the wind on deck, her windage and the lookout's eye (`physics/sails.py:349`, `world/lookout.py:223`). **2026-11-20:** the 5.2 was the scratch file's (the 74's upper deck raised 2.05 m), not a reading. PB-039's upper deck at x 0, its upper red line, stands **6.06 m** above the straight fit (Pages §5.3, measured). **The lead's ruling 4**: 6.06 m on the condition that it is the same deck by the same method as the 74's 3.16 m and the 64's 3.22 m (the upper deck in the waist). **Checked (Pages §5.3): the same deck by its place** (the highest continuous deck, at the waist, at the middle line and at the middle, above her water by the same rule), **not the same method in one particular**: the 74's figure is the mean of the top and middle red lines her sheet draws for the deck (`tools/ships/bellerophon.py`:138-145, :775-778), where Pages took the upper of PB-039's pair; the 64's leaves the edge open by ±0.4 ft (`tools/ships/indefatigable.py`:147-153). By the 74's method she stands **6.00 to 6.01 m** (5.98 to 6.00 above the line as traced; 6.04 to 6.05 by Pages' line). **Not filed: for the lead** (§18 item 7) |
| `hull_speed_kn` | **13.1**, **JUDGEMENT** | The 74's 12.0 by the square root of the lengths (61.30 / 51.2); tuned within §9's band. **2026-11-20:** unchanged on 61.26 m (13.13 either way: computed) |
| `clr_x_m`, `rudder` | tuned (§9); the rudder **13.3 m², span 8.29 m** (2026-11-20) | Her rudder from ZAZ0101's sheer (task 4); her helm's lead tuned for the 74's helm close-hauled and a tack no quicker than the 74's. **Revised, the lead's ruling 5: PB-039's rudder, accepted as measured**: 13.3 m² below her line, a span of 8.29 m to its sole on K, 1.03 m broad at the line and 1.88 m at the heel, its centroid 4.68 m down (Pages §5.6, ±5%); ZAZ0101's not read at 1,280 px. Her angle and rate the 74's until tuned. A |
| `lateral_area_m2` | not in this table → **475.2** (2026-11-20) | **The lead's ruling 5: by the drawn hulls' method, D29 (b)**: the post's after face, K and the knee's fore edge, the rudder left out, 475.2 m² to the straight fit, 0.98 of her length times her draught (Pages §5.6, measured); 455.3 m² to the keel's lower edge and the stem's fore face, 488.5 m² with the rudder, beside it. **Reckoned to the line as traced** (ruling 2's condition): **about 473.5 m²**, the strip between the two lines aft taken out (Pages §12.1, computed). A |

---

## 3. The hull profile and her shape (Build §5.0 to §5.3, §5.7)

### 3.1 The form

The 74's: `rail_m`, `breadth_m`, `keel_m`, `stem_m`, `stern_m`, `wales_m` (the main wale and, as the
74's `channel_wales_m`, a wale between each tier), `section_m`, `decks_m` (six), `ports_m` (six),
`port_size_m` (six), `head_m`, `breadth_line_m`, `sections_m`, `form` (a square stern, its
galleries and lights by tier, a figure at the head), and `marks` for every line.

### 3.2 Her lines, by source

| Line | Source | Rung (§5.0) | Note |
|---|---|---|---|
| The body plan, sections and half-breadths | ZAZ0101 (1:48, 1801) | A (S, a sister's) once read at step 1; until then PB-039 scaled, S†. **2026-11-20: PB-039's body plan (eighteen sections) and half-breadth plan, A (S, her own), unscaled** (Pages §4.3, §6) | the *San Josef* as rebuilt and fitted; her sister's after the same rebuild (VR-Sp §4). **2026-11-20:** ZAZ0101 the comparison, its sections not measurable at 1,280 px (Pages §11.2) |
| The sheer, the rail and its steps, the wales | ZAZ0101 (sheer), ZAZ0100 (colour plan, 1799) | A (S) once read; PB-039 scaled, S†, until then. **2026-11-20: PB-039's sheer, A (S, her own)**; the wale measured amidships only (Pages §5.4) | ZAZ0100 for the eye of her upper works as the British found them |
| The stem, the head, the figure | ZAZ0101 ("figurehead"), PB-039 | A (S) once read; PB-039 meanwhile; the figure's form in words. **2026-11-20: PB-039's stem and knee, measured** (Pages §5.1, §6) | PB-039's head a beakhead with rails and a figure (Res §2.4) |
| The stern, the counter, the galleries and lights | ZAZ0101 ("sternboard with decoration detail", "quarter decoration"), PB-039 | A (S) once read; PB-039 meanwhile. **2026-11-20: PB-039's quarter and its lights, measured and accepted** (ruling 5; Pages §5.5); the stern board's measures not read | PB-039: two closed tiers of quarter galleries and a third of lights above (Res §2.4); the admiral's cabins on the *toldilla* (PB_0050, via Winfield p. 409) |
| The decks | ZAZ0102 (middle, gun and orlop, 1:96), ZAZ0103 (quarterdeck, forecastle, upper, 1:96), ZAZ0101 (inboard) | A (S) once read; T until then, to read: ZAZ0102, ZAZ0103. **2026-11-20: PB-039's red lines, measured and accepted** (ruling 5; Pages §5.3); the Greenwich plans not readable for heights at 1,280 px | |
| The ports, their sills and sizes | ZAZ0101 and ZAZ0100 (rebuilt, 16 a tier); PB-039 (as built: 15, 16, 16, read on screen) | A (S) once read; PB-039's tiers, S†, meanwhile. **2026-11-20: PB-039's, A (S, her own), measured and accepted**; the sixteenth lower pair placed by ZAZ0100 (ruling 5) | §3.3 |
| The keel and the body under the water | ZAZ0101 | A (S) once read; PB-039 scaled, S†, meanwhile. **2026-11-20: PB-039's, A (S, her own)**, to the line as traced (Pages §12.1) | kept as data (§5.0 principle 11) |
| Anything a sheet does not reach | the default rule (Build §5.3) | C, `judged` | its note names the hull it must differ from, the 74 |

**Plainly:** until the Greenwich sheets are read and measured at step 1 (and the owner chooses her
hull from them: Dec 10, question 2), her lines stand on PB-039 alone, her own hull before the rebuild: lengthened by her rebuilt length
over her built length (61.30 / 59.55, 1.029: §5.0 principle 7's stand-in scaling, `stand-in`), her
sections by the breadths (16.25 / 16.16), the sills from PB-039's own tiers. That is the fallback,
not the plan.

**Revised 2026-11-20 (the owner's choice; the lead's ruling 3).** PB-039 is her hull, and **the
fallback's lengthening is dropped**: PB-039 already draws her 61.26 m from the post's after face to
the stem's fore face on her line, not 59.55; the 1.029 rested on the research note's "about 214 pies",
read 170 px short of the stem's fore face, and would make her about 63.0 m, counting the rebuild
twice (Pages §5.1). Her lines are PB-039's as drawn, rung S, her own. **The breadth's factor**
(16.25 / 16.16, 1.0056) is not named by the ruling: PB-039's body-plan frame measures 58.25 pies,
between the as-built manga's 58 pies 0 and the rebuilt 16.25 m (58.32 pies), inside the scale's
±0.4%, so the sheet cannot tell them apart. Taken as drawn, unscaled, as ruling 2's "the body as
drawn" reads (JUDGEMENT; §18 item 10). ZAZ0100 to ZAZ0103 stay as the comparison (Pages §11).

### 3.3 The ports and their sills

- **The lower deck: sixteen ports a side** as rebuilt (the sixteenth pair cut in 1791: VR-Sp §4),
  their centres and sills measured on ZAZ0101 (task 5). PB-039 gives the as-built fifteen at 12¾
  pies (3.56 m) centre to centre over 49.8 m (Res §2.4); the rebuild's added length is about one
  more room and space (judgement). Which pair is the sixteenth is not known (Res §10): **JUDGEMENT**
  the aftmost, so that her armed pairs are the lower deck's Nos. 1 to 15 and No. 16 an empty port
  (in the British fit armed); if the drawings show the new pair forward, the numbering keeps its gap
  wherever it falls (Bel-D §5.2: "a fit that leaves a place empty leaves a gap").
  **2026-11-20, measured and accepted (ruling 5):** on PB-039, **15 a side, 12.78 pies (3.56 m)
  apart, from x −24.66 to +25.18** (49.84 m), the research note's figure standing; **the sixteenth pair
  the aftmost, read on ZAZ0100**, where the lower tier's 16 ports stand each under one of the upper
  tier's 16, the aftmost included, as on PB-039 the upper tier has one port more aft than the lower
  (x −28.27). The JUDGEMENT becomes a reading; the numbering stands (lower Nos. 1 to 15 armed, No. 16
  the empty aftmost) (Pages §5.2, §11.3).
- **The middle and upper decks: sixteen a side**, the middle staggered between the lower and the
  upper, the upper over the lower and one more aft (PB-039, Res §2.4). **2026-11-20, measured:** the
  middle from x −26.46 to +26.97, the upper from −28.27 to +25.18 (PB-039); on ZAZ0100, 16, 16 and 16,
  the lower and upper port over port, 3.43 m apart, the middle staggered (Pages §5.2, §11.3).
- **The quarterdeck and forecastle**: six and three a side for the 1797 fit's 12 and 6 eight-
  pounders (VR-Sp §4); places from ZAZ0103 (task 6). **2026-11-20:** ZAZ0100 draws the quarterdeck's
  six a side at x −18.8 to −7.3 (2.30 m apart), the poop's three small ones at x −25.4, −23.4 and
  −21.4; no forecastle port could be made out at 1,280 px, and ZAZ0103's plans do not show the ports
  at that size (Pages §11.3): the forecastle's places not read. The 1809 fit's quarterdeck takes four
  eight-pounders and six obuses, its forecastle four and two: the same ports, the obuses on the
  ports nearest the ends (**JUDGEMENT**; the 74's 1812 rule, long guns in the wake of the shrouds,
  carronades elsewhere, Bel-D §5.1).
- **The poop's six obuses of 24** (1809): three places a side over the rail, as the 74's poop
  carronades (Bel-D §5.1), from ZAZ0103's poop if drawn.
- **The lower sills above her water**: not known (Res §2.6). Her water is set as the 74's was (Bel-D
  §2.2: the line where a reported clearance stands, else the drawn load line) by task 2, and the
  sills follow from the drawing. **2026-11-20, measured and accepted (ruling 5):** above PB-039's line,
  **1.91 m amidships** (the lowest 1.89 at x +3.78; 2.30 aft and 2.48 forward); the middle sills 4.29
  to 4.93 m, the upper 6.29 to 6.81 m; every triple in Pages §5.2. Above the line as traced the after
  sills stand a little higher (the aftmost lower about 0.11 m: Pages §12.1).

### 3.4 Port sizes

Measured by deck on ZAZ0101 (task 5). Interim, the 74's: lower 1.04 × 0.83 m, middle and upper the
74's upper 0.84 × 0.80, the upper works 0.79 × 0.71 (**JUDGEMENT**); the Spanish 36-pounder's port
is likely larger than the British 32's (judgement), so the lower's is measured first.
**2026-11-20, measured and accepted (ruling 5):** on PB-039, **lower 1.01 × 0.93 m, middle 0.91 ×
0.76 m, upper 0.80 × 0.67 m** (±1 cm; Pages §5.2), in place of the 74's 1.04 × 0.83 and 0.84 × 0.80;
the upper works' not measured.

### 3.5 Her measuring tasks (the Greenwich sheets read under the standing rule; the owner's choice of hull, Dec 10)

1. ZAZ0101's scale, and her length between the perpendiculars and on the lower deck (against
   Winfield's 61.30 and James's 59.21).
2. Her load line on ZAZ0101 (the drawn waterlines) and PB-039's two dashed lines identified; her
   water and draught to K.
3. Her displacement at her water by the sections (the 74's method, `Research-74-2026-10.md` §3.2.5).
4. Her rudder (area, span) and her lateral plane.
5. Every port's centre, sill and size on three tiers; the sixteenth lower pair's place.
6. The quarterdeck's, forecastle's and poop's ports and places on ZAZ0103 and ZAZ0100.
7. The decks' heights at the middle line (six decks), and her upper deck at midships for
   `deck_height_m`.
8. The stern: the counter, the galleries' tiers and the lights' bands (`galleries_m`, `lights_m`).
9. The masts' places at the partners (ZAZ0101's inboard; ZAZ0102's and ZAZ0103's decks).
10. PB-039 against ZAZ0101: the rebuild's change in length and in the stern, for her note.

**2026-11-20, done at step 1** (Pages §7): on PB-039 at full size, 2 (its part), 3, 4, 5 and 7, and 8
in part; on ZAZ0100 to ZAZ0103 at 1,280 px, 1, 9 and 10 (the length) coarsely, 5 and 6 counted, the
sixteenth pair read. Not done: 3 by ZAZ0101's sections, ZAZ0101's load line (2), its rudder (4), decks
(7) and stern measures (8), the forecastle's ports (6). With her hull PB-039's (the owner's choice),
ZAZ0101's are the comparison's, not hers.

---

## 4. The rig

**No Spanish source for her masts, yards or sails was read** (Res §5). Her rig is therefore Steel's
rule for the main mast on her own particulars and the 74's file's proportions scaled to it, every
figure marked; PB-078 (a 112's canvas, Romero Landa 1791) and any Spanish rule replace them when
read (§17 item 4).

### 4.1 The masts

| Mast | Length | Source |
|---|---|---|
| Main lower mast | **124 ft 3 in (37.87 m)** | Steel 1794 vol. I p. 39 (read (OCR)): half the lower deck and the extreme breadth, on James's 194 ft 3 in and 54 ft 3 in; **rule**, British. On Winfield's 61.30 m and James's breadth, 127 ft 2 in; the gun deck's length taken as Steel's "lower deck" (Res §5) |
| Fore lower mast, mizen lower mast, the topmasts, topgallant and royal masts | the 74's (*Dragon*'s list, Bel-D §4.1) × **1.150** (124.25 / 108) | **JUDGEMENT** until Steel's p. 39 fractions are read on the page image, which then rule |
| Mast places, heels and rakes | measured (task 9). **2026-11-20, measured and accepted (ruling 5):** PB-039's stumps above the rail, **mizen x −18.94, main −3.47, fore +23.37 m**, the main's step at −3.56; ZAZ0101's −19.07, −3.89 and +23.16 beside; the same spacing on ZAZ0102's middle deck (the partners) and ZAZ0103's decks, so upright within the reading; the rakes not read (Pages §5.7, §11.5) | A |

Each lower mast is stepped on the keel and stands through **three** decks; Steel's diameters are
"taken at the partners; which are at the middle deck in three-decked ships" (p. 49, read (OCR)).

### 4.2 Mast by mast: each spar and sail, and its class

As the 74's file (Bel-D §4), every length × 1.150 and every area × 1.32 (**JUDGEMENT**), the
heights from her own decks. The class is the engine's (`physics/sails.py`'s `SAIL_CLASSES`).

| Mast | Spars | Sails (class) |
|---|---|---|
| **Fore** | lower mast, topmast, topgallant mast, royal mast; fore yard, fore topsail yard, fore topgallant yard, fore royal yard; the lower, topmast and topgallant studding-sail booms a side | fore course (square), fore topsail (square), fore topgallant (square), fore royal (square, flying); fore staysail and fore topmast staysail (jibheaded); the lower, topmast and topgallant studding sails a side (studding); the fore storm staysail (jibheaded, in the sail room); the fore save-alls (studding, in the sail room) |
| **Main** | lower mast, topmast, topgallant mast, royal mast; main yard, main topsail yard, main topgallant yard, main royal yard; the topmast and topgallant studding-sail booms a side | main course (square), main topsail (square), main topgallant (square), main royal (square, flying); main staysail, main topmast staysail, middle staysail, main topgallant staysail (jibheaded); the topmast and topgallant studding sails a side (studding) |
| **Mizen** | lower mast, topmast, topgallant mast, royal mast; the mizen yard (`lateen_yard`), the crossjack yard (a dry yard for the topsail's sheets), mizen topsail yard, mizen topgallant yard, mizen royal yard | **mizen course (lateen, cut at the mast)**, mizen topsail (square), mizen topgallant (square), mizen royal (square, flying); mizen staysail and mizen topmast staysail (jibheaded); the mizen storm staysail and the storm mizen (jibheaded, in the sail room) |
| **Bowsprit** | bowsprit, jib boom, spritsail yard, sprit-topsail yard | jib (jibheaded); spritsail (square), sprit topsail (square), out of "plain sail" (D8 (b), Ext §4) |

- **The mizen course on its lateen yard** (B3.1, Ext §3): B3.1's whole-lateen handling, replaced in
  package 90 by the owner's answer to Dec 3, reaches only a whole lateen; hers is cut at the mast and
  lies against it as the 74's does. It is hauled aft at helm's a-lee and brailed up hove to,
  observed on the scratch file as on the 74 (Res §7). **Plainly:** whether a Spanish three-decker
  carried a lateen yard or a gaff in 1797 and in 1809 was not found; the lateen is the 74's of 1794
  and the machinery's (§17 item 4).
- **No driver.** The 74's driver boomsail is Steel's British sail, chosen by the owner for the
  British 74 (Bel-D §4.6); nothing gives it to a Spanish ship (judgement).
- **The schooner's-mast rule (B3.4)** leaves her a ship: every mast with yards carries a lower
  yard (her mizen's crossjack as the 74's), no after mast is a schooner's (observed here:
  `on_schooner_mast` false for all eight after yards). Its two classing limits (a lower square-sail
  yard on a schooner's main; a pole main with its topsail yard on the lower mast) do not reach her.
- **Groups and aliases**: the 74's, by name (`plain sail` the same eleven: courses, topsails,
  topgallants, the fore topmast staysail, the jib and the mizen course).

### 4.3 What the rig must still be given

The fore and mizen fractions from Steel's page; the yards by Steel's p. 40 proportions on her own
masts (the 74's file cites them); the sails cut by Steel's table IV, its largest column scaled
(judgement), checked against PB-078's sums when read; the ratings by her own areas; her brace
limits the 74's (no source for a first rate's: `Research-74-2026-10.md` §7.4's open item).

---

## 5. The guns (package 81's checklist, Build §6's postscript)

### 5.1 The fits

| Fit | Lower (36) | Middle (24) | Upper | Quarterdeck | Forecastle | Poop | Pieces | Broadside |
|---|---|---|---|---|---|---|---|---|
| **"concepcion 1797"** (default) | 30 | 32 | 32 × 12 | 12 × 8 | 6 × 8 | — | **112** | **1,188 libras (1,282 lb)** |
| **"concepcion 1809"** | 30 | 32 | 32 × 18 | 4 × 8, 6 × 48-pdr obús | 4 × 8, 2 × 48-pdr obús | 6 × 24-pdr obús | **116** | **1,508 libras (1,627 lb)** |

Source: Winfield p. 407 (via Winfield; VR-Sp §4). Each fit's half by calibre sums to the book's
broadside in libras exactly (observed here). **Plainly:** James's *San Josef* at her capture had 18s
on the second deck (vol. 2 p. 51); Winfield's 24s are taken, the book's own sum the check (Res §3.2).
Her default is the 1797 fit: the 1809 fit is a year's (her recommissioning, 1809 to her loss in
1810), the 1797 the class's long establishment (1793 to 1803) and St Vincent's.

**The ordinance of 1803, noted (2026-11-19;** Winfield et al. 2023, the table of the ordinance of
1803; VR-Sp §16). Its three-decker of 112 carries 30 × 36, 32 × 24 and 32 × 12 in her three
batteries; 4 × 8 and **8** × 48-pdr obuses on the quarterdeck; 4 × 8 and 2 × 48-pdr obuses on the
forecastle; 6 × 24-pdr obuses on the poop: **118 pieces**, the poop's obuses outside the nominal 112.
Its own note says she carried **18-pounders in her third battery**, as her 1809 fit has them. **Her
1809 fit stays her own record** (pp. 406-410), **116 pieces**, two 48-pounder obuses fewer on the
quarterdeck than the ordinance's 118; the ordinance is in the fit's note, not a fit. By its count
she was nominally 110 (computed).

**A third fit, booked:** "as the san josef 1801", the British first rate of 114 (ZAZ0101's "114-gun
First Rate"), with her sixteenth lower pair armed and James's 850 men (vol. 6 p. 407); for a
British scenario of 1801 to 1813, when the owner's passage of Winfield's British volume is read
(Res §11 item 4). Not drawn in this draft.

### 5.2 Places, numbers and the deck (checklist items 1 to 4)

- **Numbered by deck from forward**, each deck from No. 1 (B7.d as built): lower 1 to 15 armed
  (16 the empty sixteenth, §3.3), middle 1 to 16, upper 1 to 16, quarterdeck 1 to 6, forecastle 1 to
  3, poop 1 to 3. Ids `gun.<deck>.<n>.<side>`. A place keeps its number in both fits.
- **The deck word on every gun**: `lower`, `middle`, `upper`, `quarterdeck`, `forecastle`,
  `roundhouse` (the poop: `parts.DECK_SAID`, "the poop").
- **Checklist item 1**: `hull.profile` with `rail_m`, `breadth_m` and `decks_m` for all six decks.
- **Item 2**: `ports_m.<deck>`, a triple at every gun's own `x_m` (within 0.01 m), the sill her
  sheet's, the half-breadth her side's at the sill; the poop's places 2 in under the rail
  (`OVER_THE_RAIL_M`).
- **Item 3**: `port_size_m` for each of the six (§3.4).
- **Item 4**: every gun's `kind`, `pounder`, `place`, `side`, `x_m`, `weight_cwt` and `deck`.
- **Item 5**: `tools/check_viewer_guns.py data/ships/three-decker.yaml` clean, and the test. On the
  scratch file it is clean for both fits (observed here: 106 and 6, 104 and 12; Res §7).

### 5.3 The calibre, the weight and the crew

| Piece (libras) | `pounder`, by Dec 9's pick | The other way's English figure (Dec 9 (b)): old → **new, 2026-11-19** | Weight | Crew | Source |
|---|---|---|---|---|---|
| Long 36 | 36 | 38.85 → **36.57** | interim 66.8 → **62.9** cwt | 14 | the other way's figure the libra by Winfield's broadside pairs (1,308 / 1,212 = 1.079; Res §3.3), **JUDGEMENT**, until the book gives the English weight by calibre. **2026-11-19:** the book gives the libra itself, 0.4608 kg, 1.0159 English pounds (Winfield et al. 2023, pp. 41-46): one ratio for every calibre, the pairs' 1.079 kept as the book gives them and not used. The weight the English 32's 55 cwt scaled by the shot (judgement), now by 36.57 / 32; still interim, **the Spanish 36's weight to come from other research** (the period's Spanish artillery treatises, for example) **or JUDGEMENT**; the crew between Falconer's 13 for a 32 and 15 for a 42 (judgement) |
| Long 24 | 24 | 25.90 → **24.38** | interim 49.5 cwt | 11 | Adye's 24 of 9 ft 6 in (judgement on the pattern); Falconer's 24 |
| Long 18 (1809) | 18 | 19.43 → **18.29** | interim 42.0 cwt | 9 | Adye's 18 of 9 ft 6 in; Falconer's 18 |
| Long 12 (1797) | 12 | 12.95 → **12.19** | interim 34.0 cwt | 7 | Adye's 12 of 9 ft 6 in; Falconer's 12 |
| Long 8 | 8 | 8.63 → **8.13** | interim 24.5 cwt | 6 | Adye's 9 of 7 ft 6 in (the nearest); Falconer's 9 |
| Obús 48 (1809) | 48, as a carronade | 51.80 → **48.76** | interim 22.25 cwt | 4 | the English 42-pounder carronade's weight (Adye p. 72), the nearest; Douglas's carronade crew |
| Obús 24 (1809) | 24, as a carronade | 25.90 → **24.38** | interim 13.0 cwt | 4 | Adye's 24-pounder carronade |

**2026-11-19:** the weights by calibre are not in Winfield's passages (Dec Part D, G2). Every weight
above stays interim, a British pattern's or a scaled one's, until a Spanish source gives it (other
research: the period's Spanish artillery treatises, for example), or is ruled JUDGEMENT at her build.

- **The `pounder` rule** (the owner's, Dec 9; this draft's pick, the plan's §4 row 8): each gun
  filed by its calibre as her navy named it (`pounder: 36`), its note saying so ("a 36-pounder of
  the Spanish navy, 36 libras"), and the fit's note giving Winfield's broadside pair as the book
  gives it (1,188 libras, 1,282 lb; 1,508 libras, 1,627 lb), never a ratio drawn from it. Her
  broadside then reads a little light in the game's English pounds, and her notes say so: by about
  1.6 per cent, by the book's libra (2026-11-19).
  **Plainly:** the first draft filed each calibre by Winfield's broadside ratio (the third column),
  which re-derives the book's ratio per calibre, the thing the lead's rule asks not to be done; it is
  kept here only as the other way's figures, for the owner's eye, marked JUDGEMENT.
- **The weights** are the checklist's drawn lengths too (the pattern of nearest weight in Adye's
  tables, `check_viewer_guns` listing a weight more than a tenth off its pattern's). On the scratch
  file a long 36 of 65 cwt drew no such note (observed here), Adye having no 36; what length the
  viewer gives a Spanish 36 is to be read in `freesail/api/viewer_guns.py` before her file.
- **The crews** (one side's pairs): 552 men in 1797, 582 in 1809 (observed here).
- **Charges and the magazine**: Table No. 29 (SW-1) has no Spanish calibre; each charge a third of
  the shot's weight for the long guns and a twelfth for the obuses (**JUDGEMENT**, the period's
  common proportions, until Spanish figures are read); `g.fit_magazine` with the King's rounds;
  `exercise_allowance(n, decks=3)`.

### 5.4 The obús

Carried as a carronade of its calibre (decision 8), so that it loads, fights and is drawn by the
existing paths: its words "a 48-pounder obús", its note the reason. **Plainly:** a howitzer threw a
shell as well as a shot, and the engine has no shell; the 1809 fit's obuses fire round and grape
as a carronade does. The obús as its own kind (shell, its range) is a gunnery package's,
with the *Diana*'s 1817 obuses (Eng §6.3).

### 5.5 Orders and words by deck (observed here, Res §7)

The 74's B7.b and B7.d work on three decks today: "fire the starboard middle deck" (16 guns), "fire
No. 3 gun of the middle deck", "the middle deck's No. 16", "the gun deck" (the lower), a bare "fire
No. 3" refused naming her decks. Two things are hers to settle:
- **"The second deck" and "the third deck"** are James's own words for the middle and upper decks of
  the Spanish prizes (vol. 2 p. 51) and Falconer's "the second or middle deck" (DECKS): proposed as
  words for `middle` and `upper` on a ship of three gun decks (words only; on a two-decker "the
  second deck" would name the upper, judgement, and is left unbuilt there).
- **"The main deck"** names the upper deck today (Cumby's word on a 74, Bel-D §6.4 item 5). On a
  three-decker the word is ambiguous in the period; **proposed**: on a ship of three gun decks it is
  refused in words naming her three gun decks, as a bare number is (judgement; §17 item 5).

---

## 6. The company, her watches, the quarter bill by deck and the people file

### 6.1 The company: 839 in the second draft, by the regulations since 2026-11-19

*The second draft's split, kept for the record; the regulations below replace it.*

Winfield's 839 (VR-Sp §4; B). James's 917 at her sister's capture and the 850 of British service
in the note (Res §4). Not broken down in any source read, so the split is **JUDGEMENT**, set by what
the engine needs to man her guns:

| Part | Number | Basis |
|---|---|---|
| Posts | 18 | the 74's 16 with two more lieutenants, seven in all (judgement; Falconer's first rate has six; a Spanish flagship's second in command, the *segundo comandante*, among them) |
| Soldiers (`marines` station) | **100**, interim | **JUDGEMENT**, interim until Winfield's dotación by kind is read (Dec Part D, G3): the 74's 111 of 590 is 19%, and about 160 of 839 by that share (JUDGEMENT; no source breaks down her 839) left four of her crews unmanned (observed here), because the engine's marines never serve a long gun (Bel-D §6.3, as built). At 100, every crew of both fits is manned (observed here: 56 and 58 crews, the trimmers 105 and 103) |
| Idlers | 60 | the 74's 44 scaled (carpenter's crew 15, sailmaker's 5, cooper 2, armourer 4, cook 3, steward 4, servants 19, surgeon's mates 3, clerks 3, master-at-arms's party 2) |
| Seamen | 661 | the rest, in the 74's six stations by her shares |

**Plainly:** the Spanish practice of putting soldiers at the guns (judgement on general knowledge,
no source read) is met here by counting fewer of her people as marines, not by changing the engine's
rule; Winfield's breakdown (Res §11 item 2) replaces the split.

**Revised 2026-11-19: her company by the regulations** (Winfield et al. 2023, p. 1446 and the two
pages following, for 1 January 1788; the table of the Regulation of 16 October 1803; rung B; VR-Sp
§15). A 112 by kind ("All" computed: the book's Total leaves out the commissioned and the major
officers):

| Kind | 1788, the 1797 fit | 1803, the 1809 fit |
|---|---|---|
| Commissioned officers | 19: a brigadier (her captain), a capitán de navío (her second), a capitán de fragata, 4 tenientes de navío, 4 tenientes de fragata, 4 alféreces de navío, 4 alféreces de fragata | 19, the same |
| Major officers (purser, chaplain, surgeons, pilots) | 10 | 14 |
| Sea officers (boatswains, guardians, caulkers, carpenters, cooks, divers, armourers, lamp men, sailing masters, quartermasters) | 23 | 37 |
| **Infantry** | **168** | **200** |
| **Infantry-artillery** | **57** | **75** |
| Artillery | 130 | 190 |
| Seamen | 200 | 240 |
| Landsmen | 230 | 200 |
| Boys | 40 | 40 |
| The book's Total | 848 | 982 |
| **All** | **877** | **1,015** |
| **Her soldiers** (infantry and infantry-artillery) | **225** | **275** |

**What is filed**, old beside new:
- **The company: 839 → 877**, the file's, the 1797 default's by the 1788 regulation (its
  establishment for peace, as printed). Her own 839 (pp. 406-410, unbroken) goes in the note: 4 per
  cent under, and within nine of the book's Total of 848 without the officers (whether her 839 is
  counted on that basis her entry does not say). Truth 7-NNN-a records both (§14).
- **The soldiers: about 100 (interim JUDGEMENT) → 225**, her infantry and infantry-artillery, the
  `marines` station.
- **The 1809 fit: 1,015, of whom 275 soldiers**, by the 1803 regulation, **recorded as a departure in
  the fit's note**, a company being the file's and not a fit's (the lead's ruling (5) of 2026-11-07),
  as the polacre's corsair's 80 at 71 and the xebec's regency's 150 at 113 are. **For the lead:** or a
  second file of the same hull for the 1809 fit, `three-decker-1809.yaml`, with its own company
  (the polacre's road). The pick: the departure (JUDGEMENT: one hull, one file, as Dec 8 settled).
- **The war increase is not filed.** The 1788 complements were for peace; in war a ship gained as
  many men as guns in her main batteries, half infantry and half landsmen, and more surgeons. For
  her, 907 if her main batteries are her lower deck's 30 guns, 971 if they are her three gun decks'
  94, the book calling a gun deck a "battery" in the ordinance of 1803 (computed); James's 917 for
  her sister at her capture (Res §4) lies nearest the first. Which reading, and whether St Vincent's
  fit takes it, is the lead's (JUDGEMENT on the road: the printed establishment filed meanwhile).
- **The split onto the game's stations** at her build (JUDGEMENT, the 74's form, the regulation's
  kinds its check): her posts from the commissioned officers and the chiefs of the major and sea
  officers; her idlers from the rest of them (the carpenters, caulkers, armourers, cooks, lamp men,
  the surgeons' and the purser's people); her seamen from the artillery, the seamen, the landsmen and
  the boys, in the 74's six stations by her shares.

**What it does in the engine, to be measured.** Her soldiers stand in the `marines` station, and the
engine's marines serve carronades and never a long gun (Bel-D §6.3, as built). The second draft's
own run left four crews of the 1797 fit empty at 160 soldiers of 839, leaving 679 others (observed
here); at 225 of 877 the others are 652 (computed), fewer still, so **crews are likely to stand
empty** in both fits (in 1809 the obuses, carronades to the engine, take 28 of the soldiers).
Measured on her file at her build, by deck, both fits. **If crews stand empty, it goes to the lead at
its cause** (the owner's rule of 14 November): the engine's rule that soldiers serve no long gun,
which any Spanish or French ship of the line meets (§19), and Dec 8's other way, her soldiers at the
long guns: at least her infantry-artillery, the artillery's own soldiers, or all of them, for her
alone or for every ship that carries them. Not built in this card without the lead's word.

### 6.2 Her watches

Two, starboard and larboard, as every King's ship of the game (judgement; no Spanish source read).
**Package 75's ruling 11** (a merchantman's master and mate counted as hands of their own watch
where the watch is too few) does not reach her: she is a King's ship. Her watches are each over
three hundred, so no evolution of the game wants all hands for want of a watch (package 116's `too_few:
all hands` on `let_go_anchor` never bites).

### 6.3 The quarter bill (against the default fit) and the bill by deck

- **The bill**: trimmers by station as the 74's scaled to her seamen; the helm **4** (two wheels'
  men on a first rate, judgement); the powder 42; small arms 60; boarders 140; the bill's `marines`
  **60** (the small-arms party on the poop and quarterdeck). Observed here: in the 1797 fit, with no carronade, all 100 soldiers stand in their division (the engine's marines serve no long gun); in 1809 the obuses take 28 of them and 72 stand. **2026-11-19:** with the regulation's 225 soldiers (§6.1), all 225 stand in their division in 1797, the small arms among them, and 197 in 1809, the obuses taking 28 (computed on the same rule); the bill's other stations shrink with the 652 others, measured at her build.
- **The beat by deck** (B7.b, observed here): "The lower deck: 15 gun crews ... The middle deck: 16
  gun crews ... The upper deck: 16 gun crews ... The quarterdeck: six gun crews ... The forecastle:
  three gun crews ...", the poop's in 1809.
- **Robbing by deck** (B7.b item 4): the lower deck's crews behind shut ports first, then "the other
  decks" from the end that bears least, the lower deck's last (observed here). **Proposed, for the
  lead** (it reaches `crew/quarters.py`, the 74's code): on a ship of three gun decks, the upper
  deck's crews before the middle deck's (the lighter metal first, as the 74's reason for the lower
  deck's last: judgement), and a middle deck's crews behind shut ports with the lower's (at 30° on
  the scratch sills the middle deck's ports shut and its crews are not counted shut: observed here).
  Neither moves the 74 or the 64 (keyed on a `middle` deck).

### 6.4 The officers by deck (her people file)

After the 74's (Bel-D §6.5), by the 1795 deck plan's cabins (the admiral's on the *toldilla*, the
captain's and lieutenants' on the *alcázar*: PB_0050 via Winfield p. 409): the captain, the captain's second
and the master on the quarterdeck; two lieutenants a gun deck, the senior at the after guns and the
junior at the foremost; the forecastle under the boatswain; the poop's small arms under an officer
of the soldiers. In her people file's briefs; no engine key.

### 6.5 The flag

A flagship through most of her service (Córdova's, Lángara's, Mazarredo's, Morales de los Ríos's:
VR-Sp §4). The flag and its party are the scenario's `people:`, not her file's (Bel-D §6.6).

### 6.6 The people file

`data/people/three-decker.yaml`, hand-written: her posts' people in Spanish names (a Spanish list in
`data/crew/names.yaml` first, shared with the *Diana*), her officers' briefs by deck (§6.4). Her
`crew.names` key names the list.

---

## 7. Ground tackle, boats, pumps, hold and stores

All **JUDGEMENT** on the 74's file scaled to a first rate until Spanish figures are read: Steel's
anchor and cable table's 100-gun row where the OCR gives it (`period.STEEL_ANCHORS` holds the 64's
and the 74's; hers appended); the 74's six boats with a second launch (judgement); four chain pumps
and two hand pumps (the 74's); water and provisions scaled to 839 for 120 days (the 74's days); to
her 877 since 2026-11-19 (§6.1).
Ibargüen's plans of 1785 (Res §0.2) show the Spanish navy's wheel and its machinery: her wheel is
the game's wheel, and package 116's `relieving_tackles` and `repair_wheel` stand for her as filed
(observed here: the tackles in 380 s, the wheel repaired in 2,279 s, the 74's 385 and 2,310 s). **For
the lead:** six hands at a first rate's tiller by the tackles is the frigate's judgement; a first
rate's heavier tiller may want eight (judgement); her file could carry a timing of its own as the
74's carries `lie_a_try`'s.

---

## 8. Far description, vessel type, size rank and her words

### 8.1 What is made out, and when (package 75's made-out rule)

- **At the rig's distance** (`RIG_MADE_OUT_NM`, 4 nm): the tops make out **"a three-decker"**. A
  ship of the line is made out as such there by her size and her tiers (the lead's ruling 17 of
  2026-11-12); a three-decker's three tiers and her height are what the logs of the period record at
  first sight of a fleet ("another First-rate", Nelson's narrative, Nicolas vol. 2 p. 341)
  (judgement on the distance, as the 74's).
- **How she is rigged**: "a ship" (`RIGGED_AS["a three-decker"] = "a ship"`), so that her hail, her
  sails aback lying to, and every reader of rigging read her as a ship.
- **The glass** (`MADE_OUT_NM` × `GLASS_FACTOR`): **"a three-decker, sixteen ports a tier"** (her
  three tiers of sixteen as rebuilt). Her colours at `COLOURS_MADE_OUT_NM` (2 nm), as every ship's.
- **Not** "a first rate" in what is made out: a rate is a navy's book, not a sight (judgement); "a
  first rate" names her description in a scenario's words.

### 8.2 Her rows (in `freesail/world/ships.py` and `world/captains.py`, her window)

- `DESCRIPTIONS["three-decker"] = {"file": "data/ships/three-decker.yaml", "rig": "a three-decker",
  "what": "a three-decker, sixteen ports a tier"}`, and the file's own `ship.descriptions` with her
  fit and roles (`kings-ship`, `commodore`).
- `_DESCRIPTION_WORDS`: "a three-decker", "three-decker", "a first rate", "a first-rate", "a
  hundred-and-twelve", "a 112", "a ship of the line of three decks" to `three-decker`. "A ship of the
  line" stays the 74's.
- `SIZE_RANK["three-decker"]` and `_SIZE_WORDS`: ("three-decker", 5) before ("ship of the line", 4).
  Today "a three-decker" ranks nothing and is "a sail" (observed here).
- `RIGGED_AS["a three-decker"] = "a ship"`.

### 8.3 Her rank and what it does (observed in the code, `world/captains.py`)

- A lone frigate (rank 3) hauls off from her as from a 74 (`LINE_OF_BATTLE_RANK` 4, `_overmatched`).
- A cruiser or privateer (`stranger_hostile_nm` 6) hauls off from any bigger class: from a 74 and
  from her alike at rank 5.
- A King's 74 (rank 4, `stranger_hostile_nm` 0) does not haul off from her: the King's ship's book
  hauls off from no ship of her own class or under and leaves bigger ones to her judgement. Whether
  a lone 74 should avoid a three-decker is the owner's (§17 item 1).

---

## 9. How the engine sails her today, and what it must be given (observed here)

The scratch file (Res §7): the 74's rig scaled 1.06, 59.2 m, 4,200 t. And the design's rig
(`v_design.yaml`): the 74's rig scaled **1.15** by Steel's rule, 61.3 m, hull speed 13.1.

| Measure | 74 | Scratch (1.06) | Design rig (1.15) | Frigate-36 | What she must be given |
|---|---|---|---|---|---|
| Static polar, 15 kn abeam | 7.87 kn | 7.50 | **8.01** | 8.19 | the design rig puts her between the 74 and the frigate, as Brenton and James have her (Res §6); band in 7-NNN-d |
| Close-hauled 67.5° off, 15 kn | 4.92 kn, 3.6° | 4.75 kn, 2.7° | 4.92 kn, 3.4° | | her GM tuned so that she heels no more than the 74 (a broad ship) |
| The tack, truth 10's form (290, 292.5, 295°) | 237, 243, 258 s | 181, 184, 188 | 182, 230, 189 | 343, 447, 370 | **quicker than the 74's**: neither her company (590 the same as 839) nor her displacement (5,167 t the same) slows it; the 74's rudder adds 15 s. Her rudder from ZAZ0101 and her helm's lead tuned to a tack no quicker than the 74's, inside Luce's five to ten minutes (the lead's (1) of 2026-11-07) |
| The wear | 499 s | 498 | | 513 | as the 74's (truth 11's band) |
| Hove to | ≤ 1.18 kn, 56.5 to 63.4° | ≤ 1.39 kn, 55 to 64° | | | as the 74's |
| Classing | a ship | a ship | | | nothing |
| Pace, alone (truth 51's form) | 408, 387 | 386, 371 | | | 0.95 of the 74's; the alone clause is no truth since the lead removed 7-196's |
| Pace, three crewed (truth 7-196's world, Eng §7) | 79, 81 | 72, 75 (the engine note's three-decker probe) | | | about 0.92 of three 74s, over the floor of 60; the lead measures on the build machine. Her own p5c.py (68 against 71, 0.96) ran a world of its own, three of the file added as patrolling vessels off the Lizard, one of which stood off after the first thousand: recorded, not the truth's measure |
| Checkpoint at quarters | 168 KB gz (637 KB raw) | 174 KB (688 KB) | | | under 2 MB |

**The tack.** A first rate staying faster than a 74 contradicts every period expectation of a great
ship (judgement: no source on her own time in stays was found). The cause in the engine is her
rudder and her helm's lead scaled with her, not her mass: the yaw's inertia scales with her
displacement and length (`physics/hull.py`, `yaw_inertia`) but the tack is governed by the
evolution's phases and the swing's damping (observed: 4,200 and 5,167 t tack within a second of each
other). Her builder tunes `clr_x_m` and the rudder to the band of 7-NNN-d, and says if no setting
holds both the helm and the tack (as the 74's builder did).

---

## 10. The lee ports

The rule (package 70; Build §7) reads her sills by deck from her profile; it shuts her lower ports
first and her middle deck's at a greater heel (observed here on the scratch file's 74 sills: 11
lower at 12.5°, all 15 at 18°, the middle deck's first eight at 30°). Her own sills wait on task 2
and 5. James's general word that foreign-built ships carried their lower battery "higher from the
water" (vol. 1 p. 29) is the period's expectation; a truth on her shut heel waits on her measured
sill.

**2026-11-20, measured and accepted (ruling 5):** on her own plan **the midship lee port dips at
13.3°** (the sill's z over its half-breadth, this rule's), the lowest (lower No. 9 at x +3.78) at
13.3°, the aftmost at 18.7°, the foremost at 22.1° (Pages §5.2, computed). Against the 74's 1.57 m
sill at a moulded half-breadth of 6.93 m (Research-74 §3.2.4; 7.04 m outside the plank in the 74's
file), about 12.8° (12.6° on the file's: computed): her sill stands 0.34 m higher from the water, as
James says of Spanish ships, but her greater breadth keeps the angle within a degree of the 74's
(judgement). The midship ports stand forward of where the line as traced leaves the straight fit, so
the 13.3° holds on either (Pages §12.1). Truth 7-NNN-c may now be drafted on it.

---

## 11. Where she sails

| Scenario | Fit | The chart | The shelf's sentence (package 96, `client/harbour-shelves.yaml`, Actions) |
|---|---|---|---|
| **Cape St Vincent, 14 February 1797** (the first) | 1797 | `atlantic-east`, the `portugal` block's Cape St Vincent | "The Spanish three-decker *Purísima Concepción*, flagship of the second in command, off Cape St Vincent on 14 February 1797 with Jervis's fifteen sail of the line in sight." |
| Cádiz Bay, 7 March 1810 | 1809 | Cádiz and its bay | "The *Purísima Concepción* at anchor in Cádiz Bay as the storm of 7 March 1810 comes on, the French on the shore to leeward." |
| Brest, 1799 to 1802; Toulon, 1793 | 1797 | `biscay-north`; Toulon | booked |

- **The nations.** `data/nations.yaml`'s wars are one year's picture (Britain at war with Spain from
  12 December 1804): right in kind for 1797, wrong for 1810, when Spain was Britain's ally; the
  Cádiz scenario wants the table's dated wars or a scenario's own stance (for the lead; not hers).
- **Her signals**: Spain's own book (Mazarredo's, package 76).
- **The other side at St Vincent**: the game's 74 under British colours and the frigate; no British
  first rate exists (the *Victory*), so a scenario of the fleets would be a later package's.
- **The wheel at St Vincent**: the *Captain*'s wheel was shot away before Nelson boarded (Nicolas
  vol. 2 p. 341): the scenario's British 74 meets package 116's evolution in its own history.

---

## 12. Fits and roles

- **Her trade**: none; a King's ship of the Spanish navy (her file carries no nation; the scenario's).
- **Roles**: `kings-ship` (a ship of the line on her own) and `commodore` (a flagship leading a
  squadron), as the 74's, read from `data/captains/` by the first (`brains.INTENT_RULED_ROWS`,
  Build §8). The regency's cruiser's doctrine (package 116's road, `thresholds:`) is not hers.
- **Fits**: §5.1; the British "as the san josef 1801" booked.

---

## 13. What the viewer must draw

From her profile alone, by the rules the viewer already has (Eng §11: three tiers are drawn as two
are; `galleries_m` takes any number of tiers):
- **Three tiers of ports**, sixteen a side, the lower's sixteenth shut and empty in her Spanish fits;
  the lids; the guns in them by package 81's rule.
- **Her height**: three gun decks under a quarterdeck and forecastle with an open waist and its
  gangways, and the poop; her rail's steps at each.
- **The stern**: square, two closed tiers of quarter galleries and a third of lights above, the
  stern's lights in tiers (PB-039; ZAZ0101's sternboard). **2026-11-20, measured on the quarter and
  accepted (ruling 5):** the lights at z 4.80 to 5.92, 7.39 to 7.95 and 9.39 to 9.92 m; the lowest
  gallery's drop to 2.45 m; the taffrail's top 11.84 m at x −33.2 (Pages §5.5); the stern board itself
  (ZAZ0101) not read.
- **The head**: a beakhead with its rails and a figure (PB-039; ZAZ0101's figurehead).
- **The channels** above the upper tier, their chain plates down across it (PB-039).
- **The mizen's lateen yard** and its course cut at the mast (the 74's drawing, Ext §6.1); the
  spritsail yards (Ext §6.2).
- **The words for a port** in `client/projection.js` (Eng §6.2: "upper-deck port" and the bare word
  for any other): "a middle-deck port" for hers, by the log's "-deck" form (words only).
- **Paint and carving** in words where ZAZ0100's colours are read (the British paint of 1799, not the
  Spanish), else nothing invented (§5.0 principle 9).

---

## 14. Truths proposed (numbered by the lead at the scope card)

**2026-11-20:** her range is **7-735 to 7-739** (`Plan-Package90.md` §10.3, by the lead's nudge
30); the letters stand until her builder numbers them.

| Truth | What it holds | Form |
|---|---|---|
| **7-NNN-a, her particulars hold their sources** | her length and breadth Winfield's and James's within the rounding; three gun decks with 16 ports a side each; her two fits 112 and 116 pieces whose halves sum to 1,188 and 1,508 libras; 839 men. **2026-11-19:** 877 men by the 1788 regulation, of whom 225 soldiers; the 1809 fit's note giving the 1803 regulation's 1,015 and 275, and her own 839. **2026-11-20:** her length PB-039's 61.26 m (Winfield's 61.30 beside it, within 0.1%), her displacement her drawn body's (about 4,440 t) with Winfield's 5,167 t in the record | the 74's 7-194 form |
| **7-NNN-b, three gun decks at quarters** | the beat says the lower, middle and upper decks' crews in order; every crew of the default fit manned (2026-11-19: with the regulation's soldiers, as measured; if crews stand empty, the clause waits on the lead's word, §6.1); "fire the starboard middle deck" names sixteen guns; a bare number refused naming her decks | B7.b and B7.d on three decks |
| **7-NNN-c, her lower ports shut at the heel her sources give** | after tasks 2 and 5. **2026-11-20:** measured, the midship lee port at 13.3° (§10) | the 74's 7-195 form |
| **7-NNN-d, she sails as a fast first rate** | her best speed in 15 kn at least the 74's and no more than the frigate's; her tack from truth 10's three headings no quicker than the 74's and inside 600 s; she wears and lies to as the 74 | Brenton via Winfield; James vol. 6 pp. 3 to 4; Luce |
| **7-NNN-e, three of her crewed hold the floor** | the frigate off the Lizard with three of her crewed over `CREWED_FLOOR_TICKS_S` | the 74's 7-196, marked pace |

---

## 15. Pins her work could move

None of another ship's by her file. Her rows in `world/ships.py` and `world/captains.py` add words
and a rank; no existing description's words change ("a ship of the line" stays the 74's). The words
"second deck" and "third deck" add orders where there were none. The robbing order proposed in
§6.3 is keyed on a `middle` deck, which no file but hers has. The checks of every new attribute as a
plain class default, and every existing file byte for byte, as Build §14.2.

---

## 16. Risks, ranked

1. **Her lines unread.** Until ZAZ0101 to ZAZ0103 are read at step 1 (and if the owner chooses
   PB-039 alone, Dec 10), her hull is PB-039's stand-in (§3.2), her sills and water judged, and truth
   7-NNN-c waits. **2026-11-20: met.** PB-039 measured at full size and chosen by the owner; her sills
   and water measured; the Greenwich sheets read only at 1,280 px (no larger free image), her
   comparison. What stays: whether the sheet or its photograph bends her waterlines aft (Pages §12.1).
2. **Her tack and her helm.** The engine's tack does not slow with size (§9); if no rudder and lead
   hold both the 74's helm and a tack no quicker than the 74's, the band is the lead's to set.
3. **Her company's split** is set by the engine's rule that marines serve no long gun; Winfield's
   breakdown may say she carried more soldiers than her bill can use. **2026-11-19: it does** (225
   in 1797, 275 in 1809: §6.1); measured at her build, and the lead's at its cause if crews stand
   empty.
4. **The Spanish pound and the guns' weights** stand on one ratio until a passage gives them by
   calibre; every gun's figure moves together when it does. **2026-11-19:** the libra is the book's
   (one ratio, 1.0159); the weights by calibre are not in the passages, and stay interim until other
   research gives them or they are ruled JUDGEMENT.
5. **The displacement** (4,200 against 5,167 t) moves her heel, her way and her pace a little; her
   handling and tack not (observed). **2026-11-20:** ruled, about 4,440 t, her drawn body; Winfield's
   5,167 t, about 4,762 t as toneladas, recorded beside it (§2).

---

## 17. Open for the owner (few and plain; my pick first)

1. **Her rank.** (a) **A class above the 74 (rank 5)**: a lone frigate and every cruiser keep away
   from her as from a 74, and a lone King's 74 does not avoid her of itself (my pick; a 74's captain
   meeting a three-decker alone is a judgement the game leaves to that captain). (b) The 74's rank, 4: every
   ship of the line one class.
2. **Her sources.** (a) **Hold PB-039** (her own plan, CC BY 4.0, credited as the *Diana*'s) in
   `docs/references/images/`, **and draw her hull from her sister's lines as rebuilt, ZAZ0101 to
   ZAZ0103**, measured on Greenwich's site under the standing rule (read and cited by number, never
   copied, as *Minorca*'s are for the xebec) (my pick); (b) PB-039 alone, her hull scaled from her as
   built. (Viewing the sheets needs no permission; the choice is which hull is hers, and so it is
   the owner's: Dec 10 question 2.) *Answered 2026-11-18 as picked (a); answered again 2026-11-20*,
   put as "Draw her hull from PB-039 instead?": "Use PB-039 (Recommended)". Her hull is drawn from
   PB-039, her own plan as built; the *San Josef*'s sheets stay as the comparison, and settle her
   sixteenth lower pair, the aftmost (Dec Part F).
3. **Her soldiers at the guns.** (a) **Count about a hundred of her 839 as soldiers and the rest as
   seamen, so that every gun is manned** (my pick, interim until Winfield's dotación by kind, G3, is
   read); (b) about 160 soldiers by the 74's share (JUDGEMENT: Winfield gives the 839 unbroken), with
   the engine's rule changed so that her marines serve long guns on her bill (a change to the 74's
   rule, for her alone). *Answered 2026-11-18 as picked (a), interim; G3 read 2026-11-19:* her
   soldiers are the regulations' (225 and 275, §6.1). If they leave crews empty, (b)'s change comes
   back to the lead at its cause, with her build's measure.
4. **Her rig.** (a) **Steel's rule and the 74's proportions scaled, a lateen mizen and no driver,
   until a Spanish source is read** (my pick); (b) wait for a Spanish rule before her file.
5. **"The main deck" on a three-decker.** (a) **Refused in words naming her three gun decks, with
   "the second deck" and "the third deck" added** (my pick); (b) "the main deck" the upper deck, as
   on the 74.

Picture for the questions (side by side, words): her profile as PB-039 draws it (three tiers of 15,
16 and 16, a beakhead, two tiers of quarter galleries) beside the 74's file as drawn today (two tiers
of fourteen): for question 1, what the tops see at four miles.

---

## 18. For the lead

1. **The images README** says J1945 is "as taken in 1797"; Greenwich dates it 1799 (ZAZ0100, the
   fitting at Plymouth). The lines are ZAZ0101 (J1950) (Res §2.3).
2. **Winfield's two figures** that disagree with the foot (the keel, the rebuilt length; Res §2.1),
   for the owner's re-reading with the passages of Res §11. *2026-11-19:* the class's pages were not
   sent; at the book's own pie (278.635 mm) the keel's 190 pies 10 pulgadas are 53.17 m and the
   rebuilt 220 pies 6 pulgadas 61.44 m (computed), against the printed 53.12 and 61.30. The printed
   metres stand by the lead's rule; the difference is recorded, not resolved.
2a. **2026-11-19: her soldiers at the long guns** if her build finds crews empty with the
   regulations' 225 and 275 (§6.1): the engine's marines' rule at its cause, or her infantry-artillery
   alone at the guns. And whether the 1809 fit's company is a departure recorded or a second file.
3. **The robbing order on three decks** (§6.3), keyed on a `middle` deck: the 74's code, which the
   plan gives her builder as A9 (Plan §6, §7.1).
4. **The relieving tackles' hands on a first rate** (§7).
5. **The nations table's one year** for a scenario of 1810 (§11).
6. **A Spanish names list**, shared with the *Diana* (§6.6): the plan's N1, from the *Diana*'s
   builder.
7. **2026-11-20: `deck_height_m`** (ruling 4's condition, checked: §2; Pages §5.3). The same deck by
   its place as the 74's and the 64's, not the same method in the line taken as the deck's surface:
   6.06 m by Pages' line (the upper of PB-039's pair), 6.00 to 6.01 m by the 74's (the pair's mean);
   5.98 to 6.05 m above the line as traced. Not filed until the lead's word.
8. **2026-11-20: her `draught_m` on a bent line.** The line as traced is straight forward of about x
   −5 m and nearly parallel to the keel aft of it, so its middle (7.94 m to K) and the mean of its two
   ends (7.84 m) part by 0.10 m. The middle is taken, where the file's frame is set (JUDGEMENT; Pages
   §4.2, §12.1). And the frame's heights follow the line as traced at their stations, up to 0.15 m at
   the post's after face (Pages §12.1, JUDGEMENT on what ruling 2 asks).
9. **2026-11-20: her length's convention**, as the *Diana*'s §17.2 item 8: D29 (b) files the drawn
   hulls' length rabbet to rabbet at the load line; hers is PB-039's post to stem by ruling 3. Her
   length between the rabbets on her line is not measured (60.06 m at the lower deck).
10. **2026-11-20: the breadth's factor** of the old stand-in rule (16.25 / 16.16), not named by ruling
   3: taken as drawn, unscaled (JUDGEMENT; §3.2).

---

## 19. Found on the way

- **PB-039 at full resolution** (12,932 × 4,574 px) on the Biblioteca Virtual de Defensa, CC BY 4.0
  (**2026-11-20:** served as a one-page PDF by the record's second image group, 356204; the sheet holds
  a full body plan of ten after and eight fore sections with five diagonals, and a half-breadth plan
  under the sheer, not only a section: Pages §1.1, §1.3),
  with four sister-type sheets of the 112s (PB-049, PB-078, PB-344, PB-060) and Ibargüen's wheel
  of 1785, all from the Archivo Histórico de la Armada (Res §0.2): the same library and licence as
  the *Diana*'s PB-021; the other hulls' documents may find their own plans there.
- **The marines' rule** (they serve carronades and never long guns: Bel-D §6.3 as built) is what
  leaves a ship with a large body of soldiers unable to man her guns; any later ship with soldiers
  at the guns (a Spanish or French ship of the line) meets it too.
- **The tack does not slow with displacement** in the engine (§9): a later great ship meets the
  same, and a truth for "a first rate stays slowly" would need it said.
- **"A ship of the line of three decks"** ranks 4 through "ship of the line" today, and names no
  description (observed here).
