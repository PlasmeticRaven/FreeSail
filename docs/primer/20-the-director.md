# 20. The director

Every station before this one is a person aboard a ship: the officer of the watch, the captain, the master, the lookout, a passenger, a captain of another ship. This chapter gives the game a station that is on no ship at all: **the director**, who sits above the game, sees the world as it is, and shapes the voyage you sail through the world the ship is in. A language model may hold it through any door; you may hold it yourself at the console or in the browser; and whoever holds it, you read what it did and why only when you ask, so that a voyage becomes two stories: the one you lived and the one that was arranged. The end of the chapter says where it comes from.

## What the director is, and the one rule

The director's station is bound on the world and to nobody of the ship's company: it exists when a brief is given for it (a scenario's `director: {brief: ...}`, or `director: brief ...` at the prompt), or when you sit at it yourself (`--seat director`), and a world with neither is exactly as it was. It is not among the ship's stations: `the stations` does not list it, and no station aboard is told it is there.

**The one rule** is the proposal's: the director acts only through plausible causes. It cannot move your ship, change a sail or countermand an order; every order of the ship's is refused at its station, the deck's conversation included, since it has no place aboard to speak from. It changes the world the ship is in, and only in ways the simulation could have produced on its own: a sail that comes up over the horizon, a low that deepens where the season allows, a letter a port could have sent, a spar the carpenter finds sprung after a night of carrying sail. Every act of the director is something that could have happened anyway, so the physics stays honest and your agency stays whole.

```orders frigate plain-sail
the people
# rejected: weather: low "the low" radius 450 km at 1805-06-13T04:00 -300 500 990
# rejected: ship: a brig-sloop "Harpy" of France at the Iroise, running home to Brest
# rejected: aboard: the fore topmast is found sprung
```

The three refusals are the captain's grammar's, as chapter 15 had them: a world order is the scenario's, the director's and the owner's, never the captain's. At the director's station the same lines are the director's hand.

## The world orders: examples, not a rule

The director's tool is the world-order channel (chapter 15 and `docs/agents/Harness.md`, section 19), with what the director needed added. The forms the game performs today are:

- **the weather**: `weather: low "the low" radius 450 km fronts 140 300 at <time> <x_km> <y_km> <hPa>` appends a system, `weather: waypoint for "the low" at <time> <x_km> <y_km> <hPa>` moves one along its track;
- **a ship put on the sea, or a mind changed**: `ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth, intent: bound for Falmouth`, `ship "Nancy": intent run home to Falmouth`; words no intent's form reads (`ship "Raven": intent wait for the Amazon's boat and her captain's orders`) are her free intent, the goal told to a model seated as her captain, which her rules-based captain does not sail by: he lies her to where she is, and the order's line says so;
- **a thing found aboard** (from the table `data/director/aboard.yaml`, twenty-four things since the table was widened): `aboard: the fore topmast is found sprung` (the spar's condition cut to thirty, so that it carries away the sooner under a press of sail; the carpenter's report in your log), `aboard: the main topmast found rotten`, `aboard: the fore topsail found mildewed` or `chafed`, `aboard: the main brace found stranded`, `aboard: the best bower cable found chafed` (a spar's, a sail's, a rope's or a cable's condition cut, each by the ship's own name for it), `aboard: a cask found stove` (a ton of water) and `the leaguers found leaking` (a share of it), `aboard: the water found foul` or `brackish` (the purser's page says it, the needs read it, and watering makes it sweet again), `aboard: the bread found damp`, `a cask of beef found rotten`, `rats found in the bread room` (a share of the provisions), `aboard: the tin found wet` (a share of a good in the hold struck off the manifest with its cause), `aboard: the spare canvas found mildewed`, `rats found at the cordage` (the sail room and the boatswain's store), `aboard: the chronometer found stopped` (dead until the master winds it and sets it going by the account) and `aboard: the glass found broken` (no glass from then on), the hull's repair beside the carpenter's own work and the pumps (chapter 25), `aboard: the leak stopped` (or `her strained seams caulked`: a grounding's leak stopped, so the well gains no more; doubted when she makes no water) and `aboard: the well pumped out` (the well emptied; doubted when it is dry), and things reported with nothing modelled yet, which the answer says: `a seam found working`, `the compass found sticking`, `weevils found in the biscuit`, `the bilge found foul`. A thing whose effect wants what she lacks (no chronometer, no glass) is answered that the game has no way to do it as said;
- **a letter**: `message: at Brest from the agent: "..."` left at the port for the pilot to bring, `message: by a cutter from Plymouth from the port admiral: "..."` sent out to find her;
- **a port's stance or a price**: `port brest: closed to Britain`, `port falmouth: price of tin 130`;
- **a point of interest**: `mark: a wreck, her masts showing above the water at 49 58 N 5 16 W`;
- **a person named**: `person: supercargo "Mr Pentreath" aboard in the cabin`, `person: agent "Mr Fox" ashore at Brest`;
- **a person made from words, moved, or bound to a station**: `person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth, who knew the captain's father`, `person: "Mr Fox" comes aboard as master`, `person: "Mr Fox" goes ashore`, `person: "Mr Fox" leaves the ship at Brest`;
- **words in the mouth of a person nobody holds**: `say as the cook: "Pease and pork, sir."`, `say as Mr Fox: "I knew your father, sir."`;
- **a thing made or moved**: `aboard: a sealed packet, on the cabin table, from the Custom House`, `aboard: a cask of brandy, in the hold`, `aboard: the packet, in the keeping of Mr Veale`;
- **a sum, a freight or a debt, as a transaction with its cause**: `aboard: twenty guineas paid into the purse by Mr Veale`, `aboard: £6 paid from the purse to the pilot`, `aboard: ten tons of wool freighted by Mr Veale at the quay for Falmouth`, `aboard: a debt of £30 owed to the chandler at Plymouth`;
- **a model seated at a station of a ship, or as a person's voice**, under your grant and on your key: `seat: <the model's exact name> as captain of <ship> for 20 samples`, `... as officer of the watch for 20 samples` (your own ship), `... as Mr Veale for 20 samples`, `unseat: <the same words>` (the section on seats below).

**The new ship's words**: a description after its adjectives is read (`a French lugger`, `a small fishing lugger`, `a deep laden merchant brig`), a clause of her colours is her colours and never her goal (`British colours`, `colours shown`, `no colours`), an intent runs to the end of the order, commas and all, and a port in the `of` slot is her home and her nation its (`of Falmouth`); a refusal names the clause it could not read. A ship put on the sea in a port's harbour goes out by the port's track and not across the land. **A person is made aboard the player's ship or ashore**: `aboard the Two Brothers` or `on the quarterdeck of Cudlip's Boat` is refused in words and nothing is made, the people of another ship being no people of this world's; the player's own ship by her name is aboard, at the place said. **The truth** says the player's ship's own state (aground, at anchor riding or dragging, under way), a ship's intent where she sails by one, and `truth(within=20)` reads only the ships within so many miles of the player's and their people, the rest counted. **The director's own lines do not wake it**: what its world order writes in the log is passed over for its sampling, so a `say as` does not open its next turn.

These are given to the director **as examples of reasonable orders, never as the list of what is allowed**. Within each domain, and in domains the examples do not name at all, the director is told to attempt whatever it thinks reasonable: `news: war declared between Britain and Denmark`, `aboard: the cook reports the beef cask found rotten`, `say as the harbourmaster of Falmouth: "The packet is in."` (a stranger nobody has made yet). The game answers such an order honestly, never as "not allowed": *The game has no way to do this as said: ... Say it another way, or enter it again with a `[reason: ...]` and it will be logged as attempted.* Entered again with the reason, it is written in the director's log as an attempted act the game could not perform, with the words, so that the record says what is good, bad, useful or useless, and what the game should learn to do next. The tables (the things found aboard, the forms of the weather, the kinds of ship and intent) are what the game can do, not what the director may say.

**The forms, verified, and the dry run.** The library's grammar topic has a fourth part, **the world orders**: every form above with what it does and examples the game's own tests perform, the source of the station brief's examples and the starter briefs'. **`world_order(text, dry_run=true)`** says what an order would do, its doubt or its refusal, in the channel's own order (the budget, the rule of reach, the brief's limits, the form, the doubt), performing nothing, writing nothing in any log and costing no act; at the MCP door it is a read, and a stand-by goes on through it. The doubt it shows is not yet a doubt on the record: entered, the order is doubted there, and entered again with its `[reason: ...]` it is performed. **The truth's lookups**, each a small read in place of the whole truth: `truth(ports="Brest")` (the port's places and the people ashore there, its prices and its stance), `truth(grounds="all")` (the fishing grounds and their fish by gear and season), `truth(systems=true)` (every weather system with its centre, its pressure, its track or drift, and the field at the ship), `truth(at="49 55 N 4 35 W")` (a point or a place: at sea or on the land, its depth by the chart). And the library's page **the world** says how the world behaves: how the systems add and grow, how a ship put on the sea is crewed and her company drawn, what each order logs and to whom, and the doubt's figures, every figure the code's own. The truth's own entry for the player's ship carries `ahead`, what lies on her course within the next glass, by the truth.

