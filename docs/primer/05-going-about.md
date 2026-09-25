# 5. Going about

There are two ways from one tack to the other. **Tacking** turns her head through the wind and loses nothing to leeward when it is done well; **wearing** (Falconer's *veering*) turns her stern through it, is safe in any weather, and costs ground to leeward. A ship that fails to tack has *missed stays*. **Heaving to** is neither: it stops her with the sails set against each other, and **filling away** gets her going again.

## Tacking

Luce (1866, ch. XXIV Working to Windward, 'Tacking') gives the sequence for a ship under courses, topsails, topgallants, jib and spanker, and the game's `tack` evolution follows it: *Ready about!*, the helm eased down and *Helm's a-lee!* with the head sheets let fly; as the sails shake, *Rise tacks and sheets!*; with the wind a point on the weather bow or dead ahead, *Mainsail haul!* and the after yards swing round; as the after sails fill on the new tack, *Let go and haul!* and the head yards follow; then brace up, trim the yards, and *keep her by the wind*. Lever's 'Tacking Expeditiously' is the same sequence with the reasons, and his warning that a ship put about with too much helm "was sure to miss stays, and fall off again".

Before you give the order she must be **close-hauled with way on her**: the evolution refuses to start otherwise ("She has not way enough on her to stay: 1.4 kn through the water"; "She is not close-hauled; bring her by the wind before going about"). Two knots is the least the order will start with, but she misses stays below about three; from five she goes round, which is what plain sail gives her in a 15-knot breeze.

```orders frigate plain-sail
tack ship
```

The log, from the frigate under plain sail at 4.7 knots close-hauled on the starboard tack:

```
  Morning watch (04:16)  Order: tack ship.
  Morning watch (04:16)  Ready about. Helm's a-lee; eased off the head sheets.
  Morning watch (04:16)  All hands about ship.
* Morning watch (04:16)  Fore course taken aback.
* Morning watch (04:16)  Main course taken aback.
* Morning watch (04:16)  Fore topsail taken aback.
* Morning watch (04:16)  Main topsail taken aback.
* Morning watch (04:16)  Mizzen topsail taken aback.
  Morning watch (04:17)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:17)  Main topsail filled again.
  Morning watch (04:17)  Mizzen topsail filled again.
  Morning watch (04:17)  Main course filled again.
  Morning watch (04:18)  Let go and haul.
  Morning watch (04:18)  Fore course filled again.
  Morning watch (04:18)  Fore topsail filled again.
* Morning watch (04:21)  Tacked; braced up on the larboard tack, heading ENE (68°).
  Morning watch (04:22)  Steady on ENE (68°).
```

Read it against Luce. The helm goes down and she flies up into the wind; as her head comes within a point of it the sails are pressed back against the masts (*taken aback*, Falconer, *Aback*), which is the moment for *Mainsail haul*: the after yards are swung to the new tack while the wind on their weather leeches helps them round. Her head passes through the wind; the after sails fill on the new tack; *Let go and haul* swings the head yards, whose sails were aback and paying her head off, and she gathers way close-hauled on the larboard tack. Two minutes from the helm going down to *Let go and haul*, five to *Tacked* and six to *Steady*, most of it spent gathering way on the new tack; she is back at five knots ten minutes after the order. The fore sails may fill and go aback several times while the head yards swing; that is the same wind on a moving yard, not a fault.

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

If her way falls below eight tenths of a knot before her head comes through, or she hangs head to wind for three minutes, she has missed stays. In a 15-knot breeze under plain sail she has way to spare; in seven knots she makes 2.2 knots close-hauled, and the same order fails: Luce: "In vessels which are dull in stays and go off slowly after coming up head to wind, and particularly in a light breeze..." (Luce 1866, ch. XXIV, 'Missing Stays'); Lever's figures 497 to 500 show her boxed off by the sea and falling back. In the game the evolution fails with an urgent line:

```
  Morning watch (04:15)  Order: tack ship.
  Morning watch (04:15)  Ready about. Helm's a-lee; eased off the head sheets.
  Morning watch (04:17)  Rise tacks and sheets. Mainsail haul.
! Morning watch (04:17)  Missed stays: she lost her way before her head came through the wind. Squared the yards and fell off on the starboard tack.
! Morning watch (04:17)  Taken aback: the sails pressed against the masts and she lost her way.
```

She squares her yards and puts the helm up to fall off on the tack she came from, and you are where you started with less way: four minutes later she has 1.8 knots of sternway and her head at NW by N. What a sailing master does next is **wear** (below), or in a narrow place **box-haul** (below, and not yet in the game). Under a knot and a half she refuses the order for want of way instead, which is the same lesson given earlier.

## Wearing

"Wearing or veering is another method of going about from one tack to the other. This is only resorted to in heavy weather, with a sea on the weather bow; when under easy sail, or in light airs; when, in either case, the vessel has not sufficient headway for tacking... she must lose considerably to leeward" (Luce 1866, ch. XXIV, 'Wearing'; Falconer, *Veering*; Lever, 'Veering or Waring'). The sequence: *Up mainsail and spanker!*, helm up, *Brace in the after yards!* as she falls off, keeping the mizzen topsail lifting and the main topsail full; wind aft, *Lay the head yards square!*; wind on the other quarter, haul out the spanker and brace up the after yards; and as she comes to, brace up the head yards and meet her with the helm.

```orders frigate plain-sail
wear ship
wear
wear round
```

The log:

```
  Morning watch (04:28)  Order: wear ship.
  Morning watch (04:28)  Stand by to wear ship. Up helm; brace in the after yards.
  Morning watch (04:28)  Stations for wearing ship.
  Morning watch (04:29)  Wind aft. Squared the head yards; hauled out and braced up.
* Morning watch (04:30)  Fore topgallant taken aback.
* Morning watch (04:30)  Main course taken aback.
  Morning watch (04:32)  Main topsail filled again.
  Morning watch (04:32)  Fore course filled again.
* Morning watch (04:37)  Wore ship; braced sharp up on the starboard tack, heading WNW (293°).
  Morning watch (04:37)  Steady on WNW (293°).
```

The yards follow the wind round in stages as the watch braces the after yards and then the head yards, about a third of a degree a second, so the log has no "mainsail haul": the trim changes continuously as she turns. Half a knot of way is enough to start a wear. Nine minutes from order to *Wore ship*, which is what Luce allows a frigate (six to twelve; truth 11 of the tuning notes). She loses about a sixth of a mile to leeward doing it, less than the quarter to half a mile Luce's wear costs, because the script comes to as soon as the wind is aft instead of running her off for a spell; the map in the browser client shows it. The game does not haul up the mainsail and spanker for the wear as Luce does; a careful master gives `haul up the mainsail` and `brail up the spanker` first and sets them again after.

## Box-hauling and club-hauling: not yet

Two manoeuvres for a ship that cannot tack and has not room to wear. The parser refuses both; the game does not know them yet.

**Box-hauling** (Luce 1866, ch. XXIV, 'Box Hauling'; Lever, 'Missing Stays, Waring Short Round, Box-hauling'): when she refuses stays, keep the helm a-lee, haul up the mainsail and spanker, square the after yards and brace the head yards sharp aback; she gathers sternway with her head falling off, the helm is shifted, and as the wind comes on the quarter the after yards are braced up and she comes to on the new tack, having turned in little more than her own length. "Either of them may be termed box-hauling, a term derived from the circumstance of bracing the head yards abox."

**Club-hauling** (Luce 1866, ch. XXIV, 'Club Hauling'; Lever, 'Sounding, Box and Club-hauling'): tacking on a lee shore by letting go the lee anchor as she comes head to wind, with a spring from the cable to the lee quarter; the anchor holds her head up while the after yards are hauled, the cable is cut, and she sails away on the new tack. Lever: "This is called CLUB-HAULING." It needs an anchor and cable, which no ship file has yet (milestone 5).

```orders frigate plain-sail
# rejected: box haul
# rejected: club haul
hard a-lee
haul up the mainsail
brail up the spanker
square the after yards
brace the head yards sharp aback
```

The five orders after the refusals are how you would begin a box-haul by hand, in Luce's own words: the helm a-lee, up mainsail and spanker, the after yards squared and the head yards aback (chapter 4, 'Laying a yard aback'). A determined player can carry it through with `right the helm` as she gathers sternway, `hard up` when her head has fallen off, and `brace round the after yards` and `brace the head yards sharp up` as the wind comes on the quarter, but nothing tells the physics that she is box-hauling, and the log will not say *Box-hauled*.

## Heaving to

"Lying-to: the situation of a ship when she is retarded in her course, by arranging the sails in such a manner as to counteract each other with nearly an equal effort, and render the ship almost immoveable, with respect to her progressive motion, or head-way. A ship is usually brought-to by the main and fore-top-sails, one of which is laid aback, whilst the other is full" (Falconer, *Lying-to*). Lever's 'Heaving to' has two ships lying to speak one another, the weather ship with her main topsail aback and the lee ship with her fore topsail aback so that she can box her head off and keep clear.

The game's `heave_to` is the M2 simplification of Luce's 'To heave to' (Luce 1866, ch. XXVI Emergencies): the courses are hauled up, the spanker brailed up (Luce: "regulate by easing off the spanker and jib sheets") and the light sails forward of the backed mast clewed up ("settle down the top-gallant sails and royals, or clew them up"); the yards on the mast that carries the most square sail are braced aback (the main topsail on the frigate, the fore topsail on the schooner, which has no other), the rest are left full, and the helm is put a-lee. On the schooner the mainsail stays set, being her driving sail.

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
  Morning watch (04:51)  Order: heave to.
  Morning watch (04:51)  Hauled up the courses; brailed up the spanker.
  Morning watch (04:51)  Clewed up the fore topgallant.
  Morning watch (04:51)  Braced the main topsail aback; helm a-lee.
  Morning watch (04:51)  Hands to the after braces; heave to.
* Morning watch (04:51)  Main topsail taken aback.
* Morning watch (04:51)  Main topgallant taken aback.
* Morning watch (04:52)  Hove to, main topsail to the mast, helm a-lee.
```

and ten minutes later:

```
Amazon: heading NW by W (298°), speed 1.4 kn, leeway -44°, heel -4°
Apparent wind 56° on the starboard bow, 14.2 kn; helm +15°
```

She lies with her head about five points (58° to 62°) off the true wind, making a knot or so, mostly to leeward: the leeway of 44° says the little way she has is nearly as much sideways as ahead, and now and then it turns to sternway for a spell. That is a ship hove to (truth 12 of the tuning notes: under a knot and a half, head 45° to 60° off, steady within 15°). She will lie so as long as you leave her. The courses, spanker and topgallant that were taken in stay in until you set them again.

## Filling away

To get under way again the head sheets are hauled aft and her head let fall off until the backed sails will fill when braced, then the backed yards are braced round full and she is steered close-hauled (Luce 1866, ch. XXVI, 'To fill away, after lying to with the main topsail to the mast'). The script keeps the helm a-lee while she has sternway, which throws her head off, and puts it up once she has headway, until her head is five points (55°) off the true wind; lying to as `heave to` leaves her, that is at once:

```
  Morning watch (05:01)  Order: fill away.
  Morning watch (05:01)  Hauled aft the head sheets; kept the helm a-lee to let her fall off.
  Morning watch (05:01)  Fill away; man the after braces.
  Morning watch (05:01)  Braced the main topsail full.
  Morning watch (05:01)  Main topsail filled again.
* Morning watch (05:02)  Filled away; braced full and steering WNW (293°).
  Morning watch (05:03)  Steady on WNW (293°).
```

Two minutes to *Steady*, and she is close-hauled with four knots of way inside seven, under topsails, topgallants and headsails only; `set the courses` and `set the spanker` give her back her plain sail. Braced full from nearer the wind than five points she would only be taken aback, which is why the script waits (and gives up waiting after three minutes). `fill away` when she is not hove to is refused: "She is not hove to."

## The schooner

A fore-and-aft vessel tacks quickly and wears with her main boom: "clew up the main gaff topsail, if set, drop the peak of the mainsail, up helm and ease off the main sheet... when the wind is aft shift over the boom and head sheets" (Luce 1884, ch. XXXIV Handling Fore-and-Afters, 'To Wear'). The game uses the same four evolutions for her with her two yards playing the part of the head yards; she has no after yards, so *Mainsail haul* passes in a moment. She wears in eight minutes and heaves to with the fore topsail to the mast.

Two things do not yet work as they should for her, and both are recorded for the lead. **`tack ship` is refused when she is close-hauled**: the runner's close-hauled check reads the luff angle of her square fore topsail, which wants 50° of apparent wind, though she sails at 40° to 44° ("She is not close-hauled; bring her by the wind before going about"; `docs/dev/TuningNotes.md`, 'Bugs found on the way'). Until it is fixed, wear her. And **she does not lie to**: with only her fore topsail to lay aback against two big gaff sails she pays off and forereaches at three or four knots. A schooner is properly hove to with a jib or fore sheet hauled to windward, which the sail model has no state for (Luce 1884, ch. XXXIV Handling Fore-and-Afters); that is crew work for milestone 3.

```orders schooner plain-sail
tack ship
wear ship
heave to
fill away
gybe
```

The later word for wearing a fore-and-aft vessel is *gybe*, and the parser takes it as a synonym of `wear ship` with a note in the log ("Gybe, that is, wear ship (the period word); the boom will come over as the wind crosses her stern"). Luce 1884 says *wear*; so should you.

```
  Morning watch (04:20)  Order: wear ship.
  Morning watch (04:20)  Stand by to wear ship. Up helm; brace in the after yards.
  Morning watch (04:20)  Stations for wearing ship.
  Morning watch (04:21)  Wind aft. Squared the head yards; hauled out and braced up.
* Morning watch (04:22)  Fore topgallant taken aback.
* Morning watch (04:22)  Fore topsail taken aback.
  Morning watch (04:25)  Fore topsail filled again.
* Morning watch (04:28)  Wore ship; braced sharp up on the larboard tack, heading ENE (68°).
  Morning watch (04:28)  Steady on ENE (68°).
```

What she does not do yet: gybe as a thing of its own. There is no separate evolution to shift the main boom over with the wind aft; wearing (and so `gybe`) does it silently inside the evolution, and running by the lee costs nothing. Both are later work.
