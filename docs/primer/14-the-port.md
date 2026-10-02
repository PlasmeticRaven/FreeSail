# 14. The port

Chapter 13 brought her to an anchor in the outer road and left her riding there. This chapter takes her in: the pilot who comes off in his cutter, the roads and the mooring, the boat sent ashore, the market and the yard, and getting under way again as Luce has it, with the tide. It also gives the ship her people by name and her papers by handle, because the port is where they are wanted. Two rules run through it. **Everything inward is reached by an order or a reading**: there is no menu of the port; you send the boat and read what it brings back. **Everything outward arrives through something the ship models**: a letter comes aboard in the boat or in the pilot's pocket, is carried aft by a person, and is read where the captain is, and each of those is a line in the log. Nothing arrives from nowhere.

The port is data. Falmouth, Plymouth, Brest, St Mary's and Roscoff are five files in `data/ports/`, each the same shape: the roads, the anchorage and the mooring as the chart's features; the pilot, his cruising ground and his words; the market with its goods; the yard or the chandlers; the hands to be had. Another port costs a file and nothing else (St Mary's and Roscoff, the last two, have sections of their own before the forms table). Which nations are at war is another file, `data/nations.yaml`, and the ship's nation is her company's names unless the scenario says otherwise: the frigate is British, the schooner American.

## The people aboard

The muster of chapter 6 gives the ship her hands by rating and station. The port needs a few of them by name: the captain, the lieutenants, the master, the standing officers, a midshipman or a boy to carry the word. These are the people, each one a sailor of the muster, so the counts are what they were and the names are the muster's. The master is chapter 10's master, one man with one place.

```orders frigate plain-sail
the people
where is the master
where is the carpenter
send for the carpenter
retire to the cabin
come on deck
# rejected: send for the chaplain
```

```
The people: Captain Bowen: on the quarterdeck. Mr Pearce, first lieutenant: on the
quarterdeck. ... Mr Harvey, master: on the quarterdeck. Mr Kemp, boatswain: on the deck.
... Mr Gardner, purser: in the gunroom. Mr Davies, sailmaker: in the sail room. ... Mr
Jarvis, midshipman: on the quarterdeck.
Where is the carpenter: Mr Chambers, on the deck.
Passed the word for Mr Chambers by Mr Jarvis; he is on the deck.
Mr Chambers came aft, sent for.
```

`send for` (or `pass the word for`, or `call the carpenter`) sends the messenger; the man comes to where the captain is a minute later, which is the time it takes to pass the word along a frigate's deck, and the log says he came. Send for him again while he is on his way and you are told he is sent for already; send for a man who is at a task (the master at his day's work, chapter 10) and you are told when he will be free. `go below` (or `retire to the cabin`, which is the form this book shows, since `go` alone is a console command) puts the captain in his cabin and leaves the deck to the officer of the watch; `come on deck` brings him up. A man sent for comes to the cabin when the captain is below. At night a watch-keeper in his watch below is asleep by the bill, and `where is` says so; sent for, he is up, and does not turn in again that watch.

A person is a name, a role, a skill, a place and a state, and no more. There is no sickness model yet beyond a flag, and no character.

## The places and the papers

A place is a name and a description: the quarterdeck, the deck, the cabin, the gunroom, the tops, the sail room, the hold, the boat, the shore. Nothing moves in a place and it has no layout; it is where a person is said to be and where a paper is kept. `the places` lists them.

The ship's papers are things with a keeper and a place, and they are served by handle through the library (chapter 11 and spec M4 §12: `library(topic='papers', section='manifest')`), to the captain, the watcher and the browser's pane alike, the same page. The handles are the sailmaker's account (in the sail room), the manifest (the hold's room and the cargo, with the purse), the purser's books (the water and the provisions), the boatswain's store book (the cordage), the booms' list (the spare spars), the establishment of ground tackle, the epitome's table of the establishments (in the cabin), and the price list, which is empty until the boat has been ashore. In a merchantman the mate keeps the purser's papers. A paper is only as current as its last entry: each is dated by the muster at the start and by the keeper's hand after, and the log says when a keeper writes one up ("The manifest written up by the purser: ten tons of tin bought at Falmouth").

