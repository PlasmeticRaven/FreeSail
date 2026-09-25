# 5. Going about

There are two ways from one tack to the other. **Tacking** turns her head through the wind and loses nothing to leeward when it is done well; **wearing** (Falconer's *veering*) turns her stern through it, is safe in any weather, and costs ground to leeward. A ship that fails to tack has *missed stays*. **Heaving to** is neither: it stops her with the sails set against each other, and **filling away** gets her going again.

## Tacking

Luce (1866, ch. XXIV Working to Windward, 'Tacking') gives the sequence for a ship under courses, topsails, topgallants, jib and spanker, and the game's `tack` evolution follows it: *Ready about!*, the helm eased down and *Helm's a-lee!* with the head sheets let fly; as the sails shake, *Rise tacks and sheets!*; with the wind a point on the weather bow or dead ahead, *Mainsail haul!* and the after yards swing round; as the after sails fill on the new tack, *Let go and haul!* and the head yards follow; then brace up, trim the yards, and *keep her by the wind*. Lever's 'Tacking Expeditiously' is the same sequence with the reasons, and his warning that a ship put about with too much helm "was sure to miss stays, and fall off again".

Before you give the order she must be **close-hauled with way on her**: the evolution refuses to start otherwise ("She has not way enough on her to stay: 1.4 kn through the water"; "She is not close-hauled; bring her by the wind before going about"). Two knots is the least she will stay with, and she stays better with more.

```orders frigate plain-sail
tack ship
```

The log, from the frigate under plain sail at 8 knots on the starboard tack:

```
  Morning watch (04:21)  Order: tack ship.
  Morning watch (04:21)  Ready about. Helm's a-lee; eased off the head sheets.
  Morning watch (04:21)  All hands about ship.
* Morning watch (04:21)  Main course taken aback.
* Morning watch (04:21)  Fore course taken aback.
* Morning watch (04:21)  Mizzen topsail taken aback.
  Morning watch (04:21)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:22)  Main topgallant filled again.
  Morning watch (04:22)  Main course filled again.
  Morning watch (04:22)  Let go and haul.
  Morning watch (04:23)  Fore topsail filled again.
  Morning watch (04:23)  Fore course filled again.
* Morning watch (04:25)  Tacked; braced up on the larboard tack, heading ENE (68°).
  Morning watch (04:26)  Steady on ENE (68°).
```

Read it against Luce. The helm goes down and she flies up into the wind; as her head comes within a point of it the sails are pressed back against the masts (*taken aback*, Falconer, *Aback*), which is the moment for *Mainsail haul*: the after yards are swung to the new tack while the wind on their weather leeches helps them round. Her head passes through the wind; the after sails fill on the new tack; *Let go and haul* swings the head yards, whose sails were aback and paying her head off, and she gathers way close-hauled on the larboard tack. Four minutes from order to *Tacked*, five to *Steady*. The fore sails may fill and go aback several times while the head yards swing; that is the same wind on a moving yard, not a fault.

Synonyms the parser takes: `ready about`, `go about`, `about ship`, `put her about`, `stays`. A tack takes no side; she goes onto the other one.

```orders frigate plain-sail
ready about
go about
about ship
put her about
# rejected: tack ship on the larboard tack
```

After a tack the yards are braced sharp up for the new tack by the evolution, but nothing else is trimmed: the jib and spanker sheets find their own trim (chapter 4) and your helm order is the new close-hauled course. Say `keep her full` if you want the helmsman sailing by the wind rather than by compass.

### Missing stays

If her way falls below eight tenths of a knot before her head comes through, or she hangs head to wind for three minutes, she has missed stays. Luce: "In vessels which are dull in stays and go off slowly after coming up head to wind, and particularly in a light breeze..." (Luce 1866, ch. XXIV, 'Missing Stays'); Lever's figures 497 to 500 show her boxed off by the sea and falling back. In the game the evolution fails with an urgent line:

```
! Morning watch (04:24)  Missed stays: she lost her way before her head came through the wind. Squared the yards and fell off on the starboard tack.
```

She squares her yards and puts the helm up to fall off on the tack she came from, and you are where you started with less way. What a sailing master does next is **wear** (below), or in a narrow place **box-haul** (below, and not yet in the game). In this build, with a working breeze and plain sail, the frigate has not been made to miss; in light airs she refuses the order for want of way instead, which is the same lesson given earlier.

## Wearing

"Wearing or veering is another method of going about from one tack to the other. This is only resorted to in heavy weather, with a sea on the weather bow; when under easy sail, or in light airs; when, in either case, the vessel has not sufficient headway for tacking... she must lose considerably to leeward" (Luce 1866, ch. XXIV, 'Wearing'; Falconer, *Veering*; Lever, 'Veering or Waring'). The sequence: *Up mainsail and spanker!*, helm up, *Brace in the after yards!* as she falls off, keeping the mizzen topsail lifting and the main topsail full; wind aft, *Lay the head yards square!*; wind on the other quarter, haul out the spanker and brace up the after yards; and as she comes to, brace up the head yards and meet her with the helm.

```orders frigate plain-sail
wear ship
wear
wear round
```

The log:

```
  Morning watch (04:37)  Order: wear ship.
  Morning watch (04:37)  Stand by to wear ship. Up helm; brace in the after yards.
  Morning watch (04:37)  Stations for wearing ship.
  Morning watch (04:38)  Wind aft. Squared the head yards; hauled out and braced up.
* Morning watch (04:39)  Fore topgallant taken aback.
  Morning watch (04:39)  Fore topgallant filled again.
* Morning watch (04:40)  Wore ship; braced sharp up on the starboard tack, heading WNW (292°).
  Morning watch (04:41)  Steady on WNW (292°).
```

The yards follow the wind round at a degree a second, so the log has no "mainsail haul": the trim changes continuously as she turns. Half a knot of way is enough to start a wear. She needs only three minutes in this build, which is quicker than Luce allows a frigate; the six to twelve minutes are a known truth for the tuning work (package 10), as is the ground lost, which the map will show in the browser client. The game does not haul up the mainsail and spanker for the wear as Luce does; a careful master gives `take in the spanker` first and sets it again after.

## Box-hauling and club-hauling: not yet

Two manoeuvres for a ship that cannot tack and has not room to wear. The parser refuses both; the game does not know them yet.

**Box-hauling** (Luce 1866, ch. XXIV, 'Box Hauling'; Lever, 'Missing Stays, Waring Short Round, Box-hauling'): when she refuses stays, keep the helm a-lee, haul up the mainsail and spanker, square the after yards and brace the head yards sharp aback; she gathers sternway with her head falling off, the helm is shifted, and as the wind comes on the quarter the after yards are braced up and she comes to on the new tack, having turned in little more than her own length. "Either of them may be termed box-hauling, a term derived from the circumstance of bracing the head yards abox."

**Club-hauling** (Luce 1866, ch. XXIV, 'Club Hauling'; Lever, 'Sounding, Box and Club-hauling'): tacking on a lee shore by letting go the lee anchor as she comes head to wind, with a spring from the cable to the lee quarter; the anchor holds her head up while the after yards are hauled, the cable is cut, and she sails away on the new tack. Lever: "This is called CLUB-HAULING." It needs an anchor and cable, which no ship file has yet (milestone 5).

```orders frigate plain-sail
# rejected: box haul
# rejected: club haul
# rejected: back the main topsail
# rejected: lay the main topsail aback
```

The last two are how you would begin a box-haul by hand. The game's brace evolution braces a yard *for* a tack, never *aback*: to lay a yard aback you must name the other tack, `brace the head yards sharp up on the larboard tack` while she is on the starboard, which is what heaving to does underneath. That works, and a determined player can box-haul with it and the helm, but nothing will tell the physics that she is box-hauling.

## Heaving to

"Lying-to: the situation of a ship when she is retarded in her course, by arranging the sails in such a manner as to counteract each other with nearly an equal effort, and render the ship almost immoveable, with respect to her progressive motion, or head-way. A ship is usually brought-to by the main and fore-top-sails, one of which is laid aback, whilst the other is full" (Falconer, *Lying-to*). Lever's 'Heaving to' has two ships lying to speak one another, the weather ship with her main topsail aback and the lee ship with her fore topsail aback so that she can box her head off and keep clear.

The game's `heave_to` is the M2 simplification of Luce's 'To heave to' (Luce 1866, ch. XXVI Emergencies): the courses are hauled up, the yards on the mast that carries the most square sail are braced aback (the main topsail on the frigate, the fore topsail on the schooner, which has no other), the rest are left full, and the helm is put a-lee.

```orders frigate plain-sail
heave to
fill away
heave to on the starboard tack
fill
lie to
let draw
bring her to
# rejected: heave to on the weather tack
```

She must already be on the tack you name; "heave to on the larboard tack" while she is on the starboard is refused with "tack or wear first". Heave to twice and the second is refused: "She is hove to already." The log:

```
  Morning watch (04:52)  Order: heave to.
  Morning watch (04:52)  Hauled up the courses.
  Morning watch (04:52)  Braced the main topsail aback; helm a-lee.
  Morning watch (04:52)  Hands to the after braces; heave to.
* Morning watch (04:52)  Main topsail taken aback.
* Morning watch (04:53)  Hove to, main topsail to the mast, helm a-lee.
```

and a quarter of an hour later:

```
Amazon: heading NW (315°), speed 2.4 kn, leeway -163°, heel -6°
Apparent wind 51° on the starboard bow, 11.3 kn; helm +15°
```

Read the leeway: 163° means she is making sternway, which is what a hove-to ship with a backed main topsail does, and the wind is four and a half points on the bow. She should lie quieter than this: the tuning work (package 10) starts from exactly this observation, made at gate M1, and the target is under a knot and a half with the head 45° to 60° off. **Report what you see; do not judge her by it yet.**

## Filling away

To get under way again the helm is righted, the head sheets hauled aft, and the backed yards braced round full (Luce 1866, ch. XXVI, 'To fill away, after lying to with the main topsail to the mast'):

```
  Morning watch (05:07)  Order: fill away.
  Morning watch (05:07)  Righted the helm; hauled aft the head sheets.
  Morning watch (05:07)  Fill away; man the after braces.
* Morning watch (05:08)  Filled away; braced full and steering WNW (293°).
```

In this build she is often taken aback again a minute later and hangs with little way, because she fills from a heading too near the wind; the fix is to bear away deliberately before bracing full, which is package 10's job (`docs/dev/M2-WorkPackages.md`, truth 12). Until then, if she hangs, `bear away two points`, wait for way, and `keep her full`. `fill away` when she is not hove to is refused: "She is not hove to."

## The schooner

A fore-and-aft vessel tacks quickly and wears with her main boom: "clew up the main gaff topsail, if set, drop the peak of the mainsail, up helm and ease off the main sheet... when the wind is aft shift over the boom and head sheets" (Luce 1884, ch. XXXIV Handling Fore-and-Afters, 'To Wear'). The game uses the same four evolutions for her with her two yards playing the part of the head yards; she has no after yards, so *Mainsail haul* passes in a moment. She goes about in two minutes and wears in five, and heaves to with the fore topsail to the mast.

```orders schooner plain-sail
tack ship
wear ship
heave to
fill away
```

```
  Morning watch (04:20)  Order: tack ship.
  Morning watch (04:20)  Ready about. Helm's a-lee; eased off the head sheets.
  Morning watch (04:20)  All hands about ship.
* Morning watch (04:20)  Fore topsail taken aback.
  Morning watch (04:20)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:21)  Let go and haul.
  Morning watch (04:21)  Fore topsail filled again.
* Morning watch (04:22)  Tacked; braced up on the larboard tack, heading ENE (68°).
```

What she does not do yet: gybe. There is no order to shift the main boom over with the wind aft; wearing does it silently inside the evolution, and running by the lee costs nothing. Both are later work.
