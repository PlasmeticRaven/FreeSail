# 18. The lessons

The chapters before this one say what the ship does and what each order means. This one is a handful of worked passages, each a duty an officer of the watch must be able to do alone before anyone would give him a command: a landfall on one headland; his own reckoning, worked and judged at noon; a pilotage by cross bearings; heaving to for a pilot; coming to an anchor in a tideway; and a night standing off a lee shore. Into them go the things that neither the officer of the ninth game nor the owner knew the ship could do (the end of the chapter lists them): the captain's allowance for a set, the amplitude, what `let go` veers by itself, what `veer to` and `weigh` act on, and when a bearing's distance is laid down. It is the same chapter for the player and for a model at a station, as the whole book is: the player reads it beside the console, a model reads it in the library as primer 18, and nothing in it is for the one and not the other.

Each lesson gives the duty; the rule of the period with its source; the orders in the game's language; what the log said when it went right; and the usual mistake, with what the log says then. The lines are quoted from one run of the lesson's own scenario at seed 7, measured once and not tuned for a prettier log (`docs/dev/TuningNotes.md`, package 40b, has every order and the minute it was given). Sail it yourself:

```
python -m freesail.ui.console --scenario data/scenarios/lesson-landfall.yaml
```

and type the orders at the minutes given; `tools/lesson_run.py` gives them for you and prints the log, and at another seed, or another minute, the lines are other lines. As everywhere in this book, a block of orders is checked against the frigate off the Lizard at ten in the forenoon (the README says how), so an order a lesson gives at sunrise or at anchor, which that ship refuses at that hour, is shown `# rejected:` and the text says when it is taken.

## 1. A landfall on one headland

**The duty.** To bring her in from sea to the land by her account, and to correct the account by the first land seen.

**The rule.** Falconer's *Land-fall* is "the first land discovered after a sea-voyage", and to wish a ship "a good land-fall" is to wish her "a discovery of land, at or near the place whither their course is directed, and which they expect to make by their journals". The landfall is made on the account, and the account is then corrected by the land: a bearing of one headland is a line, and the distance by estimation along it is weighed by the master's rule ([chapter 10](10-the-reckoning.md)): it counts for much only when his own doubt along the line of sight is the greater, which after a night's run it is. Before the land, have the variation as it is today: Robertson's rule, in Falconer's *Variation*, is to observe an amplitude or an azimuth "every day, or as often as they had opportunity", and the sun's rising is the opportunity ([chapter 12](12-the-longitude.md)). Shape the course for an offing off the headland and never for the headland itself, and shape it again when the master's tide turns, since he does not alter the helm of himself.

```orders frigate plain-sail
shape a course for two leagues south of the Lizard
trim sails
# rejected: observe an amplitude
take a bearing of the land
shape a course for two miles SE of the Manacles
```

**The run** (`data/scenarios/lesson-landfall.yaml`, seed 7): the frigate thirty-three miles south-south-west of the Lizard at one in the morning of 14 June 1805, the westerly on her beam. Plain sail and the course at the start; `trim sails` when the topgallants were set; the course shaped again, and trimmed, when the master's tide turned; the amplitude at sunrise; the bearing when the lookout raised the Lizard; then the course for a berth off the Manacles. The amplitude is refused at ten in the forenoon, where this book's blocks stand, and taken in the quarter of an hour either side of the sun's rising or setting.

```
  Middle watch, 2 bells (01:00)  Shaped a course for two leagues south of the Lizard: NNE by account, 27 miles. Allowing the ebb, three quarters of a knot to the SW, steer NNE to make it good; the allowance holds till the tide turns, about a quarter past two in the middle watch. Helm ordered: steer NNE (24°).
  Middle watch (02:01)  By the master's tide the flood makes: allowing a knot and a half to the NE.
  Middle watch (02:01)  Shaped a course for two leagues south of the Lizard: NNE by account, 21 miles. Helm ordered: steer NNE (20°).
* Middle watch (03:08)  A light right ahead, bearing N by E.
* Middle watch (03:50)  Sunrise.
  Middle watch (03:50)  Observed the sun's amplitude at its rising, bearing E by N by compass: variation of the compass 24° 30' W by amplitude, 14 June, where the chart gave 21° 30' W by the chart of 1794; Mr Harvey allows it in the reckoning from now.
* Morning watch (04:16)  The Lizard bearing N by E, distant five leagues.
  Morning watch (04:16)  The Lizard bore N by E, five leagues by estimation: the account moved four miles to the SW by S.
  Morning watch (04:16)  Shaped a course for two miles south-east of the Manacles: NE by N by account, 19 miles. Allowing the flood, a knot and a quarter to the NE, steer NNE to make it good; the allowance holds till the tide turns, about a quarter past eight in the morning. Helm ordered: steer NNE (27°).
```