Four of them are also readings at the prompt, for the figures without the page:

```orders frigate plain-sail
the places
the manifest
the purse
the stores
the epitome
```

```
The manifest: empty, room for 93 tons.
The purse: £200.
The stores: water 100 tons, provisions for 120 days.
```

The hold's room comes from the ship's file by the generator's rule (a tenth of the burthen in a ship of war, half in a trader: the frigate's 93 tons, the schooner's 112), as the boats do: the frigate carries a launch of thirty-one feet, a barge, a pinnace, two cutters and a jolly boat, the schooner a long-boat and a yawl. `the boats` lists them; `the boat` is the largest, the one that goes on errands.

## The pilot

Standing in for Falmouth under sail in daylight, within six miles of Carrick Road, you will have a sail reported on the bow: the pilot cutter, coming off. She is a vessel of the world (package 32b's cutter at far detail), moved once a minute, seen by the lookout at the distance his horizon and the weather allow, and made out as she closes: first "a sail", then "a cutter standing out from the land", then the Falmouth pilot's cutter. Within four cables she hails: "a pilot for Falmouth; shorten sail and he will come aboard." Within two cables, with your way under six knots, he boards:

```
Sail ho! A sail on the larboard bow, bearing N by W, distant six miles.
The cutter hailed: a pilot for Falmouth; shorten sail and he will come aboard.
The pilot, Mr Tregenza of Falmouth, came aboard from the cutter and took charge of her.
The pilot says: Keep the fair way and the lead going; there is a narrow deep channel of
sixteen or eighteen fathoms all the way into Carrick Road. The Black Rock lies nearly in
the middle of the entrance and shows itself at half tide; the eastern channel is the
better ...
The pilot's news: Britain at war with the Batavian Republic, France and Spain; the
United States, Portugal and Denmark at peace with all.
```

He is a person from then on, with a name from the port's list and his port's knowledge, and `the people` has him on the quarterdeck. He does not steer her: the helm and the sail are yours, as the Regulations of 1806 left them to the captain, and he answers what you ask. `ask the pilot about the channel`, `... for the marks`, `... about the anchorage`, `... when the tide serves` and `... for the news` each give the port file's words for it; the tide's answer is the world's high water at the port in the ship's clock, which is what a pilot knew and the captain's epitome did not. `the pilot` reads him and the tide at once:

```
The pilot: Mr Tregenza of Falmouth aboard; high water at Falmouth about four o'clock in
the afternoon, 16 feet above the datum; the flood is making now and serves.
```

```orders frigate plain-sail
the pilot
the port
a sail in sight
# rejected: ask the pilot about the channel
```

The first two are answered at sea with no pilot aboard ("no pilot aboard"; the nearest port and how far), the third is the lookout's, and the fourth is refused until there is a pilot to ask. No pilot comes off by night (the file says so, and it is judgement: no pilot's light at the Roads in 1805), to a ship at anchor, to a ship under bare poles, or to an enemy. What he does when he comes depends on the port's stance to her, which is the nations table's: **open** to her own nation, **hostile** to one at war with the port's (no cutter comes off, and a boat sent in would be taken), **neutral** otherwise ("American colours being no bar at Falmouth"), and **closed** when the scenario shuts the port to her nation by a decree or a quarantine, in which case the pilot hails his refusal from the cutter and bears up for the land. The news he brings is the table's wars, and the table can move by the news: a peace made or a war declared is a line of news from the pilot or the boat, never a line from nowhere, and the market reads it the next time a price is asked.

## The anchorage, the moor and the kedge

