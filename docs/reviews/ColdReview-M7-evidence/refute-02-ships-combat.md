# Refuter 02: the world's ships (code-02) and combat and signals (code-04)

Second reader to `code-02-world-ships.md` and `code-04-combat-signals.md`. The checkout is at
89a6f72, one commit past the commit under review (504a250). `git diff --stat 504a250 HEAD --
freesail data client tests` is empty, so the code, data and tests are the reviewed ones. I
changed nothing but this file. I ran no suite. I ran five short python scripts from the
scratchpad, building worlds with the tests' own helpers (`tests/test_fishing.py:world_at`,
`tests/test_business.py:world_with`, `freesail.world.scenarios.make_scenario_world` +
`begin`). While the last of them was running, the machine's kernel killed a process for lack
of memory. The reviewer should know this in case it touched the timed suite.

| Finding | First weight | Verdict | My weight |
|---|---|---|---|
| 02-1 Far fisherman's haul salts from, and strips the drag of, the player's ship | high | STANDS (reproduced) | high in fishing play, medium overall |
| 02-2 Business Brest blockade blown off sets "bound for the Black Rocks" | high | STANDS (reproduced) | medium |
| 02-3 Brain state lost at the fold; ship behaves differently inside 4 miles | medium-high | STANDS IN PART | medium |
| 02-4 Eight ship forms, three flags, near ring inside crewed ring | medium | STANDS | medium |
| 02-5 Doctrine keys read by nothing; cruiser's prize block under `stations:` | medium | STANDS | medium (owner's tuning), none to the player today |
| 02-6 Duplicated machinery that has drifted | medium | STANDS IN PART | medium |
| 02-7 Tick reaches `agents` and `api` by local imports | medium | STANDS | low-medium |
| 02-8 `Hull` façade and `bind_to_hull` hazard | medium | NOT TRIED | medium (as given) |
| 02-9 Near captain overgrown, far thin | medium | STANDS (judgement) | medium |
| 02-10 Captains coarse on meeting the player; dead King's-ship rows | low-medium | STANDS IN PART | low |
| 04-1 Gun deck answers "already" with guns secured; no warning | high | STANDS (reproduced in play) | high |
| 04-2 Wheel shot away never mended | high | STANDS | medium-high |
| 04-3 Player's shot into a sleeping mark does nothing | medium-high | STANDS, and wider than stated | high |
| 04-4 Five fight models | medium | STANDS IN PART | low-medium as a judgement |
| 04-5 "Damage is just state" fails in four places | medium | STANDS | medium |
| 04-6 Boarders never leave the guns; `repel boarders` never ends | medium | STANDS | medium |
| 04-7 Strike written five ways, int and bool in one key | medium | STANDS IN PART | low |
| 04-8 Stale words to the player ("not in this game yet") | medium | STANDS | medium |
| 04-9 Signals overgrown; "engage from to windward" cannot parse | medium | STANDS IN PART | low-medium |
| 04-10 Hazardous shape (local imports, bare excepts) | medium | STANDS (not re-counted) | medium |

## code-02

### 02-1. A far fisherman's haul works on the player's ship (high, likely)

**What I did.** I read `brains.py:640-665`, `fishing.py:738-779` (`salt_aboard`, `haul_into`),
`fishing.py:902-980` (`far_work`, `trip_done_far`) and `fishing.py:1110-1128`
(`rig_gear_drag`). `far_work(self.world, self.vessel, ...)` passes the game World. `haul_into`
calls `rig_gear_drag(world, fishery)`, which reads `world.ship.extra`. It also calls
`salt_aboard(world)` and `world.hold.break_out("salt", ...)`. Nothing in the chain takes the
vessel's own stores. Then I ran it. The player was in a smack with 2.0 tons of salt and
`gear_drag` set to 1200 N (towing a trawl). A business-style smack, "Brothers", fished the
Gerrans seine ground at far detail through one shot and one haul, exactly as
`test_fishing.py:236-251` does:

```
player salt set 2.0 drag 1200.0
far catch tons 3.875 [('mackerel', False), ('pilchards', False), ('pilchards', True)]
player salt after 1.71125 drag after None
```

Her pilchards were salted from the player's hold, and his trawl's drag was taken off while
the trawl was still down. The only test of the far gear (`test_fishing.py:236`) gives the
player a frigate and asserts only on the far fishery, so it cannot see this.

