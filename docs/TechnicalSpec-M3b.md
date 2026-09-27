# FreeSail: Technical Specification, Milestone 3b (Rig geometry and canvas)

Companion to `docs/TechnicalSpec-M0-M2.md` and `docs/TechnicalSpec-M3.md`, whose conventions hold. This chapter closes the open items that gates M2 and M3 left about *how close a ship can point and why*, and about *what canvas is and how it fails*. Its research base is `docs/references/RigGeometryNotes.md` (Fincham 1843, Steel 1794, Lever 1808, Kipping 1847, Luce 1866/1884, and the tables in `docs/references/Tables.md`); read it first, because the numbers here come from it.

Owner's rulings that shape this chapter (gate M3 close, 2026-09-26):

- The historical record is the truth to compare against; the engine meets it through the physics and the parts wherever it can; a hard-coded rule only where the model has nothing to stand on.
- Bowlines are in from the start. Costly practices come as a pair with their counter.
- Suits are not a type: a sail has a canvas number and a condition, the sail room holds sails, and "best" and "second" fall out of wear. Storm sails are different parts.
- Data values are research first, judgement second, and every value names its source. Where the sources are silent (channel breadths), the measured behaviour is the data and the geometry waits.
- A short gate with the human verification step.

## 1. What milestone 3b proves

Three things:

1. **Pointing emerges.** How close each ship lies is the product of her brace limits (from Fincham's measured angles by class), the flatness of her canvas (bowlines hauled, new or worn cloth), her trim (after yards sharper than head yards), her way (full and by against pinching), and her leeway, not a number in a file. The frigate about six points, the schooner nearer five; Fincham's short ship with her catharpins swifted in, sometimes five.
2. **Practices have prices.** Swiftering in the catharpins gains a point of bracing on that mast and weakens it athwartships until eased. Bowlines hauled flatten the sail and cost hands at every brace. Carrying studding sails too close flogs them and strains their gear. Bracing one yard away from its neighbours fouls the gear between them.
3. **Canvas is a thing.** Every sail has a canvas number from period practice and a condition that wears with use. Worn canvas in a squall goes before its spar; new heavy canvas holds until the spar goes. The sail room holds spare and heavy-weather sails, and storm canvas is bent before a blow.

**Compatibility rule.** The seventeen milestone 2 truths and the six of milestone 3 keep passing, with these allowed movements only: truth 1 (close-hauled angle) and truth 2 (close-hauled speed) may move by up to half a point and half a knot once the brace limits are re-sourced and bowlines exist, and the gate report records the new values. Nothing else moves. The milestone 3 crew compatibility test (one evolution alone with the watch, to the tick) stays exact.

## 2. Brace limits from Fincham (package 21)

### 2.1 The data

Each yard's `brace_limit_deg` (from square, as now) is re-sourced. Fincham's Hardy-squadron numbers, converted from the keel to square:

| Ship | Main yard | Fore yard | Could lie |
|---|---|---|---|
| Long, fine 28-gun ships (1827) | 61° to 67° | 60° to 64° | seldom within six points |
| The short ship, measures taken to brace sharper | 69° to 73° | 62° to 65° | sometimes within five points |
| Don Juan, close-hauled all sail | 61° | | |

The frigate (a long ship of 1795, coppered, well found) takes the long ships' upper values for her lower yards: main 64°, fore 62°, mizzen (crossjack) 60°; each yard above its lower yard two degrees more, as now, because the shrouds converge aloft. The schooner's fore yards keep their present values unless package 21 finds Chapelle contradicts them. Every value's comment names Fincham art. 102.

### 2.2 Head and after yards

`trim sails` today braces every yard to one angle. Fincham art. 94: on a wind the after yards are braced sharper than the head yards by two to four degrees, "so that the whole of them are so trimmed as just to touch at the same time"; art. 96: with a sea on the weather bow or much way and a griping ship, the reverse. The trim order and the tack script's final trim brace the main and mizzen yards `AFTER_YARDS_SHARPER_DEG = 3` sharper than the fore when close-hauled, both within their limits; `brace ... sharp up` on the whole ship does the same. A modifier `head yards sharper` reverses it for the griping case. Truth 24 measures the gain.

### 2.3 Full and by, pinching

Fincham art. 99: sails kept "just lifting" is proper only with five or six knots of way; with less, keep them full. The helmsman's `keep her full` and `full and by` already exist; package 21 adds the physics consequence, which the model mostly has (lift falls off past the luff angle) and checks that a frigate pinched at three knots loses more than one kept full, as a truth (25), tuning nothing unless it fails.

## 3. Catharpins (package 21)

Per `RigGeometryNotes.md` §2. Each lower mast gets a `catharpins` state in the ship (an attribute on the mast, `swiftered_in: bool`, default false) and two orders, `swifter in the catharpins on the main` / `swifter in the catharpins` (all lower masts) and `ease the catharpins`, each an evolution of the boatswain's party (the forecastlemen and the carpenter's and boatswain's crews, `aloft: true` for the men in the rigging, about twenty minutes a mast: judgement, no period timing found).

Effects while swiftered in: the lower yard's brace limit on that mast rises by `CATHARPIN_GAIN_DEG = 4` (the upper yards' limits unchanged, since the topmast rigging is not touched); the mast's athwartships rating falls by `CATHARPIN_RATING_FACTOR = 0.85` in the strain model, so that a mast pressed hard on a wind with the catharpins in is nearer carrying away, and the log warns as for any overloaded spar. Both constants are judgement, named, and are the gate's to judge; the direction is Fincham's and Lever's.

