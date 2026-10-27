# Design note: one world, the player one part of it (package 83)

Written as a study and before anything is built (the brief of package 83 in
`docs/dev/M7-WorkPackages.md`: no code in the repository, the design and the costing first,
the refactor as package 84 on the owner's reading). Decision 52 (`docs/DesignProposal.md`)
is the frame: the world is one world that the player is in and so is everyone else; a
person seated by a model anywhere in it must be able to do at coarse detail whatever the
player can do; the full-detail ship only where the cap gives it and nothing coded out; the
director's reach the world's; the leaders of nations and companies as abstract stationed
roles left room for. The owner's evidence is his debrief on packages 70 to 72 and his notes
2, 9, 11 and 12 (`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/`); his acceptance
test is the decision's: his armed tender, a cutter under a model captain in company with
his frigate, ordered to the next region, through real weather, into a port, ashore to a
person, back with a thing, past a ship the director placed, and home to report it all, the
player none the wiser until the report. The lead's readings in the brief are taken where
the code agreed with them and departed from where it did not, each with its reason.

The note is in the brief's five parts: the world as it is (the seam named, the
player-centric assumptions counted), the world as it should be (the design whole, what a
model at another ship's captain's station sees, the acceptance test walked step by step),
the two roads costed (the code that moves, the pace measured, the pins, the consent brief's
words, what 82, 74, 75 and 77 gain), the migration in steps that keep the suite green
(package 84's brief, drafted in `docs/dev/M7-WorkPackages.md`), and what was found on the
way with the decisions only the owner can take.

## 1. The world as it is: the seam named

### 1.1 What a World holds (`freesail/core/world.py`)

`World.__init__(seed, scenario, ship)` builds **one ship's world around one ship**. Reading
the constructor from the top, the World keeps two kinds of thing on one object, and nothing
in the code tells them apart:

**The world's own** (one of each in a game): the clock (`world.clock`); the seeded streams
(`world.rng`); the chart and its tiles (`world.chart`); the tide table (`world.tide`); the
weather systems and the climatology (`world.systems`); the nations' table
(`world.nations`); the far bodies of the other sail (`world.vessels`, a `ships.Vessels`);
the squadrons' registry (`world.squadrons`, package 72); the business (`world.business`,
43b); the world orders with their ticks and sources (`world.world_orders`,
`_scenario_orders`); the points of interest a `mark:` made (`marks_of_interest`); the
director's brief, budget, seats and log (`director_brief`, `director_state`,
`director_seats`, `agent_journals["director"]`); the build's lineage (`played_under`).

**The one ship's own**, kept beside them with no boundary: her hull and rig
(`world.ship`, a `ship.graph.Ship`; a `PointShip` when the scenario names no file); her
place on the sphere (`world.origin`, `_position`, `_geo_last`; `world.position` is the
World's centre everywhere); the wind at her with her own gust stream (`world.wind`,
`wind_record`, the wind-shift bookkeeping); the sea and her motion (`world.sea`,
`world.motion`, made only when the scenario keeps a sea); the sky and the visibility at her
(`world.conditions`, `_observe_weather` once a minute at `ship_x_km, ship_y_km`); her glass
(`world.glass`); the tide's height and stream at her (`tide_state`, `_tick_tide`); the
ground under her and her anchors' dragging (`world.ground`, `_aground`, `_dragging`,
`_drag_said`); her lookout (`world.lookout`, a `Lookout(chart)` that reads
`height_of_eye(world.ship)` and `world.position`); the sun at her latitude (`world.sun`);
her reckoning (`world.navigation`, a `Navigation(world)`); her places aboard
(`world.places`, `Places(ship.name)`); her people (`world.people`, a `People(world)` built
from `world.ship.extra["crew"]` and her wardroom file); her stations and who holds each
(`world.stations`); her papers (`world.papers`); her hold, purse and stores (`world.hold`,
`world.purse`, `world.stores`); her ports' dealings (`world.ports`, a `Ports(world)`, of
which more below); her fishery (`world.fishery`); her people's needs (`world.needs`); her
book of standing orders and its runtime (`world.standing`); her rules captain
(`world.captain`, a `captains.Captain(world)`); the harnesses at her stations and their
journals (`world.agents`, `agent_journals`); the player's seat (`world.player_seat`); her
log (`world.log`), her journal and inputs (`world.journal`, `world.inputs`), the stations'
acts (`station_acts`); the readings view cached per tick (`_readings_view`); and, since
package 73 is building it, the water in her (`world.water`, a keeper of every World).

**The ship carries the World's per-ship systems back through `ship.extra`**: `rng`,
`motion`, `navigation`, `standing`, `agents`, `agent_journals`, `stations`, `player_seat`,
`crew`, `routine`, `evolutions`, `signals`, `hull`, `quarters`, `magazine`, `morale`,
`struck`, `water`, forty-odd keys in all (`grep -o 'extra\["[a-z_]*"\] = '` over
`freesail/`). The orders' grammar is given the ship and not the World
(`World.submit` → `ship.handle_order(text)` → `orders.handle(ship, text)`), and reaches the
World, where it must, through `prompt.world_of(ship)`. So an order can only ever be an
order of *the* ship of a World, and the readings registry (`api/readings.py`, 4,000 lines)
reads `world.ship` thirty-one times for the same reason.

**The tick** (`World.tick`) runs the two kinds together in one fixed order: the clock, the
scenario's world orders due, the weather followed and the wind stepped, the weather's
minute, the sea and the motion, the tide, **her physics** (`ship.step(1.0, wind)`), her
run on the sphere (`_tick_geo`), **the other sail** (`_tick_vessels`: the business's
minute, then `vessels.tick_crews(world)`, which ticks every crewed ship's whole World
inside this one's tick, then the near bodies, then the far bodies' minute), her action
(`combat.action.tick_action`), her grounding and her lookout (`_tick_chart`), her
reckoning, the ports' tick (her pilot and her boat), her people's tick, her watch routine,
her needs and her fishery once a minute, the bells, the sun, her standing orders, her
captain's judgement, the deck passing by the bill, and her stations' samples. Every pinned
passage's digest is the order of this list.

### 1.2 How a far body lives in it (`freesail/world/ships.py`, `brains.py`, 72's sets)

A ship that is not the player's is a `ships.Vessel`: a dataclass of her identity (id, name,
kind, file, nation, description, colours and flag), her truth (position, heading, speed,
sail state as one of four words, `tack`), her plan (a list of legs: `to`, `to_ship`,
`company`, `station`, `lie_to`, `anchor`, `chase`, `away`, `home`), her state
(`Vessel.state`, the captain's machine's word), her brain (`Vessel.brain`, a
`brains.FarCaptain` when she was given an intent, else nothing and she sails her goal's
legs), her crewed body while promoted (`Vessel.crew`), her dealing with the player
(`dealing_tick`), her fit of guns and the far record of her damage and her colours
(`fit`, `struck`, `damage`, `signals`), whose orders she is under (`under_orders_of`), her
set and her regime (`squadron`, `pace_cap_kn`, `regime`, `sortie`, `commission_tick`),
her fishery (`fishing`), and her short story (`story`: the lines the director's hand
wrote while she had no World, package 62). She is moved once a game minute by
`Vessel.tick`: her polar in the wind at her place (`_wind_at` reads the parent's systems'
surface wind at her plane point, or the world's base wind), the leg's bearing by
`_course_for` with a beat laid in tacks, the tide's stream added, `_arrived` at a cable.

Her brain (`brains.FarCaptain`, a `Judgement` like the player's rules captain) judges once
a minute from `brains.perceive_vessel(world, vessel)`: her own wind, heading and way; **the
World's `conditions`, which are the player's ship's sky and visibility**, and the World's
daylight; the nearest land and the lee shore by the chart from where she is; her anchor;
the nearest port by `world.ports`; and the sail in sight by `Vessels.strangers_of`, which
runs over the parent's vessels **and the player's shadow**. Her business in port is a wait
(`IN_PORT_WAIT_S`, twelve hours) and then under way again; a `trade` or `passage` intent
whose port is reached ends with `vessel.done = True`, "she has gone in and is gone from the
sea" (`FarCaptain._in_port`). Nothing of a far ship buys, sells, waters, lands a person,
reads a price or pays a purse: the business's "trade 80 tons of tin from Falmouth to
Brest" (`business.Business._trader_once`) is an intent in words with a cargo in words, and
"no price is moved by what is carried" (43b). The one far act that has the same effect at
both details is the fishing of package 56: `fishing.far_work` runs the same catch function
on the far body, and `land_far` sells the catch at the port's fish quay into the business's
record (`Business.drawn[].landed`), not into any purse.

**The player's ship is not a vessel of the sea.** To every brain, set and action she is
`PLAYER_ID = "the ship"`, defined three times over (`brains.py`, `squadrons.py`,
`combat/action.py`) and rebuilt each minute as a shadow `Vessel` by
`Vessels.player_shadow(world)` from `world.ship`, `world.position`, the manoeuvre in hand
and her locker (`signals.player_locker`). The shadow is never in `world.vessels`; it is
appended by `CrewView.vessels` and `strangers_of`, found by `squadrons._body(world, vid)`
and `combat.action._body_of`, and special-cased by `_frame_of`, `_velocity_of`, the sets'
commander rules (`if self.commander == PLAYER_ID`, nineteen places in `squadrons.py`) and
the action's firer and mark (eight in `action.py`). The sets (`squadrons.Squadrons`, one
brain at far detail) and the regimes (`regimes.minute`) are the World's and tick in the
far bodies' minute (`Vessels.tick`); the business (`business.Business`) is drawn in the
region `chart.region_at(world.position)` and **follows the player's ship** across the
regions' edge (`Business._follow`), a ship beyond the edge kept only within
`carry_over_nm` of her.

### 1.3 What the promotion builds (`freesail/world/crews.py`)

Within `CREWED_NM` (four miles) of `world.position`, under the cap (`CREWED_CAP` three;
`crews.settings` from the scenario's `crewed:` or the drivers' flags), `crews.switch` once
a minute promotes a vessel with a brain to a **`CrewedWorld`**: a subclass of `World`, a
second World made by `World.__init__` from `_crew_scenario(parent, vessel)`, which is the
parent's scenario with these fields replaced: her position, heading, way and the wind at
her; `systems=[]` and `climatology=False` (she follows the parent's systems through
`_follow_weather`); `background={}`, `glass=False`, **`sea=False`** (so she has no `sea`
and no `motion`), `sky=None`, `chronometer=None`, `current=None`; `nation` hers;
**`people=[]`, `papers={}`, `cargo={}`, `ports=[]`, `ships=[]`, `world_orders=[]`,
`books=[]`**; `intent` hers, `fit` hers; and `squadrons=[]`. So her World has: its own
`Clock` starting at **tick 0 at the promotion** (her log's ticks, her held orders and her
budget counts are converted at the seam, `_hand_crewed`, `FarCaptain.fold_in`); its own
`Rng` seeded `(parent.seed * 1009 + crc32(id)) % 2**31`; its own `Log`; the chart loaded
by name (the tiles shared); its own tide table and `tide_state` at her place; its own
`Ground`; its own `Lookout`; the parent's `conditions` (the sky and the visibility at the
**player's** ship, `_tick_weather_minute`); the wind at her own place; her `Navigation`
(the account set at her truth with half a mile's doubt); her `Places`, her `People` built
from **her own muster and wardroom file** (so she has her captain and her officers as
named persons); her `Stations`; empty `Papers`; a `Hold` with no cargo and a `Purse` of
nought; `Stores` from her file; her `Fishery`; her `NeedsKeeper`; a `Runtime` with no
book; her `Captain` with the brain's state folded in (`FarCaptain.fold_in`: the intent,
the role and doctrine, the state whose book he loads, the stranger in hand, the sails
spoken, the signals recognised, the pirates, an order over his head); her `agents` and
`agent_journals` (the station seated on her); and `self.vessels = CrewView(self)`, a view
of the parent's vessels but herself with the player's shadow appended, moving nothing. Her
signal locker is her far body's (`vessel_locker`, one object for the two bodies, package
71). `attach_crew` musters her company from her own `rng.stream("muster")`, so she gets
the same men at each promotion, fresh. She has **no ports** (`Ports._load` with
`wanted=[]` loads none), **no business, no director, no sets of her own** (an empty
`Squadrons`), none of the world's persons ashore and none of the things.

