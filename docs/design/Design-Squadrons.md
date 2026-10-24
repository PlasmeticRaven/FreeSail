# Design note: the squadron as a set, and the naval system (package 72)

Written before anything of package 72 was built (the brief's rule: "the squadron's shape is
designed first and written down before it is built, because 79 builds the regimes out from
it and the gate's six on six is measured on it"). Spec M7 Part 7-vi (§21 to §23), rule 4
(rules first, models welcome), rule 5 (the far ships fight as the near do, coarsely) and
rule 6 (realism, not pacing) bind; the owner's note 8 (a genuine set, split and joined
freely), his frame (the command system and the signals to make more ships sane; six on six
the ideal and never rushed) and his requirement of 2026-10-17 (the business follows the
player's ship across regions) are the reasons for the shape. The lead's readings in the
brief are taken where the code agreed with them and departed from in the places said
below, each with its reason.

## What the engine has, and what a squadron asks of it

Today every other sail is a `Vessel` of her own (`world/ships.py`): a far body moved a
minute at a time along a plan of legs, with a brain (`brains.FarCaptain`) when her scenario
entry gives her an intent, promoted to a World of her own within four miles of the player
under a cap of three (`crews.py`). 71 gave her a signal locker and the least relation
`under_orders_of`: a captain who reads a signal from the ship he is under the orders of
performs its `does`, a brainless vessel reads by the least captain, and a merchantman keeps
company by the `company` leg of the pilot's boat (she goes with the player's ship when
within two cables and closes her straight when beyond). The convoy of four tacks in
succession three minutes apart. Five things in that shape do not fit a squadron:

1. **There is no set.** `under_orders_of` is a field on each ship pointing at one other;
   nothing knows that six ships are one thing, who leads them, in what order they sail,
   what they are for, or that two of them were detached an hour ago.
2. **Nothing keeps a formation.** The `company` leg keeps a ship within a circle of the
   player's own ship and nothing else; it follows a stopped commodore's drift (71's
   finding), works only toward `the ship`, and gives every merchantman the same circle, so
   four of them pile on one point.
3. **Every ship judges alone.** A merchantman in a convoy has a merchant's doctrine, and
   the merchant hauls off from any hostile stranger within two leagues: a convoy of six
   with a privateer in sight would scatter the minute she was made out, which the convoy
   instructions forbade and the period's convoys mostly did not do while the escort stood
   by them.
4. **The succession is a clock.** 71's three minutes (`SUCCESSION_GAP_S`) stand in for the
   leader's wake, which is where the period's ships put about.
5. **The business draws for one region** and puts a ship out of the world at its edge;
   a convoy sailing up Channel with the player would be dissolved at 3° W.

## The design in one paragraph

