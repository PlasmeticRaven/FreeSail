# Code reader 02: the world's other ships and who commands them

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. I ran no tests and changed no files except this one. I ran
short Python commands: a YAML key census, an AST count of lines and imports, and one call to
`station_off` and `_station_square` on the channel-west chart, which took about a second.

## 1. What it is

**In the game.** Every sail the player sees that is not his own ship is a `Vessel` in
`freesail/world/ships.py`. A vessel that is given an `intent:` carries a rules-based captain. The
captain's doctrine comes from `data/captains/<role>.yaml`. That captain plans legs over the chart,
reacts to the weather and to strangers, and fights, takes prizes or runs. Inside about four miles
of the player, the vessel can be "crewed": she gets a full hull, a rig and a company under the same
physics as the player's ship. Her captain then gives real orders through the player's own order
channel. Ships appear in four ways:

- named in a scenario;
- by director world orders;
- drawn by "the business" (`business.py`): traders, fishermen, cruisers, convoys, blockades and ships in ordinary;
- formed into squadrons and convoys (`squadrons.py`).

The player sees them only as the lookout's sightings, in hails, and in log lines such as "within
hail" and "cut out". When a model takes another ship's station, the player can also see that
ship's own log.

**Size.** These 13 modules come to 16,673 lines:

| Module | Lines |
|---|---|
| `captains.py` | 4,795 |
| `ships.py` | 2,325 |
| `crews.py` | 1,779 |
| `squadrons.py` | 1,752 |
| `business.py` | 1,316 |
| `fishing.py` | 1,128 |
| `brains.py` | 1,061 |
| `seats.py` | 786 |
| `hulls.py` | 553 |
| `stations.py` | 358 |
| `regimes.py` | 344 |
| `nations.py` | 330 |
| `service.py` | 146 |

The data in my part comes to 4,992 lines:

- `data/captains/*.yaml`: 11 files, 3,014 lines;
- `data/squadrons`: 198 lines;
- `data/fishing`: 299 lines;
- `data/crew`: 252 lines;
- `nations.yaml` 879, `business.yaml` 199, `regimes.yaml` 67, `marines.yaml` 84.

**Tests.** Test files that import these modules, by grep: captains 21, ships 22, crews 20, brains 10,
nations 7, seats 5, service 4, regimes 3, squadrons 3, business 2, fishing 2, hulls 2, stations 1.
The dedicated test files are:

- `test_captains.py` (624), `test_captain.py` (690), `test_captain_rules.py` (309), `test_captain_trials.py` (552);
- `test_brains.py` (415), `test_ships.py` (889), `test_crews.py` (1,079), `test_hulls.py` (407);
- `test_squadrons.py` (829), `test_business.py` (547), `test_fishing.py` (323), `test_nations.py` (370), `test_service.py` (159);
- `test_subtypes.py` (1,211), `test_far_action.py` (368), `test_far_hail.py` (142), `test_held_hulls.py` (120), `test_between_hulls.py` (367);
- many scenario "truths" in `test_known_truths.py` (17,391 lines).

### The main types

- **`ships.Vessel`** (`ships.py:599`), the far body. A plan is a list of tuples:
  `to`, `to_ship`, `company`, `lie_to`, `home`, `anchor`, `chase`, `away` and `station`.
  `Vessel.tick` (`ships.py:880`) moves her once a minute by a polar drawn from her ship file
  (`polar_of`, `ships.py:572`), with the tide added. The dataclass has 60 or so fields, most of them
  added package by package (`ships.py:603-710`).
- **`ships.Vessels`** (`ships.py:1713`), the sea. It ticks the brains, the squadrons, the far rounds,
  the prizes, the regimes and the brainless signals. It moves the bodies, raises and lowers the level
  of detail, hails, and runs the crewed switch (`ships.py:1777-1849`).
- **`captains.Judgement`** (`captains.py:1858`), the brain shared by both bodies: the stimuli
  (`_stimulus`, `captains.py:2013`), the transitions, the weather trend and the chase log.
- **`captains.Captain(Judgement)`** (`captains.py:2308`), the near body's captain. He acts only
  through `World.submit` (`give`, `captains.py:4716`). He loads books (standing orders) per state
  into the standing runtime and works each state by hand in `_work` (`captains.py:2984`).
- **`brains.FarCaptain(Judgement)`** (`brains.py:295`), the far body's captain. He perceives from the
  truth (`perceive_vessel`, `brains.py:83`) and turns each state into a far plan (`resolve_state`,
  `brains.py:971`).
- **`captains.Planner`** (`captains.py:1234`): legs from an intent over the ports' tracks, the common
  tracks and a headland offing.
- **`hulls.Hull`** (`hulls.py:216`): one ship's fields, standing in for a World through
  `__getattr__` and `World.as_hull`.
- **`crews.CrewedWorld`** (`crews.py:205`): a World built only to make a hull's fields, then thrown
  away (`make_hull`, `adopt_hull`, `crews.py:313-361`).
