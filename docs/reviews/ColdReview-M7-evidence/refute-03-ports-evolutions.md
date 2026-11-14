# Second reader: refuting code-03 (world orders, people, ports) and code-07 (evolutions, crew)

Read under READERS.md and REFUTERS.md. Nothing under docs/dev, docs/design, docs/playtests or
docs/gates opened; no test suite run; the only file written in the tree is this one. Scripts
were kept in my scratch directory and each ran in seconds; they build worlds with the helpers of
`tests/test_ports.py` (`at_anchor_in`, `run_until`) and `freesail.api.session.make_world`.

The checkout's HEAD is 89a6f72, one commit past the 504a250 named in READERS.md. I did not
switch. `git diff --stat 504a250 HEAD -- freesail data tests tools client` is empty, so the code
read is the code under review.

| Finding | First reader's weight | Verdict | My weight |
|---|---|---|---|
| 03-R1 Trade with the boat lost takes the money, delivers nothing | high | STANDS (worse than stated) | high |
| 03-2 World-order channel a second language | high | STANDS IN PART | medium |
| 03-3 Trading written three times | medium | STANDS | medium |
| 03-R2 Recruits' ids collide | medium | STANDS | medium |
| 03-R3 "Do not wear her" read as leave to wear | medium | STANDS (wider than stated) | medium to high |
| 03-R4 Unparseable `world:` line raises after being journaled | medium | STANDS IN PART | medium |
| 03-7 Much port data read by nothing | medium | STANDS | low |
| 03-8a A port offers no repair | medium | STANDS IN PART | medium |
| 03-8b The crew pool never refills | medium | STANDS | medium |
| 07-1 The catalogue is not the seamanship | high | STANDS | high (against the claim) |
| 07-2 Only the simplest evolution by data alone | high | STANDS IN PART | medium |
| 07-3 Unknown word in a check loads as a string, always true | medium | STANDS (latent; no live case) | medium |
| 07-4 No per-man morale; `skill_aloft` never read | medium | STANDS | medium |
| 07-5 Aloft fatigue charged only by tests | low to medium | STANDS | low to medium |
| 07-6 Thirst kills only when provisions are gone too | medium | REFUTED (in substance) | low |
| 07-8 `furl_gaff`, `furl_jibheaded` unreachable | low | STANDS | low |

## code-03

### R1. A purchase with the boat lost takes the money and delivers nothing (high; sure)

**Tried.** Read `dealings.py:2276-2373` (`trade`) and `2873-2915` (`_send_boat`). `trade`
checks `self.boat.away` (2299) but not `boat.lost`; it pays (2327) and moves the market (2328)
before `_send_boat` raises on `self.boat.lost` (2887-2889). The `try/except OrderError` in
`_send_boat` (2908-2915) restores only the boat state, not the purse. I looked for a rollback
above: `orders/port.py:340-372` calls `ports.trade` bare. There is no snapshot or undo in
`orders/__init__.py`, `orders/port.py` or `core/world.py` (grep for rollback, snapshot, restore,
undo, deepcopy). Can a player lose the boat? Yes, by three roads: swamped
(`boats.py:559`), the player's own `cut the boat adrift` (`boats.py:969`), and the director
(`orders.py:3672-3685`).

Then I played it through the player's own words, with no stub. Schooner at anchor in Carrick
Road, £500. `send the boat ashore`, prices brought off. Then `cut the boat adrift`, which gave
"The long-boat cut adrift by order. A new one is the yard's." Then `buy three tons of coal`:

```
order.rejected | Order not carried out ('buy three tons of coal'): The long-boat is lost: ...
purse after 494.0 hold {} net {'coal': -3.0}
purse 3h later 494.0 hold {}
order.rejected | Order not carried out ('buy three tons of coal and two tons of tin'): ...
purse 248.0
```