**A squadron is a set** (`squadrons.Squadron`): a commander, the members in their order of
sailing, one goal, a kind (a squadron or a convoy, which decides whose book her signals
are), a formation with its interval, the divisions she is split into, her stragglers, her
rendezvous, and her book; nothing more is fixed, and ships join and leave her by the
scenario file, by the director's forms, by her commander's signals and by the world (a
straggler lost, a ship separated in a gale, a prize taken). **The set writes 71's relation**:
a member's `under_orders_of` is her commander's id (her division's leader's while the
division is detached), so that every reader 71 built (the signal obeyed, the succession's
rank, the challenge withheld from a ship under his orders, the convoy book chosen) works
unchanged, and a ship under orders outside any set keeps the field as the scenario or the
director set it. **One brain moves the set at far detail**: the commander's own brain sails
his intent as now, and each member's far body is on a `station` leg, steered each minute
for her formation offset in the commander's frame (along his course and across it, the
windward side read from the wind at him), going with him when within tolerance and closing
at her own pace when beyond, so that a convoy, a blockading squadron and a line of battle
are one body and five pieces of arithmetic until the player is near; the set's pace is the
slowest member's. **Members in a set are in a new state of the machine, `in company`**,
whose doctrine is written in each role's file and not held in code: the merchantman in
company keeps her station under a hostile stranger where the merchant alone hauls off,
heaves to in a gale and strikes when caught as before; the escort's and the commodore's
rows are theirs. A member leaves `in company` for a detour of her own (the gale, the enemy
within her engaging distance, a chase the commander's signal frees her for) and returns to
her station when the detour ends; beyond the set's `separated_nm` she sails for the
rendezvous. **Under the cap the members promote one by one, each in her station**: the
promoted member's `Captain` enters `in company` with the book of that state, which gives
`keep your station` every two minutes, a held order of the navigation that reads the flag's
bearing and distance from the lookout and shapes her course for her station under the
helm's law, shortening and making sail to hold it; the player may give the same order in
his own words (`keep station two cables astern of the Harpy`). **The succession is the
wake**: each ship puts about when she has run the distance she was astern of the ship ahead
when that ship went about, both bodies by their own run; 71's three minutes remain the
fallback for a ship under orders outside any set. **The commander's standing orders are a
book** (`data/squadrons/<kind>.yaml`: the order of sailing and its intervals, the night and
fog orders, the rendezvous, and a few rules in data that make his signals: the convoy
closed round the commodore when an enemy is in sight, the ships astern told to make more
sail when one straggles, the escort covering a straggler threatened), run once a minute by
the set when a rules captain commands her and by nothing when a model or the player holds
the commander's station (then the signals are his). **The regimes are data**
(`data/regimes.yaml`): in port, in ordinary, on station, on passage, in convoy, escorting,
on blockade, in chase, each a few rules and knobs (the blockade's inshore and offshore
stations and the gale that blows it off to its lee rendezvous; the convoy's pace; the delay
of a commission), and each nation's knobs in `data/nations.yaml` beside 71's habits (who
keeps the sea, who keeps port and slips out when the blockade is blown off, who convoys,
whose privateers chase what pays). **The business draws convoys and squadrons** under the
seed as it draws traders, by the regimes and the nations' knobs, **and follows the player's
ship across regions**: the region in play is wherever the centre is, a new region is
peopled when he enters it, and a ship under way is put out of the world only when she is
beyond the region, bound away, and far from him, a set kept whole while any member is near.
**The weather's seasonal bound** is built as a soft clamp on the summed anomaly under a
scenario switch the recorded passages keep off; **the planner across the land** is left to
78 with the reason (the convoys of this package sail the ports' tracks as the traders do).

## The pieces

### The set: `freesail/world/squadrons.py`

```python
@dataclass
class Squadron:
    id: str                 # "convoy-1", "channel"
    name: str               # "the Falmouth convoy", "the Channel squadron"
    kind: str               # "convoy" | "squadron"
    nation: str
    commander: str          # a vessel id, or "the ship" (the player's)
    members: list[str]      # every member's id in the order of sailing, the commander among them
    goal: str               # the set's goal in words (the commander's intent)
    formation: str          # "line ahead" | "line abreast" | "order of sailing" | "close order"
    interval_m: float       # between ships in a line (two cables: the period's close order)
    columns: int            # the convoy's columns under "order of sailing"
    divisions: dict[str, Division]   # name -> (leader, members, detached_since)
    stragglers: dict[str, int]       # id -> the tick she fell out of station
    rendezvous: str         # a place in words (the destination when none is given)
    book: str               # the squadron's book (data/squadrons/<book>.yaml), by the kind
    regime: str             # "in convoy", "on blockade", "on station", "on passage", ...
    made: dict[str, int]    # the book's rules fired, by key, for the re-arm
```

`world.squadrons` is `Squadrons` (the registry: `add`, `of(vessel_id)`, `find(words)`,
`tick`, `to_dict`), a class default of None so that a checkpoint from before loads with
none. **Membership is the set's one truth.** `Vessel.squadron` (the id, "" for none) is
the back-reference, written only by the set; `Squadron.join(id)`, `leave(id)`,
`detach(division, leader, ids)`, `recall(division)` and `set_commander(id)` each end by
`_rewrite_orders()`, which writes every member's `under_orders_of` (the commander's id;
the division leader's for a detached division's members; the player's shadow id for the
player as commodore) and clears a departing member's. A ship alone is a squadron of one
for the brain (`Squadrons.of` returns None and the brain sails as it does today) and no
object for the player: no set is made for her.

**Joining and leaving.** By the scenario file (`squadrons:` beside `ships:`, each
`{id, name, kind, commander, members, formation, interval_cables, columns, rendezvous,
book}`; a member's `squadron:` key in her `ships:` entry is the short form); by the
director (`squadron "Channel": join the Harpy`, `... detach the Medusa`, `... detach the
Medusa and the Harpy as the inshore division under the Medusa`, `... recall the inshore
division`, `... form the line ahead`, `... goal <words>`, `squadron: "<name>" of <nation>
under <ship> with <ship>, <ship>, <goal>` a set made of ships on the sea; `convoy: <n>
merchantmen under <ship> from <port> for <port>` a convoy the business draws now); by the
commander's own signals (the ships pointed out to chase detaches them as a division under
the first named, the recall merges it, part company releases); and by the world (a
straggler beyond `lost_nm` leaves the set with the goal `bound for <the destination>`
under her own brain, said in her story; a member separated beyond `separated_nm` keeps her
membership and sails for the rendezvous until the commander is in sight again; a prize
joins her captor's set, 74's hook: `Squadron.join(prize_id, as_prize=True)`).

### The formations and the station leg

The offsets are computed in the commander's frame each minute (`Squadron.stations(world)
-> dict[id, Position]`): the guide point is the commander's position less his own offset,
the frame's along-axis his course over the ground (his heading when he has way, his last
course when he has none, so that a stopped commodore's drift does not swing the convoy:
71's finding), the across-axis positive to leeward by the wind at him.

- **line ahead**: member i (the leader first, the members' order) at along = -i × interval,
  across = 0; the commander's slot is his place in the order (a frigate's commodore leads;
  a convoy's commodore in the order of sailing is to windward, below).
- **line abreast**: along = 0, across alternating ±i × interval from the guide.
- **order of sailing** (the convoy's; the *Signals and Instructions for Ships under Convoy*
  form the merchantmen in columns with the escort to windward, from memory): the
  merchantmen fill `columns` columns, column j = i mod columns, row = i div columns, at
  along = -row × interval and across = (j - (columns-1)/2) × interval to leeward of the
  escort; the escort(s) at across = -interval (to windward of the body) abeam the middle
  row; the figures are judgements after the instructions' words ("in close order, two
  cables apart").
- **close order** (the convoy closed round the commodore, No. 124; keep closer order, No.
  46): the body's interval halved and the escort's offset nought, the convoy about him.

**The station leg** `("station", squadron_id)` on a member's far body: `Vessel.tick`
resolves her station point P from the set; within `STATION_TOLERANCE_M` (half a cable) she
goes with the commander's velocity over the ground on his course (as `_keep_company` does);
beyond it she steers for P under her polar's course rule (`_course_for`: a station dead to
windward is closed on a board) at her own pace, or the set's pace and `COMPANY_CLOSING_KN`
more, whichever is the greater, and **never faster than her polar and her sailing factor
allow**, so that a dull sailer in a column falls astern unless the set's pace is cut to
hers. **The set's pace is the slowest member's** (`Squadron.pace_cap_kn`, the least over
the members of her polar's speed on the course at the wind, times her sailing factor,
times `convoy_pace_factor` (0.9: the commodore keeps his convoy under the slowest ship's
best, so that she can keep up; judgement), applied to the commander's far body as a cap
in `Vessel.pace_kn` while he commands a set), so a convoy sails at the slowest ship's
pace as §22 says. A member hove to for weather, chasing, evading or in port has no station
leg (her own detour) and takes it again when the detour ends.

**Stragglers.** A member more than `straggler_nm` (the book's; a mile for a convoy) from
her station for `straggler_minutes` (ten) is a straggler of the set (`stragglers[id]`,
the event `squadron.straggler` in the commander's log and the member's story); one more
than `lost_nm` (six miles: beyond the flags' range with the glass) from it is lost to the
set and leaves it. Why a ship straggles: her pace (a dull sailer when the set's pace is
not cut, the pace cap off under a general chase), a detour of her own (hove to in a
squall while the rest ran on), the scenario's own word (the convoy of six starts with one
merchantman two miles astern, "who lost her station in the night", the period's commonest
straggler).

### The state `in company`

A new state of the machine, `STATES` gaining `"in company"` after `keeping station`: a
member of a set keeping her station. For the far body `resolve_state("in company")` lays
the station leg; it is a plan state (the detours save and restore it). **Each role's file
writes the rows out of it and into it**, so the hold on a member's stranger rows is the
doctrine's and not the code's:

- the merchant in company: aground → in distress; gale → hove to for weather unless no sea
  room; hove to for weather, on gale over → in company (when in a set); enemy in range →
  engaging (she fights when caught, within three cables, as alone); **no `hostile
  stranger` row** (the convoy instructions: the ships to keep their stations and not to
  separate on a stranger's appearance; from memory);
- the commodore in company (a second escort, a subordinate of a squadron): the King's
  ship's rows from keeping station with `stranger` left out (the commander's signal frees
  her: `does: {state: chasing}` enters chasing from any state as 71 built it) and `enemy
  in range → engaging`;
- the cruiser, the King's ship and the privateer in company likewise, the packet and the
  fisherman given the rows for the loader's sake (no set of theirs is drawn).

The first state of a member of a set is `in company`; a member's `_plan()` lays no legs
(the set's goal is the commander's); a member whose brain enters a plan state (on passage,
beating, keeping station) while she is a member enters `in company` instead
(`FarCaptain._enter` and `Captain._enter` map it: one place, `squadrons.plan_state_of`).
The commander himself is never `in company`: he sails his intent (the convoy's commodore
`convoy the trade from A to B`, the blockade's `blockade Brest`, a squadron's `keep the
station off Ushant within 15 miles`).

### The succession by the wake

71's `_succession` performs an `in_succession` hoist when the ship before her in the order
has performed it and `SUCCESSION_GAP_S` has passed. It becomes: when the ship before her
has performed it, note the distance she was astern of that ship at that minute (the far
body: the truth's distance; the near body: the lookout's `estimate_m` of that sail, which
is what the officer of the watch judged by), and put about when her own run since then
(`Vessel.distance_run_m`; the near body's log by the reckoning's distance run) reaches it,
which is the wake. A ship under orders outside any set (the least relation alone) keeps the
three minutes, since she has no order of sailing to measure against. The leader's going
about is the mark: `Locker.obeyed[key]` keeps the tick as now, and the set keeps the point.

### Station keeping on the near body: `keep station` (`orders/navigation.py`)

A held order of the navigation, in the family of `keep her full and by`: `keep station`
(your station in your set, refused in words when the ship is in none), `keep your station`,
`keep station two cables astern of the Harpy` / `... on the larboard beam of the flagship` /
`... a cable to windward of the Harpy`. It sets `ship.extra["station"]` (the ship named or
the set, the bearing word, the cables) and is worked by `station_keeping(world)` once a
minute from the standing runtime's minute (a hook beside the books' `every`), which reads
the flag's bearing and estimated distance **from the lookout's sails in sight** (the
`strangers` reading's `id`, `bearing_deg`, `estimate_m`: the captain's account, not the
truth), the flag's course from her made-out course words (her heading when she is within
the rig's range) or his own heading, computes the station point relative to her, and
gives, under the rules actor and routinely (one line a glass unless something changes):

- a course for the station point under the helm's law (`_chase_course`'s clamp: never
  within the close-hauled angle; a station to windward is worked up to by boards), or the
  flag's course when within the tolerance;
- the sail to hold it: ahead of station and closing, `shorten sail` (a reef, or the
  topgallants in); astern and opening, `make sail`; in station, nothing (the period's
  station keeping was done by the topgallants and the topsails' reefs; Falconer, STATION;
  judgement on the steps);
- `sail.out_of_station` when she falls beyond `straggler_nm` and `sail.in_station` when
  she regains it, the events `out of station` and `in station` for the books.

The `in company` book of every role: `'standing order "the station": every 2 minutes, if
the manoeuvre in hand is not hove to then keep your station'`, with the trims, the offing
and the land-ahead lines of keeping station. **Station keeping lives in the books** as the
brief asked: the kind is a held order the book gives and the player may give, judged by
the lookout's readings alone (`tests/test_captains.py`'s proof that the near captain reads
no truth holds).