**Verdict: STANDS.** It is confirmed by running it, not only by reading. Any far fisherman
anywhere on the sea does this at each haul, not only one near the player. In a business-on
fishing game (`smack-falmouth.yaml`, `lugger-roscoff.yaml`) his salt drains and his trawl
speed jumps when nobody near him is fishing. Weight: high in fishing play. Elsewhere it
touches only salt that the player's ship happens to carry.

### 02-2. The business's Brest blockade, blown off, steers for the Black Rocks (high, likely)

**What I did.** I read `squadrons.py:982-1010` (`_set_goal`), `squadrons.py:1084-1105`
(`destination_words`), `business.py:980-1062` and `blockade.yaml`. I searched for a reader
of `blown_off.rendezvous`. Only `wind_kn` and `from_deg` are read (`squadrons.py:864-873`);
`rendezvous` is not. The business passes `rendezvous=str(entry.get("rendezvous") or "")`,
which is empty for the bare `- brest` (`nations.yaml:62`). Then I ran it on the business
world of `test_business.py:world_with("on")`:

```
blockade-brest 'blockade Brest' '' blockade
goal words now: the Black Rocks
business-20 bound for the Black Rocks pierres-noires
business-21 bound for the Black Rocks pierres-noires
```

I called `_set_goal(w, "bound for {rendezvous}")`, which is exactly the rule's action. Both
leaders' brains took "bound for the Black Rocks", the inshore station off Brest. I also
looked for a defence: the "gale from the west" stimulus and the doctrine's gale handling
(heave to) may hold her hove to for most of the gale. Even so, the goal she is given, and
holds when the gale moderates below the passage line, is the wrong one. In a westerly the
Black Rocks lie on a lee shore. The far body has no danger-ahead check.

**Verdict: STANDS.** It is reproduced. It is reached only in a business-on game whose region
holds Brest at war, and only in a westerly of force 8 or more. Weight medium. It is not seen
by the player unless he is near Brest in a gale, but it is wrong whenever it fires, and the
book's `rendezvous: Torbay` looks like the switch for it.

### 02-3. "One brain, two bodies" leaks at the fold (medium-high, sure)

**What I did.** I read `brains.py:861-957` whole and every writer of `fired_on`, and checked
every caller of `Captain.set_intent`.

- **`fired_on` is not carried. This part stands.** `fold_in` and `fold_back` do not touch it.
  `action.py:264-272` writes it to whichever body is struck. There is one mitigation: a hull
  put to sleep keeps its World and its `Captain` (`crews.demote` sets `awake = False` and
  drops nothing), so near-time `fired_on` survives a sleep and a wake of the same hull. What
  is lost is far-time firing at the promotion, and near-time firing while she sleeps. The
  consequence is narrower than "an enemy whatever her colours" suggests. A firer under her
  true enemy colours is an enemy by nation anyway. The pirate's act is carried (`pirates`
  is folded both ways). What `fired_on` adds is a firer under neutral or friendly colours,
  or under no colours.
- **`role`, `doctrine` and `_business` dropped by `fold_back`. This part falls in practice.**
  Every caller that sets a crewed captain's intent sets the brain's too: `squadrons.py:1009-1010`
  and `1040-1041`, `world/orders.py:788-789`, `prizes.py:627-650`, `captive.py:427-438`. The
  reader's own example, `_set_goal`, does both. The one exception, `fishing.py:1067-1069`, ends
  in `fisherman`, which the brain already holds. What remains is that the two bodies, both set
  at once, take their roles from different tables (`role_for` against `role_of_vessel`). That
  is the two-tables part, and it stands.
- **True class at the horizon** (`ships.py:1997`, `"size": _size_of(o)` whatever the level
  made out). I confirmed this, and it is used by `overmatched` at `captains.py:2003`. It
  stands. The "player's sky" part (`brains.py:99-103`, reading `world.conditions` and
  `world.daylight`) is weak if the region's weather is one field. I did not check that.

**Verdict: STANDS IN PART.** The ship does behave differently at the 4-mile ring. The causes
are true size against the lookout's words, two role tables, and the rule of the road only
when crewed. A lost `fired_on` contributes for colours other than true enemy colours. The
dropped doctrine contributes little, because every caller sets both bodies. Weight medium.

### 02-4. Eight forms, three flags, rings inverted (medium, sure)