**Verdict: STANDS, and it is worse than the reader put it.** The player is told in so many words
"Order not carried out" while the money is gone and the market has moved. Each retry takes
more. Nothing comes three hours later. I did not run the sale path. By the code (2343-2346) it
breaks the goods out of the hold and credits the purse before the same raise, so on a sale the
goods vanish and the player is paid. **Weight: high.**

### 2. The world-order channel is a second language sharing almost nothing (high; sure)

**Tried.** Counted: 58 `re.compile(` in `world/orders.py`, 0 in `orders/grammar.py`. But
`freesail/orders/*.py`, the captain's side, has 68 compiled patterns of its own (`signals.py` 28,
`stations.py` 13, `ordnance.py` 7, and others) and 97 `re.*(` calls. So "the captain's grammar
has no regular expressions" is true of `grammar.py` alone; the captain's order package is
regex-heavy too. The world channel does hand words to the captain's grammar: `ship "X": hand
<order in her grammar>` (`orders.py:75-76, 626`). Its other shares are the number reader, the
part and gun names, `free.spoken` and `OrderError`, as the reader says. The director does reach
into the private regexes (`agents/director.py:339-410`: `_aboard_match`, `_PORT`, `_SYSTEM`,
`_WAYPOINT`, `_SHIP_NEW`).

The strongest defence is that the world channel says different things. It makes ships, weather,
persons and courts; it does not work the ship's parts. Its users are the director and the owner,
never the player at the captain's prompt. A vocabulary of verbs over parts would fit it badly.
That defence holds against "it should be the captain's grammar". It does not hold against the
cost the reader names: four lists of channels, a forms table in the director kept apart from
the parser, and private regexes used from another package.

**Verdict: STANDS IN PART.** The duplication and the coupling stand. The contrast "regexes on
one side, vocabulary on the other" is overstated, and a player never meets this channel except
through `world:`. **Weight: medium** (a maintainer's cost, not a player's).

### 3. Trading is written three times (medium; sure)

**Tried.** `trade`, `trade_together` and `trade_list` repeat the in-port, stance, price-list and
boat checks, and two of the three share R1's ordering. The defence is that `trade_list` in person
goes by the lighter, not the boat, and so is a different road. That holds for that one branch
only. **Verdict: STANDS.** R1 is the proof of its cost. **Weight: medium.**

### R2. Recruits' ids collide (medium; sure)

**Tried.** `_muster_recruits` (`dealings.py:2833-2844`) numbers new men from
`len(crew.sailors)`. Burial removes the dead from `crew.sailors` (`crew/health.py:972-975`).
Prize crews are taken out too (`world/prizes.py:456-460`). Both happen in play. Run: frigate at
Carrick Road, 264 sailors `s001`..`s264`. I removed one sailor as burial does (remove, then
`reindex`) and entered two ordinary seamen:

```
dups ['s264'] sailors 265 by_id 264
```

**Verdict: STANDS.** One man is shadowed in `crew.by_id`, and so in the quarter bill and every
lookup by id. **Weight: medium.**

### R3. A told prohibition is read as permission (medium; sure)

**Tried.** `reports.told_covers` (`world/reports.py:802-835`) takes a clause as covering an order
when `mine in c`. `told` holds whatever the captain says to a station with `tell the <station>
...` (`agents/harness.py:4732`, `agents/seat.py:323-326`), and answers too (`harness.py:5365`).
Nothing filters a negative. The caller is `agents/tools.py:1014`, which returns `TOLD` before
anything else, so before `_kept_back` (`tools.py:1223-1238`), the guard that keeps the
`irrevocable` verbs (`cut away`, `vocabulary.yaml:2459-2460`) from a station's general
authority. My run:

```
told_covers(None, ['do not cut away the mainmast whatever happens'], 'cut away the mainmast') -> True
told_covers(None, ['on no account slip the cable'], 'slip the cable') -> True
told_covers(None, ['do not wear her'], 'wear her') -> True
told_covers(None, ['tack when the wind heads you'], 'tack') -> True
```

**Verdict: STANDS, and wider than stated.** "Do not cut away the mainmast" lets a model officer
cut it away, past the one guard meant to stop exactly that. A condition is dropped as well: an
order to tack *when* the wind heads her covers a tack now. **Weight: medium to high.** It is a
model officer's act, but it cannot be undone.

### R4. An unparseable `world:` line raises out after being journaled (medium; sure/likely)

**Tried.** `World.world_order` appends to `inputs` (`core/world.py:1694-1701`), then
`_apply_world_order` calls `parse` outside the `try` (1707). `WorldOrderError` is a `ValueError`
(`orders.py:180`). On the console, `_handle_line` calls it bare (`ui/console.py:731-737`).
`handle_line` has only `try/finally` (595-600), and the interactive loop (946-956) and the piped
loop (825-836) catch nothing but `EOFError/KeyboardInterrupt` and `queue.Empty`. My run, through
the console object itself:

```
con.handle_line("world: wether: a gale from the west")
RAISED WorldOrderError 'wether: a gale from the west' is no world order: ...
inputs grew by 1 {'tick': 0, 'world_order': 'wether: a gale from the west', 'source': 'the owner'}
```

Replay gives the entry again by `world.world_order` (`core/replay.py:307-312`) with no `except`
around `_give` (246), so a save that holds it fails on replay. **What falls:** the director is
not exposed. It parses first and catches (`agents/director.py:1929-1930`), and so do the
scenario's orders at load. Whether a poisoned save is written depends on a save coming after the
bad line; on the console the process ends first, so the poisoned save is most likely on the
browser's path (`ui/server.py:604`), whose handler I did not trace.

**Verdict: STANDS IN PART.** The owner's console dies on one mistyped `world:` line, and any play
since the last save is lost. The director part falls. **Weight: medium.**

### 7. Much of the port files' data is read by nothing (medium; sure)

**Tried.** Grep over `freesail tools client` for `datum`, `leave_on`, `establishment`,
`.currency`, `depth_words`, `deep_draught`, `mooring_for`: no reader in play. `port.tide` is
read only for `enter_on` (`dealings.py:2043`). The pilot's tide words are computed by
`_tide_words`, and the file's `words.tide` is never read (`dealings.py:2060-2104`). The
`_depth_words` hits are a different function in `evolutions/scripts.py`.

**Verdict: STANDS.** The cost to a player is nil and to a maintainer small: provenance carried
in data. **Weight: low.**

### 8a. A port offers no repair of any kind (medium; sure)

**Tried hard.** The yard's items (`dealings.py:2735-2777`): a new boat for one lost; water;
provisions; cordage into the store; a suit of sails into the sail room; and spars to the booms.
Counted over the 116 port files that load without a chart: every one stocks topmast, cordage,
water and provisions; 65 a yard; 49 a topgallant mast; 42 a suit of sails. 12 are King's yards,
104 chandlers. These feed real repair that the crew do:

- `shift spar` (`scripts.py:4895-4935`) refuses "No spare ... aboard; the dockyard must
  supply one", and sets the new spar's `condition = 100`, `wrecked = False`.
- bending a spare sail makes it whole (`ship/parts.py:406-407`: condition set,
  `holed_m2 = 0`).
- reeving a line afresh from the store's cordage sets `condition = 100`
  (`scripts.py:6150-6162`; `repair_scripts.py:833, 866` "wait for the dockyard").

So the port is where spars, sails and rigging are made whole again, by its materials and the
ship's hands. The first reader's own section 2 says as much ("the ship's own people then shift
it"), while his ten-findings item calls it "no repair".

What stands: nothing in a port mends the hull. Shot holes are plugged at sea
(`repair_scripts.py:186-321`), and a plugged hole leaks nothing for ever after
(`world/water.py:266-268`), so the hull has no need of a port. That is a simplification, not a
lack a player would feel. There is no careening, no survey of the hull, and no yard that does the
work itself. Worse, and missed: no port in the 116 stocks a lower mast or a bowsprit (see Found on
the way).

**Verdict: STANDS IN PART.** "No repair of any kind" falls. "No yard work and no hull repair"
stands. **Weight: medium.**

### 8b. The crew pool never refills (medium; sure)

**Tried.** `crew_pool` is a dated key (`ports.py:777`), and `Port.on_events` is reached in play
(`ports.py:1396`), so a dated row could reset a pool. None of the 121 files gives `crew_pool` as
dated rows (script count: 121 with a pool, 0 dated). There is no other writer (grep `crew_pool`,
`pool` in `world/orders.py` and `scenarios.py`). Pools are small: median 9 hands a port, at most
77; Falmouth has 4 able, 8 ordinary and 12 landsmen for the whole game.

**Verdict: STANDS.** The machinery for a refill by date exists and no data uses it.
**Weight: medium** (a long game, or a crew lost in action, finds the ports empty).

## code-07

### 1. The catalogue is not the seamanship (high; sure)

**Tried.** Recounted: 108 files load; 64 name a script (49 classes), 44 are step lists with 112
steps in all; `scripts.py` is 9,095 lines. The defence is that a tack is closed-loop control over
the physics (the hang in stays, the miss, the recovery) which no linear step list could express.
That defends the design. It does not defend the claim that the catalogue is the seamanship.

**Verdict: STANDS.** **Weight: high** as a correction of what the project says of itself; it
costs a player nothing.

### 2. A player can add only the simplest evolution by data alone (high; sure)

**Tried.** The step schema (`registry.py:95-140`) has `if:`, `instead_of:`, `via:`, `requires:`,
`sets:` and `ramp:` over expressions. The expression environment (`runner.py:683-710`) offers
`close_hauled()`, `lee_side()`, `wanted_sheet(sail)`, `dyn.*` and the rig queries. Data files do
read the wind today: `set_gaff.yaml:36` sets the sheet from `dyn.apparent_wind_angle`;
`dip_lug.yaml:33` sets the lug's side from `lee_side()`; `set_lateen.yaml:41` uses
`wanted_sheet(sail)`. So the reader's "anything that reads the wind ... needs Python" is wrong:
a data evolution can be conditional, wind-dependent and alternative-stepped. The reader's own
experiment shows the words go in `vocabulary.yaml`, which is data.

What stands: no chance, no timing decided by the state, no outcome but an attribute assigned, no
new function and no new sail class without Python, and the Python id lists
(`HANDING_EVOLUTIONS`, `QUARTERS_OWN`, `CALLS_HANDS_WHEN_SHORT`) would not know a new id.

**Verdict: STANDS IN PART.** "Only the simplest" is overstated; "nothing with judgement or chance"
stands. **Weight: medium.**

### 3. An unknown word in a check loads as a string and is always true (medium; sure)

**Tried.** `expr.Env.lookup` returns the bare name (`expr.py:305`). Run:
`sail.state != fruled` evaluates `True` for a furled sail, as does `sail.state == furled`. I
looked for a test or load-time guard (grep "bare word", "unknown word", "stands for itself" over
tests, tools and freesail): none that checks the catalogue. Then I looked for a live typo: I
walked every expression in the 108 loaded files and listed every bare name. Each one left over is
a state word that exists (`furled`, `loosed`, `belayed`, ...) or a role or subject name
(`topmast`, `boom`, `outhaul`, `halyard_spar`). No misspelling is there today.

**Verdict: STANDS** as a latent fault and a false claim in the registry's docstring
(`registry.py:25-27`). It is no live bug. **Weight: medium** for anyone who edits the catalogue,
nil for play today.

### 4. No per-man morale; `skill_aloft` never read (medium; sure)

**Tried.** Grep every spelling (`skill_aloft`, `aloft_skill`, `"skill_`, `skill_{`) over
freesail, client, tools and data. It is written by `muster.py:214` and `dealings.py:2848`,
declared at `model.py:137`, and read only in tests (`test_crew_model.py`, `test_hands.py`).
`getattr(..., "skill_deck")` exists (`combat/shot.py:216`, `combat/boarding.py:273`); nothing
reads aloft. Morale is `combat/morale.py:68` `Morale`, company-level (`morale_of(ship)`, 151); no
field on `Sailor`. **Verdict: STANDS.** **Weight: medium** against the proposal's individuals.