## 4. Bowlines (package 21)

Bowlines become parts on the courses and topsails of both ships (the frigate's courses already have them; the generator adds the topsails' and the schooner's fore topsail's, each with its bridles as one line part of class `bowline`, sided). A bowline has a `hauled: bool` state. Orders: `haul the weather bowlines` (also `steady out the bowlines`, `haul the fore bowline`), `let go the bowlines`, `ease the bowlines`. Hands: four forecastlemen or afterguard per bowline, on deck, a minute.

Effect: a sail whose weather bowline is hauled, while braced up on that tack, has its `luff_angle_deg` reduced by `BOWLINE_LUFF_GAIN_DEG = 4` (a flatter weather leech points closer, Fincham art. 98 and Luce line 28443), and its drag at the luff a little lower. The tack and wear scripts let the bowlines go at "helm's a-lee" and "up mainsail" and re-haul them when braced up on the new tack; `brace in` past `BOWLINE_SLACK_ANGLE_DEG = 40` from square slacks them (they cannot be kept hauled off the wind). The log says "Steadied out the weather bowlines." Truth 26 measures the gain, expected about half a point.

## 5. Adjacent yards, from geometry (package 21)

Spec M0–M2 §12 item 8, and spec M3 §9 (the whole-mast backing rule covers the common case). The constraint is computed, not tabulated: for two yards on one mast with a sail set between or on them, the difference of their brace angles may not exceed the angle at which the upper sail's foot (its clews at the lower yard's yardarms) would cross the lower yard's lifts, taken as `ADJACENT_YARD_MAX_DIFF_DEG` from the yard lengths (the shorter yard's half-length over the longer's gives the arc), with a floor of 10° so that the small trims of §2.2 always pass. A brace order that would exceed it is refused with the reason in words ("The main topsail yard cannot be braced so far from the main yard while the topsail is set; brace the main yards together, or clew up the topsail."); the aback rule (whole mast) and the studding sail rule (below) are checked first so that nothing is refused twice for two reasons.

## 6. Canvas, condition, wear and the sail room (package 22)

### 6.1 Canvas number and rating

Every sail in the ship file gets `canvas_no` by the rule in `RigGeometryNotes.md` §4 (courses and topsails 2, mizzen topsail 3, topgallants 4 and 6, royals 8 and 9, jib 2, flying jib 5, staysails 3 to 7 by height, lower studding sails 5, topmast 6, topgallant 7, storm canvas 1; the schooner by the same heights). The cloth rating is derived: `cloth_rating_kn = CLOTH_KN_PER_M2_NO2 * strength(canvas_no) / strength(2) * area`, with `strength` the crosswise figures of Luce App. E (`Tables.md`), so that the present ratings (tuned at milestone 2 for No. 2 courses and topsails) are unchanged for No. 2 canvas and the light sails become lighter in proportion. The generator comments each value with its number and source.

### 6.2 Condition and wear

`Sail.condition` (0 to 100, already a field) now falls with use: `CLOTH_WEAR_PER_HOUR_SET = 0.05` while set and drawing, three times that while flogging or aback, plus the strain model's decay above rating as now, and nothing while furled or in the sail room. The effective cloth rating is `cloth_rating_kn * (0.4 + 0.6 * condition / 100)`, so a sail at half condition bears seventy per cent of its rating and the same squall that a new sail rides out blows an old one out of the bolt-ropes. Blow-out stays at `BLOW_OUT_RATIO = 1.8` of the *effective* rating. A worn sail is also baggier: its `luff_angle_deg` rises by `BAGGY_LUFF_DEG = 6 * (1 - condition / 100)`, the other half of Fincham's "the flatter the sails the sharper they may be braced".