I read `ships.py:128-133` (`NEAR_DETAIL_NM = 2.0`, demotion at 3) and `crews.py:90-91`
(crewed at 4, demoted at 6). `crews.switch` promotes only `v.brain is not None`
(`crews.py:850`). So near detail serves only brainless ships and ships held asleep by the
cap, as the reader said. The strongest defence is that level of detail needs several forms by
its nature. That defence holds for far, crewed and asleep. It does not hold for a "near" ring
that a brained ship never sees, or for `crew` against `hull` naming. **STANDS.** Medium.

### 02-5. Doctrine-as-data partly a dead switchboard (medium, sure)

**What I did.** I grepped the twelve keys across `freesail client tools tests` (`*.py`, `*.js`,
`*.orders`). The results:

- `road_cables`, `leg_reached_nm`, `anchor_within_nm`, `spell_minutes`, `stranger_chase_nm`,
  `station_wear_hours`, `divide_prisoners`, `prisoners_most` and `fit_least` have 0 hits.
- `mans_prizes` and `burns_when` have 2 hits each, and `worth_least` has 1, all in comments
  and docstrings (`squadrons.py:1556`, `prizes.py:1238`, `test_known_truths.py:14667-14668`,
  which calls the burning "step 5's", that is, later).

I also looked for a generic road. `Captain._fills` (`captains.py:2769-2771`) copies every
threshold into the books' placeholders, so a book line with `{road_cables}` would read one.
I grepped `data/` and `freesail/` for `{<key>}` for all twelve: none.

The prize block parses as `stations:` keys. `yaml.safe_load` of `cruiser.yaml` gives
`stations` 17 keys, including `mans_prizes`, `prize_crew_share` and so on, and gives
`thresholds` no prize key. `business._cruisers` iterates these keys as nations but skips
them harmlessly (`nations.at_war("mans_prizes", ...)` is false). `prizes._th` falls back to
defaults that match today's figures.

**Verdict: STANDS.** No reader exists under any spelling I could find. There is no cost to the
player today. The cost is to the owner and to a maintainer, who edit figures that do nothing,
and the cruiser file presents them as live. Weight medium.

### 02-6. Duplicated machinery (medium, sure)

I checked only the "cannot tack" example. `FAR_SHAPE_WORDS` (`crews.py:1018-1025`) has no
"put her about". But the far body beats to windward on her own by the polar
(`ships.py:18`, `631`, `864`: "on the tack that points"). A model at a sleeping hull cannot
order a tack, but she does tack whenever her course lies to windward. That example is
overstated. The duplicate role, man-of-war and goal tables I did not re-count. **STANDS IN
PART.** Medium.

### 02-7. The simulation's tick reaches `agents` and `api` (medium, sure)

`captains.py:2620-2627` imports `agents.harness.holder_of` inside `_officer_held`, in the
captain's tick. The defence is that the captain must know whether a seat holds the deck, and
the seat lives in `agents`. That explains the need but not the direction of the import. I
found no import-boundary test or linter (`pyproject.toml`, `.github/`, and test names grepped
for "boundary", "layer", "import"). **STANDS.** Low-medium: the cost is to a maintainer, not
to play.

### 02-8. `Hull` façade hazard (medium, likely)

**NOT TRIED.** It is a judgement about an object-graph rewrite with no failure shown. Showing
it wrong would take reading `hulls.py` whole, which I did not do.

### 02-9. Near captain overgrown, far thin (medium, sure)

This is a judgement. The defence is that the near captain commands the ship the player is in
and the ships he can see, and that is where detail is seen. It holds for the player's own
ship. It does not hold for the rule of the road, which a far ship crossing at 5 miles ignores
and the same ship at 3 obeys. **STANDS.** Medium.

### 02-10. Coarse meeting; dead King's-ship rows (low-medium, sure)

`kings-ship.yaml:77` and `commodore.yaml:75` set `stranger_hostile_nm: 0`, and their sources
say "nought turns the stimulus off". So the dead `evading` rows are the result of a
documented switch, not an accident. The trap the reader describes (raise the figure and she
would enter `evading` and never leave) is real but hypothetical. **STANDS IN PART.** Low.

## code-04

### 04-1. The gun deck tells a secured battery it is "firing as they bear already" (high, sure)

**What I did.** I reproduced it at the scenario the reviewer played. I loaded
`data/scenarios/first-action.yaml` through `make_scenario_world` and `begin`, as
`ui/console.py:965-1004` does. I ran 400 seconds, so that Mr Bowen, the rules captain, was in
command and investigating. Then I gave the reviewer's three orders 30 s apart, then `fire` at
about 30 minutes, then ran about an hour in all. The replies were:

