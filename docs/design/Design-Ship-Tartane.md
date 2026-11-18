# Design: the tartane, a Provençal coaster under a great lateen and a square topsail (package 90, third draft)

**Third draft, 2026-11-18, on the owner's answer to question 3** (the decisions sheet,
`Decisions-Package90-2026-11.md` §3 and Part F; the lead's note of 2026-11-18, 04:30 UTC, nudge
17). The owner agreed the sheet's other nine questions as picked, so this design's questions 1 and
3 to 6 stand as picked (§16.1). On going about they gave their own shape: she tacks and wears as
other vessels do, each an ordered evolution, and changing the yard round the mast is "preferred
but not necessary". No source read says a lateen vessel could not tack
(`Research-LateenGoingAbout-2026-11.md`, **GA**). This draft re-drafts what concerns her going
about, and nothing else:
- the one sentence and decision 13;
- §0's engine steps and §5.3;
- §5.4 items 1 to 5, and a new item 11;
- §6.1's all-hands work and §10 item 2;
- truths T-3 and T-4, and a new T-9;
- §16.

It takes the engine note's third draft (`Design-Package90-Engine.md` §2.2a, §2.3, §2.4, §14: A1a
to A1d).

The design for the first and smallest hull of package 90, decision 11's third reference vessel.
**This is the second of two drafts (2026-11-18)** (`docs/design/Plan-ShipsWorkflow.md`, Phase 3;
package 90's row). It answers the critic's reading of the first draft item by item ("How this draft
answers the critic", below the decisions), takes the settlements of package 90's plan
(`docs/design/Plan-Package90.md` §4) and cites the plan's step names (§6 there: A1 the whole lateen,
A1a to A1d since the third draft, A3 a tiller's words, A4 the boat in tow, A5 and A6 a yard's level
and the pole mast, A8 the lateen in a gale, V1 to V3 the viewer's) in place of the first draft's
numbered items. The lead's scope card for the build follows the owner's answers. It follows the
bilander's and the *Bellerophon*'s designs in shape: what binds, the decisions proposed, the hull,
the rig mast by mast, how the engine sails her today (run, not guessed) and what it must be given,
her company, her guns and ports, her fits and roles, her words, what the viewer must draw, her
truths, and the owner's questions with this draft's pick first. **Nothing here is built**, and no
tracked file in the tree but the package's new documents is changed: no code, no ship file, no
generator, no scenario, no test (the lead's note of 2026-11-18, nudge 15).

**What binds, in order:**
1. The lead's note of 2026-11-18, 00:50 UTC (nudge 15): research and planning only, on
   the package's branch; the build waits for a scope card agreed with the owner
   (`docs/dev/ScopeCards-BeforeTheGate.md`, "How a package runs, as amended by the owner on
   2026-11-16"). Its item 8 is settled for her here (§5.3); its item 37 is reported for her (§1).
2. Package 90's row (`docs/dev/M7-WorkPackages.md` l. 72) and the lead's notes of 2026-10-29,
   2026-11-06 (18:00 and later) to the ships session: the tartane of decision 11, a trader's and a
   fisherman's fits first, the coastguard a role; B3.1's lateen handling, "worn, not tacked; the
   yard dipped round the mast", **replaced by the owner's answer to question 3** (2026-11-18,
   Dec Part F: tacked and worn, the yard changed or left); B3.4's schooner's-mast rule, by which
   she classes as the cutter.
3. `docs/DesignProposal.md` decision 11 (her rig, settled by the owner on 2026-11-06) and decision 56
   (package 90 widened; the count of hulls).
4. `docs/design/Build-Ships.md`: §5.0's principles and its ladder; §6's postscript, package 81's
   checklist for her guns to be drawn; §8 (fits and roles); §13.3's form for what a design settles.
5. Her research note, `docs/design/Research-Tartane-2026-11.md` (cited **Tar**), and the notes it
   cites: `VesselReferences-2026-11-Spanish.md` §1 (Winfield, the lead's words), `VesselReferences-
   2026-10.md` §3.1 (Chapman, Fincham).
6. `docs/design/Design-ShipsEngineExtensions.md` (cited **Ext**): §3 (the lateen class; §3.7, "the
   full lateen kept possible"), §5 (the settee, whose dip is the nearest machinery), §6 (the
   drawing).
7. Package 75's rulings as merged: ruling 11 (a merchantman's master and mate as working hands,
   the narrower form); the made-out rule (Phase 5, `Build-Ships.md` §16.1's row); B3.4's four
   rulings (`docs/dev/TuningNotes.md`, "The schooner's mast"). Package 116 (the anchor's `too_few:
   all hands`; the wheel shot away; `repair the wheel`; the doctrine read from `thresholds:`).
   Package 96 (`client/harbour-shelves.yaml`, a sentence a scenario).
8. Pictures for the eye only: the Roux-school watercolour held
   (`docs/references/images/tartane-roux-school-watercolour.webp`); Monleón's print (Winfield
   p. 1249), cited, not seen.

**Marks.** As her note's: *read (page image)*, *read (OCR)*, *read there*, *the lead's words*,
*secondary*, *seen*, *observed* (printed by this package's scratch probes,
`scratchpad/p90/tartane/probe_tartane.py` and `probe_cutter.py`, run with `py` from the scratch
folder, `D:/Projects/FreeSail/FreeSail-pkg-90` first on `sys.path`, `freesail.__file__` asserted
under it; the scripts are not filed; every knot they print is headway, `dyn.u`, where truth 12 reads
the speed, `dyn.speed`, a little more: a figure by truth 12's measure is marked so), *read here* (code or data of the tree at 68e769ef read for
this draft), **JUDGEMENT**. "Plainly:" marks a departure from a ruling or a source, with its reason.
The hull's rungs are §5.0's (S, S†, R, T); the evidence's are the lead's (A the period's own, B a
historian's particular, C judgement). Lengths in metres, each with its source's units beside it on
first use; Forfait's pied du roi is 0.3248 m.

**One sentence.** One module writes her: Forfait's *Humble*, a tartane of 100 tonneaux with a
topsail and a mizen (62¾ by 20⅓ pieds, 20.38 by 6.61 m; Forfait 1788 Table II, read on the page
image), drawn on Chapman's French tartane of 1768 scaled to her; a whole lateen on a 24.4-metre
yard on her main with a square topsail on its head, a small lateen on a mizen raked aft and sheeted
to an outrigger, one great jib on the berthelot, a square tréou for running; unarmed, a trader of
ten with a fisherman's fit, and a coastguard of the same hull in a second file with Chapman's eight
4-pounders; tacked and worn as other vessels are, her yards shifted round their masts in stays or
in the wear by her practice, or left on the bad hand until shifted, which the engine cannot do
today.

---

## Decisions proposed

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/tartane.py`, writing `data/ships/tartane.yaml` (the trader) and, by question 5's pick, `data/ships/coastguard-tartane.yaml` (one class in two roles) | `Build-Ships.md` §3.3's per-ship modules; principle 10 (the brig and the merchant brig) |
| 2 | Her particulars as data in Forfait's units (pieds, pouces, lignes), converted once | The bilander's and the *Bellerophon*'s way: every figure reads as its source gives it |
| 3 | **Her size is the *Humble*'s** (Forfait Table II col. 2): 62¾ by 20⅓ pieds, 20.38 by 6.61 m; 100 tonneaux | The owner's rig (topsail and mizen) is Forfait's rig for her size (p. 124: a mizen once the breadth passes 19-20 pieds and the length 60); rung A, a named vessel "known to sail well" (p. 122). Question 1 |
| 4 | **Her lines are Chapman's Pl. LVIII No. 16**, scaled to her: lengths by the waterlines' ratio, sections by the beams' (6.61 ÷ 5.22 = 1.27). **S† (`stand-in`) once the plate is read at step 1; T until then, to read: Chapman Pl. LVIII No. 16** (the plate was not reached at a readable size: Tar §2.2) | §5.0 principles 3 and 7: the type's only lines; principle 3, a source on file but unread is no rung. **Plainly:** a war tartane's fine body widened by more than a quarter for a trader, the factor in the note |
| 5 | Draught 2.50 m, displacement about 155 t, GM about 0.8 m, all JUDGEMENT to be measured on the scaled body at step 1 | No trading tartane's draught found (Tar §2.3): Chapman's draught to breadth, 0.379, on her breadth |
| 6 | **The main**: a mast *à calcet* of 59 pieds (19.17 m) heel to head, 26 pieds (8.45 m) of head, stepped 10 pieds 5 pouces (3.38 m) before the middle; column shrouds (`haubans à colonne`) | Forfait Table II; Lescallier pp. 376-378 |
| 7 | **The great lateen**, class `lateen`, whole (no `cut_at_mast`), on a `lateen_yard` of 75 pieds (24.36 m) slung at a third; cut by Forfait's rule (p. 121) | Forfait Table II and p. 121; Lescallier p. 379; Ext §3.7 |
| 8 | **The topsail**, square, on a yard of 32 pieds (10.39 m) hoisted on the main's head; **no topgallant**. Her main is a pole (no topmast), so the topsail is a course to the engine today and wants A5 and A6 before her file (§5.1a) | Forfait's *Humble*; Röding; Winfield's Monleón shows none above the topsail, and the watercolour, for the eye, none. Question 4's note |
| 9 | **The tréou**, square, on a yard of 41 pieds (13.32 m) crossed as the cutter's square sail is, set before the wind and in too much wind, out of plain sail | Lescallier p. 401; Steel; Falconer; Forfait's *Espiègle* and square-sail column. Question 4 |
| 10 | **The mizen**: 30 pieds (9.75 m), head 6 (1.95 m), 15 pieds 2 pouces (4.93 m) abaft the middle, raked aft (JUDGEMENT on the angle); its lateen on a yard of 47 pieds (15.27 m), sheeted to an outrigger over the stern | Forfait Table II; Forfait p. 128 (the lateen xebec's after mast "panché vers l'arrière", the nearest text), the angle to be read on Chapman's plate at step 1; Lescallier p. 393 (the mizen to bring her to the wind); the outrigger's length by the lugger's (Forfait Table VII). The watercolour a check for the eye only |
| 11 | **The head**: the éperon (10½ pieds, 3.41 m, **to be re-read on the page image before it is a constant**: the printed ratio, 0.151, gives 9½ pieds, Tar §2.1) with the berthelot over it; **one great jib** to the berthelot's end, by judgement; a storm jib in the sail room | Lescallier pp. 393, 401; Forfait p. 125; Steel; Röding. Decision 11 leaves the headsails' count to judgement; the images README's reading of two is recorded (§17) |
| 12 | **The bouffette**, a smaller lateen bent to the great yard in the great lateen's place in a blow, as the lugger's taille-vent is | Lescallier pp. 394-395; Forfait p. 129. Question 6's note |
| 13 | **Tacked and worn as other vessels are** (the owner's answer to question 3): `tack ship` and `wear ship` each an evolution of her own; each lateen's yard shifted round its mast in stays (once her head is through the wind) or in the wear (at "wind aft"), peaked up and its car passed round, never lowered, by the order's clause or her practice ("shift" in both by default); or left, the lateen drawing as a lug against its mast on the bad hand until `shift the mainsail`; `put her about`, and a course ordered across the wind's eye, wear her over 22 knots | The owner (Dec 3, Part F); no source says a lateen vessel could not tack (GA §4); the yard changed "pour virer de bord", either way (Lescallier p. 378); the board on the mast named and sailed (Stratico, O'Scanlan: GA §3.3); the strong wind, Forfait p. 119. Question 2, answered |
| 14 | The engine work this needs is the plan's **A1a to A1d** (the whole lateen's side, its going about with the yard's change a part, the rules captain, taken aback; shared with the polacre's and the xebec's lateens), with **A3** (a tiller's words), **A4** (the boat in tow), **A5 and A6** (her topsail on a pole main) and later **A8** (the lateen in a gale), each designed in package 90's plan (§6 there) before her file (§5.4) | Every whole lateen of the package needs A1; nothing of it is in the engine today (observed, §5.1); her pole main's topsail is a course today (§5.1a) |
| 15 | Company **ten** in trade (master and mate posts, six seamen, a boy, a cook), JUDGEMENT until sourced; her great sail's work an all-hands call | Ruling 11; package 116's `too_few: all hands`; the bilander's ruling (Tar §6) |
| 16 | The trader **unarmed**; the coastguard **Chapman's eight 4-pounders and four swivels**, until Winfield's Spanish rows replace them | Chapman Pl. LVIII No. 16 (read there); Winfield to ask |
| 17 | Roles: the trader `merchant`, a `fishing tartane` description `fisherman` (the trawl, its grounds to source: booked, the plan's card); the coastguard, description key `guarda-costa tartane`, role `revenue`, the revenue cutter's book read from `thresholds:` | Build §8; package 116's road; Tar §5 |
| 18 | Rig word **"a tartane"**, size rank 1; no nation in the file (the scenario's, as the *Neufchatel*'s) | The made-out rule; D16's bilander precedent; the type named on sight |
| 19 | **Her boat towed astern** on passage by default | Decision 11 ("the boat in tow"); the watercolour. Question 6 |
| 20 | Her name: a saint's, as Provençal tartanes were named; **Saint-Pierre** proposed | JUDGEMENT; the owner's taste (§16) |

---

## How this draft answers the critic

| Finding | What the first draft said | This draft |
|---|---|---|
| F3: her topsail on a pole main | the heave-to read from the probe, "topsail aback" | **Held.** Her file puts the topsail yard on the main's own head (§4.1), and there the engine makes it a course: re-run for this draft on the probe with the yard so filed, "Hauled up the courses", hove to "under her fore-and-aft canvas", 51.8° off at 3.29 kn by truth 12's measure at +600 s (§5.1a). A5 (and A6) become conditions of her file (§0, §5.4 item 10; the plan's §9.1); T-5 is read after A5 |
| F7 (with Plan §4 row 4): her mizen hove to | the mizen "her driver", read by the driver's paths, "brailed hove to as the rule rules" | **Settled by the plan:** worked as a ship's mizen going about, kept set hove to; the driver rule never takes a whole lateen (§4.2, §5.3, §5.4 item 4). If she forereaches past truth 12's band, the lever is her great lateen's trim |
| F9: rungs before reading | Chapman's plate "S†" | **Held.** T until the plate is read at step 1, then S† (decision 4, §3) |
| F12: her size in plain words | "as long as the cutter's deck and a half" (and the decisions sheet's "exactly your rig") | **Held.** 20.38 m is about a quarter longer than the cutter's 54.5 ft (16.6 m) on deck and a third longer than her 15.2 m on the water; the *Humble* carries a topgallant, which is left out (§16.1) |
| F13: figures from a picture | the mizen's rake and the outrigger "JUDGEMENT on the watercolour" | **Held.** The rake on Forfait p. 128 and Chapman's plate, the outrigger on the lugger's (decision 10, §4.2); the watercolour for the eye only |
| F16: her words | "a King's tartane, armed, a coastguard" | **Held.** "a guarda-costa", the period English for the Spanish service's vessel (James's "garda-costa"); "coastguard" as a vessel's name belongs to the British service of the 1820s (§8, §9, §12) |
| F20: the éperon | 10½ pieds taken as read | **Held.** The printed ratio gives 9½: re-read on the page image before it is a constant (decision 11; Tar §2.1) |
| F24: whose question | the headsails to the owner, the main's rake to the lead | **Held.** The headsails by judgement (decision 11's own words), one jib; the main's rake to the owner, their word "raking" beside their watercolour's near-upright main (§16.1 question 3) |
| The plan's settlements | numbered items of one step | the plan's step names (decision 14, §5.4); the coastguard a second file (Plan §4 row 12); no scenario in the card (§12) |

---

## 0. The gate, the order, and what waits

**Nothing opens until the owner agrees a scope card** (nudge 15; ScopeCards, as amended
2026-11-16): one building package at a time, the owner's gate of milestone 7 before new building
unless they say otherwise. This draft is input to that card. When it opens, the order this draft
proposes for her (for the plan to weigh against the other four hulls):

1. **Step 0, documents and measurement, outside the tree's code**: Chapman's Pl. LVIII No. 16 read
   at a readable size and measured outside the repository (as Gwyn's bilander was:
   `owner-notes/<ship>/`); Winfield's passages (Tar §10) read by the owner; Lescallier's Pl. XXII
   fig. 5 and Forfait's figs. 9 and 35 seen.
2. **The engine's steps A1a to A6** (§5.4; the plan's §6 and §9.1): A1a to A1d the whole lateen,
   tested on a rig in memory (the lead's `tartane_probe()` with the step's key) before any file
   carries it, every committed file byte for byte; A3 and A4; and **A5 and A6**, since her topsail
   stands on a pole main (§5.1a).
3. **Her module and her two files**, generated, her tests and truths; the viewer's drawing of the
   whole lateen and its shift (§10). Her scenario and its shelf line are booked, not in the build's
   card (§12; the plan's §4 row 15).

She comes first among the three lateen hulls because she is the smallest, the reference vessel,
and the first whole lateen; the polacre's and the xebec's lateens take the same engine step after
her. (On the plan's other road the *Diana* comes first: Plan §9.1.)

---

## 1. The module and the generator

- **Files**: `tools/ships/tartane.py` (her module, `build(out_dir)`), imported and called by
  `tools/gen_ships.py` as the package-75 ships' are; `data/ships/tartane.yaml` and, by question 5,
  `data/ships/coastguard-tartane.yaml`; `data/people/tartane.yaml` (and the coastguard's); her rows
  in `freesail/world/ships.py` and `world/captains.py`; `tests/test_tartane.py`.
- **The data**: a frozen `Particulars` in Forfait's units (Table II's column 2 whole, the
  *Espiègle*'s and the square-sail column's figures kept beside it as records), Chapman's plate's
  measured points in Swedish feet, each converted once.
- **The checks** (each a `ValueError` with a sentence, as `settee.py`'s): the great lateen's sling
  a third along its yard within 0.1 m of the main's raked line; its peak inside the outrigger's end
  and its clew inside the taffrail; the sum of her sail within a stated band of Forfait's (§4.6);
  the masts and yards within rounding of Table II.
- **Item 37** (the generator's own sail-force law): her ratings pass through `PEAK_COEFF`, whose
  lateen entry (1.25) is the engine's row's peak (1.246 at 35°, computed here from
  `data/sail_classes.yaml`); she carries no studding sail, so the studding entry's difference (1.25
  against 1.44) does not touch her. Nothing of hers moves by it, though her file, as every new one,
  is generated only after the owner has settled it (the lead's note; the plan's A0).

---

## 2. The hull blocks

| Figure | Value | Source and rung |
|---|---|---|
| Length (Forfait's *longueur*) | 20.38 m (62¾ pieds) | Forfait Table II col. 2, read (page image), A. Which length (on deck or stem to sternpost) is not stated: to read in Forfait's ch. I |
| Waterline length | **19.0 m, provisional** | JUDGEMENT; at step 1, Chapman's waterline over the plate's length between perpendiculars, applied to 20.38 m |
| Breadth | 6.61 m (20⅓ pieds) | Forfait, A |
| Draught | 2.50 m | JUDGEMENT: Chapman's 1.98 m on 5.22 m (0.379) on her breadth; the sections' factor of principle 7 |
| Displacement | about 155 t | JUDGEMENT: Cb 0.48 on the figures above; measured on the scaled body at step 1, the drawn and the filed within 15% or recorded (principle 8) |
| GM | about 0.8 m | JUDGEMENT: a broad, shallow hull (Forfait p. 125, "their relative breadth always very great") under a high centre of effort (p. 123) |
| Deck above the water | about 0.9 m | JUDGEMENT until Chapman's sheer is read (the cutter's 0.9) |
| Hull speed | 10.6 knots to start | the files' rule, 1.34 √(LWL in feet) |
| Burden | 100 tonneaux | Forfait, A; kept in the notes, no constant |

**Plainly:** the lead's probe (`tests/rig_fixtures.py`) is the cutter's 15.2-m, 106-t hull; she is
a third longer and half again as heavy (JUDGEMENT on the figures above). The probe classes her; it
was never meant to sail her.

## 3. The hull profile and her shape (`Build-Ships.md` §5.0-§5.3)

| Line | Source | Rung | Mark |
|---|---|---|---|
| Body under the water, sections, keel, rising line | Chapman Pl. LVIII No. 16, scaled | S† once read at step 1; T until then, to read: the plate | `stand-in` once read; `judged` until then |
| Sheer, rail, stem, stern | the same plate | S† once read; T until then, to read: the plate | as above |
| The éperon and the berthelot | Forfait Table II (10½ pieds, to re-read), p. 125; Lescallier p. 393; the plate's beak to read | R for its length (Forfait's table); T for its shape until the plate is read | `rule`; `judged` |
| Wales and paint | the plate where it shows them; the watercolour's dark hull and light strake for the eye | T | `judged` |
| Carving | Falconer's CAGOUILLE, the scroll at a tartane's prow: in words | — | principle 9 |

- **The factors** (principle 7): lengths 19.0 ÷ Chapman's waterline (about 18.5 m, to read); the
  sections by 6.61 ÷ 5.22 = 1.266, so her floor, flare and tumblehome keep the plate's angles. The
  depth so drawn is recorded beside her draught and never moved.
- **What the drawing must show her to be** (the watercolour, seen, no figure taken): a low, beamy
  hull with a strong sheer rising to the beak and the stern, a long beak with the berthelot almost
  level beyond the stem, a raised after deck, no ports in the trader.
- **The measuring tasks** (step 1): the plate's waterline, perpendiculars and breadth; the stations'
  sections; the sheer and the rail; the beak; the masts' places and rakes against Forfait's; the
  ports of the war tartane; the scale's check against the 1971 reprint's table (Chapman's 62¼
  Swedish feet).

## 4. The rig, mast by mast

Each spar and sail with its class. Heights above the deck are this draft's JUDGEMENT on Forfait's
lengths with the mast stepped about 2.8 m below the deck (the depth of hold not found), to be
measured on Chapman's sheer at step 1.

### 4.1 The main mast

| Part | Id; class | Figures | Source |
|---|---|---|---|
| Lower mast *à calcet* | `main.mast`; `mast` | 59 pieds heel to head (19.17 m), 22 pouces (0.60 m) at the deck, its head 26 pieds (8.45 m); the hounds about 8 m above the deck, the head about 16.4 m; stepped 3.38 m before the middle | Forfait Table II, A; heights JUDGEMENT |
| Rake | — | **3° forward, provisional** | JUDGEMENT on decision 11's "one raking mast"; no text gives it; the owner's watercolour shows the main near upright (seen, for the eye only); the owner's question, §16.1 question 3 |
| Column shrouds | lines of class `shroud`, sided, each with its runner tackle | as the lugger's and the cutter's shrouds are filed, rated by their rule | Lescallier pp. 377-378, A |
| The great lateen yard | `main.lateen_yard`; `lateen_yard` | 75 pieds (24.36 m), 9¼ pouces (0.25 m); slung at a third from the car (8.12 m before the mast); its ends 1½ pieds at the penne and about ¾ at the car | Forfait, A; Lescallier p. 379, A |
| Its gear | lines | the halyard (jeers) a `halyard`; the two ourses, *à proue* and *à poupe*, two `guy`s at the car (the bilander's mapping of the ourses, Bil §1.2); the brace (*oste*) and the vang (*van*) at the penne, `vang`s; one parrel | Lescallier p. 379, A; the forward ourse to the berthelot's end (p. 393) |
| **The great lateen** | `main.lateen`; `lateen`, whole | head 72¾ pieds (23.63 m: the yard less its ends); the clew where it falls on the deck at the mast's foot with the yard peaked as she carries it (Forfait p. 121, R), the car tacked at the stem; one sheet aft to leeward, one tack; **about 100 to 140 m²** before the cut (JUDGEMENT); one oblique reef band (Lescallier p. 379) | A, R |
| The topsail yard | `main.topsail.yard`; `yard`, **`on: main.mast`** (no topmast: a pole main) | 32 pieds (10.39 m), 6¼ pouces; hoisted on the main's head, about 15.5 m above the deck; braced as the cutter's topsail yard | Forfait, A; the brace limit the cutter's, JUDGEMENT. The engine reads it as a course today (§5.1a): A5 |
| **The topsail** | `main.topsail`; `square` | cut between its yard and the hounds by the cutter's topsail rule, its sheets to the deck (no lower yard set) | Forfait's *Humble* crosses no lower yard; Röding; Winfield's Monleón "for stability" |
| The tréou's yard | `main.treou.yard`; `yard` | 41 pieds (13.32 m), 8½ pouces; crossed as the cutter's `square_sail.yard` is ("the type set this sail flying, the yard sent up with it"; the file crosses it) | Forfait's *Espiègle* and square-sail column, A; the cutter's precedent |
| **The tréou** | `main.treou`; `square` | from its yard to near the deck; in "square sails" and "all sail", **never plain sail**; set before the wind and in too much wind | Lescallier pp. 395, 401; Steel; Falconer TREOU and SQUARE-SAIL, A |
| The bouffette | `main.bouffette`; `lateen`, whole, in the sail room | a smaller lateen bent to the great yard in the great lateen's place; its area JUDGEMENT (two-thirds) | Lescallier pp. 394-395 (the galley's); the lugger's taille-vent precedent |

- **No topgallant.** Forfait's *Humble* carries one (24½ pieds, 7.96 m); the owner's picture,
  Monleón's print and Röding do not. Left out, recorded.
- **With the tréou's yard crossed on the main's lower mast she is still one mast with yards**
  (observed: a lower square yard added to the probe, the main's two yards her head yards, not
  square-rigged, nothing on a schooner's mast). B3.4's two limits are an after mast's and do not
  reach her (§5.2).

### 4.2 The mizen

| Part | Id; class | Figures | Source |
|---|---|---|---|
| Mizen | `mizzen.mast`; `mast` | 30 pieds (9.75 m), 10 pouces (0.27 m), its head 6 pieds; stepped 4.93 m abaft the middle; **raked aft, 10° provisional** | Forfait Table II, A; the rake JUDGEMENT on Forfait p. 128 (the lateen xebec's after mast "panché vers l'arrière"), its angle to be read on Chapman's plate at step 1 |
| Its lateen yard | `mizzen.lateen_yard`; `lateen_yard` | 47 pieds (15.27 m), 6 pouces; slung at a third | Forfait, A |
| **The mizen lateen** | `mizzen.lateen`; `lateen`, whole | cut by Forfait's rule; its sheet to the outrigger; about 30 to 45 m² (JUDGEMENT) | A, R |
| The outrigger | `mizzen.outrigger`; the lugger's class for hers | its length by the lugger's `bout-dehors de tapecul` (Forfait Table VII) in proportion to her mizen yard (JUDGEMENT on the carrying) | the lugger's file; Forfait Table VII |

- **Her mizen in going about and hove to.** Lescallier p. 393: the mizen was added to bring lateen
  vessels to the wind. By the plan's settlement (Plan §4 row 4, on the polacre's measure) it is
  worked as a ship's mizen going about (hauled aft as she comes to in the wear, eased at "up helm")
  and **kept set hove to**; the heave-to's driver rule (`after_gaff_sails`) never takes a whole
  lateen, and a guard over every file holds it: §5.4 item 4.
- **The watercolour** shows her mizen raked well aft with its sheet to a spar over the stern: a
  check for the eye on the drawing, no figure taken from it.

### 4.3 The head

| Part | Id; class | Figures | Source |
|---|---|---|---|
| The éperon with the berthelot | `bowsprit`; `bowsprit`, fixed, near the horizontal | 10½ pieds (3.41 m) beyond the stem; its steeve a few degrees (JUDGEMENT) | Forfait, A; Lescallier p. 393 |
| **The jib** | `jib`; `jibheaded` | from the berthelot's end to the main's hounds; area by the files' rule on her stay | Lescallier p. 401; Steel; Röding, A. One, by judgement (decision 11) |
| The storm jib | `storm_jib`; `jibheaded`, in the sail room | the cutter's pattern | JUDGEMENT |

### 4.4 Groups and aliases

- **"plain sail"**: the great lateen, the topsail, the mizen lateen, the jib. **"all sail"**: those
  and the tréou. **"square sails"**: the topsail, the tréou. **"fore-and-aft sails"**: the two
  lateens and the jib. **"headsails"**, **"jibs"**: the jib. **"storm canvas"**: the storm jib.
  **"topsails"**: the topsail. No "courses" (her lateen is no course: the gale's reduction must not
  reef it as one; §5.4 item 6).
- **Yards**: "yards" and "main yards" the topsail and the tréou yards; the lateen yards in no yard
  group (they are no braced yards: `Spar.is_yard`).
- **Aliases**: "mainsail", "main sail", "the lateen", "the great lateen", "mestre" → `main.lateen`;
  "mizen", "mizzen", "the mizen lateen" → `mizzen.lateen`; "main yard", "the antenna", "lateen yard"
  → `main.lateen_yard`; "square sail", "the treou", "the tréou" → `main.treou`; "topsail".

### 4.5 Sail areas, and the check

Forfait's *Humble* with topsail and mizen carries 2,237½ square pieds (236.1 m²), a topgallant
among them. Her cut, without it, is checked at generation against 236 m² less the topgallant's
share (about 20 m², JUDGEMENT), within ±15%, and the figures recorded old beside the probe's
(283 m² on the cutter's hull). Forfait's centre of effort for her, 1.11 m before the middle and
8.19 m up (above the water, JUDGEMENT on Forfait's datum), is the second check, reported, not tuned to.

---

## 5. How the engine sails her today, and what it must be given

### 5.1 What it does today (observed)

The lead's `tartane_probe()` (the cutter's hull, a 120 m² lateen on a 16-m yard on the main under
the cutter's topsail, a 25 m² lateen on a small mizen), in B3.4's harness: seed 7, 15 knots from
the north, no gusts, heading 292.5° at 5 knots, plain sail set and braced sharp up, trimmed every
two minutes, settled 2,400 s; the cutter as filed beside her.

| | The probe | The cutter |
|---|---|---|
| Classing | one mast with yards (the main); the topsail yard her head yard; no after yards; the main laid aback; not square-rigged; no driver; no boom mainsails | the same gates |
| Polar in 15 knots at 40°, 60°, 90°, 120°, 180° off | 2.92, 5.67, 7.11, 6.73, 5.33 knots | 1.96, 5.89, 7.23, 6.79, 5.40 |
| `tack ship` | **tacked in 89 s**; at helm's a-lee only "ease off the head sheets"; the lateens neither hauled aft nor shifted, never against a mast | 106 s; "haul aft the mainsail sheet" at helm's a-lee |
| `wear ship` | 487 s; "Squared the head yards; shifted over the sheets; hauled out and braced up."; **the lateen yards never shifted** | 458 s; the same words |
| `heave to`, +330 s | topsail aback, helm a-lee; hove to at 123 s; **54.2° off at 3.06 knots of headway, both lateens drawing** (the probe's topsail on the cutter's topmast; on her own file's pole main, §5.1a) | mainsail hauled flat aft; 47.0° off at 1.93 knots |
| `dip the mainsail` | refused: "'dip' has no meaning for a lateen sail." | — |
| `take in the mainsail` | brailed up to its yard, six hands of the eight wanted (`take_in_lateen`) | — |

**Why** (read here): a whole lateen has no side. `against_the_mast` (`physics/sails.py:673`)
reads a dipping lug's `lug_side` alone, and the schema refuses `dipping` on any class but the lug
(`ship/schema.py:2363`). `boom_sails` and the driver's paths take a lateen cut at the mast, not a
whole one (`drives_aft`, Ext §3.5). So today she tacks faster than the cutter with nothing done to
her great sail, wears without shifting it, and forereaches hove to at twice truth 12's speed.

### 5.1a Her topsail on a pole main (observed, the critic's run re-run for this draft)

The probe's topsail yard stands on the cutter's topmast (`on: main.topmast`, read in
`data/ships/cutter.yaml`). Her own file has no topmast: the yard is hoisted on the main's own head
(§4.1). With the probe's topsail yard so filed (`on: main.mast`, B3.4's harness, the same settle):
- the courses (`scripts.lowest_square_sails`, `evolutions/scripts.py:860-868`, "square sails on
  yards that hang directly on a lower mast") are `['topsail']`;
- `heave to`: "Hauled up the courses." "The foresail sheet to windward; helm a-lee." "Hove to on the
  starboard tack, under her fore-and-aft canvas", **51.8° off at 3.29 kn by truth 12's measure** at
  +600 s, the topsail hauled up and not aback.

So her topsail is a course to the engine today wherever the polacre's pole main topsail is (Pol-D
§5.1's twelve places): the heave-to, lie a-try, the take-in words, the trim's levels. **A5** (a
yard's level read from its place on the mast) is a condition of her file, and **A6** (the pole's
quick handing and the topmast evolutions refused in words) reaches her topsail by its key, as it
reaches the smack's (the plan's §6). One point for A5's design (JUDGEMENT): with the tréou's yard
crossed below it (question 4's pick), the predicate's "rank by height on the lower mast" makes her
topsail level 1, a topsail; **without the tréou's yard it would be the lowest braced yard and still
a course**, so if the tréou is left out A5 must read a square sail over a whole lateen on the same
mast as a topsail (the lateen yard counted as the level below it), the lead's to rule at A5.

### 5.2 The schooner's mast and its two limits (observed)

She classes as the cutter does (`tests/test_schooner_mast.py`, the probe's test; observed again
here). With the tréou's yard crossed on her main's lower mast she is still one mast with yards and
not square-rigged: her main is her foremost (and only) mast with braced yards, so the rule names
nothing in her whether it counts a lower yard or not. The two limits (a lower square-sail yard on an
after main; a pole main with its topsail yard on the lower mast) are an after mast's and do not
reach her, nor the polacre or the xebec's rigs; they stay with a schooner's main, recorded (Pol-D
§5.4 states it once for the package). Her own pole main is one mast with yards, where the limits
cannot bite; what it does reach is the engine's reading of her topsail as a course (§5.1a).

### 5.3 The lead's item 8, for her

- **"A whole lateen hauled aft at helm's a-lee by nothing"**: so (observed: no line at helm's
  a-lee for either lateen). Under decision 13 she is tacked (the owner's answer to question 3):
  her mizen is hauled aft at helm's a-lee in stays and as she comes to in the wear (§5.4 item 4);
  her great lateen keeps drawing until her head is through the wind and is then shifted or left
  (§5.4 item 2).
- **"Her lateen mizen kept hove to as a fore-and-after's, and whether the heave-to's driver rule
  reaches it"**: the probe lies to with both lateens drawing and forereaches at 3.06 knots of
  headway (observed; the engine note's 3.14 kn, Eng §2.2). **Settled by the plan** (Plan §4 row 4,
  on the polacre's measure, Pol-D §5.2): the mizen is kept set hove to, and the driver rule never
  takes a whole lateen; taken in, the polacre does not heave to at all. If she forereaches past
  truth 12's band on her own file, **the lever is her great lateen's trim** (flat aft as the
  cutter's mainsail is, or eased), measured at the build against truth 12's band (§13, T-5).
  **Plainly:** the first draft leaned to the driver's rule for the mizen; the polacre's measure
  rules it out. Her heave-to on her own file is read only after A5, her topsail being a course on
  her pole main today (§5.1a).
- **The schooner's-mast rule's limits**: §5.2; not hers.

### 5.4 What the engine must be given (the plan's A1a to A1d, A3 to A6 and A8)

Each item is a behaviour, said here and designed in package 90's plan (its §6, which names the step
each belongs to); none is built now. The
package's engine note, drafted beside this document (`docs/design/Design-Package90-Engine.md`, its
§2, §3 and §10), measures the same probe on the same tree and finds the same (the tack in 89 s with
nothing said of the lateens, the wear in 487 s, the forereach hove to at 3.1 knots, the wheel's words
on a tiller-steered hull); it designs the step for all three lateen hulls, and this section says
what she needs of it.

1. **A whole lateen has a side** (A1a). The schema's `dipping` is allowed on a whole lateen, and
   `Sail.lug_side` is kept for it. `against_the_mast` reads it, so that on the bad hand it draws as
   a lug against its mast does: the game takes a third of the area (the primer's chapter 2). On
   her probe that costs 5½ per cent of her speed close-hauled (Eng §2.2a). No committed file has a
   whole lateen (read here), so no file's sailing moves.
2. **The tack and the wear each shift it, or leave it** (A1b; the owner's answer to question 3).
   - **When.** In `tack ship`, once her head is through the wind; in `wear ship`, as the wind comes
     aft.
   - **How.** Each whole lateen to be shifted goes to the new lee side:
     - the parrel eased and the runners cast off;
     - the yard stood up beside the mast by the ourses and halyard;
     - the car passed round the mast, and the tack shifted to the new weather side;
     - the yard settled and the sheet drawn on the new side.

     Lescallier pp. 378-379 and PCI 2018. It is **never lowered**. The car passes abaft the mast
     by Willaumez's MUDER and forward of it by O'Scanlan's CIMAR. The inventory and Lescallier's
     dinga pass the sheet forward of the mast, which does not settle the car's side. The side is
     not agreed (GA §3.3) and is the lead's.
   - **Or left**, by the order's clause or her practice (item 3). Her practice by default shifts in
     both (the owner's "preferred").
   - **The machinery.** The settee's `SetteeChange` with the yard peaked, not lowered; the order by
     itself `change_lateen` (Plan §4 row 3), the lead's to rule.
   - **Hands and time** (JUDGEMENT; Eng §2.4.4). Her main's 24.4-m yard wants ten hands and about
     three minutes. She can put at most eight to it, her six seamen, the boy and the cook, since
     her master and mate stay at the conn (ruling 11, §6.1). So it takes about four minutes (230 s,
     by the party's numbers term). Her mizen's 15.3-m yard takes about two minutes and six hands.
     The two are changed one after the other, the main first.
   - **The cost, measured** on her probe with its 16-m yard, 15 knots, the first quarter-hour
     (Eng §2.2a). Today a tack loses 227 m to windward and a wear 551. With the yards handled:
     - tacked with the yards left, 326 m;
     - tacked and shifted in stays, 428 to 529 m;
     - worn and shifted, 628 to 726 m.

     The board on the bad hand then costs her about 240 m an hour. So leaving the yard pays on a
     board shorter than about three quarters of an hour, and shifting it pays on a longer one. That
     is the inventory's long boards on the bad hand avoided, given by the game's own numbers.
3. **How each choice is ordered** (A1b, A1c).
   - **One going about**: `tack ship` and `wear ship` with "and shift the lateens" or "and leave the
     lateens" ("the mainsail" or "the mizen" by name).
   - **Her practice**: "in stays, leave the lateens" and its kin, shown in the readings; a standing
     order sets it as any order.
   - **The shift alone**: `shift the mainsail` (item 5).
   - **`put her about`** wears her over 22 knots, and so does a course ordered across the wind's
     eye (the course's judgement, Eng §2.3 item 6): a lateen is not put in stays in a strong wind
     (Forfait p. 119).
   - **The rules captain** keeps her practice. They leave the yards in stays under 12 knots
     (Stratico's fine weather), and shift them after half an hour on the bad hand or as the wind
     rises; after a gybe they shift a lateen left on the mast, as a lugger's lugs are dipped.
   - **The player's, the model's and the director's** `tack ship` is always a tack.

   **Plainly:** the second draft answered `tack ship` with "She does not stay under her lateen;
   wear her." and did nothing. The owner's answer drops it, and no source says it (GA §6).
4. **Her mizen as a ship's mizen** (A1b; Plan §4 row 4). A whole lateen on the aftermost mast of a
   ship with a mast before it is:
   - hauled aft at helm's a-lee in stays and as she comes to in the wear;
   - eased at "up helm";
   - eased as she pays off on the new board if no head sail is set (Eng §2.3 item 5);
   - **kept set hove to**. `after_gaff_sails` never takes a whole lateen, and a guard over every
     file holds it.

   **Plainly:** the first draft had it read by the driver's paths and "handled hove to by the
   rule"; the polacre's measure (taken in, she does not heave to) rules that out. Measured on her
   file.
5. **`shift the mainsail`** (and `shift the mizen`) (A1a), the period's *muder*, for a lateen left
   on the bad hand:
   - left by a tack or a wear with the yard left, a gybe by the helm or a shift of wind;
   - refused in words when it is on the good hand;
   - held while a manoeuvre is in hand;
   - `dip` and `change` accepted as its synonyms for a lateen;
   - the stern watch says when a gybe has left her great lateen on the mast.
6. **The gale and the lateen** (A8). "Shorten sail" takes in the great lateen before it would carry
   away (Forfait p. 120: the yard breaks in the first squall if she holds the wind in a storm), the
   tréou set if she runs, and offers the bouffette in its place (`bend the bouffette`), as the
   lugger's taille-vent; she lies to under her mizen and the storm jib (JUDGEMENT on the canvas).
   The whole lateen in no "courses" group, so the courses' reef never names it.
7. **Her lateens' evolutions sized to her** (A1a). B3.1's `set_lateen`, `take_in_lateen`,
   `furl_lateen` and `reef_lateen` want ten, eight, eight and ten hands (Ext §3.6, the 64's mizen
   course). For her the want is her own, by her file's data or the evolutions' `too_few: all hands`
   (package 116's road; the bilander's ruling), so that a watch of three calls all hands for her
   great sail.
8. **The boat in tow** (A4, drawn by V3; §11): a state of her boat, a drag, words, and the viewer's drawing; today
   the boats "towing astern" are clear-for-action's words alone (`evolutions/action_scripts.py`,
   read here).
9. **The tiller** (A3). Package 116's wheel shot away, its relieving tackles and `repair the wheel`
   are every ship's words; she steers by a tiller on deck (memory, unverified for her; JUDGEMENT).
   The plan builds a hull key `helm: tiller` with a tiller's words ("the tiller shot away", "ship the
   spare tiller") for every tiller-steered hull at once, the cutter, the lugger, the smack, the two
   schooners and the hermaphrodite brig with her (Plan §6 A3, under the owner's rule on mends).
10. **Her topsail on a pole main** (A5, A6; §5.1a). A yard's level read from its place on the mast,
   so that her topsail is a topsail to the heave-to, lie a-try, the take-in words and the trim; and
   the pole's quick handing and the topmast evolutions refused in words, by A6's key, which her main
   carries. Both before her file.
11. **Taken aback in a breeze** (A1d; Forfait pp. 119-120; Fincham p. 59). Today a lateen aback
    costs her probe only her way, in 15 to 35 knots (Eng §2.2a). With A1d her great yard, taken
    aback, is loaded by the aback factor: it begins to strain at about 28 knots and may carry away
    from about 34, before the mast. `take in the mainsail` waits till she pays off, the canvas
    wrapped round the mast. On the bad hand in a gale the yard bears on the mast and strains. All
    JUDGEMENT on the figures, measured on her file (T-9; Eng §2.4.3).

**Pins it could move** (§14): none of a committed file by item 1's key; the probe's tests
(`tests/test_schooner_mast.py`, `tests/test_rig_classing.py`) read the probe as filed, which carries
no key. Items 9 and 10 move other ships, as the plan's card names: A3 the six tiller-steered files'
key and their words where a helm is shot away; A5 and A6 the smack's topsail handled as a topsail.

---

## 6. Her company and watches

### 6.1 The trader, ten (JUDGEMENT)

| Post or station | Number | Note |
|---|---|---|
| Master (*patron*) | 1, a post | commands; heads the larboard watch (ruling 11; the sides JUDGEMENT as the bilander's) |
| Mate (*second*) | 1, a post | the officer of the watch; heads the starboard watch |
| Seamen | 6 | able (JUDGEMENT on a coaster's crew), three a watch |
| Boy (*mousse*) | 1 | ordinary |
| Cook | 1 | an idler |

- **Ruling 11** (the narrower form): the master and the mate are counted hands of their own watch
  for deck work only where the watch's whole number is under the work's want; never for the twelve
  manoeuvres, all-hands work, quarters or aloft; back to the conn when a manoeuvre begins. Her
  watches of three seamen (four with the boy) and an officer.
- **Her great sail's work calls all hands** (§5.4 item 7): setting, taking in, furling (aloft on the
  yard: the officers never counted there) and the shift. The tack and the wear are of the twelve:
  all hands, the officers at the conn; the change of her great yard in either wants ten and gets
  the eight she can put to it, her master and mate at the conn (§5.4 item 2).
- **The sources wanted**: a trading tartane's company in the prize papers' catalogue and Winfield's
  rows (Tar §10). Ten stays JUDGEMENT until then, within a range of eight to twelve.

### 6.2 The fisherman

The same ten, with two more for the net (JUDGEMENT), if the fisherman's fit is a description of the
trader's file (the company is the file's, not the fit's: `crew.complement`, read here). Otherwise
ten, the net worked by all hands.

### 6.3 The coastguard (the second file)

**Provisional thirty-four**: three a gun for the eight 4-pounders (Falconer's crew for a small gun,
the bilander's 3-pounders' rule, D31 (c)), the trader's ten for the sail, posts a master (her
commander) and a mate; JUDGEMENT until Winfield's men are read. The people file the cutter's form
for a King's small craft.

### 6.4 The people files

`data/people/tartane.yaml` in the bilander's form: the master and the mate as posts with their
watches, a boy to carry the word; `names: french` by default (the scenario's nation may change it;
the lists the lugger's). The coastguard's: `names: spanish` if the list exists (to read), else the
scenario's.

---

## 7. Her guns and ports (package 81's checklist)

| Fit | Guns | Source |
|---|---|---|
| The trader, `unarmed` (default) | none | JUDGEMENT; the bilander's and the merchant brig's pattern |
| The coastguard, `long guns` (default of the second file) | **eight 4-pounders, four a side, and four swivels** | Chapman Pl. LVIII No. 16 (read there): a French war tartane's; to be replaced by Winfield's Spanish rows when read |

**The checklist** (`Build-Ships.md` §6, postscript), for the coastguard's file:
1. `hull.profile` with `rail_m`, `breadth_m` and `decks_m` (her one deck), from the scaled plate;
2. `ports_m.<deck>`: a triple [x, sill, half-breadth] at each gun's `x_m`, **the x's from Chapman's
   ports as read at step 1**, the sills her sheet's; a gun over the rail if the plate shows no ports
   (`OVER_THE_RAIL_M`);
3. `port_size_m.<deck>`: [width, depth], from the plate;
4. each gun's `kind` (long gun), `pounder` (4, in the nation's pound as Winfield gives it, or the
   French livre's as Chapman's; the game's English pounds beside it), `place`, `side`, `x_m`,
   `weight_cwt` (the nearest pattern in Adye's tables, listed if more than a tenth off), `deck`;
   the four swivels on the rail, half-pounders, two a side aft (JUDGEMENT);
5. then `python tools/check_viewer_guns.py data/ships/coastguard-tartane.yaml` clean, and its test.

The magazine a small cruiser's (the cutter's by her guns' number, JUDGEMENT); her quarter bill the
cutter's form for eight guns; "sail before guns" for the trader.

---

## 8. Her fits and roles

| File | Description key | Rig word | Fit | Roles | Doctrine |
|---|---|---|---|---|---|
| `tartane.yaml` | `tartane` | "a tartane" | `unarmed` | `merchant` | the merchant's book |
| `tartane.yaml` | `fishing tartane` | "a tartane" | `unarmed` | `fisherman` | the fisherman's; the trawl, `gear:` in her file |
| `coastguard-tartane.yaml` | `guarda-costa tartane` | "a tartane" | `long guns` | `revenue` | the revenue cutter's book (`data/captains/revenue.yaml`: every sail spoken, an enemy of her size engaged, a man of war of the enemy's avoided), its thirteen keys read from `thresholds:` (package 116) |

- **The coastguard's doctrine.** The Spanish navy's tartanas served "now and then" as coastguard and
  look-out vessels (Winfield, the lead's words). The revenue cutter's book is the nearest (the
  search not modelled there either). A doctrine of her own (`coastguard.yaml`) only if Winfield's
  passages give a duty the revenue's book lacks; the look-out's report to a squadron is package
  72's road. JUDGEMENT.
- **The fisherman's gear and grounds.** The Provençal tartane towed a trawl (memory, unverified;
  Duhamel du Monceau to read); the smack's `trawl` gear the nearest; a grounds file for the Gulf of
  Lion on 79c's water (none exists, read here), its fish and seasons sourced or judged as
  `data/fishing/biscay-north.yaml`'s. If none is sourced before the build, the fisherman's
  description waits and the trader goes alone.
- **Nation**: none in the file, as the *Neufchatel*'s; French by default in a Provençal scenario,
  Spanish for the coastguard's (the scenario's).
- **No regency's role for her.** The Barbary regencies' cruisers are the xebec's (decision 56's
  role); a tartane taken by a corsair is a prize, not a cruiser.

---

## 9. Her words: what the tops make out, then the glass

By the made-out rule (package 75, Phase 5; `world/ships.py` l. 95-113, read here): at the horizon "a
sail"; within `RIG_MADE_OUT_NM` (4 miles; 6 with a glass aloft) her rig and her course, ranked by the
rig word; within `COLOURS_MADE_OUT_NM` (2; 3) her colours; within `MADE_OUT_NM` (1½; 2¼) what she is.

| Level | The trader | The fisherman | The coastguard |
|---|---|---|---|
| The rig (4 miles) | "a tartane, standing to the ..." | the same | the same |
| Colours (2 miles) | her colours, or "a stranger, her colours not made out" | the same | the same |
| What she is (1½ miles) | "a tartane, a coaster under her great lateen, deep laden" | "a fishing tartane" | "a King's tartane, armed, a guarda-costa" |

- **Why "a tartane" at four miles** (JUDGEMENT): the tops see one great lateen yard longer than her
  hull peaked high over a short mast, a small square topsail at its head, a diminutive mizen; the
  period named the type on sight (Falconer's "extremely large" sail). A felucca has no topsail and
  pulls oars; the polacre and the xebec have three masts. At six miles with the glass the same.
- **"A guarda-costa"** (JUDGEMENT on the words): the period English for a Spanish vessel of that
  service (James's "polacre brig and garda-costa", vol. 4 p. 167: Pol §6); "coastguard" as the name
  of a vessel belongs to the British service of the 1820s. The file's name, `coastguard-tartane.yaml`,
  is no word of hers and is the lead's to rule (§16.2).
- **The coastguard's "King's"** is in `captains.MAN_OF_WAR_WORDS` (read here), so a trader made out
  within 1½ miles treats her as a man of war; at four miles she is "a tartane" and nobody's fear,
  which is the coastguard's use.
- **Rows** (her window): `SIZE_RANK["tartane"] = 1` and `("tartane", 1)` in `_SIZE_WORDS`
  (`world/captains.py`; no earlier word matches inside "tartane"), the three descriptions in
  `DESCRIPTIONS`, and the words "a tartane", "tartane", "tartan" (Falconer's and Steel's spelling),
  "tartana" (the Spanish), "a guarda-costa", "garda-costa" in `_DESCRIPTION_WORDS`. `ship.rig:
  tartane`.

---

## 10. What the viewer must draw

1. **The whole lateen on its yard, on a side**: the sail on the lee side of its mast on the good
   hand, pressed against the mast (bellied round it) on the bad; the yard's long overhang before
   the mast and its peak above the masthead. The lug's drawing (Ext §6.1's `lugCut` as a standing
   sail on its lee side) is the nearest; the side is new (§5.4 item 1).
2. **The shift in stays and in the wear**: the yard stood up beside the mast and its car passed
   round (abaft or forward of the mast, by the lead's ruling: §5.4 item 2), as the lug's dip is
   drawn, without the lowering.
3. **The square topsail on the main's head**, the main drawn as a pole with no doubling (V2), with
   its sheets to the deck; the tréou's yard crossed
   below it, bare until the tréou is set.
4. **The mizen raked aft** with its lateen and the outrigger over the stern its sheet leads to.
5. **The beak and the berthelot**, nearly level, the jib's tack at its end.
6. **The boat in tow** on its painter astern, veered as the speed and the sea ask (JUDGEMENT).
7. **The hull from her profile** (§3), the scroll at the prow in words only.
8. **The coastguard's guns** by package 81's rule from her file alone (§7); the trader none.

The standard is the current ships' (the plan's §0); screenshots beside the watercolour for the
owner's eye, never measured against it.

---

## 11. Ground tackle, boat, pumps, hold and stores

- **Ground tackle, pumps, hold**: the merchant brig's and the bilander's rules by her size (package
  34's anchors by tonnage with hemp cables; package 35's pumps), JUDGEMENT; her anchor let go by a
  watch too small for it calls all hands (package 116).
- **Her boat**: one, about 4.5 m, towed astern on passage (decision 19; the watercolour; JUDGEMENT on
  its size); hoisted in, or veered long, in a blow (JUDGEMENT). Its drag on her: from the boat's
  resistance at her speed (`Design-BoatAndPersonAboard.md` §6's tow figures, read here, give a boat's
  own resistance at a knot), measured at the build.
- **Stores**: a coaster's, 30 days' provisions, 3 tons of water (JUDGEMENT, the smack's to the
  bilander's scale); her spare sails the bouffette and the storm jib.

## 12. Where she sails

On 79c's water: Marseilles, Toulon, Hyères, the Gulf of Lion's entries (the Rhône's mouth to Arles,
Martigues, Maguelone, La Nouvelle: Michelot 1709, Tar §5), Barcelona, Cartagena, Alicante and
Algiers, all charted (`data/ports/`, read here). Her first scenario, for package 96's shelf (a
sentence, on the **Trade** shelf): "A Provençal tartane from Marseilles to Toulon with wine for the
fleet, under her great lateen." The coastguard's, for **Actions**: "A Spanish guarda-costa tartane off
Cartagena, a stranger standing in." Neither is written now, nor in the build's card: her scenarios
are booked for a card of their own after the nations' dated wars (the plan's §4 row 15); she is
offered from the harbour for a bare start.

---

## 13. Truths proposed

Numbered at the build. Each with its source and a band to be settled by measure on her file.

| # | The truth | Source | The measure |
|---|---|---|---|
| T-1 | Her particulars hold their sources | Forfait Table II; Chapman | her masts, yards and places within rounding of Table II; her drawn hull's scale recorded |
| T-2 | **She lies about a point nearer the wind than a square-rigger** | Lescallier p. 380 (five points against six); Steel I p. 237 | close-hauled in 15 knots, her best way made good to windward against the merchant brig's, from the same settle; band JUDGEMENT |
| T-3 | **She tacks and wears, her yards shifted or left**: `tack ship` tacks her and `wear ship` wears her; by her practice each lateen is shifted to the new lee side, and after it neither lies against its mast; with "and leave the lateens" each lies on the bad hand; `put her about`, and a course ordered across the wind's eye, wear her over 22 knots | the owner's answer to question 3; Lescallier p. 378; Forfait p. 119 | the tack's and the wear's times and the ground lost to windward against the cutter's (106 s and 184 m, 458 s and 439 m in 15 knots: Eng §2.2a), within a band; the sides read after |
| T-4 | On the bad hand her lateen draws less, and `shift the mainsail` puts it right | Stratico, BISDOSSO; O'Scanlan, VELA; PCI 2018 (B); the lug's rule | the speed on the bad hand against the good (her probe 5½ per cent less at the lug's two-thirds: Eng §2.2a); the shift's time |
| T-5 | Hove to she lies within truth 12's angle and under its speed, or her own band, argued | the cutter's heave-to; §5.3 | +300 s and +600 s windows, as truth 12's, her speed by its `knots()` (`dyn.speed`); after A5 (her topsail a topsail); the lever her great lateen's trim |
| T-6 | In a gale the great lateen comes in before 30 knots and she lies to under the mizen and the storm jib | Forfait p. 120; Lescallier pp. 394-395 | the gale of B3.4's reviews |
| T-7 | A watch of hers calls all hands for her great sail, and her master and mate haul only where ruling 11 says | ruling 11; package 116 | her requests by night and by day |
| T-8 | Before the wind the tréou set adds way, and the great lateen is taken in for it | Lescallier p. 401; Falconer | the run at 180° off, with and without |
| T-9 | **Taken aback in a breeze her great yard strains**: in a strong wind it strains and may carry away, before the mast, and the sail will not come in till she pays off; in a moderate one she only loses her way | Forfait pp. 119-120; Fincham p. 59 | her head put in the wind's eye in 15, 28 and 34 knots: the yard's load over its rating, what carries away, the take-in's words; band JUDGEMENT (Eng §2.4.3) |

---

## 14. Pins her work could move

- **The engine step** (§5.4): keyed so that no committed file moves (none carries a whole lateen,
  read here); the four whole logs, the golden table, every file byte for byte, measured.
- **The probe's tests** read `tartane_probe()` as filed (no key): unmoved unless the step's key is
  made the default for a whole lateen, in which case the probe's classing test is re-read, old
  beside new.
- **`world/captains.py`'s `_SIZE_WORDS`**: a new row before none that matches inside it; every
  description ranks as before (a test over the rows).
- **A3, A5 and A6** move other ships' pins, as the plan's card names (§5.4's last paragraph).
- **The harbour**: nothing in this card (her shelf lines are booked with her scenarios).

## 15. Risks, ranked

1. **The engine step is new behaviour on every whole lateen of the package** (the polacre's fore
   and mizen, the xebec's three): designed once in the plan, built once, its key the only road.
2. **Chapman's plate unreadable or unlike a trader**: her lines then stand at T, a type judgement
   (a broad Mediterranean coaster's body), said so.
3. **Her company and guns are judgement** until the passages come: the coastguard's thirty-four
   especially.
4. **The lateen row is untuned** (`docs/dev/TuningNotes.md` l. 127): her close-hauled advantage is
   the row's today (the probe's 2.92 knots at 40° against the cutter's 1.96); T-2 is where it is
   tested, and A8 tunes it once on the lateen hulls on the branch at the time (Plan §4 row 7), her
   figures re-measured old beside new.
5. **Her topsail on a pole main** waits on A5 and A6 (§5.1a); A5's predicate must make it a topsail
   whether or not the tréou's yard is crossed below it.
6. **The fisherman's grounds unsourced**: the description waits.

---

## 16. Open

### 16.1 For the owner (few, plain; the pick first)

1. **Her size.** *The pick*: the *Humble*, 100 tonneaux, 20.4 by 6.6 m, with topsail and mizen
   (Forfait's table), on Chapman's lines widened to her. Or the *Espiègle*, 75 tonneaux, 16.8 by 5.8
   m (a tartane simple, which by Forfait carries no mizen); or Chapman's war tartane, 18.5 by 5.2 m,
   at her own scale. *A sketch*: the *Humble* is a beamy coaster about a quarter longer than the
   cutter on deck (a third longer on the water), her yard longer than her hull. She is your rig but
   for the *Humble*'s topgallant, which is left out.
2. **Going about.** *Answered by the owner, 2026-11-18* (Dec 3 and Part F), in their own shape:
   she tacks and wears as other vessels do, her yards shifted round their masts in stays or in
   the wear by her practice, or left on the bad hand until shifted; the change "preferred but not
   necessary". **Plainly:** the pick, worn not tacked, came from the brief and not from a source
   (GA §4), and is dropped (decision 13; §5.4 items 2-3).
3. **Her main's rake.** *The pick*: raked 3° forward, a little, so that your word "raking" holds and
   your watercolour's near-upright main still looks right. Or upright, as the watercolour shows it;
   or raked further, as your word might mean. No text gives a tartane's main a rake. (The headsails
   are left to judgement by decision 11 itself: one great jib, as Lescallier, Steel and Röding give
   her; the images README's reading of two is recorded, §17.)
4. **The tréou.** *The pick*: carried, a square sail on a yard crossed below the topsail, set before
   the wind and in too much wind, never in plain sail. Or left out.
5. **The coastguard.** *The pick*: a second file of the same hull, with Chapman's eight 4-pounders
   and a company of about thirty-four, one class in two roles as the brig and the merchant brig are.
   Or one file whose coastguard fit adds guns to the trader's ten.
6. **Her boat, and her name.** *The pick*: her boat towed astern on passage, as in your picture; her
   name a saint's, *Saint-Pierre*. Or the boat on deck; a name of your choosing.

**Where the owner meets them:** questions 1, 3 and 4 are the decisions sheet's question 4, and
question 2 its question 3 (`Decisions-Package90-2026-11.md`); 5 and 6 are in its Part E, taken as
recommended unless the owner says otherwise. **All are answered (2026-11-18):** questions 1, 3
and 4 as picked, 5 and 6 standing as recommended, question 2 in the owner's own shape.

### 16.2 For the lead

- **A1's machinery** (§5.4 item 2): the plan's proposal, `dipping` on a whole lateen, the change in
  the tack and the wear on the settee's `SetteeChange`, peaked and not lowered, and a new
  `change_lateen` evolution for the shift alone (Plan §4 row 3, §13.1 item 1). With it, its
  figures: the bad hand's loss, the change's seconds and hands, the side the car passes, the rules
  captain's winds, and the strain aback (Eng §2.4).
- **A5's reading of a topsail over a whole lateen** if the tréou's yard is left out (§5.1a).
- **The tiller's words** (§5.4 item 9): settled by the plan as A3 for every tiller-steered hull,
  their figures JUDGEMENT for the lead (Plan §13.1 item 3).
- **The company per fit**: settled by the plan (§4 row 12), one class in two files.
- **The file's name** `coastguard-tartane.yaml` and the description key `guarda-costa tartane`
  (Plan §13.1 item 5).
- **Item 37**: nothing of hers moves (§1).

---

## 17. Found on the way

- **The images README's "two headsails"** is one reading of the watercolour; this draft's reading
  sees one (Tar §9), and the count is judgement by decision 11 (one jib). The README is not changed
  here (Plan §13.2).
- **`VesselReferences-2026-10.md` §0** gives Lescallier's tartane at pp. 394 to 401; the article is
  pp. 400 to 401 (the range is the lateen craft's chapter). §3.1's "the rule ... was not found"
  (the lateen's tack shifted round the mast) is answered for the lateen by Tar §4.2.
- **The probe's heave-to** says "The foresail sheet to windward" of the cutter's fore staysail,
  aliased "foresail" in the cutter's file; a tartane's file aliases no foresail.
- **The probe tacks** with no word for the lateens and in less time than the cutter (89 s against
  106 s): the engine's lateen is today a jib-like sail with no side. Recorded for the step, no
  fault of the probe, which was for classing.