The light at three in the morning was the Lizard's, seen before the land; at sunrise the light goes out of sight and the land comes up a little after. The amplitude found three degrees more westerly variation than the chart of 1794 gave, which is a mile in every twenty of the run that the master had been laying down wrong. The one bearing, with the lookout's five leagues, moved an account that had run three hours and a quarter from its departure four miles to the south-west: a good landfall, at the place whither her course was directed, and the account set right by it before the course in was shaped.

**The usual mistake.** A second bearing of the same headland at once, to be sure of it. It is the same thing seen again: the same compass, the same chart and the same eye, and the master is no surer for it. The run took one, a second after the first:

```
  Morning watch (04:16)  The Lizard bore N by E, five leagues by estimation: the account moved a cable to the W by S.
```

A cable is nothing. What tells him more is a bearing of a second mark that cuts the first well, or of the same mark after a run of a few miles, which is a running fix (chapter 10), or the lead. And the course shaped across the wind without the sails trimmed to it: the run's first quarter of an hour, before `trim sails`, has "Her sails lifting, the wind 90° on the larboard bow: keep her away, or she will be taken aback" (lesson 6 has the same mistake at night, and what it cost).

## 2. Your own reckoning

**The duty.** To keep a reckoning of one's own, worked from the same log-board, the same tide and the same sights as the master's, and to have it judged by the sun at noon. The officer of the ninth game wanted "a few more landfalls on my own reckoning" before a command; this is how one is kept.

**The rule.** The Regulations of 1806 have the master keep the ship's log-book, entering "with very minute exactness ... the courses steered, and the distances run, with every occurrence relating to the navigating of the Ship; the setting and velocity of currents, and the result of all astronomical observations made to ascertain the situation of the Ship" (the Master, art. XXXII); the lieutenant "is to keep a Log-book according to the form (N°. 25) in the Appendix ... with whatever additional information, useful to navigation ... his observations may have enabled him to obtain" (the Lieutenant); and the master's mates and midshipmen "are to keep Log-books according to the form (N°. 25)", without which "they cannot be examined" for lieutenant (the Captain's articles, on rating the ship's company). Each worked the day's work for himself from the log-board by the traverse table: every course and its distance reduced to a difference of latitude and a departure, the current allowed as one more course, the whole summed (Falconer, *Dead-reckoning*, *Log-board*, *Traverse*).

