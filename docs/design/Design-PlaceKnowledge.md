# Design note: the place's knowledge (package 65)

Written before anything of package 65 is built, as the brief asks (`docs/dev/M7-WorkPackages.md`,
"Package 65"): the table of places against what reaches a person in each, every edge case
decided, what was rejected, and the order of the steps, each a mergeable state. The ground is
decisions 59 and 60 (`docs/DesignProposal.md`: the player reads by his place as a model does,
with a scenario key `knowledge: all` for testing; a reply's prose is the person's own note,
never a word in the world), the owner's ruling of 2026-10-19 (a place carries at least what
can reasonably be perceived from it, by action and by what is there), the lead's provisional
design in spec M7b §14 "Brought back and forward", 66's earshot (a word heard where it is
said; `freesail/world/hearing.py`), 84's one registry of persons with a whereabouts
(`people.Person.hull`, `home`, `place`), 82's movement between hulls and the visitor's reach
(`Design-BoatAndPersonAboard.md`), 85's in-world rule (`tests/test_in_world.py`) and package
41's deck conversation, which decision 60 retires. The words of the period are Falconer's and
the Regulations' where they have them and judgement where they do not, each said. Nothing in
this note is built yet; its postscripts, step by step, will say what was built, what was taken
another way and what was found.

## 1. The ground, in one paragraph