**The mirror** (`crews.mirror`, every tick from `Vessels.tick_crews`): her position, heading
and speed into the far record; once a minute her sail state as one of four words
(`_sail_state_of`) and her captain's state into `Vessel.state` and the brain's history.
Nothing else crosses: not her damage (70 writes `Vessel.damage` only from the far fight's
measure, `combat/far.py`, and `Vessel.struck` from `action.strike`), not her casualties,
her stores, her water, her purse, her hold, her people's places, her book.

**The demotion** (`crews.demote`, beyond `CREWED_DEMOTE_NM` or when she enters one of
`_NOT_CREWED_STATES`: at anchor, in port, running for shelter, in distress): the mirror,
`FarCaptain.fold_back` (the state, the trend, the stranger, the sails spoken, an order over
his head), and then **her World is dropped** (`vessel.crew = None`) unless a station is
seated on her, when it is kept in the **far shape** (`CrewedWorld.shape = "far"`): the far
body moves her, `far_tick` mirrors the body into her ship's `dyn` and her account each
second, her lookout looks once a minute, her agents are sampled, and `submit_far` works
the eleven `FAR_SHAPE_WORDS` on the plan (a course shaped or steered, heave to and fill
away, give chase and haul off, make and shorten sail as a state, anchor and weigh, the
station kept) and 71's colours and signals, answers the readings and the conversation
through her grammar, and refuses everything else in words (`FAR_SHAPE_REFUSAL`). What the
drop loses: her log (spec M7b §12b wants it kept), her damage and her dead, her water and
her stores, her purse, her book, her people's states, needs and places. **A vessel at
anchor or in port is never crewed** ("the port's business is the player's ship's machinery
and the far brain's wait", the module's head, the lead's judgement of 43 and 43b).
`crews.station_world` (a seat on another ship) makes her World full if she is within the
range and the cap has room **without reading her state**, so the owner's tender at anchor
in Torbay is crewed for a minute and demoted to the far shape at the next switch.

**The director's hand** (`crews.hand`, package 62): `ship "X": order <words>` goes through
her World's `submit` as her captain's when she is crewed, through `submit_far` when a
station keeps her World in the far shape, and through `far_order` on a `_FarBody` (her
vessel and the parent's sea) when she has no World, the line kept in `Vessel.story`. The
hold (a glass, a span or an event) crosses the promotion both ways. This and the forms that
name a ship (`ship "X": intent`, `crewed`, `under the orders of`, `in ordinary`,
`commissioned`; `squadron "X": join | detach | recall`; `seat:`) are the whole of the
director's reach into another ship.

### 1.4 How a station's harness, the doors and the seats bind to a World

A `agents.harness.Harness` is made for a World (`Harness.world`) and samples that World's
readings, log and people; `harness.all_agents(world)` walks the parent's `agents` and then
each crewed vessel's `crew.agents`, naming the latter "captain of <ship>"; the pace rule
(`open_samples`), the unattended check, the desk's listing and lockstep walk the same list.
The desk (`agents/remote.py` `Desk.station`) takes a `ship` in the body and seats the
station in **her World** by `crews.station_world`, the seat keyed `<ship>/<station>`
(`seat_key`); the API door, the MCP bridge and the local runner carry `--ship`. The
director's seats (`world/seats.py`, package 67) are keyed `<id>` for her captain,
`<id>/<station>`, `own/<station>` and `voice/<station>`; the harbour starts the API door
with `--ship` for a seat held (`Harbour.tend_seats`). **A person aboard another ship is
refused** at the seat ("no other ship has a World of people to bind him in", 67) and at
the making (68's R-15). The station's own line (`readings.station_line`) reads
`world.people.effective_place`, the stations held and the needs **of the World the station
is in**; hearing (`world/hearing.py` `spot_of`, `people_hearing`) compares spots within one
World's `People`, so a person ashore at Falmouth from the tender's World and the player's
Mr Gill ashore at Falmouth never hear each other, though their spots are equal.

### 1.5 How the replay and the save rebuild it (`freesail/core/replay.py`)

`World.save()` carries one `ship_ref`, the parent's `journal` and `inputs`, the parent's
`agents` (their transcripts) and `stations`, the `world_orders`, the `director` block. A
crewed World's `submit` journals into **her own** `inputs` and `journal` (`World.submit`
appends to `self.inputs`), which the save never sees; so a game with a model captain of
another ship replays by its journal with her re-promoted deterministically (the seed, her
id, the tick the switch promotes her) but **none of her captain's orders given again** (43
left it: "a save of such a game replays the parent's stations only"). The checkpoint
(`checkpoint_bytes`, `_Pickler`) pickles the whole object graph, the crewed Worlds inside
the parent, and `_rebind` recurses into each `v.crew` (58a's find: two crewed at once once
rebound each other without end); `_Unpickler.find_class` admits the game's own classes by
module and name, so **a checkpoint written before a refactor is read only while the
classes it names still exist with those names** and loads with class defaults for fields
it lacks; else `load_report` falls back to the replay road, and
`tests/fixtures/saves/` keeps three old checkpoints as tests of the load. `acts.give`
replays a station's acts by station name within one World.

### 1.6 How the pace rule and the cap centre on the player's ship

`Pace.rate()` (`ui/console.py`) is 1 while `open_samples(world)` names any station's sample
open, on any ship; the World's tick is untouched. The cap's centre is `world.position`
(`crews.switch`, `station_world`, `ask_crewed`, `far_no_way`), so "near" means near the
player, and a seated captain's own ship is promoted or demoted by her distance from him.
The floors (`tests/conftest.py`, `tests/test_known_truths.py`): `BUILD_MACHINE_FLOOR` 500
ticks a second in truth 51's form (the frigate alone, a thousand ticks to settle, the best
of three thousands), asserted by the five truth-51 measures and by 7-159; and
`crews.CREWED_FLOOR_TICKS_S` 60 with the cap full (truth 88, 7-138, 7-151, 7-160). The
pace tests carry the `pace` marker and run alone, last. `tools/pace.py` measures the
frigate alone, with the dozen far, with one, three, six and twelve crewed Worlds, and the
convoy of six; the owner's baseline is 95 ticks a second with twelve crewed ships on his
machine (1,111 alone).

### 1.7 The player-centric assumptions, one by one

The count is the study's first finding, as the brief asked. Counted by kind, each one a
thing the code assumes about a single ship at the World's centre, with the file and the
object; the method and the raw figures are in 1.8.

*The World's shape*

1. A World is built around one ship: `World.__init__(seed, scenario, ship)`,
   `api.session.make_world`, `scenarios.make_scenario_world`; a `PointShip` when none.
   `world.ship` is read 223 times in 33 files.