### The promotion in station

`crews.switch` promotes by distance and the cap as now; a member promoted folds in with
state `in company` (`FarCaptain.fold_in`), her `Captain` loads the book above and gives
`keep your station` at the entry, and her World's `squadrons` is the parent's (the
`CrewView` serves the sails; the set is read through `world.parent`). At the demotion the
near state folds back and the far body takes the station leg from where she is. A set's
commander promoted keeps his intent as now and the set's minute runs through his `Captain`
(`make the signal ...` by `give`). **The pace is the figure**: at far detail a set of six
costs six station legs a minute (arithmetic) and one brain; six on six at far detail is
measured early against the frigate alone and the dozen far ships, and again at the end,
and under the cap of three and with the cap raised to twelve (the owner's baseline) by
`tools/pace.py squadrons`, with the figures in the tuning notes and truths 7-161 and 7-162
asserting the conftest's floors (`BUILD_MACHINE_FLOOR` at far detail, `CREWED_FLOOR_TICKS_S`
under the cap), not lowered.

### The commander's book and his minute: `data/squadrons/<kind>.yaml`

```yaml
kind: convoy
source: "the Signals and Instructions for Ships under Convoy (from memory); the Regulations 1806"
order_of_sailing: {formation: order of sailing, columns: 2, interval_cables: 2, escort: windward}
pace_factor: 0.9                   # the convoy under the slowest ship's best (judgement)
straggler_nm: 1.0
straggler_minutes: 10
lost_nm: 6.0
separated_nm: 10.0
night: {lights: stern lantern, signal: "hoist the lights"}
fog: {keep_signals: true}
rules:
  - {key: enemy, on: enemy in sight, signal: "close round the commodore", rearm: enemy lost}
  - {key: straggler, on: straggler, signal: "the ships astern to make more sail", to: straggler, rearm: in station}
  - {key: cover, on: straggler threatened, do: cover, rearm: enemy lost}
  - {key: night, on: night, signal: "hoist the lights"}
  - {key: anchor, on: at the destination, signal: "anchor"}
```