**The weather appended grows in.** A system you append grows from nothing at the order's tick to its figure, over an hour at the least or until its first point's time; a waypoint appended to a track that had ended runs from where the system stands, reached an hour on at the soonest; the glass never steps. Systems add: a high appended beside the season's own makes a glass higher than either centre (the truth's `systems` lookup gives the field at the ship), and **a high is doubted as a low is**: above the season's ceiling, or a strong one put near her out of a glass that has not been rising.

## Doubted, not refused

The channel keeps the one rule with the director, and it does so by one rule: **a doubtful order is doubted, not refused.** An order the simulation could not have produced on its own from where it is gets the reason the act is doubted and the words, *if you think the action you requested is still reasonable, you may enter it again along with a `[reason: ...]`, and it will be logged and performed.* Entered again so, it is performed, and the director's log keeps the act, the doubt and the reason together, which is the data by which the sets of reasonable acts are refined. A reason is the answer to a doubt the director has read: given on the first entry, before the order was ever doubted, it is held to the doubt, which is shown, and the order entered again with its reason is performed. And the form comes before the doubt: an order the game cannot read as said is answered so in words, and never comes back "doubted" alone, so that a doubted order is one that will be performed. What the channel doubts, by channel:

| Order | Doubted when |
|---|---|
| `ship: ...` a new sail | she is put inside the lookout's horizon in clear daylight (she would have been seen coming up over it). A place on the land by the chart is no doubt but the form's refusal, the nearest water she floats in named, whatever the reason |
| `mark: ...` | the mark is inside the horizon in clear daylight (it would have been in sight already) |
| `weather: low ...` | the low is deeper than the season's floor for these waters (the climatology's table for the month and the box), or a deep low is put within three hundred kilometres out of a steady glass |
| `weather: waypoint ...` | the waypoint moves the system faster than the season's lows move, or deepens a low below the floor |
| `message: by a cutter from <port> ...` | the ship is beyond sixty miles of the port, which could not know where to find her |
| `port <id>: price of ...` | the price moves by more than three parts in ten in a word |
| `aboard: ...` | the thing has no cause in the ship's state (every condition the table names must hold): a spar sprung or a rope stranded with no strain on it and no fresh wind in the last watch; a cask stove, the casks leaking, a sail chafed, a cargo wet or a seam working on a smooth sea; the chronometer stopped or the glass broken in no more than a moderate sea; a cable chafed when she rides at no anchor; the water foul within five days of her last watering; a sail mildewed or the bread mouldy within the week, the spare canvas mildewed or the meat rotten within ten days |
| `aboard: the <thing>, <where>` (a thing moved) | no hand could carry it: from one port to another, or between the ship and a port more than six miles off |
| `aboard: <a sum> paid into the purse by ...`, `... paid from the purse to ...`, `... freighted by ...` | money or goods from nobody, or from a person the world does not know; a payer, payee or freighter neither aboard nor at a port she lies within six miles of; a sum beyond the port's means by the business's figures (a full lading of its dearest good); a freight to a ship at sea, with no lighter to bring it |
| `person: "<name>" comes aboard ...`, `goes ashore`, `leaves the ship at <port>` | no boat could carry him: she is more than six miles from his port, the nearest, or the one named |
| `ship "<name>": order ...` (the hand) | the order is implausible for her: an anchor let go deeper than thirty fathoms by the chart, plain sail in a wind over thirty-four knots, a chase by a merchantman, a fisherman or a packet |

