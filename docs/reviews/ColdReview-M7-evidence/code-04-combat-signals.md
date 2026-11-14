# Code reader 04: powder, prizes, signals and the lookout

Reader's part: all of `freesail/combat/` (13 files) and, in `freesail/world/`, `prizes.py`,
`prize_court.py`, `court.py`, `captive.py`, `ordnance.py`, `signals.py`, `signalling.py`,
`flags.py`, `hail.py`, `lookout.py`; their data, `data/signals/` (52 files) and the
`armament:` blocks of `data/ships/`. Tree at 504a25066c6995ce9829a19ffc597feb510a1870. No test
run, no file changed but this one. Two short python commands were run: one loading the six
signal roots to count their entries (`signals.load_books`), and an AST count of function
lengths and comment lines over the part.

## 0. The question the reviewer met in play: "firing as they bear already" with the guns secured

**Where it is said.** `freesail/orders/gunnery.py:539-554`, `_mode`. When the battery's mode is
already the one asked, it answers `f"The guns are {'holding their fire' if ... else f'firing
{mode}'} already."` (548-549), which for `FireMode.AS_THEY_BEAR` (`combat/guns.py:76`) reads
"The guns are firing as they bear already."

**Why the mode was already set.** The order before it, `engage her to starboard`, went to
`_engage` (gunnery.py:331-371), which silently turns a battery in `HOLD` (the default,
`guns.py:308`) into `AS_THEY_BEAR` and says so in its reply: "Engage ... to starboard: the mark
..., the starboard battery, the guns to fire as they bear" (355-357, 367). So the second order
found the intention already standing and answered "already".

**Why nothing warned that the guns were secured.** No order of the gun deck but one reads
`Gun.cast_loose`:

- The gate for every gun-deck order (gunnery.py:254-259) checks only `quarters.at_quarters`.
  Its refusal says "beat to quarters ... and cast loose the guns", but once the hands are at
  quarters it lets everything through with the guns still secured.
- `_engage` (331-371), `_mode` (539-554) and `_fire` (787-858) never look at `cast_loose`.
  `fire` with secured guns answers "no gun of it is loaded and run out yet; the word stands
  until one bears" (850-851): a word that will stand for ever. `fire a shot across her bows`
  chooses a gun from the cast-loose guns and, finding none, from any serving gun
  (`_a_gun_for_a_signal`, 862-864); that secured gun is put in `battery.single` and never
  becomes ready, so the order hangs there.
- The one place that warns is the practice order `exercise the guns`: "The guns are not yet
  cast loose: say 'cast loose the guns'." (gunnery.py:1246-1247). The pattern exists and was
  not applied to `engage`, the fire modes or `fire`.
- The battery itself is silent by construction: `Battery.serving` returns False for a gun not
  cast loose (`guns.py:335`), so `tick` gives it no work (491-492) and `_fire`'s `ready` list is
  always empty (861-871); `minute_line` returns None when nothing was fired (1059-1060), so the
  log carries nothing at all, minute after minute, for an hour.
- The reading `the guns` hides the contradiction: when no gun is cast loose it prints only the
  kinds and "secured" (`api/action_readings.py:163-179`); the engaged side and the mode are
  printed only inside `if cast:`. So the reading said "secured" while the battery held "engaged
  to starboard, firing as they bear", and neither told the player the other.

**Is beating to quarters meant to cast the guns loose?** No, by design it is a separate order,
and the code is consistent about that:

- `beat to quarters` is a crew order (`orders/crew.py:216-241`): it turns up the hands and
  assigns the quarter bill (`crew/quarters.py:196-290`) and touches no gun.
- `clear for action` ends by beating to quarters and nothing more (`evolutions/action_scripts.py:
  100-136`).