`the port` says where she is against the port: at sea, the nearest port and its roads bearing and distance; in port, which road she lies in, the port's stance, the pilot, the cutter and the boat.

```
The port: at anchor in Falmouth, the outer road; the port open to the English; the pilot
Mr Tregenza aboard; the pilot cutter standing out toward her; the boat at the booms.
```

The port has three places to lie: the **outer road**, where a ship from sea first brings up and where the pilot leaves her outward bound; the **anchorage**, where he takes her (Carrick Road, "the usual anchorage for ships of war"); and the **mooring**, the inner harbour where she lies with two anchors. Each is a feature of the chart with its depth and bottom, and the port file says how much a ship may draw to use the mooring: the frigate, drawing fifteen feet, moors in Carrick Road and not off the town. Coming to an anchor in any of them is chapter 13's evolution.

`moor` is Luce's: from single anchor she veers to twice her riding scope, lets go the second bower where she has dropped to, then heaves in on the first and veers on the second until she lies midway with a cable's length on each, the hawse open to the quarter the worst wind comes from. It takes a frigate a quarter of an hour, and `the anchor` says she is moored. `unmoor` heaves up the lee anchor and leaves her at single anchor, twenty minutes. A moored ship will not get under way: unmoor first, and the refusal says so.

```
Moor ship! Veer away on the best bower cable; clear away the small bower.
Veered to a hundred and twenty fathoms; stand clear of the small bower's cable!
The small bower let go in eleven fathoms, the second anchor of the moor.
Bring to on the best bower's cable and heave in; veer away on the small bower's.
Moored with the best bower to the WNW and the small bower to the NNE, sixty fathoms on
each; the hawse open to the SW.
```

`lay out a kedge to the NE` hoists out the boat with the kedge slung over her stern and a hawser coiled in her; she pulls out at four knots paying it out, lets the kedge go three-quarters of the hawser off on the bearing given, and comes back; the hawser is taken to the capstan. Twenty minutes, and the kedge is down on the ground tackle's list. Warping her up to it is not yet modelled: the kedge holds, as any anchor down does, and `weigh` takes it up again. The game keeps the two cables of a moor as two anchors down and does not yet foul the hawse.

```orders frigate plain-sail
# rejected: lay out a kedge to the moon
```

The words are checked before the hands are called: a bearing the ship does not know is refused at once. At sea, with no anchor down, `moor` and `lay out a kedge` are refused by the evolution itself when it is called ("no anchor is down to moor from; come to an anchor first"), which this book's parser-only test cannot show.

## The boat, the market and the yard

In port, at anchor within two miles of the roads, `send the boat ashore` hoists out the boat and sends it to the quay. It pulls at four knots, is a quarter of an hour at the quay to land a passenger or half an hour for the purser's business, and comes back with the prices, the letters waiting for the ship, and whoever went in it; a frigate's launch is an hour and a quarter about it from the outer road. `send the boat ashore with the mate` (or the purser, or any person) puts him in it, and `where is the mate` says he is in the boat, then ashore, then aboard again. A letter waiting at the port comes off in the boat, is carried aft by the messenger, and is read where the captain is: on the quarterdeck, or through the cabin door a minute later.

```
Away the long-boat's crew! Hoist out the long-boat.
The long-boat away for the quay at Falmouth with Mr Ray, for the prices and what news
there is.
The long-boat landed at the quay at Falmouth.
The long-boat shoved off from the quay.
The long-boat alongside from the shore and hoisted in.
Mr Ray came aboard from the boat.
The mate's list of the prices at Falmouth is aboard: tin £120, copper ore £9, pilchards
£17, salt £25 a ton, and the rest.
```

Until the boat has been ashore the prices are not known and `buy` is refused in those words. After it, `the prices` reads the list, and `buy ten tons of tin` or `sell five tons of tin` makes the bargain at the port's price now, moves the purse at once, and sends the boat for the goods, which go by the port's lighter while the boat is at the quay, three minutes a ton; the hold changes when the boat is back and the manifest is written up. The hold's room and the purse bound the bargain, and the refusals say which.