- **`squadrons.Squadron`** and **`Squadrons`** (`squadrons.py:170`, `1266`): formations, stations,
  stragglers and book rules. `far_captures` (`squadrons.py:1626`) is the "cut out" rule.
- **`business.Business`** (`business.py:245`): draws ships under the seed each hour.
- **`fishing`**: grounds, one catch function `take` (`fishing.py:381`), `Fishery`, `far_work`, and
  `captain_work` for a crewed fisherman.
- **`regimes`**: ships in ordinary, commissions and sorties.
- **`nations`**: wars, port stance and habits.
- **`seats` / `stations`**: the director's seats for models, and station bindings.
- **`service`**: King's ship, privateer or merchant, for the purchase rules.

**Callers.** `core/world.py` builds `Vessels` (971), `vessel_from_spec` (1050) and `Captain` (1111),
adopts hulls (1182) and ticks `_tick_vessels` (1652, 2393). Commands reach it through `world/orders.py`
(the `ship "X": ...` channel), `core/replay.py` and `core/acts.py`. The agents' `remote.py` and
`director.py` reach `seats`.

## 2. What a rules-based captain does when the player meets her

Everything comes from the doctrine's transition table, judged once a minute (`JUDGE_EVERY_S`,
`captains.py:167`). The player's ship is a stranger to her under the id `"the ship"` (`ships.py:67`).

- **Merchant, packet, Indiaman, fisherman, prize-master.** The trigger is `hostile stranger`: an enemy within `stranger_hostile_nm` (6; 8 for the packet).
  - "Enemy" needs a nation, and the lookout gives a nation only once colours are made out, at 2 miles (3 with a glass) (`ships.py:106`, `1985-1995`). So in practice she reacts at about 2 miles, not 6.
  - She then goes into `evading`. Crewed, she shapes a course 20 miles down the reciprocal bearing, turned a point at a time to keep off the land (`_haul_off`, `captains.py:4612`), again every 10 minutes. Far, her plan is `("away", id)` (`brains.py:626-630`).
  - She stops evading when the stranger is out of sight (`stranger lost`).
  - She fights (`engaging`) only if the enemy is within `engage_nm` (0.3 for the merchant) and she has guns.
  - A player who shows no colours is no enemy: she does nothing except the rule of the road at 3 cables, and only when crewed.
- **Cruiser, revenue cutter, privateer.** Any unspoken sail within 10 miles (`stranger near`) sends her to `investigating a stranger`.
  - Crewed, she orders "make her out". Far, her plan is a chase to hailing distance.
  - Then one of three things: `enemy made out` leads to `chasing` ("chase the <rig>"); `friend made out` or `stranger spoken` sends her back on passage; after 3 hours without closing (`chase stale`) she gives up.
  - Within 1 mile, an enemy not of a bigger class (`overmatched`) brings her to `engaging`. Crewed, that means: beat to quarters, cast loose the guns, load, aim, engage her on the side she bears, hold fire until the book's range, steer by `helm_in_action` (`captains.py:230`), and board if the odds allow (`_boarding`, `captains.py:4307`).
  - When the mark strikes (`enemy struck`) she goes to `taking possession`.
  - At far detail, a cruiser with a `hail:` threshold calls "What ship is that?" at 4 cables (`ships.py:2117-2127`).
- **King's ship.** On passage she has no transition for a stranger at all (`kings-ship.yaml` transitions). On passage she ignores the player completely unless an enemy comes within 1 mile, which brings `engaging`. She investigates and chases only while `keeping station`.
- **Commodore.** Same as the King's ship. He investigates only while keeping station, and turns away from enemies made out (`investigating → enemy made out → keeping station`). He chases only by the convoy book's `cover` rule (`squadrons.py:965`).
- **Rule of the road.** This runs only on the near captain (`captains.py:4676`). The far body has none, so the same ship crossing the player obeys it inside about 4 miles (when crewed) and not outside.

## 3. Is it reached?

Most of this is reached in play.

- `business: on` appears in 9 shipped scenarios (for example `merchant-brig.yaml`, `smack-falmouth.yaml`, `the-channel-observed.yaml`).
- 20 of the 69 scenarios give an `intent:`.
- `World._tick_vessels` runs every tick (`core/world.py:1652-1673`).

The following is dead or unread:

- **Doctrine thresholds that no code reads** (census of every `thresholds:` key against quoted strings in `freesail/` and `{placeholders}` in the books):
  - `road_cables`, `leg_reached_nm`, `anchor_within_nm` (in 10 files each). The code uses the constants `ROAD_CABLES` (`captains.py:381`), `Leg.reached_nm=2.0` and the 0.5 literals (`captains.py:1274, 1462-1475`).
  - `spell_minutes` (9 files).
  - `mans_prizes` (8 files; also at `squadrons.py:1556`, in a comment only).
  - `stranger_chase_nm` (5), `station_wear_hours` (4).
  - `burns_when`, `divide_prisoners`, `prisoners_most`, `worth_least`, `fit_least` (3 each).
  - The merchant's `mans_prizes: false` with "nought turns it off" switches nothing. Who takes prizes is decided by the transition rows and by `_ARMED_ROLES` (`squadrons.py:1559`).