### 5. Aloft fatigue charged only by tests (low to medium; sure)

**Tried.** `Routine.tick` charges `aloft` only for `s.id in _aloft_ids or s.at in
_aloft_instances` (`crew/routine.py:210-215`). The only writers outside the routine are
`set_aloft`/`set_instance_aloft`, called by tests alone, and `world/prizes.py:402`, which clears
them. The runner knows `step.aloft` (`runner.py:881, 1093`) but tells the routine nothing.
**Verdict: STANDS.** **Weight: low to medium.**

### 6. Thirst kills only when the provisions are gone too (medium; likely)

**Tried.** `health.py:868-871`: `water_out` is `water_tons <= 0 and provisions_days <= 0`. The
constants' comment says "The company with the water expended (the beer too)" (`health.py:104`).
The ration (`data/crew/ration.yaml:36-42`) gives a gallon of beer every day, inside the
provisions the purser counts in days (`ration.yaml:44, 67-69` measure the beer and the water
together). So a ship with water out and provisions left still has her drink, as the Navy's did.
The AND is the beer, not a slip. What remains is a docstring at 31-34 that says "the water
expended" without the beer, and a model that keeps the bread and the beer in one number.

**Verdict: REFUTED in substance.** **Weight: low** (a comment to mend).

### 8. `furl_gaff` and `furl_jibheaded` cannot be reached in play (low; sure)

