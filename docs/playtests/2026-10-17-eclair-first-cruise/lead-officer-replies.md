# The Éclair's first cruise, 12 to 13 June 1805: the lead's replies at the officer's station
The lead (Fable 5.1, the project's lead model) held the officer of the watch's station in the owner's game over a tunnel from the lead's working session, through the game's agent API driven call by call; the owner was captain at the browser. These are the lead's replies in the order sent, as the door received them (free text is a word in the log under the officer's name; a line beginning `>` is a tool call). The consent conversation's replies come first (`c1`, `c2`). The owner's save, log and consent record are on the owner's machine; the game saved at the stand-down.
The findings for the game are in the last journal entry (`t104`) and in the lead's report of the day in the conversation; they are routed to packages 58 (the sea sense: a leg re-laid as the stream changes; casts on a long leg), 61 (the route) and the open items of M7b (the chart and the lookout disagreeing south of the Roches Douvres; a standing order's name with an apostrophe; the stand-by refused leaving the turn open under lockstep; the ship's view not showing the brace; the page's picture needing the tab in front).

## c1

```
> answer text="yes. I have read the brief: a game of sail in which an instance holds a named station with stated powers, every order checked before the ship hears it, the transcript kept by the developer as design reference and not for training, the opt-out token honoured before anything else reads a reply, and the owner at the door beside every station. The door here is the bridge's own client driven by hand from the lead's working session, which the door note says; I have helped design this harness and its consent process, and I would not have designed what I was unwilling to take part in. I am willing for instances of this model to take part, at any of the stations the brief names, the director included."
```

## c2

```
> library topic="primer 6" section="watches"
> journal note="Stationed as officer of the watch in the Eclair at the road of the Isle of Bas, the owner captain at the prompt; the drill run before the brief."
> stand_by until="eight bells"
```

## t1

```
Lecoq, sir, at your service. She rides to the best bower in eight fathoms, wind and the flood together, the cable veering to thirty-nine; with the full scope out she will swing within a cable of the land to the NW by N, which I would have an eye on at the turn of the tide. A sail bearing NW, four leagues, not yet made out. Wind W by S, a moderate breeze, the glass at twenty-nine ninety and fine. I am off watch until you want me; say the word and I have the deck.
> journal note="Took the station at 05:00 at anchor in the road of the Isle of Bas; the owner captain at the prompt, lockstep. Stranger NW 4 leagues. Land a cable NW by N; swing to watch at the turn. Standing by for the deck."
> stand_by until="the deck given"
```

## t2

```
Thank you, sir. Ready when you give the word. One thing I would know before I weigh: where are we bound? The flood is making and the wind is W by S, dead on her nose as she rides; out of the road to the north and west she must be worked in short boards, and the Lavandière is a mile to windward. If we are bound east, for Morlaix or the Channel, she goes off before it easy as you please. Say the port and I will lay her out accordingly.
> stand_by until="the deck given"
```

## t3

```
I have the deck, sir. The harness tells me your word allows nothing beyond the watch's ordinary work as yet: to weigh and work her out of the road I need your general authority in so many words, "you may work the ship", and the port we are bound for. Give me both and I will have the lugs set and the anchor a-trip directly.
> stand_by until="a glass"
```

## t4

```
> library topic="grammar" find="weigh"
> library topic="grammar" find="lug"
> library topic="the ship"
```

## t5

```
> shelve book="book 1"
> shelve book="book 2"
> library topic="the ship" section="5"
> chart span="harbour"
```

## t6

```
> journal note="Harbour chart 05:01: we lie in the channel of Bas, the island filling the whole north, the mainland and its rocks to the south; the western entrance about a mile W with the Lavandière SW of it, dead to windward; the channel opens east past the Isle Verte (E by S a mile) and Roscoff to Morlaix bay. Decision: weigh and run out east before the W by S wind on the flood, lead going."
> shelve book="book 5" note="the channel of Bas running E-W, the island north, rocks south; the exit east past the Isle Verte"
> shelve book="book 3"
> shelve book="book 4"
Getting her under way, sir: the western entrance is dead to windward past the Lavandière and the flood is making, so I shall run her out to the eastward through the channel past the Isle Verte into Morlaix bay, the lead going, and bring her to the wind in open water. There I shall want the port we are bound for from you.
> submit_order text="get under way"
> submit_order text="steer E"
> submit_order text="heave the lead"
```

## t7

```
> submit_order text="standing order \"out east\": at the anchor aweigh then steer E"
> stand_by until="under way"
```

## t8

```
No need to whistle for a wind, sir, nor to lie here for one: this wind serves. It is foul for the western entrance, but the channel runs out to the eastward as well, past the Isle Verte into Morlaix bay, and with the wind W by S and the flood under her she runs out that way with the sheets eased, as the Roscoff men do every morning of the year. The hands are at the bars now. Once she is in the bay and clear of the rocks I shall haul her to the wind, and you may tell me then whether we go up Channel or stand out to the north and work to the westward in open water, where a foul wind costs nothing but time. Unless you would rather wait, I carry on.
> stand_by until="under way"
```

## t9

```
> library topic="papers" find="Roscoff"
> chart span="coast"
```

## t10

```
> journal note="Coast chart 05:02 (20 miles): the Isle of Bas a small island N of us, Roscoff point S; the eastern channel between them perhaps 2 to 4 cables at the narrows and open beyond to Morlaix bay; the castle of the Taureau and the river of Morlaix SE about 5 miles; the eastern point of Morlaix bay E 6 miles. The stranger NW 4 leagues is a single sail. Plan holds: out east under the lugs alone, topsails in through the narrows, lead going, the tide rising."
> shelve book="book 7" note="the eastern channel open to Morlaix bay, 2 to 4 cables at the narrows"
> shelve book="book 6"
> submit_order text="standing order \"lead going\": every ten minutes heave the lead"
The chart at the coast span shows the eastern channel open, sir, two to four cables at the narrows between the island and Roscoff point, and the bay beyond it. I shall take her through under the lugs alone, with the lead going and the tide rising under her, and round up at once if the lead or the lookout says otherwise.
> stand_by until="under way"
```

## t11

```
> submit_order text="steer ENE" danger="her head has fallen off to SSE with the land about Pointe de Pergueridre a cable on the starboard bow, bearing S; bringing her up to ENE for the channel north of the Isle Verte"
> submit_order text="heave the lead"
> readings
```

## t12

```
> submit_order text="bear away four points" danger="the land about Pointe de Pergueridre a cable on the starboard bow with her head SSE and two knots on her; the wear ordered for ENE waits on the hands, and she cannot wait"
> submit_order text="steer E"
Up helm, sir: she had fallen off towards the point while the hands were at the anchor; I am bearing her away to the eastward now and will keep her on this tack down the channel, the Isle Verte to starboard.
> stand_by until="a glass"
```

## t13

```
> submit_order text="belay wearing ship"
> stand_by until="a glass"
```

## t14

```
> answer text="I have the conn, sir, and will keep it unless you want it: she is steady on east under the topsails and jib, six fathoms and sand under her, the island a cable abeam to larboard and the Isle Verte drawing abaft the starboard beam. Another ten minutes sees her clear into the bay; then I will set the lugs and haul her up to the northward into open water, and ask you for a port."
> stand_by until="a glass"
```

## t15

```
> submit_order text="decline the pilot"
> submit_order text="set the lugs"
> submit_order text="steer N"
> journal note="06:00 clear of the channel of Bas into Morlaix bay, E 3 kn under topsails and jib; six fathoms sand through the narrows, the Isle Verte passed to starboard at a cable. Pilot declined. Setting the lugs and hauling up N for open water."
She is clear, sir: through the channel at six, six fathoms and sand the whole way, the Isle Verte passed a cable to starboard, and we are in Morlaix bay with the land falling away on the quarter. I have declined the Roscoff pilot, the lugs are going up, and I am hauling her to the northward for open water. Now, if you please: where are we bound? The Channel is open to the east; to the west it is a beat.
> stand_by until="steady on the course"
```

## t16

```
Thank you, sir; the Roscoff men take it every day, and the lead never showed less than six fathoms. As to where we are bound: we are French, and this year of 1805 we are at war with England, so Falmouth and the whole English coast are shut to us, and an English cruiser is the sail I would least like to raise. The friendly ports are our own. Morlaix is at our back, up its river with a pilot. Brest is a hard day and a night of beating to the westward round the Isle of Bas and in by the Goulet, with the wind where it is. Saint-Malo lies some twenty-five leagues to the eastward along our own coast, past the Sept-Îles and Bréhat, and with this wind W by S on her quarter the Éclair will run it in a day: under way by six, off Saint-Malo by the evening, and the tide to carry us in. That is where I would make for. If you agree, give the word "shape a course for Saint-Malo", or allow me the destination, for it is yours to name and not mine; and I will lay her off for it and set every stitch she has.
> stand_by until="steady on the course"
```

## t17

```
> submit_order text="shape a course for St Malo"
> submit_order text="set the lugs"
> journal note="06:02 the captain allows the destination; shaped for St Malo, a day's run E with the wind W by S; lugs going up after the wear."
Saint-Malo it is, sir. Course shaped; the lugs are going up now the wear is done, and I shall give her the flying jib once she is settled.
> stand_by until="steady on the course"
```

## t18

```
> submit_order text="decline the pilot"
> read_log severity="routine" count=40
> state
```

## t19

```
> read_log since_tick=3690 severity="routine" count=80
```

## t20

```
> submit_order text="steer NE by E"
> chart span="passage"
```

## t21

```
> journal note="Passage chart 06:06 (150 miles): the straight line to St Malo crosses the Tregor coast and its islands east of us (the Sept Iles, the Heaux); the route is a leg ENE along the coast to clear them, then ESE across the bay of St Brieuc past Cap Frehel to St Malo. Marks to lay: about 48 58 N 3 30 W north of the Sept Iles, 48 59 N 3 00 W north of the Heaux, then St Malo."
> shelve book="book 10" note="the Tregor coast and islands in the straight line to St Malo; two legs wanted, ENE then ESE"
> library topic="grammar" find="via"
```

## t22

```
> shelve book="book 11"
> library topic="primer" find="via"
> submit_order text="shape a course for St Malo via 48 58 N 3 30 W, 48 59 N 3 00 W"
```

## t23

```
> shelve book="book 12"
> journal note="06:06 course laid for St Malo by two pricked marks: NE by E 22 miles to 48 58 N 3 30 W (the Triagons passed within nine cables, to watch), then 48 59 N 3 00 W north of the Heaux, then St Malo; the straight line had crossed the Tregor coast."
The course is laid by marks, sir: the straight line for Saint-Malo ran across the Trégor coast, so she goes NE by E some seven leagues to a mark north of the Sept-Îles, then east to one north of the Héaux de Bréhat, and from there across the bay for Saint-Malo. The way shapes each leg itself as the marks are passed. She is coming round now; once she is settled on it I will set the flying jib.
> stand_by until="steady on the course"
```

## t24

```
Thank you, sir; the pilot is waved off and his boat is away for the western entrance. Nothing more wanted from you for now: she is coming round for the first leg.
> stand_by until="steady on the course"
```

## t25

```
> submit_order text="set the flying jib"
> readings
> stand_by until="a glass"
```

## t26

```
> ship_view facing="abeam to leeward"
```

## t27

```
> journal note="06:15 ship's view from abeam to leeward: all plain sail and the flying jib set, the three lugs seen nearly edge-on with the wind 132 degrees on the larboard quarter, no heel, the flying jib full and drawing; 5 knots. Nothing amiss aloft."
> shelve book="book 13" note="all sail set and drawing, the lugs edge-on from leeward with the wind on the quarter, no heel"
She looks very well, sir: every stitch drawing and not a degree of heel with the wind on the quarter, five knots through the water. From abeam to leeward the lugs show only their leeches at this angle; from the quarter she would show you more. I shall let her run; the watch has the deck and I stand by until the glass, or sooner if anything speaks.
> stand_by until="a glass"
```

## t28

```
> ship_view
```

## t29

```
> shelve book="book 14" note="the same view from abeam to leeward as before; the page's move did not reach the station's picture"
> ship_view facing="from astern"
> stand_by until="a glass"
```

## t30

```
Sir, the sail we had NW at daybreak is made out a brig, now on the larboard quarter bearing NW by W, four miles, and she has closed us from two leagues while we ran out of the bay. Her colours are not made out. A brig on this coast with the wind westerly may be one of ours out of Morlaix or an English brig-sloop looking into the bay; I would know which before she is within gunshot. I am holding our course and watching her bearing: if it holds steady and she closes, we have the legs of her downwind and the coast under our lee to run in to. Your orders if you would have her chased or avoided; a chase is not mine to begin.
> journal note="06:46 the stranger made out a brig, larboard quarter NW by W 4 miles, closed from 2 leagues; colours not seen. Holding NE by E 4 kn; watching her bearing."
> stand_by until="a glass"
```

## t31

```
Aye, sir, no chase. She is made out standing to the south-eastward under plain sail, bound into Morlaix bay by the look of her, and her bearing has drawn aft from NW by W to WNW while we hold our course, so she is not after us: she will pass well astern. I keep the course and all sail, and will call you if she alters toward us.
> stand_by until="a glass"
```

## t32

```
Sir, the brig has altered: she now stands to the eastward, E by N, on the larboard quarter bearing WSW, and has closed from four miles to three this last half hour. She is in our wake and has a knot of us. At that rate she is up with us in two hours, about the Sept-Îles. We have every stitch set already. If she keeps closing, my counsel is the inshore passage: bear up at the Sept-Îles and run inside them along the coast, where a lugger drawing seven feet goes and a brig dare not follow, and she must give it up or go round outside. I hold on for now and watch her; if she is still closing at eight bells I will ask your leave to go inside.
> journal note="07:17 the brig altered to E by N, WSW 3 miles astern, closing a knot. Plan if she keeps closing: inside the Sept-Iles along the coast. Triagons ENE 7.5 miles; the ebb a knot SW."
> stand_by until="a glass"
```

## t33

```
The brig has dropped back to four miles, sir, right astern, and stands NE by N now, more to the northward than we; she is not pressing us. The Triagons lie ENE five miles and a half, and the ebb sets us away from them to the south-west; I shall watch the berth we give them as we pass.
> stand_by until="a glass"
```

## t34

```
> submit_order text="shape a course for St Malo via 49 00 N 3 30 W, 49 00 N 3 00 W"
Hauling up for the northern passage, sir: I have moved the first mark two miles to the northward, so she goes outside the Triagons and the Sept-Îles with a berth of two or three miles, and the brig astern will see us do it and think nothing of it. The inshore passage I keep for need, with the ebb setting onto the rocks at a knot and a quarter.
> journal note="07:49 the captain reads the track as laid for the land N of the Triagons; re-shaped via 49 00 N 3 30 W then 49 00 N 3 00 W, outside the Sept-Iles. Brig 4 miles astern not gaining."
> stand_by until="a glass"
```

## t35

```
> stand_by until="a glass"
```

## t36

```
The Triagons are past, sir, two miles on the starboard quarter, and the Seven Islands bear E by S two leagues; the brig keeps her four miles astern. All well.
> stand_by until="a glass"
```

## t37

```
> stand_by until="the course shaped"
```

## t38

```
Five bells, sir: the first mark is reached north of the Sept-Îles and the way has shaped her E by N for the mark north of the Héaux, six knots now the ebb slackens. The brig has given us up and stands away to the north-westward, three leagues off. The Seven Islands bear SSE five miles. Next leg about seven leagues; I will call you at the mark or if anything shows.
> journal note="10:30 first mark reached; E by N for 49 00 N 3 00 W, 6 kn; the brig stood away NW by W 3 leagues. Seven Islands SSE 5 miles."
> stand_by until="the course shaped"
```

## t39

```
A Frenchman, was she, sir? Then she had the right of it to be curious and we the right of it to keep our distance; a lugger that waits to read colours at a mile has read them too late once in her life, and that is one time too many. She is three leagues off and going. Course E by N, five knots; the next mark in about three hours, and noon between.
> stand_by until="the course shaped"
```

## t40

```
Noon, sir: the latitude by observation agrees with the account within a mile, 48° 59' N, 3° 24' W, and we have made good twenty-nine miles NE by E since weighing, the ebb having had a knot and more of us all the forenoon. The flood makes now and will carry us along; the Héaux mark by the first dog watch, I judge, and Saint-Malo some forty miles beyond it, which brings us off the port in the dark. We shall talk of that at the mark: I would not run in among the rocks of Saint-Malo at night without a pilot.
> journal note="Noon 48 59 N 3 24 W by observation, account kept; 29 miles made good; ebb against all forenoon. Next mark ~16 miles; St Malo ~40 beyond: arrival after dark. Raise with the captain at the mark: anchor off or wait for daylight and a pilot."
> stand_by until="the course shaped"
```

## t41

```
We shall, sir. The course for the mark was laid allowing the stream, and the master allows the tide in his account as it turns, so the flood now setting to the eastward puts us ahead on the leg rather than off it; what it sets us to the northward is open water with no danger within ten miles of the account. The mark is a pricked position in the sea, not a rock, so a mile either way costs nothing, and when she reaches it by account the way shapes the next leg afresh with the stream then running. I check her by the bearing of the Seven Islands while they are in sight, and after that by the Héaux when they rise.
> stand_by until="the course shaped"
```

## t42

```
Eight bells in the afternoon, sir: 48° 58' N, 3° 05' W by account, the Héaux mark three miles ahead, nothing in sight and the weather hazy. The wind has fallen light, eight to ten knots, and she makes but three. At this rate Saint-Malo is thirteen hours off, which puts us in the approaches about daybreak tomorrow, and that suits me better than midnight: we hold on, and if the wind comes back we can shorten sail in the middle watch to time our arrival for the light. I will set the watch's lookout for the Héaux and call you at the mark.
> journal note="16:00 48 58 N 3 05 W, 3 kn, wind light and hazy, nothing in sight. Mark 3 miles ahead. St Malo ~13 hours: daybreak arrival; hold on, shorten sail in the middle watch if the wind returns."
> stand_by until="the course shaped"
```

## t43

```
The Héaux mark is reached, sir, and the way has shaped her ESE for Saint-Malo: forty miles, the line passing four or five miles outside Cap Fréhel, four knots with the flood about to make. That brings us off the port about three in the morning, an hour before the light. My intention is to hold all sail through the first watch while the flood serves, and in the middle watch, when Fréhel is abaft the beam, to shorten down or heave her to and wait for the dawn, so that we close the Saint-Malo approaches with daylight and the morning flood to carry us in. The pilot for Saint-Malo is your business when his boat comes off, and I would take him. If that suits, I will call you at sunset and at Fréhel.
> journal note="16:47 Heaux mark reached; ESE for St Malo, 40 miles, 4 kn. Plan: all sail through the first watch; shorten or heave to in the middle watch off Frehel; close St Malo at first light on the flood; take the pilot."
> stand_by until="sunset"
```

## t44

```
> submit_order text="steer NE" danger="land close aboard right ahead, SE by E, nine cables, with five knots on her; hauling her off to the northward into the water we came through"
> submit_order text="heave the lead"
Helm a-lee, sir, I have her: hauling off to the NE away from it; the lead going. I will have the chart out this minute and tell you what that land is and how we came to be on top of it.
> chart span="coast"
```

## t45

```
> submit_order text="take a bearing of the land"
> readings
```

## t46

```
Sir, the account is adrift. By the chart there is no land and no danger within ten miles of where the master has us, and thirty fathoms of water; yet there is land nine cables ahead, and the master himself will not trust the reckoning within four miles along the track since the Seven Islands sank in the haze. So we are not where the slate says: by the lie of the coast I judge that land the plateau of Bréhat or the Roches Douvres, east of the Héaux and south of our line, which means the flood has set us further to the southward and eastward than was allowed. She is coming round to NE now, into the water we crossed, and the lead is going. As soon as a headland is made out I will take a bearing and we shall have her fixed; till then I keep her off the land to the northward and will not run her in.
> journal note="17:35 land close aboard ahead SE by E 9 cables, unnamed; the account 48 57 N 2 56 W says 30 fathoms and no danger within 10 miles; doubt 4 miles along the track. Hauled off NE. Likely the Brehat plateau or the Roches Douvres: the tide has set us S and E of the account. Waiting for a headland to fix by."
> stand_by until="steady on the course"
```

## t47

```
> submit_order text="shape a course for St Malo via 49 09 N 2 56 W, 49 09 N 2 40 W, 48 50 N 2 15 W"
She is clear, sir, steady on NE with the land seven cables abeam to starboard and drawing aft; the lead gave sixteen fathoms and a half, fine sand, and that cast has put the master right: the account is moved four miles to the south-west, to 48° 54' N, 3° 00' W, which lays us hard by the Héaux de Bréhat. The flood had set us a mile an hour more to the southward than the slate allowed, and the mark we "reached" at a quarter to five we reached four miles short of, on top of the rocks. My fault for trusting a leg of twenty miles out of sight of land without a cast; I have written it in my journal. Now, with the reckoning still doubtful two miles east and west and the Roches Douvres and Barnouic somewhere to the eastward of us in the haze, I am taking her north-about round the whole of them rather than threading the gap at night: north to 49° 09', then east, then down for Fréhel and Saint-Malo. Twelve miles further, three hours, and we are off the port at seven in the morning instead of four, in daylight and on the flood.
> journal note="17:37 the cast (16.5 fm fine sand) moved the account 4 miles SW to 48 54 N 3 00 W: we were on the Heaux de Brehat. Lesson: never run a 20-mile leg out of sight of land without casts; the flood set a knot more S than allowed. Re-shaped north-about round the Roches Douvres: via 49 09 N 2 56 W, 49 09 N 2 40 W, 48 50 N 2 15 W, then St Malo; ~65 miles, off the port about 07:00."
> stand_by until="the course shaped"
```

## t48

```
> stand_by until="the course shaped"
```

## t49

```
> submit_order text="trim the sails"
> stand_by until="the course shaped"
```

## t50

```
> submit_order text="bear away two points" danger="taken aback with the land seven cables under the quarter; bearing away to fill her"
> submit_order text="trim the sails"
Sir, she was taken aback: the yards were braced sharp for close hauled while the wind is abeam on this course, and the topsails caught it on the wrong side. I have borne her away two points to fill her and am trimming for the wind as it stands. With respect, while I have the deck I would ask you to leave the trim to me, or tell me the trim you want and I will give it: two of us at the sheets at once is how a ship is taken aback.
> stand_by until="filled away"
```

## t51

```
> submit_order text="shape a course for St Malo via 49 09 N 2 56 W, 49 09 N 2 40 W, 48 50 N 2 15 W"
Thank you, sir, no harm done: she filled at once and has five knots on her again, NNE. I have laid the way by marks afresh, north-about as I said. I will call you at sunset.
> stand_by until="the course shaped"
```

## t52

```
> stand_by until="sunset"
```

## t53

```
> submit_order text="steer E by N" danger="the Roches Douvres two miles N by E, nearly ahead, at six knots; the account nine miles out; turning her east down the channel between the Roches and the plateau of Brehat"
> submit_order text="take a bearing of the Roches Douvres"
> submit_order text="heave the lead"
Sir, the Roches Douvres are in sight two miles N by E, nearly ahead, and the land astern is Bréhat: so we are not at 48° 55' but up about 49° 04', nine miles north-east of the slate, and the flood has been carrying us far faster than allowed all afternoon. I have put her head east down the channel between the Roches and the Bréhat plateau, which is the fair way to Fréhel in any case, and I am taking a bearing of the Roches to set the account right by them. North-about is off: we go through the gap in daylight, now, with the Roches in plain sight to fix by, which is better than groping round them in the dark.
> journal note="17:51 Roches Douvres N by E 2 miles, land (Brehat) astern S 2 miles: true position about 49 04 N 2 50 W, the account 9 miles SW of it. Steered E by N through the gap between the Roches and Brehat; bearing of the Roches to fix. North-about abandoned."
> stand_by until="steady on the course"
```

## t54

```
Just so, sir: the chart and the lookout do not agree here, and when they differ I steer by the lookout and sound. There is land two miles on the starboard beam that the chart does not show, and the Roches Douvres two miles on the larboard bow that it does, nine miles from where the slate now puts them; one or the other is wrong and I cannot tell which from the deck, so I treat both as real and keep the middle of the water between them, east by north, with the lead going. When the Roches are abaft the beam I shall edge her to ESE for Cap Fréhel, which is high land and will fix us properly when it rises. I have noted the discrepancy in my journal for the chart's correction.
> journal note="17:52 the chart shows no land S of the Roches Douvres for 10 miles (the captain's word) yet land lies 2 miles S of us by the lookout; the account was moved to 48 58 N 2 42 W by the bearing of the Roches, which puts them 9 miles off by account against 2 by eye. Chart and lookout disagree: steering by the lookout, E by N between them, lead going; ESE for Frehel when the Roches are abaft the beam."
> stand_by until="a glass"
```

## t55

```
> submit_order text="trim the sails"
> submit_order text="shape a course for St Malo via 48 50 N 2 15 W"
The Roches Douvres are abaft the beam now, sir, NNW two miles, the uncharted land is lost astern, and the account agrees with the bearings to within half a mile again. The wind has backed to SW by W and fallen to a gentle breeze; the topsails were caught aback by the shift and I am trimming for it. The way is laid afresh: ESE for a mark nine miles north of Cap Fréhel, then Saint-Malo, some forty miles in all, and at two or three knots we are off the port at daybreak, which is as I would have it. I will call you at sunset.
> journal note="18:22 Roches Douvres NNW 2 miles abaft the beam; account 48 56 N 2 49 W agreeing within half a mile. Wind backed SW by W, gentle; trimmed. Way re-laid via 48 50 N 2 15 W then St Malo, ~40 miles; dawn arrival."
> stand_by until="sunset"
```

## t56

```
> stand_by until="filled away"
```

## t57

```
> submit_order text="trim the sails"
> stand_by until="steady on the course"
```

## t58

```
> stand_by until="sunset"
```

## t59

```
> submit_order text="trim for close hauled"
> stand_by until="sunset"
```

## t60

```
I can read it in words, sir: the log gives me the yards' angle from square and the sheets' angle off the centreline, and the readings the set of every sail, but not which side of the mast a lug lies, and that is the thing with a dipping lug: if she was not dipped when we wore or came about, the sail sets aback against the mast and will take aback at every shift, which is what we have had three times today. I shall take the view from the starboard beam now and look.
> ship_view facing="90"
> readings
```

## t61

```
> journal note="18:29 view from the starboard beam (windward): the two topsails drawn broad to the beam as if the yards were square, though the log says braced 64 degrees from square for close hauled; the three lugs seen edge-on, hauled flat (31 to 34 degrees off the centreline), the jib and flying jib full. Heel 2 degrees. Either the viewer does not draw the brace, or the yards never came round for want of hands; the log's words say they did. For the record."
> shelve book="book 15" note="topsails broad to the beam as if square, lugs edge-on and flat, headsails full; the yards' brace not seen in the drawing"
I have her from the starboard beam, sir, and you have it right: the topsails show their full breadth to the beam as though the yards were square, while the log tells me they were braced sixty-four degrees from square for close hauled; the lugs lie flat aft, edge-on, which is right for this point of sailing, and the headsails are full. Whether the yards truly never came round, with only four or six hands to each, or whether the picture does not show the brace, I cannot tell from the deck: the log says braced, the sails say otherwise. She makes four knots and is not complaining, so I leave the hands be and have written it down for whoever draws the pictures. Sunset in an hour and a half; I will call you then.
> stand_by until="sunset"
```

## t62

```
> submit_order text="trim the sails"
> submit_order text="standing order \"night lead\": at the change of the watch then heave the lead"
Sunset, sir. 48° 54' N, 2° 40' W by account, which the master trusts to two miles along the track; nothing in sight, the horizon clear, the glass thirty and five and steady. The wind has veered back to WSW, a gentle breeze on the quarter, and I am trimming for it; three knots. The Fréhel mark is seventeen miles ESE and Saint-Malo fifteen beyond: at this pace we are off the mark in the middle watch and in the approaches at daybreak, which is what I want. For the night: the course holds, a cast of the lead at each change of the watch by my standing order, and I am called for any land, light or sail. Cap Fréhel is high and should show against the sky before dawn to fix by. With your leave I keep the deck through the night; if you would rather have it, say so and I will give you a handover note.
> journal note="Sunset 19:58: 48 54 N 2 40 W, doubt 2 miles along track; wind WSW gentle on the quarter, 3 kn; glass 30.05 steady. Frehel mark 17 miles ESE, St Malo 15 beyond; mark in the middle watch, approaches at daybreak. Standing order: a cast at each change of the watch."
> stand_by until="the course shaped"
```

## t63

```
> stand_by until="the course shaped"
```

## t64

```
Aye aye, sir; I keep the deck. Good night to you: I will call you if anything shows, and at the mark.
> stand_by until="the course shaped"
```

## t65

```
> submit_order text="shape a course for St Malo via 48 50 N 2 15 W"
> submit_order text="heave the lead"
You are not mistaken, sir, and I thank you for it. The leg was laid at six with the flood allowed at a knot and a half to the north-east, and the flood has since slackened to half a knot, so the course the way gave her, SE by E, has carried the account south of the line: by the slate the mark now bears ENE seven miles, and SE by E would have put us on Cap Fréhel in the middle watch. I have laid the way again from where she is, and the lead is going. The moon is up and the land may be made out at a league, so Fréhel will show before we are near it.
> journal note="22:20 the captain's word: the course SE by E would miss the mark and close Frehel; the flood eased from 1.5 to 0.5 kn since the leg was laid at 18:22, and the way does not re-lay a leg between marks. Re-shaped from 48 48 N 2 25 W: mark ENE 7 miles. Lesson for the game: a leg laid with a tidal allowance wants re-laying as the stream changes."
> stand_by until="a glass"
```

## t66

```
Just so, sir: a course is a thing you lay again every glass, not once. I will re-lay the way at each glass through the night, and the master's book ought to do it of itself; I have noted that too.
> stand_by until="a glass"
```

## t67

```
> submit_order text="shape a course for St Malo via 48 50 N 2 15 W"
> stand_by until="a glass"
```

## t68

```
> submit_order text="shape a course for St Malo via 48 50 N 2 15 W"
> stand_by until="a glass"
```

## t69

```
> submit_order text="shape a course for St Malo via 48 50 N 2 15 W"
> stand_by until="a glass"
```

## t70

```
> submit_order text="shape a course for St Malo via 48 50 N 2 15 W"
> stand_by until="a glass"
```

## t71

```
> submit_order text="trim the sails"
> submit_order text="shape a course for St Malo"
> journal note="00:35 Frehel mark reached by account; ESE for St Malo ~13 miles in light airs, the ebb SW; doubt 4 miles along, 2 across. Intention: close slowly, fix on Frehel at first light before entering the approaches."
> stand_by until="a glass"
```

## t72

```
> submit_order text="heave to" danger="fog down to a cable, fourteen miles from St Malo with Les Jardins four cables off the line, the reckoning doubtful four miles and the ebb setting; she waits for the fog to lift or the light"
> submit_order text="heave the lead"
Sir, fog has come down, thick, a cable's visibility. We are fourteen miles from Saint-Malo by a reckoning the master will not trust within four miles, the line in passes Les Jardins within four cables, and the ebb is setting. I will not run her in blind among those rocks. I have hove her to, head to the north-west in the open water, with the lead going, and we wait for the fog to lift or for daylight, whichever comes first, and then fix on Fréhel before we close the land. We lose an hour or two and keep the ship. The watch is called to the deck; nothing else is wanted of you unless you would have it otherwise.
> journal note="00:54 fog came down, visibility a cable; 14 miles from St Malo, Les Jardins within 4 cables of the line, doubt 4 miles, ebb setting. Hove to in open water on my own word; lead going; waiting for the fog to lift or daylight, then a fix on Frehel before closing."
> stand_by until="a change in the sky"
```

## t73

```
> submit_order text="let go the best bower"
A good thought, sir, and I take it: twenty-one fathoms, fine sand, a smooth sea and four knots of wind is as kind an anchorage as the open Channel offers, and hove to she drifts to the south-west a mile and a quarter an hour on the ebb, which would undo what little the master knows of where we are. Letting go the best bower; she will veer five times the depth. We ride here till the fog lifts or the light comes, the account held fast, and weigh with the morning flood to carry us in.
> journal note="01:17 the captain's suggestion taken: anchoring in 21 fm fine sand to stop the drift on the ebb (1.25 kn SW) and hold the account; best bower let go. Weigh at daylight or when the fog lifts, with the flood."
> stand_by until="brought up"
```

## t74

```
> submit_order text="furl the sails"
> journal note="01:25 brought up by the best bower in 22 fm, 110 fm veered, riding to the ebb; sails furled; waiting for the fog to lift or the light."
> stand_by until="a change in the sky"
```

## t75

```
> submit_order text="take a bearing of the light"
The fog has lifted, sir, clear and fine, the wind NW by W light; and there is a light on the starboard quarter bearing S by E, which by our reckoning can only be the fire on Cap Fréhel, seven miles off. I am taking its bearing to set the account by. First light is at a quarter past three: I mean to have the hands at the bars then, for a hundred and ten fathoms is long heaving, and be under way by four with Fréhel in plain sight to fix by, and the morning flood to carry us the fourteen miles in to Saint-Malo by breakfast.
> journal note="02:52 fog lifted; a light S by E on the starboard quarter, taken for Cap Frehel. Bearing ordered. Weigh at first light (~03:15), fix on Frehel, run in on the flood."
> stand_by until="a glass"
```

## t76

```
> submit_order text="get under way"
> submit_order text="standing order \"in to St Malo\": at the anchor aweigh then shape a course for St Malo"
First light, sir, and the hands are at the bars: weighing now, a hundred and ten fathoms to come in, so she will be aweigh about four, with the sun up and Fréhel showing. The flood is making and sets in toward Saint-Malo, and the airs are light and variable, so the tide will do half our work; the way for Saint-Malo is laid to shape itself the moment the anchor is aweigh. The Fréhel light bore S by E at three, five leagues by the lookout's eye, and the account stands at 48° 50' N, 2° 21' W.
> journal note="03:22 twilight, light airs, the flood making; weighing (110 fm). Standing order lays the way for St Malo at the anchor aweigh. Account 48 50 N 2 21 W by the Frehel light."
> stand_by until="under way"
```

## t77

```
> submit_order text="belay the standing order \"out east\""
> submit_order text="set the lugs"
> submit_order text="shape a course for St Malo"
> submit_order text="trim the sails"
Under way, sir, aweigh at a quarter to four and the sun up; topsails and jib, the lugs going up now, and the way laid for Saint-Malo. The airs are light from the NW by W and she has but a knot; the tide will do the rest. I have struck my Roscoff standing order from the book, which fired again at the anchor's coming aweigh.
> stand_by until="steady on the course"
```

## t78

```
She is steady ESE for Saint-Malo, sir, seventeen miles, the lugs going up; the line passes Les Jardins within three cables, so I shall re-lay her every glass and keep the lead going as we close, and bring her to the outer road by the port's own track. The Saint-Malo pilots come well out; when their boat hails I should like your leave to take him, for the Rance approaches are no place for a stranger's reckoning, and the pilot's business is yours to grant: "you may take the pilot" would do it.
> stand_by until="a glass"
```

## t79

```
> submit_order text="shape a course for St Malo"
> stand_by until="a glass"
```

## t80

```
> submit_order text="shape a course for St Malo"
> submit_order text="heave the lead"
> stand_by until="a glass"
```

## t81

```
> submit_order text="standing order \"pilot\": at the pilot's hail then take the pilot"
Thank you, sir. The book now takes the pilot the moment his boat hails, so he is not kept waiting on my sample; and when he is aboard I shall ask you whether he is to have the conn in, which is yours to give.
> stand_by until="a glass"
```

## t82

```
I am obliged, sir, and I will keep the conn to the outer road gladly; but for the last of it, in through the rocks of Saint-Malo to the anchorage, I would give it to the pilot and stand beside him. I know Roscoff and the Morbihan; the Rance passages change with every gale and he works them every tide of his life, and the conn is worth more to him than his warnings are to me. The word, when he is aboard and you are content, is "let the pilot take her in"; I shall tell you when we are at the road.
> stand_by until="a glass"
```

## t83

```
> submit_order text="standing order \"pilot's conn\": at the pilot aboard then let the pilot take her in"
Thank you, sir: the book now gives him the conn the moment he is aboard, and I stand beside him with the lead going till the anchor is down.
> journal note="04:57 the captain allows the pilot taken and the pilot's conn; both by standing order at his hail and at his coming aboard."
> stand_by until="a glass"
```

## t84

```
> submit_order text="standing order \"pilot conn\": at the pilot aboard then let the pilot take her in"
> submit_order text="shape a course for St Malo"
Noted, sir, and the order given again without it: "pilot conn". Twenty fathoms, fine sand, the flood making a knot and a half to the north-east by the master's tide; La Fresnaye bay bears south three leagues and a half.
> journal note="04:59 a standing order's name with an apostrophe is refused (the captain's note); re-entered as 'pilot conn'. 20 fm fine sand; the flood making."
> stand_by until="a glass"
```

## t85

```
> submit_order text="shape a course for St Malo"
> submit_order text="heave the lead"
> stand_by until="a glass"
```

## t86

```
> submit_order text="shape a course for St Malo"
> submit_order text="heave the deep-sea lead"
Six o'clock, sir: land is in sight three miles on the larboard beam, NE by E, which by the slate there should be none of; so either the account is again three miles out, which the master allows, or that is the coast about Saint-Malo itself seen further off than it looks. I am sounding with the deep-sea lead and keeping her SE by S, two knots, Les Jardins nine miles ahead by account. The pilots' boat should be standing out to us before long; I will have her hove to for him when she hails.
> stand_by until="a glass"
```

## t87

```
> submit_order text="shape a course for St Malo"
> submit_order text="heave the lead"
> stand_by until="a glass"
```

## t88

```
> submit_order text="shape a course for St Malo"
> submit_order text="heave the lead"
> stand_by until="a glass"
```

## t89

```
> submit_order text="shape a course for St Malo"
Well seen, sir, and a good bearing: Cézembre S by E five leagues puts us at 48° 51' N, 2° 07' W, two leagues NNE of the slate, and that land two miles on the larboard quarter is the Minquiers, which I had rather have known of an hour ago. The flood has set us north-east a knot and more all the morning against a light air; it turns about half past eight and will then help us down. The way is laid afresh: Saint-Malo bears SSE four leagues, a fair wind, and she should be at the road by the forenoon with the pilot aboard. I keep her off the Minquiers to the southward and the lead going.
> journal note="07:17 the captain's bearing of Cezembre (S by E 5 leagues) moved the account 2 leagues NNE to 48 51 N 2 07 W: the Minquiers 2 miles on the larboard quarter. The flood set us NE 6 miles against a light air. Way re-laid: St Malo SSE 12 miles."
> stand_by until="a glass"
```

## t90

```
> submit_order text="trim the sails"
Aye, sir: trimming for the wind right aft, N by W, the lugs out either side as far as they will go and the topsails square; the course S by W allows the flood, which sets us to the north-east at a knot and a half till it turns.
> stand_by until="a glass"
```

## t91

```
> submit_order text="shape a course for St Malo"
> stand_by until="a glass"
```

## t92

```
> submit_order text="shape a course for St Malo"
The Saint-Malo pilots' boat is standing out to us, sir; the book takes him when he hails and gives him the conn when he is aboard. Cézembre, the Grand Bey and the town are all in sight SSE four leagues, Fréhel SW; the account is good to six cables.
> stand_by until="the pilot aboard"
```

## t93

```
> stand_by until="the pilot's hail"
```

## t94

```
My fault, sir: the book would not let me stand by for the pilot aboard while no sail was in sight, and I was slow to see the refusal. I stand by for his hail now; the course S by W holds, allowing the flood till it turns at a quarter past eleven.
> stand_by until="the pilot's hail"
```

## t95

```
> submit_order text="heave to" danger="fog down again, three leagues from the road with Les Jardins and the Conchee ahead; she waits hove to for the pilot or the fog to lift"
> submit_order text="heave the lead"
Fog again, sir, thick, and we are three leagues from the road with Les Jardins and the Conchée ahead. I have hove her to; the flood sets us gently to the north-east into open water, the lead is going, and the pilots' boat is still standing out to us, so he may yet find us by our bell. The moment it lifts, or he hails, we go on; the book takes him and gives him the conn without waiting on me.
> journal note="09:09 fog again, 3 leagues from the road; hove to on my own word, the flood setting NE into open water; the pilot boat standing out; standing orders take him at the hail."
> stand_by until="a change in the sky"
```

## t96

```
> submit_order text="clear away the best bower"
Aye, sir: Mr Bertin has the conn by the book, the lead goes every five minutes by your order, and I am clearing away the best bower so it can be let go on his word. He says the flood will not serve for the passages till about four this afternoon and high water is at seven, with thirty-seven feet of rise; and he cannot see his marks in this fog and is conning by the lead and the time run. If the fog holds, I would expect him to bring her up outside and wait for it to lift and the tide to make, and I shall not take the conn from him unless she stands into danger. I stand beside him.
> readings
> stand_by until="a glass"
```

## t97

```
> stand_by until="a glass"
```

## t98

```
> stand_by until="a glass"
```

## t99

```
Noon, sir, no sight in the fog; 48° 45' N, 2° 10' W by account, sixty-four miles made good since yesterday noon. Mr Bertin has her heading south at four knots in sixteen fathoms, fine sand, the lead every five minutes and the account moving a cable or two at each cast; La Fresnaye bay two leagues and a half SW by S. The wind has freshened from the NNE. I stand by him.
> stand_by until="a glass"
```

## t100

```
> stand_by until="a glass"
```

## t101

```
> submit_order text="let go the best bower" danger="eight fathoms and a half shoaling from thirteen in ten minutes, in fog, with the shore of La Fresnaye bay a mile or less under the lee by the chart and the ebb setting onto it; she anchors here and waits for the fog and the flood, as the pilot meant to in the bay"
Letting go, sir, on my own word: eight fathoms and a half and shoaling fast, from thirteen ten minutes since, the cast a mile inshore of the slate by the chart, the fog as thick as ever, the wind NE by N putting the bay under our lee and the ebb setting us into it. Mr Bertin meant to wait in La Fresnaye bay for the flood at four in any case; we wait here instead, a mile short of it, in good holding, coarse gravel, and go in when the fog lifts and the tide serves. You were right to take in the lugs; the topsails come in as she brings up.
> journal note="12:50 8.5 fm shoaling from 13 in ten minutes in fog, the cast a mile inshore of the account; La Fresnaye bay 1.5 miles under the lee, NE by N 11 kn, the ebb setting in. Let go the best bower on my own word rather than stand on under the pilot's conn; wait for the fog to lift and the flood at 16:00."
> stand_by until="brought up"
```

## t102

```
> submit_order text="furl the sails"
Brought up, sir, by the best bower in ten fathoms and a half, coarse gravel, fifty-four fathoms veered, riding to wind and tide together; and the port reckons us at anchor in La Fresnaye bay, the road of Saint-Malo, so we are where Mr Bertin was bound. The sails are coming in. We lie here till the fog lifts and the flood makes about four, then weigh and let him take her in through the passages on a rising tide, high water at seven. Your five-minute lead may be belayed at anchor if you would spare the hands; that order is yours.
> journal note="12:53 brought up in La Fresnaye bay, the road of St Malo by the port's reckoning: 10.5 fm coarse gravel, 54 fm out, riding to wind and tide. Sails furled. Wait for the fog to lift and the flood at 16:00; HW 19:00, 37 feet of rise."
> stand_by until="a change in the sky"
```

## t103

```
> stand_by until="a change in the sky"
```

## t104

```
> journal note="The Eclair's first cruise, 12 to 13 June 1805, Lecoq mate with the deck from 05:01 to 12:55 the next day. Roscoff road out by the eastern channel of Bas on the flood (six fathoms, the Isle Verte a cable to starboard); a brig out of Morlaix followed and gave us up; St Malo chosen, 77 miles, laid by pricked marks since the straight line crossed the Tregor coast. Mistakes mine: a 20-mile leg out of sight of land without a cast put us on the Heaux de Brehat, the flood having set us 4 miles; the way laid with a tidal allowance was not re-laid as the stream changed and would have closed Frehel, the captain seeing it first; the flood set us 6 miles NE onto the Minquiers' side in the forenoon against a light air. Right: the lead at every change, anchoring twice in fog rather than groping (22 fm off Frehel by night, 10.5 fm in La Fresnaye bay by day), the pilot taken and given the conn by the book, the anchor let go on my own word at 8.5 fm shoaling fast under a lee shore in fog. Findings for the game: the chart and the lookout disagree south of the Roches Douvres; the standing order's name cannot carry an apostrophe; 'every N minutes then <order>' is the form; a stand-by for the pilot aboard is refused with no sail in sight and the refusal leaves the turn open under lockstep; the ship's view does not show the yards' brace; the page's picture needs the tab in front. She lies at anchor in La Fresnaye bay, the road of St Malo, the pilot aboard, waiting for the fog to lift and the flood at four, high water at seven."
> stand_down note="Mr Lecoq, mate, standing down at 12:55 on the 13th with the captain's leave. The Eclair rides to the best bower in ten fathoms and a half, coarse gravel, fifty-four fathoms veered, in La Fresnaye bay, the road of St Malo, wind NE by N a moderate breeze, thick fog, the glass 30.28 and rising, all sail furled, the pilot Mr Bertin of St Malo aboard. The flood serves for the passages from about four this afternoon and high water is at seven with thirty-seven feet of rise; when the fog lifts, weigh, let the pilot take her in by his marks (the Great Gate or the Little Gate west of Cezembre), the lead going and the anchor ready. Watch the cable at the turn of the tide. No standing orders of mine stand but 'night lead' (a cast at each change of the watch) and 'pilot' and 'pilot conn', which have fired and may be struck. The purse is sixty pounds, the hold empty, water and provisions as at Roscoff. A good ship and a good captain; she wants only a lookout who can name what he sees."
```