- **`data/captains/cruiser.yaml:111-148`**: the cruiser's whole prize block (`prize_crew_share`, `prize_master_from`, `prize_goal`, `prize_company`, `parole_accepted`, `prisoners_landed` and others) is indented under `stations:`, not under `thresholds:`.
  - The YAML census confirms it: `thresholds` has no `mans_prizes`, while `stations` has 13 non-nation keys.
  - `prizes._th` therefore falls back to its defaults (`prizes.py:238-242, 339-346, 376`), which happen to match today. Editing the cruiser's file changes nothing.
  - `business._cruisers` loops over these keys as if they were nations (`business.py:760`).
  - `revenue.yaml` has no prize thresholds at all, although the revenue cutter is a captor (`squadrons.py:1559`).
- **Squadron books**:
  - `interval_cables`, `formation`, `columns` and `night` are never read from the book (`squadrons.py:203-223` reads only five knobs). `from_spec` reads `interval_cables` from the scenario spec instead (`squadrons.py:1229`).
  - `straggler_minutes` is in the data (15 in `blockade.yaml`), but the code uses the constant `STRAGGLER_MINUTES` (10; `squadrons.py:617`).
  - `blown_off.rendezvous: Torbay` is never read (see finding 3).
- **`regimes.yaml`**:
  - Only five knobs are read (`regime_knob` callers: `captains.py:881`, `regimes.py:299-301`, `business.py:813, 1134`, `orders.py:913`). The rest (`rule`, `intent`, `book`, `role`, `escort`, `formation`) is prose.
  - `on blockade` has no `inshore_nm`, so `captains.py:881` always uses its default of 6.
  - The code defaults differ from the data (`slip_out_clear_nm` 10 against 15; `slip_out_wind_max_kn` 27 against 22; `regimes.py:299-301`). If a key is ever renamed, behaviour changes without a sound.
  - `regimes.REGIMES` (`regimes.py:27`) is used nowhere.
- **`nations.yaml`**:
  - The `naval:` keys `keeps_the_sea`, `keeps_port`, `engages` and `privateers` are read by no code (0 hits).
  - Each nation's `relations:` is not loaded at all (`load_nations`, `nations.py:278-297`, drops it).
  - `Nations.allied` and `port_nations` have no caller outside tests.
  - The `ports:` index (`nations.yaml:719ff`) is a second table of port nations, read only by tests, and it disagrees with the port files: `valletta: order-of-st-john` against `data/ports/valletta.yaml`, which has Britain from 5 September 1800; Barcelona, Rosas and others have dated lists that the index flattens.
  - The header says "Seven nations" (`nations.yaml:3`); there are 16.
- **Dead code in the modules**:
  - `brain._drawn_wait` is written (`business.py:1262`) and never read.
  - `_NOT_CREWED_STATES` and `FAR_ONLY_ROLES` are kept empty "for the rule's one place" (`crews.py:119, 126`); the checks at `crews.py:883, 891-892` can never fire.
  - `CrewView = HullView` (`crews.py:202`) exists only for old pickles.
- **Stimuli** handled in code but used by no doctrine file: `weather mending`, `weather worsening`, `cargo done`, `at the road`, `ready for sea`, `anchored` (census).
- **Doctrine rows that cannot fire.** The King's ship and the commodore have `stranger_hostile_nm: 0`, so `overmatched` (which uses that distance, `captains.py:2061`) never fires for them, and their `engaging/taking possession → evading` rows are dead. Their `evading` state has no way out except `enemy in range` or `aground` (`kings-ship.yaml:282, 318`). And `_haul_off` searches within `0*3` miles (`captains.py:4616-4618`). If the figure is ever raised, she would enter `evading`, never haul off, and never leave.
- **`Vessel.promote`** (`ships.py:1094`) only sets `detail`. Its docstring ("the crewed promotion ... milestone 6's; this switch is their seam") is out of date: the crewed promotion is `crews.switch` and does not go through it.

## 4. Built more than once