`Squadrons.tick` runs once a minute after the brains have judged and before the bodies
move (`Vessels.tick`): the stations computed, the stragglers counted, and, for a set whose
commander is a rules captain (nobody seated at his station), the book's rules read against
the set's perception (the commander's own `Perception` and the members' places: an enemy
in sight is any member's enemy by the commander's `_is_enemy`; a straggler threatened is an
enemy within `cover_nm` of a straggler) and each fired once until its re-arm, the signal
given through the commander's `give` (crewed or the player's rules captain) or made on the
far locker (`signals.make_hoist`); `do: cover` enters the escort's `chasing` with the enemy
as his stranger and `covering` in his business, which `_chase_order` reads to hold between
the straggler and the enemy rather than run the enemy down (the escort does not leave the
convoy: `commodore.yaml`'s own head). The blockade's book: `inshore` and `offshore`
stations, `blown_off: {wind_kn: 34, from_deg: [225, 315], rendezvous: Torbay}` (Cornwallis's
squadron bore up for Torbay in a westerly gale; the figures judgement on the record), the
rule `gale from the west → the set's goal becomes bound for the rendezvous; gale over → the
blockade again`. A model at the flagship is the orchestrator: he reads `the squadron` in his
sample and commands by `make the signal`; no rule of the book fires while he holds the
station (the commander's station is held, as 71's hand reads it).

### The escort's and the commodore's doctrine (`data/captains/commodore.yaml`)

Thresholds `cover_nm` (an enemy within two miles of a straggler is covered; judgement),
`convoy_close_nm` (the enemy within four miles brings the convoy round him: the signal's
rule), and the engaging rows as 70 wrote them (an enemy within `engage_nm` is engaged); the
transitions `in company` as above. The privateer gains `man_of_war_nm` (two miles and a
half: a sloop of war that can bring her to action within the hour drives her off;
judgement; `stranger_hostile_nm` keeps `overmatched` at two leagues), so that she hovers on
a convoy and runs when the escort bears down, as the record has the Channel privateers do.

**The straggler cut out, at far detail (rule 5's least, and 74's hook).** The far body has
no battery (70's measure, 74's wiring). A ship brought to within pistol shot (a cable) by
an armed enemy of a class above hers or equal, with no friendly man of war within
`cover_nm`, whose doctrine says `yields_when_caught: true` (the merchant's and the
packet's: a merchantman brought to by a privateer alongside struck without a fight more
often than not, the prize courts' Channel record; judgement, marked so), strikes by rule
(`Vessel.struck`, her colours struck, her story saying why) and joins her captor's set as a
prize; the privateer's `enemy struck` row takes her back to her cruise with the prize in
company. 74 replaces the rule with `combat/far.py`'s rounds for the ships that fight.

### The regimes: `data/regimes.yaml`, and the nations' knobs

```yaml
regimes:
  in port:      {rule: "at anchor within the port's reach; her business by the brains' wait"}
  in ordinary:  {rule: "a hull in port with no company and no intent; commissioned with a delay", commission_delay_h: [48, 120]}
  on station:   {intent: "keep the station off {place} within {nm} miles", book: squadron}
  on passage:   {intent: "bound for {place}"}
  in convoy:    {book: convoy, formation: order of sailing}
  escorting:    {intent: "convoy the trade from {a} to {b}", role: commodore}
  on blockade:  {intent: "blockade {port}", book: blockade, inshore: {...}, offshore: {...}}
  in chase:     {rule: "the state chasing, by doctrine; a division detached in chase"}
```

Each regime is a few rules and knobs the business and the director read; the regimes'
intents are the captain's intents (`blockade Brest` is a new intent kind, `blockade`, a
station off the port's approach with the blockade book). The nations' knobs in
`data/nations.yaml` beside `habits:` and `signals:`: `naval: {keeps_the_sea, keeps_port,
engages, blockades: [brest], convoys: true, convoy_escort: brig-sloop, in_ordinary: [{port,
description}], slips_out_when_blown_off: true, privateers: chase what pays, single_actions}`,
every figure a judgement from the standard histories (Mahan on the blockade; James; the
convoy acts of 1798 and 1803; from memory, said so). This package writes the shape and the
first of each regime (the convoy and its escort, the blockade and the sortie, in ordinary
and the commission, on station and on passage as they are); 79 fills them out.

### The business: convoys and squadrons drawn, and the player followed

`Business.start` and the hourly draw gain `_convoy()` (a convoy of `convoy_size` (four to
eight) merchantmen of a nation that convoys, under an escort of the nation's
`convoy_escort`, formed in the order of sailing, in port at a port of the region bound for
a port the trade's routes give, or at an edge bound in; the merchantmen the trader's draw
with one cargo each) and `_blockade()` (a nation that blockades a port of the region keeps
a squadron off it: the inshore division of a cutter or a brig-sloop and the offshore of a
frigate, under the blockade book; and the blockaded nation's ship in ordinary in that port
by `in_ordinary`, who slips out when the blockaders are blown off), each `Drawn` with its
kind for the record; the figures in `data/business.yaml` (`population: {convoys: 1,
blockades: 1}` in the Channel; judgement). **Following the player**: `Business.tick` reads
`chart.region_at(centre)` each minute; when it differs from `self.region` the region and
its bounds move, `start`'s draws are made for the new region (the ports and the grounds of
it, the cruisers of it) once per region entered, and the record says so
(`Business.regions_entered`). A drawn ship is put out of the world only when she is beyond
the current region by `GONE_BEYOND_NM`, bound away, **and** more than `CARRY_OVER_NM` (thirty
miles: beyond the horizon and a watch's sailing; judgement) from the centre, and never while
she is a member of a set any of whose members is within that distance: a convoy sailing up
Channel with the player crosses 3° W whole, with its state and its set, and the chase that
began in the west ends in the east.

### The weather's bound (R-39), as far as the squadrons want it

A blockade kept for days wants the gale that blows it off and no glass at 1041 in June.
The small part (the ramp, the high doubted) is 58a's and stands. **The summed field's
seasonal bound** is built as a soft clamp in `Weather.pressure_at` and `geostrophic_at`:
the anomaly summed over the systems is scaled, where it would take the glass under the
month's floor or over the month's ceiling (the table's `central_hpa` floor; the background
with the strongest high's anomaly and `HIGH_CEILING_MARGIN_HPA`), by the one factor that
brings it to the bound, the gradient scaled by the same so that the wind and the glass agree
(a hard clamp would give a flat field and no wind where the bound bites). It is **under a
switch** (`weather: {bound: seasonal}` in the scenario, `Scenario.weather_bound`, off when
not said), because it can move any sailing passage of days; the blockade scenario turns it
on; the recorded passages leave it off; the owner judges it in play. The climatology's
drift onto Iberia is the Iberian boxes' provisional data (38's), which no squadron of this
package sails under: read and left to 79 with the Mediterranean block, said in the notes.

### The planner across the land (61)

Left to 78 with the reason: the convoys of this package sail port to port by the same
tracks the traders do (`Planner.legs_for`, the far-detail guard refusing a crossing and the
business not drawing a refused route again), the blockade's stations are at sea, and the
Plymouth approach from the south-west is the tracks' data (the track up Channel passes the
Eddystone a mile to the westward and the leg from off the Lizard to its first mark crosses
the Dodman), which is looked at on the way and mended as data if it is small, else left
for 61's route finding with the finding written.

### The stations, the director and the readings

Readings: `the squadron` (the set's name and kind, the commander, the formation and its
interval, every member in her order with her station and whether she is in it, the
stragglers, the divisions detached; for the player's own set, or the set his ship is a
member of, and "the ship is in no squadron" otherwise: a squadron is shown to the player by
his own ship's membership and never as the world's object), `the station` (own station:
the flag by name, the bearing and distance the station wants and the lookout's estimate of
where she lies, in or out of station, by the readings), `the convoy` (the same reading for a
convoy's commodore, the merchantmen by name with the stragglers), `the order of sailing`
(the formation's words and the order). Events: `a ship out of her station`, `in station`,
`a straggler`, `the commodore makes a signal` (every `signal.read` from the ship he is
under the orders of), `a division detached`, `the division recalled`. The director's forms
after `WORLD_ORDER_FORMS` (the squadron channel above and the ship channel's `in ordinary
at <port>` and `commissioned for <intent>`), each with examples a test performs; his truth
shows every set with its commander, its members and their stations (`squadrons:`). The
harness: the commodore's sample carries `squadron` (its deltas: a member fallen out, a
straggler, a signal answered by all), a subordinate's `station`, the convoy's commodore
both; Harness.md §21e says what each station reads and may do.

### The scenarios and the truths

`data/scenarios/convoy-six.yaml` (the player's brig-sloop Harpy commodore of six merchant
brigs out of Falmouth for Plymouth in two columns, one two miles astern; a French privateer
schooner to the south-west under British colours; a north-westerly), `blockade.yaml` (the
player's frigate off Ushant commanding the offshore division, a brig-sloop and a cutter
inshore off the Black Rocks, the business's French frigate in Brest; a westerly gale
scripted for the afternoon), `squadron.yaml` (a French squadron of six in line ahead at far
detail off the Lizard, the player closing from windward under the cap). Truths 7-152
onward: the set and its stations at far detail; the convoy's hoist obeyed and the straggler
cut out or the privateer driven off; the blockade blown off and the sortie; the line kept
at far detail and the promotion member by member in station; the succession by the wake;
station keeping on the near body; the business's convoy and the region followed; the
division detached and recalled; in ordinary and the commission; the pace at far detail and
under the cap.

## What was rejected, and why

- **The set as a list of `under_orders_of` fields** (71's relation grown): rejected, because
  the order of sailing, the divisions, the stragglers and the book are the set's and not
  any member's, and a convoy with no commander on the sea (the escort taken) still exists;
  the field is kept as the set's cache so that 71's readers stand.
- **One brain moving every member's position directly** (the lead's words taken literally:
  "moved as one brain"): rejected for the physics' honesty and the promotion. A member
  teleported to her slot would never straggle, never be separated, never fall to leeward;
  the station leg lets each body sail at her own pace toward her slot and keeps the set
  one thing by the slots alone, which is cheap enough (arithmetic a minute a member) and
  honest.
- **A hold in code on a member's stranger rows**: rejected for the state `in company`,
  whose rows each role writes; the doctrine stays data the owner tunes with an editor.
- **The far fight wired for the straggler**: rejected by the brief (74's); the strike by
  rule when brought to by a superior force with no cover is the least honest thing and
  the hook 74 replaces.
- **The convoy's pace by the commander's own sail orders** (shorten sail signals): rejected
  for the far body (a far body's sail is a state and its pace a polar); the pace cap is
  the same thing said once; on the near body the station-keeping order does shorten and
  make sail.
- **A `squadron` state per division** or a tree of sets: rejected; a division is a named
  subset with a leader and a detached flag, enough for a chase and a recall; a division
  that must become a set of its own is detached whole by `Squadron.split`.
- **The weather's bound on by default**: rejected by the head rules (it moves passages of
  days); under a switch until the owner judges it.
- **The planner's graph** (61's hard half): rejected here; the convoys want the tracks and
  not the graph, and the owner's framing of 61 wants testing of the captains' present
  behaviour before it is briefed.
- **Showing the squadron to the player as an object of the world** (every set in `the
  squadron`): rejected by the brief; the player reads his own set, which he knows from his
  orders, and sees the others as ships and signals.

## What hangs from this (the later items)

Item 1 is the set and its membership; item 2 the station leg, the set's pace and the
promotion in station with the pace measured; item 3 the state `in company`, the near body's
`keep station`, the succession by the wake and the stragglers; item 4 the squadron's book,
the commander's minute, the escort's and the commodore's doctrine and the model at the
flagship; item 5 the regimes and the nations' knobs; item 6 the business's convoys and
squadrons and the region followed; item 7 the bound under its switch; item 8 the planner
left with the finding; item 9 the readings, the events, the forms and the harness; item 10
the scenarios, the truths from 7-152 and the records. 79 builds the regimes out from
`data/regimes.yaml` and the nations' knobs; 74 gives the prize to her captor's set and the
far fight to the straggler; 76 corrects the books' numbers the squadron's signals use.