Nothing repairs canvas in 3b (the sailmaker's mending is milestone 8), so the only remedies are shifting to the spare and keeping the best for a blow.

### 6.3 The sail room

`crew.stores.spare_sails` (a count) becomes a list of sails: each with the kind of sail it is (`fore.topsail`), its `canvas_no` and its `condition`. The frigate's sail room, from Luce's allowance: a second of every sail at condition 100 in the working number, plus the heavy-weather foresail and fore and main topsails of No. 1. The schooner's: a second foresail, fore topsail and jib. `shift the fore topsail` (package 19's evolution) now chooses the best spare of that kind, or the one the order names (`shift the fore topsail for the heavy one`, `bend the No. 1 fore topsail`), and the unbent sail goes back to the room with its condition. `muster` gains a sail-room line; a new query `the sail room` lists it.

### 6.4 Storm canvas and the obscure kit

New parts in the frigate file, each with its gear and No. 1 canvas: a fore storm staysail (on the fore stay, set in place of the fore topmast staysail), a mizzen storm staysail, and a storm mizzen (a small gaff sail bent to the spanker's gaff and mast in place of the spanker; Luce's "storm mizzen"). In the schooner: a storm trysail on the main and a storm jib, judgement. They are ordinary sails to the physics; the storm staysails' evolutions `set`/`take in` as jib-headed sails; the storm mizzen requires the spanker unbent (`shift the spanker for the storm mizzen`).