1. **Representations of a ship.** I count eight live forms, plus three adapters.
   - The forms:
     - (a) the far `Vessel`, moved once a minute;
     - (b) the same vessel at `detail="near"`, moved every second with a 1°/s turn limit (`ships.py:926-930, 2035-2048`);
     - (c) a vessel whose `Hull` is asleep (`shape="far"`). Her body is still the plan, and the hull is mirrored from it each second (`mirror_far`, `crews.py:373`). `far_tick` runs her lookout, dealings, people and bells (`crews.py:388`);
     - (d) a vessel whose hull is awake (`detail="crewed"`). She runs full physics and her own `Captain`, mirrored back into the vessel (`mirror`, `crews.py:518`);
     - (e) the player's own hull, plus a shadow `Vessel` under `PLAYER_ID` with `detail="crewed"` that the sea never moves (`ships.py:1875-1950`);
     - (f) a brainless member of a set on a `station` leg (`squadrons.keep_station`, `squadrons.py:1694`);
     - (g) a hull in ordinary (no brain, an anchor plan; `regimes.put_in_ordinary`);
     - (h) a pilot's boat or a ship's boat (`Vessel.boat_of`, `ships.py:739`; `crews.py:566-569`).
   - The adapters: `CrewedWorld` (a builder, thrown away), `HullView`, and `_FarBody` (`crews.py:1531`), which exists to let `far_order` run without a hull.
   - One vessel is described by three overlapping flags: `Vessel.detail` (far, near or crewed), `Hull.shape` ("full" or "far", derived from `awake`), and `Vessel.crew`, which is the hull under the field's old name, with a `hull` property over it (`ships.py:723-730`).
   - **The rings are inverted.** The crewed promotion is at 4 miles in and 6 out (`crews.py:90-91`). "Near detail" is at 2 miles in and 3 out (`ships.py:132-133`). So a ship with a brain is crewed before she could ever be "near", and the near ring now serves only brainless ships and ships held asleep by the cap.
   - **How one becomes another:**
     - a scenario or business spec becomes a far vessel (`vessel_from_spec`, `ships.py:1509`);
     - a far vessel becomes near or far again by distance (`_promote_and_hail`, `ships.py:2083`);
     - with a brain, a far vessel becomes a crewed hull (`crews.switch` → `promote` → `make_hull`/`adopt_hull`, or `_to_full` for a sleeping hull);
     - a crewed hull goes to sleep (`demote`; damage summed by `write_damage`);
     - a hull is released when the vessel is done (`release_done`).
2. **One brain, or several?** Formally one: `Judgement` with two bodies, `Captain` and `FarCaptain`. In practice there are four rule engines:
   - the doctrine transitions;
   - the near `Captain._work` hand code (some 2,000 lines of state work that the far body does not have: casts, sail after the gale, aback recovery, danger ahead, boarding, repairs, rule of the road);
   - the squadron books' rules, with their own `_stimulus` (`squadrons.py:839`). The same name means different things there: `gale over` is "wind under 34−6 knots" in the squadron book (`squadrons.py:870-873`) but "under the line for `gale_over_minutes`" in the doctrine (`captains.py:2032-2040`);
   - the brainless plan grammar `_goal_plan` (`ships.py:1323`).

   The two `Judgement` bodies also each implement their own hooks, and these have drifted apart:
   - `_nearest_enemy` and `_nearest_stranger` are copied word for word (`captains.py:4599/4581`, `brains.py:565/668`);
   - `_is_enemy` finds the ship's own nation differently: `dealings.ship_nation` (`captains.py:4596`) against `vessel.nation` (`brains.py:527`);
   - `_shelter_port` uses `ports.stance(port)` by account (`captains.py:4666`) against a hand-written `nations.stance(..., blockaded_by=...)` from the truth (`brains.py:587`);
   - `_station_mark` returns a tuple in one and a `Position` in the other (`captains.py:4079` / `brains.py:500`).
3. **Two grammars of a goal.** The far goal grammar `_goal_plan` ("trading A to B", "patrolling off X") and the intent grammar `read_intent` ("trade tin from A to B", "keep the station off X", `captains.py:710-895`) say the same things in different words and resolve places differently:
   - `ships.place_position` (`ships.py:1261`) takes a port's outer road;
   - `captains._place_id` and `_mark` (`captains.py:898`, `1162`) take a port id, a feature, a fishing ground or a position.
4. **Three geometries of keeping a station.**
   - The goal grammar lays a square of four marks around the *place*, moved off the land (`ships.py:1350-1367`, with `_off_the_land` from package 109).
   - The brain lays a square around the *station point*, which is already `radius` out to seaward (`brains.py:286-292`, `1023-1027`), with no land guard. So one corner comes back toward the place: off Ushant at 15 miles, the east mark is 5.8 miles from Ushant (I ran it; the water there is still deep).
   - The near `Captain` steers for a single point (`captains.py:4079-4090`).

   The same cruiser therefore patrols three different patterns depending on whether she has a brain and whether she is crewed.
5. **Two role tables.**
   - The tables:
     - `captains.role_for` (`captains.py:1021`): no `fish → fisherman` row, so a crewed fisherman given a new fish intent becomes a merchant; `captain_work` patches this by hand (`fishing.py:1067-1069`). A frigate or a brig-sloop is a King's ship only by its wardroom file.
     - `brains.role_of_vessel` (`brains.py:214`): a frigate is always a King's ship, a brig-sloop is always a cruiser, and `fish → fisherman`.
   - So `Captain.set_intent` on a promoted frigate in trade gives the merchant, while the far brain gives the King's ship.
   - Five further tables of "a man of war" or "armed" that do not know of each other:
     - `MAN_OF_WAR_WORDS` (`captains.py:200`);
     - `_is_escort`'s description list (`squadrons.py:469-475`);
     - `_ARMED_ROLES` and `_MAN_OF_WAR_DESCRIPTIONS` (`squadrons.py:1559-1563`);
     - `_MAN_OF_WAR_ROLES` and `_MAN_OF_WAR_DESCRIPTIONS` again (`regimes.py:193-198`);
     - the frigate list in `role_of_vessel` (`brains.py:244`).

     Three more decide "King's ship": `_is_kings_ship` (by the wardroom, `captains.py:1055`), `service.ROLE_SERVICE` (`service.py:55`), and the brig-sloop override in `player_shadow` (`ships.py:1903`).
   - Two ways to rank a ship's size: `SIZE_RANK` keyed by description, and `_SIZE_WORDS` keyed by words (`captains.py:296-340`). A new description must be added to both, and to `DESCRIPTIONS` and `_DESCRIPTION_WORDS` in `ships.py:180-363`.
