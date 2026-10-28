# Decisions: the three ships, the owner's second round (2026-10-25)

**Status (2026-10-28): answered by the owner (2026-10-27) and ruled on by the lead (2026-10-28), both recorded below; D18 and D25 stay open.** The sheet was written before Package 75's brief (`docs/dev/M7-WorkPackages.md`), which binds. The brief reopened or settled these decisions, as the answers below take into account:
- **D12** (the lee ports): the brief has the 74's lower-deck ports shut within a foot of the water as the sources give. A truth pins it.
- **D14** (the viewer's hull): the brief adds a sourced hull profile to every ship file through the generator. The viewer still stays at today's standard.
- **D17** (the Indefatigable's fits): the brief wants a fit "as razeed 1795", with later armaments as data for the scenario editor.
- **D27 and D39** (the Neufchatel's scenario and names): the brief makes her an American vessel of 1812.
- **D10** (her main topgallant): the brief leaves the physics unchanged and has a rig the engine lacks reported to the lead.
- **The 74**, the sub-types as fits and roles, and the per-gun pivot arc are new in the brief, and are not in this sheet.

## The owner's answers (2026-10-27)

"Unless indicated here, decision as recommended." So every decision below not named here is taken as recommended, subject to the brief where the status note above says the brief reopens it.

| Decision | The owner's answer |
|---|---|
| **D3** | **(b).** The settee is kept drawing as a ship's mizen is, to help her through the wind, and dipped last. |
| **D8** | **(b).** Yards under the bowsprit where the period shows them: the 64's spritsail and sprit-topsail yards, and the bilander's. "Let's live a little; spritsails are a reasonable thing to try for." |
| **D9** | **(c).** The 64's mizen on its proper lateen yard, the dormant lateen class finished. The 64 should be "rightly sailable and as detailed as any other ship", and the lateen will serve later ships (a tartane), so it is to be properly implemented. |
| **D12** | **(b).** The lee ports shut within a foot of the water, for every ship. |
| **D14** | **(c), in this package.** The sourced hull profile goes into every ship file **and is drawn by the viewer**, for every ship. |
| **D18** | **Open, with the owner's measure:** whichever choice gives the best impression in the viewer and matches the sources. The convention may change, so long as the change is an improvement. |
| **D35** | **(b), limited.** The fore topgallant studding sail, together with (a)'s studding sails and main topmast staysail. |
| **D25** | **Open** until the 74's research reports. A French 74 would make the *Droits de l'Homme* action of January 1797 a third candidate, beside the sheet's (b) and the lead's (c). The research has reported (`Research-74-2026-10.md`): it recommends the British *Bellerophon* for this package and proposes a *Téméraire*-class French 74 as a later ship of its own, which the *Droits de l'Homme* option needs (its owner's question 16). The owner holds D25 open. With the French 74 a later ship (below), that option would wait for her. |

**The owner's word on the viewer (2026-10-27).** "Changing the viewer is alright now." The sourced hull profile, and drawing it properly in the viewer, are part of this package and are to be properly implemented.

**The 74 (2026-10-28).** The owner chose HMS *Bellerophon*, the Arrogant-class 74 of 1786 on the Bellona-class draughts, as this package's 74 (`Research-74-2026-10.md` §1.2). A *Téméraire*-class French 74 is the second ship of the line, a later goal outside this package. The note's other questions (§11, 2-18) are not yet answered.

**What follows from the answers:**
- **D46 becomes (d) with rule 3 restored,** since D3 is (b). In stays, the ourse is braced to leeward as the helm goes down, and the yard is changed last. Each rule is carried over by judgement from a ship's mizen, and its truth says so.
- **D10 stays (a):** an opt-in key whose yards the handling ignores. Reported to the lead under the brief's "a rig the engine lacks is reported".
- **D17 is taken with the brief:** two files. The razee's fits are the brief's "as razeed 1795" (Winfield p. 99's establishment, D17(b)'s fit) and the 1796 fit as carried (26 × 24-pdr, 2 × 12-pdr, 18 × 42-pdr carronades, 330 men: James vol. 1 p. 361). The default is the 1795 fit, as the brief names it. The owner may say otherwise.
- **D27 and D39 are taken with the brief:** the *Neufchatel* is an American vessel of 1812, with her names American by default. Her scenario's year, and the war's state in the table of nations, are for the design.
- **D18, the lead's reading for the design:** with D14(c), the viewer draws her true sides, sheer, wales and port sills from the hull profile, and no longer from the one deck line. The deck-height convention can then serve the physics and the spar heights alone. The design proposes against the owner's measure and shows the screenshots.

**Ruled on by the lead (2026-10-28, the brief as amended at `3e2c8d8`): all five accepted.**
- **The hull profile drawn in the viewer for every ship is in this package.** The pictures' tests are kept passing, any threshold that moves is re-pinned with the old figure beside the new, and package 81 starts from the drawn hull.
- **The lateen class and the yards under the bowsprit go under the lead's gate with the settee.** One design document for the three engine extensions reaches the lead before Phase 4. The physics' equations are not changed.
- **The lee ports are wired for every ship, with sourced sill heights, "as data honesty".** This is built only after 86's head is in. Every combat pin it moves is shown with the old figure beside the new, the reason, and the proof by bisection.
- **The settee tacking as a ship's mizen is within the settee's design.**

**Beyond the brief as first written, for the lead.** The owner's answers widened package 75 in five places, which the lead has ruled on as above:
1. **The viewer.** The brief says "the viewer itself stays at the current standard in this package" and, under "Not built here", "the viewer's hull (81's)". The owner's answer to D14 brings the sourced hull's drawing into 75, for every ship.
   - **The owner's reading (2026-10-27):** package 81 is booked for the gun ports, the guns, the muzzle flash and the smoke. Drawing the hull itself properly is booked to no package, so it comes to 75 without taking anything from 81.
   - The owner is confirming this with the lead.
2. **The lateen class** (D9), finished for the 64's mizen: its evolutions, its brace, its curve and its drawing.
3. **Yards under the bowsprit** (D8): new engine and viewer work. The engine note found that such a yard changes how a ship is classed and handled (Eng §5; §7, risk 2).
4. **The lee ports wired for every ship** (D12): every existing ship's combat pins move, and are re-measured old beside new.
5. **The settee's tack as a ship's mizen** (D3), within the settee's design, which goes to the lead under the brief's gate.

Items 2 and 3 extend the engine as the settee does. Their designs come to the lead beside the settee's, under the same gate.

This sheet gathers the questions the four research notes leave for you, merged where they ask the same thing, each with its options and evidence, a recommendation that keeps your rulings, and what depends on it. One question the notes did not ask is added as D48: where the 64 sails. You may accept every recommendation at once, or answer by number (for example "D9: a").

Notes cited, all in `docs/design/`: **Ind** Research-Indefatigable-2026-10; **Neuf** Research-PrinceDeNeufchatel-2026-10; **Bil** Research-Bilander-2026-10; **Eng** Research-ShipsEngine-2026-10. The marks (read, measured, catalogue, secondary, memory, judgement) are the notes'. Where a citation is the lead's own reading and is not in any note, it says so, with the OCR line.

## Part 1. The big decisions

They are ordered by what blocks the design most: the settee first, then the work across the engine and the viewer, then each ship's design, the speeds and the scenarios. Where the evidence argues against one of your rulings, or against your picture of a ship, the recommendation says so plainly.

### D1. How the settee goes about

Is the settee lowered and dipped round the mast, as the lug is? Or is it changed over without lowering, by peaking the yard up and down the mast, or left on one side with only the tack shifted? And is this done in tacking, in wearing, or both?

- **(a) Dipped.** Röding II col. 581 (c. 1795, read on the page image) groups the great sail of the bilander with the lug-sails, which must first be lowered and passed round. He is the only source that speaks of the bilander herself going about (Bil §1.5). Your ruling and your confirmation of 2026-10-17 say the same (`docs/dev/M7b-WorkPackages.md` l. 1056-1058). The engine's lug dip ran unchanged on a scratch bilander: she tacked in 200-250 s at 20 kn (the dip took 130 s) and wore in 529 s (Eng §4.4, observed).
- **(b) Changed by peaking.** The heel is passed abaft the mast and the tack hauled to the new weather side. This is how a ship's whole mizen was worked, and her yard copies that mizen (Steel 1794 I p. 220; Röding I col. 494, which calls it laborious; Steel 1794 II pp. 248*, 255*; Mainwaring pp. 187-188; Boteler p. 163; Willaumez p. 406). None says it of a bilander, and the English examples are mostly a century before the era. It needs a new evolution and a new drawn state.
- **(c) Left on one side, only the tack shifted.** Lescallier p. 390's two tacks and Röding's plate fig. 521 would allow it, and the late ship's half mizen was worked so (Bourdé 1765 pp. 91-92). No source says it of a bilander. On one board the sail lies against the mast, and a standing settee keeps drawing when she is hove to (she forereached at 2.7-3.6 kn in the trial).

Steel 1794 I p. 220, the era's one English text on her yard, says it "hangs to the main-mast, as a ship's does to the mizen-mast". The engine note reads this as a yard that is not shifted (Eng §4.2, judgement), which leans to (b) or (c). But the sentence says how the yard hangs, not how she goes about.

**Recommended: (a), in tacking and wearing both.** It is the only reading any source gives of the bilander going about. Steel's sentence says how her yard hangs, and Röding's own dictionary keeps her sail ("lowered first") apart from the mizen's peaking. His *Wenden* covers both evolutions, and the engine's dip already runs in both. It rests on one German dictionary, so her truths should pin what the period states, not a time: that the rig was inconvenient (Steel p. 220, "has proved inconvenient"; Röding II col. 581, inconvenient because the sail must be lowered and shifted in going about). Röding's "laborious" (I col. 494) is said of changing a mizen by peaking, way (b), not of the dip.

*Depends on it:* D2 (it rules out the lateen class), D3, D4 and D46; B3's evolutions; the viewer's drawing of which side of the mast the sail is on.

### D2. How the settee is built in the engine

Your ruling builds the settee "on the lug's yard and dipping machinery". Should it be a kind of lug, a new class that borrows the dip, or the unused lateen class finished?

- **(a) A lug variant,** with a flag that sends it to evolutions of its own. It reuses the dip, the sheet trim, the drawing from four corners and the penalty against the mast, with the least code. It needs a guard on every lug-keyed path: in the trial she took the lugger's way of getting under way and failed, and the heave-to, the gale and "furl" all catch her (Eng §4.4, §4.6).
- **(b) A new settee class.** It stays clear of the lugger's paths, but it needs about twelve additions (schema, curve, trim, vocabulary, evolutions, the viewer's rank and drawing), and it reuses the dip only by generalising it (Eng §4.7).
- **(c) The dormant lateen class.** The schema refuses dipping on anything but a lug, so the dip is lost. Its braced yard makes the bilander square-rigged by itself, and the viewer draws a lateen as a rectangle at a fixed tilt (Eng §4.7; `projection.js:612, 1067-1072`).

**Recommended: (a), with (c) ruled out.** (c) loses the dip that D1 and your ruling rest on, and (a) is the most literal reading of the ruling. Stage 0 lists every lug-keyed path (Eng §4.6, plus the untried rounding-to and shorten-sail paths) and keys each guard on the new flag, which the lugger's file never carries. The settee's design may still choose (b) if the guards prove too many.

*Depends on it:* B3 and stage 0's settee stubs; a second override key in evolution routing; the lugger's pins; D44 and D45; B5's drawing through `lugCut`.

### D3. When in a tack the settee comes down

Is it lowered as the helm goes down, as the game's lug is now? Or is it kept drawing to help her into the wind, and dipped once she is through it?

- **(a) As the lug now:** lowered at "helm's a-lee", then dipped and hoisted once she is through the wind. This is the dip as it stands (the trial's 200-250 s). Röding says only that the sail is lowered before it is passed round (II col. 581).
- **(b) As a ship's mizen:** kept drawing, with the heel's ourse braced to leeward as the helm goes down so that the after sail helps her round, then lowered and dipped last, after the head yards are swung (Bourdé 1765 p. 87; Steel 1794 II p. 316; Boteler p. 163). All of these are said of a ship's mizen, so carrying them over to the settee is judgement. It is the bilander note's truth candidate 3.

**Recommended: (a), the simpler build.** No source gives a bilander's order, and Röding fits either. (b) is the better-argued analogy and would make her truer in stays, but it needs a branch in the dip for the settee alone that leaves the lugger's pins where they are. If you want it, truth 3 pins it (D46).

*Depends on it:* B3's dip within the tack (`LugDip`); truth 3 (D46).

### D4. Heaving to

When the bilander heaves to, which topsail goes aback, and what becomes of the settee? Today the engine backs the mast with the most square canvas, which for her is the fore, and lowers a dipping sail, and she falls off.

- **(a) A file setting** that names the mast whose yards go aback: the main for her, and absent from every other file. The settee is clewed up aloft, as the engine already brails a square-rigger's after gaff sail. It follows "the main topsail to the mast", which the heave-to code itself cites (Luce 1866, later than the era; `scripts.py:504-508`).
- **(b) A rule instead of the setting** (the main first wherever it carries square yards). It needs no file key, but every existing ship's heave-to must be shown not to move.
- **(c) As now.** In the trial the settee was lowered, the fore topsail backed, and she fell off to 79-87° by 300 s. The brig, with her main topsail aback, lies 63-64° off at 1.4-1.8 kn (Eng §4.4).

**Recommended: (a).** It follows the rule the engine itself cites, and as an opt-in key it cannot move an existing ship. No source describes how a bilander lay to: the one account, the Gibraltar bilander of 1781, says only that she lay to to repair, names no sail, and her rig is uncertain (Bil §4, §6). So the settee's part is judgement, kept in line with how the engine treats a square-rigger's after sail. Every drawing gives her a main topsail, whatever D40 decides.

*Depends on it:* a new setting and the heave-to path (stage 0, B3), with the dipping-lug lowering there (`scripts.py:2241-2249`) guarded for the settee; B4's file.

### D5. The settee's cut, and where its yard is slung

Gwyn's English drawing has a short luff, so the sail is nearly a triangle, on a yard of about 45° that reaches from amidships to over the stern. Chapman draws a deep luff on a flatter, shorter yard. Which cut, and how far along the yard does it hang at the mast?

- **(a) Gwyn's, slung at a third.** Measured off PAG3828 (±10 px a point): the luff 0.16 of the leech; the leech and foot each 0.72 of the head; the yard at 44° and 0.72 of the length at the rail. Falconer 1780 (BILANDER) and Röding I col. 304 give the yard about 45°, from the middle of the ship to over the stern. Steel 1794 I p. 136's settee rule (the luff a fifth of the leech) and Kipping pp. 127-128 agree on the luff, but they are rules for a boat's settee. The yard is slung a third of the head from the throat, the point the viewer already pivots a lug on, so drawing and physics agree with no new field (`projection.js:370-376`; Eng §6.3). A third is within the sources: Chapman 0.32-0.33, and lateen yards slung at a third (Steel p. 237; Lescallier pp. 377-380).
- **(b) Gwyn's, slung at his own 0.395** (Lescallier fig. 7: 0.41), through a new per-sail sling setting that defaults to a third, so the lugger is unchanged. The difference is about 3 ft on a yard of 52-55 ft.
- **(c) Chapman 1768, Pl. LXII No. 5** (measured): the luff 0.46 of the leech, the leech 1.06 of the head, the yard at 35-36° and 0.54 of the length. It is the only bilander drawn to scale, but it is a generic, Swedish-drawn type, and on the yard it disagrees with every text (Bil §2.5).
- **(d) Lescallier 1791, Pl. XVII fig. 7** (measured, ±5%): the luff 0.39 of the leech, the yard at 32°. A schematic Dutch bélandre, good for ratios only.

**Recommended: (a).** It is the drawing your ruling names, and it agrees with the English and German texts. Gwyn's 0.16 is within his measuring error of Steel's 0.20, though the written support is a boat's rule. Slinging at a third needs no new setting. The corners keep the peak over the stern (on Gwyn about 0.09 of the length inside the taffrail), not abaft it, and give the sail's centre above the water, not above the deck; the scratch variant got both wrong.

*Depends on it:* B4's settee corners, area and centre of effort, which are all the physics reads of an oblique yard (Eng §4.3); the main lower mast (D6); the viewer's oblique yard; the polar and the balance; the sheet's lead (D45).

### D6. The bilander's size and spars

What tonnage is she, and where do her masts and yards come from?

- **(a) About 130 tons:** Elizabeth (Liverpool 1756) and the Bristol Duke of York (1762/63; the last bilander verified in the register, 1789) (read). Chapman's No. 5 works out at 118-128 tons (judgement), so his figures scale by only about 2%.
- **(b) About 140 tons:** Kerrison (Yarmouth 1778, the youngest verified; she drew 10 ft and carried six 4-pounders in 1781-83) (read).
- **(c) Chapman's spars, scaled.** It is the only bilander rig drawn to scale. But it carries more spar than his own Tractat rules allow (fore yard 41.9 Swedish ft against 34-36; bowsprit 28.5 against 22.9), and it stands taller than Gwyn's (the main top 0.53 of the rail length above the deck, against 0.35).
- **(d) The game's brig rules, scaled down** (Harpy's file: Fincham 1843 p. 88). The fore yard comes to 0.59 of the waterline, near No. 5's 0.578, but the lower masts are as tall for her length as Chapman's: Harpy's fore lower mast stands 46 ft above the deck on 88 ft of waterline (0.52), against Chapman's main top at 0.53 of the rail length, both far above Gwyn's 0.35 (judgement on the comparison).
- **(e) Gwyn's heights with Chapman's yards:** the mast heights from Gwyn's profile (main top 0.35, main truck 0.95 and fore truck 0.85 of the rail length above the deck; measured), and the square yards from No. 5's ratios to the waterline, which a freehand profile cannot give.

**Recommended: (a) with (e).** 130 tons matches Chapman's to-scale figure and sits in the middle of the register. Gwyn's 44° yard, slung just under the top with its heel a few feet above the rail, fits only his short main lower mast. On Chapman's mast or the brig's, its heel would hang about 20 ft above the rail (judgement), so the heights follow D5. If you take Chapman's yard in D5, take his whole rig here.

*Depends on it:* B4's hull and spars; the settee's corners; the polar, heel and spar rating; how she looks.

### D7. The bilander's hull

No lines of any bilander exist, and the game draws every hull with one shape. Should she take Chapman's proportions, or the game's brig hull scaled down?

- **(a) Chapman's No. 5** (measured): a waterline of 3.6 breadths (70.6 by 19.4 English ft at about 123 tons), with the rail 5.3-5.5 ft above the water. The draught comes from Lloyd's column for the loaded draught: 10-12 ft for bilanders of 120-140 tons, and 11 and 12 ft for the two of 130 (read). The rest (displacement, stability, lateral plane, speed) by the brig file's methods, marked judgement.
- **(b) The brig's hull scaled to her tonnage** (Harpy: 88 ft by 28 ft 1½ in, 3.1 breadths, flush-decked). The plan named this as the fallback "until the research finds better" (plan §1).
- **(c) Gwyn's profile at an assumed scale:** a raised quarterdeck from abaft the main shrouds, and freeboard in the waist 0.08 of the length. The drawing has no scale (the figures on her deck would make her about 290 ft long), so it gives her shape, not her size.

**Recommended: (a), drawing about 11-12 ft loaded at 130 tons.** The research has found the better figure the fallback was waiting for, measured to Chapman's own scale bar. Gwyn's raised quarterdeck, round windowed stern and figurehead go into her description. They show in the viewer only if D14 adds a hull setting.

*Depends on it:* B4's hull fields; her polar and stiffness; her hull speed (D24). The viewer reads only the length, beam and deck height (Eng §6.1).

### D8. Yards under the bowsprit, on every ship

Steel's 64 has a spritsail yard and a sprit-topsail yard, the bilander may have a spritsail yard, and the Neufchatel's plan draws a spar under the bowsprit labelled "the Jack". No ship file carries a bowsprit yard. Should any of the new ships carry one?

- **(a) None.** No account shows the razee setting either yard (Ind §5), and the frigate-36 she sails beside has none. What "the Jack" did is unknown (Neuf §8). This option costs nothing.
- **(b) Where the period shows them.** The 64 (Steel 1794 I p. 49: spritsail yard 57 ft 6 in, sprit-topsail yard 34 ft 6 in). The bilander (Steel 1794 Plate 1; Lescallier Pl. XXII fig. 8). The lead also reads, on the held 1560-px Gwyn image, a short spar crossing under the bowsprit near the jib-boom, with ropes from the jib-boom end to its near arm, that may be a spritsail yard. It is small and foreshortened, the bilander note records a spritsail yard on Gwyn as not seen (Bil §2.6), and it is not counted here until it is confirmed. Option (b) needs new engine and viewer work, because such a yard counts as a square-rigged mast for the helm, tack and heave-to. On the brig it became the only head yard, and "mainsail haul" swung the fore yards. It turned the topsail schooner square-rigged. It stayed set when she was hove to, gave negative thrust at 60° off the wind, and is drawn at the stem with its foot 2 m under water (Eng §5; §7, risk 2).
- **(c) As (b), and on the razee, and "the Jack" as well.** Whether the razee kept the 64's yards is open (Ind §10.4). "The Jack" is read at 8×, about 15 ft long as drawn, or 30 ft if drawn halved like the yards. Herald's spar list has a jack yard for a square sail of 25 ft (Chapelle p. 165).

**Recommended: (a), each file marking the departure where the evidence shows a yard.** The engine work is new, no ruling commissions it, and it is of the riskiest kind: a yard that changes how a ship is handled. If you want bowsprit yards later, they are one package for every ship. Plainly: the evidence leans towards the 64 (Steel p. 49) and the bilander (Steel's Plate 1; Lescallier's bélandre) having them; the lead's reading of a spar on Gwyn is not counted until it is confirmed. And your premise, that every sail but the settee is a type the game already has, does not hold for these yards.

*Depends on it:* a bowsprit-yard package, or none; the head spars of all four files; D9.

### D9. The 64's mizen

Steel's 64 of 1794 sets her mizen on a 77-ft lateen yard and has no gaff (1794 I p. 49, read twice). Neither the engine nor the viewer can carry a lateen yard today. Should the 64 have that yard, and if so on what, or a gaff like the frigate-36's?

- **(a) The lateen yard, as a second user of the settee** (D2), set on one side and not dipped. Steel says the mizen yard was "not often used, except in ships above 50 guns" (p. 207, page image). Lescallier says the bilander's settee yard is exactly a ship's mizen yard (p. 390), and the late ship's half mizen was left on one side in stays (Bourdé 1765; Röding; Bil §1.5). The 64's file would then wait on B3's stage-0 interfaces, as the bilander's does, and the settee would need an undipped mode on a square-rigger.
- **(b) A gaff mizen,** its spars by Steel's rule as for the razee (D20), with the design to say whether she has a boom. Nothing in the engine or viewer is new, and B1 stays independent, as the plan has it. It departs from Steel, for a ship that was never in commission as a 64 (Ind §1.4 V4).
- **(c) The lateen yard on the dormant lateen class, apart from the settee** (Eng §4.7, way 2). Neither reason that rules this class out for the bilander applies to the 64: her mizen is not dipped, so losing the dip costs nothing, and her mizen already carries square yards, so a braced yard there does not change how she is classed. It still needs set, take-in and trim evolutions; the yard taken out of the braced yards, or its brace given a meaning (today every brace order would brace it); `PEAK_COEFF["lateen"]`; a viewer branch (a lateen is drawn now as a rectangle under a braced yard at a fixed tilt: `projection.js:612, 1067-1072`); and tuning of a curve never tried (Eng §4.3, §4.7). It does not tie B1 to B3, but it is a package of new engine and viewer work.

**Recommended: (b), her file saying that the gaff stands in for Steel's mizen yard.** She never sailed as a 64, so her file serves chiefly as the razee's parent, and the razee had a gaff. A gaff sail stands in for the mizen in the physics, and what is lost is mainly the yard drawn before and above the mast (judgement). (a) would make the builder of the main goal wait on the riskiest builder. (c) would not, but it is engine and viewer work that no ruling commissions, for a ship that never sailed as a 64. Plainly: the evidence argues for the lateen yard, (a) or (c). Your premise that every sail but the settee is a type the game already has holds for the razee, but not for the 64 as Steel rigs her. (a) and (c) stay open as later packages, (a) once the settee exists.

*Depends on it:* whether B1 depends on B3 (under (a) only); the 64's mizen spar and sail; the razee's derivation (D20); under (a), the viewer's settee on a ship's mizen and an undipped settee mode; under (c), the lateen class's evolutions, brace and drawing.

### D10. The Neufchatel's main topgallant

Her sail plan of April 1815 and Reed's model show a small square topgallant at the main masthead, set on two light yards above the gaff topsail. Cobb has her main rigged as a schooner's. In the game, any square yard on the main makes her tack, wear, heave to and steer as a brig. Should she carry it, and how?

- **(a) On yards the handling ignores,** through an opt-in key in her file (stage 0 or B2). No existing file carries the key, so nothing moves. The yards are drawn about 34-35 and 24-25 ft long, 95.7 and 107.5 ft above the water, with a sail about 11.8 ft deep and 300 sq ft (measured, ZAZ6179; Neuf §1.2, §3.3). They match Fincham's main topsail and topgallant yards, 36.3 and 23.22 ft (p. 78). She is handled as a fore-and-after, as Cobb has her main: in one piece, with no top (pp. 38, 91).
- **(b) With no rule, and handled as a brig.** In the trial, a 30 m² main topsail raised the topsail schooner's tack from 149 s to 219 s, with a "mainsail haul". She brailed up the mainsail to wear, and hove to with the fore topsail aback, 68-70° off (Eng §3.3). In a gale the engine would take in her mainsail at the third reef, but on 28 December the Neufchatel kept a closely reefed mainsail (Cobb p. 95; `storm.py:370-411`).
- **(c) Leave it out.** She sails as a fore-and-after with a full square fore. In the trial she tacked in 149 s and made 7.1 and 8.1 kn at 70° and 90° (Eng §3.3). It loses about 300 of the some 10,300 sq ft drawn, about 3%.
- **(d) Fincham's 48.4-ft main square-sail yard as well** (p. 78), with a square main topsail in place of the gaff topsail. Her plan does not draw it, though some of the type had square main topsails (Chapelle pp. 102, 164).

**Recommended: (a); if stage 0 finds the rule costly, (c), not (b).** The sail is on her own plan. Her accounts handle the main as a schooner's, which (b) would contradict in every evolution and truth. The rule moves no existing ship and adds no sail type. Her own sail plan does not draw Fincham's 48-ft yard: his table crosses it, and his Ex. 1 is probably her, but his yards are proportions of the length, not her own spars (Neuf §3.1, §3.4). The gaff topsail beneath can be the engine's jib-headed one: its head spar is about 4.5 ft as drawn and cannot be made out at 1280 px, and Chapelle calls the American form nearly jib-headed (pp. 174-175).

Plainly: the main topgallant is a sail type the game knows, but carrying it as her plan does is not "fully implementable already", as your premise has it. One small yard on the main switches every handling path (Eng §3.3; §7, risk 2), so it needs a new opt-in rule in stage 0 or B2. Without that rule, (b) would have her handled as a brig and lose what you chose her for: a full square fore on a ship handled as a fore-and-after, "a combination no current file has" (Eng §3.3). Plainly too: the evidence makes her main not wholly fore-and-aft, which differs from your picture of her. Nothing in your ruling forbids it.

*Depends on it:* how the engine classes her masts (`physics/sails.py:852-866`, `scripts.py:472-479`: `_square_rigged`, `_masts_with_yards`, `working_yards`), and so the helm, tack, wear, heave-to and gale paths; truths T1, T4 and T5; the viewer, which draws the lower yard bare, as on the schooner's fore topsail. This is the engine note's risk 2.

### D11. Sweeps

She was pierced for sweeps, but no account shows her using them. Should rowing under sweeps become a new engine feature for her, or be left out?

- **(a) Leave them out, and record the sweep ports in her notes.** She has 11 small ports a side, one just abaft each gun port (measured, ZAZ6177), probably for about 22 sweeps (judgement; Chapelle pp. 95-96). On 10 October 1814 she lay becalmed off Nantucket with Endymion coming up. At sunset it fell calm and she anchored, the current setting her ashore, and no account has her sweep (T8: Niles vol. VII p. 120; Coggeshall p. 242; Stevens pp. 26-27; Maclay pp. 380-381).
- **(b) Build sweeping under way:** an evolution, crew stations and physics. The engine has no sweeps, no towing by boats and no warping (Neuf §8). The type swept often, at night when chased or attacking in light airs (Chapelle p. 13).
- **(c) Defer them** to a later package for all the clippers, with the ports recorded now.

**Recommended: (a), with (c)'s intent.** Her own accounts show none, and in the one calm recorded she did not sweep. Sweeping would be new engine work competing with the razee and the settee.

*Depends on it:* engine work, only if chosen; how she behaves in a calm in her scenario.

### D12. Lee ports shutting with heel

The spec has a lee gun port shut when the heel brings its sill within a foot of the water. The code for it exists (`lee_port_shut`) but is called nowhere, so the 64's lee lower-deck ports never shut today. Should it be wired?

- **(a) Leave it unwired in this build.** No existing combat moves, and the 64 fights her lee lower tier in any wind (`combat/shot.py:22, 48-53, 116-120`; Eng §2.6).
- **(b) Wire it for every ship** (M7 §9). The period evidence is mixed:
  - Cobb has the Neufchatel's lee guns mostly under water in the chase (p. 97), which fits a heel rule.
  - James has the Droits de l'Homme's lower-deck ports shut almost as soon as they were opened, in the sea of January 1797 (vol. 2 p. 14, OCR l. 1059-1066; the lead's reading, not yet in the Indefatigable note). But he gives the reasons: her ports stood 14 in nearer the water than most French 74s', and she rolled heavily for want of sail to steady her. That is rolling on an unusually low tier, not the steady heel the rule models.
  - The same night the razee fought her main-deck guns with "the People on the Main Deck up to their Middles in Water" (Gazette 13972; Ind §7.1 item 8), which tells against a rule that would shut her lee ports.

  And the existing ships' ports would shut at about 21° of heel in the frigate, 25° in the brig, 24° in the cutter and 11° in the privateer schooner, and this build may not move them.
- **(c) Wire it only in files that opt in.** It is faithful for the new ships, but the razee's main battery (sills about 6 ft 5 in above her water: Ind §2.3.7) would shut its ports, while the French frigate of the 36's file in her scenario never would.

**Recommended: (a), with the rule put forward as its own package for every ship, the pins re-measured once.** This is a stated simplification, one the evidence does not clearly condemn: Cobb supports a heel rule, James's Droits case is rolling on low ports, and the razee fought her main deck in that sea. (c) would handicap the razee, the main goal, against the very file her scenario sets against her.

*Depends on it:* combat for the 64, the razee and the Neufchatel; every ship's combat pins, if it is wired.

### D13. The false "Tacked"

The tacking routine can report "Tacked" for a brig-hulled ship that has fallen back onto her old tack: once she is through the wind, it never checks again. Should this build fix it?

- **(a) Leave it,** and judge every new truth by her heading and tack a set time after, never by the report. Nothing existing moves (`scripts.py:1129, 1218-1229`; `tack.yaml:50`; Eng §4.4, §7 risk 3).
- **(b) Fix it here.** That moves the brig's pins, and perhaps others', against the plan's rule that no existing ship's passages move.
- **(c) Fix it after this build,** in a package of its own, re-measuring the pins it moves.

**Recommended: (a) now, and (c) after.** In the trial the brig lay 148° off on her old tack, with sternway, when "Tacked" was logged at the 300-s timeout. A settee truth pinned on that report would pin the fault.

*Depends on it:* Phase 5's handling truths (D46); the tack script; the brig's pins, if it is fixed.

### D14. The viewer's hull

Keep the one generic hull every ship has, with no ports and one deck line, so that the 64 and the razee differ only in that line's height? Or add a hull setting, off for every existing ship, that draws the 64's two tiers of ports and the razee's cut-down sides?

- **(a) The generic hull, the current standard.** It is one lens shape in which only the length, beam and deck height vary, with no ports, wales, galleries, boats or guns (`projection.js:1416-1448`). The razee shows as a lower deck line and a lower rig. There is no viewer work (Eng §6.1-6.3).
- **(b) An off-by-default setting for ports and topsides,** set only in the new files. The view is sent no armament, deck or port data today, so B5 needs a new served field and new drawing, and three ships would be drawn above the standard your ruling names.
- **(c) The same setting for every ship, later,** as its own package. The existing ships' pictures would change.

**Recommended: (a), as your viewer ruling asks.** With D18, the razee's deck line stands about 1.4 m above the water, against the 64's 3.2 m and the frigate's 1.8 m, so her cutting down shows. Her real sides stood higher than the line drawn, as the frigate's do. Ports for every ship can be a later package; until then the Neufchatel's ports, and Gwyn's quarterdeck and stern, are not drawn either.

*Depends on it:* B5; the hull schema and `/api/ship`, if a setting is added; your screenshot checks.

### D15. What the game calls the Neufchatel's rig, and so her size class

The word also sets how lookouts describe her at a distance, and which size class captains rank her in. The rank is read from the words: the first of the size words found inside them wins, "brig" before "schooner" (`captains.py:296-315`). Her size class is decided here, not in D16.

- **(a) "Hermaphrodite brig".** It is the American usage of her day, used of her by Niles vol. VII p. 120 (29 October 1814), Cobb p. 38 and Coggeshall p. 241. Rankine defines it as a brig's bowsprit and foremast with a schooner's main (Chapelle p. 164). Steel 1794 uses the word for a different British rig (vol. I p. 220). The word "brig" in it puts her in the brig-sloop's size class, 2.
- **(b) "Schooner",** as the Admiralty's sheets of 1815 ("American Schooner", ZAZ6177, ZAZ6179) and Winfield pp. 335-336 name her. Fincham puts her type among the schooners, brig forward (pp. 72, 78). It puts her in class 1 with the privateer schooner, and she would then treat her scenario's brig-sloop escort as a superior force and keep away from it (`captains.py:1799-1815`).
- **(c) "Brig",** as her own log has it ("privateer brig", Stevens p. 26), with James vol. 6 p. 237, Emmons pp. 190, 200, Cobbett via Niles, and Cobb throughout. Class 2.
- **(d) "Brigantine"** (Cobb pp. 40, 117; Rankine's other name for the rig, Chapelle p. 164). But Lescallier 1791 uses it for a rig square on both masts (pp. 402-403). The word contains "brig", so it ranks as one, class 2.

**Recommended: (a) for her name and for her description once she is made out, and "a brig" for the lookout's word at a distance.** It is what her people and her country's press called her, it is exact, and it is your own word for her; British writers called her a brig. Either way, the word "brig" puts her in the brig-sloop's size class, 2. That suits 328 tons and 18 guns beside the brig-sloop Harpy's 316 tons (judgement).

*Depends on it:* stage 0's descriptions and size ranks (`world/ships.py:163, 205`; `world/captains.py:286, 296`, where "brig" is matched before "schooner"); the rig name in her file's header; the captains in her scenario.

### D16. Size classes, and the razee's rate

Captains judge a stranger by her size class: they keep away from a superior force and close with a weaker one. The frigate is now the top class, 3. Where do the new ships sit, and what rate is the razee given? (The Neufchatel's class follows from her words, in D15.)

- **(a) The 64 in a new class 4, the razee at 3, the Neufchatel at 2, the bilander at 1.** The 64 is described as a ship of the line, in a new class above every frigate. "Ship of the line" is already a man-of-war word, and her size word must come before "a ship" (`captains.py:286-306, 1799-1815, 3809-3813`). The razee is rated a 44, and described and ranked as a frigate. The Neufchatel goes with the brigs (D15). The bilander goes with the cutter and the lugger, her description carrying "merchant", so that a cruiser takes her for a weaker mark, to be chased and closed, whatever her class (`_weaker`, `captains.py:3809-3813`, used at 3720). The word also keeps a bigger merchant hull from counting as a superior force (`_overmatched`, 1810).
- **(b) The razee at 4 with the 64,** for her 24-pounders. She would then treat every frigate as weaker and run alongside it. And the rank reads a description, not a broadside (`captains.py:286-296`).
- **(c) The razee rated a 38,** as registered in 1795 for her long guns (James vol. 1 p. 454; Steel's List, January 1795), or a 40 (Steel 1809 and September 1816).

**Recommended: (a).** The razee was a 44 in Steel's List 1799-1802, the Naval Chronicle, the Navy List 1815-16, and James for 1805 ("the British 44-gun frigate Indefatigable", vol. 3 p. 311, OCR l. 16809; the lead's reading of the words, the note giving "the 44": Ind §8.3) and 1809 (Ind §4.1). James also calls her and Amazon "the two frigates" beside the 74 (vol. 2 p. 17). The 64 was a third rate, above the fifth-rate frigates. The Neufchatel's class follows D15. Stage 0 must also add the 64's and the razee's descriptions to the man-of-war sets and `role_for`, or they are not treated as King's ships (Eng §1.5; §7, risk 7).

*Depends on it:* stage 0 (`DESCRIPTIONS`, `SIZE_RANK`, `_SIZE_WORDS`, `MAN_OF_WAR_WORDS`, `_MAN_OF_WAR_DESCRIPTIONS`, `role_for`); the captains in all three scenarios.

### D17. The 64 and the razee: files, fits and complements

A fit changes only the guns and their powder and shot, never the hull, rig or crew (`Builder.armament`, `gen_ships.py:760-785`; `FIT_KEYS`, `schema.py:214`). How many files should there be, with which fits and how many men?

- **(a) Two files.**
  - The 64: her fit of 1784 as the default (26 × 24-pdr, 26 × 18, 12 × 9), and the class's additions of 1794 as a second fit (two 24-pdr carronades on the forecastle, six 18-pdr carronades on the roundhouse: Winfield p. 99; both are already in the generator's table). Her company is 491: the class's figure from 1794 (Winfield p. 99) and the 1806 Regulations' column for a 64 (p. 165). The 1784 establishment was 500, but a file carries one complement whatever its fits, so the 1784 fit sails with 491.
  - The razee: one fit, as carried: 26 long 24s, 2 long 12s and 18 × 42-pdr carronades, with 330 men and boys (James vol. 1 p. 361; 310 at first, then 330, p. 454). Her guns were the same in kind in January 1797 (vol. 2 pp. 16-17) and in 1805 (vol. 3 p. 313; ADM 1/2408/84, catalogue).
- **(b) As (a), with the razee's establishment of 1794 as a second fit** (26 × 24, 12 × 12, 6 × 42-pdr carronades: Winfield p. 99; the tables on ZAZ2371 and ZAZ2398). It is cheap, but James says none of the three razees went to sea with the established long guns: she "mounted but 28" (vol. 1 p. 454).
- **(c) The 64 with her 1784 fit only, and 500 men** (Winfield p. 99; Falconer, RATES). She was never in commission as a 64, and she was being cut down from September 1794, so the 1794 fit was the class's, never hers (Ind §1.4 V4, judgement).
- **(d) A third file, for the razee's first rig of 1794-95,** which a fit cannot carry. Two candidates:
  - Steel's spars for a 50 (1794 I p. 49), the only candidate that fits both Osler's "reduced in proportion" and the kit's 50's rig (judgement). Osler gives no particulars of the spars (pp. 107-108).
  - The 64's 77-ft lateen mizen yard for her first months. No account shows it on her, and the engine cannot carry it (D9).

  Osler says the plan reduced their rig and that all three proved slow and unmanageable; the Navy Board blamed the stowage of ballast and hold (p. 107). So her slowness would have to be tuned in. By Osler's dates, Pellew had altered her before her first cruise of March 1795 (pp. 107-110; judgement on the dates).

**Recommended: (a), with no first-rig file.** It follows your ruling of the 64 first and the razee derived from her, within what the engine allows. The razee's one fit is her armament in every action read from 1796 to 1805, so no year needs to be chosen, and James's statement goes in her notes. The 64's 1794 fit lets a later scenario sail her as a 64 of the class after 1794; where she sails in this build is D48. 491 is the column that her company's ratings come from, and the nine men's difference does nothing to her sailing. A first-rig file would cost a whole file, on spars that are judgement (or, with the lateen mizen, on engine work no ruling commissions), for a ship no scenario uses.

*Depends on it:* B1's module (the derivation; the fits; a quarter bill for each fit; the 64's exercise allowance of a third, by a per-file override: Eng §2.6); two people files; the regeneration test; the fit each scenario names; D48.

### D18. Which deck the heights are measured from

Every mast, yard, sail corner and gun height in a file is measured from its deck height, and the viewer draws that deck as her side. For the 64, is it her upper deck or her lower? For the razee, her gun deck (about 4 ft 6 in above the water) or her quarterdeck and forecastle (the 64's old upper deck, about 12 ft)?

- **(a) The uppermost continuous deck,** the frigate-36's rule (`frigate-36.yaml` l. 34-35; `gen_ships.py:1486`). That is the 64's upper deck, 3.2 m above the water, and the razee's gun deck, 1.36-1.42 m, since her waist has only gangways (Ind §2.3.5; ZAZ2375, measured). The engine note's cut-down table is built on it (Eng §2.4).
- **(b) The 64's lower deck (0.93 m) and the razee's gun deck.** This is the same physical deck in both files, so the derivation needs only her rise. But the 64 is drawn with a side under a metre high, lower than the razee's.
- **(c) The 64's upper deck and the razee's quarterdeck and forecastle (3.66 m),** the deck her course sheets and tacks work from. Again it is one deck in both, with the bowsprit drawn where it stood. But the razee is drawn as high-sided as the 64 she was cut from.

**Recommended: (a).** It is the convention the engine already carries, the frigate-36's own. Under it the drawn razee comes out lower than the 64 and the frigate (1.4 m against 3.2 m and 1.8 m); that follows from the convention, not from any source. James calls both frigates, Amazon included, comparatively low in the water beside the 74 (vol. 2 p. 17), so his remark does not set the razee below the frigate-36. The cost is the generic hull's: her side is drawn below her real waist rail, which stood about 3.5 m above the water, and her bowsprit is drawn rooted at the gun deck, about 7½ ft below where it stood.

*Depends on it:* every height in both files; spar windage and the deck wind's height; Δdeck in the derivation; the drawn freeboard and bowsprit (D14).

### D19. The razee's lower masts

When she took the 64's masts again, were the lower masts shortened at the heel by the height of the deck taken off, or kept at their full length?

- **(a) The heel cut, one deck,** measured at 6 ft 3 in-6 ft 9 in (judgement on ZAZ1280). That leaves lower masts of 94 ft 5 in, 83 ft 4 in and 79 ft 3 in, each head as high above her new upper deck as the 64's was above hers. This is the kit's account (your Vanguard notes, V11; probably Gardiner 2006, secondary); no period document was found. It brings her lower masts within about 2½ ft of Steel's 50's (the main 2 ft 5 in over the 50's 92 ft 0 in, the fore 1 ft 10 in, the mizen 6 in), which may explain the kit's other claim, that she first had a 50's rig (judgement).
- **(b) The 64's full lengths:** 101 ft 0 in, 89 ft 7 in and 86 ft 0 in (Steel 1794 I p. 49), with the whole rig about 6½ ft higher. Magnanime's catalogue entry speaks of a 64's masts and yards, but also of their being lost (ADM 1/2491/62, catalogue, self-contradictory).

**Recommended: (a).** It is the only account that speaks to the point, and no period source read contradicts it. It also follows the razeeing's own logic, the courses hanging over the lowered sides. It rests on the kit's text alone, and her file says so. In the engine it is one figure per mast (c in Eng §2.4), so either is as easy to build.

*Depends on it:* the razee's lower masts, yards, gaff and boom, and every corner and centre height; her heeling arm and the "stiffer" truth; how she looks beside the 64.

### D20. The razee's mizen

She had a gaff by April 1796. Which gaff and driver boom should she have, and should she have a boom at all? (A first-rig file with the 64's lateen mizen is in D17(d).)

- **(a) Gaff and boom by Steel's rule on the 64's own yards.** The boom is the main topsail yard's length, 65 ft 4 in, and the gaff five-eighths of it, 40 ft 10 in (Steel 1794 I p. 40). Every column of his p. 49 table that has a boom obeys the boom rule, but the table's gaffs run 0.64-0.72 of the boom (0.638 for the 44, 0.644 for the 38, 0.724 for the 50), so the gaff could as well be 41 ft 10 in at the 44's and 38's own ratio (Ind §3.2, §3.3). The gaff is read in the Virginie action, where she lost "her Gaff and Mizen-Top-Mast" (Gazette 13887 p. 388; James vol. 1 p. 361). The boom overhangs the taffrail by 33-34 ft.
- **(b) The 38's spars** (gaff 38 ft, boom 59 ft) **or the 50's** (44 ft and 60 ft 9 in) (Steel p. 49). These are other ships' spars. The 38's shorter boom would ease the overhang (judgement).
- **(c) A gaff with no boom, and the driver only later.** No source names a driver for her (Ind §5), and Steel has the driver set occasionally, in light fair winds. A file carries one rig, so "later" would mean a second razee file.

**Recommended: (a), for the whole of her file, the gaff at 40 ft 10 in by the rule (41 ft 10 in is a foot longer).** The gaff is the only after-rig recorded on her. Steel's boom rule is the period's own and holds across his table. That she kept the 64's yards to set them from is the kit's account; Magnanime's catalogue entry, the only other support, contradicts itself (D19). A spanker on gaff and boom is the frigate-36's arrangement, so nothing new is needed, and her sister Agamemnon set a driver in 1795 (Nicolas vol. 2 pp. 12-14). No source objects to the overhang. Note that the frigate-36's boom is 44 ft, by Luce 1866, so the razee's after sail will be relatively larger than hers.

*Depends on it:* the spanker's area and centre; her balance (`clr_x_m`) and weather helm; the truth of losing her after sail (Ind §7.1, item 6).

### D21. The Neufchatel's fore gaff sail

Her own sail plan makes the boomless gaff sail on the foremast large, not small. Should it be built to the plan, reaching just past the mainmast with its sheet shifted round the mast at every tack, or cut to clear the mast?

- **(a) To the plan, lapping the main.** The gaff is about 33 ft, the luff 38 ft, the leech 50 ft, and the loose, curved foot 47 ft, about 1,660 sq ft in all (±10%), as large as the fore topsail. The clew is 2.7-2.9 ft abaft the mainmast's line (measured, ZAZ6179; Neuf §1.2). She lay-to under this "fore-and-aft foresail" in the gale (Cobb pp. 33-34, 79). The topsail schooner already carries such a sail (`gen_ships.py:2821-2843`), and the tack already shifts its sheets (`evolutions/scripts.py:298`).
- **(b) To the plan, but cut so the clew stays before the mainmast.** The plan draws the leech dashed where it passes the mast, which may mean the sail laps the mast only in profile. Moving the clew about 3 ft forward costs a few per cent of its area (judgement).
- **(c) Small, as first understood.** No source read supports it, and Fincham's table for the type has an even longer fore gaff, 37.1 ft (p. 78).

**Recommended: (a).** It is her own plan, Cobb shows it was a working sail of size, and the engine and viewer already carry exactly this sail. Plainly: this differs from your picture of a small gaff sail (plan §0). The sources confirm the rig your ruling chose her for, but they make this sail large.

*Depends on it:* B2's foresail, on the topsail schooner's pattern; the polars on a wind. The viewer draws every gaff at 35°, where hers peaks at about 27° (judgement) and her main at about 24°. It also sets the foot 1.5 m above the deck, and draws this sail and the course overlapping on the one mast (Eng §6.1, §6.3).

### D22. The Neufchatel's guns

Which guns should she carry by default, and is a second fit wanted?

- **(a) 16 × 12-pdr carronades and 2 × 6-pdrs,** the 6s long guns (judgement), 18 in all (Winfield pp. 335-336, from Admiralty records, undated). The count agrees with three sources of December 1814: she sailed from Boston with 18 guns on 21 December (Niles vol. VII p. 284); Cobb, aboard, counts 18 (p. 39); and at her capture she was pierced for 22 and mounted 18 (Naval Chronicle vol. 33 p. 72). James vol. 6 p. 237 also gives 18 at the boat action in October. In October her captain double-shotted with 12-pound bags of musket balls (Stevens p. 27), which fits 12-pdr carronades (judgement).
- **(b) 18 guns "of nine and eighteen pounders"** (Cobb p. 39). Cobb was aboard, but he wrote in 1841, some 26 years later, and no other source gives these calibres.
- **(c) 17 guns in October 1814, after the summer cruise** (Niles vol. VII p. 120; Coggeshall p. 241), **or 14 by her log** (Stevens p. 26). Emmons also gives 17, undated (pp. 190, 200). No calibres are given.
- **(d) Any of these with a pivot gun.** The engine has one (`gen_ships.py:3607`), but no source mentions one for her and none is drawn. No deck plan exists, so the absence is weak evidence.

**Recommended: (a), as her one fit, with no pivot.** She was never commissioned, so the record most likely describes her as taken (judgement). Its count is borne out by three sources of December and James's of October, and its calibre by one, while Cobb's calibres stand alone. Where the 6s stand (as chasers or in the broadside) is the build's judgement: she had 11 ports a side and probably two stern ports (a tentative reading). Add a second fit only if a scenario asks for one.

*Depends on it:* B2's fit, quarter bill and magazine (both kinds of gun are in the generator's tables, `gen_ships.py:3435-3436`); her scenario's fight with the brig-sloop.

### D23. The Neufchatel's stiffness

Her metacentric height (GM) is in no source. The period's ratios make her far stiffer than the game's small ships. But in the chase she shortened sail before the frigates did, and her prize crew thought her over-sparred. How stiff should she be?

- **(a) About 2.0-2.2 m, then tuned by the truths.** Her metacentre is 1.59 m above the sailing-trim waterline (measured, ±0.5 ft; Neuf §2.5). Fincham's ratios give 2.12-2.51 m for naval brigs, corvettes and merchant brigs, which rests on his Ex. 1 being her (p. 19 with p. 72; judgement). The note's weight budget puts the centre of gravity about 2 ft below the waterline, which gives 7.2 ft (2.2 m), not the note's 2.3 m.
- **(b) 2.3-2.5 m,** the stiffer end of Fincham's classes (18-gun brigs 2.40 m, merchant brigs 2.48, corvettes 2.51), or 2.78 m if she is likened to a yacht schooner.
- **(c) Low, near the game's other small hulls** (the topsail schooner 1.0 m, the brig-sloop 0.95, the frigate 1.3; all judgement in their files). For it: she took in her lighter sails while the frigates held theirs (Cobb p. 96, T5), and her prize crew blamed the size of her masts and spars (p. 138, T7, weak). Against it: Cobb puts the frigates' advantage down to their strength and heavy dimensions (p. 96), which is size.

**Recommended: (a).** Every period-based estimate puts her well above 1 m, and no source supports a tender hull. The chase compares her with ships several times her size, so it is a test for the truths T1 and T5, not evidence of a low GM. At 2.0 m her righting moment per degree of heel is about 1.5 times the brig-sloop's (288 t × 2.0 against 413 t × 0.95). Whichever figure is chosen, it is judgement.

*Depends on it:* heel and sail-carrying; strain (truth 9); the polars; T1 and T5.

### D24. Speeds

There are no period knots for any of the new ships. What hull speed should each file carry? The frigate-36 has 13.0 kn (Winfield's 12-13 kn for 18-pounder frigates, per her file), and the topsail schooner and the brig 11.5 kn, by judgement.

- **(a) Start by judgement, and let pinned truths set the final figures.**
  - The starting figures:
    - the razee at about 14.0 kn, the frigate-36's 13.0 carried by the square root of the length (160 against 137 ft), tuned within about 13-14.5;
    - the 64 lower, at about 12.5-13.0 (judgement), not the length's 14.0, since the period ranks her under the razee and under a crack French frigate;
    - the Neufchatel tuned so that she makes about 12.5 kn running: once in the gale and heavy sea of the chase (Cobb p. 138, T2), and 12.5 "miles per hour" running out of Boston in a stiff breeze (p. 54, T3, the unit loose); about 10 kn under bare poles in the gale (p. 90, T4);
    - the bilander, for whom no source gives a speed or a time (Bil §4), at the brig's 11.5 kn carried by the square root of the length: about 10.3 kn on Chapman's 70.6 ft of waterline against Harpy's 88 (judgement), tuned by her truth 1 (she lies as close as a brig of her size) and her polar.
  - The razee: she ran Amazon (the frigate-36's own ship) and Concorde out of sight by evening, and caught the Virginie, called one of the fastest in the French navy, averaging 11.2 kn over the 15 hours of the chase, from lying to (Osler p. 125; Gazette 13887 p. 388; Ind §7.1 item 5). In January 1797 she was 7-8 miles ahead of Amazon (James vol. 2 p. 13).
  - The 64, by her sister: Agamemnon outsailed the line and the lesser frigates, but was outsailed by the Melpomene, France's fastest (Nicolas vol. 1 pp. 334-335, 346).
  - The Neufchatel: she held closer to the wind than the frigates and gained to windward of them (Cobb p. 96, T1, strong), but running in a gale and a heavy sea, they gained on her as she pitched (p. 97).
- **(b) Fix the figures now by judgement, without the truths:** the razee at 13.5-14 kn, the 64 at 12.5-13.
- **(c) Leave the Neufchatel at 11.5 kn,** the schooner's and the brig's type figure, below the frigate.

**Recommended: (a).** The figures stay judgement, as in every other file, and the truths set the order. The razee is clearly faster than the frigate-36, close-hauled and running large, and averaged 11.2 kn over the Virginie chase. The 64 is pinned as the Indefatigable note ranks her: slower than the razee, and slower than a crack French frigate (Ind §7.3, I12). Plainly: no account compares the 64 with Amazon or any British 36, and she outsailed the lesser French frigates. The game's only frigate file is the frigate-36, so to pin the 64 against it would be to make it stand for the Melpomene by judgement alone; the 64 against the frigate-36 is left unpinned. "Faster than the line" has no ship-of-the-line file to sail against. The Neufchatel is closer-winded than the frigates, and makes about 12.5 kn running. The bilander's figure is only a start for her polar. Hull speed is only one knob among several (displacement, GM, draught and the sail centres also count: Eng §2.5), so no figure is fixed before the polars are run. Two things are not pinned: her crew's opinion that she could outsail any ship in the Navy (Cobb p. 105, T6), and her damaged passage (T7). Whether the seaway can reproduce the run in a heavy sea is for the design to check: the engine models pitching, and added resistance only in a head sea (`physics/motion.py`).

*Depends on it:* `hull_speed_kn` in the four new files, with `gm_m`; the polars; Phase 5's truths (lighter, stiffer, faster; the best point of sailing); the chases in the scenarios.

### D25. The razee's scenario

The plan puts her on the Ushant station in a westerly, with a French frigate standing out of the Iroise. The one account read of the French standing out with her on that station (August 1805) has the wind north by east; the one westerly read near it was the Droits de l'Homme chase of 1797, with a 74 making for the French coast. Keep the westerly, change the wind, or move the scenario?

- **(a) Keep the westerly** (plan §3), the prevailing wind. No account read shows the French standing out in one (Ind §8.3).
- **(b) The same station, in August 1805, with the wind north by east, moderate and hazy,** as on 21-22 August 1805. On the 22nd she (under Rodd), being ahead, stood towards the Alexandre 80, which was leading the French fleet out in line of battle from its anchorage between Camaret and Bertheaume, and exchanged fire with her before tacking (James vol. 3 pp. 311-313). That wind rests on this one account (Ind §8.3, judgement on one account), and it was a fleet sortie of 21 of the line and 5 frigates. The scenario would borrow only that day's weather and place, with a lone frigate of the 36's file in the Alexandre's place. Her fit is the one as carried (D17).
- **(c) Off the Lizard, 20 April 1796, in a fresh south-easterly:** the Virginie chase, with Amazon (the frigate-36, as she is under your ruling) and Concorde in company. It is the best-documented action, and the source of truths 5 and 6 (Gazette 13887 p. 388; Osler pp. 125-128; James vol. 1 pp. 361-362; Clowes vol. 4 p. 497).
- **(d) The approaches to Brest, 13-14 January 1797, in a hard westerly and a rising sea, with Amazon in company:** the Droits de l'Homme chase and action (Ind §7.1 items 7-8, §8.2; Gazette 13972; James vol. 2 pp. 12-19). The frigates first saw her with Ushant about 50 leagues to the north-east, the wind "still from the westward" (James vol. 2 p. 12, OCR l. 977, 987; the lead's reading), and the action ended on the Penmarks. It is the one account read with a westerly near the station, and the source of truths 7 and 8. But the opponent was a 74 making for the French coast, not a frigate standing out, and the game has no 74's file: it fits the plan's westerly, not its opponent.

**Recommended: (b).** It keeps the plan's station and a French ship standing out of the Iroise, and changes the wind to the one the period gives for the French standing out with her there. Plainly: that wind rests on a single account, of a fleet led out by an 80, so the scenario takes only its weather and place. The westerly is in the plan's §3 table, not among your rulings. The one westerly read near the station, (d), had a 74 coming in, which no file in the game can play. The Lizard chase is the richer history, but it moves her off the station.

**The lead's view, against the sheet: (c).**
- It puts the razee and *Amazon*, both real ships the game holds, in company.
- It is the best-documented action of her career.
- It tests what the razee is: a chase in a fresh breeze, where she ran *Amazon* and *Concorde* out of sight and outsailed the *Virginie* on a wind. Truths 5 and 6 come straight from it.
- The 36's file stands in for the *Virginie* under French colours.
- The Lizard is the western Channel, which the game already sails.

(b) borrows one day's weather for a skirmish that no account gives her.

*Depends on it:* B6's scenario: the pinned weather, the positions, the French frigate's course out, and the fit and date it picks; D48.

### D48. Where the 64 sails

(Numbered after the rest, so that they keep their numbers.) The plan's §3 gives the razee's scenario "the 64 as a second fit or a second scenario". Under D17(a) the 64 is a file of her own, which a fit cannot carry, and your ruling gives one scenario each. Should she sail in any scenario?

- **(a) In the razee's one scenario, by the drivers' own choice of ship.** The drivers already take a ship file given on the command line over a scenario's (`make_scenario_world`, `world/scenarios.py`: "the ship the command line's, else the file's"), so the razee's scenario can be sailed in the 64 with no second scenario file. The razee has one fit (D17), so her scenario need name none, and the 64 then sails with her own default; a fit named that a file lacks is refused (`ArmamentSpec.fit`, `ship/schema.py:576-581`). The French frigate's captain will take a 64 of class 4 for a superior force (D16), so the scenario plays differently with her, which is an outcome, not a fault. B6 checks it, and a truth can round-trip it.
- **(b) A second scenario of her own.** It needs your leave, since your ruling gives the Indefatigable one.
- **(c) The harbour only,** where every ship file is listed (`ui/harbour.py:82, 382`) and where you sail each ship after the merge (plan §6).

**Recommended: (a), within "one each".** Plainly: the plan's "second fit" is impossible under D17(a), since a fit changes only the guns and their stores.

*Depends on it:* B6's scenario (it names no fit); a scenario truth with the 64's file; D17's 1794 fit.

### D26. The bilander's age, home port and trade

Is she an old vessel still sailing in a rig that was going out of use? And what are her home port and trade for the Falmouth to Plymouth passage?

- **(a) An old survivor.** The rig was rare by 1769 (Falconer) and "seldom used but by the Dutch" in 1794 (Steel p. 220). The 1806 Art of Rigging repeats Steel word for word, so it is not fresh evidence for 1806. The last register entry verified is 1789. The register's code for the rig went out in 1790 with others, which is a change in the register, not proof of the rig's end (Bil §2.2). The register carried vessels 23 to 32 years old (Princess of Wales, built 1744, in 1776; Hopewell, 1749, in 1779; the Duke of York, 1762/63, in 1789).
- **(b) Out of Poole,** in the Newfoundland trade or coasting: Diana, Hopewell, Speedwell and Vigilant in Lloyd's (read), and the George of Poole (1762) and the Nancy of Poole (to 1778) in TNA's catalogue. This is the West Country's group of bilanders. Poole lies east of Plymouth, so the passage is on her way home (judgement).
- **(c) Yarmouth to Cork** (Kerrison): a short-sea trade whose Channel route passes Falmouth and Plymouth (judgement).
- **(d) A London-Rotterdam constant trader** (Twyman's eight, the largest group) **or an Irish Sea coaster** (Bristol-Dublin). Both are well attested, but neither trade passes along that coast.

**Recommended: (a) and (b), an old survivor out of Poole.** Her file stays undated, as you ruled, and its notes say plainly that the rig was rare and that the last verified entry is 1789. Poole is her type's strongest West Country connection, and it puts the passage on her road home. For the scenario's date, a summer early in the range (1793-1795) keeps her nearest the evidence (judgement).

*Depends on it:* her scenario (its date, cargo and port, and what the lugger means); her description and notes.

### D27. The Neufchatel's scenario

The plan has her as a French privateer of about 1805 in the western Channel. Her own war was as an American privateer in 1814, partly in those same waters. Keep the plan's setting?

- **(a) The plan's setting:** a French privateer of about 1805, and a convoy under a brig-sloop working up from the Lizard. The era ruling lets a scenario give her any flag and year. The game's table of nations stands at June 1805, with Britain at war with France (`data/nations.yaml`).
- **(b) Herself, an American privateer of 1814.** In August and September she was in the Channel and the Irish Sea, where she took many prizes and sank a brig by broadside on 21 August (Niles vol. VII p. 120; vol. VIII p. 111). In the spring she was sending prizes into France (Niles vol. VI pp. 150, 368). But the table has the United States at peace with Britain, so the war of 1812 would have to be added, outside this build.

**Recommended: (a), which your rulings already cover.** Plainly: she did not exist in 1805 (she was built in 1812-13), and her own Channel cruises were American, in 1814. A scenario of 1814 must wait for dated wars in the table of nations, whose dates are from memory and still to be checked, as its header says.

*Depends on it:* B6's scenario; her names list (D39); the table of nations.

## Part 2. The details

### The Indefatigable

#### D28. The razee's waterline

Should the razee float on the line drawn on her razeeing draught of September 1794, or a little deeper, by Osler?

- **(a) ZAZ2371's line,** 1.45 ft below the 64's: 19 ft 3 in aft to the main keel and 19 ft 10 in to the false keel, measured to ±0.25 ft on the 1280-px image. All the note's figures for the razee rest on it (displacement about 1,870-1,925 tons, the lateral plane, the rudder, KM). That it is her intended load line is inference: no label was read (Ind §2.3.1, §2.3.3).
- **(b) 1.2 ft below the 64's:** Osler's "nineteen and a half feet abaft" on 7 May 1795 (p. 111). It is her own draught at sea after Pellew's alteration, here counted to the main keel, as Steel counts a 64's (judgement). It gives about 40 tons and 40 sq ft of lateral plane more.

**Recommended: (a).** It is the Navy Office's own drawing of her as razeed, measured at both ends, and Osler's single figure, counted to the main keel, lies within its ±0.25 ft. The difference, about 3 in of draught and 2% of displacement, is too small for any truth to detect: this is the better-documented reading, not a decisive one.

*Depends on it:* her draught, displacement, lateral area and rudder; δT, her rise in the derivation (Eng §2.4); every height above the water; the "lighter" truth.

#### D29. The false keel, the draught's datum and the length (the 64, the razee and the Neufchatel)

Should the lateral plane and the draught count the half-foot band under the keel (probably a false keel) and the knee at the bow? And which length goes in the file? The Neufchatel's keel bottom is open in the same way (Neuf §2.3, §8).

- **(a) The band and knee in the lateral plane, the draughts to the main keel's lower edge.** Steel's 64 has a 5-in false keel (1805 Folio I), and his printed draughts for a 64 match the load line to the main keel within 0.05 ft aft (judgement), so this is the period's way of stating a draught. The lateral plane is then 305.5 m² for the 64 and 283.4 m² for the razee (Ind §2.3.6), with mean draughts of 6.15 m and 5.71 m. For the Neufchatel, the draughts come out about 0.5 ft less than in D38 (her main keel's lower edge is probably the faint line), and her lateral plane stays at 102 m². But the engine grounds a ship when `draught_m` passes the charted depth (`world/chart.py:1079-1097`), so every hull, the Neufchatel's included, would ground about half a foot late, and the lateral plane and the draught would stand on different lines.
- **(b) The band and knee in both, the draughts to the band's bottom** (6.33 m and 5.88 m mean; for the Neufchatel 3.16 m, as D38 has it). That is the deepest wood, which is what grounds, and one datum serves both fields. It raises the wetted-area estimate L(1.7T + 0.7B) (`ship/parts.py:1797`) by about 1.5% for the Indefatigable and about 2.5% for the Neufchatel. The Neufchatel's note takes her draughts this way.
- **(c) The band in neither:** 298-299 m² and 276-277 m² (Eng §2.4). That the band is a false keel is itself judgement (Ind §10.7).

The length, whichever datum is chosen:
- the 64 and the razee: 48.8 m moulded, rabbet to rabbet at the 64's load line; or 50.2 m (49.9 m at the razee's line) outside the post and stem, the knee included (Ind §2.3.6, §2.4);
- the Neufchatel: 32.7 m between the rabbets, or 33.6 m over the post and the gripe (Neuf §2.4, §2.9).

**Recommended: (b), for all three hulls, with the lengths rabbet to rabbet (48.8 m and 32.7 m).** The band and knee resist leeway, so they belong in the lateral plane. The draught the engine reads is the one that grounds her, so it is taken to the same deepest line. The period's draughts to the main keel (Steel's convention, and Osler's 19 ft 6 in as D28 reads it) go in the notes beside the file's figure. The cost is about 1.5-2.5% of wetted area. The knee is a fin, not length. The datum is a judgement either way, and it moves the draught by half a foot. The measured fullness of 0.97 (the area over the immersed length times the draught) stands, against the frigate-36's 0.85, which is judgement.

*Depends on it:* `lateral_area_m2`, `draught_m` and `length_waterline_m`; leeway and balance against the frigate-36; grounding; the wetted area; D38.

#### D30. The razee's quarterdeck ports and her two long 12s

For 1796, did her quarterdeck have six ports a side, as her 1794 plan draws, or seven, as the kit reports? And where do the 18 carronades and the two long 12s stand?

- **(a) Six a side** (ZAZ2375, measured and checked). With the forecastle's six, that makes 18 ports for the 18 carronades exactly. The two 12s go as a pair of bow chasers: the kit calls them chasers (Ind §4.1), and that they are bow chasers is the build's judgement. The generator's chasers helper places such a pair at the bow or the stern (`gen_ships.py:3588`).
- **(b) Seven a side,** the kit's fourteen, reported as twice mentioned by the Admiralty but not seen (V9). That gives 20 ports for James's 20 pieces on the quarterdeck and forecastle (vol. 1 p. 361), and fits the two extra 12s of 17 February 1795 (Gardiner via Wikipedia, secondary). The seventh port's place would be judged.
- **(c) Six a side, with the 12s on the broadside** among the carronades. James counts one 12 in her broadside of 23 (vol. 1 p. 362), but he halves every gun and places none.

**Recommended: (a).** Her own plan holds the 18 carronades exactly, where the kit's fourteen rests on documents not seen. The kit calls the 12s chasers; placing them at the bow is the build's judgement, for a ship whose record is mostly as the pursuer. The engine models no ports, so only the guns' positions and the 12s' arc change.

*Depends on it:* her gun list, quarter bill and magazine; her broadside and chase fire.

#### D31. Her guns and their crews

Which 24-pounder does she carry (Adye p. 155 gives 9 ft 6 in and 49½ cwt, 9 ft and 47½, or 10 ft and 52), and which 12? And are her gun crews counted by the period (Falconer and Douglas: 11, 7 and 4) or by the generator's rule (12, 9 and 6)?

- **(a) The 9 ft 6 in 24-pdr of 49 cwt 2 qr, the generator's 34-cwt 12, and the 42-pdr carronade at 22 cwt 1 qr (Adye p. 72), with crews by the generator's rule.** The generator's weights for the 18 and the 12 are Adye's 9 ft 6 in guns (Eng §1.4; its comment calls them 9 ft, which affects the comment only). A 64's lower deck usually had that length (memory, unverified). Every existing file is crewed by the rule (`gen_ships.py:3438-3455`, a judgement reading of Douglas).
- **(b) The 9-ft or the 10-ft 24-pdr, and a short 12** (7 ft 6 in-8 ft 6 in, 29¼-31½ cwt; judgement). No source names her patterns (Ind §6.4, §10.10).
- **(c) Crews by the period:** Falconer's 11 men to a 24-pdr and 7 to a 12 "when the ship is well manned" (1780, QUARTERS), and Douglas's 4 to any carronade (2nd ed. 1829, art. 136, later than the era). That makes 186 men for one broadside of 1796 (13 × 24, 1 × 12, 9 × 42), against the rule's 219 with (a)'s 34-cwt 12 of 9 men (the note's 218 counts a 32-cwt 12 of 8: Ind §6.3).

**Recommended: (a).** It follows the pattern the generator already uses, and no source names her own guns. The note leans to a short 12 for her two chasers (7 ft 6 in-8 ft 6 in, 29¼-31½ cwt, 8 men by the rule: Ind §6.4); (a) departs from that lean for the generator's pattern, which changes only the crew and the cycle time. The crews stay on the rule because the frigate-36 she sails and fights beside is crewed by it, and the guards forbid changing existing files. Falconer's and Douglas's figures go in her notes as the period's check. The rule runs one man over Falconer on the 24, two on the 12, and two over Douglas on a carronade: a correction to make in every file at once, if you want it. The gun's weight sets only the crew and the cycle times, never her stability.

*Depends on it:* new keys, 24 in `LONG_GUN_CWT` and 42 in `CARRONADE_CWT` (byte-safe); the crews, the quarter bill and the hands left for sail at quarters; combat cycle times.

#### D32. The razee's company

How is her company of 330 made up? Should her officers and petty officers come from the 1806 Regulations' column for a 44 (her rate) or for a 50 (nearest her numbers)? And how many marines does she carry?

- **(a) The 294 column, the 44's** (Regulations 1806 p. 165): 3 lieutenants, 8 midshipmen and 11 quarter gunners, with the 36 men over it as seamen. The frigate-36's posts carry over. The 20 men Pellew asked for in 1796 were added hands (ADM 1/1718/297, catalogue).
- **(b) The 343 column, the 50's:** 4 lieutenants, 10 midshipmen, 13 quarter gunners and a few more petty officers. It is nearest her 330 (Ind §4.2).

The marines: 7 officers and NCOs by either column. No establishment of private marines was found (Ind §10.8). The frigate-36's 40 in 264, scaled to 330, gives about 43 privates. Falconer's 50 small-arms men for a fifth rate is a proxy only.

**Recommended: (a), with about 50 marines (7 officers and NCOs and about 43 privates), the privates marked judgement.** Every list rated her a frigate. Her men over a 44's establishment were hands for her heavy guns, not officers (judgement on the 1796 request), and the frigate's posts carry over unchanged.

*Depends on it:* the complement, posts, stations and people file; the marines in the quarter bill (Eng §7, risk 11); victualling.

#### D33. Ground tackle

Which anchors and cables should she carry: the 64's allowance, which her unchanged hull suggests, or a 44's?

- **(a) Steel's 64:** four bowers of 57 cwt, a stream anchor of 15 cwt, a kedge of 7 cwt 2 qr, and 21-in bower cables (Steel 1794 I, the anchor and cordage tables, page images). His table runs by rate and tonnage, and her burthen stayed 1,384 tons, against his 64's 1,369.
- **(b) Steel's 44:** four bowers of 40 cwt and 17½-in cables. It is her rate from 1799, but the table sizes it for a ship of 879 tons.
- **(c) The generator's rule:** 5 cwt of anchor to every 100 tons (Luce 1866) and half an inch of cable to a foot of beam (judgement). That gives about 69 cwt and 22-in cables (`gen_ships.py:494-530`).

**Recommended: (a), in both files.** It is a period table read on the page, and anchors answer to the hull's mass, which was the 64's less about 240 tons. The generator's later rule comes out a fifth over Steel's own 64. The new module writes Steel's figures without touching any existing file.

*Depends on it:* the ground tackle in both files; anchoring and holding only.

#### D34. The 64's stated particulars

Should the 64's stated particulars be the design's or her own as built?

- **(a) As built:** 160 ft 1¼ in on the gun deck, 131 ft 10¾ in on the keel, 44 ft 5 in, 1,384 3/94 tons (Winfield p. 100; 1,384 tons also in James vol. 1 p. 362).
- **(b) The design:** 160 ft 0 in, 131 ft 8 in, 44 ft 4 in, 1,376 47/94 tons (ZAZ1407's table and ZAZ1279; Charnock 1802 vol. III p. 251).

**Recommended: (a), since they are her own figures.** The measured lines stay as measured, unscaled: the differences lie inside the measurement's own ±0.15 ft, and the engine cannot tell the two apart.

*Depends on it:* the notes; `beam_m` (13.54 m extreme); the tonnage that the anchor and boat rules read.

### The Prince de Neufchatel

#### D35. Her light sails

Which light sails should she carry: the studding sails on the fore, and the large main topmast staysail? ("The Jack" is decided in D8.)

- **(a) The lower and topmast studding sails on the fore, and the main topmast staysail.** The studding-sail booms run out 16.1 ft beyond the fore yardarm and 6.9 ft beyond the topsail yardarm. The lower studding sail is drawn solid, about 19 by 35 ft; the topmast one is dashed; none is drawn on the main. The staysail's foot is dashed at two heights, 45 and 73 ft above the water (all measured, ZAZ6179; Neuf §1.2). The engine has studding sails and their booms (`schema.py:362, 394`).
- **(b) As (a), with the topgallant studding sails and the other dashed light sails.** These are only partly made out at 1280 px (Neuf §1.2, §8).

**Recommended: (a).** These sails are drawn on her plan, and the engine already carries them. The build picks one of the staysail's two drawn feet and marks it. It rigs the three headsails drawn (fore staysail, jib, flying jib); the count is tentative.

*Depends on it:* B2's light sails; the running polars (T2 and T3 were runs).

#### D36. Her company

How many men should she carry? A fit cannot carry a complement (`FIT_KEYS`, `schema.py:214`), so her file has one, whichever guns she carries.

- **(a) 130:** "from Boston, 18 guns, 130 men" (Niles vol. VII p. 284, 31 December 1814). Collier's report as reprinted gives 130 (seen only in a snippet). Emmons gives 127, undated (p. 190), and Wikipedia 129 at her capture (secondary).
- **(b) 163 "all told"** (Cobb p. 39), from a memoir. "All told" may count officers and boys that the press figure leaves out (judgement).
- **(c) About 150, "probably", when she left New York** (Coggeshall p. 241), or about 80 (Maclay p. 378).
- **(d) 33 to 38,** after manning prizes in October 1814 (Niles vol. VII p. 120; Stevens p. 27). That was a moment in a cruise. A scenario cannot set a smaller crew (`core/world.py`), so it would need a second file.

**Recommended: (a), 130.** The press of the day gives it, the captors' report agrees as far as it was seen, and Emmons is close; Cobb's 163 is one man's memory.

*Depends on it:* the complement, quarter bill, stations and people file; her stores and water.

#### D37. Her spars: her own sheets or Fincham

Her sail plan and Fincham's spar table for the type differ in a few places. Which should the build follow?

- **(a) Her own sheets, with Fincham only for spars they do not draw:** the fore gaff 32.9 ft, the royal yard about 24.5 ft, the drag 33 in (ZAZ6177), and rakes of 12.4° on the main and 10.3° on the fore (measured; Neuf §3.2).
- **(b) Fincham's Ex. 1 throughout:** the fore gaff 37.1 ft, the royal yard 21.3 ft, the drag 24 in, and rakes of 33 and 28 in in 12 ft (pp. 72, 78). Ex. 1 is very probably her, or the Woolwich copy of her, but Fincham does not name it (Neuf §3.4, judgement).
- **(c) Her sheets, but Fincham's figure where a proportion looks wrong.** The royal yard as measured (±1.5 ft) is 0.94 of the topgallant yard, where Fincham has 0.8.

**Recommended: (a).** The sheets were drawn from her at Deptford, while that Ex. 1 is her is inference. The yards' agreement with Fincham adds no weight, because the drawn yards were judged to be half-lengths partly on his evidence (Neuf §1.2). The royal yard's odd proportion is noted, not changed.

*Depends on it:* B2's spar lengths and heights; the sail corners; the drag and rakes.

#### D38. How deep she floats

Her lines carry a waterline marked as her sailing trim; another vessel's proportions would put her deeper aft. Which should the file use?

- **(a) The sailing trim drawn on her lines:** 11 ft 8¾ in aft and 9 ft 0 in forward to the bottom of the false keel, 10.36 ft mean, about 288 t ±10 t. ZAZ6177 carries the note "Draught of Water when in sailing Trim", and ZAZ6179 gives about 11.8 and 9.25 ft independently (Neuf §2.3, §2.5). Cobb has her lying low in the water (p. 38). In December she was cleared below for prize goods, keeping only water and provisions (p. 40).
- **(b) About half a foot deeper,** by the note's own weight budget: about 315 t for 130 men, 18 guns and stores, some 27 t over the drawn trim, at 4.8-4.9 tons an inch (the budget is judgement).
- **(c) Mammoth's proportions** (Marestier; Chapelle pp. 112-113). On her beam they give about 8.9 ft forward and 14.3 ft aft, 11.6 ft mean (12.5 ft if scaled by length), not the "about 13 ft" in the note's question. Her forward draught already matches Mammoth's, so the whole difference is aft.

**Recommended: (a).** The waterline was drawn on her own lines by the officers who took them off, and the note's weight budget finds it plausible, perhaps a little light. The keel bottom is the scale bar's border, as the note takes it, since the gripe and the rudder heel run into it. D29 decides whether the file's draught is counted from there or from the main keel above it: under D29's recommendation, from there, 10.36 ft (3.16 m) mean; under D29(a), from the faint line, about 9.9 ft.

*Depends on it:* her draught, displacement, lateral area and deck height; the polars; `clr_x_m`.

#### D39. Her hands' names

Her file must name one list of names for her crew, and that list sets her nation whenever a scenario names none. Your ruling gives her file no nation. Which list?

- **(a) The French list.** It already exists and needs no engine change. Her two captains of 1814 were Frenchmen (Stevens p. 27; Cobb p. 41), and her one scenario is French. She keeps French names when a scenario sails her as an American (`crew/muster.py:168-174`).
- **(b) American names.** She was owned in New York (Niles vol. VII p. 120), the press and her captors called her American, and most of her December crew were Americans (Cobb p. 108). This makes the United States her default.
- **(c) A mixed privateer list, as her companies were.** In October she had a French captain and a Swedish first mate (Stevens p. 27). In December her crew were Irish, English, French, Spanish, Portuguese, Dutch, African and American (Cobb p. 42, OCR l. 1533-1534; the lead's reading, not in the Neufchatel note), with five or six French and Portuguese messing apart (p. 108). This is data only, plus one line in stage 0 mapping the list to a nation; without that line it defaults to Britain (`world/nations.py:39, 153-155`).
- **(d) A scenario setting that picks the names along with her nation,** on the pattern of the fit setting. This is stage-0 engine work (Eng §3.5; `core/world.py:244`), and the 29 scenarios that set a nation are unchanged.

**Recommended: (c), mapped by default to France, as the plan's scenario has her, with the mix weighted by judgement on Stevens and Cobb.** It suits a privateer under any flag, for the cost of data and one line, where (a) gives her a French crew under every flag. Plainly: no option leaves her file wholly without a nation, since the schema requires a list and any list implies a default nation. (d) is the step to take if a scenario ever sails her as an American, and a test can require every scenario that uses her to set her nation. Her people file should fix no nationality in its outlines (the topsail schooner's, for example, makes her master a Baltimore man: `data/people/topsail-schooner.yaml:25`).

*Depends on it:* `data/crew/names.yaml`; `NAMES_TO_NATION` in stage 0; her people file.

### The bilander

#### D40. The main dry yard and the topgallants

Should the main mast carry a bare (dry) yard under the top for the main topsail's sheets? And which upper sails should she set on her two masts?

- **(a) A dry yard under the main top.** Gwyn's PAG3828 has one (on the held image, the main topsail's clews come down to its arms), and so do Lescallier's Pl. XVII fig. 7 and Pl. XXII fig. 8. Steel 1794 I's BRIG article, next to BILANDER, says that English brigs carry no main yard but a crossjack yard (the lead's reading of the OCR only, l. 24728; not in the bilander note).
- **(b) No dry yard.** Chapman's No. 5 draws none, and the main topsail's clews come down to the top (measured).
- **(c) Royals as well, as the game's brig carries.** No drawing has a royal. All of them have topgallant sails or yards on both masts (Gwyn, Chapman, Steel's Plate 1, Falconer 1769 Pl. XII, Lescallier fig. 8).

**Recommended: (a), with topgallant sails on both masts and no royals.** Gwyn is the drawing your ruling names, Lescallier agrees, and Steel's brig shows the English practice; only Chapman draws no dry yard. It costs no new engine work: the trial bilander kept a dry yard, and her main counts as square-rigged through its topsail yard either way (judgement on Eng §4.4). B4 checks the braces at "mainsail haul" (Eng §7, risk 2).

*Depends on it:* B4's main spars; how the viewer draws the main topsail's clews.

#### D41. The armed merchant fit

For the armed merchant fit, which guns, and how many swivels?

- **(a) Four 3-pounders:** Elizabeth, 130 tons, in Lloyd's for 1779 and 1782 (read on the row images). The generator's table already has the 3-pounder.
- **(b) Six 4-pounders:** Kerrison, 140 tons, in 1781-83. The 4-pounder is in the table too.
- **(c) Two 2-pounders:** Essex, 160 tons, in 1781. The 2-pounder would be a new key in the gun table, byte-safe (Eng §1.4).
- **(d) The merchant brig's four long 6-pounders** (`gen_ships.py:4174-4215`). That fit is a judgement for a brig of about 300 tons, twice her size, and it has no swivels.

**Recommended: (a), with four half-pounder swivels on the rail, two a side.** Elizabeth's guns are the fit recorded on a bilander of D6's tonnage. No British source counts a bilander's swivels and the register has no column for them, so four is judgement: it is the privateer schooner's provisional figure in the generator (`gen_ships.py:3995`). Your ruling's "as the merchant brig's" is read as the pattern of a few small guns. Plainly: the register shows 2- to 4-pounders on bilanders, not the merchant brig's 6-pounders.

*Depends on it:* B4's armed fit, its magazine and its quarter bill.

#### D42. Reefing the settee

How is the settee reefed: by one reef band along the foot, as a lug is, by the old mizen's way of "balancing" (rolling up the peak), or both?

- **(a) One reef band parallel to the foot,** about a fifth of the leech up. Lescallier fig. 7 has it at about 0.22 (there it might be a bonnet's lacing), Chapman No. 5 at 0.16-0.19, and Steel's Plate 1 near the foot (measured, ±0.05). Steel 1794 I p. 136's settee rule puts the reef at a fifth.
- **(b) The balance:** the yard lowered a little and the peak rolled up, about a fifth in from the yard-arm (Falconer 1780, BALANCE; Lever 1808). Steel 1794 II p. 245* says that balancing is peculiar to a ship's mizen and to mainsails extended by a boom.
- **(c) Both:** the reef for a fresh breeze and the balance for a gale. No source gives either for a bilander.

**Recommended: (a).** All three drawings and Steel's settee rule agree, and the lug already reefs this way. By Steel's own account the balance belongs to other sails.

*Depends on it:* B3's settee reef, on the lug's pattern; the reef band in the viewer; how she shortens sail.

#### D43. Her company

How many men does she carry?

- **(a) About 7 to 9** (the note's judgement). The merchant brig's rate of five men to 100 tons (`gen_ships.py:6491-6520`) gives 6 or 7 at 130-140 tons, and a settee dipped by hand at every tack wants the upper figure.
- **(b) About 10:** the Nancy of Boston, 170 tons, had 10 men in 1779 (HCA 32/405/21, catalogue). She is a doubtful bilander, and those were her American crew.
- **(c) The merchant brig's rate exactly:** 6 or 7.

**Recommended: eight, in both fits.** A fit cannot change the crew. No source gives a bilander's company in wartime (the letters of marque in HCA 26 were not searched), and eight leaves hands for the dip. The build should check how the lug's six-hand evolutions, and a square sail's take-in and furl at ten and twelve hands, run with a company of eight (Eng §4.1, §4.5).

*Depends on it:* B4's crew and stations; the time each evolution takes; the armed fit's quarter bill.

#### D44. The settee's curve of lift and drag

Which curve of lift and drag should the settee sail on?

- **(a) The lug's** (lift peaking at 1.2 at 35°, a luff angle of 18°). It comes with D2's way and needs no new key. It is untuned, like every lug, lateen and sprit curve (`data/sail_classes.yaml`; TuningNotes l. 127).
- **(b) The lateen's:** about 4% less lift, a little more drag and furled windage (0.08 against 0.06), and the same luff angle. It is also untuned, and under D2's way it would need a curve key (`sail_classes.yaml:93-104`).
- **(c) A new settee curve,** tuned to the period's claims: that lateen sails lie a point nearer the wind than square sails (Steel 1794 I p. 237; Lescallier p. 380), and that they are more liable than the lug to be taken aback (Fincham 1843 p. 59).

**Recommended: (a),** with her truths deciding whether it needs tuning: she should lie no worse than the square fore, and the settee should press the mast harder when aback. No source gives a figure, and the two existing curves differ by a few per cent, with neither tuned. Neither curve carries Fincham's claim, since both have the same luff angle.

*Depends on it:* B3 (nothing new under D2's recommendation); her polar and truths.

#### D45. The settee's ropes

Lescallier gives the settee a peak lift (the derrick), a peak brace (the English vangs), two heel ropes (the ourses, the English bowlines), tacks to windward and a sheet to the taffrail. In the engine, a fore-and-aft sail's trim is held by its sheet alone. Which of these ropes should do anything?

- **(a) The lift, vangs and ourses carried as lines,** for the yard's strength rating, with no order to work them; the sheet holds the trim, as on the lug. The engine never reads a fore-and-aft yard's slope, so an order would move nothing (Eng §4.2, §4.3, §6.1; Bil §1.2, §1.4).
- **(b) Orders that work the vangs and the ourses:** close-hauled, the heel hauled to leeward by its ourse and the peak drawn to windward by the vangs (Bourdé p. 87; Steel 1794 II p. 316; Falconer, VANGS). This means new orders, and physics that reads the yard's angle, with no period figure to tune it.
- **(c) As (a), with the sheet led to the taffrail** in the trim (`trim.py:274-279, 371-396`) and drawn there. The view now leads it to the lee rail, 1 m abaft the clew (`projection.js:1309-1315`).

**Recommended: (a), with (c)'s taffrail lead made part of B4's lines and B5's drawing.** Your ruling, "set and clewed up as Lescallier gives it", is met by the new evolutions for setting, taking in and furling aloft, and by the sheet led to the taffrail as Lescallier leads it (p. 390), which is part of setting the sail, not an option. With D5's corners the clew lies about a fathom inside the taffrail (judgement on Gwyn's measured tack and foot), so the trim's block one fathom abaft the clew (`trim.py:274-279`) already falls near it, and B4 checks that it does. The drawing needs a settee branch that leads the sheet to the taffrail in place of the lee rail. The lines take the bilander note's names (the ourses and the vangs), not the plan's "two vangs". Whether the peak rope is filed as a vang (not drawn, not loaded) or as a brace (drawn, and loaded with 0.3 of the sail's force) is the build's choice.

*Depends on it:* B4's lines, the sheet's lead included; B3's trim; B5's drawing of the lines and the sheet.

#### D46. Her handling truths

The bilander note gives five handling rules (Bil §4):

1. She lies as close as a brig of her size, or a little closer (Steel 1794 I p. 237; Lescallier p. 380).
2. Going about costs her more time and hands than a brig (Steel p. 220, Falconer, Röding), and it costs her ground, as it does a lugger (Steel p. 221).
3. In stays, the ourse goes to leeward and the yard is changed last (Bourdé, Steel II, Boteler).
4. In wearing, the settee is clewed up, and set again once the stern is past the wind (Steel II pp. 321-322).
5. Aback, the settee presses the mast harder than a square sail does (Fincham 1843 p. 59).

Which of them become pinned truths?

- **(a) All five, as written.**
- **(b) All but rule 2's comparison with the brig,** which is pinned on her own dip instead: that the yard is lowered and passed round, and by how many hands. The brig hull logs "Tacked" on a timeout (D13), and in the trial the brig "took" 466 s against the settee's 200-250 s, so a truth against the brig would fail, or would pin that fault.
- **(c) Only rules 1 and 5 now,** with the going-about truths held until the false "Tacked" is fixed.
- **(d) Rules 1, 2, 4 and 5, fitted to D1 and D3:**
  - rules 1 and 5 as written;
  - rule 2 pinned on her own dip, as in (b);
  - rule 4 reworded to the dip: in wearing, the settee is lowered and dipped as she bears up, and hoisted again on the new lee once the stern is past the wind (Steel II pp. 321-322's order for a ship's mizen, carried over by judgement). The truth pins the order of events, not a clewing up, since D1's dip lowers the yard to the deck in the wear ("Lowered the mainsail to dip them; hoisted on the new lee 123 s later": Eng §4.4);
  - rule 3 only if D3(b) is chosen. Under D3(a) the settee is lowered at "helm's a-lee", so its ourse is never braced to leeward.

**Recommended: (d).** Answering "D3: b" brings rule 3 back. Rule 4 as written would either fail against D1's dip or force a clewing up the build does not do. Each rule rests on texts about the ship's mizen, the lug or the lateen, so each truth says that it is carried over by judgement. Each is measured on B4's file, not on the trial's scratch bilander, whose settee was 175.7 m² on the 316-ton brig hull, against Chapman's measured 92 m².

*Depends on it:* Phase 5's truths and pins; the tack and wear of B3 and B4; D1 and D3.

### All three ships

#### D47. The full-resolution images

You ruled against buying full-resolution Greenwich images, and asked whether anything would be missed. Is anything?

- **(a) Buy none, as ruled.**
  - The Indefatigable (Ind's image key, §1.2, §10.16):
    - her load line, bow lines, ports, profile below water, lateral plane and rudder were measured on the free, public-domain Commons originals of ZAZ1407 and ZAZ1279 at 100 px to the foot, and the rest of her lines on ZAZ1407's 3840-px Commons copy (14.5 px to the foot);
    - her decks, masts and heels on ZAZ1280's 3840-px Commons copy (19.9 px to the foot);
    - the razee's waterline on ZAZ2371 (6.1 px to the foot), and her gun deck, quarterdeck and ports on ZAZ2374 and ZAZ2375 (7.5-7.6 px to the foot), all Greenwich's free 1280-px images.
  - The Neufchatel: her 1280-px figures agree wherever they can be checked. Her length agrees between her two sheets within 0.6 ft. Her draughts are 11.73 and 8.98 ft on ZAZ6177, against about 11.8 and 9.25 ft on ZAZ6179. Her deck measures 110.8 ft, against the table's 110 ft 8 in. Her masts and booms fall within about 3% of Fincham's Ex. 1 (the yards' match is partly circular).
  - The bilander: nothing she needs waits on a paid image.
- **(b) Buy ZAZ2371 alone.** It would settle D28 to a few hundredths of a foot, and read the razee's dimension table and its December 1794 note.
- **(c) Buy ZAZ6177 and ZAZ6179.** They would give her dimension tables (the principal dimensions are already in Winfield pp. 335-336) and the sailing-trim figures. They would also show the dashed light sails and the number of headsails, the gaff topsail's head, the deck fittings, the step in the deck line, the year in the title, and which line is her keel bottom (Neuf §8). Commons holds no free copy.

**Recommended: (a); the evidence does not argue against your ruling.** For the Indefatigable, what would be missed is about 3 in of the razee's draught, a tentative hold depth (13 ft 3 in), a date, ZAZ1953's illegible tables, her ports' positions within half a foot, and the roundhouse's height. For the Neufchatel, it is a few inches of draught, which light sails are drawn and how many headsails, the shape of the gaff topsail's head, and the keel bottom's datum: the scale bar's border or the faint line above it, half a foot of draught and about 5% of the lateral plane (Neuf §2.3, §8). Each is marked. None moves a figure the engine reads beyond the build's own margins, except the keel datum, which D29 settles by convention on the note's reading. The only open point that might later justify a purchase is the Neufchatel's headsail count, if the unfinished check of her sail area against Fincham comes to turn on it. The bilander's open gaps lie in free sources still to be read: Steel's Art of Rigging Pl. 10 and a clearer Plate 1, the right half of Chapman's plate, and TNA's letters of marque.

*Depends on it:* nothing in the build; the sources lens's marks.

## The notes' questions, decision by decision

| Decision | The notes' questions | Also from |
|---|---|---|
| D1 How the settee goes about | B1, E2 | Eng §4.2, §8.8; plan §2, Phase 2 |
| D2 How the settee is built | E1 | |
| D3 When in a tack the settee comes down | | Bil §1.5, §4 (truth 3) |
| D4 Heaving to | | Eng §8.11 |
| D5 The settee's cut and sling | B2 | Eng §8.9 |
| D6 The bilander's size and spars | B3 | plan §2, Phase 2 |
| D7 The bilander's hull | B4 | |
| D8 Yards under the bowsprit | I7; E7 (the bowsprit yards); N3 ("the Jack") | Ind §3.1; Bil §2.6 |
| D9 The 64's mizen | E7 (the 64's mizen yard) | Ind §3.1; Eng §4.7 |
| D10 The Neufchatel's main topgallant | N2, E5 | Eng §8.7; plan §2, Phase 2 |
| D11 Sweeps | N9 | |
| D12 Lee ports | | Eng §8.5 |
| D13 The false "Tacked" | | Eng §8.13 |
| D14 The viewer's hull | E4 | |
| D15 The Neufchatel's rig name and size class | N7; E6 (her rank) | |
| D16 Size classes, the razee's rate | E6 | Ind §4.1; Eng §8.16 |
| D17 Files, fits and complements | I5, I6 (a first fit's lateen mizen), I13, E3 | Ind §4.1; plan §2, Phase 2 (the armament year) |
| D18 The deck heights are measured from | I3 | Eng §8.2 |
| D19 The razee's lower masts | I4 | Eng §8.1 |
| D20 The razee's mizen | I6 (the gaff and boom) | |
| D21 The Neufchatel's fore gaff sail | N1 | plan §2, Phase 2 |
| D22 The Neufchatel's guns | N4 | |
| D23 The Neufchatel's stiffness | N10 | |
| D24 Speeds | I12 | Neuf §2.9, §6; Bil §4 |
| D25 The razee's scenario | | Ind §8.2, §8.3 |
| D48 Where the 64 sails | | plan §3; D17 |
| D26 The bilander's age, port and trade | B8 | |
| D27 The Neufchatel's scenario | | Neuf §5.1 |
| D28 The razee's waterline | I1 | Eng §8.1 |
| D29 The false keel, datum and length | I2 | Neuf §2.3, §2.9, §8; Ind §2.4 |
| D30 The razee's ports and long 12s | I8 | |
| D31 Guns and gun crews | I9 | Eng §8.3 |
| D32 The razee's company | I10 | |
| D33 Ground tackle | I11 | |
| D34 The 64's particulars | I14 | |
| D35 The Neufchatel's light sails | N3 (the studding sails and staysail) | |
| D36 The Neufchatel's company | N5 | |
| D37 The Neufchatel's spars | N6 | |
| D38 How deep the Neufchatel floats | N8 | |
| D39 The Neufchatel's hands' names | E8 | Neuf §5.3 |
| D40 The dry yard and topgallants | B5 | |
| D41 The armed merchant fit | B6 | |
| D42 Reefing the settee | B7 | |
| D43 The bilander's company | | Bil §2.8 |
| D44 The settee's curve | | Eng §8.10 |
| D45 The settee's ropes | | Eng §8.10 |
| D46 The bilander's handling truths | | Bil §4 |
| D47 The full-resolution images | N11 | Ind §10.16 |

Every one of the notes' questions is answered above: I1-I14 (Ind §11), N1-N11 (Neuf §9), B1-B8 (Bil §7) and E1-E8 (Eng §9). D48 answers one they did not ask: where the 64 sails, now that the plan's "second fit" cannot carry her. The rest of the engine note's open items (Eng §8) are left to the build, either settled by a source or the code, or to be investigated there:
- items 4 and 12, settled: the 64's exercise allowance, a third by the 1806 Regulations (Gunner, Art. XXI) through a per-file override, while the razee keeps a fourth; the getting-under-way guard, a fault to fix whatever is chosen, keyed so that the lugger's path is unchanged;
- items 6, 14 and 15, to be investigated in the build: the 66-gun quarter bill with no marines in its divisions (B1); the untried paths (B3); the polar cache's size;
- items 17 and 18: nothing to decide.

Every ship file, the bilander's included, must also carry navy rations (`tests/test_stores.py`), as the merchant brig's does.