And, pulled forward from milestone 8 because the generator is open and the studding sail rule now exists, the occasional light-weather sails, placed where the sources put them (owner's question at the 3b review; `RigGeometryNotes.md` §8):

- **The frigate** gets a **ringtail** abaft the spanker of the boom-and-gaff kind (owner's clarification): a quadrilateral sail bordering the spanker's after leech, its head on a short yard or gunter hoisted to the gaff end and its foot hauled out on a ringtail boom run out on the driver boom, as Kipping describes a brig's ("sets like a topmast studding sail, outside of the after-leech of the main-trysail", line 26611) and Luce's "ring-tail, which sets abaft the spanker" (1884 line 29072); and a **save-all** under each lower studding sail boom (Luce, same passage). Falconer's 1780 ring-tail, "a small triangular sail, extended on a little mast ... on the top of a ship's stern", is the older form for ships whose driver had no boom, in effect a yawl's mizzen, and is not built. No water sail by default: Steel says only that "some ships have a water-sail, similar to a sloop's", and the owner's reading, that it was a fore-and-aft vessel's sail and often jury-made from an old jib, stands. The format allows one on any ship.
- **The schooner** gets a **ringtail** on the main boom (Falconer: "as in all sloops, brigs, and schooners ... of the same depth with that part of the main-sail upon which it borders"; Steel 1794, "Sloop's ringtail sail", No. 5 or 8 canvas, "occasionally hoisted abaft the mainsail in calm weather"; Kipping: No. 5 or 6, a sliding-gunter ringtail boom run out on the main boom) and a **water sail** under the main boom (Steel, "Sloop's water-sail"). Steel's *save-all topsail*, a small square sail under a cutter's topsail, is a different sail and waits for the cutter (milestone 8).

Each with its halyard, tack and sheet as a studding-class sail subject to the wind rule (§7); data only; the physics treats them as studding sails.

### 6.5 The gale truths

Truth 27: the gate M2 gale (35 knots, all sail) blows out a worn royal (condition 50, set in the scenario) before its yard goes, and a new royal loses its yard first, as at milestone 2. Truth 28: with the storm staysails set and the topsails close-reefed in 45 knots the frigate lies a-try under a knot and a half with nothing carrying away for an hour.

## 7. Studding sails through the physics (package 23)

Per `RigGeometryNotes.md` §5 and the owner's principle:

- The studding class's curve (`data/sail_classes.yaml`) gets a stall: lift falls to nothing and the sail counts as flogging when the apparent wind is forward of `STUDDING_MIN_APPARENT_DEG` per level (lower 100° off the bow, topmast and topgallant 80°, from Luce's "abaft the beam" and "one point free"); flogging strains the sail and its boom as the strain model already does for a sail with a parted sheet. So a ship that comes up too far with them set gets a shivering studding sail, a strain line and, kept so, a lost boom, and the log tells her why. There is no refusal.
- **Booms and the lee rigging** are geometry: a boom rigged out on a yard braced beyond `BOOM_FOUL_BRACE_DEG = 45` from square lies against the lee rigging; `rig out` refuses when the yard is already so braced ("The fore yard is braced too sharp for the boom to go out."), and bracing beyond it with the boom out is refused by the adjacent-yards machinery's sibling check ("Rig in the studdingsail boom before bracing the fore yard sharper."). This is the one hard rule, kept because the model has no cloth or spar collision to simulate.
- **Booms start rigged in.** `Spar.rigged_out` defaults to false; the generator writes the state; `set the studdingsails` on a ship with booms in reports what must be done first, and the tack and wear scripts take studding sails in and booms in as the first all-hands work, as Luce's sequences begin. Gate M3's item 4 scenario is retold with topgallants.
- Truths: 29, the studding sails flog and strain when the ship comes up to six points with them set, and draw when she bears away to nine; 30, a frigate running with studding sails both sides in 15 knots makes about a knot more than under plain sail (Luce: "to increase the speed of a vessel"; the number is package 23's to measure and the owner's to judge).

## 8. The view (package 23)

- **Goose-winging drawn true:** the lee clew hauled up to the yard, the weather clew sheeted home; the sail as a triangle from the weather clew to the yard with its foot rising to the lee side (spec M3 §9 item 13).
- **Fixed scale:** the view's scale from the ship file's full rig, so that spars sent down leave the sky they filled (item 14).
- **Sail draw order** (spec M0–M2 §12 item 9): sort by the sail's centre along the view axis with a class tie-break; staysails that cross a mast drawn in two parts.
- Bowlines drawn as faint lines from the leech forward when hauled; catharpins not drawn.

## 9. Truths for milestone 3b

| # | Truth | Source |
|---|---|---|
| 24 | The frigate close-hauled with the after yards three degrees sharper than the head yards lies a quarter of a point closer or makes a quarter knot more than with all yards alike | Fincham art. 94 |
| 25 | Pinched to five points at three knots she makes less good to windward than kept full at six | Fincham art. 99 |
| 26 | Weather bowlines hauled gain about half a point of pointing at the same speed | Fincham art. 98, Luce |
| 27 | In the M2 gale a royal of condition 50 blows out before its yard; a new one loses the yard first | §6.2 |
| 28 | Storm staysails and close-reefed topsails in 45 knots: lying a-try under 1.5 knots, nothing lost in an hour | Luce ch. XXVI |
| 29 | Studding sails flog and strain at six points and draw at nine | Luce ch. XXIII |
| 30 | Studding sails both sides running in 15 knots: about a knot more than plain sail | Luce ch. XXIII |
| 31 | Catharpins swiftered in on the main: the main yard braces four degrees sharper and the frigate lies about a quarter of a point closer; in 30 knots on a wind the main mast's strain ratio is a sixth higher | Fincham art. 102, Lever |
| 32 | Pointing by ship: the frigate lies about six points, the schooner about five, measured as the closest heading at which speed holds above two thirds of her beam-reach speed | Fincham art. 102, Chapelle |
| 33 | Bracing the main topsail yard alone beyond the adjacent-yard clearance is refused with the reason; bracing the main yards together is not | §5 |

Every truth as a test in the existing style; measured values in `TuningNotes.md`; the owner judges 24, 26, 30, 31 and 32 at the gate.

## 10. Gate 3b (outline)

Short, about ten items, the human step kept: the frigate's pointing before and after bowlines; the after yards' trim; catharpins swiftered in and the strain line that follows; the schooner's pointing; the gale with a worn royal against a new one; the storm mizzen bent; the studding sails carried too close and then eased; a ringtail set running; the view's goose-wing, fixed scale and draw order; the primer's new chapter section. Expected numbers from the build's own seed-7 runs.

## 11. Open items from this chapter

1. **Geometric brace limits** from channel breadths and shroud spread: research (Steel 1805, draughts, model photographs with the owner's eyes).
2. **Fincham's Bouguer and Euler tables** from the page image, for a leeway-by-angle band.
3. **Steel's spar tables by rate** as a period replacement for Luce's rules in the generator.
4. **The sailmaker's mending** of worn canvas: milestone 8.
5. **Hardy's other measures** (shifted chain-plates) if catharpins alone do not reach the short ship's five points.
6. **Sternway when lying a-try** (package 24, truth 28). In 45 knots under storm staysails and close-reefed topsails the frigate lies 45° off and loses nothing in an hour, but goes astern at four to five knots; under bare poles she already makes 5.6 knots of sternway. The hull's resistance astern and the rig's windage are milestone 2 physics that no 3b constant touches; a hull that goes astern that fast in a gale is wrong, and the fix is in `hull.py`'s resistance law (astern resistance should be no less than ahead, and the windage of a hull lying a-try drives her mostly to leeward, not astern). For the rig-geometry follow-up or milestone 5's sea state, whichever opens the hull first.
7. **Storm canvas in gusts.** In the console's gusty 45 knots the storm staysails blow out (package 24's gate rehearsal). Either the gusts are right and No. 1 canvas should hold them (the cloth anchor of 0.32 may be low for storm canvas, which was made heavier than its number by roping and lining), or a storm staysail in 50-knot gusts should go. The owner's judgement at the gate.
8. **The after-yards trim, held for a ruling** (gate 3b). Truth 24's gain is a fifth of a knot and a degree, and the premise itself is contested: Fincham art. 94 has the after yards sharper (the head sails bend the wind aft), but Luce 1884 ch. XXIV "Working to Windward" (OCR line 29638 onward) says of that argument, "we find theorists saying ... that therefore the after yards should be braced sharper than those forward. But in practice it is much better to keep the fore yard sharper, so that in 'luffing to' a cloth or two of the main topsail will be lifting when the weather leech of the fore-topsail is just trembling. By this means a ship is more readily kept away." So the practical seaman of the later period kept the *head* yards sharper. The owner holds the ruling until item 11 is grounded; the built `trim sails with the head yards sharper` already gives Luce's trim, and the default may follow it.
9. **Lying a-try, lying a-hull, under bare poles** (gate 3b, owner). Falconer: to *try* or lie-to is to lie with the head near the wind under a small sail (a trysail, a main staysail, a close-reefed main topsail), the helm a-lee, making a little headway and much leeway; *a-hull* is with all sail furled and the helm a-lee, drifting; *bare poles* is scudding or lying with no sail set. The accounts have a ship a-try making a knot or two of headway and drifting to leeward; ours goes astern at four to five knots, and under bare poles at 5.6. The cause is upstream of 3b: the rig's windage at 45° on the bow is resolved along the hull as an aft push that the storm canvas cannot overcome, and the hull's resistance astern is no greater than ahead, so the balance goes astern fast. A real hull drags more astern than ahead (the run is fine, the entry full, the rudder trails), and windage drives her mostly to leeward. To do, when the hull is next opened: an astern resistance law and a check of the windage's direction; then truth 28's speed is re-measured and ruled.
10. **`trim` with an object** (gate 3b, owner). `trim the mainsail` and `tend the sheets` are not understood; `trim sails` trims everything. A `trim <sail>` that tends that sail's sheet (and its yard's brace if square) and a `tend the sheets` that tends only the sheets belong with the standing dialect in milestone 4, where "trim the X when Y" needs them.
11. **How a mast is trimmed from bottom to top** (gate 3b, owner's question; answered by Luce 1884 ch. XXIV, line 29638). The period practice is the *reverse* of bracing sharper aloft: "The upper yards should be braced in more than the lower, first, because the larger sail having greater curvature than the smaller must have its yard braced up to a sharper angle, that the plane of both may have the same angle with the keel; second, because the upper portion of the sail being attached to the yard approaches nearer to a plane than the lower part which bellies out, hence the upper part need not be so sharp; and thirdly, the lighter yards and braces require a greater angle for their support. Further, the upper yards being in, when the main royal is just lifting all the other sails are a 'clean full and by,' which makes it a good sail to steer by." So the owner's steering-by-the-topmost-sail is period, and comes from the upper yards being a trifle *in*, not sharper. The same page cites Fincham's 19½° for the main yard close-hauled (70½° from square) and says "many ships work within [five and a half] points". To do: `trim sails` braces each yard on a mast a trifle in of the one below (a constant per level, Luce's reasons cited), the head yards a shade sharper than the after (item 8), and the truth "the main royal lifts first, and the ship is a clean full and by when it does". Harland's *Seamanship in the Age of Sail* would be worth adding to the references as the modern synthesis.
12. **Bowlines on fore-and-aft vessels** (gate 3b, owner). On the schooner the measure is not the gain in speed but the highest pointing at which her square topsail still fills; a truth in that form when the pointing truths are next touched.
13. **Telltales and pennants** at the mastheads for the viewer: a wind and apparent-wind reference and later signalling; with the viewer pass.