6. **Three performers of a far order.**
   - `crews.far_order` (`crews.py:1107`): shape a course, steer, heave to, fill away, give chase, haul off, make or shorten sail, anchor, weigh, keep station.
   - `signals.far_perform` (`signals.py:1284`): put about or wear, heave to, fill away, make or shorten sail, anchor, weigh, steer, close the flag, shape a course.
   - `brains.resolve_state`, which writes plans directly.

   The word sets differ: `far_order` has no "put her about", so a model at a sleeping hull cannot tack (`FAR_SHAPE_WORDS`, `crews.py:1018`), while `far_dangers` calls `far_perform("put her about")` (`crews.py:943`).
   Related near-copies:
   - `_is_a_reading` and `_needs_no_physics` (`crews.py:1251`, `1286`) differ mainly in `read_whole` against `parse`;
   - `_promote_and_hail` (`ships.py:2128-2141`) and `_deliver_to_hulls` (`ships.py:2050`) both say "she has a letter for the ship";
   - `transact` (`business.py:117-129`) re-runs the price-ratio loop of `Business.routes` (`business.py:436`).
7. **Two ways to see.**
   - `Vessels.in_sight` (for the lookout, `ships.py:2156`) and `Vessels.strangers_of` (for brains, `ships.py:1952`) repeat the same horizon, `seen_within`, night and visibility rules.
   - The wind at a place is computed three times: `Vessel._wind_at` (`ships.py:760`), `squadrons._wind_from_at` (`squadrons.py:1479`), and `regimes._wind_kn_at` (`regimes.py:253`), which falls back to the gusting `wind.speed` while the others use `base_speed`.
   - There are two port registries, `world.ports` (`Ports`) and `world.dealings` (`Dealings`), with differently shaped `stance` methods. My modules pick between them at random: `captains` and `ships.place_position` use `dealings`, while `brains`, `business` and `crews.far_order` use `ports`.
8. **Fish prices** live in `data/fishing/fish.yaml` (`price:`, `markets:`), while the ports' market tables also list "fish" and "pilchards", which the business uses to choose a home port (`business.py:697-698`).

## 5. Size and shape as a hazard

- **Longest functions:**

  | Function | Lines |
  |---|---|
  | `vessel_from_spec` (`ships.py:1509`) | 171 |
  | `Perception.read` (`captains.py:1627`) | 164 |
  | `far_order` (`crews.py:1107`) | 142 |
  | `Judgement._stimulus` (`captains.py:2013`) | 135 |
  | `_weather_work` (`captains.py:3415`) | 134 |
  | `read_intent` (`captains.py:770`) | 126 |
  | `Vessel.tick` (`ships.py:880`) | 117 |
  | `seats.hold` (`seats.py:310`) | 115 |
  | `_danger_ahead_by_chart` (`captains.py:3132`) | 101 |
  | `_passage` (`captains.py:3558`) | 99 |