`work my reckoning` gives you the master's slate since his last fix: where it begins (the departure, the reckoning set by hand, a fix by cross bearings, or an observation that laid the account down) with his doubt there, each board as he laid it down with the tide he allowed and her drift if she lay to, each sight he worked in since and how far it moved his account, and the board in hand. It is a reading for you alone, in your reply, and not a line of the log. `my reckoning is <position>` gives him yours: kept beside his, it moves nothing, it is run on by the log-board, and at noon the line after the noon's says it beside his account before the sight, with where the sun's latitude lies from it. It is then carried on from your own noon figure, as each day's work began from the last, and said again at the next noon; a new `my reckoning is` replaces it, and it is forgotten only when you leave the station (stood down, withdrawn, or the player's seat left). You keep it with the deck or off watch; a standing order may give neither order. `the officer's reckoning` reads the officer of the watch's as it stands, and the captain adopts it, if he will, with `set the reckoning to`, which is his.

```orders frigate plain-sail
work my reckoning
my reckoning is 49 40.4 N 5 7.2 W
the officer's reckoning
set the reckoning to 49 40.4 N 5 7.2 W
```

**The run** (`data/scenarios/lesson-reckoning.yaml`, seed 7, the player seated at the officer's station with `--seat officer`): the frigate off the Lizard at half past nine in the forenoon, standing east-south-east across the ebb with the westerly on her quarter. The captain gave the deck; the officer trimmed sails, and at half past eleven asked for the slate:

```
  Forenoon watch, 7 bells (11:30)  The master's slate since the departure at 09:30: 49° 47' N, 5° 22' W by account then, and his doubt then: "I would not trust the reckoning within a mile east or west, nor a mile north or south." The boards, each course as he laid it down (true, his variation and his leeway allowed) and its distance: 09:30 to 10:00, ESE (116°) 2.5 miles at 5 knots by the log, the tide 0.5 miles to the SW; 10:00 to 11:00, ESE (112°) 6.8 miles at 6.75 knots by the log, the tide 1.2 miles to the SW; in hand since 11:00, not yet laid down, ESE (115°) 3.0 miles at 6 knots by the log, the tide 0.7 miles to the SW. The tide he allows now: the ebb, a knot and a half to the SW, by the directions for the open Channel and high water at the Lizard by the epitome. Work it, and give your own with 'my reckoning is <position>'.
```

Worked by the traverse, each course and the tide with it to a difference of latitude (N or S) and a departure (E or W), in miles:

| Course | Distance | N | S | E | W |
|---|---|---|---|---|---|
| 116° | 2.5 | | 1.10 | 2.25 | |
| the tide, SW | 0.5 | | 0.35 | | 0.35 |
| 112° | 6.8 | | 2.55 | 6.30 | |
| the tide, SW | 1.2 | | 0.85 | | 0.85 |
| 115° | 3.0 | | 1.27 | 2.72 | |
| the tide, SW | 0.7 | | 0.49 | | 0.49 |
| | | | 6.61 | 11.27 | 1.69 |

Six miles and six tenths of southing is 6.6' of latitude: 49° 47' N less 6.6' is 49° 40.4' N. The departure is 9.6 miles east, which at that latitude (divide by the cosine of 49° 40', 0.647) is 14.8' of longitude: 5° 22' W less 14.8' is 5° 07.2' W.

```
  Forenoon watch (11:31)  Mr Pearce's own reckoning: 49° 40' N, 5° 07' W, on the master's account, within what he would trust it; kept beside the master's, it moves nothing, and is said at noon.
  Forenoon watch (11:32)  The officer's reckoning: 49° 40' N, 5° 07' W by Mr Pearce's own reckoning, worked at 11:31 and run on by the log-board, on the master's account, within what he would trust it.
* Afternoon watch, 8 bells (12:00)  Noon. Latitude by observation 49° 44' N; the reckoning was 49° 39' N: the account moved three miles to the NE by N. Course made good since the departure SE by E, 14 miles. Longitude by account 5° 01' W. The day's work carried the master's tide by the directions and the epitome.
* Afternoon watch, 8 bells (12:00)  The officer of the watch's own reckoning (Mr Pearce), worked at 11:31 and run on by the log-board: 49° 39' N, 5° 04' W, on the master's account before the sight, within what he would trust it. The latitude by observation lies five miles N of his.
```

Worked right, the slate gives the master's account: the same boards make the same reckoning, and that is the first thing to be sure of. The sun then judged both, and both were five miles south of the latitude: the master's own tide, out of his books, had set her further to the south-west than the sea did that forenoon. That is what the officer's own reckoning is for: not to agree with the master, but to be worked, judged, and in time trusted, and to say so when the officer thinks the master's tide or his leeway is wrong. Change the figure the slate gives where you have reason, and say the reason in your journal.

**The usual mistake.** Leaving the tide out of the working, which is the column most often forgotten on a slate of courses and distances. Worked so, from the same slate, the run's reckoning was 49° 42.1' N, 5° 04.6' W:

```
  Forenoon watch (11:31)  Mr Pearce's own reckoning: 49° 42' N, 5° 05' W, two miles and a half NE of the master's account, within what he would trust it; kept beside the master's, it moves nothing, and is said at noon.
* Afternoon watch, 8 bells (12:00)  The officer of the watch's own reckoning (Mr Pearce), worked at 11:31 and run on by the log-board: 49° 41' N, 5° 01' W, two miles and a half NE of the master's account before the sight, within what he would trust it. The latitude by observation lies three miles N of his.
```

It came out nearer the sun than the master's that day, and was still worked wrong: the sea's tide and the master's book did not agree, and the error happened to lean the same way. One noon proves nothing. Keep the tide in, and when the sun and your working disagree day after day the same way, that is a set the books do not know (lesson 3 says what to do with it).

## 3. A pilotage by cross bearings, and the allowance for a set

**The duty.** To take her through pilot water by fixes, giving the dangers their berth, and to allow for a stream the master's books do not know.

**The rule.** "The reckoning is always to be corrected, as often as any good observation can be obtained" (Falconer, *Dead-reckoning*); in pilot water the good observation is the fix by two or three marks that cut well, which the master works by the one rule ([chapter 10](10-the-reckoning.md)): marks near before marks far, and never two that cut within thirty degrees, since two lines that nearly lie one on the other cross nowhere in particular. Look at the dangers before shaping a course (`the dangers`), and shape for a berth off them, never for the danger itself: the master says what the line passes. Where two fixes show the account running off the same way, the difference is the current, which Bowditch's *Practical Navigator* (1802) has the navigator find by comparing the account with the observation and allow as one more course; `allow <n> knots of set to <point>` puts your set in the traverse and in every course shaped, in place of the master's own tide, until `allow the tide by the book` hands it back (chapter 10). Nothing turns your set for you when the tide turns.

```orders frigate plain-sail
take a fix
allow half a knot of set to the south south east
shape a course for a mile east of the Manacles
trim sails
take a fix
# rejected: take a fix by St Anthony's Head and Pendennis Point
allow the tide by the book
```

**The run** (`data/scenarios/lesson-falmouth.yaml`, seed 7): the frigate four miles south-east of Black Head at eight in the morning of 14 June, the westerly on her beam and Falmouth to the north. She fixed at once, and again half an hour on:

```
  Forenoon watch (08:01)  Fixed by cross bearings: Coverack N by W, the Lizard WNW, Cadgwith Cove NW by W; the lines met within six cables. The account moved three cables to the W by N: 49° 56' N, 5° 05' W by the fix, good to four cables along the shore and three cables off it.
  Forenoon watch, 1 bell (08:30)  Fixed by cross bearings: Coverack NW by N, Cadgwith Cove W by N, Manacle Point N by W; the lines met within five cables. The account moved three cables to the SSE: 49° 58' N, 5° 02' W by the fix, good to three cables.
```

In the half hour between, the master had allowed his own tide, two knots and a quarter to the west and then a knot and a half to the south-west, and the fix found his account three cables north-north-west of her: the stream had set her that much more to the south-south-east than his book. Three cables in half an hour is about half a knot. The officer allowed it, shaped for a berth off the Manacles, and fixed again twenty minutes on:

```
  Forenoon watch (08:31)  Allowing half a knot of set to the south-south-east in the reckoning, by the captain's order, in place of the master's own tide.
  Forenoon watch (08:32)  Shaped a course for a mile east of the Manacles: N by E by account, 5 miles; the line passes the Manacles within five cables. Allowing half a knot of set to the SSE by the captain's order, steer N by E to make it good. Helm ordered: steer N by E (6°).
  Forenoon watch (08:50)  Fixed by cross bearings: the Manacles N by W, Coverack WNW; the lines cut at 50 degrees. 50° 00' N, 5° 01' W by the fix, good to two cables along the shore and a cable off it; the account kept, within half a cable of it.
```

"The account kept": the set was right. The allowance overrules the master, so it is the captain's, and an officer's only by the captain's word naming it (chapter 16). When the pilot came aboard she handed the tide back to the master's books.

**The usual mistake.** A fix by two marks that lie nearly one behind the other. Off the Manacles St Anthony's Head and Pendennis Point both lie to the north, and the master will not have it:

```
  Forenoon watch (08:51)  Order not carried out ("take a fix by St Anthony's Head and Pendennis Point"): St Anthony's Head and Pendennis Point cut too fine for a fix: they bear N and N by W, their lines within 9 degrees of one another, and a fix wants 30. Take a bearing of one for a line, or wait for a mark that cuts better.
```

Said bare, `take a fix` lets him choose the marks that cut best. The other mistake is the allowance left standing when the stream turns: it is yours until you hand it back.

## 4. Heaving to for a pilot

**The duty.** To take the pilot aboard from his boat without running her down or leaving her astern.

**The rule.** Luce's way of lying stationary "to await the coming up of, or to speak another vessel", is to heave to: the main yards braced square with the fore yards full, so that "though the sails on the main mast are aback, she will range ahead slowly" (Luce 1866, ch. XXVI, 'Two or more Vessels communicating at Sea: Heaving to'); the pilot's boat comes alongside under her lee. A pilot comes aboard only when the captain takes him ([chapter 14](14-the-port.md)), and taking him is the port's business, the captain's or by his word. Heave to when the boat hails, take the pilot, and fill away when he is aboard, and only then give her a course.

```orders frigate plain-sail
heave to
# rejected: take the pilot
fill away
shape a course for Falmouth outer road
```

`take the pilot` is refused in this book's frigate, with no pilot's boat in sight: "There is no pilot to take: no pilot's boat is in sight." **The run** (the same scenario, an hour on), standing in for Falmouth with the pilot's cutter coming off:

```
* Forenoon watch (09:36)  The cutter hailed: a pilot for Falmouth, if you will take him.
* Forenoon watch (09:40)  Hove to on the larboard tack, main topsail to the mast, helm a-lee.
  Forenoon watch (09:40)  Answered the cutter: we will take the pilot for Falmouth.
* Forenoon watch (09:41)  The pilot, Mr Tregenza of Falmouth, came aboard from the cutter to pilot her in.
* Forenoon watch (09:41)  Filled away on the larboard tack; braced full and steering NNW (336°).
  Forenoon watch (09:41)  Shaped a course for Falmouth outer road: NW by N by account, 3 miles; the line passes the Old Wall within two cables. Allowing the ebb, a quarter of a knot to the W by S, steer NW by W to make it good, a point and a half of leeway allowed; the allowance holds till the tide turns, about a quarter past two in the afternoon. NW by W (309°) lies too near the wind to be laid; she is kept full and by on the larboard tack. Helm ordered: keep her full and by.
```

The hail asked nothing of her sail ("if you will take him"): she was slow enough over the ground for the boat, the ebb against her. A ship faster than six knots over the ground is asked to shorten sail, and at the second hail to heave to (chapter 14); hove to, she is slow enough at any speed she had. He does not con her: the course in was the officer's, and he warns. Read what he says when he comes aboard (`ask the pilot about the channel`): in Falmouth, the Black Rock in the middle of the entrance, the eastern channel the better.

**The usual mistake.** The course given before she has filled away. In another run of the same scenario the officer gave the three orders together as the pilot came aboard:

```
  Forenoon watch (09:37)  Order not carried out ('shape a course for Falmouth outer road'): She is hove to; fill away before giving her a course.
```

and she filled away a few minutes later steering where the fill-away left her, north-north-west for the entrance, with nobody's course on her until the lookout called the Black Rock "steady and closing". Give the course when the log says she has filled away.

## 5. Coming to in a tideway

**The duty.** To bring her up to an anchor where the stream runs, with scope enough to hold and no more than the berth allows, and to weigh again.

**The rule.** "Lying at anchor in a tideway, a vessel will ride to the wind or tide whichever is the stronger" (Luce 1866, ch. XXI, 'Getting under way in a Tideway'), and swings at every turn of the tide; Luce's chapters on anchoring and mooring (ch. XXXIV, XXXV) have the scope veered to the weather and the berth. Come to with her way off, head to the stream, sounding as she goes in. In the game, `let go the best bower` lets it go where she is and **veers five times the depth by itself**; `veer to <n> fathoms` and `heave in to <n> fathoms` act on **the anchor she rides by**, and so does `weigh` said alone ([chapter 13](13-the-tide-and-the-anchor.md)); name the other anchor when you mean it. In a narrow berth keep the scope short, so that her swinging circle stays small: the officer of the ninth game wrote that one in its journal.

```orders frigate plain-sail
standing order "the lead": every 5 minutes then heave the lead
heave to
let go the best bower
strike standing order "the lead"
veer to seventy fathoms
weigh
```

**The run** (the same scenario): the pilot aboard, she stood in for the outer road with the lead going every five minutes, hove to in twelve fathoms, let go, and veered a little more when she was brought up:

```
* Forenoon watch (10:23)  Quarter less twelve; good ground. The account moved three cables to the SE by S.
* Forenoon watch (10:27)  Hove to on the larboard tack, main topsail to the mast, helm a-lee.
* Forenoon watch (10:30)  The best bower let go in twelve fathoms and a half; sixty-three fathoms of cable veered.
* Forenoon watch (10:39)  Brought up by the best bower in twelve fathoms and a half, sixty-three fathoms of cable; Riding by the best bower to the ebb, the wind across the tide.
  Forenoon watch (10:39)  Veered to seventy fathoms on the best bower.
* Afternoon watch (12:19)  The cable slack at the turn; she swings to the flood. Riding by the best bower to the flood, the wind across the tide.
* Afternoon watch (12:34)  The best bower is aweigh.
* Afternoon watch (12:41)  The best bower catted and fished; she is under way.
```

Sixty-three fathoms is five times the twelve and a half she let go in, veered by the order itself; `veer to seventy fathoms` and `weigh` both went to the best bower, the one she rode by. At the turn she swung to the flood, which is when a foul anchor or too long a scope in a crowded road shows itself. A pilot anchored in the outer road stays aboard: a ship from sea waits there for her tide to go in (chapter 14).

**The usual mistake.** Naming the wrong anchor:

```
  Afternoon watch (12:19)  Order not carried out ('weigh the small bower'): the small bower is at the bows, not down; she rides by the best bower
```

And weighing with no sail ready: the run's frigate, aweigh with her sails as she had lain at anchor, was under way and helpless in the same minute ("Her sails aback; she had no way on to lose"), and the stream had her. Luce's order is sail first, then the anchor (chapter 13).

## 6. A night standing off a lee shore

**The duty.** To keep her off a coast the wind blows on, through a night, and have her offing at daylight.

**The rule.** "In clawing off a lee shore, all the sail possible must be carried" (Luce 1866, ch. XXIV, 'Clawing off a Lee Shore'), which is all the sail she can carry close-hauled: clawing off is, in Falconer's word, "beating, or turning, to windward from a lee-shore, so as to acquire a sufficient distance from it" (*Clawing*). Stand off and on by boards on the tack that makes offing, braced sharp up and full and by; reef before the night, not in it; go about in stays, which loses no ground, and wear only if she misses, which loses much; and do not stand in on the shoreward board further than the lookout can see by night, which is a mile ([chapter 10](10-the-reckoning.md), the nearest land). Look at the sails before shifting the helm, and brace up before hauling toward the wind: two more of the ninth game's officer's own lessons.

```orders frigate plain-sail
brace sharp up on the starboard tack
keep her full and by
take in the topgallant sails
reef the topsails
standing order "the land": at land ahead then tack ship
tack ship
wear ship
the nearest land
```

**The run** (`data/scenarios/lesson-lee-shore.yaml`, seed 7): the frigate twelve miles south of the Nare Head at eight in the evening of 14 June, a fresh southerly blowing straight on the coast between the Lizard and the Deadman. Braced up, the topgallants taken in and the topsails reefed before dark, a night order to go about at the lookout's warning of land, `wear ship` ready if she missed stays, and a board of two hours each way:

```
  First watch (20:05)  Braced up for the starboard tack, the after yards two degrees sharper.
* First watch (20:29)  Reefed the main topsail; now set, 1 reef.
* First watch (22:05)  Tacked; braced up on the larboard tack, heading W by S (254°).
  First watch (22:08)  Steady, full and by, the wind 49° on the larboard bow.
  First watch, 6 bells (23:00)  The nearest land: none seen within a mile; by night the shore shows no further off than that, and land beyond it cannot be told.
* Middle watch (00:07)  Tacked; braced up on the starboard tack, heading ESE (110°).
* Middle watch (02:05)  Tacked; braced up on the larboard tack, heading WSW (246°).
  Middle watch (03:50)  Order not carried out ('take a fix'): Only the Lizard lights is in sight, and one mark gives a line and no fix: take a bearing of the Lizard lights.
```

She kept the sea all night, and at dawn the only land in sight was the Lizard's lights. The reading at eleven is the one to understand: by night the lookout cannot say there is no land beyond a mile, only that he sees none within it, and on a lee shore that is the distance you have to act in.

**The usual mistake.** `trim sails` where `brace sharp up` was meant, and nobody looking to see that she came about. In another run of the same scenario the officer kept her full and by and then trimmed the sails, which braced the yards to the wind where it was as she paid off, abaft the beam; she ran east at nine knots on a reach, missed stays at ten, fell off on the old tack, and stood on in the dark:

```
  First watch (20:10)  Braced twelve yards to the wind, 103° on the starboard quarter, abaft the beam; trimming the sheets of the mizzen spanker, the fore topmast staysail and the jib.
  First watch (21:00)  Hove the log: nine knots and three quarters.
  First watch (21:22)  The deep-sea lead would not get bottom with the way she has on; bring her to, or shorten sail, and try again.
! First watch (22:23)  Missed stays: she lost her way before her head came up to the wind. Up helm; square the yards; flatten in the head sheets; ease off the spanker sheet.
* First watch (22:24)  Squared the yards; she fell off on the starboard tack, to try again or to wear.
  First watch (22:29)  Steady on E by N (78°).
* Middle watch (00:22)  Could not go about: she is not close-hauled; bring her by the wind before going about.
! Middle watch (02:26)  Missed stays: she lost her way before her head came up to the wind. Up helm; square the yards; flatten in the head sheets; ease off the spanker sheet.
* Middle watch (02:55)  The Bolt Tail bearing E, steady and closing: distant two miles.
* Middle watch (02:58)  Land right ahead, a mile: she is standing into it.
! Middle watch (03:04)  Land close ahead, fine on the starboard bow, four cables! She will be on it in three minutes.
! Middle watch (03:07)  She has taken the ground forward: two fathoms and a half of water by the chart, and she draws 15 feet; she struck at seven knots and a half, heeling 5 degrees, the tide rising.
```

Every line of that night said what was wrong while there was time: the wind abaft the beam on a ship that was to be by the wind; the deep-sea lead that could not get bottom with her way, and a dozen hands at it every glass, so that the tack ordered at ten began at twenty past; "missed stays" twice, and "steady on E by N" after each, a course nobody gave; "could not go about: she is not close-hauled". Read the line each order makes, and answer it.

## What neither of you knew she could do

| What | Where it is shown | In a word |
|---|---|---|
| `allow <n> knots of set to <point>` | lesson 3 | your set in the traverse and in every course shaped, in place of the master's tide, until `allow the tide by the book` |
| `observe an amplitude` | lesson 1 | the variation as it is today, at the sun's rising or setting, allowed from then on |
| what `let go` veers by itself | lesson 5 | five times the depth; say `let go the best bower and veer to <n> fathoms` for another scope |
| what `veer to` and `weigh` act on | lesson 5 | the anchor she rides by; name the other to mean it |
| when a bearing's distance is laid down | lesson 1 | weighed always, and counting for much only where the master's own doubt along the line of sight is the greater: after a long run, or at a departure |
| `work my reckoning`, `my reckoning is` | lesson 2 | the master's slate, and your own reckoning beside his at noon |

## The path to a command

Asked in the ninth game whether a command of its own would interest it, the officer of the watch said yes, and that it would want first "to have made a few more landfalls on my own reckoning, and taken her in and out of a road or two without your hand on the con". Those are the two conditions, in its words, and this chapter is the path to them:

1. **Landfalls on your own reckoning.** Keep your own reckoning on a passage (lesson 2), make the landfall on it (lesson 1), and let the land and the noon sun judge it, day after day, until it is trusted.
2. **In and out of a road without the captain's hand on the con.** Take her in by fixes past the dangers (lesson 3), take the pilot (lesson 4), come to an anchor in the road with the stream running and weigh again (lesson 5), and keep her off the land when the wind blows on it (lesson 6), with the captain's general authority to work the ship (chapter 16) and no word of his needed.

A captain who has seen both done gives the command; until then the captain's station (chapter 17) says what it holds, and the officer's journal is where the record of each is kept.

## Where it comes from

Falconer 1780, *Land-fall*, *Variation*, *Dead-reckoning*, *Log-board*, *Traverse*, *Clawing*; the Regulations and Instructions of 1806 (the 1808 printing in `docs/references/admiralty/`), the Master, art. XXXII, the Lieutenant on his log-book, and the Captain's articles on the mates' and midshipmen's log-books; Luce 1866, ch. XXI, 'Getting under way in a Tideway', ch. XXIV, 'Clawing off a Lee Shore', ch. XXVI, 'Two or more Vessels communicating at Sea: Heaving to', and ch. XXXIV and XXXV, anchoring and mooring; Bowditch, *The New American Practical Navigator*, 1802, on currents; the pilots chapters 10 to 15 cite for the water off Falmouth (White 1835, Imray 1874). The design is spec M6 §5 and §6, from the review of gate 5c's playtests (`docs/playtests/2026-10-05-gate-5c-review/report-2.md`, G19), which quotes the officer of the ninth game; the package is 40b in `docs/dev/M6-WorkPackages.md`, and the runs, every order and the minute it was given, are in `docs/dev/TuningNotes.md` under it.