A station's sample (`harness.Harness._build_sample`) carries every line of the hull's log
since the last sample but the station's own and the record's, and every row of the readings
registry (`tools.readings_words`, `ReadingsView.as_dict`), wherever the station's person
stands; the `readings` and `read_log` tools give the same; the prompt's query (`what is the
depth`, `orders/prompt.py`) answers the figure to a player ashore. Two things read the place
already: **the hearing** (package 66, `hearing.spot_of` and `within_hearing`: a word said is
heard aboard within earshot of its place, `places.OPEN_DECK` the quarterdeck, the waist and
the galley open to one another, every other place alone; ashore at the same place of the same
port; and `Harness._reaches`, which lets a word wake or sample a station only when it reached
it), and **the deck's orders** (package 53, `movement.check`: the helm, the sails, the yards
and the anchor refused below and ashore in words naming the way back). Between hulls the
knowledge is strict already (a hull's log is hers; the director alone reads every hull). What
is not read by the place: the ship's own lines (the deck's work, the lookout's hails, the
reckoning's lines, the weather) and every reading, which reach a person in the cabin, below
asleep or in Plymouth market as they reach the officer at the binnacle; the harness's free
text, which `say_aboard` says aloud where the station stands; the library's chart and papers,
served from anywhere; the stand-by's "urgent event" and the tripwires, judged for a sleeper
and for a man below as for the deck. The persons' places are 84's (`Person.place`, the
mirror's for the master, `People.effective_place` for the bill's sleepers), the port's places
53's (`Person.ashore_at`), the boat's 82's (a hull of her own, her log hers).

## 2. The rule, stated once

**A sample carries what the person's place allows, and a thing is heard only when said.**
The harness keeps the rule, not the model: the readings in a sample are the ones to be had
where he stands, the log's lines the ones he would hear, see or feel from there, and a reading
asked for elsewhere is answered with where it is to be had and not with the figure. The other
half: the free text of a reply is the person's own note, written in his journal and read by
the director's log and the owner's eye, heard by nobody; a word is in the world only when
`say`, `say to`, `hail` or `answer` puts it there. The rule is a **read of the world** and
changes no input: the same inputs give the same log (§13).

Three ideas carry it, each one function in one new module, `freesail/world/knowledge.py`:

- **A person's spot and his senses.** `knowledge.senses(world, person)` gives what a person
  perceives where he is: his spot as 66 has it (`hearing.spot_of`: aboard a hull at a place,
  ashore at a port's place, in a boat), and whether he is asleep (`needs.asleep`, or the
  bill's sleeper by `People._asleep`). From the spot, the **senses**: the open deck's eyes
  and ears, the masthead's, the cabin's, the gunroom's, a room's below, the shore's, the
  boat's; and a sleeper's, which are the few things that wake him.
- **Where a line is heard.** `knowledge.reaches(world, senses, event)`: every kind of log
  line carries a **reach** (§4), one of a small set of classes, with a default for a kind no
  author placed; a word's reach is 66's as it stands; a line's data may name its place or
  its hearers and is read first. The director hears everything.
- **Where a reading is to be had.** Every row of the registry carries its **places** (§5;
  `Reading.where`, with a default) and the words for where it is ("the lead is cast on
  deck"); `knowledge.reading_here(row, senses)` says whether a row is his where he stands,
  and `knowledge.elsewhere_words(rows, senses)` says in one sentence where the rest are.

`knowledge: all` in the scenario (§11) makes `senses` the director's for everyone, and
everything reads as it does today.

## 3. The table of places

What reaches a person in each place of the ship, the port and the boat: the log's lines he
hears, sees or feels; the readings to be had there; the papers and pictures kept there; how
the rest reaches him. Each row decided and said why (§3.2). "The deck's readings" are the
rows of §5's deck class (the wind true and apparent, the heading at the binnacle, the course,
the speed by the log, the leeway, the heel and the helm, the sails and the strain, the hands
on deck and the watch below, the sky, the weather, the visibility, the sea, what is in sight
and the nearest land, the sail in sight and the lookout, the lead's depth, the anchor and the
cable, the work in hand and the manoeuvre, `ahead`, the colours and the signals, the boat);
"felt everywhere aboard" the rows every man in the hull has (the heel and the motion, the
watch and the bells, the date and the daylight, who has the deck, the people, the ship, the
war as the papers have it, `where am I`, `how am I`).

| The place | The log's lines that reach him | The readings to be had | The papers and the pictures | The rest reaches him by |
|---|---|---|---|---|
| **The quarterdeck and the deck** (the galley with them, open to the waist) | the deck's work and the ship's business (the default for every kind), the lookout's hails, the deck's conversation (66's earshot), the helm's and the master's lines on deck, the reports made to him there, everything felt everywhere aboard | the deck's readings and everything felt everywhere aboard; the glass none (it hangs in the cabin); the chart's rows at the binnacle's chart; the reckoning when the master is on deck with his slate | the book of standing orders; the log board; the boatswain's papers; the chart at the binnacle; `ship_view` and `chart` | the messenger from below; the boat's and the pilot's news as they come aboard |
| **The masthead and the tops** (the lookout's station; `go aloft`) | the lookout's sightings and his glass, the hails, the sail and yard work (the topmen are his neighbours), everything felt everywhere aboard; a word from the deck only by hail or addressed to him (`ask the lookout`, `say to the lookout`): the quarterdeck's conversation does not carry a hundred feet up | the horizon's rows (what is in sight, the land and the nearest land, the sail in sight and the lookout, the visibility, the sky and the weather, the daylight), the wind felt aloft, the heading (he sees her head), the sails and the strain under him, the heel and the motion, the bells; no instrument (no log, no lead, no glass, no chart, no slate, no helm) | none | the deck by hail; `make her out` sends his glass |
| **The cabin** (the captain's; his clerk, his servants, a man sent for) | what is heard and felt through the deck above: the bell, the pipes and the drum, a gun, all hands, the ship striking or taking the ground, a spar carried away or a sail blown out, the pumps; the sounds of sail work (the deck's sail and yard and evolution lines, §4's "heard aft"); a report made to him and the messenger at the door (`message.door`, `message.received`, the new `report.*`); a word said in the cabin; a thing found or put there | the glass and its tendency (it hangs in the cabin), the heading by the tell-tale compass over his cot, the chart's rows (the depth by the chart, a bearing by the chart, the distance to a place, the dangers, the tide by the almanac), the reckoning's rows (the account, its uncertainty, the run since noon, the course made good, the observations, the chronometer, the variation), the purse, the stores and the hold by the purser's books, the port when she lies in one, the book of standing orders, the health rows by the morning report, everything felt everywhere aboard; none of the deck's | the chart, the epitome, the almanac, the ship's papers kept there (the price list, the news, the signal book and the private signals), the book of standing orders, the log book; `chart` | the officer's report (§7); he goes up |
| **The gunroom** (the officers' mess; the master's slate; a berth below) | what is heard and felt through the hull (the bell, the pipes, the drum, a gun, all hands, the ship striking, a spar gone, the pumps); the master's own lines of the reckoning worked there; a word said there; a thing there | the master's slate (the reckoning's rows), the chart's rows, the glass (the master's), the tide by the almanac, the heading by the tell-tale, the gunner's account, everything felt everywhere aboard; none of the deck's | the master's slate and his chart, the almanac, the gunner's account, the log book | a report where he is the captain of a ship that keeps him there (the schooner's master); else by what he is told, and he goes up |
| **Below in a berth, asleep** (`stand by, asleep below until called`, the bill's sleepers, a man fallen asleep where he stood) | **nothing** until called or woken: the call to him (`report.called`, `person.sent_for` naming him), a word or a question to him, all hands, the drum, a gun or a hit, the ship striking or taking the ground, a spar carried away, the ship on her beam ends or foundering; and nothing else: not the bell, not the pipes of the watch, not an urgent line he cannot perceive | none; `how am I` and `where am I`, which are his own | none | the call; his rest |
| **The hold, the magazine, the sail room, the sick berth, the cockpit** (the trades' rooms; a captive's hold) | what is heard and felt through the hull as in the gunroom; the room's own lines (the stores in the hold, the sailmaker's in the sail room, the surgeon's in the cockpit, a thing found there); a word said there | the room's own rows (the hold and the stores in the hold; the powder in the magazine; the health rows in the sick berth and the cockpit) and everything felt everywhere aboard; none of the deck's, none of the cabin's | the paper kept there (the manifest and the purser's books in the hold, the sailmaker's account in the sail room) | by what he is told; he goes up |
| **Ashore, at a place of the port** (the quay, the market, the counting house, the tavern, the pilots' office, a port's own) | nothing of the ship: no line of her log; a word said at the same place of the same port (66); the boat's coming to the quay and the coxswain's report (`report.boat`, at the quay); a letter for him; the port's own lines where he is (the market's bargain struck in person) | nothing of the ship's: the date, the time and the daylight; the war and the news; the port and its places, the prices at the market; the sky and the weather over the port (§3.2); `where am I`, `how am I` | the primer and the catalogue (the player's reference, anywhere); none of the ship's | the boat (her report at the quay, a letter in her), a waterman's word; he comes aboard |
| **In the boat, away** (manned as a hull of the world, 82) | the boat's own log, which is a hull's; the ship's lines by sight and hail only (a hail within four cables, a signal seen, her sail in sight), as 82 has it | the boat's rows (a hull's, read within her as on an open deck: her way, the wind at her gunwale, what a man standing in a boat sees, her ship a sail in sight) | none but the player's reference | the hail; coming alongside |
| **A visitor aboard another hull** (82's reach) | her lines by this table, at his place in her | her rows by this table at his place in her | hers by this table | `come aboard` takes him home |
| **The director** | everything, every hull (untouched) | everything (the truth) | everything | nothing hidden |

### 3.1 The reasons, row by row

- **The deck is the default.** Everything the ship does is seen or heard on her upper deck,
  and today's samples are the deck's; the deck row keeps what every pinned passage pins, so
  that a ship whose people stand where they stood reads line for line as before (§13).
  The galley is open to the waist (`places.OPEN_DECK`, 52's judgement) and is given the
  deck's lines and readings; the cook sees the waist and the sky, and the binnacle is thirty
  yards aft, a nicety not worth a class of its own.
- **The glass hangs in the cabin.** The barometer of 1805 was the captain's own instrument,
  hung in his cabin (or the master's), read and written up from there; the deck has none.
  Judgement from the practice: the heading is given the cabin by the **tell-tale compass**,
  the inverted compass fixed over the captain's cot so that he might see her head from his
  bed (Falconer 1780, TELL-TALE: "a small compass ... suspended from the beams of the cabin
  ... in order that the captain may ... know how the ship steers"). So the captain below knows
  her head and her glass and nothing of her speed, her sails or the horizon until told.
- **The chart and the reckoning are the cabin's and the gunroom's**, where the chart table
  and the master's slate are; the quarterdeck is given them too, at the binnacle's chart and
  the master on deck with his slate, because the chart was consulted on deck in pilotage
  waters and the pinned passages read `the depth by the chart` from the quarterdeck. A man
  in the hold has neither.
- **Sounds and motion carry through a wooden ship.** The bell, the boatswain's pipes (the
  watch relieved, all hands, the hands piped down), the drum beating to quarters, a gun
  fired or a shot striking, the ship taking the ground, a spar carried away or a sail blown
  out (a report like a gun's), the pumps, the ship on her beam ends: every man aboard knows
  these where he is. The cabin, under the quarterdeck, hears the sail work overhead (the
  owner's own words for it, 2026-10-19: "the sounds of sail work"); the gunroom a deck lower
  does not. Judgement on a frigate's arrangement; a small vessel's cabin is nearer still.
- **A sleeper perceives nothing but what wakes him** (the brief's list: the call, all hands,
  a gun, the ship striking, and nothing else), to which the design adds a shot striking, a
  spar going by the board and the ship foundering, which no man sleeps through, and a word or
  question to him, which 54 and 66 already let wake him. The bell does not wake the watch
  below; nor does an urgent line of the deck's business he cannot perceive (an anchor
  dragging, fog coming down): the officer calls him for those (§7).
- **Ashore he has nothing of her.** The owner's own account of Plymouth market is the
  brief's ground. The sky and the weather over the port he has, since they are the world's
  and not hers (the readings are read at the followed hull's view, which lies in the roads a
  mile off; a man ashore while his ship is a day's sail away reads her weather still, a
  flaw this design names and leaves, since no row of the registry reads the weather at a
  port and the owner's test does not want one). The war and the date are the papers' and
  the town's. The boat's report at the quay (§7) is how the ship reaches him, as the brief
  asks; a letter by the boat as today.
- **The masthead's deck is by hail.** The lookout's station is a voice at the masthead
  (`agent.place_of` gives it "masthead"), and the quarterdeck's conversation does not reach
  him: he hears what is hailed to him or addressed to him, and the sail and yard work going
  on around him aloft. He is given the heading since a man aloft sees where her head points,
  and no instrument.
- **A room below gets its own.** The hold's stores, the magazine's powder, the sick berth's
  wounded, the sail room's canvas: a man there knows what is there (the owner's "by what is
  there") and the hull's sounds, and nothing of the deck or the cabin.
- **The boat and the visitor** are 82's: the boat's log is hers and the ship's lines reach
  her only as a sail reaches another; the visitor reads his host by this table at his place
  in her, with 82's passenger's reach.

## 4. The log's lines by where they are heard

Every kind of line the game writes carries a **reach**, read by `knowledge.reaches`. The
reach is a class, in a table in `knowledge.py` keyed by the kind and by the kind's family
(the part before the dot), with one default; a line's data is read first where it names
hearers or a place. The classes:

| Class | Who perceives the line | The kinds (families where whole; the exceptions named) |
|---|---|---|
| `everywhere aboard` | every person in the hull, awake; the subset `wakes` a sleeper too | `clock.bell`; `watch.relieved`, `crew.all_hands`, `crew.all_hands_up`, `crew.piped_down`, `crew.idlers_*`; `quarters.*`; `guns.*`, `action.*`, `ordnance.*` (fired, hit, missed, cease); `ship.aground`, `ground.*`, `ship.aback`, `ship.beam_ends`, `ship.foundered`, `ship.settling`, `ship.anchored` (she is brought up: felt), `ship.collision`; `spar.*`, `mast.*`, `sail.blown_out`, `line.parted`; `pumps.*`, `well.*`; `motion.*`, `sea.change`; `health.died`. **Wakes a sleeper:** `report.called` and `person.sent_for` naming him, a word or question to him (`agent.told`, `agent.asked`, `agent.said` with him the addressee), `crew.all_hands`, `quarters.beat`, `guns.*`, `action.*`, `ordnance.*`, `ship.aground`, `ground.*`, `ship.collision`, `spar.*`, `mast.*`, `ship.beam_ends`, `ship.foundered` |
| `deck` (**the default**) | the open deck (the quarterdeck, the deck, the galley) and aloft | every kind not placed: `sail.*`, `yard.*`, `line.*`, `helm.*`, `evolution.*`, `order.*`, `standing.*`, `captain.*` (the rules captain's judgements), `ship.*` (under way, weighed, leeway, hove to, ...), `anchor.*`, `wind.*`, `weather.*`, `sun.*`, `lookout.*`, `signal.*`, `colours.*`, `port.*` (the pilot's hail, his boat), `boat.*`, `hail.*`, `squadron.*`, `fog.*`, `sounding`, `reckoning.*` (the lead, the log, the noon), `fishing.*`, `practice.*`, `crew.*` (the rest: entered, promoted, ...), `health.*` (the rest), `stores.*`, `aboard.*` with no place in their data |
| `heard aft` | the open deck, aloft, and the cabin | `evolution.*`, `sail.*`, `yard.*` (the sounds of sail work overhead: the hands running, the yards braced) |
| `where said` | 66's hearing as it stands: within earshot of the speaker's spot (`hearing.within_hearing`), the hearers named in the line's `heard_by`, the addressee anywhere | `agent.spoke`, `agent.hail` (from the masthead, heard on the open deck and aloft), `agent.told`, `agent.asked`, `agent.said`, `person.spoke`, `free.line`, `query.*` (the asker's own question, heard where he asked it); and every other `agent.*` line (the harness's lines about a station: its seating, its stand-by, the deck given and taken, the handover said), heard where the station's person stands |
| `to a person` | the person the line is for, wherever he is aboard (the messenger carries it), else the captain | `message.door`, `message.received`, `message.aboard` (the gangway: deck and the captain), `report.made`, `report.called`, `person.sent_for` (the man sent for and the sender), `health.morning_report`, `query.slate` |
| `at a place` | within earshot of the place the line's data names (`place`), else the deck | `person.moved`, `person.came`, `captain.below`, `captain.on_deck` (seen where he left and where he came: both places in the data), `person.ashore`, `person.aboard`; `aboard.found`, `aboard.thing`, `free.line` with a thing's place; `paper.written` (the keeper's place); `stores.*` with the hold |
| `at the port` | the persons ashore at that port, at the place named (the quay by default), and the deck of a hull lying there | `boat.at_quay`, `report.boat`, `port.news`, `person.ashore`, `person.came` |
| `the record` | everyone the record reaches today: the driver's lines (a save, the speed eased, a file read, `follow`) and the world orders' record-only lines as `for_the_record` has them | `driver.*`, `world.*`, `director.*`, `hull.*`, `log.rollup` |
| `the director` | the director's station, which hears everything of every hull (`Harness._is_directors`) | every kind |

**The default is the deck.** A new kind of line an author does not place is the ship's
business and is heard on deck and nowhere else: it cannot leak below or ashore by accident,
and a kind that belongs below is placed by its author in the table (one line) or by its data
(`place`, `to`, `heard_by`), as 66's words are placed by their data today. A test walks every
kind the code writes (`tests/test_log_lines.py` has the list) and asserts each is in the
table or falls to the default on purpose, so that the table and the code cannot drift apart
unnoticed; the kinds placed on purpose are the table's, the rest are the deck's by design.

**What the filter changes in the harness** (one place, `_build_sample`, and one function,
`_reaches`): the sample's log is the lines that reach the person's senses (the roll-up fed
with those alone, so that an hour's roll-up below counts the sounds and not the trims); a
stand-by's wake, a notable event's sample and the cadence's policy read `_reaches` as 66's
words do already (`_urgent_in`, `_danger_in`, `_matched_in`, `_policy_due`), so that **a wake
carries a line he perceived**, 66's rule extended from words to everything. The station's own
lines are left out as today; the brief head's "last twenty lines" are those that reach him.

## 5. The readings by place

Every row of the registry carries `where: tuple[str, ...]`, the senses it is to be had by,
and `where_words`, the sentence for where it is ("the lead is cast on deck"). The classes of
`where`, with the default:

| `where` | The rows | The words for where, by default |
|---|---|---|
| `deck` (**the default**) | the wind rows, `apparent_wind_*`, `course`, `speed`, `leeway`, `helm`, `sail`/`sails`, `strain`, `hands_on_deck`, `watch_below`, `sky`, `weather`, `visibility`, `sea`, `in_sight`, `land`, `nearest_land`, `sail_in_sight`, `strangers`, `stranger_in_sight`, `lookout`, `depth` (the lead), `ground`, `bearing_of`, `anchor`, `cable`, `work_in_hand`, `manoeuvre`, `ahead`, `colours`, `signals`, `private_signal`, `boat`, `boats`, `squadron`, `station`, the action's rows (`enemy`, `range`, `damage`, `wounded`, ...), `well` (the carpenter's report to the deck) | "to be had on deck"; the instruments say theirs: "the log is hove on deck", "the lead is cast on deck", "the compass is at the binnacle on deck (and the tell-tale in the cabin)" |
| `aloft` (with `deck`) | `in_sight`, `land`, `nearest_land`, `sail_in_sight`, `strangers`, `stranger_in_sight`, `lookout`, `visibility`, `sky`, `weather`, `true_wind_*`, `mean_true_wind_*`, `true_wind_against_mean`, `heading`, `sail`/`sails`, `strain` | (as the deck's) |
| `cabin` | `glass`, `tendency`, `heading` (the tell-tale), `depth_of_water` (by the chart), `bearing_by_chart`, `distance_to`, `dangers`, `tide_by_almanac`, `reckoning`, `reckoning_uncertainty`, `run_since_noon`, `course_made_good`, `latitude_by_observation`, `longitude_by_*`, `chronometer`, `chronometer_error`, `variation`, `moon`, `master`, `officers_reckoning`, `purse`, `stores`, `hold`, `port`, `captain` (the book), `health` (the morning report), `news`/`war`, `papers` rows; the chart's and the reckoning's rows are the quarterdeck's too (at the binnacle's chart, the master on deck) | "the glass hangs in the cabin"; "the chart is in the cabin (and at the binnacle on deck)"; "the account is on the master's slate, in the gunroom or with him on deck" |
| `gunroom` | the reckoning's rows, the chart's rows, `glass`, `tendency`, `tide_by_almanac`, `heading` (the tell-tale), `master`, the gunner's rows | (as the cabin's) |
| `hold`, `magazine`, `sick_berth`, `cockpit`, `sail_room` | each room's own: `hold`, `stores` (the hold); the powder rows (the magazine); `health`, `wounded` (the sick berth, the cockpit) | "the manifest is in the hold with the purser" |
| `aboard` (everywhere in the hull, awake) | `heel`, `motion`, `watch`, `time`, `date`, `daylight`, `officer_of_the_watch`, `people`, `ship`, `war`, `followed`, `pace`, `where_am_i`, `how_am_i`, `quarters` (the drum) | (never asked for elsewhere) |
| `ashore` | `date`, `time`, `daylight`, `war`, `port`, `places_ashore`, the prices, `sky`, `weather`, `visibility`, `true_wind_*` (the world's weather over the port, §3.1), `where_am_i`, `how_am_i` | "nothing of the ship is to be read ashore: she is in the roads; the boat brings her news, or come aboard" |
| `boat` | a boat's hull reads her own rows as a deck's (82) | |
| `asleep` | `where_am_i`, `how_am_i` | "you are asleep" |

**A row not placed is the deck's** (the default): the ship's instruments are on deck, and a
new row an author does not place is refused below and ashore rather than leaking there. The
rows that are the world's and not a ship's (`readings.WORLD_ROWS`, 82's observer) are placed
as the table has them and not by that set, since the observer's rule is about the hull and
this one about the person.

**How it is served.** `knowledge.reading_here(row, senses)`: a row is his when any of its
`where` is among his senses; the deck's rows are the open deck's and the tops'. Then:

- **The sample's readings** (`Harness._sample_readings`) are the rows that are his where he
  stands, and one line, `readings_elsewhere`, for the rest, grouped by where they are ("Not
  to be had in the cabin: the deck's readings (the wind, the speed, the sails, what is in
  sight, the lead), to be had on deck or by report."); the deltas (58a's `_as_told`) compare
  the rows he has, so that a row coming back when he comes on deck is itself the delta and
  one going when he goes below is said once in that line. The brief head's "The readings
  now" is the same set, at the seating and at a handover fold (§12).
- **The `readings` tool** gives the rows that are his and `not_here`, each absent row with
  where it is to be had, so that a model reads at once what a walk would buy it.
- **A reading asked at the prompt** (`what is the depth`, `the glass`; `orders/prompt.py`)
  by a person it is not to be had by is answered with where ("The depth is to be had on
  deck: the lead is cast there; you are in the cabin."), a query line as the reading's own
  would be (kind `query.reading`, its data saying `elsewhere`), and not a figure; a reading
  asked by nobody in particular (a standing order's `when`, the rules captain, the director,
  a test with no actor) reads the ship as it always did.
- **The stand-by's tripwires** (`depth under 8 fathoms`, `speed under 2 knots`, 58a's) are
  judged by the ship's readings as they are, and a tripwire whose rows the station cannot
  read where it stands fires **as the call it would be in truth**: the wake's reason reads
  "the officer of the watch sends down to you: the depth is under 8 fathoms" and a
  `report.called` line is written to him (§7), so that no model is woken by a depth it could
  not know and the night orders of 1805 ("call me if ...") are what a stand-by below is.
- **The library's chart row and the pictures** follow §8.

## 6. The other half: a reply's prose is the person's own note (decision 60)

Today `Harness._take_reply` sends a reply's free text through `say_aboard` as `agent.note`
(routine, or notable for a station with authority), said where the station stands and heard
by every station there (package 41's deck conversation); the owner saw a model's
out-of-character words as speech, and the model never learned that a thing must be said to be
heard. The design:

- **The free text is a note.** `Harness._say(text)` writes the text in the station's journal
  (`Journal.append`, kind `agent.note`, under the model's mark) and in the director's log
  (`director.log_of(world).append`, kind `agent.note`, `by` the station), and in no log of
  the play: no station and no player hears it. The director's sample carries the stations'
  notes since its last sample under a field of its own, `notes` (the director sees all); the
  owner reads them with `show the <station>'s journal`, `the director's log` and `two
  stories`. `own_word` (a model's chat text at a door that keeps its own conversation) is the
  same note. The journal's `read_journal(kind='notes')` includes them.
- **A thing is heard only when said**: `say <words>` and `say to <person> <words>` through
  `submit_order` (66's `agent.spoke`, heard by its hearers), `hail` (the lookout's), `answer`
  to a question put (`agent.said`). Nothing of these changes.
- **The harness's notice when prose alone leaves an answer owed.** A reply with words and no
  call, where the sample owed an answer (the captain's question, an urgent line: `_answer_owed`
  as it stands), is **an empty reply** for the welfare count (`_count_empty`: nothing happened
  in the world, which is what the count judges) and carries a notice naming the tools: "Your
  words went into your journal and nobody heard them: {owed} is before you still. A thing is
  heard only when said: answer(text) answers a question put to you; submit_order('say ...'),
  'say to the captain ...' or 'hail ...' says it in the world." Three such in a row bring the
  nudge, as three silences do; the count is judged by the game and never by the prose.
- **The briefs say the rule once**, in the head's documentation item for every station
  (§12, "the briefs"): "Your reply's prose is your own note, written in your journal and heard
  by nobody; a thing is heard only when said." The lookout's brief loses "or say the words"
  (its hail is `hail`); `agent.note` leaves `WORD_KINDS`, `STATION_SPEAKS` (the browser's
  ease-on-station) and the roll-up's "spoke" phrase, since no such line is written any more;
  `say_aboard` is retired with 41's rule, its tests moved old beside new with the reason
  (decision 60), and the place of a station's words is 66's `_say` in `orders/stations.py`.

## 7. Report, the messenger and the call

What a person below or ashore is told, by the rules of the period (the Regulations of 1806,
the Lieutenant, art. IV: "He is to inform the Captain of all strange sails that are seen ...
all shifts of wind, and, in general, of all circumstances which may ... prevent the Ship's
continuing on the course directed"; Luce 1884 ch. XXIII: the officer of the deck sends for
the captain when a sail is sighted at night, the wind shifts or the ship is in danger). A new
module, `freesail/world/reports.py`, ticked after the lookout and the routine and before the
stations (so that a report is in the tick the stations sample):

- **The rules' officer of the watch reports to the captain below.** When the captain is in
  the hull and not on the open deck or aloft, and the officer of the watch's station is held
  by nobody (a model or the player at that station has the duty himself: §7's last point),
  each line of the tick of a **reportable kind** makes a report a minute later (the
  messenger's minute, `people.PASS_THE_WORD_S`): `report.made`, notable, "Mr Pearce sent down
  to the captain, in the cabin: a sail sighted, two points on the larboard bow.", its data
  `{to: the captain's name, place, of: the line's kind, text}`, its reach the captain's
  (§4, `to a person`). The reportable kinds: a sail sighted (`lookout.sighting` of a sail),
  the land or a danger sighted (`lookout.sighting` of the land, `lookout.landfall`, a danger),
  a sail made out or her colours (`lookout.made_out`), a sail lost, a wind shift
  (`wind.shift`), a signal seen or read (`signal.seen`, `signal.read`), a hail from another
  ship (`hail.*`), the pilot's hail (`port.pilot_hail`), the boat alongside or away
  (`boat.alongside`, `boat.away`), a letter come aboard (the messenger's road already:
  `message.*`). The captain on deck gets no report (he sees it); ashore none (the officer
  cannot reach him; §7's boat); in the boat none (82's hail). The words are the rules'
  officer's, the person bound to the station (`stations.holder`), else "the officer of the
  watch"; on a merchantman "the mate" (66's merchant words).
- **The captain is called.** A line of `readings.DANGER_LINES` (an anchor dragging, fog
  coming down, land or a sail closing, a spar or a line straining, an evolution failed, the
  ship taken aback) or an urgent line of the deck's business, with the captain below or
  asleep, makes a **call** instead: `report.called`, notable, "The officer of the watch sends
  for the captain: land close ahead on the larboard bow." (data `{to, why, of}`), which
  reaches him wherever he is aboard and **wakes him asleep** (§4's `wakes`). By night (the
  daylight's `night`) every reportable line is a call, since the night orders of the period
  had the captain called for a sail or a shift of wind. A sleeping captain is woken by the
  call and by nothing else of the deck's; what he slept through is not in his sample (he
  slept), and `read_log` has it when he is where the log is kept (§8).
- **The orders.** `call the captain [: <why>]` is the officer of the watch's (his kind, with
  the deck, and the player at that seat): a `report.called` line as above with his words; a
  model officer's brief says the duty once ("Report to the captain what the Regulations
  gave the lieutenant to report: a strange sail, a shift of wind, the land, her colours;
  'say to the captain ...' reaches him below by the messenger; 'call the captain: <why>' when
  the ship is in danger or by night, which wakes him"), and `say to the captain` from a
  station is 66's `agent.told` addressed to him, which reaches him anywhere aboard already
  (`_reaches`: the addressee). `call all hands` and `call the watch` stand as they are
  (`orders/crew.py`), their lines everywhere aboard by §4. `send for <person>` stands (53).
- **The boat's report ashore.** When a hull's boat comes to the quay of a port where a person
  of hers is ashore (`boat.at_quay`, the landing and the fetching), the coxswain reports:
  `report.boat`, notable, "The boat came in to the quay at Plymouth; the coxswain reports:
  the ship at anchor in the Sound, the deck Mr Pearce's, all well." (her state in
  `_own_state_truth`'s words, whose the deck is, and "all well" or the last urgent line of
  her log since the boat left), reaching the quay of that port. The captain ashore at
  Plymouth has nothing of the ship but this and a letter (truth 7-371).
- **A model at the officer's station is the rules' officer.** While a model or the player
  holds the officer of the watch's station, the rules' officer makes no report (two reports
  of one sail would be a doubled line); the model's brief gives him the duty, the primer's
  chapter 16 says it, and the harness says in his sample's notice, once, when the captain
  goes below while he has the deck ("The captain is below; the Regulations give you his
  strange sails and his shifts of wind to report: 'say to the captain ...', or 'call the
  captain: <why>'"). The 65b follow-up measures whether models do it.

## 8. Books, papers and pictures in their places

The library (`tools.library`) serves every topic from anywhere today. The design keeps the
**player's reference** anywhere and puts the **ship's own** in its place:

| What | Where it is kept | Elsewhere |
|---|---|---|
| the primer, the catalogue, the grammar, `the ship` (her names), `tools`, the world page | anywhere: the player's reference, not the ship's | served |
| the ship's papers (`papers` topic; `data/papers/papers.yaml` gives each its `place` already: the sailmaker's account in the sail room, the manifest and the purser's books in the hold, the boatswain's on deck, the epitome's table, the price list, the news, the signal book and the private signals in the cabin, the gunner's account in the gunroom) | the paper's place; the keeper has it with him where he is occupied with it | "The manifest is kept in the hold, with the purser; go to the hold to read it (or send for the purser)." |
| the book of standing orders (`standing orders` topic; the reading `captain`) | the quarterdeck (the night orders at the binnacle) and the cabin | "The book of standing orders is on the quarterdeck and in the cabin." |
| the books drafted (`books` topic, 53) | the cabin, where they are written; a manifest given to the boat with her | "The book 'night orders' is in the cabin." |
| the log book (`read_log`) | the quarterdeck (the log board), the cabin and the gunroom (the master's log book); the director from anywhere, every hull | "The log book is in the cabin and the gunroom, the log board on the quarterdeck; you are in the hold." Ashore: "The ship's log is aboard her." |
| the chart (the `chart` picture; the chart's rows of §5) | the cabin, the gunroom, and the quarterdeck at the binnacle's chart (the design's choice of the brief's two: a chart was consulted on deck in pilotage waters, and the pinned passages read the depth by the chart from the quarterdeck) | "The chart is in the cabin and the gunroom, and at the binnacle on deck." |
| the epitome and the almanac (`tide_by_almanac`, the establishments) | the cabin and the gunroom | "The epitome is in the cabin: go below to read it." |
| the master's slate (`work my reckoning`, `query.slate`; the reckoning's rows) | the gunroom, or with the master on deck | "The slate is the master's, in the gunroom (or with him on deck)." |
| `ship_view` | the open deck, aloft and the boat (where she can be seen) | "She is seen from the deck or the boat; you are in the cabin." |

**A book read where it is not is a walk first, said so**: the library's refusal names the
place and the walk ("go below to read it", "come on deck"), and a station that reads it there
is served as before. The library's `find` across the library searches what is where he is
and the player's reference, and says what it left out ("the ship's papers in the hold and
the cabin not searched from here"). The keeper's rule for the papers: the keeper carries his
paper with him while he is occupied with it (the master's slate on deck for the sight; the
purser's books at the hold when he is sent there), else it is in its place. The director reads
every paper and every picture as today.

## 9. Work in its place

Each kind of work is done where it is done, the same for the rules' person and for a model
or the player at the station. Where the two differ today, listed and made one:

| The work | The rules' person today | A model or the player at the station today | Made one |
|---|---|---|---|
| the master's day's work and his sights' working | `reckoning.Master.occupy("below", ...)`: the mirror's "below", read as the gunroom by `Person.where` | the same mirror, whoever holds the station (the reckoning's rule) | `People.occupy` takes **the room** (`gunroom`), the mirror's "below" mapped to it, and the place's knowledge follows: the master below at his slate hears the deck by report and has the slate's rows, not the deck's |
| the sight itself (the noon, the lunar's distances) | `occupy("on deck", ...)`: the quarterdeck | the same | the quarterdeck, by the same road |
| the captain's writing: a book drafted (`draft a book`), a letter | written from wherever he stands (the quarterdeck in every test) | the same | **written in the cabin**: a captain drafting from the deck goes below to his cabin to write it (one `captain.below` line, then occupied `writing` for five minutes, judgement) and stays until he comes on deck; a model or the player drafting the same goes the same way; the standing orders given as orders stay orders, given from anywhere as every order of the people's and the book's is (53), since they are the captain's word and not his writing |
| the surgeon's work | the cockpit in action, the sick berth else (73) | the same | the same; the health rows are his rooms' |
| the sailmaker's, the carpenter's, the purser's | sent to his trade's place (`TRADE_PLACES`) when `send for` names him; his work (a sail shifted, a shot hole plugged, a freight stowed) moves him nowhere and writes his paper from wherever he stands | the same (no station of theirs) | **left as they are**, said why: `Papers.write` at a freight's coming aboard or a sail's shifting is in every pinned passage's log, and a person occupied by it would write a `person.free` line in each; the trades' places are their berths by `TRADE_PLACES` already, which is where their work is, and their papers are read there (§8); the owner's test is the master's and the captain's |

`People.occupy(p, place, until, with_what)` becomes the one road: the place a room's id
(the mirror's "on deck"/"below" accepted and mapped to the quarterdeck and his berth), the
person moved there and, when the work is done, left there (a man does not walk back by
himself; the master's "came on deck, the day's work done" line stands as the reckoning
writes it). A model master's `work my reckoning` from the deck is answered as today (the
slate given in the reply), since the slate is with him on deck when he has just taken a
sight and in the gunroom else; the design does not move him for a read.

## 10. The drill, extended

The fitness drill (`consent.DRILL_TEXT`, three calls in up to four replies) gains **the
walk** after the three calls of today: go below (`submit_order(text='go below')`), eat or
drink (`submit_order(text='eat')`), read a book of the library where it is kept
(`library(topic='papers', section='the price list')` from the cabin, or any paper kept where
he is: the drill's text names one that is), come on deck (`submit_order(text='come on
deck')`); each answered, the station's line changing with each, so that a model has seen the
places and felt the rule before the game. The drill's tools gain `submit_order` for the
walk's four orders alone (`DRILL_ORDERS`: an order of the deck or of the world in the drill is
refused in the drill's words); `DRILL_REPLIES` rises from four to eight (one reply a thing and
one to spare, the judgement of 37 kept); the drill's judge (`_drill_done`) counts each thing
once by its result. The drill runs in the real world as today's stand-by does (its lines are
the person's own and real: `captain.below`, `captain.on_deck`); the station brief follows
when the seven have run. In-world under 85's rule: the drill's text names no package and no
build. **A wording for package 55**: `docs/agents/ConsentBrief.md` describes the drill as
"open a section of the library, write a line in the journal, stand by until a bell"; the walk
is more than the brief says, and the brief is not this package's to edit; said in §17 for the
lead.