A mind changed (`ship "X": intent ...`), a letter left at a port, a port closed or opened, a person named or made from words, a thing made, a debt entered, a word said as someone, and the seat under your grant are never doubted. Your own live order (`world: ...` at the prompt) is never doubted either: it is the owner's word.

## The director's voice: people made from words, and words in their mouths

The director may make the people its story needs and speak for those nobody holds.

**A person from words** stays in the world: `person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth, who knew the captain's father` gives him who he is, his age, where he is and a line of history, in any order after his name, and his outline says it in one sentence (*Mr Fox, Guernsey pilot, sixty years of age, who knew the captain's father.*). He is among the people from then on (`the people`, `where is Mr Fox`). `person: "Mr Fox" comes aboard as master` brings him aboard (a line of your log: *Mr Fox came aboard from Falmouth.*) and binds the master's station to him, so that a model seated at the master's is in his place and reads his outline; `goes ashore` and `leaves the ship at <port>` put him ashore, his station going back to the ship's own master or unbound. A move no boat could make is doubted, and done with a reason. You may give the same orders as the owner (`world: person: make ...`) to set a scenario's people; they are saved and replayed with the game.

**Words in a mouth**: `say as the cook: "Pease and pork, sir."` is a line of your log in his name where he is (*Mr Squire, the cook, in the galley: Pease and pork, sir.*), heard by the stations within earshot (the quarterdeck, the deck and the galley hear one another; below, each place alone) and written in his own journal, which a model bound to him later reads back; never the order. A man of the ship's company by his trade, the cook or the cooper, is found when he is first spoken for; a person ashore is heard only while she lies within a boat's reach of his port, and there only by whoever stands at the same place ashore (the counting house is not the market); a stranger is made first. The director may speak **by station or trade** as well: `say as the master`, `say as the boatswain`, `say as the officer of the watch` (whoever the station is bound to), and the ship's own voices, which are no persons: `say as the lookout: "Sail ho!"` is the lookout's hail from the masthead (*The lookout, from the masthead: Sail ho!*), heard on deck, and `say as the hands: "Huzzah!"` the hands on deck. A lookout's station held by a model or by you is refused as any held station. The result of each **says who heard it**, in the director's log: *Mr Veale spoke ashore at Falmouth, heard by the captain, ashore at Falmouth, at the counting house*; or, with nobody near, *heard by nobody: the captain is ashore at Falmouth, at the market*.

**The rule of reach**: the director speaks as anyone no model or player holds, and never as a held station, whose words are its holder's own; and so it moves nobody held and binds nobody to a held station. Your captain is yours while you are at the prompt, and the officer is the model's while one holds his station: `say as the captain: ...` is refused outright, in the director's log, the result naming the stations held (*the stations held now: the officer of the watch (Mr Pearce, a model); the captain (Captain Bowen, the player at the prompt)*). It is the one refusal beside your brief's limits.

**Questions to people nobody holds.** While a director is seated, `ask the cook what is for dinner` (yours, or a station's) is said where it is said and put to the director in its next sample, with until when it waits: it may answer in the cook's words with `say as`, which costs none of its day's acts, and the answer goes back to the station that asked, waking it; unanswered within a glass, the station is told so. A word (`tell the boatswain ...`) goes to it the same, and wants no answer. With no director seated, such a question is refused as it always was; the masthead and the master's reckoning answer by their rules whoever is above.

```orders frigate plain-sail
# rejected: say as the cook: "Pease and pork, sir."
# rejected: person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth
```

At your prompt both are world orders, refused as chapter 15 has them; at the director's seat, or after `world:`, they are the director's and the owner's.

## Things, and money paid, not said

The director makes things as he makes people. **A thing** has a name, a few words of what it is, and where it is, and nothing more: `aboard: a sealed packet, on the cabin table, from the Custom House` lays it on the table in the cabin; `aboard: a cask of brandy, in the hold`; `aboard: a letter, ashore at Plymouth, at the counting house`; `aboard: a sealed packet, in the keeping of Mr Veale` puts it in a person's keeping, where it goes with him. `aboard: the packet, <where>` moves the one known. The play log says nothing of the order: the thing is met where it is, in the people's words and the places' (chapter 14). A thing made is never doubted; a thing moved where no hand could carry it is. By the rule of reach the director puts nothing into the keeping of a person a model or you hold, and takes nothing out of it: *nothing is put into a held person's keeping but by his own act; leave it where he can take it ('on the cabin table') and say so*. So the packet for a model captain is left on his table, and the cook says so.

The people's own hands are the free lines (chapter 14: `give the packet to Mr Veale`, `take the packet`, `throw it overboard`), which move a thing the words name within reach and say *as said; nothing of the ship's changed* where they name nothing. They are the people's, never the director's, who has no hands aboard; he reads them in his sample as he reads the deck's conversation, and answers them in the story.

**His words move no money.** What a person he speaks as says he pays is words until the director gives the transaction: `aboard: twenty guineas paid into the purse by Mr Veale` is written in the purse's own ledger with its payer and the purse after, a notable line of the purser's books in your log (*Paid into the purse by Mr Veale, twenty guineas (£21); the purse £55.*), the act in the director's log. `aboard: £6 paid from the purse to the pilot` pays out, and is refused below nothing; `aboard: ten tons of wool freighted by Mr Veale at the quay for Falmouth` is the market's form at no price, the wool off by the port's lighter and the freight in the manifest with its cause, refused where the hold has no room; `aboard: a debt of £30 owed to the chandler at Plymouth` (or `owed by Mr Veale`) is entered in the purser's books and moves nothing. Each is doubted where it is implausible (the table above) and done with a reason; a held person's own money is his holder's word, refused by the rule of reach. There is no setting of the purse, or of any figure, at the director's station: a sum changes by a cause in the record, or not at all.

```orders frigate plain-sail
# rejected: aboard: twenty guineas paid into the purse by Mr Veale
# rejected: aboard: a sealed packet, on the cabin table
```

At your prompt they are world orders like any other, refused as chapter 15 has it; at the director's seat, or after `world:` as the owner, they are his forms.

## The director's hand: another ship's captain's order, as his own

The director may give another ship an order of her own grammar through her captain, as his own: the minute that matters, a heave-to, a chase, a course for the port, without seating anyone.

`ship "Harpy": order heave to` passes *heave to* to the Harpy's captain's station. In her own log it is his: *By the captain: heaving to.* The director's log keeps it as the director's act, with its doubt and its reason as every act; your play log never carries it, and what you meet is what your lookout sees (*The glass on the brig-sloop of war on the starboard bow: heaving to.*). Her captain is told the order came over his head, so that he does not fight it: he holds by it a glass, or until the director's next order to her, and then sails by his intent again (filling away, the course for his station shaped anew); `ship "Harpy": order carry on` gives her back to him sooner. **The hold may be named**: `ship "Harpy": order heave to for a watch`, `... for two glasses`, `... for an hour`, or `... until` one of her own events, `a sail within hail` (four cables), `a sail in sight`, `a landfall` (the land in sight from her), `hove to` or `at anchor`: she holds by it until the event comes to her, past the glass, or a day at most, and her captain then takes up his plan again (*The captain takes up his plan again*, in her story). An event she cannot be held until is refused in words naming those she can. The hold named crosses the promotion both ways as the glass does.

- **Crewed** (near you, at full detail), the order is her World's as any order of her captain's, under his own domain and nothing more: whatever her captain could not do, the director cannot do through him, and her grammar refuses it in her words.
- **At far detail** she carries only what the far shape carries: a course shaped or steered, heave to, fill away, give chase, haul off, make or shorten sail, come to an anchor, weigh, keep the station. A sail by name or a boat lowered is answered honestly, *the game has no way to do this as said*, naming what she can carry, and logged as attempted if entered again with a reason. Within the promotion's range the answer adds that the director may ask for her crewed first: `ship "Harpy": crewed` makes her a full ship now if the crewed cap has room (the cap and its order are yours and unchanged), and the order is then hers at full detail. A ship asleep keeps her own log, which the director reads with `read_log(ship='<her name>')`; a vessel with no captain of her own keeps a short story, which the truth shows.
- **Doubted** only where the order itself is implausible for her, since a captain's order is a plausible cause of itself: an anchor let go deeper than thirty fathoms by the chart, plain sail in a gale, a merchantman, a fisherman or a packet giving chase. Entered again with a `[reason: ...]`, it is done.
- **Refused where a model or you hold her captain** (the rule of reach): *Hazard's captain (Captain Reynolds) is held by a model: his orders are his holder's own, and nobody gives one through him; write to him instead*. Your own ship is never the hand's, whoever holds her.

```orders frigate plain-sail
# rejected: ship "Harpy": order heave to
```

At your prompt it is a world order like any other, refused as chapter 15 has it; at the director's seat, or after `world:` as the owner, it is the hand.

## The brief and its limits

You write the director's brief: the tone of the voyage, the challenge wanted, the limits set, the period's bounds the director must keep. It is a file beside the scenario or given at the prompt:

```yaml
# data/director/briefs/quiet-passage.yaml, the quietest starter
name: A quiet passage
tone: >
  A quiet passage in fair weather, with the texture of a real sea ...
challenge: >
  Interest, not danger. One notable thing a watch at most ...
limits:
  wind_max_kn: 27          # no gale: nothing above force 6 by any system appended or moved
  enemy_heaviest: cutter   # no enemy heavier than a cutter put on the sea
  nobody_dies: true
  the_war_as_it_is: true
  the_chart_as_it_is: true
cadence: glass
budget: {samples_a_day: 48, acts_a_day: 4}
```

Four starters are under `data/director/briefs/`: `quiet-passage`, `interesting-passage`, `hard-cruise` and `chase`. A scenario names one, a file or the mapping itself (`director: {brief: quiet-passage}`); at the prompt `director: brief quiet-passage` gives a starter, `director: brief a quiet passage with a chase on the second day` gives your own words (with no brief before them, no limits beyond the channel's doubt; over a brief, the tone changed and its limits, cadence and budget kept), `director: budget 60 samples, 10 acts` changes the day's budget and nothing else (a brief whose budget the day's counts are within lifts a hold the old budget made), and `director: brief` alone reads the brief as it stands. **The limits are the channel's to enforce, never the model's to remember**: a `weather:` order whose system would blow above the brief's knots at its tightest is refused with the reason, an enemy heavier than the brief allows is refused (ranked as the tops rank a sail: a frigate over a brig over a cutter, a schooner or a lugger), a thing found aboard that would kill is refused where nobody dies, a port closed to or opened to your own nation is refused where the war is as it is. These are the only refusals the director meets; everything else is doubted or attempted. The brief's words, limits and budget are the last part of the station brief the model reads, after the fixed part every director reads.

## The clock and the budget

The director samples on the notable and urgent lines and on a slow clock: every glass by the brief's default, every watch where the brief says `cadence: watch`, under the pace rule like every station (chapter 19), so your clock slows to 1x while its sample is open and runs at your compression when it stands by. A director that stands by for a watch lets you run at three hundred times. Every sample opens with **the director's line**: *You: the director, above the game; the day's budget 3 of 48 samples and 1 of 48 acts used; the clock waits on you and the captain*, the last naming every station whose sample holds the clock at 1x, and closing with the ship's time since its last reply (*...; 50 minutes of the ship's time since your last reply*), so that it knows what its thinking cost. While it stands by it may read **the truth and the chart** besides the log, the readings, the library and its journal, and the stand-by goes on; a world order or words of its own sent meanwhile end the stand-by at once, logged as ended at its own word, and are run in the turn they open. Its budget is the brief's, in **samples a day and acts a day** of the ship's time (an act is a world order performed; a doubt, a refusal and an attempt cost none): spent, either count holds the director until the next day of the ship's calendar, the log says so, and the sample that renews the day says the budget is renewed. The owner's compression is untouched.

## The log, hidden and revealed

Every act of the director goes to the **director's log** with its tick and its reason: an order given, one doubted, one entered again with its reason, one refused by the brief, one the game had no way to perform and one attempted all the same, the budget spent and renewed, the brief given, and every thought the director writes (its journal, and whatever it says in a reply, which is never a line of your log). It is the station's own journal, kept in the save with the stations' acts and replayed as a station's notes are, and it is **hidden in play from every station and from you**: nothing of the director reaches the play log, a station's sample, its `read_log`, its `state` or the `stations` reading (a director you can see coming is not a director); the play log carries only the effects of its acts as they are met (the sail sighted, the glass falling, the carpenter's report), as it carries the effects of your own `world:` orders.

You may ask for it at any time, by name:

```
the director's log
```

at the console or in the browser's order box. The log is printed (in the browser, in a pane of its own beside the play log, shut until you ask), the asking is written in the record as a driver's line, and **the director is told in its next sample that you asked**. `two stories [N]` prints the last lines of the play log with the director's log inline, each of its entries marked `D`: the replay view, which reads a saved voyage as two stories. `show the director's journal`, `ask the director` and `tell the director` are refused in words: the director is above the game, and the log is read by name; your word to it goes the way the next section says.

## A word apart from the game

You may speak to the director outside the game, whatever seat you hold or none:

```
director: keep it quiet tonight, if you would
```

at the console or in the browser's order box. Your words go to **the director's log only**, never the play log, and come to the director in its next sample as *The player, apart from the game: keep it quiet tonight, if you would*, waking it from a stand-by as a word does; nobody aboard heard them. The director answers you with `answer the player: <its words>` (its `world_order` tool, or a reply or an answer that opens with those words), which costs none of its day's acts: the answer comes back to you as a line of your own driver's, never the play log's (*The director, apart from the game: Aye, a quiet passage it is.* at the console; in the browser a small pane in the corner, shut until a line comes), and is kept in the director's log, so that `two stories` and the replay show both beside the play log and the play log says nothing of either. `director: brief ...`, `director: budget ...` and `director:` alone are the brief's, as before; every other `director:` line is a word. The director's brief keeps it honest: its plans and the truth stay in its journal, a question to you is phrased without world detail, and an answer tells you nothing your ship could not know. With no director seated your word is kept in the log for when one is, and you are told so.

## A model seated by the director, and what it costs

The director may seat a model at a station of a ship for a while, under **your grant**, the scenario's `director:` block: `models` (the names the director may seat, each with a consent record's yes), `seats` (how many at once), `seats_in_voyage`, and `seats_on_the_players_ship` (true unless you say false). The form:

```
seat: <the model's exact name> as captain of Harpy for 20 samples
seat: <the model's exact name> as officer of the watch for 2 hours
seat: <the model's exact name> as Mr Veale for 20 samples, within an hour
unseat: Harpy, the chase is over
```

A station of another ship (the captain, an officer of the watch, the master, the lookout or a passenger), or of **your own ship** with no `of <ship>`, never a station you or a model holds (the rule of reach); or **a person** by his name: one a station of your ship is bound to is seated at it, and one nobody holds, aboard or ashore, is seated as **his voice**, where he is (a passenger's station bound to him under his name: he speaks, asks and tells where he stands, keeps a journal and stands by, gives no order of any ship, and while the model holds him the director's `say as` for him is refused). A person aboard another ship has no world of hers to be seated in, and is refused. `within <a time>` lets the seat go if no door comes for it in that time; `unseat:` takes the same words.

**What it costs.** A seat runs a model on your key for its budget: each sample is a request carrying the conversation so far, paid for by you, for the samples or the hours the seat names, counted from the moment its door is admitted; when they are spent the game stands the station down with the reason, and the director's log says each step (held, admitted, stood down, ended, lapsed). The director is told so in its brief, and its budget line names the seats held and their spending. Where the game has a harbour (`py -m freesail`, or the browser's server) **the game starts the API door for a seat itself**, as the harbour starts one from its page: the model the seat names, which must be one your settings can call (the API door's model, or one of `doors.api.models`; a seat for another is refused in words to the director, with the API door's model named), its key from your credential store in the door's own process, never the game's; its pane appears in the harbour's doors tab beside your own, marked the director's seat's, and ends of itself when the seat is stood down. At the console the seat is a record, and its result says the door to start by hand. A seated API door's handover fold is counted from **two fifths of its model's context** (your settings' `doors.api.seat_budget_tokens` names another figure, in tokens or as a share), so that a long seat folds its conversation instead of resending all of it with every request.

## Holding the station yourself

`--seat director` at the console or the browser seats you at the director's station, above your own ship:

```
py -m freesail.ui.console --scenario data/scenarios/merchant-intent.yaml --seat director
```

A bare world order typed there is the director's, through the channel's door: doubted with its reason, entered again with a `[reason: ...]`, refused by the brief's limits if one is given, and written in the director's log under your name; `the truth` reads the world as the director sees it (every ship's true position, heading and sail, the weather as it is and as the systems will make it for the next watch, the tide, the people aboard every crewed ship, the markets and the news); an order of the ship's is refused. Your own `world:` order is still yours as the owner, undoubted and unlogged in the director's log. A model at the station reads the same truth through its `truth` tool and gives its orders with `world_order`; `docs/agents/Harness.md`, section 19, says how to seat one through each door.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `director: brief quiet-passage` | `director: brief <file>`, `director: brief <your words>`, `director: brief` | the director's brief given at the prompt (a starter, a file, or words: over a brief, its limits kept), the station bound; alone, the brief as it stands |
| `director: budget 60 samples, 10 acts` | `director: budget 9999 samples` | the day's budget in play, the rest of the brief kept; a hold lifted when the day's counts are within it |
| `director: keep it quiet tonight` | any words but `brief` and `budget`, at the console and the browser | your word to the director apart from the game: its log and its next sample, never the play log |
| `answer the player: <words>` | in `world_order`, or opening a reply or an answer, at the director's station | the director's answer to you, at your prompt or in the browser's pane, in its log, no act counted |
| `seat: <model> as officer of the watch for 20 samples` | `... as captain of Harpy ...`, `... as Mr Veale ...`, `... for 2 hours, within an hour` | a model seated by the director at a station of a ship (yours too, the grant allowing) or as a person's voice, under your grant and on your key; the harbour starts its API door |
| `unseat: officer of the watch, a note` | `unseat: Harpy`, `unseat: Mr Veale` | the seat given up, the station stood down with the note |
| `the director's log` | at the console and in the browser | the director's log revealed: every act with its reason; the director told you asked |
| `two stories 40` | `two stories` | the last lines of the play log with the director's log inline, each of its entries marked `D` |
| `--seat director` | at the console and the browser | you at the director's station; a bare world order there is the director's |
| `the truth` | at the director's seat | the world as it is: every ship, the weather now and in a watch, the tide, the people, the markets, the news |
| `--station director` | at the MCP bridge, the local runner and the API door | a model at the director's station, when the game has a brief for one |
| `chart(span)` | at a door that carries pictures | the player's chart as the browser draws it, his ship by her account and no other ship: for planning, not the truth; there is no `ship_view` above the game |
| `world_order(text)` | the station's tool | a world order through the brief's limits and the channel's doubt, logged in the director's log |
| `<order> [reason: ...]` | | an order doubted, entered again with its reason and performed; one the game cannot perform, logged as attempted |
| `aboard: the fore topmast is found sprung` | `aboard: the fore topsail found mildewed`, `aboard: the best bower cable found chafed`, `aboard: the bread found damp`, `aboard: the tin found wet`, `aboard: the chronometer found stopped`, `aboard: the glass found broken`, `aboard: a cask found stove`, `aboard: the water found foul` | a thing found aboard, from the table, the people's report in the play log |
| `person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth` | `..., aboard in the cabin`, `..., aged forty-five`, `..., who knew the captain's father` | a person made from words, with his outline, among the people from then on |
| `person: "Mr Fox" comes aboard as master` | `person: "Mr Fox" goes ashore`, `person: "Mr Fox" leaves the ship at Brest` | a person moved, a station bound to him or given back; doubted beyond a boat's reach |
| `say as the cook: "Pease and pork, sir."` | `say as Mr Fox: ...`, `say as the carpenter: ...` | words in the mouth of a person nobody holds, heard within earshot, in his journal; refused for a held station |
| `ship "Harpy": order heave to` | `... order give chase`, `... order shape a course for Falmouth`, `... order carry on` | the director's hand: an order of her own grammar given to her captain as his own, in her log as his; held a glass, then his intent again; at far detail what the far shape carries; refused where a model or you hold her captain |
| `ship "Harpy": crewed` | | a far ship within the promotion's range made a full ship now, the cap allowing |
| `aboard: a sealed packet, on the cabin table` | `aboard: a cask of brandy, in the hold`, `aboard: a letter, in the keeping of Mr Veale`, `aboard: the packet, ashore at Plymouth, at the counting house` | a thing made with a name and where it is, or one known moved; met where it lies; nothing into or out of a held person's keeping |
| `aboard: twenty guineas paid into the purse by Mr Veale` | `aboard: £6 paid from the purse to the pilot`, `aboard: a debt of £30 owed to the chandler at Plymouth` | a sum paid in or out, or a debt, with its cause in the purse's ledger; doubted from nobody or from afar, refused below nothing |
| `aboard: ten tons of wool freighted by Mr Veale at the quay for Falmouth` | | a freight at no price, off by the lighter, in the manifest with its cause; refused where the hold has no room |
| `ask the cook what is for dinner` | `tell the boatswain <words>`, with a director seated | a question to a person nobody holds, put to the director; its answer as him back to the asker, or after a glass the asker told none came |
| `director: {brief: quiet-passage}` | in a scenario file, beside `models`, `seats`, `seats_in_voyage`, `seats_on_the_players_ship` | the brief given by the scenario, the station bound when the game is made |

## Where it comes from

The director's principles: an agent on a different channel, acting only through plausible causes, its actions visible after the fact, sampling on events and a slow clock, with a brief as the guardrail; stations as data bound at run time, so that a station on no ship is a binding like any; a world order never shown as sent; a world order doubted, not refused, and the brief's hard limits the only refusals; the forms and the tables examples and not a rule. The sources of the things found aboard are in the table itself (Falconer 1780, SPRUNG; the Regulations and Instructions of 1806, the Purser).