- Casting loose is its own evolution, `CastLooseScript` (`action_scripts.py:157-187`;
  `data/evolutions/cast_loose_guns.yaml`, "Wanted at quarters; refused in words before the
  beat"), the only code that sets `Gun.cast_loose = True` (182).
- The scenario's own head lists the two orders separately (`data/scenarios/first-action.yaml:
  20-22`); the rules captain gives both in turn (`world/captains.py:4177-4180`); every test that
  engages casts loose first (`tests/test_known_truths.py:8524-8527`, `tests/browser_plans/
  action.yaml:8-15`). No test exercises `engage` or `fire as they bear` with the guns secured.

So the two-order design is intended, matches the period's drill, and is tested on the path the
rules captain takes; the defect is that the player's path is not, and the game answers the
player with a statement that is false ("the guns are firing") rather than the one sentence it
already has for the dumb show. Weight high (the reviewer lost an action to it with no word from
the game), confidence sure. Joining it: one check in `_engage`, `_mode` and `_fire` appending
the 1247 sentence, or a line from the battery's minute when it is engaged with nothing cast
loose.

## 1. What it is

**In the game.** The great guns' service and fire, the fall of shot into the mark's parts and
men, the strike by morale, musketry and boarding, the fight between sleeping ships, the lee
ports, practice at a cask, the gunner's filling of cartridges, powder and shot taken in at a
port; the prize possessed, the prisoners and their rising, the captive player, the prize court
and its money, the court martial and a new command; colours, flags of command, signal books
(numerary, telegraphic, night, fog, convoy, private), dressing ship and the nations' days; the
hail; and the lookout (land, dangers, sail, the glass).

**Size.** `freesail/combat/`: 13 files, 5,866 lines (`guns.py` 1,225, `boarding.py` 775,
`action.py` 609, `far_action.py` 560, `hits.py` 548, `marks.py` 526, `small_arms.py` 438,
`far.py` 325, `ports.py` 244, `filling.py` 229, `shot.py` 216, `morale.py` 165). The world
files: 11,954 lines (`lookout.py` 2,241, `prizes.py` 1,693, `signals.py` 1,629, `flags.py`
1,264, `captive.py` 1,061, `court.py` 960, `signalling.py` 960, `ordnance.py` 838, `hail.py`
656, `prize_court.py` 652). In all 17,820 lines; comment and docstring lines about 17% of them
(1,094 comment lines, 2,022 docstring lines). Beside it, not mine but its front: `orders/
gunnery.py` 1,437, `orders/signals.py` 1,258, `orders/fight.py` 238, `orders/prize.py` 242.

**Data.** `data/signals/`: 52 files, 6,554 lines, six roots (basic, britain, france, naples,
spain, united-states), each with `book`, `numerary`, `telegraphic`, `night_fog`, `convoy`,
`private`, `colours`, `flags`, and some `dressing` and `days`. Loaded, they hold 997 signal
entries: 487 whose `does` is an order, 302 news, 89 a state, 67 an answer, 17 a release, 9
"closer", 26 nothing (python over `signals.load_books`). Of the numerary entries, 297 of 515
are marked `made: true` (the builder's numbers). Britain's telegraphic dictionary is 1,496
lines. The guns: the `armament:` blocks of 13 ship files, about 7,400 lines and 612 gun
entries (the seventy-four's alone 2,717 lines, 234 guns over three fits). The frigate's
armament is marked in its own file as INCORRECT on the quarterdeck "pending correction"
(`data/ships/frigate-36.yaml:2694`, 2698).

**Main types and functions.** `guns.Battery` (the per-ship runtime: intentions, per-gun
`Service` state machine, `tick`, `_fire`, `_discharge`, `minute_line`), `guns.Target`,
`guns.Firer`; `shot.ballistics_of`, `hit_chance`; `hits.resolve_shot` and `Damage`;
`morale.Morale`; `action.tick_action` (called from `core/world.py:2397-2399` for every awake
World), `action.strike`; `boarding.Fight`, `boarding.tick`; `small_arms.tick`; `far.FarShip`,
`far.round_once`; `far_action.minute` (called from `world/ships.py:1803`);
`prizes.possess`, `retake`, `burn`, `minute`; `prize_court.sentence`; `captive.player_taken`,
`cartel_minute`; `court.sit`, `verdict`, `new_command`; `ordnance.take_in`, `apply_job`;
`signals.Books`, `Hoist`, `Locker`, `read_flying`, `far_perform`; `signalling.near_minute`,
`far_minute`; `flags.flies`, `dressing_flies`; `hail.hail_order`, `answer_by_table`;
`lookout.Lookout.look`, `strangers`, `find`, `sail_named`.

**What the player sees.** The log's lines ("Five shot at the brig: two struck her, ..."; "Shot
from the cutter: a shot through the side to starboard; one killed"), the readings `the guns`,
`the damage`, `the bill`, `the enemy`, `the range`, `the strangers`, `what is in sight`, `the
signals`, `the prizes`; the hail's answers; the viewer's flags.

**Tests that belong to it** (grep of tests for imports and order words): `test_known_truths.py`
(17,391 lines; truths 7-133 onward are the action's, e.g. 8121-8530), `test_lee_ports.py`
1,937, `test_ports.py` 2,401 (ports of call and the lee ports both), `test_ordnance.py` 966,
`test_practice_orders.py` 908, `test_signals.py` 754, `test_flag_drawings.py` 694,
`test_captive.py` 629, `test_practice.py` 627, `test_court.py` 510, `test_dumb_show.py` 506,
`test_fight.py` 505, `test_powder_orders.py` 504, `test_filling.py` 501, `test_prizes.py` 470,
`test_lookout.py` 457, `test_prize_court.py` 400, `test_far_action.py` 368, `test_flags.py`
321, `test_pivot_gun.py` 217, `test_far_hail.py` 142. Module imports: `combat.guns` in 25 test
files, `combat.action` 23, `world.lookout` 14, `combat.hits` and `combat.ports` and
`world.prizes` 13 each; `combat.small_arms`, `combat.far_action` 2 each; `world.ordnance`,
`world.court`, `world.prize_court` 1 each.

## 2. Is it reached?

The near action is reached every tick: `core/world.py:2397-2399` calls `tick_action`, which
serves the battery, the small arms and the boarding (`action.py:66-132`). The far fight is
reached once a minute from `world/ships.py:1803`. Prizes, captive, court, ordnance and
signalling are reached through the world's minute, the orders and the director's forms. The
lookout is the World's every minute. Dead or unread, each by grep over `freesail/`:

- **`hits._far_hit`'s sums are written and never read.** A near gun that strikes a far vessel
  adds `damage["hits"]` and `damage["weight_lb"]` (`hits.py:424-427`). No code reads either key
  (grep of `"hits"` and `weight_lb` over `freesail/`: only these two lines). The far fight reads
  `killed, wounded, dismounted, holes, holes_below, sail_cut, spars_gone, morale`
  (`far_action.py:72`, 158-169). So when the crews' cap leaves the mark asleep, the player's
  shot that "struck her" does nothing to her at all: no man hurt, no morale lost, no strike;
  while her reply by the tables does land in his parts (`far_action.py:359-443`). The module's
  head says the opposite: "the awake hull's battery fires at the far mark by 70's road already
  (`hits._far_hit` sums into the far record)" (far_action.py:21-23). No test touches
  `_far_hit` or `weight_lb`. Weight medium-high, sure.
- `Gun.elevation_deg` (`ship/parts.py:544`) is never read: the quoin is computed afresh at each
  discharge (`guns.py:1013-1016`). Sure.
- `Gun.condition` is lowered by a shot on the carriage (`hits.py:260`) and read by nothing in
  combat: a "wounded" carriage serves and fires as a whole one. Sure.
- `captive.CARTEL_SPEED_KN` (`captive.py:164`) is defined and never used. Sure.
- `ship.extra["boats_stove"]` (`hits.py:225`) is read only by a reading (`api/
  action_readings.py:318`); the boats module knows a lost boat by `BoatState.lost`
  (`world/boats.py:893-929`) and never reads this list, so a boat stove by shot can still be
  hoisted out and manned (see 3). Sure.
- `far.fight` (the measure loop, `far.py:308-325`) is reached only by tests
  (`test_known_truths.py:8448`, 14569); the world runs `round_once`. Acceptable as a measure.
- Switches always True and never set by anything but tests: `far_action.ENABLED`,
  `signalling.CHALLENGES`, `DOCTRINE_COLOURS`, `TRUE_COLOURS_HELD`, `flags.FLAGS_SPOKEN`,
  `lookout.SAIL_BY_NAME`. They are bisection toggles; they add a branch to every caller.

## 3. Built more than once

- **The strike is written in five places, with two types.** `action.strike` writes
  `extra["struck"] = tick`, the colours, `vessel.struck`, the sharers and the captain's state
  (`action.py:484-533`); the gunnery fallback writes `extra["struck"] = True` and `set_colours(...,
  None, ..., 0)` (`orders/gunnery.py:939-944`); `boarding._end` with no defender's World writes
  `extra["struck"] = tick` and nothing else (`boarding.py:575-576`); `far_action._strike` writes
  `vessel.struck`, `damage["struck_tick"]`, the colours, `state`, `plan`, the brain
  (`far_action.py:318-356`); `world/orders._taken` calls `action.strike` and then sets
  `taken.struck` itself (`world/orders.py:716-718`). An int tick and a bool share one key, and
  a strike at tick 0 reads as not struck everywhere `extra.get("struck")` is tested. Joining:
  one `strike(vessel_or_world, ...)` that the far side calls too.
- **Morale twice.** `Morale.judge` (`morale.py:81-121`) and `far._judge` (`far.py:262-278`)
  carry the same formula with their own reading of the masts ("a spar at far detail is not a
  lower mast", `min(1, spars_gone/3)*0.5`) and no repulses. The weights are imported, the law
  is copied.
- **The broadside's weight four times.** "Starboard broadside guns and every non-broadside gun"
  is summed in `action._enemy_weight` (453), `action._far_weight` (471), `morale.judge` (105)
  and `far.file_figures` (114-117). A pivot counts once; a pair of swivels counts both sides.
- **The gun's cycle twice.** `guns.Battery._phases` and `_factor` (602-607, 539-559) and
  `far._cycle_s`, `_crew_factor` (142-159). The far crew factor is the company's fit share, the
  near one the men at the gun; both raise the shortfall to `NUMBERS_POWER`.
- **The boarding round three times.** `boarding._round` (498-553), the prize rising's own loop
  of up to 15 rounds in one tick (`prizes._rise`, 1435-1509, which reaches into
  `boarding._strength`, `_poisson`, `ROUND_LOSS`), and the far rising by counts, which has no
  fight at all: if the hourly draw passes, the prize is retaken (`prizes.far_minute`,
  1668-1692). In `_rise` the prize crew's casualties go through `hit_man` but the prisoners'
  are written directly (`s.fit = False; s.hurt = ...`, 1473-1479), bypassing the health keeper.
- **A shot's damage to a sail two ways.** Near: `Sail.holed_m2` (`hits.py:302`), read by the
  aerodynamics (`physics/sails.py:609`). Far record carried into a woken hull: `condition`
  lowered by `sail_cut * 100` (`far_action.py:544-548`). A spar gone at far detail is set
  `wrecked = True` directly (`far_action.py:550-554`), not through `strain._wreck_spar`, so its
  yards and sails are not wrecked with it as they are when a near shot takes it
  (`physics/strain.py:613-628`). The far carry-in also fixes every hole at 0.12 m and
  12 pounds (536-538) and dismounts "from the end of the engaged side" by reversing the gun dict
  (519-521), which is not the engaged side.
- **Two Poisson samplers and a third.** `hits._poisson` (409-418), `small_arms._poisson`
  (190-201), `boarding._poisson` (143-154, a different cap, 60), and `far._men` inline
  (246-259). Same code, three caps.
- **Finding a sail by words, four ways.** `orders/gunnery._mark` (374-413: substring both ways
  on id, known words, name, kind, what), `hail._addressee` (161-226: in sight first, then name,
  kind, `lookout.sail_named`, then the whole sea by `sea.find`), `Lookout.find` (1419-1476:
  `_SAIL_WORDS`, `_RIG_WORDS`) and `Lookout.sail_named` (1480-1497). They differ: `engage the
  brig` matches "brig" inside "brig-sloop" by substring; `hail the brig` matches the kind
  exactly first; a name reaches beyond sight for the hail and not for the guns.
- **Nations read from words in code beside the data.** `hail.nation_in_words` hard-codes
  "his majesty" to Britain, "republic" or "national" to France and so on (`hail.py:81-94`)
  before it reads the nations table; captains' names for a liar are hard-coded lists in code
  (`hail.py:569-575`) while the ports and the lies' ship names are in `data/captains/hail.yaml`.
- **A second order parser for far bodies.** `signals.far_perform` (1284-1420) reads tack, wear,
  heave to, anchor, steer, close the flag, colours and lights in its own words, a parallel to
  the orders grammar the near body uses. Of the 44 distinct orders the signal books give, the
  far body performs the subset it lists; "beat to quarters", "clear for action", "scud",
  "moor", "heave the lead" and the rest return "" there (no line, no effect).
- **The galley fire twice.** `ClearForActionScript` says "The galley fire is out" and sets
  nothing (`action_scripts.py:128-129`); the powder's state is `Stores.galley_fire_out`, set only
  by the hoy (`ordnance.py:570`) and read by the filling and the meals (`filling.py:107`,
  `world/needs.py:791-793`).
- **The ladder of standing three times.** `prizes.LADDER` ("first lieutenant", "lieutenant",
  "mate", "master's mate", "midshipman", `prizes.py:90`), `boarding.boarders_officer`'s
  ("first lieutenant", "lieutenant", "mate", `boarding.py:632`) and `prize_master`'s default
  ("lieutenant", "mate", "master's mate", "midshipman", "petty officer", 346).
- **A boat stove twice** (see 2): shot's `extra["boats_stove"]` against `BoatState.lost`.
- **Two random systems.** The private table and the hail's fills use `random.Random(zlib.crc32(
  ...))` (`signals.py:503`, `hail.py:488`) beside the World's named streams. Deterministic, but
  outside the streams the rest of the simulation is audited by.

## 4. Size and shape as a hazard

Longest functions (AST): `prize_court.sentence` 192 lines, `prizes.possess` 150,
`Lookout.look` 146, `signals.far_perform` 137, `signalling._judge_challenges` 136,
`court.new_command` 133, `ordnance.take_in` 127, `signals.read_flying` 122 (11 parameters),
`guns.Battery._work` 116, `prizes.retake` 103. Many-parameter functions: `hits._deck_hit` and
`_hull_hit` 11 each, `signals.make_private` 11, `far_action._into_parts` 10,
`guns._discharge` 9. `_work` is a phase state machine with a `while` inside a `while` and five
special cases (dumb show, shut port, loaded, swivel, cartridge wait); a change there is the most
dangerous edit in the part.

Imports inside functions: 234 in this part (`prizes.py` 39, `captive.py` 26, `boarding.py` 22,
`far_action.py` 19, `marks.py` 16, `court.py` 15, `ordnance.py` and `lookout.py` 14 each),
mostly to dodge cycles between `combat`, `world` and `orders`. Bare `except Exception` 57
(`prizes.py` 13, `signalling.py` 12, `hail.py` 7): in `signalling` every order a rules captain
gives by signal is wrapped in one (`_answer`, `_obey`, `_challenge_strangers`,
`fog_signals_minute`), so a signal that fails to become an order fails silently.

State hung on objects by `getattr(self, "_x", {})` and `hasattr` rather than declared:
`Lookout._sail_ident`, `_colours_said` (`lookout.py:720-721`, 786-788, 819-821),
`Prisoners.landed` (`captive.py:839`), `Battery` class defaults for pickling (`guns.py:276-298`).
Module caches: `@cache` on `load_books`, `load_colours`, `load_signal_flags`, `load_dressing`,
`load_days`, `hail._table`; `lru_cache` on `far.file_figures`, `far_action._fit_has_guns`,
`_fit_reach_m`; a module-level mutable counter `far_action.FALLBACK_COUNT` (70), incremented in
play and never reset.

Comments carrying history: 213 lines name a package, the owner, the lead or a ruling. Examples
of history in place of explanation: `guns.py:129-146` (eighteen lines on the pivot's arc's
rulings before the two constants), `ports.py:16-23`, 46-52 (the line counts of other tests that
moved), `hail.py:391-395` ("the playtest of 2026-10-27: called as a method, the TypeError was
swallowed"). The docstrings are long and accurate more often than not, but a newcomer must read
three sentences of provenance for each sentence of rule.

The lookout reads the world's log to learn names: `_identify` scans `world.log` backwards for
`hail.answered` and `hail.heard` entries and parses their text (`lookout.py:746-777`,
`_name_in` 1831-1844). The log is the narrative; here it is also a data bus, so rewording a
hail's line can change whom the deck knows by name.

## 5. Correctness and honesty

**Follow one round shot** (`engage her to starboard`, the guns cast loose, `fire as they
bear`). The order sets `battery.target`, `engaged`, `mode` (`gunnery.py:341-357`). Each tick
`tick_action` builds the `Target` from the mark's body (her crewed World's `Ship` when she is
awake, else the far `Vessel`, `action.py:138-185`) and the `Firer` (214-226). `Battery.tick`
shuts or opens the lee ports (`ports.update`), then for each pair of guns finds the men at it
from the quarter bill, refuses under half a crew, and works the phases at the crew factor
(`guns.py:477-505`); at the cartridge phase a filled cartridge and the shot are taken from the
magazine (640-681). When a gun is loaded, run out and primed, bears within its arc, is of the
engaged side and the mark is within its random shot, it fires (861-882). `_discharge` lays the
quoin for the range, adds or takes the heel by lee or weather, computes the shot's reach, the
platform's scatter from the roll and the sea, the mark's aspect, the crew's aim, and draws once
for "struck" against `hit_chance` (1008-1039). There is no flight: the fall is resolved in the
same tick (the module head's "the shot's flight is shot.py's", `guns.py:24`, names a flight
that does not exist). A struck shot goes to `hits.resolve_shot`, which divides it by the aim's
shares into hull, deck or rigging (`hits.py:141-166`) and writes state: a hole into
`Damage.holes` (read by the well, `world/water.py:266`, and the carpenter, `evolutions/
repair_scripts.py:173`), a gun dismounted (`Gun.dismounted`, which `Gun.serves` reads,
`parts.py:615-617`), a line parted through `strain._part_line` and a spar through
`strain._wreck_spar` (`hits.py:294`, 312), a sail holed through `holed_m2`, men through the
health keeper (`hit_man`, 392-406). The firer's minute line says what his people could see;
the mark's own World writes her minute line and judges her morale (`action.py:370-443`).

**"Combat is another set of evolutions and parts, not a separate system"; "damage is just
state".** Largely true for the near fight on the rigging, the hull and the men: a halyard shot
away is the same call with `how="shot away"` as one parted by strain, and a spar wounded by
shot loses `condition` that the strain then reads (`physics/strain.py:250-251`). Not true in
four places:

- **The wheel shot away is a flag that never clears.** `hits.py:212-221` sets
  `extra["helm_lost"]` and says "the helm is lost until the relieving tackles are rove";
  `physics/hull.py:551-554` then holds the rudder where it was. Nothing in `freesail/` or
  `data/evolutions/` reeves relieving tackles or clears the key (grep of `helm_lost`,
  "relieving", "wheel": readers only). A ship whose wheel is shot away steers by her last rudder
  angle for the rest of the game, player or enemy; no test covers it (grep of tests for
  `helm_lost`, `helm.shot_away`: none). It is not a part of the graph that some other cause
  could also break. Weight high, sure.
- A boat stove by shot is a list nobody honours (sections 2, 3).
- A carriage wounded by shot is a number nobody reads (section 2).
- The far fight is not parts at all: counts on a dict, carried into parts by different rules
  when she wakes (section 3).

The `cast_loose` evolution is an evolution, the beat is a crew order, but the guns' service is
"no evolution's but the battery's own cycle" (`action_scripts.py:7-8`): the work that most
competes for hands in action does not go through the runner. The filling of cartridges takes
"no hands from other work", said honestly as a stopgap (`filling.py:14-18`).

**One fight model or several.** Several, by the shape of the two ships:
(a) both awake: the per-gun cycle and the part graph (`guns.py`, `hits.py`); (b) awake firer,
far mark: the near cycle firing into `_far_hit`'s dead sums (section 2); (c) both asleep:
`far.round_once` every three minutes, beam-on, aim 1.0, no heel, no ports, no roll
(`far.py:174-204`); (d) far firer, awake mark, the cap full: the tables' hits each resolved into
the awake parts by a synthetic gun of her heaviest calibre, with "between wind and water"
mapped to the rigging (`far_action.py:424-429`: `H.Aim.HULL if fa.aim == "hull" else
H.Aim.RIGGING`); (e) the far record poured into a hull when she wakes (`far_damage_into_parts`).
The musketry and the boarding work only between two awake decks (`small_arms.py:298-300`,
`boarding.py:356-357`). The result is that the same two ships fight differently by how many
other ships the cap has woken.

**Boarding, the strike and the prize.**
- The boarders never leave their guns. `boarders_of` recomputes the party every round from the
  attacker's muster by skill (`boarding.py:242-275`); nothing moves a man's `at` or his quarters,
  so the same men serve the battery (`guns.py:494`) and fight on the enemy's deck. Their losses
  are drawn not from the party but from the attacker's "exposed" men by `strike_a_man`
  (`small_arms.py:211-278`; `boarding.py:513-515`). Weight medium, sure.
- `repel boarders` sets `Musketry.repelling = True` and the battery to `HOLD`
  (`boarding.py:718-722`) and nothing ever sets it False (grep: no assignment of False outside
  the dataclass default). Its docstring says "until the guns are cast loose again" (706-707);
  `CastLooseScript` does not touch it. The guns are not silenced, only their mode: `fire as they
  bear` fires them with the gun crews notionally at the gangways. No test calls `repel` (grep).
  Weight medium, sure.
- The deck carried is struck by `action.strike` and possessed by `prizes.possess` in one
  function whatever the road (`boarding.py:686-702`, `prizes.py:655-804`). That is sound: one
  possession for the strike, the boarders, the far body at hail and the director's form.
- The player's own `strike the colours` says "What follows (the prize crew, the prisoners, the
  captive's channel) is not in this game yet" (`orders/gunnery.py:946-949`), though `possess`
  and `captive.player_taken` (`captive.py:306-381`) are built and tested (`tests/
  test_captive.py`). `morale.py:27-28` says the same of package 74. Stale words the player
  reads. Weight medium, sure.
- The player's ship strikes by rule too: `_judge_morale` runs for every awake World, the
  player's included, with the default 0.7 start and 0.3 line where the World has no captain's
  doctrine (`action.py:426-443`, `morale.py:63-64`, 151-165). That may be intended (rule 7);
  nothing in the orders says the player's colours can come down without his word. Suspicion as
  to intent; sure as to the code.
- The prize's rising uses "the captor's temper" from `rec.get("morale", 0.7)`
  (`prizes.py:1449`); no code writes `"morale"` into a prize record (grep), so it is always 0.7.
  The far rising always succeeds when its hourly draw passes (1677-1683). Low, sure.

**Prize court.** `valuation` prices any vessel whose description lacks the word "merchant" as a
man of war (`prize_court.py:153-155`), so a cutter, lugger or smack carrying fish is a man of
war's hull at the man-of-war rate. The neutral-carrying-enemy-cargo test looks for an enemy
nation's id inside the prize's old intent words (`any(e in goal.lower() for e in enemies)`,
347): intents name ports ("carry wine to Brest"), not nation ids, so the condemnation by cargo
will rarely if ever fire. Low-medium, likely.

**Ordnance.** When the purse is short at the hoy's coming alongside, `_alongside` records the
miss and returns without `_hoy_home` (`ordnance.py:553-563`), unlike the "gone" branch
(542-550); the hoy vessel put on the sea at the demand (`_hoy_off`) is left with its plan to the
ship. Low, likely.

**Signals that cannot be obeyed.** Britain's Nos. 31 and 32 and France's 16 and 17 have `does:
{order: "engage from to windward"}` / `"... to leeward"` (`data/signals/britain/numerary.yaml:
68-69`, `france/numerary.yaml:29-30`). `_engage` reads "from to windward" as a sail's name and
refuses ("No sail in sight answers to ...", `gunnery.py:404-413`), and `signalling._obey`
swallows the refusal (`signalling.py:336-341`). Likely (read, not run).

**Comments and the code.** `hits.py:9-11` names `ship.extra["shot_holes"]` and says "no water
flows from it here"; the holes are in `extra["damage"].holes` and `world/water.py` now floods
through them. `far_action.py:21-23` claims `_far_hit` feeds the far record (it does not).
`boarding.py:706-707` (above). `guns.py:24` (the flight). Each a small finding; together they
show the module heads were written once and not kept.

**The hard boundary.** `combat/` imports nothing from `agents`, `api`, `ui` or `client`; it does
import `orders.prompt` and `orders.errors` (`hits.py:367`, `boarding.py:198`, ...). The world
files in my part import `agents` inside functions nine times: `prizes.py:512`, 1123;
`captive.py:560-561`; `flags.py:1210-1211`; `hail.py:371`, 402; `court.py:777`
(`agents.remote.SAVES_DIR`). If `world` is held to the simulation's side of the boundary, these
cross it; the imports are local, which hides them from an import-graph check.

**Nondeterminism.** None found in the action: the gunnery's stream is opened lazily per World,
the quarterdeck's share on the health stream (`hits.py:363-370`), sets are sorted before
logging (`ports.py:183-191`). `hits._clock_of` falls back to `datetime(1805, 6, 1, 4, 0)` when
no runner has a clock (539-544): a fake time in a simulation path, harmless in play.

**Figures and sources.** The ballistics are "from memory and UNVERIFIED against a page"
(`shot.py:13-14`, 81-92); the hit chances, casualty means and dismount odds are judgements
(`hits.py:49-103`); the boarding's every figure is judgement (`boarding.py:33-35`). The files
say so plainly. That is honest, and it means the fight's outcomes rest on about forty untested
numbers.

## 6. Thin or overgrown

Overgrown against what it serves. The signals and flags are 3,853 lines of code here (plus
1,258 in `orders/signals.py` and 206 in `api/viewer_flags.py`) and 6,554 lines of data: six
roots of books with 997 entries, flag drawings sourced leaf by leaf, dressing ship by the
fashion of the year, the nations' days with a first lieutenant's reminder (`flags.py:1201-1235`).
In play, ten of 69 scenarios name a squadron, a convoy, ships under orders or the private
signals (grep of `data/scenarios/`); 297 of 515 numerary numbers are the builder's own. Of the
487 entries that carry an order, the near body gives them through the full grammar but the far
body performs only `far_perform`'s list. The private signal and colours do real work (they
decide recognition before fire, `action._recognition`, `signalling._judge_challenges`); the
dressing, the days, the telegraphic dictionary's derived word forms (`signals._entry_forms`,
287-321) and the drawn flags serve the viewer and the record far more than play.

The parole's reading of the captive's words is 60 lines of negations, yes-words and regex in
three languages (`captive.py:96-160`, 712-740) for one question asked once per capture. The
court martial writes a scenario file from a world order (`court.py:788-920`), a career feature
the code itself says is M8's.

Thin where the game leans on it: the far fight, which settles every action the cap does not
wake, is 325 lines with no heel, no ports, no roll, no aim by crew and a beam-on aspect, and its
damage does not join the parts' state (section 3). The near fight is detailed and mostly
coherent; it is the joins between its models that are thin.

## 7. What is not tested

By grep of `tests/` for the names and their log kinds: the wheel shot away (`helm_lost`,
`helm.shot_away`): none. `hits._far_hit`, `weight_lb`: none. `boarding.repel` and the
`repelling` state: only "repel boarders" text in `test_fight.py`, no call that checks the guns or
the flag's end. A boat stove by shot (`boats_stove`): none (the `boat.stove` hits are the
director's in `test_boat_director.py`). `captive.cartel_doubt`, `CARTEL_SPEED_KN`: none.
`engage`, `fire as they bear`, `fire` with the hands at quarters and the guns secured: none
(every engaging test casts loose first). The signals whose orders do not parse ("engage from to
windward"): none. `prize_court.verdict`'s cargo branch: not found in `test_prize_court.py`'s
names (I did not read that file whole). The far-body fallback reply's mapping of "between" to
the rigging: `test_far_action.py` counts `FALLBACK_COUNT` but I found no assertion on the aim.

Behaviour a player meets that the tests cannot see: the false "already" answers of the gun deck
(section 0), the silence of a battery that cannot fire, the "not in this game yet" line after a
strike, a rudder frozen for good.

## The ten findings that matter

1. **The gun deck lies to a player whose guns are secured.** `engage` sets `AS_THEY_BEAR`
   (`orders/gunnery.py:355-357`), `fire as they bear` then answers "The guns are firing as they
   bear already" (548-549), `fire` says "the word stands until one bears" (850-851), and no
   order or minute line says the guns are not cast loose, though the sentence exists for the dumb
   show (1246-1247) and the reading hides the intention while "secured" (`api/action_readings.py:
   163-179`). Beating to quarters is by design not casting loose (`orders/crew.py:216-241`,
   `evolutions/action_scripts.py:157-187`). Untested path. High, sure.
2. **A wheel shot away is lost for good.** `hits.py:212-221` sets `helm_lost`, `physics/
   hull.py:551-554` freezes the rudder, and nothing clears it or reeves relieving tackles, though
   the line promises them. Untested. High, sure.
3. **The player's shot into a sleeping mark does nothing.** `hits._far_hit` writes `hits` and
   `weight_lb` that no code reads (`hits.py:424-427`; `far_action.py:72`, 158-169), while her
   reply by the tables lands in his parts (`far_action.py:359-443`); the module head claims the
   sums are used (21-23). Medium-high, sure.
4. **Five fight models by the cap's whim, not one.** Near-near, near-far, far-far, far-near
   fallback and the far record poured in on waking each resolve damage differently (sections 3,
   5), with morale, the broadside weight, the cycle and the boarding round each written two to
   four times. Medium, sure.
5. **"Damage is just state" holds for lines, spars, sails, holes and men in the near fight and
   fails elsewhere:** the helm is a flag (2), a boat stove is an unread list (`hits.py:225`
   against `world/boats.py:893-929`), a carriage's wound is unread (`hits.py:260`), and the far
   carry-in wrecks spars without their dependents and cuts sails by `condition`
   (`far_action.py:544-554`). Medium, sure.
6. **Boarders never leave the guns, and `repel boarders` never ends.** `boarding.py:242-275`
   moves no man; `repelling` is never set False (`boarding.py:718`), its docstring's end
   (706-707) is not built, and the guns can still fire. Untested. Medium, sure.
7. **The strike is written five ways with an int and a bool in one key.** `action.py:489`,
   `orders/gunnery.py:940`, `boarding.py:576`, `far_action.py:318-338`, `world/orders.py:716-718`.
   Medium, sure.
8. **Stale words to the player and the reader.** "What follows ... is not in this game yet"
   after a strike (`orders/gunnery.py:946-949`) with possession and the captive built; module
   heads naming a key that does not exist (`hits.py:9-11`) and a flight that does not happen
   (`guns.py:24`). Medium, sure.
9. **Signals overgrown against play, and partly unobeyable.** 3,853 lines of signal and flag code
   in this part and 6,554 lines of data, most numbers the builder's, dressing ship and the days
   for the viewer; ten scenarios of 69 use squadrons or orders; the far body performs a fraction
   of the 44 orders, and "engage from to windward" (four entries) cannot parse, its refusal
   swallowed (`signalling.py:336-341`). Medium, likely.
10. **Hazardous shape.** 234 imports inside functions, 57 bare `except Exception` (12 in
    `signalling.py` around every order a signal gives), functions to 192 lines and 11
    parameters, the lookout learning names by parsing the log's text (`lookout.py:746-777`),
    and nine local imports from `agents` in world code (`prizes.py:512`, `captive.py:560-561`,
    `flags.py:1210-1211`, `hail.py:371`, 402, `court.py:777`). Medium, sure.

## What I did not read

Read whole: every file of `freesail/combat/` and the ten world files named. Read in part, as
callers: `orders/gunnery.py` (1-120, 240-570, 770-951, 954-1020), `orders/crew.py` (120-253),
`evolutions/action_scripts.py` (whole), `crew/quarters.py` (158-332), `api/action_readings.py`
(128-197), `world/captains.py` (4160-4189), `world/boats.py` (890-929), `physics/hull.py`
(549-558), `physics/strain.py` (519-534, 613-628), `ship/parts.py` (528-625, the Magazine's
fields). Of the data: `data/signals/basic/book.yaml` and the head of `britain/numerary.yaml`
read; the rest of the 52 files counted by loading them, not read line by line; Britain's
telegraphic dictionary not read. Of `data/ships`: the frigate's armament head read, the others
measured by line and gun count only. `data/scenarios/first-action.yaml` and
`data/standing_orders/fighting.orders` read whole. Of the tests: only the truths cited
(8490-8535 of `test_known_truths.py`) and `tests/browser_plans/action.yaml` lines 1-40; the
test files listed in section 1 were counted, not read, so a claim of "untested" rests on grep of
names and log kinds and may miss a test that reaches the code by another word.
