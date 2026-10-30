# Design note: the boat as a hull of the one world, and the person aboard another ship (package 82)

Written before anything of package 82 is built, as the re-brief asks (`docs/dev/M7-WorkPackages.md`,
"Package 82" and "The re-brief after 84 and 85", approved by the owner on 2026-10-30): the
seat's decision for a person who changes hulls, the cost of a world with no followed hull as
measured, the boat's figures with their rungs and sources, the oar force's source, and the
order of the steps. The ground is package 84's one world as merged (`Design-OneWorld.md`, "As
built, steps 1 to 11"): one `World` of hulls, the player's ship a hull among them and a vessel
of the sea, one clock, one registry of persons and things, one journal with the hull on each
input and act, the ports the world's and the dealings each hull's, a hull awake under the
physics or asleep whole, the drivers following a hull. The sources named below are the ones on
file (`docs/references/README.md`) unless marked judgement; the ships session's principles for
a hull's file and her drawing (`Build-Ships.md` §5.0 to §5.3 and §5.6 on `claude/pkg-75`) bind
the boat's file and are read here as the brief's item 4 asks. Nothing in this note is built
yet; its postscripts, step by step, will say what was built, what was taken another way and
what was found.

## 1. The ground, in one paragraph

A hull (`world/hulls.py`) is what a World keeps of one ship, read and written under the
World's names through `world.own`, the hull current for the block; the followed hull
(`world.followed`) is the default, the player's own (`World.players`, `hulls[PLAYER_ID]`)
until `follow "X"` names another. A person (`people.Person`) has a whereabouts of his own:
`hull`, the id of the hull he is in (None ashore or in a boat), and `home`, the hull that
keeps him; `aboard` is a bool over `hull`, kept on the wire of every pinned line. A station is
a binding on one hull's `Stations` and a `Harness` in that hull's `agents`, the harness
holding the hull as its `world`; every act of a station on a hull other than the followed one
carries `ship: <her id>` and a replay gives it to her by either road (`acts.target_of`); the
save's `hulls` block holds each hull's stations. The boat today is a `BoatState` of a hull's
`Dealings` and a script (`SendBoatScript`, `LayOutKedgeScript`) that holds the boat and not
the ship, or, on a sleeping hull, two jobs of the port at the boat's pace. The physics
(`physics/integrate.py`) take a hull's thrust from her sails alone, with the cable's pull at
the hawse and the trawl's drag the two outside forces the integrator knows.

## 2. The seat's decision: a person who changes hulls (item 3)

**The question.** A station is a person aboard: when he goes into the boat, aboard another
ship or into a captor's hands, either he keeps his station and the hull under it changes, or
the station ends and a new one begins on the other hull with the same holder. The replay (his
acts keyed by hull), the consent's record and the harness's samples (which follow his hull,
as the brief asks) must all hold.

**The decision: the person is the world's, the station is a hull's, and the harness is the
person's.** A station's authority is the hull's it is bound on (the Raven's captain's station
commands the Raven and nothing else, and the consent brief describes it so: "a captain, who
commands a ship"); a person's conversation with the game is one conversation wherever he
goes (the harness keeps its turns, its journal and its budget, as a station keeps across the
sleep and the wake with no reseat). So when a stationed person moves into another hull:

1. **His harness goes with him and holds the hull he is in as its `world`** (`Harness.world`
   re-pointed; taken out of the hull's `agents` he leaves and entered in the hull's he comes
   into). Its samples are that hull's readings, log and people from the next tick; its acts
   carry that hull's id; the pace rule finds it where it is (`all_agents` walks every hull's
   `agents`).
