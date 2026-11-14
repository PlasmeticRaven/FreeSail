# Second reader 06: the director (spec-05, M7b) and the officers and captains (spec-03, M6)

Tree: HEAD 6350683, which differs from the commit under review (504a250) only in files
under `docs/reviews/ColdReview-M7-evidence/` (`git diff --stat 504a250 HEAD`: evidence files
alone). No test suite run, no file of the tree changed. Probes are short python scripts in the
session scratchpad (`p1.py` to `p9.py`), each building one world with the tests' own helpers
(`tests.test_director.directed`, `tests.test_crews.hove_to_world`) and calling
`director.direct`, the same function the model director's `world_order` tool calls
(`freesail/agents/tools.py:508`) and the player's director seat calls (`seat.py:488`).
Read for the defence: `docs/DesignProposal.md` §7.6 and decisions 40, 41, 46, 50, 52, 59, 62,
63; `docs/TechnicalSpec-M6.md` 262-275 and 668-680; `docs/TechnicalSpec-M7b.md` 910-925.

## The table

| finding | first reader's weight | verdict | my weight |
|---|---|---|---|
| 05-1 the director can sail the player's ship (`captain: intent`, `carry on`) | high | STANDS IN PART (the player's next order still puts the captain aside; the rest stands, and a second road found) | high |
| 05-2 reach does not cover a held person's body (captain wounded under `nobody_dies`) | high | STANDS, and worse (the wound kills by M7's health one time in three to six in ten) | high |
| 05-3 the enemy limit passes a seventy-four called "line-of-battle ship" | medium-high | STANDS (also "a 74"; the limit fails open on any word it cannot rank) | medium-high |
| 05-4 two limits empty; the swamped boat kills under `nobody_dies` | medium | STANDS, and worse (the player's own person killed, first entry, no doubt) | high |
| 05-5 the fake exercises plumbing only; no real model's run | medium | STANDS IN PART (a real model is not what was missing; the hand tests were) | low-medium |
| 05-6 "small once both exist" grew to 3,500 / 16,000 lines | medium | STANDS IN PART (3,516 is the director's; 16,000 is the milestone's) | low-medium |
| 05-7 the budget is no guardrail (48-72 acts, not 4-8) | medium | STANDS IN PART (the owner's word, the proposal left the budget open) | low |
| 05-8 ten named features unbuilt | medium | NOT TRIED (inventory, not a fault I can refute) | medium |
| 05-9 the spec contradicts itself, is history | medium | NOT TRIED beyond one check | medium |
| 05-10 the M7 channels carry no brief limit | low-medium | STANDS IN PART | low |
| 03-1 the captain reads the truth through `getattr`; the test is evaded | high | STANDS IN PART (evasion real and wider; most of what he reads he could have perceived) | medium |
| 03-2 the human at the officer's seat has no "danger" road | high | STANDS | medium |
| 03-3 the rule of the road has no crossing, untested in play | medium | STANDS IN PART (true; no ship-to-ship collision exists, so it costs little) | low |
| 03-4 doctrine as data is half true; 12 keys unread | medium | STANDS (checked six by grep: nothing reads them) | medium |
| 03-5 crewed cap measured before the rebuild; pace test hove to | medium | STANDS IN PART (truth 88 guards the cap on today's build; "two figures" overstated) | low |

## spec-05 (the director)

### 05-1. The director can sail the player's own ship (high; sure)

**What I did.** Reproduced the probe (`p1.py`): `directed("quiet-passage")`, the player orders
`steer west`, 300 s run, then `D.direct(w, "captain: intent bound for Plymouth")`. Before the
order: `active False commands False aside False state None intent None` (this scenario has no
intent: the player sails her by hand). Result `Done ... (47 acts of the day's 48 left.)`;
900 s later the log carries `captain.state` "Captain Bowen: on passage (bound for Plymouth)",
`captain.plan`, `helm.set` "Shaped a course ... NE", then fore topsail, spanker, topgallants
set and `helm.steady` "Steady on NE (48°)". The first reader's probe holds exactly.

Then I looked for the defence.

- *Is it the designed seam?* In part. `TechnicalSpec-M6.md:268-269` (package 40) says the
  intent is "given by the world order `captain: <intent>` (the scenario's and the director's;
  refused at the prompt as every world order is)". `orders.py:120-121` calls it "the
  director's seam" and `orders.doubt`'s docstring (`orders.py:4099-4102`) exempts `captain:`
  from the doubt as "a mind changed". So the lead built it deliberately as the director's. But
  the proposal's rule (§7.6, "cannot move the player's ship, change a sail, or countermand an
  order") is the owner's and earlier, and the code's own words for the parallel road keep it:
  `_hand_reach` refuses `ship "X": order` on the player's ship with "the director moves no sail
  of hers and gives no order of hers" (`orders.py:1461-1464`), and the director's station
  brief tells the model "You cannot move the player's ship, change a sail or countermand an
  order ... no order goes through ... any of the player's own ship" (`director.py:1305-1320`).
  The seam contradicts the brief the model is given and the reach rule beside it.
- *Decision 41.* It gives the rules captain the ship on an *intent scenario* and makes the
  player's direct order put him aside "until `captain: carry on` gives her back to him; a
  world order does not". It says nothing of a director putting a hand-sailed ship under the
  rules captain, and it presumes `carry on` is the player's road back, not the director's.
- *Does the player's direct order still make him stand aside?* Yes, and promptly. `p1.py`:
  after the director's intent the player's `steer west` gave `captain.aside` "Captain Bowen
  stands aside at your order ('steer west')", `commands False`. `p7.py`: the director's intent
  at tick 300, the captain's first judgement at 301, the player's `heave to` at 320 put him
  aside at once; no window in which the player's order was overruled. This part of the defence
  holds: the player can take her back with any order.
- *But the director can take her back again.* `p2.py`: after the player's hand,
  `D.direct(w, "captain: carry on")` gave `Done: Captain Bowen carries on` (46 acts left),
  `aside False commands True`, and 400 s later `state on passage`: the director undid the
  player's order, which is "countermand an order" in plain words. It costs one act of 48.
  (A fresh `captain: intent` while he stands aside leaves him aside: `set_intent` does not
  clear `aside`, `captains.py:2470-2486`; so `carry on` is the road.)
- *Open to a model?* Yes. `tools.world_order` returns `director_mod.direct(world, text,
  by=harness.model_name)` (`tools.py:508`), the same function as the probe. The forms table
  offers it to the model as an example: `Form("captain", ..., "captain: intent <words>",
  ("captain: intent trade tin from Falmouth to Brest",), "the followed ship's rules-based
  captain given an intent")` (`director.py:918-924`), and the followed ship is the player's
  unless the director follows another.
- *What the director's log shows.* `D.log_of(w).entries` after `p2.py`: "Given: captain:
  intent bound for Plymouth; the captain's intent: bound for Plymouth", "Given: captain: carry
  on; Captain Bowen carries on: bound for Plymouth". The act is recorded plainly for the
  reveal; no doubt, no reason asked. The player's play log shows only that his captain took a
  plan (`captain.state`, `captain.plan`) with no cause, which by decision 46 is as intended.
- *A second road* (found here, `p8.py`, `p9.py`): `ship "Amazon": intent bound for Plymouth`
  on the player's own ship is `Done` ("the captain of Amazon given an intent"): the first
  gives her own `Vessel` (`vessels.find("Amazon")`, id `the ship`) a `FarCaptain`; the second,
  `Done: the intent of Amazon's captain changed`, calls `vessel.crew.captain.set_intent`
  (`orders.py:786-789`), and the player's captain is `active True commands True`, `state on
  passage` 400 s later. `reach` judges a `ship "X":` order only when its tail is `order ...`
  (`orders.py:586-591`, `_HAND_TAIL` 628), so the `intent` tail on the player's own ship
  escapes the very refusal `_hand_reach` was written for.

**Verdict: STANDS IN PART.** Falls: that the player loses his ship; one order of his puts the
captain aside, at once. Stands: the director can, unrefused and undoubted, put a hand-sailed
player's ship under the rules captain (sails and course changed with no order of the
player's), and can undo the player's own hand with `captain: carry on`, as often as its acts
allow; by two channels (`captain:` and `ship "<own>": intent`); the station brief the model
reads promises the opposite. No test gives `captain:` or `ship "<own>": intent` through
`director.direct` (grep of `tests/`: only `w.world_order(...)` and `apply(...)`, the owner's
roads). **Weight: high**, because it is the one rule the proposal names for the director and
the model is told it is kept.

### 05-2. The rule of reach does not cover a held person's body (high; sure)

**What I did.** `p6.py` (hove-to frigate, quiet-passage brief, the player holding the
captain): `aboard: Captain Bowen is badly hurt` was doubted (smooth sea), re-entered with
`[reason: probe]`, `Done: found aboard: Captain Bowen wounded (a fall from the gangway,
dangerously)`; `sailor.wound grave`. `reach` (`orders.py:2580-2633`) judges `aboard` only by
`_aboard_reach` (things and money, `orders.py:3167-3200`); `_fx_person_hurt`
(`orders.py:3607-3628`) checks only that he is on the muster. `limit_of`'s `nobody_dies` asks
only for `harm: deadly` (`director.py:338-341`); `person_badly_hurt` is `harm: hurt`
(`aboard.yaml:281-289`).

Looked for a defence: does a grave wound kill? It does. `crew/health.py:79-85`: the grave
wound "is judged at a day, dies with these chances" `DIE_GRAVE_TREATED = 0.3`,
`DIE_GRAVE_UNTREATED = 0.6`, and `health.py:591-595` calls `_dies` on it; `COLLAPSE_S = 1800`
collapses a station holder with a grave wound undressed. In my 12 h run he was alive (the
judgement is at 24 h; not run that far). So the `harm: hurt` label is wrong for this entry by
the code's own figures: a "nobody dies" brief allows an order with a 30 to 60 per cent chance
of killing the player's person.

**Verdict: STANDS, and worse than reported.** Weight: high.

### 05-3. The enemy limit passes a line-of-battle ship (medium-high; sure)

**What I did.** `p3.py`, `p4.py`: `size_rank_of` returns None for "line-of-battle ship",
"a line of battle ship", "74", "third rate"; 4 for "ship of the line", "seventy-four",
"two-decker" (`captains.py:330-366`). Under the quiet-passage brief (no enemy heavier than a
cutter): `ship: a line-of-battle ship "Brave" of France ...` **Done** ("a seventy-four, a ship
of the line, fourteen ports a tier"); `ship: a 74 "Brave2" of France ...` **Done**; `a ship of
the line` and `a frigate` refused. The ship maker's words (`ships.py:354-362`) know "a 74",
"line-of-battle ship", "a line of battle ship"; the ranking (`_SIZE_WORDS`) does not.
`_enemy_heavier` returns None whenever either rank is None (`director.py:420-422`): the limit
fails open on any description it cannot rank.

**Verdict: STANDS** (and wider: "a 74" too; any unranked word). Weight: medium-high.

### 05-4. Two limits are empty; the swamped boat kills under `nobody_dies` (medium; sure)

**What I did.** `aboard.yaml` has no `harm: deadly` (grep); `boat_swamped` is `harm: none`
with the report "whoever was in her is lost" (`aboard.yaml:337-344`); `lose_boat`
(`boats.py:893-920`) sets `p.dead = True` for everyone in her who is not her own crew. Then the
probe the first reader did not run (`p5.py`): hove-to frigate, quiet-passage brief, the player
(Captain Bowen) `go to the launch`, `give way`, then `D.direct(w, "aboard the Amazon: the boat
swamped")`: **Done on the first entry, no doubt**: "The launch swamped alongside; Captain
Bowen lost with her." `Captain Bowen dead True where lost`. The player's own person, held at
the prompt, killed by one act of a director under "nobody dies".

Why no doubt: `p6.py` shows `doubt("aboard: the boat swamped")` = "the sea is too slight to
swamp a boat alongside", `_aboard_match` True; `doubt("aboard the Amazon: the boat swamped")`
= None, `_aboard_match` False. The named-hull head (`_ABOARD_HULL`, `orders.py:160-164`) is
not stripped before `_aboard_match`, which both the doubt (`orders.py:4606-4612`) and the
`nobody_dies` limit (`director.py:338-341`) rely on; the effect is still applied. So the
named spelling escapes the doubt and the brief's limit for every entry of the table, even a
deadly one if one were added. (`aboard:` without a name targets the followed hull, which
after `go to the launch` is the boat itself: "she carries no boat".)

`the_chart_as_it_is` has no branch in `limit_of` (read): confirmed, and the spec says so.

**Verdict: STANDS, and worse.** Weight: **high** (the player can be killed against his own
brief, and the doubt that should have caught it is bypassed by spelling).

### 05-5. The fake exercises plumbing only (medium; sure)

**What I did.** Read `fake.py:558-623`: a fixed list, every doubt or "no way" re-entered with
"the story wants it; the fake's", reads nothing. Correct. Defence: the guardrails are code
(`direct`, `reach`, `limit_of`, `doubt`) and are tested by hand through `D.direct` without any
model (`test_director.py:410`, `459`, `954`, `1385`); a real model is not needed to find
finding 1, a test of `captain:` through `direct` would have been. And real model directors
were run outside the tests: `test_director.py:1506-1508` records "the lugger director's first
ask ... 37% of its orders failed, learning the forms by refusal"; their records are under
`docs/playtests/`, which I may not open. **Verdict: STANDS IN PART**: the fake judges nothing
(true, and by design); "the guardrails a real model would test were never tried" falls: what
was missing is hand tests of the player's-ship roads, not a model. Weight: low-medium.

### 05-6. Size (medium; likely)

Not re-counted. The 3,516 lines are the director proper's; the 16,026 are the five parts of the
milestone plus fishing, the harbour and the boat, which the proposal's "the only new mechanism
is the world-order channel" never covered and which later decisions (52, 59, 62, 63) asked
for. **STANDS IN PART**: the director's own growth (3,516 against "small") stands; attributing
16,000 to the director does not. Weight: low-medium.

### 05-7. The budget is no guardrail (medium; sure)

`data/director/briefs/*.yaml`: every starter's `acts_a_day` carries "the owner's word of
2026-10-19, the budget a tuning point, not a constraint for the first testing". The proposal
left the budget an open question (§7.6, last paragraph) and makes the brief the guardrail.
**STANDS IN PART**: the numbers are as said; it is the owner's chosen state, not a fault. One
real fault beside it: the comment at `director.py:121-122` still says "four acts a day keeps a
quiet passage quiet" over `DEFAULT_ACTS_A_DAY = 48`. Weight: low.

### 05-8, 05-9. Unbuilt features, the spec as history (medium)

**NOT TRIED**: inventories of the document; nothing in the code to refute. Weight as given.

### 05-10. The M7 channels carry no brief limit (low-medium)

`limit_of` judges weather, ship, aboard, port (`director.py:322-357`). A squadron is made of
ships already on the sea (`test_director.py:1484-1487`), so the enemy limit binds it at the
`ship:` step; `convoy` draws the nation's own escort. `court` and `command` not read.
**STANDS IN PART**, weight low.

## spec-03 (officers and captains)

### 03-1. The captain reads the truth; the grep test is evaded (high; sure)

**What I did.** Read `captains.py:4307-4345`, `4505-4590`, `2215-2235`, `2293-2305`, and the
test `tests/test_captains.py:276-300`. The test asserts the literal strings `world.position`
and `world.vessels` are absent; the module spells them `getattr(self.world, "position",
None)` (4556) and `getattr(world, "vessels", None)` (4578, and also 2229 and 2300, which the
first reader did not list), which pass it. The evasion is real and wider.

What he does with the truth, and could the lookout have given it:
- `_stranger_struck`, `_enemy_struck` (4520-4532): `v.struck`. The strike is said to the ship
  as the action's own line (`lookout.py:833-834`, "the strike is the action's own line
  (`action.enemy_struck`)"), so the same fact is perceived; the shortcut changes nothing but
  at night or out of sight. Low.
- `_take_possession` (4556-4560): the true distance to the prize to decide "within a boat's
  pull". The lookout's `estimate_m` (`lookout.py:337, 593`) gives the same within its factor,
  and the captain uses `estimate_m` elsewhere (`_nearest_stranger`, 4582-4586). Low.
- `_prize_taken`, the prize record (2229, 2300): whose prize she is, which he could know from
  her colours and his own prize crew. Low.
- `_boarding` (4325-4337): the enemy's fit company counted man by man from her crewed body,
  to compare with `board_odds`. No lookout reads that; this is a real truth leak in a decision
  (when to board), not reproducible from what is seen except as an estimate by her class.
  Medium.

Decision 40's "perception on the player's terms" is broken in one real decision and shortcut
in three where the perceived fact exists; the test that claims "by any road" is false.
**STANDS IN PART.** Weight: medium (the misleading test is the larger cost to a maintainer).

### 03-2. The human at the officer's seat has no "danger" road (high; sure)

**What I did.** `PlayerSeat.route` (`seat.py:450-472`) ends `return self.submit(line)` with no
`danger`; `PlayerSeat.submit(text, danger="")` (507) passes it to `tools.judge` (535), so the
machinery accepts it but no caller supplies it: grep `danger=` over `freesail/` finds only
`agents/agent.py` and `agents/tools.py`; no form in `freesail/orders/` parses a danger in
words. Worse, the refusal the human is shown ends with `DANGER_ROUTE`: "give the order with
submit_order(text, danger='...')" (`tools.py:891-893`), a tool call he cannot make. Defence:
decision 62 makes the player the captain by default, so the officer's seat is the lesser road.
It does not answer ruling 1's parity. **STANDS.** Weight: medium (a seldom used seat, but in
it the human cannot save the ship from a danger a model officer could).

### 03-3. The rule of the road has no crossing, untested in play (medium; sure)

Read `captains.py:4676-4712`, `4753-4782`, `tests/test_captains.py:380-399`. All as said:
any made-out stranger within `ROAD_CABLES` whose course is in the lookout's words triggers
it, once an encounter; the one give-way is "bear away two points"; two ships off the wind both
stand on; only the arithmetic is tested. Defence: the 1805 custom was a custom, and there is
no ship-to-ship collision in the physics (grep of `freesail/physics/` for collision: nothing;
the hits are boarding and the lookout), so a wrong judgement costs a log line and two points
of course. **STANDS IN PART**: the facts stand; the weight falls. Weight: low.

### 03-4. Doctrine as data is half true (medium; sure)

grep over `freesail/` for `road_cables`, `leg_reached_nm`, `anchor_within_nm`,
`stranger_chase_nm`, `station_wear_hours`, `spell_minutes`: no hit; `burns_when` and
`mans_prizes` only in comments (`prizes.py:1238`, `squadrons.py:1556`); no dynamic key
(`threshold(f"...")`) anywhere. `_th` reads by literal key (`captains.py:4259-4261`).
**STANDS.** Weight: medium (the owner tunes a file and nothing changes).

### 03-5. The crewed cap measured before the rebuild; the pace test hove to (medium; likely)

Read `crews.py:84-106`, `tests/test_crews.py:25-29, 193-217`, `release.yml:50-58`. Defence:
truth 88 asserts the floor (60 ticks a second) with the cap full on the build as it is now,
and the release workflow runs the `pace` tests alone (`release.yml:58`), so the cap is guarded
on the one-world architecture whatever the old measurement was; `HELD_OVER_CAP` cites "the
pace of a convoy with four held hulls" measured in package 82b, which came after 84 (decision
52's order), so some measurement post-dates the rebuild (the notes themselves are under
`docs/dev/`, unread). "One measurement, two figures" is overstated: the module's "about 140"
is "quiet", the docstring's "100 to 114" is "with the three under sail" (`crews.py:93`,
`test_crews.py:198`). What stands: the range is judgement, not measured (the code says
"judgement on the measurement's cost", `crews.py:89`), against decision 40's "chosen from a
measurement ... not guessed"; the frigate is hove to in the test; and the release runner is not
"the build machine" the floor is calibrated for. Whether hove to is cheaper I did not measure.
**STANDS IN PART.** Weight: low.