```
Bought 10 tons of tin at Falmouth at £120 a ton, £1200 paid; the boat goes for it. The
purse: £800.
10 tons of tin hoisted in and struck down into the hold; the manifest 10 tons of tin;
room for 102 tons.
The manifest written up by the mate: 10 tons of tin bought at Falmouth.
```

The prices are the port file's figures, which are **from memory** of the period's price currents and say so in the file (Cornish tin about £120 a ton in the war years, French brandy at a smuggler's price in England, English tin dear in a French port under the blockade), moved by three rules and no more:

| Rule | What moves the price | Figure |
|---|---|---|
| the season | the file's factor for the month (pilchards dear in spring, coal in winter, wine at Christmas) | the file's, 0.8 to 1.3 |
| the war | the good's nation at war with the port's nation, by the nations table | one and a half (`WAR_FACTOR`) |
| the supply | each ton sold to the port takes a hundredth off, each ton bought from it puts a hundredth on, between a half and double; the glut or the want clears by a seventh a day | `SUPPLY_PER_TON` 0.01, a week to clear |

So the five tons sold back at Falmouth above fetched £132, not £120: ten tons bought from the port had made tin a tenth scarcer. The figures are judgement and are named as such in `docs/dev/TuningNotes.md`; the shape is a captain's: a price list, a day's news, a glut you made yourself.

The yard is the other half of the quay. At Plymouth the King's yard supplies a frigate by demand, surveyed and vouched, for no money (the Regulations of 1806); at Falmouth there is no yard and the chandlers sell at a price; at Brest the arsenal sells to a neutral. `demand a topmast from the yard` brings a spare spar off in eight hours and puts it on the booms' list; `buy a suit of sails from the chandlers` is two days and the sail room; `demand cordage` the boatswain's store; `take in twenty tons of water` and `take in provisions for thirty days` the purser's books, by the ton and the day. `enter six able seamen` takes hands from the port's pool at its bounty, and they come off in the boat after the pool's delay (twelve hours at Falmouth, a day at Plymouth where the press takes most) and are mustered into the company by name.

```
Demanded a spare topmast by demand on the King's yard, surveyed and vouched at
Plymouth; it will be alongside in 8 hours.
A spare topmast came off and was got in on the booms.
The booms' list written up by the boatswain: a spare topmast came off and was got in on
the booms.
Entered 4 able seamen from Falmouth, come off in the boat: Nathl. Dawson, Lawrence
Tucker, Robt. Higgins, Jno. Brown; the company is 44.
```

```orders frigate plain-sail
the prices
the boat
the boats
# rejected: send the boat ashore
# rejected: buy twenty tons of tin
# rejected: enter six able seamen
```

At sea every one of the port's orders is refused in words: she is not in port, and the boat has nowhere to go.

## Getting under way, with the tide

Chapter 13's `weigh` is the anchor and nothing else: heave short, break out, cat and fish, and she lies with the anchor at the bows and no sail set, which is what the word meant. `get under way` is Luce's whole sequence (ch. XXI): all hands up anchor, the messenger passed and the bars shipped; heave short; the sail-loosers aloft and the topsails let fall, sheeted home and hoisted; the after yards braced for the tack she is to cast on and the head yards abox; heave round until the cable is up and down and the anchor is aweigh; the jib hoisted and the helm a-lee for the stern-board; and when she has paid off seven points, the head yards braced round and the spanker set, the anchor catted and fished as she gathers way. From the outer road a frigate is twenty-five minutes about it and comes out under topsails and jib at four knots.

```
All hands up anchor! Pass the messenger, ship the bars; send the ready-men aloft to get
the sails ready for loosing.
The messenger passed, the bars shipped and swiftered; heave round!
Pawl the capstan; stopper the cable. Stations for loosing sail! Lay aloft, sail-loosers!
Man the topsail sheets and halliards.
Let fall! Sheet home! Hoist away the topsails! Brace up the after yards for the
starboard tack, the head yards abox. Man the bars; heave round!
The cable is up and down. Man the jib halliards!
The best bower is aweigh.
Let go the downhauls, hoist away the jib! Helm a-lee for the stern-board.
The best bower up to the bows; avast heaving, pawl the capstan. Hook the cat.
She has paid off; right the helm, brace round the head yards, set the spanker.
Under way on the starboard tack, under topsails and the jib; the best bower catted and
fished; full and by (S by E (169°) lying too near the wind to be laid).
```

`get under way on the larboard tack and steer SW by S` says the cast and the course; said bare, with a pilot aboard, the cast and the course out are his (Falmouth's by the eastern channel, S by E; Plymouth's by the western, S by W), and the log says so. A course that lies closer to the wind than she will sail is not steered: she is kept full and by and the line says why, because a helm held to a course she cannot lie pinches her into irons with no way on. The tide serving is the pilot's word (`ask the pilot when the tide serves`): the ports take a ship in on the flood and let her out on the ebb, and the world's stream in the roads is a knot and a half at springs, which chapter 13 says she stems or does not.

Outward bound, once she is clear of the outer road and a mile beyond it and standing away, the cutter comes off again for the pilot; he leaves her within two cables, his pilotage is paid from the purse and his certificate signed, which is the Regulations' article, and the log has it:

```
The cutter hailed: she has come off for the pilot.
Mr Tregenza left her in the cutter, clear of the outer road; the pilotage, £5, paid and
his certificate signed.
```

```orders frigate plain-sail
# rejected: get under way on the moon
```

A tack or a course the ship does not know is refused in the words; at sea, with no anchor down, `get under way` is refused when it is called ("no anchor is down: she is under way already, or adrift").

## St Mary's, in Scilly

St Mary's is the first port of the Approaches and the natural start of a passage up Channel, and the port a King's ship puts into when the Atlantic has used her hard. It is a file like the others (`data/ports/st-marys.yaml`) on the Scilly patch the chart already carries. White's word for strangers is "not to attempt the harbours of Scilly without pilots", and the pilots are worth having: they come off "from one quarter or the other, even in the worst weather, as soon as the signal for that purpose is made". The isles' pilots came off in gigs, six oars and a lugsail; the file says so, and the game brings the pilot off in the pilot cutter until its pilot vessel is taken from the port's file, so the log calls her a cutter.

The way in from the Channel is St Mary's Sound, between St Mary's and St Agnes, "by far the best and safest channel" (Imray): the Great Minalto in one with the north-east side of the Great Mincarlo carries a ship between the Woolpack to starboard and the Spanish and Bartholomew ledges to larboard, and when the daymark on St Martin's opens west of Bants Carn she steers north by east for the anchorage. **St Mary's Road**, between St Mary's and Samson, is the one anchorage for a large ship, four and five fathoms on loose sand that does not hold well, sheltered from every wind but those between west-north-west and south-west; in those, White says, run to sea through Crow Sound at a proper time of tide. **The Pool** off Hugh Town is for small craft: a ship drawing more than nine feet lies in the Road, so the frigate, the schooner and the brig anchor there and only the cutter takes the Pool. The outer road is the mouth of the Sound, and the pilot leaves her a mile beyond it outward bound.

Standing in for the Sound from the south-east of Peninnis with the wind at east-south-east, the frigate has the pilot aboard in a quarter of an hour and is brought up in the Road in three-quarters:

```
Sail ho! A cutter standing out from the land on the starboard bow, bearing N by W,
distant two miles.
The cutter hailed: a pilot for St Mary's; shorten sail and he will come aboard.
The pilot, Mr Woodcock of St Mary's, came aboard from the cutter and took charge of her.
The pilot says: Strangers do not attempt the harbours of Scilly without a pilot. St Mary's
Sound, between St Mary's and St Agnes, is by far the best and safest way into the Road ...
Anchor in St Mary's Road with Hangman Island its own breadth open north of the Nut Rock, a
third of a mile south-east of it, in four and five fathoms ...
All hands, bring ship to anchor! Stand by to take in the light sails.
The best bower let go in six fathoms.
```

There is no yard at St Mary's in 1805 (Imray's spars and rope-walk are the 1870s'), so `demand a topmast from the yard` is refused there in words; the chandlers have water, fresh provisions and a little cordage. The market is the isles' produce, kelp, salt fish, pilchards, potatoes and barley, with what the islands bought in, and French brandy at the war's price as everywhere in England. The hands to be had are few: the young men of the isles pull in the gigs.

## Roscoff, behind the Isle of Bas

Roscoff is a small French harbour at the eastern end of the narrow channel between the Isle of Bas and the main. Faden (1793) says what it lived by: "a kind of free port for the exportation of rum brought from their colonies, which was there deposited, and sold to our smugglers"; the King's council had allowed the rum to be warehoused there for a year for export in 1769. The harbour dries at low water and is for vessels that take the ground; a ship lies in **the road of the Isle of Bas**, over against the great cove with its houses in the middle of the island, in three or four fathoms on sand. The chart there is Bellin's sheet of 1764, in brasses, georeferenced by the church of Roscoff and the island's marks (`data/charts/overrides/channel-west/roscoff.yaml`).

The western passage is the easier. Come to the end of the island within cannon-shot, where the Lavandière stands a third of the way to the main; keep it close aboard to starboard, for the Couillon lies under water twice a ship's length from it on the other hand. The eastern passage, by the town, is for high water and a pilot only: at low water there is no passing at all. The tide sets west a quarter south and east a quarter north through the channel, and the springs rise twenty-three feet, so the road that has three fathoms at low water has seven at high.

What Roscoff does when a ship stands in depends on her colours, which is the nations table's word. To a King's ship in June 1805 it is **hostile**: France and Britain are at war, no pilot comes off, and every order of the port is refused ("Roscoff is hostile to her; a boat sent in would be taken."). To a neutral it is open to trade and the town's pilot takes her in on the flood:

```
Sail ho! A sail right ahead, bearing E, distant three leagues.
The cutter hailed: a pilot for Roscoff; shorten sail and he will come aboard.
The pilot, Mr Cabioch of Roscoff, came aboard from the cutter and took charge of her
(American colours being no bar at Roscoff).
The pilot says: The western passage is the easier. Come to the end of the isle within
cannon-shot, where a single rock stands about a third of the way to the main: that is the
Lavandière ...
The best bower let go in five fathoms.
```

The market is the trade the port lived by, brandy, geneva, rum, tea and tobacco priced for the Cornish run, beside the wine, the salt and the canvas of the coast. Those prices are judgement and the file says so; no price current of Roscoff is in the references. The English smugglers who bought there came under false colours or by licence, and that run waits for the colours of a later milestone: an English ship that stands in for Roscoff today is met as an enemy.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `the people` | `who is aboard`, `the officers` | each person by name and role, with his place and state |
| `where is the master` | `where is the carpenter`, `where is the pilot` | one person's place and state; refused in words for a name not aboard |
| `send for the master` | `pass the word for the carpenter`, `call the surgeon` | the messenger goes; he comes to where the captain is a minute later |
| `go below` | `go to the cabin` | the captain to his cabin |
| `come on deck` | `come up` | the captain to the quarterdeck |
| `ask the pilot about the channel` | `ask the pilot for the marks`, `ask the pilot about the anchorage`, `ask the pilot when the tide serves`, `ask the pilot for the news` | the port file's words, and the world's high water at the port |
| `the places` | | the places aboard, each a name and a description |
| `the manifest` | `the cargo`, `the hold` | the cargo by tons and the room left |
| `the purse` | `the money` | the pounds in hand |
| `the stores` | | the water by the ton and the provisions by the day |
| `the epitome` | | the table of the establishments the captain carries |
| `the port` | | the nearest port, its roads, its stance, the pilot, the cutter and the boat |
| `the pilot` | `the pilot's words` | the pilot aboard and when the tide serves; "no pilot aboard" |
| `a sail in sight` | `the pilot cutter` | the other sail the lookout sees, nearest first |
| `the boat` | | the boat and its errand |
| `the boats` | | every boat she carries, by length, oars and crew |
| `the prices` | `the market`, `the price list` | the last list the boat brought off |
| `send the boat ashore` | `send the boat ashore with the purser`, `send the boat ashore with a letter`, `away the boat` | the boat to the quay and back with the prices, the letters and whoever went |
| `buy twenty tons of tin` | `sell twenty tons of tin` | the bargain at the port's price; the boat for the goods |
| `demand a topmast from the yard` | `buy a suit of sails from the chandlers`, `indent for cordage` | the yard's job, with its time and its cost |
| `take in water` | `take in twenty tons of water`, `water ship` | the water completed, or so many tons |
| `take in provisions` | `take in provisions for thirty days`, `victual the ship` | the provisions, by the day |
| `enter six able seamen` | `enter ten landsmen` | hands from the pool at a bounty, come off after the pool's delay |
| `get under way` | `get under way on the larboard tack and steer SW by S`, `weigh and make sail`, `up anchor and away` | Luce's whole sequence; the pilot's cast and course when he is aboard |
| `moor` | `moor ship`, `moor with the small bower` | a second anchor laid, a cable each way, the hawse open |
| `unmoor` | `get to single anchor` | the lee anchor hove up |
| `lay out a kedge` | `lay out a kedge to the NE`, `carry out the kedge` | the kedge carried out by the boat and let go on the bearing |
| `at the pilot aboard` | `at the pilot off`, `at the pilot refused`, `at the boat alongside`, `at a message`, `at a sail sighted`, `at moored`, `at got under way`, `at the hands entered` | the events, for the book |

## Where it comes from

The pilot is the Regulations of 1806, the Pilot's articles (borne as a supernumerary, the captain's certificate, the hand lead kept going in pilot water) and the Master's art. XXIX; the roads are White 1835 ('Coast of England', Falmouth pp. 26 to 27 and Plymouth pp. 31 to 35), Imray 1874 (pp. 78 to 90) and Moore 1799's catechism for Falmouth, Faden 1793 for Brest; St Mary's is White 1835 pp. 13 to 17 and Imray 1874 pp. 104 to 108, Roscoff Faden 1793 pp. 45 to 46, La Barre 1825, Norie 1839, Imray 1874 pp. 211 to 212, the King's council's arrêt of 3 September 1769 on the rum warehoused there, and Bellin's sheet of 1764 for its chart (package 35b; the tuning notes say what is judgement); the pilot's words in each file are those pages' directions. Getting under way is Luce 1866 ch. XXI, 'Remarks on Casting' and 'To get under way and stand out on a wind'; mooring and unmooring Luce ch. XXXIV and Lever 1808, 'Mooring' (the open hawse); the kedge Falconer 1780, KEDGE, and Lever p. 100; the boats Luce 1866, 'Boats', and Falconer, LONG-BOAT and YAWL; the yard's supply the Regulations' Captain's art. XVI and the standing officers' expense books. The nations table's dates are from memory and say so; the market's prices are from memory and say so; the rules that move them, the pilot's distances and the boat's times are judgement, named with their reasons in `docs/dev/TuningNotes.md`, package 35. The design is spec M5 §22 to §24 and `docs/design/InwardAndOutward.md`.