```
> beat to quarters => crew.quarters | Beat to quarters! Quarters: three gun crews manned, ...
> engage her to starboard => guns.engage | Engage a cutter to starboard: ... the guns to fire as they bear.
> fire as they bear => guns.mode | The guns are firing as they bear already.
> fire => guns.fire | Fire the starboard broadside: no gun of it is loaded and run out yet; the word stands until one bears.
guns reading: 6 12-pounder carronades; secured
battery mode as they bear target renard cast [False, False, False, False]
```

I read every one of the roughly 70 log lines from 400 s to 3,900 s, of every kind. None says
the guns are not cast loose. The lines the player was given are:

- `captain.aside`: "Mr Bowen stands aside at your order ('beat to quarters') and his book
  'investigating a stranger' struck". It says nothing of the guns.
- `guns.load`: "The guns are loading with round shot already" (by standing order 'the
  charge'). This is a second false "already", which the first reader missed.
- `action.fired_at` at 2,628 s: "A cutter opens fire on us at 5 cables". Then, by standing
  order 'return her fire', "The guns are firing as they bear already", repeated at 2,880 s.
- Then six `action.hit` lines, three shot away. No shot was fired from the cutter's side all
  hour. The bill read "nobody hurt" only by luck.

The only place the truth is shown is the reading `the guns`, which says "secured" if the
player asks for it (`api/action_readings.py:163-179`), and the browser viewer's gun drawing
(`api/viewer_guns.py:491`). I searched for any other warning: `grep -i "cast loose"` over
`freesail/ui`, `freesail/orders`, `freesail/standing`, `freesail/api`, `data/standing_orders`.
The only sentences are the gate's (`gunnery.py:258`, shown only before the beat) and the
practice order's (`gunnery.py:1247`). The scenario's head comment lists `cast loose the guns`
among the orders, but that is a YAML comment the console does not show.

The strongest defence is that casting loose is a separate, period-correct order
(`action_scripts.py:157-187`). That holds as design. It does not excuse three replies that
state the guns are firing or loading.

**Verdict: STANDS.** It is reproduced in the reviewer's own scenario. See also "Found on the
way" 1 for why the captain did not save the player here. Weight high.

### 04-2. A wheel shot away is never mended (high, sure)

I grepped `helm_lost`, "relieving" and "wheel" across `freesail data tools client`. The
writer is `hits.py:213`. The readers are `physics/hull.py:551`, `api/action_readings.py:316`
and `344`. No evolution or order clears the key. The only "relieving" hits are the watch's.
No `extra.pop` and no reset of `extra` touches it (I grepped every `extra.pop`). The comment
at `hull.py:553` names "73's repair", which was not built. The chance is
`HELM_SHOT_SHARE = 0.06` of an aft deck hit, so it is uncommon but certain over enough
actions. When it happens, the player's ship, or the enemy's, holds her rudder for the rest of
the game.

**Verdict: STANDS.** I would put it medium-high rather than high, only for its rarity. When it
happens, it ends the player's game as a sailing game. No test covers it.

### 04-3. The player's shot into a sleeping mark does nothing (medium-high, sure)

I read `hits.py:118-136` and `424-427`. I grepped `"hits"`, `weight_lb` and `_far_hit` across
`freesail client` (`*.py`, `*.js`): only the writer, plus a docstring in `crews.py:629-630`
("Nothing of it is read yet beyond the record", which is honest). `far_ship_of`
(`far_action.py:150-169`) reads seven other keys. The module head's claim at
`far_action.py:21-23` is false.

The finding is **wider than the reader stated.** The mark sleeps not only when the cap is full:

- `crews.switch` promotes only ships with a brain (`crews.py:850`). So every brainless ship is
  a far body under fire, always. That covers the merchants without an `intent:` in
  `merchant-*.yaml`, `convoy*.yaml`, `naval-cruise.yaml`, `directed-passage.yaml` and
  `prize-home.yaml`'s Deux Frères (a YAML scan of the scenarios' `ships:`).
- `tender.yaml:44` sets `crewed: {cap: 0}`, so nobody is ever promoted there.

For all of these, the player's broadsides "strike her" in his log and do nothing. The
asymmetric half (her reply by the tables damaging him, `far_action.py:359-443`) needs a brain
and a full cap, as the reader said.

**Verdict: STANDS, and it is wider.** Weight high, since a brainless mark can never be hurt
or brought to strike by gunfire.

