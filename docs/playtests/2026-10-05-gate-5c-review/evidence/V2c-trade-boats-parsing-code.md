# V2c: the port's trade, the boats, the ship's papers and the order language's parsing (code and data)

Code reader's report, read-only. Baseline tree: `D:\Projects\FreeSail\FreeSail-gate-m5c\` (all `path:line` references are to it).
Every file cited here is byte-identical in `FreeSail-gate-m5c-b` (checked with `cmp`: `world/ports.py`, `world/places.py`,
`orders/*.py`, `evolutions/scripts.py`, `evolutions/runner.py`, `standing/*.py`, `data/vocabulary.yaml`, `data/papers/papers.yaml`,
the port files, `send_boat.yaml`, primer 14), so every finding holds for both builds.

Method: reading the code and data; greps of the sessions' full logs, inputs and transcripts; and parse-only checks run in memory
against the package (`orders.grammar.parse`, `orders.port.number_in`, `orders.ground_tackle._fathoms`,
`standing.grammar.parse_condition` / `parse_duration` / `parse_standing`, `orders.stations.recognises`,
`orders.verbs._take_in_word_check`) with `PYTHONDONTWRITEBYTECODE=1`, and one check through `orders.handle` on a bare ship
object (no world, no runner) with an anchor marked down, for the at-anchor gate in section H. No world was run, nothing was
written but this file. One caution on the parse checks: `orders.handle` wraps `parse` with a few extra passes
(`orders/__init__.py:70-102`), so where it matters I traced `handle` by reading.

## Verdicts at a glance

| # | Claim | Verdict |
|---|---|---|
| A1 | Owner: the price list should hold every visited port's prices, updated on a visit | PARTLY: the *paper* already does (every list aboard, dated); the *reading* `the prices` and its alias `the price list` show one list; the paper's own catalogue words say "the last port". Not refreshed by a bargain's boat. |
| A2 | Model: a port's goods are not visible before the prices are known; Roscoff takes neither coal nor pilchards | CONFIRMED in code and data. No reading, paper or pilot's word gives another port's goods. Only primer 14 has one prose sentence each for Roscoff and St Mary's. |
| B | One bargain per boat trip, about 4½ hours each | CONFIRMED (as built and as the primer documents; spec M5 §23 is silent). 4 h 36 m is the 40-ton trip; the other bargains' trips ran 2 h 17 m to 3 h 49 m, a trip for the prices about 2 h. |
| B' | `send the boat` refused 2½ miles from Falmouth's roads, the words not saying why | CONFIRMED: the rule is "an anchor down within 2 nautical miles of the outer road, the anchorage or the mooring"; the refusal says "no shore within a boat's pull". |
| C | A boat belayed mid-hoist is stuck "away, hoisting out" for good | CONFIRMED in code. Three routes, two of them seen: a `belay` (session 3), and a silent one with no belay by anyone (session 4, the anchoring evolution). A refused order also put the mate "in the boat". |
| D | Number words above twelve fail | CONFIRMED, and wider: five separate readers with five different word lists; none reads thirteen, fourteen, seventeen, eighteen or nineteen. |
| E | The water sail cannot be taken in by name; `take in the water sail` is read as watering; `furl` refused; `watersail` unknown; only the group works | CONFIRMED for the four mechanisms; PARTLY for "only the group works": `haul down / douse / hand the water sail` parse correctly. |
| F | `full and by` for the captain | WORKS AS DESIGNED: accepted, canonical verb `keep her full`. `close hauled` is not taken. |
| G | `what is she`, `make her out`, `the strangers` | CONFIRMED working. |
| H | Refusals that read as bugs | 545 `order.rejected` lines in sessions 2, 4, 5, 6, 7, 8: 322 (59%) raised by standing orders firing, 131 the captain's, 92 the officer's. Table below. |
| I | The ship's papers | CONFIRMED working; eight papers, all made live from their stores; three ever get a new "last written" date. No paper or reading holds the ship's draught, which two sessions searched for. |

---

## A. The price list, and what a port shows of its trade before arrival

### What the code does today

- The lists aboard are `Ports.price_lists`, a dict by port id of `(tick, when, [(good, price), ...])` (`freesail/world/ports.py:516`).
  One entry per port, overwritten when a new list comes off from that port.
- A list is written (a) at the start for each id in the scenario's `papers: price_lists` (`ports.py:544-548`, no log line), and
  (b) when the boat comes back carrying a `prices` item (`ports.py:1615-1633` calling `_write_price_list`, `ports.py:1065-1079`;
  log lines "The price list written up by the mate: the prices at Plymouth brought off by the boat." and "The mate's list of the
  prices at Plymouth is aboard: coal £2, canvas £55, hemp £65, salt £24 a ton, and the rest.").
- The boat carries a `prices` item only when its errand is prices, person, message or yard, or when the port's list is not aboard
  yet (`ports.py:1552-1556`). A purchase or sale trip to a port whose list is aboard does not bring a new one.
- **The paper** "the price list" prints every list aboard, each with its port and date: `freesail/world/places.py:440-449`
  (`for port_id, (_tick, when, listed) in ports.price_lists.items(): lines.append(f"Prices at {port.name}, {when}, a ton at the quay:")`).
  It is served by `library(topic='papers', section='price list')` and the browser's papers pane (`agents/tools.py:1330-1372`,
  `ui/server.py:588-617`).
- **The reading** `the prices` (aliases `the market`, `the price list`: `data/vocabulary.yaml:1303-1304`) answers one list only
  (`ports.py:1034-1055`): in port with that port's list aboard, "at Plymouth (21 June, ...): coal £2 a ton, ..."; otherwise
  "the last list, <port> (<when>): ..."; with none aboard, "the prices at X are not known until the boat has been ashore" in
  port or "no prices are known: the boat has not been ashore in any port" at sea (`ports.py:1057-1061`).
- Documents against code: `data/papers/papers.yaml:62` describes the paper as "the prices at the last port the boat was ashore
  in"; the code prints all of them. `freesail/api/readings.py:1948` describes the reading as "the prices at the port she lies in".

So the owner's note 3 is already true of the paper as coded (verified by reading; tool results are not kept in the saves, so I
could not see a page). What a captain at the order line gets from `the price list` is the one-list reading, because that phrase is
an alias of `the prices`, not the paper. CANNOT TELL which of the two the owner was looking at.

Three smaller faults in the same place:

1. "The last list" is the last port *first inserted* into the dict, not the list brought off most recently
   (`ports.py:1047`: `list(self.price_lists.items())[-1]`; re-writing an existing key keeps its position). Plymouth, Roscoff,
   Plymouth again, then at sea: the reading shows Roscoff.
2. The list goes stale against the bargains it invites. A bargain is struck at the live price (`ports.py:1121`,
   `price_of` at `1081-1084`), each ton moves the price 1% (`ports.py:142`, `258-262`), and the list aboard is not refreshed by
   the purchase's own boat. After buying 40 tons, the next ton of that good costs 40% more than the list says, and the captain
   learns it only from the bargain line. Not hit in the playtests (each good was traded once per visit).
