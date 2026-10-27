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