- **Imports inside functions:** 255 across the 13 modules (`captains` 49, `ships` 56, `crews` 55, `seats` 22, `squadrons` 19, `business` 18, `brains` 15). Many of them dodge import cycles. For example, `captains` ends with a module `__getattr__` that lazily re-exports names from `brains` (`captains.py:4787-4795`), because `brains` imports `captains`.
- **The boundary.** `core/world.py` imports `world.captains` and `world.crews` (`core/world.py:1111, 1182`). The captain's tick calls `freesail.agents.harness.holder_of` (`captains.py:2624`). `crews` imports `freesail.agents.agent` and `harness` (`crews.py:825-826, 1547-1548`) and `freesail.api.session` (`crews.py:219`). `captains` and `crews` import `freesail.api.readings` (`captains.py:3150`, `crews.py:979`). So the simulation's tick reaches the agents and the API layer, hidden behind function-level imports. The rule "the simulation must not import from the agents" is not kept in fact, only in each file's top-level import lines.
- **The `Hull` façade** (`hulls.py:269-297`): `__getattr__` runs any World method with this hull made current through a context manager, which is global mutable "current hull" state. `bind_to_hull` (`hulls.py:432`) walks the hull's whole object graph and rewrites references by identity. A new object kept in a hull that holds a World or a clock gets silently rewritten or silently missed. This is the most dangerous piece to change.
- **Module-level caches:** the `lru_cache` on doctrine (16 entries, sized by hand to the number of roles, `captains.py:972-975`); `polar_of`, `rig_height_m` and `file_descriptions` (32 each, `ships.py:390-393`); `squadrons._BOOKS` (`squadrons.py:113`); `regimes._LOADED` (`regimes.py:38`, a global); `chart._tracks` and `chart._fishing_grounds`, attributes added to the chart from outside (`captains.py:1213`, `fishing.py:259`).
- **Switches kept for bisection:** module-level flags `HELM_IN_ACTION`, `ABACK_RECOVER`, `DANGER_AHEAD`, `ENGAGING_CHASE_STALE` (`captains.py:227, 451, 470, 477`) and `ADVERSARIAL_SEATS_CONSENTED` (`seats.py:76`).
- **Comments.** About 19% of lines are whole-line comments or docstrings (`captains` 20%, `ships` 22%, `hulls` 28%, `squadrons` 11%), and there are many trailing comments on top of that. History in place of explanation is heavy: "package N" appears 180 times in `captains.py`, 122 in `ships.py` and 58 in `crews.py`. Comments such as "the owner's merchantman, given to the pilot in the Goulet, was taken back from him..." (`captains.py:3945-3947`) record why a line exists, but rarely what it does. A newcomer reads three sentences of case history for every one sentence of rule. The `Vessel` field block (`ships.py:603-710`) is mostly such history.
- **Checkpoint compatibility** shapes the code throughout: class-level defaults, `getattr(..., None)` guards, and fields left out of `__getstate__` "so that none of them moves" (`ships.py:712-721`). This keeps every change from being a plain change.

## 6. Correctness and honesty

1. **A far fisherman's haul works on the player's ship.**
   - The call chain: `FarCaptain._fishing` → `fishing.far_work(self.world, ...)` and `trip_done_far` (`brains.py:655, 658`) → `haul_into(world, fishery)` (`fishing.py:942, 980`).
   - `haul_into` calls `rig_gear_drag(world, fishery)` (`fishing.py:754`) and `salt_aboard(world)` / `world.hold.break_out("salt", ...)` (`fishing.py:756-759`).
   - Here `world` is the game World, because the brain is made with it (`ships.py:1653`). The far brains tick with the followed hull current (`core/world.py:2392`, `1671`). `hold` and `ship` are per-ship façade fields (`hulls.py:130, 74`).
   - So the business's far smack salts her catch from the *player's* hold and takes the salt out of it. Her haul also removes the player's own trawl drag (`extra.pop("gear_drag")`, `fishing.py:1128`) while the player is towing.
   - Only one test names `haul_into`, and none names `far_work` with the player's own fishery.
   - Likely (by reading the whole chain; not run).