3. A scenario's `price_lists` id that matches no port is skipped in silence (`ports.py:546-548`: `if pid in self.ports`).
   `data/scenarios/merchant-schooner-plymouth.yaml:64` (the owner's playtest scenario, dated 3 October) says
   `price_lists: [Plymouth]`; the port id is `plymouth`. The Speedwell therefore started sessions 3 and 4 with no list
   ("The prices: the prices at Plymouth are not known until the boat has been ashore.", session 3 tick 2,992) and spent the first
   two hours of session 4 on a boat trip for it (tick 114 to 7,649). The other four scenario files spell it `[falmouth]`.

### Is a port's trade visible anywhere before arrival?

No. CONFIRMED from code:

- The only place the game names what a port deals in is the market's refusal, and that needs her in port with the list aboard:
  `ports.py:1113-1118`, "Roscoff's market has no coal; it deals in brandy, geneva, rum, tea, tobacco, wine, salt, canvas, onions,
  tin, salt beef." (session 4 tick 212,090, the officer's `sell forty tons of coal`).
- The pilot's news is the scenario's `news` strings plus the wars (`ports.py:940-944`). `the port` gives stance, pilot and boat
  (`ports.py:976-1018`). The epitome's paper is the tide table (`places.py:426-439`). No reading names a good.
- The one pre-arrival source is prose in the primer, a library topic and not a reading: `docs/primer/14-the-port.md:259`
  ("The market is the trade the port lived by, brandy, geneva, rum, tea and tobacco priced for the Cornish run, beside the wine,
  the salt and the canvas of the coast") and `:238` for St Mary's. Nothing for Plymouth or Brest. Session 4's officer read that
  Roscoff section at tick 198,139 (transcript entry 201), two days after buying the coal (tick 7,792) and the pilchards (24,374).

### What each port trades

A port has one list of goods and one price per good; it buys and sells at the same price (`Market.price`, `ports.py:242-246`;
`trade` uses it for both verbs). Prices below are pounds a ton in June 1805 with no supply shift: base price × the month's
season factor × 1.5 when the good's origin is at war with the port's nation (marked *). Computed from `data/ports/*.yaml`
(market sections: `falmouth.yaml:77`, `plymouth.yaml:60`, `st-marys.yaml:99`, `brest.yaml:62`, `roscoff.yaml:103`) and checked
against the lists the logs printed (Falmouth session 2 tick 6,141; Plymouth session 4 tick 7,649 and session 5 tick 54,016;
Roscoff session 2 tick 182,223; Brest session 1 tick 130,550).

| good | Falmouth | Plymouth | St Mary's | Brest | Roscoff |
|---|---|---|---|---|---|
| tin | 120 | - | - | 270* | 255* |
| copper ore | 9 | 11 | - | 30* | - |
| pilchards | 17 | 19 | 15½ | 45* | - |
| coal | 2 | 2 | 3 | 9* | - |
| salt | 25 | 24 | 28 | 12 | 12 |
| canvas | 60 | 55 | - | 40 | 42 |
| hemp | 70 | 65 | - | 55 | - |
| wine | 70 | 75 | - | 35 | 38 |
| brandy | 300* | 315* | 240* | 110 | 100 |
| timber | 6 | 6 | 8 | 5 | - |
| salt beef | 55 | 50 | 60 | 70 | 70 |
| biscuit | - | 40 | - | - | - |
| geneva, rum, tea, tobacco, onions | - | - | - | - | 70, 80, 170, 60, 6 |
| kelp, salt fish, potatoes, barley | - | - | 4½, 20, 5, 9 | - | - |

What this says for the playtest:

- **Plymouth to Roscoff:** the two ports share five goods (canvas, salt, wine, brandy, salt beef). Only **salt beef** pays
  (50 to 70, +£20 a ton). Coal and pilchards are not on Roscoff's list at all. They do sell at Brest (coal 2 to 9, pilchards
  19 to 45), so the cargo was a sound one for the other French port; nothing the game showed before arrival told the two apart.
- **Was the mistake avoidable from what the game showed?** Only by reading the Roscoff section of primer 14 before buying, and
  that sentence omits tin, onions and salt beef and does not say what is refused. Not from any reading, paper or person.
- **Ten goods are dealt in at one port only** and so can be bought and never sold: biscuit (Plymouth); geneva, rum, tea,
  tobacco, onions (Roscoff); kelp, salt fish, potatoes, barley (St Mary's). The Roscoff file and the primer call the first four
  "priced for the Cornish run" (`roscoff.yaml:105-107`), and no Cornish port's list has them. Documents and data disagree; a
  trader who buys tea at Roscoff has nowhere to land it.

### Fixes and sizes

- **(1) Lists by port with the date seen.** The store and the paper are done. Left to do: make `the price list` at the order
  line answer the paper (all lists) instead of the one-list reading, or add `the prices at <port>` as a parametric reading like
  `the bearing of <mark>`; pick "the last list" by tick; correct `papers.yaml:62`. Touches `ports.prices_reading`,
  `orders/prompt.py`, `data/vocabulary.yaml` (`reading_words.aliases`), `api/readings.py`. **S** for the alias and the words,
  **M** with the parametric reading and tests. Refreshing the list on every boat back from the port (drop the errand test at
  `ports.py:1552-1556`) is S. Risk: an extra `paper.written` and `market.prices` line on each purchase trip would move the pinned
  merchant passage (`tests/test_known_truths.py:3732-3733`, `GATE_5C_MERCHANT_LINES = 2460`, `GATE_5C_MERCHANT_DIGEST`).
  Validate `price_lists` ids at load, case-folded, as `ports:` ids already are (`ports.py:538-542`): S.
- **(2) Goods before prices.** The data exists (each port file's goods). Cheapest form: the price-list paper and the
  "not known" answers add, for each port of the world with no list aboard, "Roscoff: no list aboard; deals in brandy, geneva,
  rum, tea, tobacco, wine, salt, canvas, onions, tin and salt beef". `places.py:440-449` and `ports.no_prices_words`: **S**.
  The design question is what the ship knows at the start. A master of 1805 had it from common knowledge of each coast's trade,
  the printed prices current and Lloyd's List, his owner's letter of instructions and correspondents, and other masters and
  pilots spoken on the way. That argues for a paper of its own ("the owner's instructions" or "the supercargo's memorandum")
  listing the trades of the ports the scenario names, without prices, plus the pilot's news naming what his port wants.
  **M** with a scenario key, the primer and tests; a small design decision first (all ports of the world, or only those in the
  instructions). The one-port goods are a data decision for the owner.

---

## B. One bargain per boat trip, about four and a half hours each

**Verdict: CONFIRMED as built.**

### Mechanism

- `Ports.trade` (`ports.py:1086-1183`) refuses a bargain while the boat is away (`1109-1112`: "The long-boat is away; wait for
  her."), moves the purse at once (`1137` for a purchase; `1156-1157` breaks out the hold and credits the purse for a sale), and
  then starts a boat trip of its own for that one item (`1139-1143`, `1159-1163`: `_send_boat(port, "purchase", [one item])`).
  There is no way to make the bargain without the trip and no way to add to a trip.
- Logs: session 4 tick 7,793, one second after the coal bargain, `buy twenty tons of pilchards` refused "The long-boat is away;
  wait for her."; the pilchards were bought at 24,374, ten seconds after the coal came aboard. Session 2 ticks 182,318 and
  182,334, `buy fifteen tons of brandy` refused the same way three seconds after the tin's sale had sent the launch off.
- Only one boat ever goes: `boat_spec` picks the largest (`ports.py:1426-1430`), `Ports.boat` is a single `BoatState` (`:517`),
  and the script holds "the boat" (`evolutions/scripts.py:5233-5234`). The schooner's yawl, the brig's cutter and jolly boat and
  five of the frigate's six boats never leave the booms.
- The trip's length (`SendBoatScript`, `scripts.py:5236-5304`):
  `2 × hoist (300 s × the weather and crew factor) + 2 × (straight-line distance from the ship to the port's landing ÷ 4 knots)
  + BOAT_ASHORE_S[errand] + 180 s × tons`. Constants at `ports.py:117-137`: prices and yard 1,800 s, a person 900 s, a purchase
  or a sale 3,600 s, the lighter three minutes a ton. All marked judgement in the file.
- The boat's evolution asks for 11 hands on every ship (`data/evolutions/send_boat.yaml:36`), the frigate launch's figure, and
  holds what it gets for the whole trip. The schooner's long-boat is listed at 7 hands and the cutter's boat at 5; on the
  cutter 11 is over a third of a company of 30, away for hours. This is one source of the notes' "lead standing orders fight
  for hands".

### The trips in the logs

| session, port | errand | ordered to alongside (ticks) | pull each way | at the quay | whole trip |
|---|---|---|---|---|---|
| 4, Plymouth (Cawsand Bay) | prices | 114 to 7,649 | 2,537 s (2.8 nm) | 1,800 s | 2 h 06 m |
| 4, Plymouth | 40 tons of coal | 7,792 to 24,364 | 2,543 s | 10,800 s = 3,600 + 40 × 180 | **4 h 36 m** |
| 4, Plymouth | 20 tons of pilchards | 24,374 to 37,212 | 2,512 s | 7,200 s | 3 h 34 m |
| 4, Roscoff | 16 tons of brandy | 212,162 to 224,147 | 2,446 s | 6,480 s | 3 h 20 m |
| 2, Falmouth | 7 tons of tin | 6,143 to 14,337 | 1,304 s | 4,860 s | 2 h 17 m |
| 2, Roscoff | prices | 173,285 to 182,223 | 3,009 s (3.3 nm) | 1,800 s | 2 h 29 m |
| 2, Roscoff | 7 tons of tin sold | 182,315 to 193,896 | 3,000 s | 4,860 s | 3 h 13 m |
| 2, Roscoff | 15 tons of brandy | 193,898 to 206,933 | 3,024 s | 6,300 s | 3 h 37 m |
| 2, Plymouth | 15 tons of brandy sold | 650,072 to 663,827 | 3,356 s (3.7 nm) | 6,300 s | 3 h 49 m |

"About 4½ hours" is the coal trip; the formula reproduces every row. The cost that matters is the serial rule: the Speedwell
was 10 h 19 m at Plymouth for a list and two purchases (05:01 to 15:20), the Harpy 9 h 20 m at Roscoff for a list, a sale and
a purchase (05:08 to 14:28).

### What M5 specified

Spec M5 §23 (`docs/TechnicalSpec-M5.md:479`): "the boat (sent ashore and back with hands and time, carrying a person, a message
or a purchase)". It does not say one bargain a trip. Primer 14 documents what was built (`docs/primer/14-the-port.md:137`:
"makes the bargain at the port's price now, moves the purse at once, and sends the boat for the goods, which go by the port's
lighter while the boat is at the quay, three minutes a ton"). The code's own comment says the boat does not carry the cargo
(`ports.py:134-136`: "Goods bought or sold go between the quay and the ship by the port's lighter, not by the boat's trips").

### Reasonable loosenings

The data path already takes several items a trip: `BoatState.carrying` is a list, `SendBoatScript.check` sums the tons of every
purchase and sale in it (`scripts.py:5255-5260`), and `_boat_back` stows each (`ports.py:1642-1663`). What blocks it is `trade`.

1. **Several bargains, one trip.** A compound order (`buy forty tons of coal and twenty tons of pilchards`) or bargains added
   while the boat is still hoisting out. `ports.trade` restructured to check every item before the purse moves;
   `orders/port.py:_tons_and_good` split on "and". **M.** For the Speedwell at Plymouth: about 5 h 35 m in one trip where the
   two took 8 h 10 m.
2. **The lighter as a job, the boat free.** The yard already delivers without a boat (`Job`, `ports.py:488-497`, `1240-1243`:
   "it will be alongside in 8 hours"). The market could do the same and keep the boat for prices, letters and people. **M.**
3. **A second boat** for prices, a letter or a person while the launch is on cargo: `BoatState` per boat, holds keyed by boat
   id. **M to L.**

Risk for all three: the merchant passage pins the single-bargain timing (`tests/test_known_truths.py:3709`,
`GATE_5C_MERCHANT_TIN_ABOARD_TICK = 14249`; `:3731`, `..._TIN_SOLD_TICK = 123004`). Options that only add a path leave those
ticks alone; changing the one-bargain path moves them and the digest. The 4 kn, 3,600 s and 180 s a ton are tuning constants
the owner can change in one place.

### The distance rule and its refusal (session 2, tick 525,621)

- **The rule.** `Ports.in_port` (`ports.py:578-583`): an anchor down (`core/world.py:550-552`) and the nearest of the port's
  three spots (outer road, anchorage, mooring; `Port.spots`, `ports.py:318-319`) within `IN_PORT_NM = 2.0` nautical miles
  (`ports.py:111-113`). The landing is not one of the three. The boat's pull is then measured to the landing
  (`to_shore_m`, `ports.py:592-594`), in a straight line.
- **The refusal.** `ports.py:1470-1478`. Under way within five miles: "She is under way; bring her to an anchor in Falmouth's
  roads before the boat goes ashore." At anchor outside two miles: "She is not in port; there is no shore within a boat's pull."
- **The log.** Tick 525,172, the officer: "the outer road two and a half miles W by S". Tick 525,621 (officer) and 526,536
  (captain), `send the boat ashore with the purser`: "She is not in port; there is no shore within a boat's pull." They gave up
  Falmouth and ran for Plymouth, where she grounded.
- **Why the words mislead.** They name neither the rule nor her distance, and "a boat's pull" is not what is measured. From the
  port files and the chart, lying two miles outside the outer road is accepted at a pull of up to 3.8 nm at Falmouth, 4.6 nm at
  Roscoff, 5.1 nm at Plymouth and 10.6 nm at Brest (the road of Bertheaume is 8.6 nm from the quay). The Harpy lay about 4 nm
  from Falmouth's quay and was refused; she had pulled 3.3 nm at Roscoff and would pull 3.7 nm at Plymouth. The primer does
  state the rule (`14-the-port.md:123`: "In port, at anchor within two miles of the roads").
- **What it should say.** "She lies two and a half miles from Falmouth's outer road; the boat goes ashore when she is at anchor
  within two miles of the outer road, Carrick Road or the harbour." The same for `trade`, `demand` and `enter_hands`
  (`ports.py:1096-1099`, `1196`, `1269`), which say only "She is not in port". **S**, one place each; no digest risk unless a
  pinned book is refused this way (the merchant passage's is not). Whether the rule should instead be a bound on the pull itself
  is a design question for the owner.

---

## C. A boat stuck "away, hoisting out"

**Verdict: CONFIRMED in code. Worse than reported: three routes, and the state is never recovered.**

### States and transitions

`BoatState` (`ports.py:467-485`): `away`, `errand`, `carrying`, `bringing`, `phase`, `people`. The life of a trip:

1. `Ports._send_boat` sets `self.boat = BoatState(away=True, ..., phase="hoisting out")` **before** it starts the evolution
   (`ports.py:1451-1462`), so the boat is "away" while its evolution may still be waiting for hands.
2. `SendBoatScript.tick` walks hoist_out, pull_out, ashore, pull_back, hoist_in (`scripts.py:5273-5304`), calling
   `Ports.boat_phase` for the lines.
3. The only reset is at the very end: `_boat_back` (`ports.py:1664`: `self.boat = BoatState(boat_name=name, ...)`).

`Runner.belay` removes the instance and releases its hands (`evolutions/runner.py:421-454`, `_remove` at `881-890`). `Script`
has no hook for being belayed or failed (`scripts.py:561-612`), and neither `SendBoatScript` nor `LayOutKedgeScript` cleans up.
So any removal before the last tick leaves `away=True` for ever. With it:

- `send the boat` is refused, "The long-boat is away already." (`ports.py:1446-1447`);
- `buy` and `sell` are refused, "... is away; wait for her." (`ports.py:1109-1112`);
- `get under way` is refused, "the long-boat is away; she cannot leave without her boat" (`scripts.py:4578-4579`);
- `lay out a kedge` is refused (`scripts.py:5091-5092`);
- a purchase's money is gone and the goods never come (the purse moved at `ports.py:1137`; the item sits in `carrying`). By
  reading only: both stuck boats in the logs were on the errand for the prices, so no money was lost in play;
- anyone sent in the boat stays "in the boat";
- a station's `stand by until the boat alongside` never ends by its event (session 3: stood by at tick 3,055, ended at its own
  word an hour later).

### Route 1: the captain's belay (session 3, not session 4)

The belay is in `3-schooner-trial-opus`, the first start of the Speedwell scenario, which was abandoned for it; session 4's
journal says so ("the first run of this scenario was restarted after the long-boat stuck halfway out").

```
3037 | order.accepted | the officer of the watch | By the officer of the watch: sending the boat ashore.
3038 | evolution.started | sim | Away the long-boat's crew! Hoist out the long-boat.
3054 | order.accepted | captain | Order: belay that.
3054 | work.belayed | captain | Belayed sending boat; the helm and the yards left as they stand at hoist out.
3058 | order.rejected | captain | Order not carried out ('Send the boat ashore with the mate'): The long-boat is away already.
3237 | order.rejected | captain | Order not carried out ('Send the boat ashore with the mate'): Mr Ray is in the boat.
6695 | query.reading | the officer of the watch | The boat: the long-boat away for the prices and what news there is, hoisting out.
6698 | order.rejected | the officer of the watch | Order not carried out ('send the boat ashore'): The long-boat is away already.
```

Two more faults show in those lines:

- **A refused order changed the world.** `Ports.send_boat` puts the named person in the boat (`ports.py:1496-1498`:
  `person.aboard = False; person.where = "boat"`) before `_send_boat` checks whether the boat is free (`:1502`, raising at
  `1446-1447`). The order refused at tick 3,058 moved Mr Ray; the second refusal at 3,237 reports him there. Mr Ray is the
  person whose place the officer of the watch holds, which is the notes' "the mate can be sent off in the boat while he holds
  the deck".
- The belay line describes a ship's manoeuvre ("the helm and the yards left as they stand", `runner.py:462-465`) for a boat.

### Route 2: no belay by anyone (session 4, St Mary's)

`_belay_held_work` (`scripts.py:3923-3936`) belays **every** waiting or paused evolution on the runner, whatever it is, and is
called when the anchoring evolution clews up (`:4046`), when it finishes furling (`:4117`) and when getting under way looses
the topsails (`:4663`). Its docstring speaks of sail work only. It writes no log line; the list `Runner.belay` returns is
dropped.

```
548129 | evolution.started | sim | All hands, bring ship to anchor! Stand by to take in the light sails.
548996 | evolution.step | sim | Brought up. Stations for furling sail; square the yards.
549185 | order.rejected | the officer of the watch | ... ('sell 16 tons of brandy'): The prices at St Mary's are not known; send the boat ashore first ...
549186 | order.accepted | the officer of the watch | By the officer of the watch: sending the boat ashore.
549187 | evolution.waiting | sim | Not hands enough on deck to send boat; the hands are coming to anchor.
549749 | ship.brought_up | sim | Brought up by the best bower ...          (the furl step ends; line 4117 runs)
550494 | order.rejected | captain | ... ('send the boat ashore'): The long-boat is away already.
553622 | order.rejected | captain | ... ('belay send the boat ashore'): Nothing in hand or waiting answers to 'send the boat ashore' ...
553637 | order.rejected | captain | ... ('belay hoist out the boat'): Nothing in hand or waiting answers to 'hoist out the boat' ...
```

The captain's reading at 553,567 was right ("I don't see it in the 'in hand' tasks"). The list never came off, the brandy was
not sold at St Mary's, and `get under way` was closed to them (they used `weigh`).

### Route 3, by reading only

`LayOutKedgeScript` marks the boat away in `begin` (`scripts.py:5117-5126`) and resets it only at its end (`:5196-5200`); its
own `fail("no bottom to let the kedge go in")` (`:5157`) or a belay leaves the boat away, "pulling out with the kedge".

### Fix

1. A hook on `Script` (say `abandoned(reason)`) called from `Runner.belay` and `Runner._fail`; `SendBoatScript` and
   `LayOutKedgeScript` use it to put the boat back at the booms, bring the people back aboard, and either refund a purchase or
   keep the bargain as goods lying at the quay for the next boat. A boat already clear of the side is out of hail, so a belay
   after "away" should be refused in words or read as a recall with its time.
2. `_belay_held_work` limited to work on sails and yards.
3. `Ports.send_boat`: check the boat first, move the person after `_send_boat` returns; and set `away` when the evolution
   begins, as the kedge's script does.
4. A self-heal for old saves: `boat.away` with no evolution holding "the boat" is reset with a log line.
5. `belay <the order>` should find port and ground-tackle work: `work._evolution_ids` (`orders/work.py:235-253`) knows only
   the sail verbs and three navigation ones, so `belay send the boat ashore` and `belay get under way` name nothing even when
   the work is in hand (session 8 tick 121,801: refused with "getting under way (waiting its turn)" in the same sentence). The
   module's own docstring promises "the order that gave it" (`work.py:4-6`).

Size **M** (`evolutions/runner.py`, `scripts.py`, `world/ports.py`, `orders/work.py`, tests). Risks: item 2 changes what the
end of an anchoring leaves waiting; if a pinned passage has a lead cast or a trim waiting at that moment its log moves, so the
5b and 5c digests need re-measuring. Item 4 changes a replay only of a journal that already has a stuck boat. No consent-brief
text is touched.

---

## D. Number words above twelve

**Verdict: CONFIRMED, and wider than reported.** There is no one reader. Five tables, five word lists:

| Reader | Where | Serves | Words it takes | Example that fails |
|---|---|---|---|---|
| The grammar's `numbers` | `data/vocabulary.yaml:1113-1129`, read by `grammar._count_at` (`orders/grammar.py:590-618`) | reefs, points, fathoms of a line, degrees; and the whole standing dialect (durations, intervals, every comparison: `standing/grammar.py:323`, `552-555`) | a, an, one to twelve, **sixteen**, half; "N and a half" | `every fifteen minutes`: "'fifteen minutes' is not an interval the ship keeps; say minutes, a glass, half an hour, an hour or a watch." `the true wind exceeds thirty knots`: "'the true wind exceeds' what number?" `come up thirteen points`: "... but not 'thirteen points'; did you mean 'three'?" `ease the main sheet twenty fathoms`: "There is no such part as the main sheet twenty in this ship" |
| The port's | `orders/port.py:37-78` (`number_in`) | tons, days of provisions, hands, fathoms of cordage | a, an, one to twelve, fifteen, twenty, "twenty five", thirty, forty, fifty, sixty, seventy, eighty, ninety, (a) hundred, two hundred, three hundred | `buy sixteen tons of brandy`: "How many tons? Say 'buy twenty tons of tin'." (session 4 tick 212,160; `:99-102`) |
| The ground tackle's | `orders/ground_tackle.py:77-114` (`_fathoms`) | cable: `veer`, `veer to`, `come to an anchor in`, the kedge's hawser | ten, twelve, fifteen, twenty, "twenty five", thirty, forty, "forty five", fifty, sixty, seventy, "seventy five", eighty, ninety, (a) hundred, "a hundred and twenty". **Not one to nine, not eleven** | `veer five fathoms`: "'five fathoms' is not a number of fathoms I can read." `veer to ninety-four fathoms`: "'four fathoms' is not a number of fathoms I can read." |
| The set's | `orders/navigation.py:58-90` | `allow <n> knots of set` | no, half, a quarter, a, one, two, three, four | `allow five knots of set to the east` |
| The canvas numbers | `orders/grammar.py:281-291` | `bend the No. 1 ...` | one to nine | by design |

Digits work everywhere. Not read by any table: thirteen, fourteen, seventeen, eighteen, nineteen; any compound but the three
above (after normalisation a hyphen is a space, so "twenty-five" tons works and "thirty-five" does not); "a dozen", "a score";
"half" outside the grammar's own list. Courses are digits or compass points (`grammar.py:791-808`).

Three things make it worse than a refusal:

- **The log writes what the readers cannot read.** `world/reckoning.py:319-329` (`number_words`) and `scripts.py:3845-3848`
  write "Veered to a hundred and eighty-five fathoms" (session 4 tick 548,756), "eighty fathoms of cable veered", "fifty-one
  fathoms on each". Echoed back: `veer to a hundred and eighty-five fathoms` gives "'five fathoms' is not a number of fathoms
  I can read."; `veer to fifty-one fathoms` gives "'one fathoms' is not ...".
- **The refusals name the wrong fault.** "How many tons?" when the tons were said; "what number?"; "did you mean 'three'?";
  "is not an interval ... say minutes" when minutes were said. A compound at the port turns into a good that does not exist:
  `buy thirty five tons of tin` is read as 30 tons of "five tin" and refused as "the market has no five tin".
- **Some misreads are silent.** For water and provisions the words left over are thrown away (`port.py:156-177`):
  `take in provisions for sixteen days` finds no number and takes the default thirty; `take in provisions for thirty five days`
  takes thirty. Each is charged and logged as if asked for. `take in sixteen tons of water` finds no number either: with her
  water short it completes her to the allowance; with it complete (always, in m5c, since nothing is expended) it answers "Her
  water is complete ... Say 'take in twenty tons of water' to stow more", the very form just used.

The officer's own note at tick 212,166 has it right: "'buy sixteen tons' is refused ... 'Twenty' and 'forty' were fine". The
grammar's list does have sixteen (for sixteen points); the port's does not.

**Fix.** One reader for all five places: units, teens, tens, compounds with a hyphen, a space or "and", "a hundred and
fifty-two", halves and quarters, "a dozen", "a score"; returning the value and the words used. Callers: `grammar._count_at`
and `_modifier_words` (so that a number word ends the noun), `port.number_in`, `ground_tackle._fathoms`, `navigation._knots`,
`standing.parse_duration` and `_number`. And refusals that quote the word not read. Size **M** (one small module, five call
sites, tests). Risk: low. Parsing only; nothing accepted today changes meaning except the silent misreads above. No effect on
replay or the pinned passages unless a pinned book holds an order refused today for its number.

---

## E. The water sail and the occasional sails

**Verdict: CONFIRMED for the mechanisms; one sentence of the claim is too strong.**

The water sail is `water_sail` in `data/ships/topsail-schooner.yaml:289-298`: class `studding`, boom `main.boom`,
`bent: false` (it starts in the sail room). Group `occasional sails: [ringtail, water_sail]` (`:755-757`). No alias for it.

**How it was set.** `bend the water sail` (captain, tick 75,003; "Bent the water sail (No. 7 canvas, new) and furled it",
75,942), then `set the water sail` (officer, 76,374; "Set the water sail.", 76,587). `set` has no competing phrase, so it
parses. The second time (462,176) `set the water sail` alone, the sail being bent already.

**1. "`Take in the water sail` is read as taking on water from the yard": CONFIRMED.** The verb is the longest phrase at the
start of the line (`grammar._match_verb`, `orders/grammar.py:412-419`; phrases sorted by word count, `orders/vocabulary.py:208`).
`take in water` has the synonym `take in the water` (`data/vocabulary.yaml:743-747`), four words, which beats the sail verb's
`take in the` (`:31`), three. Parse check: `take in the water sail` gives verb `take in water`, object `sail`; so does
`take in water sail`. `port.execute` then finds no number in "sail" and asks the yard for water (`orders/port.py:156-171`),
which answers "She is not in port; there is no yard to demand it of." (`ports.py:1196`; captain, ticks 140,875 and 140,904).
The same parse has two other faces:

- For the officer the order never reached the grammar's refusal. The authority gate read it as port business:
  `140862 | agent.refused | The officer of the watch may not take in the water sail without the captain: the port's business
  is the captain's.`
- In port with her water short it would be carried out as watering, and paid for. Stores are not consumed in m5c, so in
  practice it would answer "Her water is complete" (`port.py:164-168`).

**2. "`Furl` is refused because the game counts it as a studding sail": CONFIRMED, as designed.** `furl` has an evolution for
square sails only (`data/vocabulary.yaml:913-914`); any other class gets `refusals.furl` (`:994`) through
`verbs._sail_check` (`orders/verbs.py:407-409`): "A studding sail is not furled on its spar; take it in instead." (officer,
tick 140,866). Also "A jibheaded sail is not furled ..." for `furl the flying jib` and `furl the main gaff topsail` (ticks
201,077 and 201,078). The advice is the trap: for this sail "take it in" is the one form that cannot work.

**3. "`Watersail` isn't recognised": CONFIRMED.** Names are generated from the id's words (`orders/resolve.py:284-312`), so
only "water sail" (and "water-sail", the hyphen being a space). "There is no such part as the watersail in this ship.
('take in' was understood.)", three times (140,879, 140,907, 140,922), with no "did you mean". The missing hint is a small bug
of its own: a part whose id is one segment (`water_sail`, `ringtail`, `jib`, `flying_jib`, `storm_jib`, `square_sail`) is
entered first under its raw id with `suggest=False`, and the plain name, having the same key, never joins the suggestion list
(`NounTable.add`, `resolve.py:81-104`; checked: "water sail" is in the table and not among `names` on all four ships).

**4. "The water sail can't be taken in by name; only `take in the occasional sails` works": PARTLY.** By parse check these
reach the right verb with the water sail as object: `haul down the water sail`, `douse the water sail`, `hand the water sail`
(`take_in_words`, `data/vocabulary.yaml:1013`: studding takes "take in, haul down"), and `take in the ringtail and the water
sail` (the water sail second). Nobody found them, and the refusals pointed the other way: `lower`, `clew up` or `brail up the
water sail` answer "a studding sail is taken in, not lowered; say 'take in the water sail' or 'take in the water sail'"
(`verbs._take_in_word_check`, `orders/verbs.py:466-480`; the advice repeats itself when the proper word is "take in"). So
three different refusals all recommend the one order that is misread.

**The same trap elsewhere.** I parsed every sail verb phrase (58) against every sail noun, group and alias of the four ship
files. The only collision is `take in [the] water sail` on the schooner. Around it:

| Ship | Occasional sails | `furl` refused for | Other name gaps |
|---|---|---|---|
| topsail schooner (Speedwell) | ringtail, water sail (both in the sail room; the ringtail wants its boom rigged out) | 12 of 14 sails (every gaff, jib-headed and studding sail) | `watersail`, `ring tail` |
| frigate-36 (Amazon; the merchant ship of session 8) | ringtail, two fore save-alls | 21 of 32 | `saveall`, `ring tail`; `save-all` and `save-alls` work |
| brig (Harpy) | none; ten studding sails | 20 of 28 | `take in the occasional sails` refused, there being no such group |
| cutter (Sherbourne) | none; the square sail ("the crossjack") and the topgallant | 6 of 9 | `squaresail`; `lower the square sail` refused ("a course is hauled up, not lowered") though her square-sail yard is hoisted from the deck; no `occasional sails` group |

No ship file has bonnets. Studding sails by name parse on all three ships that carry them.

**Fix, all S and independent.**

- The verb: drop the synonyms `take in the water` and `take in the provisions` (the fallback `_stores_order`,
  `orders/__init__.py:96-102` and `149-163`, already carries `take in twenty tons of water`), or, better, in `grammar.parse`
  prefer a sail verb whenever the words after its phrase are a noun of this ship. This also cures the officer's "port's
  business" refusal.
- The noun: an alias `watersail` (and `ring tail`, `saveall`, `squaresail`). The ship files are generated, so in
  `tools/gen_ships.py`.
- `furl`: map the other classes to their take-in evolutions (four lines in `vocabulary.yaml`, `evolutions.furl`; taking in
  ends with the sail made up), or keep the refusal and have it name a word that works for this sail.
- `_take_in_word_check`: one remedy, not the same one twice.
- `NounTable.add`: let the plain name be suggested.

Risk: none to replay; a pinned book would move only if it holds a `furl` refused today. The library's grammar topic should say
what `furl` now takes.

---

## F. "Full and by", for the captain

**WORKS AS DESIGNED.** `full and by` is a synonym of the verb `keep her full` (`data/vocabulary.yaml:172-182`, object none,
level 1). The helm goes to `HelmMode.FULL_AND_BY` and the line is "Helm ordered: keep her full and by."
(`orders/verbs.py:1963-1970`; session 4 tick 54,257 for `Keep her full`, 397,814 for `Keep her full and by`). It is refused
only when she is hove to or heaving to ("She is hove to; fill away before giving her a course.", `:1949-1961`), at anchor or
aground.

Other words that reach the same order: `keep her full`, `keep her full and by`, `sail her full and by`, `steer full and by`,
`bring her by the wind`, `steer by the wind`, `keep her by the wind`, `by the wind`, `bring her to the wind`, `haul her wind`,
`haul the wind`, `keep her a good full`, `a good full and by`, `nothing off`, `no higher`, `luff and touch her`.

**Not taken** (parse check): `close hauled` and `close-hauled` ("... is not an order this ship understands; did you mean
'box haul'?"), `steer close hauled` ("'steer' was understood, but not 'hauled'; did you mean 'haul'?"),
`bring her close hauled`, `sail close hauled`, `sail by the wind`, `keep her close to the wind`. The game's own refusal uses
the word: "She is not close-hauled; bring her by the wind before going about." Adding them as synonyms is **S**.

For the other reader: the name mismatch the model reports is the canonical verb showing through. `You may full and by`
(session 4 tick 43,096) is logged "The officer of the watch may keep her full", because `stations._verb_in`
(`orders/stations.py:354-369`) returns the canonical name and not the phrase said; and the refusal before it reads "may not
full and by without the captain".

---

## G. `what is she`, `make her out`, `the strangers`

**CONFIRMED working.**

- `what is she` and `make her out` are one order (`data/vocabulary.yaml:705-711`; `orders/navigation.py:387-391`;
  `Lookout.make_out`, `world/lookout.py:525-558`): a glass sent aloft at the nearest sail, or the one named
  (`make out the brig`), answered at once with what the distance allows. Session 4 tick 42,626: "The glass aloft makes out the
  cutter abeam to starboard: the Plymouth pilot's cutter, standing to the south-eastward (SE by S), under plain sail; British
  colours, the red ensign." Tick 83,160: "The glass aloft makes out nothing more of the sail abeam to starboard: her hull is
  below the horizon, distant two leagues." With nothing in sight: "No sail in sight to make out."
- `the strangers` (also `what sail is in sight`) is a reading (`world/lookout.py:560-599`; `api/readings.py:2023`): every sail
  in sight, nearest first, with her bearing, her distance by estimation, what has been made out of her, her course, and her
  colours once made out. Never her position.
- One neighbour fails: `where is she` (captain, tick 42,638, twelve seconds after `what is she`) is the people's `where is`
  and answers "Nobody aboard answers to 'she'; 'the people' lists them." `who is she` and `what ship is that` are not orders.

---

## H. The refusals

Every `order.rejected` line of sessions 2, 4, 5, 6, 7 and 8, split by who raised it:

| Session | Captain | Officer | A standing order firing | All | Refused share of a person's orders |
|---|---|---|---|---|---|
| 2 Harpy, Opus | 55 | 28 | 12 | 95 | 12% (officer alone 10%) |
| 4 Speedwell, Opus | 46 | 27 | 100 | 173 | 11% (11%) |
| 5 cutter, Gemma | 16 | 24 | 9 | 49 | 23% (officer 24 refused, 36 accepted: 40%) |
| 6 cutter, Qwen (Ollama) | 4 | 0 | 0 | 4 | 7% |
| 7 cutter, Qwen (llama.cpp) | 9 | 4 | 145 | 158 | 11% (15%) |
| 8 merchant ship, Opus | 1 | 9 | 56 | 66 | 5% (8%) |
| **All six** | **131** | **92** | **322** | **545** | |

The share is refusals over refusals plus `order.accepted` lines for the same actors; the captain's accepted lines include his
words to the officer, so his own share is understated. The authority gate's refusals are a different kind (`agent.refused`:
19, 6, 4, 1, 4, 5 by session) and another reader's.

### H.1 Refusals raised by standing orders: 322 of 545 (59%)

| Order fired | Refusal | Count | Sessions | Reading |
|---|---|---|---|---|
| `take a bearing of the land` by "every 10 minutes then ..." or "every glass then ..." | "Nothing is in sight to take a bearing of." (161); "The land is not in sight; in sight: Sail ho! ..." (30) | 191 | 7 (145 of 159 firings), 8 (46 of 54) | Each refusal right; the class is noise. |
| `take in the occasional sails`, `take in the studdingsails`, `take in the royals`, `set plain sail` and the like, the work already done | "Nothing done: the ringtail is already furled; the water sail is already furled." | 113 | 4 (99: 'light sails' 90 of its 91 firings, 'studding' 9), 2 (11), 8 (3) | A satisfied order logged as a refusal. |
| `trim the sheets`, `bear away one point`, `heave to` | "She is at anchor; '...' must wait till she weighs." / "She is hove to; ..." | 10 | 5 (9), 2 (1) | Right, noise. |
| `trim sails` | "There is no wind to trim to." | 8 | 8 (7), 4 (1) | Right, noise. |

The extra fact checks out: in session 4 between ticks 486,001 and 521,401, 64 of the 66 `order.rejected` lines are "Nothing
done" from 'light sails' (56) and 'studding' (8).

**Mechanism.** A firing is an ordinary `World.submit` (`standing/runtime.py:361-368`), and `submit` records every `OrderError`
as `order.rejected` (`core/world.py:999-1009`), with no memory of the last one. The runtime already has the right habit for
the neighbouring case: a failing `, if` is said the first time and then once a watch, as a routine `standing.held` line
(`runtime.py:327-344`; session 4 tick 478,801, "Standing order 'light sails' every 10 minutes: not carried out; the mean wind
is 8 knots, not above 10 knots."). The players wrote `every N minutes, if ... then ...` because they wanted a condition
*kept* (the owner's note 16); once the condition holds and the work is done, every firing is a refusal.

**What a satisfied standing order should log.**

- Work already done ("already furled", "already set", "at anchor already"): not a refusal. One routine `standing.held` line,
  "Standing order 'light sails' every 10 minutes: nothing to do; the ringtail and the water sail are furled already", the
  first time and then once a watch while the answer is the same; or nothing at all. It should not count as a firing.
- Cannot be done now (at anchor, hove to, no wind, nothing in sight): the same once-a-watch `standing.held ... not carried
  out; <reason>`.
- A real refusal (the order no longer reads on this ship, a part gone): keep `order.rejected`, once, notable.

Touches `standing/runtime.py` (`_fire`), two fields on `Rule` (`standing/rules.py`, kept in a save), `core/world.py`
(`submit`), tests. Size **S to M**. Risk: this one does move pinned logs. The merchant passage's own book fires
`trim the sheets` and `come to an anchor` into refusals (92 such lines in session 1, the same scenario and seed), so
`GATE_5C_MERCHANT_LINES` and `GATE_5C_MERCHANT_DIGEST` (`tests/test_known_truths.py:3732-3733`) and probably the cruise's
(`:3707`) need re-measuring. Old saves replay to a different log from that point. A new field on `Rule` (or on `BoatState`,
section C) needs a plain default: a checkpoint is a pickle of the object graph (`core/replay.py:13-28`) and an old one will
not carry it.

### H.2 Standing-order grammar, typed by a person (21 refusals)

| As typed | Refusal | Count, sessions | Classification |
|---|---|---|---|
| `standing order "light sails" by the mate: every 10 minutes if the mean wind above 10 knots then ...`; also `... above 10`, `... the mean wind speed above 10 knots`, `... the wind above 10 knots`, `... the wind over 10 knots` | "'the mean wind' cannot be 'above 10 knots'; a wind is compared in knots or points." | 5, session 4 (478,078 to 478,091, officer) | **Words mislead; phrase the grammar should take.** It *was* compared in knots; the copula is missing. Every numeric comparison but `exceeds` needs "is" or "are" (`standing/grammar.py:558-580`, `983-1073`; the catch-all `refuse()` at `667-674`). Should take `above 10 knots`, or say "say 'is above 10 knots' or 'exceeds 10 knots'". |
| `... if the mean wind is 11 knots then ...` | "'the mean wind' cannot be '11 knots'; a wind is compared in knots or points." | 1, session 4 (478,159, captain) | **Words mislead.** There is no equality; say so, and offer `is over` / `is under`. (The seventh try, `is above 10 knots`, was taken at 478,201.) |
| `standing order "stuns'l": ...`, `"pilot's lead": ...`, `"stuns'l breeze": ...` | "After the name say a colon and then when, at or every: standing order "stuns": when the true wind exceeds 30 knots ..." | 3: session 4 (478,815), session 2 (14,581; 527,749), officer | **Bug.** `_quoted_name` closes the name at the first of *any* quote character, the apostrophe among them (`standing/grammar.py:91`, `129-133`). The colon is there; the echoed name is cut short. Fix: close on the mark that opened. |
| `standing order "Bearings, Close In": ...` again; `"trim on a shift" ...` again | "There is a standing order '...' in the book already; belay it, or give the new one another name." | 2: session 7 (10,514), session 8 (68,409) | **Words mislead.** A belayed order stays in the book and keeps its name (`standing/book.py:99-103`); the word wanted is "strike it". |
| `standing order "Pilot hails": at the pilot hail then ...` | "'at the pilot hail' names no event the ship knows; did you mean the pilot's hail, ...?" | 1, session 4 (190,249) | **Phrase to take.** Events are matched exactly (`standing/grammar.py:230`); `at the pilots hail` fails too. |
| `... every 2 minutes when the distance to the land is under 3 miles then ...` | "'2 minutes when the distance to the land is under 3 miles' is not an interval the ship keeps; say minutes, ..." | 1, session 7 (11,035) | **Words mislead.** Wants `, if`; say so, as the "begins with 'if'" refusal does. |
| `... if the land is in sight and the land is within 3 miles ...`; `... when the pilot asks off then heave to` | "'the land' cannot be 'within 3 miles'; the land is compared as in sight or not in sight." / "'the pilot' cannot be 'asks off'; the ground is compared by what the lead brings up" | 2: session 6 (11,611), session 2 (16,587) | First right, and could offer `the distance to the land is under 3 miles`. Second: **words mislead** (it talks of the ground). |
| The starter book read on the cutter: `... then take in the studdingsails; take in the royals` and four more | "In standing order 'night routine', 'take in the studdingsails' is refused: There is no such part as the studdingsails in this ship ..." | 5, session 5 (tick 1) | Right each; **design gap.** A group evolution passes over what the rig has not (`orders/__init__.py:211-215`); a standing order's orders do not, so the starter book is a frigate's. |
| `standing order "...": if the pilot asks off then ...` | "A standing order begins with when, at or every, not 'if' ..." | 1, session 2 (16,630) | Right, good words. |

**How forgiving is the grammar of a dropped apostrophe or copula?**

- *Apostrophes.* Verb phrases: forgiving (`vocabulary.key` strips them, `orders/vocabulary.py:117-119`; `_match_verb` strips
  them from what was said). Ship nouns: forgiving. Not forgiving: the journal sentence (`show the officers journal`, session 2
  tick 51,741; the next row); a standing order's quoted name (an apostrophe ends it); event names (`at the pilots hail`); a
  mark's name in `take a bearing of` (`st marys`, session 4 tick 545,523: "St marys is not in sight; did you mean St Mary's or
  St Martin's?"; `mark_in_sight` splits the name at the apostrophe, `orders/navigation.py:473-476`); `ill take the deck`.
- *The copula.* Not forgiving anywhere in a condition: `the depth under 20 fathoms`, `she hove to`, `the wind over 10 knots`
  are all refused; only `exceeds`, `backs`, `veers`, `shifts` and `gets up` stand without "is". No "at least", "or more",
  "within", or equality.

### H.3 Orders typed by a person: the most frequent and the most telling (223 in all)

| As typed (examples) | Refusal | Count, sessions | Classification, nearest accepted form |
|---|---|---|---|
| `Set the jib`, `set the foresail`, `heave to` when hove to, `Fill away` when not, `Trim sails` in a calm, `haul the fore staysail sheet starboard`, `belay that` with no work | "The jib is already set." / "She is hove to already; ..." / "There is no wind to trim to." / "... already hard in." | 42: 2 (12), 4 (10), 5 (17), 6 (1), 8 (2) | Right. |
| `steer SE by S`, `Bear off half a point`, `shape a course for plymouth` while hove to | "She is hove to; fill away before giving her a course." | 12: 2 (8), 4 (2), 6 (1), 8 (1); nine the officer's | Right, clear. The commonest single refusal of an officer's order; worth `fill away and steer <course>` in one. |
| `take a bearing of the lavandiere` (×4), `... lavandiére`, `... st marys`, `... the pilot gig` (for "the St Mary's pilots' gig") | "The lavandiere is not in sight; did you mean the Lavandière? In sight: the Lavandière bearing ..." | 7 of the 13 name misses: 2 (2), 4 (4), 8 (1) | **Phrase to take.** Fold accents, apostrophes and a possessive plural in `mark_in_sight` (`orders/navigation.py:473-508`); a captain at an English keyboard cannot type the grave accent. The other six are misspellings, rightly refused with the name offered. |
| `take a bearing of the lugo rock`, `... the governor`, `... the old wall`, `... the light` | "The Lugo rock is not in sight (a danger of the chart); the Black Rock, in sight, is another feature; in sight: ..." | 6: 2 (3), 4 (3) | Right, good words. |
| `set the foresail sheet`, `set the fore staysail sheet starboard`, `Loose the lee bowlines` | "You set sails; the starboard fore staysail sheet is a sheet (a line). Did you mean the fore staysail?" | 10: 5 (9, Gemma in three bursts), 2 (1) | Right. It could name the verb that does work a sheet (`haul`, `ease`, `trim the fore staysail`). |
| `You may shape a course` (×2), `You may hail the pilot`, `You may bring her up`, `You may show the officer's journal` | "'shape a course' names no order the officer of the watch could be allowed; say the order's words first ..." | 10: 2 (7), 4 (2), 6 (1) | **Words mislead** for `shape a course`: the allowance wants the vocabulary's exact phrase, `shape a course for` (`stations._verb_in`, `orders/stations.py:354-369`). An alias cures it. |
| `hail the pilot` | "'hail the pilot' is not an order this ship understands; did you mean 'haul'?" | 1 and two `You may ...`, session 2 | **Design gap** (the owner's note 9). No order; the pilot comes of himself. |
| `bring her up` | "... is not an order this ship understands." | 2: 2 (574,313), 4 (143 as an allowance) | **Phrase to take**: `bring up`, `come to an anchor`. The log's own word is "Brought up". |
| `The deck is yours`; `Mr pearce you have the deck`; `You have the deck mr pearce` | "... did you mean 'i have the deck', 'you have the deck' ...?" / "... did you mean 'moor'?" / "'you have the deck' is said to an agent's station, and names one: ask the watcher ..." | 3, session 2 (573,870; 216,829; 216,825) | **Phrase to take, and words mislead.** `_GIVE_DECK` needs the name first and a comma (`orders/stations.py:69`). Accepted: `Mr Pearce, you have the deck`. |
| `show the officers journal` | "'show the officers journal' is said to an agent's station, and names one: ask the watcher how the sails are drawing; ..." | 1, session 2 (51,741); `show the officer of the watchs journal` was taken at 51,753 | **Bug.** The vocabulary's own key for the phrase is exactly these words (`data/vocabulary.yaml:853-856`), but `_JOURNAL` strips only "'s" or " s" (`orders/stations.py:89-92`), so the station read is "officers" and matches none; the long form passes because the alias "officer" matches by prefix (`:104-114`). `show the watchers journal` fails the same way; `show the officer journal` works. |
| `Tell the watcher ...`, `Ask the watcher ...` with an officer seated | "There is no watcher at the station; nobody has been stationed there." | 4: 2 (2), 4 (1), 7 (1) | Right. It could add "the officer of the watch is at his station: say 'tell the officer'". |
| `Wear to north`, `Wear north` | "'wear ship' was understood, but a heading belongs with 'steer'." | 2, session 2 | **Phrase to take.** `wear ship`, then `steer north`. |
| `Steady on SE by S`, `Steady on` | "'steady' was understood, but not 'on'; did you mean 'one'?" | 2, session 7 | **Phrase to take.** `steer SE by S`. |
| `brace the fore yards up sharp` | "'brace' was understood, but not 'sharp'; did you mean 'trim sails head yards sharper'?" | 1, session 4 | **Phrase to take.** `... sharp up`. |
| `rig in the studdingsail booms`, `rig out the starboard studdingsail booms` | "There is no such part as the studdingsail booms in this ship; did you mean the studdingsails, the fore lower studdingsail boom ...?" | 2: 2 (573,882), 8 (79,252) | **Phrase to take.** `rig out the stuns'ls`. No group of the booms. |
| `shake out the reefs` | "There is no such part as the reefs in this ship. ('shake out' was understood.)" | 1, session 8 | **Phrase to take; words mislead.** `shake out the reefs in the topsails`. |
| `Let fly the headsail sheets`; `Back the fore staysail` | "There is no such part as the headsail sheets ..." / "The fore staysail is a jibheaded sail; it has no yard to brace. Trim it with its sheet." | 2, session 4 | **Phrase to take.** `let fly the jib sheet` (one sail at a time); `haul the fore staysail sheet to windward`, which the refusal could name. |
| `clear away the bowers`, `clear away the best bower` | "There is no such part as the best bower in this ship. ('let go' was understood.)" | 2, session 4 (officer) | **Words mislead.** `clear away` is the line verb's synonym; the anchor has no "clear away" state. |
| `lay out the stream anchor astern` | "There is no such part as the out in this ship; did you mean the spanker outhaul, ...? ('brace' was understood.)" | 1, session 2 (aground) | **Words mislead.** `lay` is a synonym of `brace`. Nearest: `lay out a kedge to the SW` (a compass bearing only; "astern" is refused too). |
| `heave in the best bower cable to 160 fathoms`, `heave in 70 fathoms of cable` | "'heave short' takes nothing after it; 'the best bower cable to' was not understood." | 2, session 4 (officer) | **Phrase to take.** Nothing shortens the scope to a figure; `heave short` and `veer to N` only. |
| `Veer the cable, small bower` | "Veer how much? Say 'veer twenty fathoms', ..." | 1, session 2 | **Words mislead.** He said which cable; no form names the cable to veer on. |
| `Furl sails` at anchor | "She is at anchor; 'furl sails' must wait till she weighs." | 1, session 2 (526,581); `Furl the square sails` was then taken | **Bug.** See below. |
| `furl the water sail`, `furl the flying jib`, `furl the main gaff topsail`; `take in the watersail` (×3); `take in the water sail` (×2) | Section E | 8, session 4 | Section E. |
| `buy sixteen tons of brandy` | "How many tons? Say 'buy twenty tons of tin'." | 1, session 4 | Section D. |
| `send the boat ashore with the purser` (×2); `send the boat ashore` (×2); `buy ...` with the boat away (×3) | Sections B and C | 7: 2 (4), 4 (3) | Sections B and C. |
| `belay get under way`; `Cancel standing orders` | "Nothing in hand or waiting answers to 'get under way': ... The work in hand: ... getting under way (waiting its turn)." | 2: 8 (121,801), 7 (10,528) | **Bug / phrase to take.** Section C item 5; and `cancel standing orders` is read as belaying work, where `belay all standing orders` was meant. |
| `where is she` | "Nobody aboard answers to 'she'; 'the people' lists them." | 1, session 4 | **Phrase to take.** `the strangers`, or `the reckoning`. |
| `as you were`; `pipe down the watch below`; `turn north by east`; `Swifter in the weather catharpins` | "... is not an order this ship understands ..." | 4: 2 (3), 5 (1) | **Phrases to take.** `belay that`; `pipe down` or `send the watch below`; `steer north by east`; `swifter in the catharpins`. |
| `man the pumps`, `sound the well`, `hoist our colours`, `send a lookout to the mizzen yard`, `Go to the tops` | "The ship has no well to sound yet; that reading comes with the world." and unknown-verb refusals | 5: 2 (4), 8 (1) | **Not modelled.** `hoist our colours` reads as setting a sail ("There is no such part as the our colours"); `go` is a console word. |

**`Furl sails` at anchor.** `verbs.execute` sends every verb whose evolution is a single name through `_not_riding`
(`orders/verbs.py:93-99`, `1924-1933`; the comment says "the helm, the trim and the manoeuvres want her under way"). That net
also holds `furl all`, `loose sails to dry`, `square`, `brace`, the topgallant-mast and topmast orders, the catharpins,
`cut away`, `reeve` and `splice` (`data/vocabulary.yaml:922-980`). Checked in memory on the brig with an anchor marked down:
`furl sails`, `loose sails to dry`, `square the yards`, `strike the topmasts`, `send down the topgallant masts`,
`reeve a new main brace` and `clear the wreck` each answer "She is at anchor; '...' must wait till she weighs.", while
`furl the square sails` passes. Marked **aground**, `clear the wreck`, `reeve a new main brace`, `strike the topmasts` and
`furl sails` answer "She is aground; '...' must wait till she floats." So the harbour's own routine is closed at anchor, and a
ship ashore may not lighten or clear herself. No test pins either sentence. Fix: gate the helm, `trim` and the manoeuvres
only. **S.**

Unknown-verb and unknown-noun refusals come to 36 in all. Eleven are slips of the keyboard or words that were never orders
(`heaev to`, `Tell the offier ...`, `bely that`, `stnading order`, `Stead`, `tools`, `150`), rightly refused and mostly with
the right word offered; the other 25 are the sailor's phrases in the table.

---

## I. The ship's papers

**Verdict: CONFIRMED working, with three things the documents say that the code does not do.**

Eight papers (`data/papers/papers.yaml:22-62`), served by handle to every station and the browser alike
(`agents/tools.py:1330-1372`):

| Paper | Keeper, place | Page made from | "Last written" moves when |
|---|---|---|---|
| the sailmaker's account | sailmaker, sail room | the sail room, live | the yard delivers a suit of sails |
| the manifest | purser (the mate in a merchantman), hold | the hold and the purse, live | a bargain is made (`ports.py:1168-1175`) |
| the purser's books | purser, hold | water and provisions, live | the yard delivers water or provisions |
| the boatswain's store book | boatswain, deck | spare cordage, live | the yard delivers cordage |
| the booms' list | boatswain, deck | spare spars, live | the yard delivers a spar |
| the establishment of ground tackle | boatswain, deck | the anchors and cables, live | never |
| the epitome's table of the establishments | master, cabin | the tide table, static | never |
| the price list | purser, cabin | the lists brought off, a true snapshot | the boat brings a list off (`ports.py:1073-1078`) |

- **Every page is made from its store when it is read** (`Papers._lines`, `world/places.py:393-450`), so the content is always
  current. Only the price list is a real record of a past moment.
- **Documents against code.** The file's head, the module and the primer say "a paper is only as current as its last entry"
  (`papers.yaml:6-8`, `places.py:18-19`, `docs/primer/14-the-port.md:39`). The only thing that ages is the date. Only three
  call sites ever write one (`ports.py:1075`, `1170`, `1371`), so a sail bent from the sail room, a line rove from the
  boatswain's store, a spar shifted or an anchor lost changes the page and leaves it dated at the muster.
- **The manifest and a purchase.** It is written up at the bargain, the purse already paid, while the goods reach the hold when
  the boat is back (`ports.py:1137`, `1168-1175`, `1642-1654`). For the hours between, the page shows the money gone and no
  cargo. With a stuck boat (section C) it stays so.
- **The keeper's name is right:** the mate where there is no purser (`places.py:347-353`; "The price list written up by the
  mate", session 4).

**What the playtests asked of the papers** (query lines in the logs; the models' `library` calls in the transcripts):

- Answered: `the prices` (7 times), `the manifest` (6), `the purse` (5), `the stores`, `the epitome`, `the boats`, the
  boatswain's store; `library(topic='papers')` whole or by handle in sessions 2, 3 and 8.
- **Not answered: the ship's draught.** Session 4 tick 527,027, `library(find='draught', topic='papers')` then
  `library(find='draws')`, working out whether she could cross into St Mary's Road; session 8 tick 544,
  `library(find='draught')`. No paper and no reading holds it ("draught" does not occur in `agents/tools.py` or
  `api/readings.py`), though the ports' rules turn on it (`deep_draught_ft` in the port files; primer 14: "a ship drawing
  more than nine feet lies in the Road") and so does grounding. The schooner's is 10.9 ft (`topsail-schooner.yaml:23-24`); the
  primer gives only the frigate's fifteen. A paper of the ship's particulars (burthen, length, breadth, draught, complement,
  boats, hold) from the ship file is **S**.
- Not answered: `the well` (session 1 tick 30,358; the owner's note 2); `the chandlers` (session 5 tick 1). Nothing lists what
  the yard or the chandlers supply, or the cost and the time, short of a refused `demand`, whose list shows the file's key
  ("... it supplies topmast, topgallant_mast, yard, ...", session 2 tick 637,060).
- Not answered: another port's trade (section A).

---

## Surprises, for the lead

1. **The boat can be killed with no belay at all.** The end of the anchoring evolution silently belays every waiting
   evolution (`scripts.py:3923-3936`, called at `:4117`); a boat sent while she was still furling vanished and left the port
   closed (session 4, tick 549,187 to 549,749).
2. **A refused order moved a person.** `Send the boat ashore with the mate`, refused, put the mate "in the boat"
   (`ports.py:1496-1502`; session 3 ticks 3,058 and 3,237).
3. **Three refusals recommend the one order that cannot work.** `furl`, `lower` and `clew up the water sail` all answer "take
   it in"; `take in the water sail` is watering; the officer's copy of it was refused as "the port's business".
4. **59% of all refusals in the six sessions were standing orders firing**, most of them into work already done. Quieting them
   moves the pinned merchant-passage digest.
5. **The Speedwell never had her starting price list**: `price_lists: [Plymouth]` against the id `plymouth`, skipped in
   silence.
6. **Roscoff's "trade for the Cornish run" has no buyer.** Geneva, rum, tea and tobacco are on no British port's list; ten
   goods in all are dealt in at one port only. From Plymouth, salt beef is the only cargo that pays at Roscoff.
7. **The "in port" rule is not a boat's pull.** It accepts a pull of 10 miles at Brest and refused the Harpy about 4 miles from
   Falmouth's quay.
8. **At anchor, `furl sails`, `loose sails to dry` and `square the yards` are refused; aground, so are clearing a wreck,
   reeving a line and striking the topmasts.**
9. **Numbers: five readers.** The cable's cannot read "five fathoms"; the log writes "a hundred and eighty-five fathoms".
   Provisions for "sixteen days" silently become thirty.
10. **The price-list paper already keeps every port's list**; the owner's note 3 is about the reading and an alias.
11. **No paper or reading gives the ship's draught**, and two Opus sessions went looking for it.

## Where documents and code disagree (collected)

| Document says | Code does |
|---|---|
| `papers.yaml:62`: the price list is "the prices at the last port the boat was ashore in" | prints every port's list (`places.py:440-449`) |
| `papers.yaml:6-8`, `places.py:18-19`, primer 14:39: a paper is only as current as its last entry | every page is made live; only the date is old |
| primer 14:123: the boat goes "at anchor within two miles of the roads" | the same rule; the refusal says "no shore within a boat's pull" |
| `roscoff.yaml:105-107`, primer 14:259: spirits, tea and tobacco "priced for the Cornish run" | no Cornish port deals in geneva, rum, tea or tobacco |
| `orders/work.py:4-6`: `belay` takes "the order that gave it" | port and ground-tackle orders are not found (`work.py:235-253`) |
| `standing/book.py:97-98` and its refusal: "belay it, or give the new one another name" | a belayed order keeps its name; only striking frees it |
| `scripts.py:3924-3928`: the sail work is not taken up at anchor | every waiting evolution is belayed, the boat too |
| `verbs.py:99`: "the helm, the trim and the manoeuvres want her under way" | harbour work and wreck work are gated too |
| `port.py:102`: "How many tons? Say 'buy twenty tons of tin'" | said when the tons were given in a word the table lacks |
| the scenario's line `price_lists: [Plymouth]`, "the list the supercargo brought off the day before" | no list aboard (the id is `plymouth`) |