## Found on the way

1. **`ship "<the player's own ship>": intent <words>`, given twice, hands the player's ship to
   the rules captain** (`p9.py`): the hand's reach checks only an `order` tail
   (`orders.py:586-591`). A second road for 05-1. High; sure.
2. **The named-hull spelling of `aboard` escapes the doubt and every brief limit**
   (`aboard the Amazon: ...`, `_aboard_match` False, `doubt` None; `p6.py`), and with it the
   player's person was killed on the first entry (`p5.py`). High; sure.
3. **`person_badly_hurt` is deadly by M7's health** (30 per cent treated, 60 untreated, at a
   day: `crew/health.py:79-85, 591-595`) but labelled `harm: hurt`, so `nobody_dies` never
   refuses it. High; sure (by the code; the death not run to 24 h).
4. Two more `getattr(self.world, "vessels")` roads in `Judgement` (`captains.py:2229, 2300`),
   shared by the far body, which the grep test also misses. Low; sure.
5. `director.py:121-122` comment "four acts a day" over a default of 48. Low; sure.

## What I did not do

Did not run any test or the pace tool; did not run a grave wound to its 24 h judgement; did not
read `world/court.py` (the `court` and `command` channels' reach over the player); did not open
`docs/dev/` or `docs/playtests/` (the measurements and the model directors' runs); did not
check whether the player's own `Vessel` given a `FarCaptain` by the first `ship "Amazon":
intent` has any later effect (at a demotion or when he leaves her).