2. **Brain state lost across the promotion.**
   - `fold_in` and `fold_back` (`brains.py:861-957`) carry the intent, trend, stranger, spoken, recognised, pirates and given_up, but not `fired_on`. Yet `combat/action.py:266, 272` writes `fired_on` to whichever body is struck. A ship that fired on her is an enemy "whatever her colours" (`captains.py:1880-1882, 2211`), but only until the next promotion or demotion.
   - `fold_back` also drops `role`, `doctrine` and `_business`. A crewed captain whose intent changed role (`Captain.set_intent`, `captains.py:2476-2478`, for example by the squadron book's `_set_goal`, `squadrons.py:1009`) hands the far brain the new intent under the old doctrine. The fishing hours survive only because `captain_work` writes them into the *brain's* `_business` by hand (`fishing.py:1042-1043`).
   - Sure (by reading).
3. **A business-drawn blockade, blown off, sails for the Black Rocks.**
   - The blockade book's rule sets the goal "bound for {rendezvous}" (`data/squadrons/blockade.yaml`, rule `blown_off`).
   - `_set_goal` fills it with `self.rendezvous or self.destination_words(world)` (`squadrons.py:985`). The book's own `blown_off.rendezvous: Torbay` is never read (no `blown.get("rendezvous")` anywhere).
   - The business makes the Brest blockade from the plain entry `- brest` (`nations.yaml:62`), so `rendezvous=""` (`business.py:1059`).
   - `destination_words` then reads the goal "blockade Brest" through `read_intent`, whose destination is the port's `blockade_station` feature, `pierres-noires` (`captains.py:861-885`; `data/ports/brest.yaml:154`).
   - So in a westerly gale the squadron's intent becomes "bound for" the Black Rocks: toward a lee shore, not toward Torbay.
   - The truth that passes (`test_known_truths.py:9099-9113`) uses a scenario that names `rendezvous: Torbay` itself. `test_squadrons.py:545` stands in for the gale by setting the blockaders `done`.
   - Likely (by reading; not run).
4. **Perception is not as clean as the module says.** The docstring says "nothing here reads the world's truth" (`captains.py:39-43`). But `Captain` reads:
   - sail objects directly (`jib.is_set`, `captains.py:3018`; `ship.sails...is_set`, `3403`);
   - the struck state and prize records of other vessels from `world.vessels` (`2229-2234`, `4521-4533`);
   - the mark's true position in `_take_possession` (`world.position` and `v.position`, `captains.py:4556-4559`);
   - the well's true depth and the foundering tons (`4385-4404`);
   - the enemy's fit company for the boarding odds (`4327-4335`).

   These may be fair judgements, but the claim is overstated, and `test_captains.py`'s proof covers only part of it. Sure.
5. **Far brains know a stranger's true class at the horizon.** `strangers_of` sets `"size": _size_of(o)` from her description, whatever the level made out (`ships.py:1997, 2288-2296`). The near captain gets size only from the lookout's words (`captains.py:1688`), which are "a sail" (size 0) until the rig is made out at 4 miles. So `overmatched` fires for a far cruiser as soon as a frigate tops the horizon, but for the same cruiser crewed only at about 4 miles: her behaviour changes at the promotion ring. The far brain also judges by the *player's* visibility and daylight wherever she is (`brains.py:99-103`). Sure.
6. **The business stream is moved by the player.** The quay's rumour draws from the `business` stream (`business.py:1300-1306`) each time the player's boat brings prices. So whether the player sends a boat changes every later business draw. The head says the draw "moves no other draw" (`business.py:36-37`). That holds in one direction only. Replay stays deterministic. Sure.
7. **Doctrine loading does not validate stimuli.** An unknown name in `on:` or `unless:` evaluates to `False` forever (`captains.py:2147`); only the states are checked (`captains.py:999-1001`). Every name used today is known (census). The risk is a mistyped row in the owner's own edits, which nothing would catch. Low.
8. **Outcomes decided by rule, not simulation.** `far_captures` makes a merchantman struck by rule when an armed enemy at war is within 4 cables with no cover (`squadrons.py:1626-1691`), with no fight. The design says so (`squadrons.py:1544-1551`). It is honest, but the player can never cut one out this way: the player's shadow has no brain and is skipped (`squadrons.py:1583-1585`).
9. **Docstrings that name things that do not exist.** `Perception.of_vessel` (`brains.py:299`, `ships.py:1956`) does not exist; the function is `perceive_vessel`. `ships.py:21-27`'s level-of-detail account is out of date (see 4.1).
10. **Unsourced numbers.** Many figures say "judgement", which is honest. `crews.py:92-99`'s cap figures cite `docs/dev/TuningNotes.md`, which I may not open. `business.yaml`'s names and fleets are "from memory". Nothing in my part claims a source and then gives none.

## 7. Thin or overgrown

Overgrown at the near captain, thin at the far one.

- `Captain` carries about 2,000 lines of per-state hand work: deep-sea casts brought to once a watch, sail after the gale in three steps, aback recovery from Luce, stream re-laying, the lugger's taille-vent, boarding odds, repair priorities. That captain commands only the player's ship when nobody sits at its captain's station, and at most three crewed ships within 4 miles.
- The far body, which is most of the sea most of the time, has none of it: no rule of the road, no danger-ahead check (except for model-held hulls, `crews.far_dangers`), a polar and a plan.
- The data has also grown past the code that reads it (section 3): 12 threshold keys, half the squadron books, most of `regimes.yaml` and four `naval:` knobs are read by no one, while the files present themselves as the owner's tuning board.
- `seats` and `stations` are proportionate. `service` is small and sound.

## 8. What is not tested

- **No test names** (grep of `tests/`):
  - `Captain._rule_of_the_road` (only the pure `_road_rule` table is tested, `test_captains.py:377-394`; no test looks for a `captain.road` event);
  - `_haul_off`, `_take_possession`, `_boarding`, `_repairs`, `_musketry`, `_through_the_eye`;
  - `fold_back`, `keep_station`, `far_order`, `ask_crewed`, `far_dangers`, `_far_danger_ahead`;
  - `fishing.captain_work`, `land_far`, `sell_catch`, `ships.port_course`, `_off_the_land`;
  - `regimes.put_in_ordinary` (by name), `Business.draw_convoy`, `Business._commissions` (by name), `seats.voice_station`.

  Several of these are reached through scenario truths by behaviour (for example `box her off` in 4 files, `squadron.cut_out` in 3).
- **Behaviour the tests cannot see:**
  - the far haul's effect on the player's hold and drag (6.1);
  - `fired_on` across a promotion (6.2);
  - the business-drawn blockade's gale (6.3);
  - the cruiser's misplaced prize block (it matches the defaults, so no test could notice);
  - the change at the 4-mile ring in when `overmatched` fires (6.5).

## The ten findings that matter

1. **A far fisherman's haul salts from and strips the player's own ship.** `haul_into` and `rig_gear_drag` are called with the game World, so they use the followed hull's `hold` and `ship` (`brains.py:655-658` → `fishing.py:754-759, 1119-1128`; `core/world.py:2392`). Weight high (corrupts the player's stores and towing in business-on fishing play). Confidence likely.
2. **The business's Brest blockade, blown off by a westerly gale, sets "bound for" the Black Rocks, not Torbay.** The book's `blown_off.rendezvous` is unread, and the drawn squadron has no rendezvous (`squadrons.py:985, 1084-1105`; `business.py:1059`; `brest.yaml:154`). The truth that passes names its own rendezvous. Weight high. Confidence likely.
3. **"One brain, two bodies" leaks at the fold.** `fired_on`, `role`, `doctrine` and `_business` are not carried across promotion or demotion (`brains.py:861-957`; `combat/action.py:266-272`). Two role tables disagree (`captains.py:1021` against `brains.py:214`), and far brains see true class and the player's sky (`ships.py:1997`; `brains.py:99-103`). The same ship behaves differently inside and outside 4 miles. Weight medium-high. Confidence sure.
4. **Eight representations of a ship with three overlapping flags (`detail`, `shape` / `awake`, `crew` / `hull`).** The crewed ring (4 miles) sits outside the "near" ring (2 miles), so near detail is a leftover (`crews.py:90`; `ships.py:132`; `crews.py:359`). Weight medium (cost of understanding and of every change). Confidence sure.
5. **Doctrine-as-data is partly a dead switchboard.**
   - 12 threshold keys are read by no code (`mans_prizes` in 8 files; `road_cables`, `leg_reached_nm`, `anchor_within_nm` in 10).
   - The cruiser's whole prize block sits under `stations:` (`cruiser.yaml:111-148`).
   - Squadron books' `interval_cables`, `formation` and `straggler_minutes` are unread (`squadrons.py:617`).
   - Most of `regimes.yaml` and four `naval:` knobs are prose.

   Weight medium (the owner tunes things that do nothing). Confidence sure.