2. **The station he holds on the hull he comes into is one of hers**, bound quietly to him
   for as long as he is in her, of the kind his standing in her gives him:
   - in **his own ship's boat** (manned and away, a hull of the world; §5), he is her
     commander: the senior officer in a boat has her (Luce 1866, 'Boats': the officer in the
     stern sheets gives the orders, the coxswain steers), so his station in her is her
     `captain`'s, every order of the boat's his (the sweeps, the lug, the helm by the
     coxswain, the hail);
   - **aboard another ship** (by the boat alongside her, by boarding, by capture) he is a
     person aboard her with no duty in her: his station in her is **his voice**, a station
     of the passenger's kind under his own name (package 67's `VOICE_KIND`, as a seat at a
     person aboard another hull binds it today), so that he reads her deck as a passenger
     reads it, speaks and is spoken to by spot, goes about her places, gives and takes and
     reads, and gives none of her deck's orders; an order of his own ship's deck is refused in
     words from there ("You are aboard the Amazon; the Raven's deck is not yours from here:
     hail her, make a signal or send a letter"), as a captain ashore is refused today
     (`movement.check`).
3. **His station on the hull he left stands bound to him** (the binding is the hull's and
   names him; `holder` is he), so that the Raven still has a captain's station and knows
   whose it is, but it has no harness while he is away: the deck is nobody's or the book's
   (`deck_words_for` says so of a captain not aboard already), her rules captain sails her by
   his intent as he does for a captain gone ashore today, and a door asking for that station
   is told he is away from her. **When he comes back aboard** his harness is his station's
   again, the same object, the visiting binding unbound.
4. **The capture hook for package 74**: `movement.put_aboard(world, person, hull, place,
   seat="follows" | "stands down", why="")`, one function for every change of a person's
   hull, which 74 calls for the captive put aboard the captor; with `seat="stands down"` the
   harness is stood down with the reason as a handover stands a station down (the game
   saved, the journal kept, the station released), which is "the handover's rule" the brief
   names; the default follows him. The boat's landing and fetching, the boat alongside
   another hull, the boarders' party and `person: "X" comes aboard the <ship>` all go through
   it.

**Why not the other way (the station ends and a new one begins).** A new station is a new
harness, a new conversation and a new `seated` act: the model would be re-briefed in the boat
and again on the quay, its journal split in three, and the replay would have to seat a station
whose `seated` entry the play never wrote by a door; and a captain's station of the Raven
could not "begin" on the Amazon, which has a captain. The one rule above keeps one
conversation and gives him on each hull exactly the authority a person of his standing has
in her.

**The replay holds.** Every move between hulls is a consequence of an input or of a job: an
order (`go to the boat`, `go ashore`, `come aboard`, `send the boat to the Amazon with Mr
Pope`), a world order (`person: "X" comes aboard the <ship>`), a job of the port due at its
tick, or a fight's end; none is an input of its own, so a replay makes the same move at the
same tick by giving the same inputs, and the harness is on the same hull when the act after
the move comes. The acts carry the hull they were made on (`acts._entry` reads
`hull_id_of(world)` of the harness's world at the act). **One change for the transcript
road**: the save's blocks group a hull's stations by the hull they are on at the save, and a
replay by the transcript seats a block's stations on that hull at their stationed tick, which
would seat a captain who has since gone aboard the Amazon on the Amazon from the start. The
harness therefore keeps the hull it was first seated on (`Harness.seated_on`, in its save
record), `World._save` and `_hull_blocks` group the records by it, and `restore_hull` seats
them there; the replayed moves carry each harness on from there as the play did. A save from
before this package has no `seated_on` and reads as it does (the hull of its block).

**The consent's record holds without a new question.** The consent brief
(`docs/agents/ConsentBrief.md`, never edited by this package) describes the captain's station
as the command of a ship, the player's or another, and the passenger's as "aboard with no
duty"; a station that goes with its person into another hull is a station of one of those
kinds on that hull, with no more authority than the brief describes (a visiting captain has a
passenger's reach, less than his own), and "the particulars of a station may change as the
game is built without this question being put again". The boat's `captain` is the captain's
kind on a small hull. So no gap is named for package 55 by this design; the one sentence the
brief does not say in words is that a station's person may leave his ship and come back, and
that is a particular of the station (his place, which `movement` already lets him change by
going ashore) and not a kind of thing. The seat at a model (`seat: <model> as captain of
<ship>`) is read from the consent record as 67 reads it (`seats._consent_record`) and nothing
of it changes; the player's own seat on another ship (§4) is the owner's and asks no record.

**`where am I`, `the ship` and the station line answer the hull he is in.** `where am I` is a
new reading of the `query` kind: the asker's place by his whereabouts ("aboard the Raven, in
the cabin"; "in the Raven's boat, under oars, pulling for the quay"; "ashore at Plymouth, at
the market"; "aboard the Amazon, on her quarterdeck, a visitor"), the asker the order's actor
as `movement.person_of_actor` finds him, and for a visitor the hull's he is in. The station
line's "where" (`readings._line_where`) and `spot_words` say the hull where it is not the
station's own; the reading `the ship` (85's) is the followed hull's and, asked by a visitor,
the hull he is in. The hearing is by spot already (84's step 2), so a visitor on the Amazon's
quarterdeck hears what is said there and nothing of the Raven's.

**The boat as the road between hulls at sea** is item 3's "by the boat" without the boat as a
hull (which is item 4's): `send the boat to the <ship> with <persons>` is an errand of a
hull's dealings (`Dealings.send_boat_to`), the pull to the other hull at the boat's pace as the
pull to the quay is (her distance by the truth, within the hail's reach doubled: a boat is not
sent across the sea), the persons put aboard her by `put_aboard` when the boat is alongside
her and the boat back as from the shore; on a sleeping hull two jobs of the port as step 4
of 84 made them. The other ship's `come aboard` fetches a person of any hull's company from
the quay of her port (`find_anywhere`, where `fetch_person` finds the company's own today).
The boarders' movement (73's deck won): `boarding._end("carried")` puts the attacker's
boarding officer (the person the quarter bill names as the boarders' officer, else nobody) on
the carried deck by `put_aboard` with his station following, so that a model seated as the
first lieutenant who led the boarders stands on the prize's deck as a visitor and reports from
there; the prize crew and the captive are 74's on the same function.

## 3. The world with no followed hull (item 1): the design and its cost

**The design.** A scenario with `ship: none` (or `director: observe`, which implies it) builds
the World with no ship file: today's point-ship World, which `World.__init__` makes already
(`PointShip` at the scenario's position) and which `make_scenario_world` returns for a file
with no `ship:`. That World's own hull is **the observer's**: a hull of no ship, kept as
`hulls[PLAYER_ID]` so that every id rule of 84's stands (the save's top block hers, her acts
unprefixed), with `World.observed` true and `World.followed` **None**. The one rule, the
followed hull is the World's default, then gives: `World.own` the observer's hull when
nothing is followed (it does: `hulls.get(None)` is None and `_own` is returned);
`followed_words` "no ship followed" (the branch 84 left ready); `follow "Palinure"` the
centre on her hull, made in the far shape if she has none, and awake under the cap as the
followed hull of the world (the switch holds the followed hull fast as it holds the player's);
`follow nobody` (or `unfollow`) back to the observer's. What the observer's hull does and does
not do:

- **No vessel of hers on the sea**: `Vessels.player_shadow` returns None for an observed
  world, so no brain, lookout, set or action meets "the ship" (today every far captain sees
  the player's ship; an observed world has none to see). `_tick_vessels` runs the far bodies
  as before (its gate reads the other sail).
- **The ship's orders refused in words** at her prompt: `World.submit` on the observer's hull
  answers every order but a world order and the world's readings (the date, the war as the
  news has it, the weather at the view) with "No ship followed: follow one ('follow
  \"Palinure\"') or give the world an order ('world: ...')"; the standing book is empty and
  takes no order; her rules captain is none (`Captain` of a point ship judges nothing).
- **The readings that assume a hull answer "no ship followed"** through the registry's
  `none_words` on the observer: the ship's rows (the helm, the sails, the log, the lead, the
  account, the people, the stores, the port, the boat) give the words and no figure; the
  world's rows (the wind at the view, the sky, the tide at the view, the sail in sight from
  the view by a lookout of a height of eye of nought, which sees what a boat would) answer.
- **The centre**: the cap's, the business's region, the near detail's and the chart's view
  are `world.position`, the observer's point: the scenario's position, moved by `look at
  <place or position>` (a driver's line, journaled and replayed as `follow` is), or the
  followed hull's when one is followed. The lookout on the observer's hull looks from the
  view (so the observer's log says what passes within sight of the view, as the owner
  watching the chart would see it); her weather is the systems' at the view.
- **The pace rule** reads `open_samples`, which walks the hulls; the observer's hull has the
  director's station and nothing else; the floor of truth 51 is the frigate's and does not
  apply to her; the cap's count leaves her out as it leaves the player's hull out.
- **The console and the browser open at the director's station**: the drivers seat the
  player at the director's (`seat_player(world, "director")`, which `--seat director` does
  today) when the scenario is observed and no seat is named; the console's prompt says
  "the director" in place of the captain, the browser's snapshot carries `followed: {id:
  null, name: "no ship followed"}` and draws the chart's view with no ship on it until one
  is followed (the page's own ship drawn only with a followed hull).
- **The director** is bound on the observer's hull as it is bound on the player's today
  (`agent_journals["director"]` rides `World.players`, which is the observer's); its truth
  walks the hulls as before; `aboard:` without a name and `captain:` are refused in words
  until a hull is followed (there is no ship of the followed's to act on), `follow "X"` is a
  form of its own (§7).

**What the World's construction assumes of a ship, found on the way to the measurement.** A
point-ship World on a scenario with a book of standing orders fails at the book's parse
(`standing.grammar.parse_standing` reads `ship.extra["orders.nouns"]`, which a `PointShip`
has not got): an observed scenario carries no `books:` and no `intent:`, and the loader
refuses them in words when `ship: none`. The other places 84's postscript names (the
readings registry's rows, the lookout's height of eye, the reckoning, the snapshot, the
`ship_words` of a brief) each read `world.ship` and answer a `PointShip` oddly rather than
failing; item 1 gives each its words. Measured as each is touched; the list goes in the
postscript.

**The cost, measured.** Truth 51's form (a thousand ticks to settle, the best of three
thousands), this container, one after the other with the load under 0.5:

| the world | ticks a second |
|---|---|
| the frigate alone on the station trial (`tools/pace.py alone`) | 687 |
| a point-ship World at the trial's position on the Channel's chart, the tide and the weather, three ships under brains (a brig-sloop, a merchant brig, a frigate) and no ship of the player's | 6,448 |

The observer's hull costs about a tenth of the frigate's tick: its body is a point ship's
(`PointShip.step` is a few lines), its lookout, tide, weather and geo as any hull's; the three
brains' minutes are the same in both. So **the world with no followed hull costs nothing the
pace rule or the floors see**, and following a hull costs what that hull costs awake, which the
cap already pays for. The promotion's cap: the followed hull is held awake and left out of the
count against the cap, as the player's hull is since 84's step 10 (`crews.crewed`); that is the
one rule carried through.

**What should move: nothing pinned.** No recorded scenario has `ship: none`, and every World
of 84 keeps the player's hull as its own; the observer's hull is that hull with
`followed = None`, so a world with a ship reads line for line as it did. The proof is the
fast tier whole and the known truths' slow tier after the step; a pin that moved would be a
finding.

## 4. The player's own seat on another ship, and the director's door (item 2)

**`--seat captain --ship <name>`** for the player at every driver: the scenario's world
built as it is, her hull made (in the far shape by `station_world` when she has none, awake
when the cap allows), the drivers set to **follow her** (`World.follow`, a driver's line
journaled and replayed, as 84 built it), and the player's prompt hers: his orders go to the
followed hull (`World.submit` reads `self.own`), his person is her captain (`people.captain`
of her company, the rules captain standing aside at his hand as on his own ship:
`captain.player_hand`), his `--seat` at a lesser station of hers (`--seat officer --ship
Raven`) a `PlayerSeat` on her hull. This is 84's follow with the seat's words; what the
brief adds is **the player's own hull "brainless and far or under her rules captain as the
scenario says"**: with an `intent:` she has her rules captain, who sails her by it and judges
once a minute as he judges a crewed stranger's (the player's hull is awake always, 84's rule,
so he has the whole surface); without one she lies where she is, her watch kept and her
sails as they were (a hull with no intent and no hand is becalmed in her orders, which is
what a ship left with no captain does), and the words say so at the start. `follow` back to
her gives the player his own prompt again, the Raven's captain hers (her rules captain
carries on by his intent, or a model holds her).

**The consent read as 67 reads it**: a model seated at her captain's station by the director
(`seat:`) or by a door (`--station captain --ship`) is read from its record exactly as today;
the player asks no record (he is the owner at the door, the consent brief's standing party).
Where the player is at her captain's station and a door comes for the same station, the door
is refused by the rule of reach as it is on his own ship.

**The director's door's question (84's open item), decided from the one rule, the followed
hull is the World's default.** The owner's door (the console's and the browser's "the
director's log", `two stories`, the channel) and the director's own reads between ticks see
the World's names, which are the followed hull's: when the player follows the Raven, the
director's `read_log` without a ship reads **the Raven's log**, `aboard:` without a name is
**aboard the Raven**, `captain:` and `captain: carry on` are **the Raven's rules captain's**
(the one the player has been commanding and stood aside), and the truth's `within=` is from
her. Why: the director shapes the game the player is in, and the player is in the followed
hull; a director that kept reading the player's own hull while he commanded another would
doubt a cask found stove aboard the ship he cannot see and act on a log he is not reading.
The director's harness itself stays bound where 84 left it, on `World.players` (the player's
own hull, or the observer's), since the director is a station of the world and of no hull
and `World.players` is the one hull every world has; its samples read the World's names,
which follow. The hull is named at an order's head when the director means another
(`aboard the Amazon: ...`, 84's step 9), and the words of the refusals say which hull is
meant where it matters ("the followed ship, the Raven").

**86's three seams reworked on it.**

- **The free intent** (`captains.FREE`, the review's section 5): a free intent is the goal
  told to a model at her captain's station, which her rules captain does not sail by; he
  lies her to "until a model or the player takes her captain's station". The test of who
  holds her is by the hull: `Captain._free` lies her to unless her hull is **held**, where
  held is one of a model at her captain's station (`CAPTAIN in hull.agents`, the holder not
  released), the player's seat at it (`hull.player_seat`), or the player's prompt (she is
  the followed hull and the player has given her an order, so the captain stands aside
  already). No `parent is None` anywhere in it; the one place the captain reads `parent`
  (`_hold_event_came`, the hold's event read from her far body) stays, since it reads her
  vessel and not the player's ship.
- **`hail.model_holds_her`** by the hull a model or the player holds, not `parent is None`:
  the other hull is held when a model holds her captain's station, or when she is the
  followed hull and her rules captain does not command (the player at her prompt, who
  answers by `say to her`), or when she is the player's own hull with no rules captain at
  all; a hull nobody holds is answered by the table as before. So the player who follows the
  Raven answers a hail of her, and the Amazon he left is answered by her table or her rules
  captain.
- **Keeping the station on the player's ship by her name** (`orders/station._named_or_kind`):
  the player's ship is `World.players`' vessel (`root.vessels.own`), read by her name and
  her description as any sail's; `player_shadow` is not called (it brings her up to her
  truth, which the station's reader has no business doing); the id 'the ship' stays her
  vessel's id, since `PLAYER_ID` is hers (84's step 7).

## 5. The boat as a hull of the one world (item 4)

### 5.1 Her file, through the generator, to the ships session's principles

**Which boats get a file.** The eight ships' `boats:` lists stand as they are (the brief:
"no existing ship file moved by a byte but for that key where it must point at a file"). A
file is made for a pattern of boat the game sends away as a vessel, and the lists point at
it with `file:` as the last key of the entry; a boat without a file (the frigate's barge,
pinnace and jolly boat, the schooners' long-boats and yawls, the merchant brig's, the
cutter's punt, the smack's boat) keeps her errands as they are and cannot be manned as a
hull ("she has no file of her own to be a vessel by: her errands are the script's"). Five
patterns, one class each in the ships that carry it, listed as such (principle 10: no silent
sharing):

| the file | the boats of the eight it is the class of | the figures the file is built from | the rung and the source |
|---|---|---|---|
| `boat-yawl-16.yaml`, a 16-ft four-oared boat with a standing lug stepped at will | the lugger's boat (16 ft), the brig's jolly boat (16 ft), the cutter's boat (15 ft: the difference of a foot recorded in the cutter's note and never moved) | length 16 ft, breadth 4 ft 0 in (Luce's rule, a quarter of the length), depth 1 ft 9 in, draught 1 ft 2 in laden (judgement), displacement laden 1,000 kg (the boat about 500 kg, five men and their gear the rest; judgement), four oars of 12 ft, one mast of 12 ft with a standing lug of 60 sq ft (judgement after the yawl's and cutter's columns of Steel's boats' stores) | Falconer 1780, YAWL ("a wherry or small ship's boat, usually rowed by four or six oars"); Steel 1805 p. 181 (OCR l. 11336 to 11380: the yawl "less than the pinnace", the boats "constructed for rowing or sailing"); Steel 1794 vol. II, the boats' stores table (the YAWL or CUTTER column: masts, sails and halyards allowed, OCR l. 20713, 21856, 22936); Luce 1866, 'Boats'. The lines `judged`: to read, Steel 1805 Folio LVII, "Dimensions and scantlings of boats" (IA leaves 599 to 602; the OCR at l. 43444 is garbled), which gives the yawl's dimensions by length. |
| `boat-cutter-28.yaml`, the frigate's first cutter | the frigate's first cutter (28 ft); her second cutter (25 ft) is the same pattern smaller and is recorded so, no file | length 28 ft, breadth 7 ft (Luce), depth 2 ft 9 in, draught 1 ft 6 in laden (judgement), displacement laden 2,900 kg (judgement), eight oars, a lug of 160 sq ft | Steel 1805 p. 181 ("ships' cutters ... shorter, broader, and deeper, in proportion ... clincher built, and constructed for sailing or rowing"); Luce 1866 'Boats' (the first cutter .9 of the launch); the frigate's file (Luce's rule, 0.9 x 31). `judged`; to read, Folio LVII. |
| `boat-launch-31.yaml`, the frigate's launch | the frigate's launch (31 ft) | length 31 ft, breadth 7 ft 9 in (Luce), depth 3 ft 3 in, draught 1 ft 10 in laden (judgement), displacement laden 4,500 kg (judgement: Luce's weight rule for the launch herself, 2.5 lb x B^2 x L, gives about 2.1 tons, and the water she brings off in gang casks is her load), ten oars, a lug of 250 sq ft | Steel 1805 p. 181 ("the launch ... longer, more flat in its bottom, and lower ... better calculated for rowing and approaching a flat shore"; "fit to weigh an anchor"); Steel 1794 vol. I ("sent in the long-boat", the stream anchor, OCR l. 5739); Luce 1866 'Boats' (2.6 root(L)). `judged`; to read, Folio LVII. |
| `boat-launch-25.yaml`, the brig's launch | the brig's launch (25 ft); the merchant brig's long-boat (20 ft) and the schooners' long-boats (20 ft) are the pattern smaller and recorded so, no file | length 25 ft, breadth 6 ft 3 in (Luce), depth 2 ft 9 in, draught 1 ft 6 in laden, displacement laden 2,700 kg (judgement), eight oars, a lug of 160 sq ft | as the frigate's launch; the brig's file (Luce's rule, 2.6 root(95)). `judged`; to read, Folio LVII. |
| `boat-cutter-23.yaml`, the brig's cutter | the brig's cutter (23 ft) | length 23 ft, breadth 5 ft 9 in (Luce), depth 2 ft 4 in, draught 1 ft 3 in laden, displacement laden 1,900 kg (judgement), six oars, a lug of 110 sq ft | as the frigate's cutter; the brig's file. `judged`; to read, Folio LVII. |

The figures in the table are the design's; the file's own figures are worked by the
generator from the length and Luce's breadth rule as the ships' are, and the file's comments
carry each rung and source in the ships' form (the hull's keys with their notes, the spars'
and the sails' with theirs). **The ladder is honest**: no boat's lines are on file (S) and no
period plan of a boat is read (S†); Luce's rule of breadth is a named period rule (R) and the
rest is judgement (T) that names what it differs from, each line marked so (`judged`, `rule`)
in the `marks` key once the shape keys of stage 0H are on the trunk (§5.4), and in the notes
meanwhile. Steel 1805's Folio LVII is the better source and is named in every file as "to
read": read, its figures replace the judgement in the file and the drawing, and never the
game's behaviour (principle 12), since nothing the oars or the sail read is taken from the
shape.

**The generator's smallest change** (`tools/gen_ships.py`): `Builder.boats` takes an optional
`file` as the ninth field of an entry and writes it as the last key of the boat's mapping;
`boat_entries` passes it through; five small functions `boat_yawl_16`, `boat_cutter_28`,
`boat_launch_31`, `boat_launch_25`, `boat_cutter_23` after the smack's, each a `Builder` of a
boat's hull, one mast, one lug and its lines, four to ten oars (a new `oars:` section, §5.2),
a crew of a coxswain and the oarsmen, no guns, no ground tackle but a grapnel, no hold, no
boats; and the five calls in `__main__`. The eight ships' functions change by the `file`
field on the entries named above and nothing else, so that the eight regenerate
byte-identical but for a `file:` line under each such boat (`test_generator_reproduces_the_
committed_files` the gate on the commit, run on the merged tree). The ships session's branch
moves the generator's profile helpers beside this; the boat functions use none of them until
the shape's helpers are on the trunk, and then take `hull_profile` and `hull_form` as the
eight do (§5.4).

### 5.2 The oar force on a hull: the physics addition, with its source

**The model.** The oars are a thrust along the hull's axis, added to the sails' in the
integrator's substep (`integrate._substep`, beside the cable's pull and the trawl's drag,
which are the two outside forces it has), read from `ship.extra["oars"]`, an `Oars` state the
orders set: the hands at the oars (`manned`, up to the file's number), the stroke (`give
way`: the full stroke; `easy`: half; `lie on your oars`: none), and the men's fatigue (hours
pulled since fresh). The thrust of one oar is

    F_oar(u) = min(F_0, P / max(u, u_min)) x stroke x f(hours)

with `F_0` the pull a man sustains on the blade at no way, `P` the power a man delivers to
the water at the oar over hours, `u` the boat's way through the water, `u_min` a floor so the
thrust is finite at rest (0.3 m/s; the stroke's own speed at the catch, judgement), and
`f(hours)` the men's tiring: 1 fresh, falling by a third in the first two hours and to a half
at four, then to a quarter at eight (judgement on the period's practice of towing watch and
watch: "the boat's crew tiring by the hour", the brief). **The figures**, marked judgement
against the brief's three words (three to four knots light, a knot and a half towing, the men
tiring by the hour): `F_0` 50 N, `P` 60 W an oar. They are not in the period's books, which
give no figure for a man's power at an oar (Falconer 1780, OAR: the oar as "a lever of the
second class, whose fulcrum is the station upon which the oar rests on the boat's gunnel",
and nothing of its force; Steel 1805 p. 181 the boats' purposes), so they are fitted to the
behaviours the brief and the sources give and written as such:

- a 16-ft boat under four oars, 8.5 m2 wetted (Denny-Mumford's rule as `parts.Hull.wetted_
  area` has it), hull speed 5.4 kn: the engine's resistance (`hull.resistance`, unchanged) at
  3.5 kn is 133 N, 239 W; four oars at 60 W give 240 W, so she makes 3.5 kn fresh under the
  full stroke, and 3 kn when the men have pulled two hours (Falconer's "four or six oars"
  yawl; the pilots' boats of `ports.py` pull at `BOAT_PACE_KN` 4 kn by the owner's judgement
  of package 35, which this meets within half a knot);
- the frigate's launch under ten oars, 28.3 m2 wetted: 394 N at 3.5 kn, 710 W; ten oars at
  60 W give 600 W, so 3.3 kn fresh;
- the tow (§6): at a knot the boat's oars give `F_0` x oars less her own resistance, so the
  16-ft boat 200 N less 10 N; the cutter (129 m2 wetted) wants 140 N at a knot and the
  lugger (133 m2) 144 N, so each is towed at about **a knot fresh, falling to three
  quarters of a knot in two hours and half a knot in four**, which is the brief's "a quarter
  of a knot to a knot for a cutter or a lugger by the boat's size and hands" and 7b-113's
  "towed clear at half a knot" with the men an hour or two at the oars; the frigate (669 m2
  wetted; 182 N at half a knot, 726 at a knot) towed by her launch alone (500 N less 15)
  makes **0.8 kn fresh and half a knot after four hours**, and by every boat she has (46
  oars by her file) 1.7 kn fresh: §6 says what the truth makes of it.

**The source of the model's form**: the oar as a lever that strikes the water (Falconer,
OAR), the thrust the water's reaction to the blade; a man's sustained output bounded in force
at low way and in power at speed is the ordinary model of a rower and is marked as the
design's, not the period's. Nothing else of the physics changes: the boat's hull is a
`HullSpec` as every ship's, her resistance, sway, yaw and rudder the engine's (her rudder a
yoke's, `max_angle_deg` 35), her sail a `lug` of the engine's classes, her heel the engine's
with a `gm_m` of a boat's (judgement, 0.5 m). The oars are a new section of the ship file
(`oars: {number, thrust_n, power_w, tiring_h}`, the schema's one new key for the one new
figure, each with its note), read by `physics/integrate.py` through the `Oars` state and by
nothing else.

### 5.3 The boat manned and away: a hull of the world

**When she is a hull.** The boat becomes a vessel of the sea with a hull of her own **when
she is commanded**: `go to the boat` (the player or a stationed person goes down into her to
take her), `tow her with the boat` (§6), or `man the boat` with the sweeps' orders to follow;
she is put on the sea by `Vessels.add` (id `<her ship's id>:<boat id>`, her name "the
Raven's boat", `boat=True` so that she is seen within `BOAT_SEEN_NM` and no farther, her
nation her ship's, her file the pattern's, no brain: she is commanded or she is alongside),
her hull made by `crews.make_hull` from her file at her ship's truth a boat's length off the
ship's lee quarter, awake, her company mustered from her file (the coxswain's post and the
oarsmen, her own `muster` stream, fresh at each manning: the hands the ship loses while she
is away are the boat's crew, taken from the ship's muster as the evolution `send_boat` takes
them, so that a cutter of thirty feels her boat away and a frigate does not), the person who
commands her put aboard her by `put_aboard` with his station following (§2: her `captain`).
**The errands as before when nobody commands her**: the prices, a letter, a passenger landed
or fetched, the kedge laid out, the pilot's cutter, the lighter's and the hoy's jobs run as
they do today by the script or the port's jobs, with no hull made and no line moved, so that
every recorded passage with a boat away in it reads as it did; `go ashore` from a station
lands him by the script as today, and a person landed by the boat is in no hull (`hull`
None, `where` 'boat', as 84 left it). The one new road into the boat is to command her.

**Her tick** is a hull's: the World's tick with her current, within `tick_crews`, her physics
by the oars and the lug, her lookout (a height of eye of a man standing in a boat, 1.7 m
over her gunwale: `height_of_eye` reads her file's `deck_height_m`), her account (her
coxswain keeps no reckoning: her `Navigation` is set to her truth each minute at the
promotion's sigma, as a sleeping hull's is, since a boat in sight of her ship does not work a
traverse board; said once in the note), her log her own (hers while she is away; hoisted in,
her log's lines are kept in her ship's log under the boat's name as `boat.log` entries, so
that nothing of her voyage is lost and the ship's record says what her boat saw), her bells
none (a boat strikes no bell: `_bells_struck` reads a hull with no bell), her people's needs
hers (the oarsmen's fatigue is the oars' model, not the needs'). The cap: a manned boat is
held awake with her ship while her ship is awake or followed (she is a dealing of her ship's
and counts as one hull of the cap's three; a boat whose ship sleeps sleeps with her, her far
body moved by the plan at `BOAT_PACE_KN` as the pilots' boats are).

**The orders of the boat** (her grammar, through the vocabulary as every ship's; new verbs
with their synonyms in `data/vocabulary.yaml`, handled by `orders/boat.py`, each refused in
words on a hull that is no boat): `give way` (the full stroke; `give way together`), `easy
all` (half), `lie on your oars` (the oars out, no stroke; `oars`), `boat your oars`/`in oars`
(the oars in), `pull for <a point, a bearing, the ship, the shore, a sail in sight>` (the
coxswain steers for it and keeps steering as it bears: the helm set each minute by the
truth's bearing, a boat in sight of her mark), `step the mast` and `unstep the mast` (the
mast up or down, by a small evolution of her hands: three minutes, judgement; the lug cannot
be set with the mast down and the oars cannot be pulled with the lug drawing, which is the
period's practice and the words of the refusals), `set the lug` and `take in the lug` (the
engine's `set_lug` and `take_in_lug` on her one lug), `come alongside` / `the boat alongside`
(she pulls for her ship and, within a boat's length, is hoisted in: her people aboard the
ship by `put_aboard`, the one who commanded her back at his station, her vessel gone from the
sea and her hull released, her log folded into the ship's), the helm's words of any hull
(`steer <course>`, `port`, `starboard`), the hail, the colours, the readings, the
conversation and the free lines. The ship's grammar in the boat is refused in words naming
hers ("A boat has no topsails: the lug, the oars and the helm are hers").

**The player aboard her** by `go to the boat` (and `go to the launch`, `the cutter`, a boat
of the file's by her name): the boat manned and made a hull if she is not, his person put
aboard her with his station following (the captain's prompt in the boat is the boat's
`captain`'s), **the drivers following him** (`world.followed` moves to the boat's hull with
him: a consequence of the order, deterministic, recorded as a routine line `hull.followed`
of the ship's log and not as a driver's input, so that a replay of the order moves it the
same; the console's and the browser's `follow` stand for the owner's own choice), so that
her readings are his while he is in her (the wind at her, her way under oars, her account,
what her lookout sees, the ship a sail in sight from the boat) and the ship's again when
`come alongside` brings him aboard (`followed` back to his hull by the same rule). `where am
I` says "in the Raven's boat, under oars, pulling for the quay". The ship's deck orders from
the boat are refused in words ("You are in the boat; the ship's deck is not yours from
here"), and her book sails her meanwhile. A model seated as a ship's captain takes her boat
the same way, and the harness's samples are the boat's.

**The boat lost** is a state the ship's file knows: `BoatState.lost` with the word (`stove`,
`swamped`, `cut adrift`) and the tick; set by the sea when she is away under oars in a sea
above her weather (the sea's words beyond "moderate" for a 16-ft boat, beyond "rough" for a
launch: judgement; she is swamped, her people lost into the water as a man overboard is lost
today, said urgently in both logs), by the director's `aboard: the boat stove` (a form of the
`aboard.found` table with its condition: she was hoisted in or out in the last watch), or by
`cut the boat adrift` in a sea the ship cannot hoist her in; a boat lost is sent on no
errand and manned by nobody ("the boat is lost: stove on the 12th; a new one is the yard's")
until the yard's job at a port replaces her (`demand a boat of the yard`, the yard's time two
days, judgement); the truth and the reading `the boats` say so.

### 5.4 Her drawing

The viewer draws the boat under oars or sail as it draws any hull, from her file; her shape
keys (stage 0H's `profile:` with `rail_m`, `breadth_m`, `stem_m`, `stern_m`, `section_m`,
and `form: {stern: {type: square}, head: none}`, each `judged`) are filed by the ladder
through the ships session's `hull_profile` and `hull_form` helpers if B5's road is on the
trunk at that hour, and her oars are drawn as lines from the thwarts when `oars.manned` and
not `lie on` (the viewer reads `ship_view`'s state, a `oars` block in the server's state, the
only reader beside the tests). If the road is not yet on the trunk, the boat's shape keys are
filed by the ladder with the figures ready and her drawing is left to the ships session's
road, said so in the postscript; the drawing never changes how she pulls, sails or is hit
(principle 8), and the guard that nothing under `physics/`, `combat/`, `crew/` or `world/`
reads a shape key stands. Her drawing is the last commit of the package.

## 6. Towing by the boat, and the kedge's false denial (item 5)

**`tow her with the boat [to <the point or bearing>]`** from the ship, in a calm or an air
too light to steer by: the boat manned and made a hull (§5.3) with the tow-line (the
hawser's bight to her stern-sheets' bolt, Luce 1866 'Boats', 'Towing': "take the tow-line
to the foremost stem-sling bolt"; "the heaviest boats should always be nearest the tow"),
her plan the tow's bearing (ahead when none is said, as the kedge is laid ahead); the boat
holds her station a line's length ahead of the ship on the bearing (her position set each
tick from the ship's, since the two are one body on the line: the coupling is kinematic,
which is stable and costs nothing), and the force on the ship is the boat's oars' net pull at
the ship's speed, `oars x F_oar(u_ship) - R_boat(u_ship)`, applied at the ship's stem along
the line (`ship.extra["tow"]`, read by the integrator as a thrust and a yaw moment at the
bow with the lever of half her waterline, as the cable's pull is read at the hawse); the
rudder answers as the water passes it. **The ship's head comes round first** (the yaw inertia
is small beside the mass: the frigate's head comes round two points in a few minutes under a
500 N pull at the stem) and she gathers way by her resistance: the figures of §5.2 as measured
in the postscript. **The boat's crew tire by the hour** by the oars' `f(hours)`; the period
relieved them watch and watch, which a boat of five cannot, so the tow fades and the words
say so once an hour ("the boat's people are tiring; her way is falling"). **`the boat
alongside`** ends it (the line cast off, the boat hoisted in by §5.3's road, the ship's way
left to die). **Refused in a sea the boat cannot work in** (the sea's words beyond "moderate"
for a 16-ft boat, beyond "rough" for a launch, the same bound as her swamping; judgement),
with no boat, with the boat away or lost, and when the ship is at anchor or aground ("weigh
first"; "she is aground: the tide floats her or the kedge hauls her, the boat cannot").

**The frigate, taken another way, with the reason.** The spec's §21k and 7b-113 say the
frigate's boats "towed her head round in a calm and no more", "little or nothing" of way.
The physics as they stand (unchanged by this package but for the oar force) do not bear it
out: her resistance at half a knot is 182 N and her launch's ten oars give some 500 N fresh,
so she makes about 0.8 kn with her launch alone and 1.7 kn with every boat she has, falling
as the men tire; and the period's logs bear the physics out rather than the words (Luce 1866
p. 466, Hull's report of the Constitution's chase of 1812: "four of the enemy's ships ...
some of them having six or eight boats ahead, towing, with all their oars and sweeps out, to
row them up with us, which they were fast doing"; "the boats all out towing ship" of a ship
of war becalmed, p. 339). The design therefore **keeps the physics' answer** and makes
7b-113's frigate clause "her head brought round in a calm by her launch, and her way under a
knot and falling as the men tire", which is the period's practice as the book has it, and
puts the words to the lead with this note: the brief's "little or nothing" was a judgement
and the physics give a figure; the owner may have the lesser by a smaller `F_0`, which the
note's table shows the cost of (the cutter's tow would fall with it).

**The kedge's false denial.** `Dealings._boat_kept` says "the boat was not sent away" and
puts her back at the booms once a minute when no `send_boat` evolution is in the runner's
hands, which is true of the lay-out of a kedge (`LayOutKedgeScript` holds the boat and is no
`send_boat`) while it goes on: the boat said away with the kedge was denied and the state
stood down under the script. The mend: the keeper reads every evolution that holds the boat
(`send_boat`, `lay_out_kedge`, the tow's), by the scripts' `holds()` word for her, and
denies nothing while one of them has her. Kedging itself is left to the anchor physics it is
in (spec §21k's head: the pull has been there since package 34).

## 7. The stations, the director and the readings (item 6)

- **Readings**: `the boat` (alongside, away on her errand and where, manned and a vessel of
  the sea with who is in her, or lost and since when), `the boats` (each with its length,
  oars, crew and file, lost ones said), `where am I` (§2), `the followed ship` (the drivers'
  centre by name, "no ship followed", or "the observer's view at <position>"), each a row of
  the registry with its `none_words`.
- **Events and tripwires**: `the boat away` and `the boat alongside` stand (`boat.away`,
  `boat.alongside`), and gain `the boat manned` (`boat.manned`), `the boat lost`
  (`boat.lost`), `aboard the <ship>` (a person come aboard another hull: `person.aboard`,
  with the ship's name in its data, watched by the station's stand-by as `at a sail within
  hail` is), `the tow begun` and `the tow ended` (`tow.begun`, `tow.ended`); each a row of
  the events table the primer's chapter 11 keeps equal to the registry (85's test).
- **The director's forms** after `WORLD_ORDER_FORMS` where 84 has not got them: `follow
  "<ship>"` and `follow nobody` at the director's seat (the drivers' centre moved by the
  director, which the owner's door and the observed world want; a driver's line journaled
  as the console's is, source the director), `person: "<name>" goes aboard the <ship> by the
  boat` (a person of any hull put aboard another by his ship's boat, the errand of §2 as a
  world order: doubted where the two are beyond a boat's pull of each other, refused for a
  held station's person), `ship "<name>": order send the boat to the <ship> with <persons>`
  (the hand, as the errand is her captain's order), `aboard: the boat stove | swamped | cut
  adrift` (the `aboard.found` table); the dry run knows each (it performs on the copy as
  every form does).
- **The truth** shows every boat as a vessel when she is one: a manned boat is a row of the
  hulls' walk with her ship named, who is in her, under oars or sail, towing whom; a boat at
  the booms, away by the script or lost is a word in her ship's row.
- **The harness**: a station's samples follow the person's hull (§2); `shape_words` says of
  a boat "the Raven's boat, a hull of the one world under your oars"; the brief head's
  `ship_words` for a station in a boat names the boat and her ship.

## 8. The truths

7b-113 and 7b-114 as the spec has them (with §6's reading of the frigate's clause), and
7-320 onward, 85's rule binding their words and the primer's:

- **7-320** a world with no followed hull (`ship: none`, `director: observe`) runs a day at
  seed 7 with its business on and a director observing, the centre on the observer's view
  and then on the hull the observer follows; nothing pinned moved (the fast tier and the
  known truths' slow tier, before and after). Slow.
- **7-321** the observer's readings answer "no ship followed" in words, the ship's orders
  are refused in words, the world orders stand, `follow "X"` moves the centre and the cap
  wakes her, `follow nobody` gives the view back.
- **7-322** the player seated as captain of another ship (`--seat captain --ship Raven`),
  his own hull brainless and far, the drivers following him, his orders hers, her rules
  captain aside at his hand; the save replays his acts to the same digest of both logs.
- **7-323** the director's door with another hull followed: `read_log` without a ship reads
  the followed hull's, `aboard:` without a name is aboard her, `captain: carry on` gives her
  captain his hand back; named, the other hull's.
- **7-324** a person moved from one hull to another by the boat (`send the boat to the
  Amazon with Mr Pope`) in play and in the replay to the same digest by both roads, his
  station following him as a visitor's voice and his own again when he comes home.
- **7-325** the boarders' officer stands on the deck won (73's `action.carried`) by
  `put_aboard`, his station following; a captive put aboard the captor with his station
  standing down by the handover's rule (the hook 74 calls, exercised here).
- **7-326** the free intent by the hull: a free-intent ship lies to under her rules captain
  until the player follows her and gives an order, or a model is seated at her captain's
  station; `hail.model_holds_her` by the hull the player or a model holds; the station kept
  on the player's ship by her name reads `World.players`.
- **7-327** `go to the boat` makes her a hull and puts the player in her, the drivers
  following; `give way` pulls her at three to four knots light fresh and slower as the men
  tire; `step the mast` and `set the lug` sail her; `come alongside` brings him aboard with
  the readings the ship's again; the boat's log folded into the ship's.
- **7-328** the boat's errands run as before with nobody commanding her: a recorded
  passage with the boat away in it (the gate's day) holds its digest; `go ashore` lands a
  person by the script; the hoy comes off as a vessel of the sea by the same road and the
  lookout sees her.
- **7-329** the boat lost: swamped in a sea above her weather with her people lost, stove
  by the director's form, cut adrift by order; sent on no errand after, manned by nobody,
  the reading and the truth say so; replaced at the yard.
- **7-330** the tow: the cutter becalmed is towed at about a knot fresh by her boat, falling
  as the men tire, her head brought round first; `the boat alongside` ends it; refused in a
  sea the boat cannot work in, at anchor and aground.
- **7-331** the kedge's false denial mended: `lay out a kedge` runs to its end with the boat
  said away and no "was not sent away" line.
- **7-332** the director's new forms (`follow`, a person put aboard by the boat, the boat
  stove) perform on the copy in the dry run and in play; the truth shows a manned boat as a
  vessel.
- **7-333** `where am I`, the station line and `the ship` answer the hull the person is in
  (aboard, in the boat, ashore, a visitor), and the hearing by spot hears a visitor where he
  stands.
- **7-334** the pace: the observer's world at truth 51's form on the build machine against
  the frigate alone, the figures recorded (informative, `pace`).

The rest of 7-320 to 7-339 is left free for what the build finds.

## 9. The order of the steps, each a mergeable state

Each step one commit (or a few) on `claude/pkg-82` with the fast tier whole on its final
tree, the slow tier of the touched files and the known truths (`--slow -m "not pace" -n 4`),
the pace tests alone and last, ruff clean, the lead's head merged in at the boundary before
the step's final run; never the whole slow tier.

0. **This note**, reported to the lead for reading before item 3 is built.
1. **Item 3, the person's movement between hulls** (§2): `movement.put_aboard`, the
   harness following (`Harness.seated_on`, `move_to`), the visitor's voice, the save's blocks
   by the seated hull and the replay's restore, `send the boat to the <ship> with <persons>`
   on awake and sleeping hulls, `come aboard` across the registry, the boarders' officer on
   the deck won, the capture hook, `where am I`, the station line and `the ship`, `person:
   "X" goes aboard the <ship> by the boat`; truths 7-324, 7-325, 7-333. **Reported to the
   lead as soon as it is green, since 74 starts on it.**
2. **Item 1, the world with no followed hull** (§3): `ship: none` and `director: observe` in
   the loader, the observer's hull, `followed` None, the refusals and the `none_words`,
   `look at`, `follow nobody`, the drivers at the director's station, the snapshot with no
   ship; truths 7-320, 7-321, 7-334; what moved measured (nothing pinned should).
3. **Item 2, the player's seat on another ship and the director's door** (§4): `--seat
   captain --ship`, the player's own hull's state, the door's rule, 86's three seams;
   truths 7-322, 7-323, 7-326.
4. **Item 4, the boat as a hull** (§5), in commits of its own: (a) the five boat files
   through the generator with the eight regenerated byte-identical but for `file:`, the
   `oars:` section in the schema; (b) the oar force in the integrator and the boat's orders,
   the boat manned as a hull, `go to the boat`, `come alongside`, the boat lost, the hoy as
   a vessel; truths 7-327, 7-328, 7-329, 7b-114.
5. **Item 5, the tow and the kedge's denial** (§6); truths 7-330, 7-331, 7b-113.
6. **Item 6, the stations, the director and the readings** (§7): the readings, the events,
   the forms and the dry run, the truth's boats; truth 7-332.
7. **Item 7, the records**: the spec's §11, §12 and §21k "as built", the Harness's §17 and
   a §17b, the primer's chapter on the boat and on going aboard another ship (in-world under
   85's rule, run through `tests/test_in_world.py` and the forms tables), the director's
   library, the tuning notes "## Package 82", this note's postscripts; and last, in a commit
   of its own, **the boat's drawing** (§5.4).

## 10. What was rejected, and why

- **The station as a thing that ends and begins** (the brief's second reading): three
  conversations and three `seated` acts for one voyage ashore, and a captain's station that
  cannot begin on a ship with a captain (§2).
- **The boat a hull from the moment she is hoisted out, every errand hers.** It would move
  every pinned passage with a boat away in it (the gate's day sends the boat for the prices;
  the kedge trial lays it out), for no behaviour anyone sees until a person commands her;
  the errands stay the script's and the jobs', and the boat is a hull when commanded.
- **A two-body tow in the physics** (the boat and the ship each integrated, the line a
  spring): stiff, a new integrator's business, and nothing the player sees differs from the
  kinematic coupling (the boat is a line's length ahead at the ship's speed either way).
- **The frigate's tow made "little or nothing" by a rule** (a mass over which the oars move
  nothing): a rule against the physics, which the period's logs do not want (§6).
- **A separate observer object for the world with no ship.** The World's own hull with a
  point ship is that object already, and keeps every id rule of 84's.
- **The director following the player's own hull while he commands another** (§4).
- **The boat's crew taken from nowhere.** A manned boat takes her hands from her ship's
  muster, as the evolution does, so that a small vessel feels her boat away.
- **Files for every boat of the eight** (the barges, the pinnaces, the punt, the smack's
  boat): five patterns serve every boat the game sends away as a vessel, and a file nobody
  mans is a file to keep for nothing; the rest are recorded as their pattern's smaller or
  larger sisters, to be given files when a package wants them (77's cutting out).

## 11. Open for the lead

1. The frigate's clause of 7b-113 (§6): the physics' figure or a smaller `F_0`.
2. Whether `go to the boat` should move the drivers' centre with the player (§5.3), or leave
   `follow` to the owner's hand; the design moves it, since the brief says her readings are
   his while he is in her.
3. The boat's log folded into the ship's at the hoist-in as `boat.log` lines (§5.3), or kept
   apart in the save as a hull's log under her name: the fold is simpler and the save has
   no block for a hull gone from the sea; the design folds.