2. `world.position` is her position and the world's centre, 55 reads: the chart's bounds
   check at the start, `Business.start` and `_follow`, `crews.switch`, `Vessels.
   _promote_and_hail`'s near-detail switch, `systems.locate`, the tide at her, the lookout,
   the pilot's reach (`Ports.in_port`, `nearest`), the sights, `truth(within=)`.
3. The weather, the sea, the motion, the sky and the visibility, the glass, the tide's
   state, the ground and the sun are the World's at her place: one ship's weather per
   World (`_tick_weather`, `_tick_sea`, `_tick_motion`, `_observe_weather`, `_tick_tide`).
4. The per-ship systems are reached from the ship object through `ship.extra`, and the
   grammar is given the ship (`orders.handle(ship, text)`, `prompt.world_of(ship)`): an
   order is an order of the World's one ship.
5. `world.log` is her log and the world's in one list with one digest (a ship put on the
   sea, a system appended, a price moved, and her deck's lines together); a crewed ship's
   log is another World's and is dropped at her demotion.
6. `world.people` is her company **and** the persons of the world (a pilot, a person made
   ashore by `person: make`, the things in `People.things`); the registry of the world's
   persons is the player's ship's registry, built from `world.ship.extra["crew"]`.
7. `world.ports` (`Ports`, 4,270 lines) holds the ports' files (the markets, the stances,
   the blockades, the tracks, the yards and the pools: the world's) and her dealings (the
   pilot and his conn, the cutter, the boat and its errands, the jobs, the price lists held,
   `lay_in`: hers) in one object; `Ports.ship_nation` is the scenario's or her file's, and
   `Ports.stance(port)` is the port's stance to *her*.
8. `world.hold`, `purse`, `stores`, `papers`, `fishery`, `needs`, `standing`, `captain`,
   `stations`, `places`, `navigation`, `lookout`, `water` (73): hers, on the World.