**Tried.** Grep for the ids and for built names (`f"furl_`, `furl_{`, `"furl_" +`) over freesail,
tools, client and data. The only mentions are `HANDING_EVOLUTIONS` (`scripts.py:579-580`) and
comments in other evolution files. `vocabulary.yaml:1917-1920` maps `furl` for square, lateen and
settee only, and refuses the rest (2019). `furl all` is `FurlAllScript` (`scripts.py:5047`),
which does its own work and starts neither. The agents and director go through order text.
**Verdict: STANDS.** **Weight: low.**

## Found on the way

1. **R1's refusal tells the player the opposite of what happened.** Following
   `cut the boat adrift`, the words "Order not carried out ('buy three tons of coal')" are shown
   while £6 is taken and the market's `net_sold` moves. A second try for two goods took a further
   £246. A player who reads the refusal and tries again is robbed each time. Run above. High;
   sure.

2. **No port supplies a lower mast or a bowsprit.** Across the 116 port files that load, the yard
   items are only topmast, topgallant mast, yard, cordage, suit of sails, water and provisions.
   `shift spar` needs a spare of the spar's class on the booms (`scripts.py:4901-4904`), and
   `demand a mainmast from the yard` is refused at Plymouth (`tests/test_ports.py:887-888`). A
   ship that has cut away or lost a lower mast or her bowsprit is jury-rigged
   (`repair_scripts.py:616`, `JURY_CONDITION`) for the rest of the game, in any port. Medium;
   sure of the data, likely of the consequence (I did not check whether any ship file carries a
   spare lower mast).

3. **`told_covers` beats the irrevocable guard.** As in R3: `TOLD` is returned at
   `agents/tools.py:1014`, before `_kept_back` (1223-1238) can refuse `cut away`. So any told
   sentence containing "cut away the mainmast", "do not" included, licenses it. Medium to high;
   sure of the order of the checks and of `told_covers`' answer. I did not drive a model officer
   to do it.

## Not tried or not read

- The server's handler around `ui/server.py:604`: not traced, so whether a bad `world:` line kills
  the browser session or only the request is not known.
- The sale branch of R1 was read, not run.
- code-03 items 9 and 10 (layering; several finders) and code-07 items 7, 9 and 10 (close-hauled
  four times; layering; duplicated helpers) were not tried. They are judgements of shape that the
  owner would not act on before the faults above.