### 04-4. Five fight models (medium, sure)

The strongest defence is that level of detail is the design (the coarse far round) and is
needed for the tick rate (`crews.py:92-99`). Under it, three forms are inevitable: near and
near, far and far, and the carry-in on waking. That defence holds for those three. It does
not hold for (b), which is not a model but nothing (04-3), or for (d), the fallback, which
maps the French "between wind and water" to the rigging (`far_action.py:429`, read). The
duplicated formulas (morale, broadside weight, cycle) are real copies.

**Verdict: STANDS IN PART.** "Five models" as a count is mostly the design, and defensible.
The defects are 04-3 and 04-5. Low-medium as a judgement.

### 04-5. "Damage is just state" fails in four places (medium, sure)

`boats_stove` is written at `hits.py:225` and read only at `api/action_readings.py:318`. `Gun.condition`
is lowered at `hits.py:260` and read by nothing in `combat/` or `orders/gunnery.py` (grep).
The spar carry-in sets `sp.wrecked = True` directly, and dismounts guns from the reversed
dict, at `far_action.py:518-554` (read). **STANDS.** Medium.

### 04-6. Boarders never leave the guns; `repel boarders` never ends (medium, sure)

`grep repelling` over `freesail` finds only one assignment: `boarding.py:718`, which sets it
True. **STANDS.** I did not test the boarders' muster against `at`. Medium.

### 04-7. The strike written five ways, int and bool in one key (medium, sure)

`gunnery.py:939-944` writes `True` only when `world_of(ship)` is None. That happens off any
World, which play rarely reaches. A strike at tick 0 needs a scenario's opening order to
strike. The five writers are real. The int-and-bool hazard is near nil in play. **STANDS IN
PART.** Low.

### 04-8. Stale words to the player (medium, sure)

`gunnery.py:946-950` is the reply to every `strike the colours`. It is not a fallback branch.
`possess` and `captive.player_taken` are built. **STANDS.** Medium: the player reads it at the
most consequential moment of the action.

### 04-9. Signals overgrown, "engage from to windward" unparsable (medium, likely)

I confirmed that the four entries carry `does: {order: "engage from to windward"/"leeward"}`.
No handler for "from to", "weather gage" or "lee gage" exists in `freesail/orders`.
`_engage` → `_mark` would take "from to windward" as a sail's words (`gunnery.py:374-413`).
I did not run it, and I did not read `_side_of`, which might consume "windward". The
"overgrown" part is a judgement I did not test. **STANDS IN PART.** Low-medium.

### 04-10. Hazardous shape (medium, sure)

**NOT re-counted.** The local `agents` imports I sampled are real (`captains.py:2624` is in
code-02's part). **STANDS** on the reader's counts.

## Found on the way

1. **The player's first order of the gun deck relieves the captain who would have cast loose,
   and says nothing of it.** I ran the same three orders at ticks 0, 30 and 60, before the
   captain's first judgement (`player_hand` gives no hand then, `captains.py:2491-2494`).
   Mr Bowen then went on to `engaging` at 480 s, gave "casting loose the guns (an enemy in
   range)" himself, and the action was fought: `guns.cast_loose` at 694 s, then "Three shot at
   a cutter: one struck her".

   Given at 400 s, `beat to quarters` made him stand aside (`core/world.py:2108`), striking his
   book. His casting loose was never given. So whether the guns are ever cast loose depends on
   whether the player spoke before or after the captain's first judgement. Neither the
   `captain.aside` line nor the beat's reply tells him that the gun deck is now his to finish.
   This is the mechanism behind the reviewer's silent action.
2. **A second false "already"**: by standing order 'the charge', "The guns are loading with
   round shot already" with every gun secured (log at 401 s in the run above).
3. **Brainless ships cannot be hurt by gunfire at all** (04-3, widened). About twelve shipped
   scenarios carry brainless sail. `tender.yaml` (cap 0) makes every mark so.
4. **The near Captain persists across sleep** (`crews.demote` keeps the World). This softens
   02-3 and is worth the reviewer's knowing before he puts the fold to the owner.

## What I did not do

I did not read either first reader's modules whole. I read only the lines cited and those
named above. I did not read `hulls.py` (02-8), `_side_of`, the squadron or regime data beyond
`blockade.yaml`, or the boarding muster. I ran no test. Each reproduction used the tests'
helpers or the console's own construction of the world, not the console itself.