6. **Duplicated machinery that has already drifted.**
   - Three far-order performers (`crews.far_order`, `signals.far_perform`, `resolve_state`): a station at a sleeping hull cannot tack (`crews.py:1018`).
   - Two goal grammars and two place resolvers (`ships.py:1323, 1261`; `captains.py:770, 898`).
   - Three station geometries, only one guarded against the land (`ships.py:1365`; `brains.py:286`; `captains.py:4079`).
   - Six tables of "man of war" (`captains.py:200`; `squadrons.py:469, 1559-1563`; `regimes.py:193-198`; `brains.py:244`).

   Weight medium. Confidence sure.
7. **The simulation's tick reaches `freesail.agents` and `freesail.api` through function-level imports** (`captains.py:2624, 3150`; `crews.py:219, 825, 979, 1547`). There are 255 imports inside functions in this part, and a lazy `__getattr__` re-export works around the captains–brains cycle (`captains.py:4787`). The hard boundary is kept only on paper. Weight medium. Confidence sure.
8. **The `Hull` façade and `bind_to_hull`'s object-graph rewrite** (`hulls.py:269-297, 432-510`) make any new field held by a hull a silent hazard. Weight medium. Confidence likely (by reading; no failure shown).
9. **The near captain is overgrown and the far one thin.** About 2,000 lines of near `Captain._work`, against a far body with no rule of the road and no danger check (`captains.py:2984-4727` against `brains.py:611-637`). A further rule engine (squadron books) reuses stimulus names with other meanings (`squadrons.py:870` against `captains.py:2032`). Weight medium. Confidence sure.
10. **What the captain does on meeting the player is coarse and partly asleep.** Merchants react only once colours are made out at 2 miles. King's ships on passage ignore strangers entirely. The King's ship's and the commodore's `evading` and `overmatched` rows are dead, and would be a dead end if the 0 were raised (`kings-ship.yaml:77, 282, 318-329`; `captains.py:4616`). The rule of the road exists only when crewed. Weight low-medium. Confidence sure.

## What I did not read

- **Code:** all 13 modules were read whole. Outside my part I read only the slices cited: `core/world.py:1648-1687` and `2380-2399`, `combat/action.py:250-275`, `prizes.py:236-247` and `333-350`, `signals.py:1284-1324`. I did not read `signalling.py`, `prizes.py`, `captive.py`, `hail.py`, `combat/*`, the orders, or the standing runtime, although the captains call into all of them.
- **Data read whole:** `merchant.yaml`, `business.yaml`, `regimes.yaml`, and the three squadron books (their non-comment lines).
- **Data seen only partly:**
  - the other ten `data/captains` files: thresholds and transitions through a YAML dump, not their book texts or comments;
  - `nations.yaml`: lines 1-50, the `naval:` and `ports:` excerpts, and the key census;
  - `fishing/channel-west.yaml` and `fish.yaml`: the first non-comment parts only.
- **Data not opened:** `hail.yaml`, `fisherman.yaml`'s text, `fishing/biscay-north.yaml`, `data/crew/*.yaml` (`names`, `needs`, `ration`), `marines.yaml`.
- **Not done:** I ran no tests, and opened none of the tests beyond the excerpts cited (`test_known_truths.py:9099-9180`, `test_squadrons.py:530-575`, `conftest.py:255-270`).