9. There is one clock, and a crewed World's clock starts at tick 0 at her promotion
   (`_crew_scenario` sets `start_time` to the parent's now; `Clock.tick` 0); the seam
   converts (`_hand_crewed`, `fold_in`, `fold_back`), and her log's ticks are not the
   world's.
10. The squadrons, the business, the world orders, the marks and the director live on the
    player's World alone; a crewed World gets an empty `Squadrons`, no `Business`, no
    director, no `world_orders`.

*The far bodies and the brains*

11. The player's ship is a shadow, not a vessel: `PLAYER_ID = "the ship"` three times
    over, `Vessels.player_shadow`, 66 special cases in nine files (the sets' commander
    rules, the action's firer and mark, the brains' hail, the station leg's frame, the
    signals' `own_id`).
12. Every far captain anywhere on the chart perceives the **player's** sky and visibility
    (`perceive_vessel` reads `world.conditions`).
13. A far ship's business in port is a wait and a trade intent ends by her leaving the sea
    (`FarCaptain._in_port`, `IN_PORT_WAIT_S`): no far ship buys, sells, waters, goes
    ashore, reads a price or pays; the business's cargo is words.
14. The business's region is the player's (`Business.region`, `_follow`, `_carried_over`).
15. A vessel's dealings, her hail and her letter are with the player's ship only
    (`_promote_and_hail`, `hail.player_hailed`, `Vessel.letter` "for the ship",
    `Vessel.alongside`).
16. A far ship has no log; `Vessel.story` holds the hand's lines alone (62).

*The promotion*

17. A promoted ship is a second `World` (`CrewedWorld(World)`): a second clock, rng, log,
    chart, tide, ground, lookout, people, stations, ports registry, needs, standing runtime,
    captain, and the mirror between the two bodies. This is the seam.
18. `_crew_scenario` cuts the world out of her World: no ports, no persons of the world, no
    things, no papers, no cargo, no books, no sea and no motion, no glass, no sets, no
    business, no director. The tender's "no port in the world" is
    `movement.go_ashore`'s "There is no shore within a boat's pull: the ship is not in a
    world with ports" (and, in the far shape, `FAR_SHAPE_REFUSAL`).
19. The switch's centre, range and cap are the player's (`crews.switch`, `settings`,
    `station_world`, `ask_crewed`); `shape_words` tells a seated captain she is "beyond the
    range of the player's ship".
20. A ship at anchor, in port, running for shelter or in distress is never crewed and is
    demoted when she comes to one (`_NOT_CREWED_STATES`), because the port's business is
    the player's ship's machinery; `station_world` does not read the states, so a seat on
    a ship at anchor is crewed for a minute and then demoted to the far shape.
21. The demotion drops her hull's state: her damage, her dead and wounded, her stores and
    water, her purse and hold, her people's places and needs, her book, her log, her
    journals (`demote`; `mirror` carries position, heading, speed, sail state, the brain's
    state and nothing more).
22. The promotion re-makes her from her file each time (`make_ship`, `attach_crew` from her
    own muster stream, `_set_sail` from one of four words): the same men, fresh, with no
    memory of the last promotion.
23. A crewed ship's lookout sees the parent's far bodies and the player's shadow, never
    another crewed hull (`CrewView`); two crewed ships in action find each other's bodies
    through `parent` (`action._body_of`), and a crewed ship's own body is left out of the
    sail she watches.
24. Her weather is the parent's systems' wind at her place but the **player's**
    `conditions`; she has no sea and no motion, so `action.firer_state` reads a roll of
    nought for a crewed firer (`roll_deg` from `world.motion`, None), where the player's
    gunnery is scattered by the sea.
25. The director's `aboard:`, `person:`, `say as`, `message:` and the transactions act on
    the player's World (`orders._aboard` on `world.ship`, `world.stores`, `world.purse`;
    `_make_person` and `_move_person` on `world.people`; `_hearers` on the player's
    stations and people; `people.message_aboard` to the player's captain); only the hand
    and the forms that name a ship reach another.

*The stations, the doors and the seats*

26. A harness is bound to a World (`Harness.world`), and a station on another ship lives
    in her World, keyed `<ship>/<station>`; `all_agents` and `open_samples` walk the
    parent's and then each `crew.agents`.
27. A seat at a person aboard another ship is refused for want of a World of people (67);
    a person made aboard another ship is refused (68, R-15); `person: "X" comes aboard` is
    aboard the player's ship.
28. A seated captain of a far ship works the eleven far-shape words and nothing else
    (`submit_far`): he cannot go ashore, trade, speak to a person ashore, take a thing,
    send a boat, water or victual, however coarse the act.
29. Hearing compares spots within one World's `People` (`hearing.spot_of`,
    `people_hearing`), and a word ashore is heard "at the same place of the same port" only
    among persons of one registry.
30. The briefs' words: the consent brief says "the ship" of a station's ship, and already
    "a captain, who commands a ship, the player's or another in the same world" (3.5 reads
    it); the station briefs and the harness's notices say "the player's ship" (`agent.py`,
    `crews.shape_words`, `seats.py`'s eleven "the player's ship" words).

*The replay and the save*

31. The save carries one `ship_ref`, the parent's journal, inputs, agents and stations; a
    crewed World's inputs and transcripts are in the checkpoint alone.
32. The checkpoint pickles the crewed Worlds inside the parent and names today's classes;
    `tests/fixtures/saves/` holds three old checkpoints the load must still read.
33. A pinned passage with a crewed ship in it depends on the tick she was promoted at (her
    rng and her clock are seeded there), so the pins with crewed ships (the two stranger
    trials, the first action, the encounter, 7-155's promotions, 7-160) move with any
    change in *when* a ship is crewed.

*The drivers and the pace*

34. The console's prompt is the captain of `world.ship`; the server's `state()` and the
    chart's drawing read `world.ship`, `world.navigation` and `world.chart_marks`; there is
    no `follow` (82's §11).
35. The pace floors and `tools/pace.py` are measured with the player's ship as the centre
    and the crewed Worlds beside her; the crewed floor is "with the cap full".
36. The cap is one for the world, a setting of the scenario or the flags, centred on the
    player (`crews.settings`).

*The director's truth*

37. `readings.director_readings`: the player's ship first by name with her purse, cargo and
    state; `within` from her; the other ships' guns, damage and people only while crewed at
    full detail; a far ship's story is not in it; `_own_state_truth` is hers alone.
38. `truth(ports=)` and the markets are one registry (right), but their dealings (the
    price lists held, the boat, the lighter's jobs) are the player's.

Thirty-eight by kind; the lead's instinct in the brief ("the World's construction assumes
a ship in several places") is a large understatement, and the owner's note 11 ("strongly
reorient the current implementation of the world so that it generalizes beyond the
player") is the right reading.

### 1.8 The count's method and the raw figures

A throwaway script in the scratchpad (`count_assumptions.py`, described here so that the
count can be made again) counts seven patterns over `freesail/**/*.py`: `ship` (`world.ship`,
`parent.ship`, `self.world.ship`), `centre` (`world.position`, `parent.position`), `player`
(`PLAYER_ID`, `_player_id()`, `"the ship"` compared as an id), `shadow` (`player_shadow`),
`parent` (`.parent`), `crew` (`v.crew`, `vessel.crew`, `crew.shape`, `crew is None`), and
`words` ("the player's ship" in strings and comments). On the head `908741f`:

| pattern | hits | files | the five heaviest files |
|---|---|---|---|
| `ship` | 223 | 33 | `ports.py` 31, `api/readings.py` 31, `reckoning.py` 23, `agents/tools.py` 18, `captains.py` 17 |
| `centre` | 55 | 11 | `ports.py` 21, `sights.py` 6, `reckoning.py` 5, `crews.py` 4, `ships.py` 4 |
| `player` | 66 | 11 | `squadrons.py` 19, `ships.py` 12, `combat/action.py` 8, `orders.py` 7, `brains.py` 5 |
| `shadow` | 16 | 9 | `ships.py` 3, `hail.py` 3, `crews.py` 2, `squadrons.py` 2, `signalling.py` 2 |
| `parent` | 45 | 13 | `crews.py` 15, `remote.py` 5, `ship/schema.py` 5 (the part graph's, noise), `graph.py` 4 (noise), `queries.py` 3 |
| `crew` | 120 | 30 | `crews.py` 38, `ships.py` 10, `evolutions/runner.py` 9 (the muster, noise), `orders.py` 8, `squadrons.py` 8 |
| `words` | 71 | 17 | `seats.py` 11, `ships.py` 8, `orders.py` 8, `crews.py` 6, `director.py` 6 |
| all | 596 | 59 | |

The noise: `.parent` in `ship/schema.py`, `graph.py`, `parts.py`, `physics/sails.py`,
`orders/verbs.py` and `evolutions/scripts.py` is the part graph's parent (sixteen hits),
and `.crew` in `evolutions/runner.py`, `orders/crew.py`, `crew/victuals.py`, `people.py`,
`places.py`, `needs.py` and `ship/parts.py` is the muster (`ship.crew`, about twenty-five).
Net of it, **some 555 reads in about fifty files** stand on the thirty-eight assumptions.
Of the 223 `world.ship` reads, most are *right* under either design (a reading of her
helm, a part by name, a sail set) and want only that "the World" they are given be the
hull's view; the ones that move are those that take the World's one ship for the player's
(the truth, the shadow, the business, the ports' dealings, the hearing, the seats) and are
named in part 3.

### 1.9 The owner's acceptance test walked on today's code

The frigate Amazon lies in Torbay, the cutter Raven her armed tender in company (71's
`under the orders of the ship`, or a set of 72's), a model seated as the Raven's captain by
`seat: <model> as captain of Raven for 40 samples` (the owner's `m7-cutter-tender-test`
save).

1. *The seat.* `station_world` makes the Raven a `CrewedWorld` at full detail (she is
   within four miles and the cap has room), her clock at tick 0, her log new; at the next
   minute `switch` reads her state `at anchor` in `_NOT_CREWED_STATES` and demotes her to
   the far shape with an urgent line. The model's first sample says she is "at far detail,
   beyond the range of the player's ship" (`shape_words`), which is false in words (she is
   two cables off) and true in effect.
2. *The order to the next region.* The player signals her (71) or hails her; the hoist is
   read by her lookout in `far_tick`, her brain standing aside because a model holds her
   (`FarCaptain.tick` returns when `near.seated`). The model orders `weigh` and `shape a
   course for Plymouth`: `far_order` lays `[("to", Plymouth's road)]` as **one straight
   leg with no land guard** (`vessel_from_spec`'s `land_crossing` is run at a vessel's
   making and by the business, not by the far shape's order), so from Torbay she steers
   across Berry Head or the Start if the line crosses them. The business, whose region is
   the player's, draws nothing where she goes.
3. *Through real weather.* The far body sails by her polar in the parent's systems' wind at
   her place, reefs over thirty knots and lies to over forty-five by `_state_for`; the sky
   and the visibility in her readings are the frigate's in Torbay; she has no sea state,
   no glass and no gale book; the model has her wind and her account.
4. *Into a port.* `come to an anchor` where she is; no pilot, no track in, no tide's
   window, no "in port" business: the far body's `("anchor", "")` leg rides head to wind.
5. *Ashore to a person.* `go ashore`: the far shape refuses it ("not one of the far shape's
   orders"); forced crewed (the owner's hotfixed "Raven at full detail" saves), `go
   ashore` answers "There is no shore within a boat's pull: the ship is not in a world
   with ports" (`movement.go_ashore`, her `ports.ports` empty). **The journey breaks
   here**, as the owner's note 2 says.
6. *Back with a thing.* The person and the thing the director made ashore at Plymouth
   (`person: make "Mr Gill" ... ashore at Plymouth`, `aboard: a sealed packet, in the
   keeping of Mr Gill`) are in the **Amazon's** `People`; the Raven's World has no Mr Gill
   and no packet; `give`, `take` and `say to` find nobody.
7. *Past a ship the director placed.* `ship: a French lugger "Renard" of France at <place>,
   cruising` goes into the parent's `vessels`; the Raven's far body perceives her through
   `strangers_of`; neither is crewed unless within four miles of the *Amazon*; the far
   fight is not wired (74); they pass, or the Raven's model orders `give chase` to hailing
   distance and nothing follows.
8. *Home to report.* Back within hail of the Amazon she speaks by `say` (four cables) or
   by signal; her World's log, kept in the far shape because a station is seated, holds
   her orders but not her voyage (no port lines, no person, no thing); the player's log has
   what his lookout saw. The report is the model's words and nothing of the game's record
   stands behind them.

Steps 2 to 4 are coarse and partly true; 5 and 6 are false; 7 and 8 are true by accident
of the far body's limits. The design in part 2 makes each step a thing the world does.

## 2. The world as it should be: one world, many crewed hulls

### 2.1 The design in one paragraph

**One `World` holds the world and the hulls hold the ships.** The World keeps what is one
of in a game: the clock, the seeded streams, the chart, the tide table, the weather, the
nations, the ports (their files, markets, stances, blockades, tracks, yards and pools, and
who is found at each place ashore), **the persons of the world and the things** in one
registry, the far bodies of every ship **the player's among them**, the sets and the
regimes, the business, the world orders and the marks, the director and the offices (the
leaders' roles, 2.10). A ship that is or has been at full detail has a **`Hull`**, kept in
`world.hulls`: her part graph, her company and her muster, her places aboard, her stations
and their holders, her hold, purse, stores and papers, her reckoning, her lookout, the
wind, sea, motion, sky, glass, tide and ground **at her place**, her book of standing
orders and its runtime, her rules captain, the harnesses at her stations and their
journals, her log, her needs, her fishery, her water (73), her signal locker, her dealings
with the ports (her pilot and his conn, her boat and its errands, the price lists she
holds, her jobs). Everything the World keeps of one ship today becomes the Hull's, and the
player's ship is one hull like the others, the hull the game **follows** (`world.followed`,
82's §11). A hull has a **physics switch**: *awake*, her parts stepped by the physics every
tick, her evolutions run by her hands, her lookout looking, her captain's book judged, as
a crewed World is ticked today; or *asleep*, her far body moved by the plan at the minute
as a far ship is moved today, her parts, people, stores, water, damage, purse and log kept
and untouched, her needs and her people's minute ticked coarsely. The cap's business is
**which hulls are awake**, by the same rule as now (the nearest to the followed hull first,
a ship in dealings before a nearer one that is not, a stationed hull before an idle one),
and nothing is ever dropped at the switch: the promotion is a hull woken, the demotion a
hull put to sleep. A ship that has never been at full detail has no hull and is a far body
with a short story, as now, until the cap wakes her, a person is seated on her, or **an act
of hers needs a hull** (a person goes ashore from her, she trades, a thing is given aboard
her), when her hull is made from her file at her truth once and kept. **The acts of a
person are the world's acts, not a World's**: going ashore is the port's job on the person
by his hull's boat or a waterman, being ashore is a place in the one registry of persons,
hearing is by spot in that registry, a thing is in it, trading is the market's transaction
on the hull's purse and hold whether her physics sleeps or wakes, the pilot and the track
in and out are the port's jobs on the hull; so a person anywhere can go ashore, trade,
speak, take a thing, anchor, sail for a port, chase and report **at coarse detail from a
sleeping hull**, and the full surface comes beneath the same station when she wakes. The
consumers of a World today (the grammar, the readings, the harness, the captain, the
standing runtime, the ports' dealings, the needs) are given the hull, which answers to the
same names, so that the orders' 3,600 lines and the readings' 4,000 move not at all and
the thirty-eight assumptions are retired at the seams where they live. One clock, one rng
with the hulls' streams named by hull, one journal with the hull named on each input, one
checkpoint of the one World, a log per hull kept in the save.

### 2.2 The pieces

**`freesail/core/world.py`: `World`, the shared.** Keeps: `clock`, `rng`, `chart`, `tide`,
`systems`, `nations`, `ports` (the world's half of today's `Ports`, 2.4), `people` (the
one registry of persons and things, 2.3), `vessels` (every ship's far body, the player's
included, 2.2 below), `squadrons`, `business`, `world_orders`, `marks_of_interest`, the
director (`director_brief`, `director_state`, `director_seats`, the director's journal),
`offices` (2.10), `hulls` (`dict[id, Hull]`), `followed` (the hull the drivers and the cap
centre on), `journal`, `inputs`, `station_acts`, `played_under`, `chart_marks`,
`compression`. Its `tick` runs **in two phases, in the order today's tick has them**:
the clock, the world orders due, the weather's minute (the systems advanced once, not per
hull); then *the bodies move*: every awake hull's wind, sea, motion, conditions, tide,
physics and run on the sphere, the followed hull first and the rest by hull id; then *the
world sees and acts*: the other awake hulls' action, grounding and lookout, reckoning,
dealings, people, routine, needs, fishery, water, bells, sun, standing, captain, watches
and agents (as a crewed World's whole tick runs today between the player's run on the
sphere and his lookout), the far bodies' minute (the business, the brains of the sleeping
and hull-less ships, the sets, the regimes, the moves, the hails, **the switch**), the
sleeping hulls' minute (their people, needs, water and dealings coarsely), the ports'
jobs, the offices' day, and **the followed hull's own seeing and acting last**, as the
player's run after `_tick_vessels` today. The order is chosen so that every line of the
followed hull's log and of a crewed ship's falls at the tick it falls at today; part 3
says which pins that keeps and the one step that proves it.

**`freesail/world/hulls.py` (new): `Hull`, the ship.** Owns every per-ship field 1.1
lists, the methods that work them (`submit`, `record`, `readings`, the `_tick_*` of her
own systems, `state`, `summary_lines`) and a `world` back-reference, and **exposes the
World's shared fields as properties** (`hull.clock`, `hull.rng`, `hull.chart`, `hull.tide`,
`hull.systems`, `hull.nations`, `hull.ports`, `hull.people`, `hull.vessels` (a view like
today's `CrewView`: every far body but her own, moving nothing), `hull.squadrons`,
`hull.business`, `hull.world_orders`, `hull.director_*`), so that a consumer written
against `world.<name>` reads the same name on a hull. This is the façade the whole
migration stands on: `CrewedWorld` is a World that *copies and empties* the shared things;
`Hull` is a ship that *delegates* them. `Hull.awake` is the switch; `wake()` sets her
sail from the far words and folds her brain in (`_set_sail`, `FarCaptain.fold_in` as now);
`sleep()` mirrors her truth into the far body and folds the brain back (`mirror`,
`fold_back` as now) and stops her physics; neither makes or drops anything. A hull's
streams are the World's rng's, named by her id (`rng.stream(f"{id}:muster")`), the
followed hull's unprefixed so that the player's draws are what they were. Her `log` is her
own (`hull.log`) and the World's log is the followed hull's for the drivers (`world.log` a
property) until 82's observed world wants a log of the world's own events; **a hull's log
is never dropped**, which is §12b's "a crewed ship that demotes keeps her log" and the
ground of `read_log ship=`.

**`freesail/world/ships.py`: `Vessel` and `Hull` one identity.** `Vessel.crew` becomes
`Vessel.hull` (None for a ship with none); `Vessel.detail` gains the word `asleep`. **The
player's ship is a `Vessel` of the sea** made at the World's start from her file's
description, under the id the save and the signals know (`PLAYER_ID`, kept as the followed
hull's vessel id for the old saves' sake and defined once, in `ships.py`), in
`world.vessels` with the rest; `player_shadow` is retired and `strangers_of(viewer)` leaves
the viewer's own vessel out, as `CrewView` does today. The mirror runs for every awake hull
(`Vessels.tick_hulls`), so the lookouts, the brains, the sets and the action read one list
of bodies and the sixty-six special cases of `PLAYER_ID` become one rule: a vessel with a
hull awake is read from her hull, else from her record. `Vessel.story` stays the log of a
ship with no hull and becomes her hull's log's first lines when a hull is made.

**`freesail/world/crews.py` becomes the switch and nothing else.** `switch` (the cap's
rule over `world.hulls` and `world.vessels`, centred on `world.followed`), `wake`,
`sleep`, `make_hull` (a hull from her file at her truth: today's `CrewedWorld.__init__`
less the scenario copying), `hand` (the director's hand, now one road: `hull.submit`
awake, `far_order` on her far body asleep, the hull's log either way), `ask_crewed`
(`ship "X": crewed` wakes her; the cap's order stands), `station_world` retired for
`hull_for(world, words)` (make or find her hull, wake her if the cap allows, else leave
her asleep with the station on her). `_NOT_CREWED_STATES` is retired: a hull at anchor or
in port may be awake (the port's business is the port's now), and the owner's bound on it
is an open decision (part 5). `CrewedWorld`, `CrewView`, `far_tick`, `mirror_far`,
`_crew_scenario` and `_to_full` go; `FAR_SHAPE_WORDS` stays as the sleeping hull's words
for the plan, widened by the person's and the port's acts (2.5).

**`freesail/core/replay.py`.** One journal: each input carries `"hull": <id>` (absent for
the followed hull, so every old save reads as it did) and `_give` submits to that hull;
the save carries `"hulls": {id: {ship_ref, agents, stations, standing_orders, log}}` for
every hull but the followed one, whose fields stay where they are; `acts.give` takes the
hull by the act's station key. A replay re-makes a hull where the journal or the switch
made her (the far record's file and her truth at that tick are deterministic from the
seed) and gives her inputs again at their ticks. The checkpoint pickles the one World as
now; `_rebind` walks `world.hulls` once each; `World.__setstate__` converts a checkpoint
from before the refactor (the per-ship fields lifted into a followed `Hull`, a
`CrewedWorld` found on a vessel lifted into a hull of the same id), so that the three
fixture saves and the owner's saves load by the checkpoint road as now.

### 2.3 A person of the world

Today's `People` does two jobs: the company of one ship (built from her muster and her
wardroom file) and the registry of everyone named (the pilot, a person made ashore, the
things). The design keeps **one registry on the World** (`world.people`, the class kept)
and gives every `Person` a whereabouts that is the whole truth of where he is: `aboard`
the id of the hull he is in (None ashore or in a boat), `port` and `ashore_at` as now when
ashore, `boat` the hull whose boat he is in, and a **home**: the hull he belongs to by his
station or his muster (`Person.ship`), so that `come aboard` knows whose boat to send and a
prize crew's men (74) know whom they left. The hull's company is a view (`hull.company`:
the persons whose home is her, wherever they are; `hull.aboard`: the persons in her now,
hers or not), built when her hull is made from her muster as `People._build` builds it
today, and the muster's counts stay the hull's (`ship.extra["crew"]`). The things stay in
the registry (`world.people.things`), a thing's `keeper` any person of the world and its
`place` any hull's place or any port's. Hearing's spot (`hearing.spot_of`) becomes
`("aboard", hull id, place)`, `("ashore", port, place)` or `("boat", hull id)`, and
`within_hearing` compares them as it does: two persons at the market at Plymouth hear each
other whichever hull brought them. The needs (`NeedsKeeper`) are kept per hull over her
company and tick for a sleeping hull at the minute (a keeper's tick costs nothing the
measure can see, 3.3). A person seated by a model is a person of the registry at a station
of some hull (or of an office, 2.10); **a seat at a person aboard any hull** is the same
`seat:` as today with the hull named, 67's refusal lifted, and a person moving between
hulls (82's boat, 73's boarding, 74's capture) changes `Person.aboard` and nothing of his
station, which follows him (the station is bound to the person; the hull under the station
changes; 82's builder decides the seat's words from this ground).

### 2.4 The ports as the world's, and a hull's dealings

`world/ports.py`'s 4,270 lines are two things in one class, told apart by which fields a
method reads. **The port's** (`Ports`, the World's): `ports` and `_load`, the port files
and their state (`Port`, `Market`, `Dockyard`, the pools, `Spot`, the tracks, `PilotSpec`),
`stance(port, nation)` (the nation an argument, not `ship_nation`), `blockades`,
`watched_by`, `nearest(pos)`, `in_port(pos)`, `find`, `price_of`, `demand`, `recover`,
`news_words`, the places ashore and who is found there (`places_lines`), `trade_together`,
and the jobs of every hull (`jobs`, `_apply_job`, keyed by the hull they are for). **The
hull's** (`Dealings`, new, one per hull): the pilot and his conn (`pilot`, `pilot_port`,
`pilot_since`, `conn_*`, `_tick_pilot`, `give_conn`, `take_conn_back`, `answer_pilot`,
`_hail*`, `_waits*`), the cutter sent for her (`cutter_*`, `_launch_cutter`), her boat
(`BoatState`, `_send_boat`, `send_boat`, `boat_phase`, `_boat_back`, `boat_reading`,
`boats_words`, `land_person`, `fetch_person`, `waterman`, `_passengers`, `_people_back`),
the price lists she holds (`price_lists`, `_write_price_list`, `prices_reading`),
`lay_in`, `declined_until`, her `trade` and `trade_list` (the market's transaction on
*her* purse and hold), `enter_hands` and `_muster_recruits` (the pool into *her* muster),
`craft`. `Ports.tick` runs the jobs for every hull; each awake hull's tick runs her
`Dealings.tick` (the pilot's minute, the boat kept); a sleeping hull's dealings tick at the
minute too, since a boat's pull and a lighter's load are jobs with a time and want no
physics. A trade by a sleeping hull is the same `Dealings.trade` with the lighter's job;
and a far ship of the business that reaches her port with a `trade` intent **transacts**
by it instead of vanishing (`FarCaptain._in_port` sells her cargo and buys the return
cargo at the market's price by the code the player's trade uses, against a hull made for
her purse and hold, or, the owner's cheaper choice in part 5, against the market alone with
no hull), which is "the business's own means" the brief names and the first thing that
gives the markets a supply loop (M8's "prices moved by what the ships carry" becomes a
knob).

### 2.5 The coarse acts anywhere

A person on a sleeping hull, seated or rules, acts through her `submit`, which routes by
the act and not by the shape:

| the act | awake | asleep (coarse) | the means |
|---|---|---|---|
| the helm, the sails, the guns, the anchor's detail | the grammar | refused in words naming the coarse forms | the physics |
| shape a course, steer, heave to, fill away, make and shorten sail as a state, anchor, weigh, give chase, haul off, keep the station | the grammar | `far_order` on her far body, **by the port's track in and out and under the land guard** (`_approach`, `_out_of_port`, `land_crossing`, today the business's alone) | the plan |
| the colours, a signal, the hail, the lights | the grammar | `signals.far_order_words` as now | 71's two bodies |
| go ashore, come aboard, hire a waterman, go to the market, send the boat ashore for the prices or a purchase | `Dealings` | the same `Dealings`: a job of the port with the boat's time, the person's whereabouts changed when it is done | the port's jobs |
| buy, sell, water, victual, the yard's repair, enter hands | `Dealings.trade`, the yard, the pool | the same, the lighter's job and the yard's time; the yard's repair of a sleeping hull's parts by the file's condition, coarsely | the market, the yard |
| say, say to, ask, tell, a word ashore | hearing by spot | the same | the one registry |
| give, take, show, stow, read, throw; eat, drink | the free lines | the same | the one registry |
| write a letter, send it by a ship or a cutter, carry a letter | `message:` widened to any hull and any person | the same | the far bodies' carriage |
| the needs, the sick, the water in her | the keepers | the keepers at the minute | per hull |
| a far fight | the action | 74's rounds | 70's tables |
| report | `say` within hail, a signal, a letter, the log read | the same | 71, `read_log ship=` |

The sleeping hull's grammar is `submit` with `hull.awake` false: a reading, the
conversation, the book's listing, the person's acts, the port's acts, the free lines and
the signals go through the grammar as they stand (today's `_is_a_reading`, widened to
"needs no physics"); the plan's words go to `far_order`; the rest is refused naming the
coarse forms. The far brain (`FarCaptain`) is the rules body of a sleeping hull's captain
and gains the port's acts in its `_in_port` (the transaction, the watering by the needs'
rule, the boat for the prices), so that a convoy's merchantman trades and a cruiser waters
without a model; the same doctrine files (`data/captains/*.yaml`) say when.

### 2.6 The cap, the switch, what sleeps and what wakes

`switch` keeps today's rule with three changes. The centre is `world.followed`. The
candidates are the hulls and the vessels with brains; a vessel without a hull is given one
at her waking (`make_hull`, measured 0.5 to 0.7 s on the build machine, once per ship
rather than once per promotion). The order: a hull in dealings with the followed hull, then
**a hull with a stationed person** (a model's or the player's seat: the owner's note 11,
"a ship with a stationed person on it at full detail"), then the nearest; beyond the cap,
asleep. A sleeping hull costs no tick but her minute (3.3); the memory is the hull's
(80 KB in the checkpoint for a cutter with her log). A hull `done` (gone in and gone from
the sea, the business's end) is discarded with her log kept in the save when a station was
ever held on her, else dropped as a far body is dropped today. The physics switch is the
only switch: the far shape of a World kept for a seated station is retired, since a
sleeping hull *is* that shape with her state kept.

### 2.7 The stations, the readings, the samples and the deltas, per hull

`Harness(hull)` samples her readings, her log, her people and her deltas as it does a
World's today; `all_agents(world)` walks `world.hulls` (and the offices); `open_samples`
and the pace rule unchanged; the desk's `ship` names the hull and the seat key is
`<hull>/<station>` as now; `station_line` reads the person's whereabouts from the registry
("aboard the Raven, at anchor in Plymouth Sound, in the cabin"; "ashore at Plymouth, at the
market"). `shape_words` becomes the hull's "awake" or "asleep" notice with the coarse forms
named and no "beyond the range of the player's ship". `readings.ahead_words`, the
tripwires, the station line and the deltas take the hull. The seat at a person on any
hull: `seats.hold` with the hull named; the budget, the admission and the harbour's doors
as now.

### 2.8 The director's reach

The truth (`director_readings`) walks `world.hulls` and `world.vessels`: every ship by
truth, the hulls' people, purses, cargoes, guns, damage and water, the sleeping hulls
included, the persons ashore at every port, the things, the sets, the offices;
`within=` from the followed hull. The forms gain a hull where they had the player's:
`aboard the Raven: a cask found stove`, `aboard the Raven: twenty guineas paid into the
purse by ...` (the followed hull when none is named, so every example and every old order
reads as it did); `person: "Mr Fox" comes aboard the Raven as master`, `person: make ...
aboard the Raven`; `say as <person>` for any person anywhere, heard by spot; `message: at
<port> from <whom> to the Raven`; `ship "X": order` as now; `follow "X"` (82's). The
director's log one, the doubts the same, the rule of reach the same (a held person's acts
are his holder's). `focus` and `read_log ship=` (§12b) read a hull's log awake or asleep.

### 2.9 The replay and the save of a world with several hulls and persons who moved

One journal with the hull on each input (2.2); the stations' acts keyed by hull and
station; the save's `hulls` block; a person's moves are the inputs and the jobs that made
them (the boat's errand, the waterman, 74's capture as a world order), so a replay moves
him the same; a hull made in play by an act (a far trader's transaction, a person seated)
is made in the replay at the same tick by the same act. A save from before the refactor
has no `hulls` block and no `hull` on its inputs and reads whole; its checkpoint converts
(2.2). The log digest of the followed hull is what the pins read today; part 3 names the
pins that move and why.

### 2.10 The leaders of nations and companies: room left

An **office** is a station of the world and of no hull: the port admiral at Plymouth, the
Admiralty, a company's board at Falmouth, the minister of marine at Brest. The design
leaves it room by three things it does anyway: the stations' registry and the harness take
a *domain* that answers to the readings' names (a hull does; an office would answer with
its purview's truth: its nation's ships and their regimes, its ports' stances and markets,
the news), `world.offices` beside `world.hulls`; a person of the one registry may hold an
office's station ashore or unseen (`Person.aboard` None, `port` set or not); and the
office's acts are **world orders restricted to a purview**, through the channel the
director uses (`commissioned for`, `in ordinary at`, `convoy:`, `blockade <port>`, a price
regulated, a letter of marque, a court's verdict), doubted the same way, with a rules body
that is the regimes' book run once a day (72's `data/regimes.yaml` knobs: the sortie, the
commission's delay, the convoy's sailing) as the rules captain is the captain's. Biased and
competitive is the brief of each office and the nations' knobs; never seen as a person is
`Person.aboard` None with no port. Nothing of this is built by 84; 84 builds the domain
parameter, the registry's whereabouts and the orders' purview hook so that M8's package
adds an office without touching the hulls.

### 2.11 What a model at another ship's captain's station sees and may do

Seated as the Raven's captain (by the door's `--ship Raven` or the director's `seat:`),
with the Raven asleep at anchor in Torbay: his line, "You: the captain of the Raven,
aboard, on the quarterdeck, at anchor in Torbay, since 06:10; the deck yours"; his
readings: her place by her account, the wind at her, her way, her sail as a state, the sail
in sight from her masthead (the Amazon among them, by name once made out), her people and
their states, her stores, water, purse and hold, her colours and signals, the port's places
and prices when in port and her price list held, the news; her log (her own lines, kept
from her last waking); the deltas and the stand-by's tripwires as any station's. He may:
weigh, shape a course for Plymouth (by the track out of Torbay and the land guard), make
sail, heave to, anchor, give chase; show colours, make and answer a signal, hail and answer
a hail; go ashore and come aboard, send the boat for the prices, buy and sell, water and
victual at the yard, hire a waterman; go to the market, speak to a person there, be told
and asked; give, take, read, stow a thing; write and send a letter; keep his journal; stand
by. He may not, while she sleeps: name a sail, work the helm's detail, exercise or fire the
guns, reef, tack by the evolution: each refused in words naming the coarse form. When the
cap wakes her (near the Amazon, or in dealings, or because he is stationed and the cap has
room), the whole surface comes beneath the same station with no reseat and the log says so,
as 43 built it. What he sees of the Amazon is what her lookout sees: a sail, a frigate,
British colours, a hoist; nothing of the player's log.

### 2.12 The owner's acceptance test under this design

The Amazon in Torbay, the Raven her tender in company, a model seated as the Raven's
captain; the player at the Amazon's prompt.

1. *The seat.* `seat: <model> as captain of Raven`: her hull made from her file at her
   truth (once; half a second), awake since she is within four miles and the cap has
   room and she carries a station; her people, her stores and her purse hers from here
   on, her log begun. The player's log says nothing.
2. *The order.* The player signals her by 71's book ("proceed to Plymouth"; or hails her
   within four cables, or sends a letter by the boat). The model reads the hoist in its
   sample, answers it, and orders `weigh` and `shape a course for Plymouth`: awake, her
   own evolutions and her captain's grammar; the Amazon's lookout sees her under way and
   the player's log says so.
3. *Through real weather.* Six miles out she is put to sleep by the cap (the Amazon lying
   still, nothing in dealings): her far body sails the plan by the port's track and the
   polar in the systems' wind at her place, reefed over thirty knots and lying to over
   forty-five, the systems' sky and visibility **at her** (one `conditions_at` per hull per
   minute); the model's sample says she is asleep and what it may do; it may heave to for
   the night or carry on. Her water, needs and people tick at the minute.
4. *Into a port.* `shape a course for Plymouth` ends at the road by the track; `come to an
   anchor` in the Sound; the pilot and the track in are the port's job on her (the
   `Dealings` of a sleeping hull run the pilot's minute as a job without the conn's
   physics: she is brought to the anchorage at the track's time; the owner's open decision
   in part 5 is whether a sleeping hull takes the pilot at all or anchors in the road).
5. *Ashore to a person.* `go ashore`: her boat's pull by the port's job, the model's person
   landed at the quay, `go to the counting house`, where Mr Gill (made by the director,
   `person: make "Mr Gill", a merchant, ashore at Plymouth, at the counting house`) is
   found in the one registry; `say to Mr Gill: ...` heard by spot; the director answers
   as Mr Gill by `say as`, or a model seated as his voice does.
6. *Back with a thing.* `aboard: a sealed packet, in the keeping of Mr Gill` (the
   director's, anywhere); `give the packet to the captain of the Raven` by the director's
   `say as` and the free line, or the model's `take the packet` when it lies before him;
   `come aboard`: the boat fetches him, the packet in his keeping aboard the Raven.
7. *Past a ship the director placed.* `ship: a French lugger "Renard" of France at <place>,
   cruising` on the sea; the Raven weighs and sails for Torbay by the track out; the
   lugger's brain makes her out and chases by doctrine; both asleep, 74's far fight
   resolves it in rounds, or the Raven's model hauls off and runs; both would wake if
   within the cap's reach of the Amazon, and the owner's cap decides whether a fight
   between two stationed or dealing hulls far from the player wakes them (part 5).
8. *Home to report.* Within four cables of the Amazon the model hails or signals; `say to
   the captain of the Amazon: ...` heard on both quarterdecks; the player reads it in his
   log and nowhere before: his log had a sail going and a sail coming and nothing between,
   and the Raven's log, read by `read_log ship="Raven"` or shown by the director's
   `two stories`, has the port, the quay, the counting house, Mr Gill, the packet and the
   lugger, every line the game's own.

Each step is a thing the world does; none is a special case of the player's.

### 2.13 What was rejected, and why

- **Many Worlds sharing the world's state** (the brief's cheaper reach): costed in part 3
  and rejected there; the short reason is that its sharing shims are half the one-world
  work, it keeps two clocks, two logs and the drop at demotion, and 82's followed ship then
  has to make the player's World a CrewedWorld of a headless parent, which is this design
  by a worse door.
- **Every ship a hull from the start.** A hull costs half a second to make and 80 KB to
  keep, and most of the business's ships never meet anyone; a hull made at her first need
  is the same ship, later and cheaper.
- **A stationed ship awake at all times** (the owner's thought in note 11). A hull awake
  costs what the frigate costs (3.3); the cap's order gives a stationed hull priority
  rather than exemption, so that two stationed hulls and the player's fit the owner's
  machine and a dozen do not stop it. The owner may raise the cap for a scenario as now.
- **The far shape of a World kept for a station.** A sleeping hull is that shape with her
  state kept and no second clock; nothing of it is worth keeping.
- **A vectorised many-hull physics** (the risk table's hot loop). Nothing here needs it:
  the awake set is the cap's, as today. It stays the answer if the owner wants every ship
  in a region awake.
- **Persons with no home hull.** `come aboard`, the prize crew, the watch bill and the
  muster all want to know whose man he is; a person of the world keeps a home.
- **Merging `Vessel` into `Hull`.** The far record stays the cheap thing every ship has;
  the hull is the costly thing some ships have; one identity, two objects.
- **Renaming `world` to `hull` through the consumers.** The façade keeps the names so that
  the migration moves the seams and not the 7,600 lines of the grammar and the readings;
  the rename is the long tail, done file by file as each is touched, never as a step.
- **A world order for every person's act** (the director moving persons by `person:` as
  the means for a model's `go ashore`). The act is the person's and journaled as his
  station's; the director's form stays the director's.

## 3. The two roads costed, honestly

**Road A, one World with many hulls** (part 2; the lead's instinct). **Road B, many Worlds
sharing the world's state** (the brief's cheaper reach): `CrewedWorld` kept as the
promoted ship's container, her World made as today but given the parent's registries by
reference instead of empty copies (`self.ports = parent.ports`, `self.people` the parent's
persons for the shore, `self.business`, `self.squadrons`, `self.director_*`,
`self.world_orders` the parent's), the player's World the parent as now with its shadow,
two clocks and two logs as now, and the demotion's drop mended by keeping her World asleep
when she carries something worth keeping.

### 3.1 What moves in the code

Both roads must do the same four splits, because the sharing is impossible without them:
**the ports' dealings** out of `Ports` (2.4: about 1,200 of its 4,270 lines are the ship's
pilot, cutter, boat, jobs, price lists and trade; under B each CrewedWorld needs its own
`Dealings` against the one shared `Ports` exactly as under A); **the persons' registry**
out of `People` (2.3: the whereabouts, the home, the company as a view; under B the
crewed World's `People` must read the parent's persons ashore and write its own man ashore
into them, which is the same registry by a longer road); **hearing and movement by the
registry** (`hearing.py`, `movement.py`, `things.py`: the spot with the hull in it); and
**the far brain's port acts** (`brains.FarCaptain._in_port`, `far_order` by the track and
the guard). These four are about 2,200 lines moved or changed under either road, and
they are the owner's acceptance test's steps 4 to 6.

Road A then does what B does not: `core/world.py` split into `World` and `hulls.Hull`
(some 600 lines moved behind properties, 100 of properties); `crews.py` rewritten from
1,309 lines to the switch (about 500); `ships.py` the player's vessel of the sea and
`tick_hulls` (150); `squadrons.py`, `combat/action.py`, `signals.py`, `signalling.py`,
`hail.py`, `brains.py` the sixty-six `PLAYER_ID` cases made one rule (about 150);
`orders.py` and `director.py` the forms with a hull and the truth over the hulls (350);
`readings.py` the truth and the station line (150); `harness.py`, `remote.py`, `seats.py`
the hull in place of the World (150); `replay.py` the hull on the inputs, the `hulls`
block, the converter (200); `ui/server.py`, `console.py`, `harbour.py` the followed hull
(100); and the tests beside each. About 4,000 lines touched and 2,000 moved in all, the
size of package 70. Road B touches about 2,500 (the four splits, the sharing in `crews.py`
and `_crew_scenario`, the save's `crews` block for the crewed Worlds' inputs and
transcripts, the asleep World) and leaves the rest.

By the assumptions of 1.7: Road A retires all thirty-eight (the twelve of the World's
shape and the promotion become the Hull's own; the five of the player's shadow become one
rule; the four of the far brain become the port's acts; the five of the stations and the
hearing become the registry's; the three of the save become the hull on the input; the
three of the drivers become `followed`; the two of the truth become the walk over the
hulls; the consent brief's words are 55's). Road B retires fourteen (6, 7, 13, 18, 20, 21,
25, 27, 28, 29, 31, 37, 38 and half of 10) and keeps twenty-four: the one ship at the
World's centre (1 to 5, 8, 9), the shadow and the special cases (11, 12, 15), the switch's
centre (19, 36), the second clock and log (9, 17, 22, 23, 24), the drivers (34, 35) and
the save's shape (32, 33). The twenty-four are the ones 82's followed ship and the
observed world then have to retire, since a world with no player's ship under B is a
parent World with no `ship`, which every one of the 223 `world.ship` reads refuses; so B's
saving is paid again by 82 and, the hulls being then made under 82's time pressure, paid
worse.

### 3.2 The pace, measured

The method is truth 51's (a thousand ticks to settle, the best of three thousands, in
ticks a second of wall clock), by `tools/pace.py` on the head `908741f` and by the
scratchpad's `measure_seam.py` (described in 1.8's manner: its figures are reproducible
from the script's docstring), on the build machine with package 73's builder running
beside (the load average is given with each figure; the floors are judged alone). The
owner's baseline, 95 ticks a second with twelve crewed ships on his machine and 1,111
alone, is not re-measured here.

| measure (`tools/pace.py`) | this run | package 43's table (the slower machine) |
|---|---|---|
| the frigate alone, the station trial | 573 (load 0.7) | 560 |
| the frigate with the dozen ships at far detail | 516 (0.8) | 718 to 764 on the faster machine |
| the frigate with one crewed ship | 282 (0.9) | about 280 |
| with three (the cap) | 181 (0.9) | 100 to 114 |
| with six | 86 (2.3) | 56 |
| with twelve | 47 (3.8) | 34 |
| the convoy of six and the privateer, far detail alone | 520 (4.5) | 551 (72) |
| the same under the default cap | 298 (4.9) | 328 (72) |
| the same under a cap of twelve | 335 (5.1) | 311 (72) |

| measure (`measure_seam.py`) | figure |
|---|---|
| a promotion (`CrewedWorld` made: her ship from her file, her muster, her stations), best of three | a cutter 465 ms, a brig 634 ms, a frigate 698 ms (load 5.5) |
| the checkpoint of the first action at tick 60, the privateer far | 460 KB |
| the same at tick 900, the privateer crewed and fourteen minutes in action | 539 KB: **a crewed World's weight about 80 KB** with her log |
| a station's World kept in the far shape, `far_tick` a thousand times | 27 ms: **0.03 ms a tick**, a hundredth of a crewed tick |
| the schooner at anchor in Carrick Road with the dozen far ships, no orders | 1,898 ticks a second (load 5.7); 1,931 with the cap at nought |
| the frigate under way on the station trial, the same minutes | 539; hove to 515 |
| of three crewed ships' ticks (cProfile, 600 ticks): the sails' physics | **63 per cent** of `World.tick` |
| the evolutions' runner (the hands at the sheets and the sails) | 21 per cent |
| the strain | 3.5; the captain's judgement 2.4; the routine 1.4 |
| the World's own bookkeeping that a refactor touches (the tide, the weather followed and observed, the ports' tick, the people's tick, the needs, the lookout, the reckoning) | **under 3 per cent together** (0.1, 0.9, 0.1, 0.1, 0.1, 0.0, 0.4, 0.5) |

What the figures say for the roads:

- **A crewed ship's cost is her hull's, not her World's.** Eighty-four per cent of her
  tick is the physics and the hands, which every road pays for every awake hull alike;
  the World-level bookkeeping both roads move is under three per cent. **Neither road
  changes the pace of an awake ship within the measure's noise**, and the owner's 95 with
  twelve is untouched by either.
- **A sleeping hull costs nothing a tick.** Road A's hulls kept asleep are not ticked but
  at the minute (the people's, the needs', the water's and the dealings' minutes, each
  measured at a thousandth of a tick or less per hull); the far shape's 0.03 ms is the
  upper bound of what a sleeping hull's mirror costs, and the design mirrors nothing while
  she sleeps. The memory is 80 KB a hull in the checkpoint; fifty hulls are 4 MB against
  `test_checkpoint`'s 2 MB bound on one world, so the bound moves with the hulls kept, said
  in the notes, and the owner's decision in part 5 on which hulls are kept decides it.
- **A promotion's hitch** (half a second to seven tenths, a frozen frame at 60x) is paid
  today at every promotion and under road A once per ship; a ship that flaps at the edge
  costs today's road a hitch each time and road A none.
- **A hull at anchor costs a quarter to a third of one under way** (1,898 against 539 are
  different hulls, the schooner's against the frigate's; the frigate hove to at 515 says
  the physics runs whole while she has sails set, and the anchored hull's saving is the
  sails furled and the hands idle). So "a ship with a stationed person at full detail at
  all times" (the owner's note 11) costs, at anchor in port, about a third of a crewed
  ship, and under way the whole; the cap's order with the stationed hull first (2.6) is the
  honest bound, and the owner may raise the cap.
- **The floors.** `BUILD_MACHINE_FLOOR` 500 (truth 51's form) and `CREWED_FLOOR_TICKS_S`
  60 with the cap full hold under either road by the same margin as today; nothing here
  lowers them. The crewed figures under load above (86 at six, 47 at twelve) are the
  machine's and not the code's: 43's table has 56 and 34 for the same on the slower
  machine, quiet.

### 3.3 The pins

The recorded passages pin the player's log's digest, line count and ticks: the gate 5a
day, the three gate 5b passages, the merchant passage and the naval cruise, the 6a intent
and fake-captain days, the five captain's trials, and the M7 truths' inline ticks (the first
action's strike at 7560, the encounter, the convoy of four's hoist at 2866, the convoy of
six's signal at 2760, the squadron promoted by 600, 7-155's line within a cable and a half).
**The aim is none moved**, and the design keeps each by three rules, each a step's proof in
part 4:

1. **The followed hull's streams keep their names** (`rng.stream("muster")`, `"strain"`,
   `"wind"`, `"weather"`, `"reckoning"`, `"business"`, `"gunnery"` unprefixed) and the other
   hulls keep today's seeding (an `Rng` of her own seeded `(seed * 1009 + crc32(id))`,
   made once at her first waking), so every draw the player's passage makes is the draw it
   makes today, and a ship woken once in a passage draws what her promotion draws today.
2. **The tick's two phases keep today's order of lines** (2.2): the bodies move in today's
   order, the other hulls see and act, the far minute runs, the followed hull sees and acts
   last; a line's tick cannot move unless the order does.
3. **The player's vessel of the sea is appended last** to `world.vessels` and left out of
   every viewer's own sail, so that the brains' nearest-first orders and the lookouts'
   lists are what the shadow gave.

What can move, and why, each a finding and not a regression: **a ship woken twice in one
passage** draws her second waking from streams that continued (today she is re-mustered
fresh), and her hands are tired by what they did: the trade trial's French brig if she is
demoted and promoted again within it (the trial's as-merged record of 70 says she is
crewed while chasing; whether she is demoted within the trial is the bisection's to say);
**a crewed ship's own log** keeps the world's ticks, not ticks from her promotion (nothing
pinned reads them: `test_crews.py`'s truth 89 reads the lines' kinds and words); **a
sleeping hull's dealings** run where today a far ship waits twelve hours and vanishes:
no recorded passage has a business ship reach her port and transact (the business is off
in every recorded scenario, 43b), and the scenarios' own far ships with `trade` intents
reach no port within their pinned spans (the Palinure in the cruise is a passage, not a
trade). Under road B the same three rules apply to the sharing and the same findings
follow; B has no new risk of its own, and no saving either, since the dangerous moves (the
registry, the dealings, the far acts) are B's too.

The checkpoint's classes: the three fixture saves (`tests/fixtures/saves/`, m5c, no crewed
ship in any) load by `World.__setstate__`'s converter (2.2) and the tests
`test_a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_glass` and `..._watch` are
the proof; the owner's eleven saves of 70 to 72 have crewed Worlds in them and are the
converter's second test (the lead's, with the folder).

### 3.4 What the consent brief's words assume

`docs/agents/ConsentBrief.md` is read and not edited; these are its sentences that name
"the ship" and what each would mean under the design, for package 55:

- "*a captain, who commands a ship, the player's or another in the same world, with every
  power a human player has at the prompt*": already the design's words; true today only
  in the promotion's shape, true whole under it.
- "*the ship's log, her readings, a reference library ... and tools to read those, to
  give orders where the station allows*": true of a hull; "the ship" is the station's
  hull, awake or asleep, and asleep the orders are the coarse forms. The brief says
  nothing of a station whose ship's surface changes under it (43 built it under 40's
  decision; the brief never said it): **a sentence for 55** that a station's ship may be
  at full or at coarse detail by the game's budget and that its orders are refused in
  words where she is coarse.
- "*The officer of the watch stands in the place of one of the ship's officers*", "*The
  captain stands in the place of the person who commands the ship*": true for any hull;
  **the station bound to a person who moves between ships** (82, 74) is not in the brief
  at all: a sentence for 55 that a station is a person's and follows him aboard another
  ship or ashore, with the orders that place allows.
- "*It gives no order to the world outside the ship (the weather, another ship, a port):
  those are the scenario's and refused in words*": still true; a person's acts ashore (a
  purchase, a word to a merchant, a thing taken) are his station's acts, not orders to
  the world, and the brief's "a port" in that list means the port's stance and prices,
  which stay the director's. Worth a clause for 55 so that "a port" is not read as "go
  ashore".
- "*A paused or silent lookout or master has its work done meanwhile by the ship's own
  people*", "*the deck lent to its own book ... by the game's own rules in the captain's
  place*": true for any hull; for a sleeping hull the rules in the captain's place are the
  far brain's, which the brief need not name.
- "*a passenger, who is aboard with no duty*": true aboard any hull; a person ashore with
  no duty (the voice of 67, a person made ashore) is not "aboard": a word for 55.
- "*a director, who sees the whole world, shapes events, and may seat models at the
  stations of its ships*": under 2.10 an office is a station of the world and of no ship;
  M8's package and 55's revision say so together, not 84.

Nothing in the brief is made false by road A that road B keeps true; the two sentences 55
wants (a station's ship coarse or full by the budget; a station following its person) are
wanted by 82 and 74 under either road.

### 3.5 What 82, 74, 75 and 77 gain or must wait for

- **82 (the boat, the player aboard another ship)** gains most. Under road A its item 1
  (the followed ship) is `world.followed` and the drivers reading it, a day's work on 84's
  ground instead of the spec's "the World's construction assumes a ship in several
  places"; its item 2 (a person aboard another ship, the seat following him) is the
  registry's whereabouts and the station bound to the person, 84's; its item 3 (the replay
  of a station on another ship) is the hull on the input, 84's; its items 4 and 5 (the
  boat as a vessel, the oar force, the tow) are its own and unchanged: the boat is a small
  hull, a vessel of the sea when away, awake under the cap like any, her file through the
  generator. 82 after 84 is the boat, the oar force and the seat's words. Under road B, 82
  pays the twenty-four assumptions of 3.1 itself.
- **74 (prizes, the captive, the far fight)** gains the prize as a hull with a new nation
  and the prize crew as persons whose home is the captor and whose whereabouts is the
  prize (the registry), the captive as a person aboard the captor's hull with his station
  following him and his voice heard by spot (66's line and hearing, no new channel), and
  the far fight's damage written into a sleeping hull's parts as state (rule 1) where 70's
  `Vessel.damage` sums it. 74 waits for 84 and 82 (the owner's order) and is simpler for
  both; its consent draft (item 6) reads 3.4.
- **75 (the ships)** waits for nothing: the files are the files; a sub-type's fit is the
  hull's at her making, as the far record's `fit` is today.
- **77 (the evolutions and the catalogue)** waits for nothing: the hands are the hull's;
  the boarders' drill and the cutting out read 82's boat, as before.
- **73 (building now)** is merged first (the owner's order): its water keeper "of every
  World" becomes the hull's at 84's first step by a rename, and gains that a demoted
  ship's water and wounded are no longer forgotten (1.7's 21).
- **76, 79, 81** wait for nothing. **55** gains the two sentences of 3.4.

### 3.6 The recommendation

**Road A, one World with many crewed hulls, done once and now.** The reason in a
paragraph: the four splits that make a person's acts possible anywhere (the ports'
dealings, the persons' registry, hearing by the registry, the far brain's port acts) are
the same work under either road and are the owner's acceptance test's hard steps; what
road B saves by keeping two Worlds (the player's at the centre with her shadow, two clocks
and two logs) is some 1,500 lines of the split and the drivers, and every one of those
lines is paid again by 82's followed ship, whose first item is a world with no player's
ship, which a parent World cannot be; the pace is the hull's and not the World's under
either road (84 per cent the physics and the hands, under 3 per cent the bookkeeping), so
A costs nothing in ticks and B saves nothing; the pins are kept by the same three rules
under either; and A ends with the thirty-eight assumptions retired where B ends with
twenty-four kept and a `CrewedWorld` that is a hull by a worse name. The owner's frame
("a sweeping refactor on any large scale would be better to do sooner rather than later")
is the lead's instinct, and the code agrees with both.
