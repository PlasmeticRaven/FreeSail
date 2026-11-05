# Design note: the door follows its harness, the visitor's name, the far hull's hail (package 82b)

Written before anything of package 82b is built, as its brief asks (`docs/dev/M7-WorkPackages.md`,
"Package 82b", and the section it draws on, "The owner's testing week: loose ends mended by the
lead"; the case study `docs/playtests/2026-11-05-small-convoy-all-models/case-study.md`, lessons 2,
4 and 5). It completes the reach of package 82 (`Design-BoatAndPersonAboard.md` §2: a station is a
person aboard, and his harness goes with him). Short, as asked: the seat's identity and its place in
the save, the visitor's name in every listing and reading, the far hull's sample for the hail, the
cap for a held hull, the boat's names scoped to the giver's hull. Nothing here is built yet; the
postscripts will say what was built and what was taken another way.

## 1. What the trunk does now (read and probed, 2026-11-05)

- **The harness moves; the desk's seat holds it by reference.** `movement.put_aboard` carries a
  harness into the host hull (`Harness.move_to`), entered in her `agents` under the visitor's
  station name. A probe in one live process (two doors of one model at the captains of the frigate
  and a brig, the brig's captain put aboard the frigate): the brig's door's seat (`Desk.seats`
  key `x/captain`) kept its harness object, its turns were served, and `stand down the captain
  pope` stood that harness alone down. So the breaks are in the roads that go through the name and
  the ship, not through the object:
  - **the seat's key is `<ship>/<station>`** (`remote.seat_key`), and every lookup that has no
    harness in hand goes by it: a door's stationing (`Desk.station`: `self.seats.get(key)`, then
    `world.agents.get(name)` on the hull the door names), its attach after a cut call or a restart
    of the door, the library read. After the move the harness is not where the key says
    (`agents["captain owen"]` on the *Lynx*, nothing at `captain` on the *Chevalier*), so a door
    stationing again by its own station's name finds an empty station and a fresh harness is made
    (the owner's note 4 of 11-01: "a new station made and a separate model seated");
  - **the seat's `world` is the hull at stationing** and is never moved: `Desk.holding()` (the
    lockstep's floor) and `Desk.stations()` test `seat.world` against the World, so a moved seat
    can drop out of the floor and the listing's consent rows;
  - **the listing names a moved station by the hull it is in**, not the ship it is of
    (`harness.all_agents`: "captain owen of Lynx"), beside the host's own station held by the same
    model through the same kind of door: the *Lynx*'s list read as one door holding two stations
    (lesson 5);
  - **the save has no identity for a harness**: its record carries the station of its first
    seating and the hull it was seated on (`seated_on`), which a second harness at the same home
    station (made while the first is away) shares; and a door after a load has only the name.
- **The owner's account of the stand-down of both** ("the Mr Hill" and his officer, 11-01) is not
  reproduced in one live process. Every road I can see to it goes through a re-stationing by name
  (the door seated afresh at the moved station, two seats then answering for one harness or one seat
  for two). I ask the lead for the save of 11-01 (`boat-between-ships-test`, as data) to reproduce
  it before item 1 is closed; the design below closes those roads whatever the exact one was.

## 2. The seat's identity, and its place in the save (item 1)

- **`Harness.ident`**, an identity of its own, made once when the harness is made and never changed
  by a move, a reseat or a take-over: `<seated_on>/<station>` (the hull it was first seated on, its
  station there: `ship-1/captain`, `own/officer of the watch` for the player's ship), with `#2`,
  `#3` appended where a harness of the game already bears it (a second seating at a home station
  while its first holder is away). Made in the order the harnesses are made, so a replay by either
  road makes the same idents.
- **In the save**: the harness's record carries `ident`; `restore` reads it; a save from before
  derives it as above (the same order, the same words), so old saves load and replay unchanged.
  The key still never enters a save.
- **The desk's seats are keyed by the harness's ident** once a station is taken (a seat still in
  its consent conversation keeps a provisional key of the door's address until its harness exists).
  A call carrying a key is resolved **by its key** (unique to one seating), the station's name and
  ship in its path read only to refuse a call whose key is another seating's; a call with no key
  (a stationing) resolves its address `(<ship>, <station>)` to a harness by **its home station**:
  a harness whose own station is that one (`h._home` while it visits, its station when home), the
  harness at that name on that hull only where none is away from it. So a door stationing again
  after a cut call, a restart or a load attaches to its own harness wherever its person is, and a
  loaded game's moved station (a `Playback` visiting the host) is taken over where it stands.
- **`seat.world` follows the harness** (read from `seat.harness.world`, never kept apart), so the
  floor and the listing see a moved seat.
- **`stand down <station>`** in the game stands down the one harness the words resolve to on that
  hull (as now); the desk's release stands down its seat's harness alone (by the key); a seat whose
  harness is stood down answers its door with the release and never re-points to another station.
- **The listing** (`Desk.stations`, `GET /api/agents`, the console's `state`, the browser's
  snapshot) names each station with its ship and, for a visitor, his host: "the officer of the
  watch, of the Raven, aboard the Amazon (X, through the API door)"; a station at home "the
  captain of the Lynx" off the followed hull as now.
- Truths: **7-390** (a door's station moved by the boat keeps its door and its model through the
  move, a stationing again by its own name, and a save and load: one harness, one seat, its
  model's name, its turns run on); **7-391** (two "captain" stations on two hulls through one door
  each, same model; one person moved aboard the other's hull; each door answered by its own
  harness; a stand-down of one leaves the other stationed).

## 3. The visitor's name, in every listing and reading (item 2)

- **The name**: `visiting_station` names the visitor's station `<his station>, of the <his ship>,
  aboard the <host>` ("officer of the watch, of the Raven, aboard the Amazon"), from his home
  station's name (`h._home`), never his own name; the kind the passenger's (`VOICE_KIND`), the
  domain the visitor's (`VISITOR_DOMAIN`), the brief `VISITOR_BRIEF` as 82 wrote it. The player's
  seat visiting gets the same name. The host's own "officer of the watch" is untouched: the
  visitor's name never equals a station of hers, and no prefix of it does either (the comma
  follows his station's words, so `_station_in`'s `name + " "` prefix rule cannot read "officer of
  the watch, of the Raven, ..." as the host's officer).
- **Addressed** in the host's orders by the full name, by his person's name (`_person_station`, as
  now: the voice is bound to him), or by "the <station> of the <ship>" (commas optional): the
  sentences' resolver strips the commas of a visitor's name when it matches.
- **His voice and his journal his own**: the journal is the person's already (`journal_of` by the
  holder, package 45c), so it follows him unchanged; the log's mark and the readings' station line
  carry the new name. `_unbind_visit` and the save's grouping use the same function for the name,
  so the replay and a save mid-visit name him the same.
- **The director's voice of a person nobody holds** (package 67's `voice/<name>`, named for the
  man) is not a visitor and keeps its name.
- **The primer's chapter 26** keeps its promise; its words are brought up where they say how the
  visitor is named and addressed. Truth **7-392**: the visitor's station named so in the host's
  stations, the listing, `where am I` and the log's mark; addressed by each of the three forms; the
  host's own officer of the watch unchanged and answered by his own harness.

## 4. A far hull's hail answered by her captain's model (item 3)

- **`model_holds_her` read for any shape**: the hailed vessel's hull (`vessel.crew`), full or far,
  is asked; a far hull keeps her stations and her `agents`, so the test is the same. Where a model
  holds her captain, `deliver` writes `hail.heard` (urgent) in her log, the stations hear it, the
  pending hail is remembered for `say to the <hailer>`, and nothing answers by table; the table
  answers only a ship nobody holds (far or full, as now).
- **His sample** is the far shape's as 84 left it (the far hull's harness samples on her far tick;
  an urgent line wakes him as on a full hull); nothing of 65's sample or `_reaches` is touched: the
  hail is a line of her log, which the sample already reads.
- **His answer**: `say to the <hailer>: <words>` from a far hull goes as from a full one (the
  hailer's log `hail.answered`, `_read_answer` for the nation); checked, and mended in `hail.py`
  alone if the far road misses.
- **The hailer's log** says "she has not yet answered" until he does (the words of `hail_order`'s
  pending line, the same for both shapes). The one existing sentence for a model-held full hull is
  replaced by these words; no pin reads it (searched), and any passage whose digest it moves is
  re-measured old beside new with the toggle.
- Truth **7-393**: two hulls at far detail, a model (a fake) at each captain's station; one hails
  the other; the hailed captain's sample carries the hail, no table answer is written, the hailer's
  log says she has not yet answered; his `say to` answers and the hailer's log carries it. Truth
  **7-394** replays such a passage by both roads to the same digests (with §5's danger).

## 5. A model-held hull is not half blind at far detail (item 4)

- **The cap**: a hull whose captain's station a model holds through a live door (a harness at
  `captain`, started, not released, its model not a `Playback`) ranks with the hulls in dealings
  (rank 0) and is **held over the cap**: the cap's count leaves out up to `HELD_OVER_CAP` such hulls
  (two, judgement from the brief's "four or five"; measured in the pace notes with four held hulls
  and the convoy's six sail). Held over the cap she is awake under the range's rule as any other;
  beyond the range and its hysteresis she sleeps as now. A hull held only by a `Playback` (a
  replay) counts as she was recorded (the transcript's live door): the rank is read from the
  harness's own `live` flag, carried in the save, so a replay wakes the same hulls.
- **Where the cap must hold** (more held hulls than the cap and its allowance): the far shape's plan
  keeps her off the dangers as the rules captain does: the plan's next leg is checked against the
  chart by 88's rule (`Captain._danger_ahead_by_chart`'s test, read and called, not copied), and a
  leg that stands into danger is put about or borne away under the plan's own orders, logged in her
  log as the plan's; and her captain is sampled at a danger line as on a full hull (an urgent line
  of her log, which wakes him).
- **The glass refused at far detail** ("the hull sleeps and only the plan's orders are mine") goes
  with her waking under the cap; where she must sleep the refusal stands, its words saying why.
- Truth **7-394** takes the plan's danger (a far, held hull whose plan stands for a rock is borne off
  and her captain woken) beside §4's replay; the pace of a convoy with four held hulls measured
  informatively in `docs/dev/TuningNotes.md` (no pace truth moved).

## 6. The boat's names are the giver's hull's (item 5)

- **To reproduce** from the owner's save (`m7-small-convoy-encounter-all-models.json`, as data; the
  lead holds it): the player's `send the boat to Lynx with the captain and Mr Pearce and ...`, and
  read how each name resolved (`orders/port.py` `_boat_to_ship`: `people.find_aboard`, then
  `people.find`, 84's one registry across hulls) and why the far hulls' people passed
  `Dealings.send_boat_to`'s check (`person.hull != self.hull_id`: my first reading is that the far
  hulls' people, never moved, carry no `hull` of their own and compare equal to a player's hull
  whose id is blank, or `find` returns another hull's "captain" by his role; the save decides).
- **The rule**: the names are resolved among the giver's hull's company (persons whose whereabouts
  or home is the giving hull; the visitors aboard her by name, as 82 built); a person of another
  ship is refused in words ("Captain Owen is of the Chevalier, not of this ship; the boat is not
  sent"), the boat not sent; the `for <persons>` side among the target hull's.
- **The truth's number**: 7-389 was given to 65 in the lead's reading of the owner's notes ("truth
  7-389 (free) takes it", the word heard across hulls), so I do not take it; I ask the lead for a
  number (7-394 is shared by items 3 and 4 already).

## 7. The files, and 65's

Mine by the brief: `agents/remote.py`, `world/seats.py`, `movement.py`'s visitor naming,
`world/hail.py`'s answer path, `docs/agents/Harness.md`, the primer's chapter 26,
`docs/dev/TuningNotes.md`, the tests. **Touches outside them, said first and kept small:**
`agents/harness.py` (65's file, but not its sample or `_reaches`): `ident` in the constructor,
`to_dict`, `restore` and `all_agents`' name, a dozen lines; `orders/stations.py` (65 owns `_say`
only): `_station_in`'s comma rule for a visitor's name, a few lines; `world/crews.py` (no package's
by the brief): the cap's rank and allowance for a held hull, and the far plan's danger check;
`orders/port.py` and `world/dealings.py`: item 5's scope. Nothing of the console's or the browser's
views (65's) beyond what they already read from `Desk.stations()`.

## 8. The order

The five items in the brief's order, each a mergeable state reported at its boundary, the trunk
brought in before each step's final run: 1 (the seat's identity, the desk, the save; 7-390,
7-391), 2 (the visitor's name; 7-392), 3 (the far hull's hail; 7-393), 4 (the cap and the far
plan's danger; 7-394 with 3's replay), 5 (the boat's names; the number the lead gives).

## 9. Open for the lead

1. The save of 11-01 (`boat-between-ships-test`) and the convoy's save, as data, to reproduce item
   1's stand-down of both and item 5.
2. Item 5's truth number (7-389 is 65's by the lead's own reading).
3. `HELD_OVER_CAP` = 2, held hulls ranked with the dealings: the lead's word, or the brief's "or"
   taken the other way (the cap held at three and the far plan's danger alone).
4. The touches in §7 to `agents/harness.py` and `orders/stations.py`, files 65 is working in.