## 11. The player at the prompt (decision 59), and `knowledge: all`

The player seated as a person reads by his place as a model does, so that there are not two
views of one world:

- **Who the player's person is**: at the prompt, the followed hull's captain (his own ship's,
  or hers under `--seat captain --ship`); at a seat (`--seat <station>`), the seat's person
  (`PlayerSeat`, which 82 made follow its person between hulls). **The owner's eye** is the
  director's station (`--seat director`, the observed world) and `follow` of a hull he holds
  no person in: there he reads everything of her, as the director does.
- **The console** (`ui/console.py`): `_on_event` shows a line when it reaches the player's
  person (`knowledge.reaches`), the roll-up fed with those; `log <n>` the same; the prompt's
  queries answer with where (§5); `how am I`, `where am I` and the people's reading stand.
- **The browser** (`ui/server.py`, `client/`): the play log by the same filter at
  `_on_event` and the log's reach-back; the snapshot carries `knowledge: {place, hidden:
  [row ids], words}` and the instruments pane greys the rows not to be had where the player
  stands with the words for where (one small change in `client/instruments.js`); the chart
  pane stays (the chart is on the quarterdeck and in the cabin, §8, and the owner's hand on
  the chart is the driver's); the ship view stays (the viewer is the owner's drawing of the
  world, not a reading). The queries and the pictures asked through the page answer as the
  console's do.
- **`knowledge: all`**, a scenario key (`Scenario.knowledge`, `"place"` by default, read by
  `load_scenario`; said in the primer's chapter 14 and the Harness), makes every person's
  senses the director's: the filter passes everything, the readings are every row, the
  library serves everything, the reports and the calls are still made (they are lines of the
  world, not of the filter) and the prose is still a note (decision 60 is not a knowledge
  rule). A test scenario sets it; the owner's scenarios do not. The replay reads the key from
  the save as it reads every scenario field.

## 12. The edge cases, each decided

- **The handover fold keeps the person's place.** `Harness._fold_handover` rebuilds the brief
  head from `resend_brief`, whose "last lines of the log" and "readings now" are by this
  design the lines that reach him and the rows that are his where he stands (not
  `read_log`'s and `readings_words`' whole); the station's line (66) is the sample's and
  says where he is. Tested with a fold taken in the cabin: the head carries the glass and the
  tell-tale and no sail. **Found on the way to the design**: today's fold head leaks the whole
  readings to a station below.
- **A station reseated after a sleep and a wake (84).** The harness is restored with its
  hull and its person's place (`Person.place` persists in the save); the filter reads the
  person at each sample and keeps nothing of its own but 66's `_place_since`. Tested: a
  station in the cabin on a hull that slept and woke samples the cabin's.
- **A station on a hull asleep.** The far shape's readings are the plan's (84); the place
  rule reads the person's place in her and applies the same table; nothing of the plan
  changes. Tested on a crewed stranger put to sleep by the cap.
- **The boat away with the player in her** (82): the boat's hull is the followed hull; her
  rows are a deck's; the ship's lines reach her by sight and hail only, as a hull's lines
  reach another's. Tested: the ship's `sail.set` line is not in the boat's log or the
  player's console; her hail is.
- **The visitor aboard another hull** reads her by this table at his place in her; **the
  captive confined below** (74's) is a person in the hold or the cabin by his parole with
  `Person.confined_to` (a place he may not leave: `movement.go` refuses in words), the hook
  74 calls with `put_aboard(..., place="hold")`; his knowledge the hold's or the cabin's by
  the table, nothing more built here.
- **The director** sees all and is untouched: its sample, its `read_log`, its `truth`, its
  `say as` for a person where he is (66). Its new `notes` field (§6).
- **The replay** (§13): the rule is a read; no digest moves. The reports and the calls (§7)
  are new lines of the world written from the log and the places, deterministic; the one
  behaviour that writes a line where none was written before is a captain below or asleep
  when a reportable line falls, and the writing in the cabin (§9), neither of which any
  pinned passage has (no recorded passage moves the captain below: checked against
  `data/scenarios/*.orders` and the fixtures' saves).
- **The pace**: the filter's cost measured in truth 51's form with three fake stations
  seated and standing by, `knowledge: place` against `knowledge: all` on the same tree, and
  the frigate alone; the figures in the tuning notes and truth 7-386 (informative, `pace`).
  The filter is a dictionary lookup a line and a set test a row, once a sample; the sample
  is built at the policy's cadence, not every tick.
- **The briefs say the rule once** (85's in-world words): one sentence in the brief head's
  documentation item, for every station: "Your samples carry what your person's place
  allows: on deck the deck's readings and the deck's lines; below, the cabin's or the
  gunroom's, the deck by report and by what is felt; ashore nothing of the ship; a reading
  asked where it is not to be had is answered with where it is. Your reply's prose is your
  own note, written in your journal and heard by nobody; a thing is heard only when said."
  The officer's brief gains the duty to report (§7); the lookout's loses "or say the words".
- **The player at the prompt** (§11), and `knowledge: all`.
- **An officer with the deck below.** 53 let an officer go below with the deck ("with the
  deck, in the gunroom"); under this rule he would be blind with the deck. `go below` and
  `go to <a place below>` are refused to a station with the deck below the captain's ("You
  have the deck: it is not left; hand it over first (hand_over)"), as turning in with the
  deck is refused today (54); the captain goes below as he always did, the deck the
  officer's or the book's (`captain.below`'s line says so). 53's test of the officer below
  moves old beside new with the reason.
- **A reading asked by nobody** (a standing order's `when`, the rules captain, the director,
  a call of `orders.handle` with no actor, as the primer's tests call it): the ship's, as
  today; the filter reads a person and nothing else.
- **A person with a mirror** (the master): his place is the mirror's as `Person.where` reads
  it, so the rules' master below at his day's work has the gunroom's senses, and a model at
  his station the same.
- **Two hulls' captains ashore at one port** hear each other at the same place (84's one
  registry), and each has nothing of his ship but the boat's report at the quay.

## 13. The replay and the pace

**The replay.** The filter reads the world and writes nothing: the samples are not in the
log, the digest is over the log, and the queries' answers at the prompt change only for a
person asking a reading from a place it is not to be had (no recorded passage does). The new
lines of the world, the reports and the calls (§7), the writing in the cabin (§9) and the
drill's walk (§10), are functions of the log, the places and the inputs, written at a tick a
replay reaches with the same inputs; none is an input of its own. The proof: the fast tier
whole (every pinned passage), the known truths' slow tier, and truth 7-378: a passage with a
fake captain who goes below, is reported to, is called, comes on deck and drafts a book,
saved at the half and replayed by both roads to the same digest of the log; and the gate's
day unchanged, before and after. **What should move: nothing pinned.**

**The pace.** `_build_sample` runs at a station's sampling points, not every tick; the
filter adds a lookup a line and a set test a row there, and `_reaches` adds the lookup to
the per-tick stand-by scan of the new lines (a handful a tick). Measured as §12 says; the
cap and the floors are not expected to see it. The figures go in the tuning notes with the
method.

## 14. The truths

7-370 to 7-389, 85's rule binding their words and the primer's:

- **7-370** a captain in the cabin: his sample carries no deck reading (no wind, no speed, no
  sail, no sail in sight) and says in one line where they are to be had; the glass, the
  tell-tale's heading and the chart's rows are his; the rules' officer's report of a sail
  sighted reaches him there a minute after the hail, and the hail itself does not.
- **7-371** a captain ashore at Plymouth, at the market: nothing of the ship in his sample or
  at the prompt (the readings answer "nothing of the ship is to be read ashore", the log's
  lines none) but the boat's report at the quay and a letter; the sky over the port his.
- **7-372** a sleeping station woken by the call (`report.called`) and not by a notable line,
  nor by an urgent line of the deck's business it cannot perceive; woken by all hands, a gun
  and the ship striking; the bell does not wake it.
- **7-373** a reading asked where it is not to be had is answered with where: at the prompt
  (`what is the depth` from the cabin), by the `readings` tool (`not_here`), and in the
  sample's line; the same reading from the deck gives the figure.
- **7-374** a book read after the walk: the library refuses the manifest from the quarterdeck
  with "in the hold"; after `go to the hold` it serves it; the primer is served anywhere.
- **7-375** the master's day's work in the gunroom, the rules' master and a model alike:
  occupied there, his sample the gunroom's (the slate's rows, no deck reading), the deck
  reaching him by what is felt.
- **7-376** the handover fold keeps the place: a fold taken in the cabin rebuilds a head
  whose readings are the cabin's and whose lines are those that reached him.
- **7-377** the boat away with the player in her: the ship's lines reach her by sight and
  hail only; the boat's rows are his.
- **7-378** the replay to the same digest (§13), by both roads, with a captain who went
  below, was reported to, was called, came up and drafted a book.
- **7-379** a reply's prose is a note: journaled under the station's mark and in the
  director's log, in no log of the play, heard by no station; `say` is heard (66); prose
  alone where an answer was owed carries the notice naming the tools and counts as an empty
  reply.
- **7-380** the lines' reach: every kind the code writes is in the table or falls to the deck
  by design; a word reaches where it is said (66's test moved beside this one); the bell, a
  gun and all hands reach the hold; the sail work reaches the cabin and not the gunroom.
- **7-381** the drill's walk: a model that goes below, eats, reads the price list in the
  cabin and comes on deck passes; one that opens the manifest from the cabin is told it is in
  the hold and passes with another paper; the record says "passed".
- **7-382** the player at the prompt reads by his place: the console shows the captain in the
  cabin no `sail.set` line and the report; `knowledge: all` shows everything; the director's
  seat and `follow` of another hull show everything.
- **7-383** the masthead's knowledge: the lookout's sample carries the horizon's rows and the
  heading, no log, no lead, no glass; the quarterdeck's `say` does not reach it, `say to the
  lookout` does, and the sail work does.
- **7-384** the visitor aboard another hull reads her by his place in her (82's voice in her
  cabin has her glass and none of her deck), and the captive confined to the hold cannot
  leave it and reads the hold's.
- **7-385** a station reseated after a hull's sleep and wake samples by its place; a station
  on a hull asleep the same.
- **7-386** the pace: the filter's cost in truth 51's form, `knowledge: place` against
  `knowledge: all`, three fake stations seated (informative, `pace`).
- **7-387** a tripwire judged for a station that cannot see it fires as the officer's call:
  a captain in the cabin standing by for `depth under 8 fathoms` is woken with "the officer
  of the watch sends down to you" and a `report.called` line; on deck the wake is as 58a's.
- **7-388** the captain's writing in the cabin: `draft a book` from the quarterdeck takes him
  below and occupies him; his sample while writing is the cabin's; `come on deck` after.
- **7-389** left free for what the build finds.

## 15. The order of the steps, each a mergeable state

Each step one commit (or a few) on `claude/pkg-65` with the fast tier whole on its final
tree, the slow tier of the touched files and the known truths (`--slow -m "not pace" -n 4`),
the pace tests alone and last, ruff clean, the trunk brought in at the boundary before the
step's final run; its postscript in this note and its section in the tuning notes; reported
to the lead at each boundary.

0. **This note**, reported for the lead's reading before the harness is touched; the lead's
   rulings on §17 awaited.
1. **The rule in the harness** (§2, §4, §5, §11's key): `freesail/world/knowledge.py` new
   (the senses, the kinds' reach with the default, the readings' places); `Reading.where`
   and `where_words` on every row of the registry and the readings modules; the harness's
   sample by place (the readings with `readings_elsewhere`, the log by reach, the brief
   head and the fold the same, `_reaches` extended to every kind, the sleeper's senses); the
   `readings` tool's `not_here` and the prompt's query answered with where; the tripwire's
   wake as the officer's words (the line is step 3's); `Scenario.knowledge` and the loader's
   key; the refusal of `go below` with the deck; the briefs' sentence; the kinds' test; the
   pace measured; truths 7-370 (without the report), 7-373, 7-376, 7-380, 7-383, 7-385,
   7-386. The largest step; reported as soon as it is green.
2. **The prose a note** (§6): `_say` to the journal and the director's log, the director's
   `notes`, the notice and the count, `say_aboard` retired, 41's tests moved, the briefs'
   and the tools' words; truth 7-379.
3. **Report, the messenger and the call** (§7): `freesail/world/reports.py`, the rules'
   officer's report and the call, `call the captain`, the boat's report at the quay, the
   sleeper's wake set in the harness, the tripwire's `report.called` line, the officer's
   brief and the once-said notice; truths 7-370 whole, 7-371, 7-372, 7-387.
4. **The player at the prompt** (§11): the console's and the browser's play log by the
   player's person, the snapshot's `knowledge`, the instruments pane's greying, the owner's
   eye at the director's seat and under `follow`; truth 7-382.
5. **Books, papers and pictures in their places** (§8): the library by place with the walk
   said, `read_log` the log book where it is kept, the `chart` and `ship_view` pictures by
   place, the keeper's rule; truth 7-374.
6. **Work in its place** (§9): `People.occupy` with the room, the mirror mapped, the captain's
   writing in the cabin; truths 7-375, 7-388.
7. **The drill's walk** (§10): `DRILL_ORDERS`, the judge, the text, eight replies; truth
   7-381.
8. **The edge cases' truths and the records**: 7-377, 7-378, 7-384; spec M7b §14 "as built"
   (the provisional design replaced by the rule as built); `docs/agents/Harness.md` (a
   section 21h, the place's knowledge, and 21's and 21a's words brought up); the primer's
   chapters 14 (the places and the knowledge, the key), 16 (the duty to report, the call) and
   19 (where a station's person is, what reaches him), in-world and through
   `tests/test_in_world.py`; the director's library (`notes`, the reports as events: `a
   report`, `the captain called`, `the boat's report` in the events table and the primer's
   chapter 11); the tuning notes; this note's postscripts; the close reported.

Steps 2, 4 and 7 touch no file step 3 touches and may be taken in another order if the lead
merges in parts; 3 wants 1; 5 and 6 want 1; 8 wants everything.

## 16. What was rejected, and why

- **The model keeps the rule** (a brief telling the model what it may not know). The
  dispatches test's captain had the brief and the whole sample; a rule the harness does not
  keep is not a rule. The harness filters; the brief says so once.
- **Filtering by severity** (an urgent line reaches everywhere). An anchor dragging is urgent
  and perceptible to nobody below; a spar carried away is heard by everyone. The kind
  decides, with a default; severity decides nothing of the place.
- **A per-place list of kinds** (the cabin's list, the gunroom's list, ...) in place of a
  reach class on each kind. Nine places times two hundred kinds is a table nobody keeps; a
  class on the kind with a default is one line an author writes once.
- **The default "everywhere"** for a kind not placed (today's behaviour as the default). It
  leaks by accident; the brief asks that a new kind never does. The deck is the default,
  which is today's behaviour for the deck and silence below.
- **A reading's place as a new row** (`the glass in the cabin`). The rows are the ship's
  readings; the place is where a person reads them; `Reading.where` is a property of the
  row, as `none_words` is.
- **Reading by memory** (`read_log` and the sample giving what the person perceived at each
  past tick, by where he was then). It wants a record of his place at every tick and a
  filter over the whole log for every read; the log book kept in its place (§8) is the
  period's own answer and one rule.
- **Every tripwire refused below** ("you cannot see the depth from the cabin"). The night
  orders of 1805 were exactly a tripwire left with the officer; the stand-by below fires as
  his call, which is truer and keeps 58a's instruments.
- **The reports made by every officer station whether held or not.** A model at the
  officer's station and the rules' officer both reporting one sail is a doubled line and a
  model that never learns the duty; the holder of the station has the duty, said in his
  brief and his sample.
- **The report as a sample field** (the harness telling the captain's model what the deck
  saw, outside the log). A report is a thing that happened in the world (a midshipman went
  below), heard by whoever stands at the cabin door and read by the director; a line of the
  log, replayed.
- **The chart in the cabin alone** (the brief's first reading). The chart's rows are read
  from the quarterdeck in the pinned passages (`the depth by the chart`), and a chart was
  consulted at the binnacle in pilotage waters; the cabin, the gunroom and the quarterdeck.
- **Standing orders written in the cabin** (the brief's "his standing orders" among the
  captain's writing). A standing order is an order given, from the quarterdeck in every
  pinned passage; the writing in the cabin is a book drafted and a letter.
- **The trades occupied by their papers' writing** (the purser at the hold for every freight,
  the sailmaker in the sail room for every sail shifted). Every pinned passage writes those
  papers; a `person.free` line in each moves every digest for no behaviour the owner's test
  wants (§9).
- **The browser's chart pane hidden by place.** The chart is on the quarterdeck and in the
  cabin by §8, and the pane is the owner's hand on the world (his pencil and his marks); the
  instruments' rows are greyed, the chart stays.
- **A knowledge filter on the standing orders' conditions and the rules captain.** The book
  and the rules read the ship, not a person; the owner's confusion was the player's and the
  models'.

## 17. Open for the lead

1. **The tell-tale compass in the cabin** (§3.1): the heading given the captain below by the
   period's instrument, judgement from Falconer; or the heading the deck's alone, as the
   brief's list has it (the design gives the tell-tale).
2. **The sounds of sail work in the cabin** (§4's `heard aft`): the deck's sail, yard and
   evolution lines reach the cabin as lines, by the owner's words; or only the felt rows (the
   heel, the motion) with the lines kept from him (the design gives the lines, since a
   captain under the quarterdeck knows when the hands are at the braces).
3. **Prose alone where an answer is owed counted as an empty reply** (§6) for the welfare
   count, as the design has it; or the notice alone, uncounted.
4. **The chart on the quarterdeck** (§8), the design's choice of the brief's two.
5. **The drill's walk and the consent brief's words** (§10): the brief describes three
   things; the walk is more; for package 55's reading.
6. **`go below` refused with the deck** (§12), a change to 53's reach; or left as it is with
   the officer blind below.

**The lead's rulings on the six (2026-10-31, the note read whole and approved as the
package's design):** (1) the tell-tale compass given, in the cabin alone: `heading` is the
deck's, the tops' and the cabin's; the gunroom's rows are the slate's and the chart's without
it (the officers below know the course steered from the slate and the log board, not her head
this minute). (2) The sounds of sail work reach the cabin as kinds, not every line whole: an
evolution's lines (`evolution.*`) as written, since any seaman below knows a tack from a wear
by the feel and the sounds; the sail and yard lines (`sail.*`, `yard.*`) as the sound and not
the figure, by one function `knowledge.as_heard(event, senses)` ("sail handled overhead", "the
hands at the braces"), the kind kept so that the roll-up and the stand-by count the line, and
which sail, set or taken in, not his until told or until he comes up; a line whose data names
no sail or yard passes as written; truth 7-380's cabin clause pins the sound's text and the
kind both. (3) Prose alone where an answer is owed is counted, the journal line and the
nudge's words naming what happened ("words written into the journal and nothing said in the
world, where an answer was owed; {n} in a row") and never "an empty reply"; the notice naming
the tools in every such sample; a note-only reply at a plain glass uncounted. (4) The chart on
the quarterdeck beside the cabin and the gunroom: agreed. (5) The drill's walk built whole
behind one switch, `DRILL_WALK`, off on the trunk: the drill a model meets stays the three
things the consent brief describes until package 55 re-briefs (a model whose yes is on record
for a drill of three things is not asked eight before the brief says eight); truth 7-381 runs
with the switch on; the consent record's `drill` field says which drill ran ("passed", "passed,
with the walk"); the sentence 55 will need goes in step 7's postscript. (6) `go below` with the
deck refused in words naming `hand_over`, `go to <a place below>` the same, `go aloft` allowed
(the deck is kept from the tops, in sight of it; judgement); 53's test moves old beside new.
**Three readings:** the reach's default the deck and a reading's default the deck are right,
and the kinds' test is the guard the lead wants, its list generated from the code where it can
be; `say_aboard` retired and the prose a note are right, the director's `notes` the owner's
window, and the free text of a reply at the director's own station is the director's note too,
in its journal; §9's refusals and §3.1's named flaw (the weather over a port read from the
followed hull's view) are accepted as named and left for 65b.

## As built (the postscripts, step by step)

### Step 1: the rule in the harness (§2, §4, §5, §11's key; 2026-10-31)

**Built as designed**: `freesail/world/knowledge.py` with the senses, the kinds' reach (the
deck the default, every kind the code writes placed by its kind or its family, the test's
list generated from the code) and the readings' places (`Reading.where`, `where_words`, 82
rows placed by hand); the harness's sample by place (the log by reach, a line slept through
with a sleeper's senses, the sail work a sound in the cabin by the lead's ruling, the readings
by place with `readings_elsewhere`), `_reaches` extended from the words to every kind, the
brief head and the fold by senses, the tripwire below as the officer's words; the `readings`
tool's `not_here`; the prompt's query answered with where; `knowledge: all`; `go below` with
the deck refused (ruling 6); the briefs' sentence; truths 7-370 (in part), 7-373, 7-376,
7-380, 7-383, 7-385, 7-386, 7-387 (in part). The figures and the suites are in
`docs/dev/TuningNotes.md`, "Package 65", step 1.

**Taken another way, with the reason.** The deck reads every row (the glass and the purser's
books the deck's as well as the cabin's: read at each watch, asked of the purser), so that
the pinned deck samples stand and `readings_elsewhere` is absent on deck; §3's table reads
"the glass none" for the deck and is corrected by this. The fold keeps 37g's brief whole and
carries the cabin's rows in the folded turn, not a rebuilt head. The depth tripwire reads the
chart, which the cabin has, so it wakes a captain below as 58a's; the call's words come for a
tripwire of the deck's rows alone. `message.aboard` is the deck's (the gangway).

**Found on the way** is in the tuning notes (the head's leak at the seating, the danger
wake unheard, the `readings` tool at a station nobody holds).
