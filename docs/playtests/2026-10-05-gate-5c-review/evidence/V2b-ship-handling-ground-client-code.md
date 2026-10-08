# V2b: the ship's handling, the ground tackle, grounding and the leak, and the browser client

Code reader's report, gate m5c. All `path:line` references are to the m5c tree
(`D:\Projects\FreeSail\FreeSail-gate-m5c\`). The m5c-b tree is the same in every file cited
here except `physics/hull.py` and `physics/integrate.py`, where it only changes the
"taken aback" lines; nothing below is fixed or altered by m5c-b.

How this was checked: by reading the code and the session logs. Five throwaway checks were
run with `PYTHONDONTWRITEBYTECODE=1 py -B`, none of them a World and none of them a tick: one
listing of the vocabulary's evolutions, three parse-only calls of `orders.handle` on a ship
object built from a ship file (to get the exact words of refusals), and one piece of plain
arithmetic copying `geo.Position.advanced` (section E). Nothing was written under the project.

## Verdicts at a glance

| | Claim | Verdict |
|---|---|---|
| A | Kedging refused aground; hauling up to a kedge not modelled | CONFIRMED (refusal); PARTLY (the hauling: no order for it, but `heave short` does haul a floating ship to whichever anchor has most cable out). Wider than claimed: 26 verbs, bracing aback and `furl all sail` among them, are refused aground and at anchor |
| B | The well, the carpenter, the pumps | CONFIRMED, all four parts. The leak is a counter with log lines; it stops when she floats and nothing reads it |
| C | With sternway the helm steers as with headway | NOT REPRODUCED from code as stated: the rudder's force and the helmsman both reverse. What the log shows is the helmsman taking the short way round through the wind's eye; and the conning words' log text assumes headway |
| D | The schooner's `get under way` does not cast her | CONFIRMED in code and in the logs: every cast the schooner had to make timed out (3 of 3), two of them in the owner's own scripted passage |
| E | Anchoring in very deep water; no depth/draught check | WORKS AS DESIGNED for the scope (five times the depth up to the cable bent, 240 fathoms on every best bower); no warning and no draught check: CONFIRMED absent. A separate fault found: the depth over the anchor is kept up from the wrong place |
| F | "NaN fm" on the chart | CONFIRMED: `client/units.js` has no `FATHOM` |
| G | The reckoned track thinned | CONFIRMED: capped at 168 points server-side, and a point is added at every cast and bearing, not every hour |
| H | 1x option; anchor facts in the state panel | Size S. The "1x option" is the ease-to-1x checkbox; the anchor facts exist as readings and are not in the snapshot |
| I | Charting tools | Size M, client-side. Nothing of the kind exists today |
| J | The cutter's square sail short in the viewer | CONFIRMED. The drawing follows the file (area over yard length); the file hangs a 27 ft sail from a yard 52 ft above the deck |
| K | Weighing, heaving to, filling away | Six faults found, each with ticks (below) |

The things I did not expect are at the end ("Surprises").

---

## A. Kedging

**Claim.** "Kedging is refused while aground, which is when it's needed most. Hauling her up
to a kedge isn't modelled either."

**Verdict.** CONFIRMED for the refusal. PARTLY for the hauling.

### The kedge orders that exist

- `lay out a kedge [to the <point>] [<n> fathoms]` and its synonyms (`carry out the kedge`,
  `run out a kedge`): `data/vocabulary.yaml:668-672`; `freesail/orders/ground_tackle.py:28-29,
  71, 191-204`; the script `LayOutKedgeScript`, `freesail/evolutions/scripts.py:5060-5215`;
  `data/evolutions/lay_out_kedge.yaml`.
- `let go the kedge` (a synonym of `let go the anchor`: the kedge dropped from the bows where
  she lies, `vocabulary.yaml:604-611`) and `cat and fish the kedge` (`:630-634`).
- There is no order to heave on the kedge by name. `heave short the kedge` is rejected
  ("'heave short' takes nothing after it; 'the kedge' was not understood"; the primer lists
  it as rejected, `docs/primer/13-the-tide-and-the-anchor.md:105`).

### The refusal

`scripts.py:5084-5085`, in `LayOutKedgeScript.check`:

```python
if self.ship.extra.get("aground"):
    return "she is aground"
```

The runner turns a failing check into the order's rejection (`evolutions/runner.py:332-335`).
Session 2, tick 637,001: `Order not carried out ('lay out a kedge to the SW'): she is
aground`. No comment in the code gives a reason. The same guard, the same three words, is in
every anchor script that lets go or weighs: `come to an anchor` (`scripts.py:3979-3980`),
`let go the anchor` (`:4147-4148`), `weigh` (`:4296-4297`), `get under way` (`:4574-4575`),
`moor` (`:4852-4853`), `unmoor` (`:4968-4969`). Not guarded: `heave short`, `veer cable`,
`back the anchor`, `cat and fish`.

### What a grounded captain can and cannot do in m5c

The order layer refuses much more than the anchors. `freesail/orders/verbs.py:93-99`:

```python
if (spec.object in ("heading", "points") or order.verb in HELM_VERBS or order.verb == "trim"
    or (order.verb in vocab.evolutions and isinstance(vocab.evolutions[order.verb], str))):
    _not_riding(ship, order)  # the helm, the trim and the manoeuvres want her under way
```

`_not_riding` (`verbs.py:1924-1933`) refuses with "She is aground; '…' must wait till she
floats." or "She is at anchor; '…' must wait till she weighs." The last clause of the test
catches every verb whose evolution in `vocabulary.yaml:896-991` is a single string, which is
26 verbs, not only the manoeuvres: `brace`, `square`, `back`, `furl all`, `loose sails to
dry`, `send down the topgallant masts`, `send down the topgallant yards`, `strike the
topmasts`, `cut away`, `send down`, `reeve`, `splice`, `swifter in the catharpins` and the
rest, beside `tack ship`, `wear ship`, `heave to`, `fill away`.

Parse-only check, the brig with `extra["aground"]` set:

| Order | Result |
|---|---|
| `brace the main yards aback`, `back the main topsail`, `square the yards` | refused: "She is aground; 'brace' must wait till she floats." |
| `furl all sail` | refused: "She is aground; 'furl all sail' must wait till she floats." |
| `send down the topgallant masts`, `strike the topmasts` | refused |
| `trim sails`, `helm a-lee` | refused |
| `let go the anchor`, `lay out a kedge to the SW` | refused: "she is aground" |
| `take in all sail`, `furl the fore topsail`, `set the jib` (one sail or a group) | pass the guard (session 2, 636,665: `Take in all sail` accepted twelve seconds after the strike) |
| `heave short`, `veer cable` | pass the guard; refused only when no anchor is down |

The same check at anchor refuses `square the yards`, `furl all sail`, `loose sails to dry`,
`strike the topmasts`, `send down the topgallant yards`. Session 2, tick 526,581, at anchor:
`Order not carried out ('Furl sails'): She is at anchor; 'furl sails' must wait till she
weighs.`

So aground she can: take sail in sail by sail or by a group, send the boat, heave short or
veer on an anchor that was down before she struck, and wait. She cannot brace aback, send
down the upper masts, furl all, let go an anchor or lay out a kedge.

**The documents against the code.**

- `freesail/world/ground.py:12-14` quotes Luce for the strike: "the first step is to brace
  aback ... send down the upper yards and top-gallant masts". Both are refused aground.
- `docs/primer/13-the-tide-and-the-anchor.md:42`: "`at aground then furl all sail` is a
  sensible standing order". That order is refused aground by `verbs.py:93-99`.
- `ground.py:26-28`: "Getting off is the tide's business, or the anchor's: a kedge laid out
  by the boat is package 35's (the boat); what the hands can do here is lighten nothing and
  wait for the flood". The package 34 brief says the same (`docs/dev/M5-WorkPackages.md:1320-1322`).
  Package 35 built the kedge and refused it aground.
- `docs/TechnicalSpec-M5.md:405` ("a kedge is later") and `:661` (§32, what M5 does not do:
  "the kedge"); `data/evolutions/lay_out_kedge.yaml:11-13` ("Warping to it (heaving the ship
  up to the kedge) is milestone 8's; here the kedge holds as any anchor down does");
  `docs/gates/gate-m5c.md:93` ("Warping, towing, the hawse fouled, the kedge worked (M8)");
  `docs/DesignProposal.md:509` lists "warping, kedging off" as must-have.

In sum: M5 meant the grounded captain to wait for the flood, and expected the kedge to be the
anchor's way off once the boat existed. What was built is Falconer's harbour kedge, which
cannot be laid aground.

### What happens to a kedge once laid

`scripts.py:5153-5185`: the kedge goes `DOWN` at the hawse's position plus the hawser's length
along the bearing, with `scope_m = out_m` (three quarters of its 120 fathoms unless said). From
then on `physics/anchor.py:150-217` treats it as any anchor: it pulls at the hawse (the bow,
never a quarter port) and holds four times its weight times the ground's factor.

Can the hawser be hove on? Only by accident. `heave short` and `weigh` act on
`tackle.riding_by()`, "the one down with the most cable out" (`ship/parts.py:967-972`;
`scripts.py:4249, 4293`). If the kedge has more cable out than any bower, `heave short` heaves
the hawser in to a cable and a half the depth, and while `anchor.heaving` is set the physics
does not let the anchor drag and the cable's pull "brings her ahead" (`anchor.py:194-198`). A
ship afloat is therefore warped up to her kedge by `heave short`, undocumented. With a bower
down on a longer scope the same order takes the bower instead.

Aground nothing moves her: `physics/integrate.py:138-145` overwrites her speeds every substep
("the ground holds her ... no way through the water but the stream's past her, no swing") and
`:149-150` does not advance her position. The cable's pull, the sails and the helm are all
computed and thrown away.

### Float, re-strike, and whether an anchor holds her (session 2)

`ground.py:118-156`. Each tick the keel is tested at bow, stern and amidships against the
chart's depth plus the tide (`chart.py:786-828`). Once aground she is "off only with a foot
under her": the test is repeated at `draught + AFLOAT_MARGIN_M` (0.3 m; `ground.py:66-72,
137-150`). When she floats, `_afloat` clears `extra["aground"]` (`:271-279`) and the physics
has her again at once, with the wind and the stream acting from that tick. The strike test is
then the bare draught again, so she strikes as soon as any of the three points finds a foot
less water. The tide is stepped once a minute (`core/world.py:554-572`); 651,840 is a minute's
tick, which is why she floated then, and 21 seconds of drift in eleven knots of wind put her
back.

"She struck at half a knot" is not her speed over the ground. `ground.py:164` takes
`dyn.speed`, which is speed through the water (`integrate.py:200`), and while aground the
physics sets that to the stream past her (`integrate.py:141-143`). A ship that floats and
touches again in a half-knot stream "strikes at half a knot" standing still. The mast shock
(`ground.py:204-206`) and the leak rate (`:208-211`) are worked from the same figure.

An anchor let go while aground: normally none can be, since `let go` is refused. The Harpy's
was ordered 22 seconds before she struck (636,631), and the script's fifteen seconds of
"stand clear" ran on through the strike with no second check (`scripts.py:4170-4184`), so the
best bower went down under her forefoot at 636,676 and 28 fathoms were veered (five times the
depth). When she floats the cable gives nothing until it is taut: `anchor.py:177-182` returns
no force while `hypot(dist, depth) <= scope`. She can drive about 27 fathoms in any direction
before the cable takes a strain, which is far more than the foot of margin she floated on. So
no, it does not hold her from striking again. What did get the Harpy off was `heave short` at
the second float (653,522 to 653,995, "nine fathoms of cable"), which is allowed aground and
afloat and took the slack out.

### What a fix would touch

1. **Narrow `_not_riding`** to the helm, the trim and the nine true manoeuvres, by name, so
   that bracing, furling all, sending down masts and yards and the harbour evolutions are
   given aground and at anchor. `verbs.py:93-99`. **S.** Risk: a pinned passage whose book
   gives one of those at anchor would gain an accepted line where it had a refused one
   (digests in `tests/test_known_truths.py`).
2. **Let the kedge be laid aground and hold her when she floats.** Drop the guard at
   `scripts.py:5084-5085`. **S**, but with it `heave short` must be refused in words while
   she is fast, or capped as in item 3: on a taut hawser with the ship held, the heave would
   raise the tension without limit (the drag is skipped while heaving, `anchor.py:194-198`)
   and `judge_cables` would part it. The kedges are light (the brig's is 100 kg, holding at
   most some 4 kN by `HOLDING_PER_WEIGHT`), so whether one holds her in a breeze wants
   measuring.
3. **Kedging off proper**: a limit on what the capstan can heave, and the ground's grip as a
   force to be overcome by the hawser and backed sails rather than an absolute hold
   (`integrate.py:138-150`, `anchor.py`, `ground.py`), plus an order that names the anchor to
   heave on. **L**, a design decision first; the documents give it to M8.
4. **The strike's speed over the ground** (`ground.py:164, 297-299`; `scripts.py:3824-3831`
   already has the sum). **S.** Risk: truth 66's wording ("at the speed the log gives").

---

## B. The leak, the well, the carpenter, the pumps

**Claims.** "'The well' still says there is no well" (owner, 2); "the carpenter reports 'four
feet and gaining' as text, with no reading behind it and no pumps to answer it. 'Send for the
carpenter' brings him aft with nothing to say."

**Verdict.** CONFIRMED, each part.

**The reading and the order.** `freesail/api/readings.py:973-977`:

```python
REGISTRY.add_absent("well", ("the well",),
    "The ship has no well to sound yet; that reading comes with the world.")
```

`sound the well` parses as the lead's verb with the object "the well", and
`freesail/orders/__init__.py:121-126` refuses it in that sentence (`prompt.absent_named`,
`orders/prompt.py:181-188`). Session 2, tick 673,476.

**"The starter's `sound the well` held" (package 33c).** The starter book has `standing order
"sound the well": every glass then sound the well` (`data/standing_orders/starter.orders:122`).
It was refused at every start from milestone 4a. Package 33c made the standing grammar enter
it and hold it "until the world has that reading" (`standing/grammar.py:253-258`;
`tests/test_standing.py:1839-1863`). It has never fired.

**Where "four feet and gaining" comes from.** `freesail/world/ground.py`:

- At the strike a rate is set: `LEAK_ROCK_M_PER_H` 0.6 or `LEAK_SOFT_M_PER_H` 0.05 metres an
  hour at four knots, times the square of her speed over four knots (`:55-60, 208-211`), kept
  in `ship.extra["leak_m_per_h"]`. Above 0.02 the line "The carpenter reports her stove on the
  rock and making water" is written (`:212-219`).
- `_leak` adds the rate to `hull.water_in_well_m` each tick and writes `well.rising` at each
  whole foot (`:241-261`); at `WATERLOGGED_M` 2.0 m one urgent line, "She is waterlogged"
  (`:262-269`).

So there is a level and a rate. What they do:

- **Nothing reads the level.** `water_in_well_m` (`ship/parts.py:1020`) appears in `ground.py`
  and nowhere else: no draught, no speed, no stability, no foundering. The module says so
  (`ground.py:17-20`: "the pumps are milestone 8's with the well's reading ... at two metres
  she is waterlogged and nothing more is modelled").
- **The leak stops the moment she floats.** `_leak` is called only `if self.grounded is not
  None` (`ground.py:155-156`). The Harpy had 4 feet at 17:21 and floated at 18:04 and 18:32;
  by the rate she stands at about 4 ft 10 in for good. No line says the well has stopped
  gaining.
- **A second, gentler strike lowers the rate.** The rate is assigned, not added
  (`ground.py:211`). The Harpy's fell from 0.35 m/h (three knots on rock) to 0.02 m/h at the
  re-strike "at half a knot".
- **"Rocky" in a note about sand is rock.** `rock = rock or "rock" in bottom.lower()`
  (`ground.py:169`). The Harpy took the ground "on sand, foul and rocky in the north part" and
  was "stove on the rock" at twelve times the soft rate. `anchor.GROUND_HOLDING`
  (`physics/anchor.py:76-88`) matches the same way, "rock" first.

**Pumps.** No order exists. `man the pumps` is "not an order this ship understands; did you
mean 'demand'?" (session 2, tick 636,737). The package 34 brief listed "the well rising, the
pumps" among the consequences (`docs/dev/M5-WorkPackages.md:1318-1320`); the tuning notes
record "Not done ... the pumps" (`docs/dev/TuningNotes.md`, package 34's found-on-the-way
list) and the primer says they are "a later milestone's" (`primer/13:39`).

**`send for the carpenter`.** `freesail/orders/people.py:45-55` calls `People.send_for`
(`freesail/world/people.py:465-508`), which sets a move in hand; a minute later the tick
writes "Mr Kemp came aft, sent for." (`:576-580`). That is all: the module's own words are
"here a person is data and a line" (`world/people.py:27-28`).

**What M5 specified against what is unfinished.** Spec §18 (`TechnicalSpec-M5.md:403-405`):
"the consequences are the hull's (a stop, a strain on the masts, a leak by the bottom's kind
and the speed) and the log's". The stop and the masts are built whole. The leak is built as a
counter that speaks. Plainly unfinished: the reading, the pumps, any effect of the water, and
the leak after she floats. The absent sentence itself is stale: "that reading comes with the
world" was written in milestone 4, and the world has come.

**The smallest coherent steps.**

1. **The carpenter's word.** When he is sent for and the well is not dry, his arrival line
   says the level and whether it gains; and `ship.afloat` says the same once.
   `world/people.py:576-580`, `world/ground.py:271-279`. **S.** No pinned day moves.
2. **`the well` as a reading, `sound the well` as an order that says it.** Replace the absent
   row with a row over `hull.water_in_well_m` in feet and inches (a comparison in feet for the
   dialect), stop the refusal at `orders/__init__.py:121-126`. **M**, because the starter
   book's rule stops being held and fires every glass: the "Held until" line and forty-eight
   firings a day change every pinned day run under the starter book (`GATE_5A_DAY_DIGEST` and
   the rest in `tests/test_known_truths.py`), and these tests pin the absence today:
   `test_standing.py:606-611, 1839-1863`, `test_orders_m4a.py:316-330`,
   `test_python_api.py:310-314`, `test_weather_script.py:254-261`, `test_agents.py:418`,
   `test_replay.py:92-117`, `test_known_truths.py:2066-2086`.
3. **Pumps as a duty that holds the level**: an order, hands held and tiring, a rate against
   the leak, and the leak going on afloat. **M to L**; whether a leak continues afloat is a
   decision the code has not made.
4. **The water mattering** (draught, speed, foundering). **L.**

---

## C. Sternway

**Claim.** "With sternway, the helm steers as if she had headway."

**Verdict.** NOT REPRODUCED from code as stated. Two nearby things are true.

**The rudder reverses.** `freesail/physics/hull.py:231-243`:

```python
flow = u * abs(u) + math.copysign(RUDDER_SMALL_SPEED2, u if u != 0 else 1.0)
side = -q * flow * rudder
return side, side * rudder_lever(hull)
```

`flow` is negative for negative `u`, so the side force and the yaw moment change sign: "With
sternway the rudder works the other way, as it should." `integrate.py:106-107` passes
`d.u`, speed through the water.

**The helmsman shifts his helm.** `hull.py:358-362`, when steering a course or full and by:

```python
if d.u < -STERNWAY_SHIFT_SPEED:
    st.helm_integral = 0.0
    wanted = -(HELM_KP * err - HELM_KD * d.r)
```

`STERNWAY_SHIFT_SPEED` is 0.15 m/s (`hull.py:81`), about a third of a knot. Between nothing
and that he holds the headway helm, when the rudder has almost no force either way.

**What the model saw (session 2, ticks 683,528 to 684,810).** She had lost her way close to
the wind on the starboard tack ("Hove the log: no way", 684,041). The officer ordered `steer
ENE` meaning to bear up. `hull.heading_error` (`hull.py:315-316`) is `wrap_pi(target -
heading)`, the short way round. By the log's own lines (684,398, the wind "43° on the
starboard bow"; 684,676, on ENE, "100° on the larboard quarter") the wind was about NNW and
her head about WNW, and from WNW to ENE the short way is some 143 degrees to starboard,
through the wind. The owner's words at 684,794: "I saw the helm was trying to steer through
the wind with no way on." The rudder did what the helmsman asked; the helmsman chose to go
through the wind's eye with a ship that could not stay. The model put it down to the rudder.
(The heading at the order is my working from those two lines; the log does not give it.)

**What is true of the words.** The conning orders hold the rudder where ordered and describe
the result as for headway whatever her way. `verbs.py:2060-2067`:

```python
way = "her head coming up to the wind" if verb == "helm a lee" else "her head paying off"
```

With sternway `hard up` brings her head up and `hard down` throws it off, and the log line
says the opposite. `FillAwayScript` knows this and tends the rudder by the sign of `u`
(`scripts.py:1338-1340`); `GetUnderWayScript` puts the helm a-lee for the stern-board and
leaves it there whatever `u` is (`scripts.py:4700-4701`; section D).

**Fix.** (a) `verbs._conn`: say the truth when `dyn.u` is astern ("she has sternway: the helm
works the other way"). **S.** (b) `steer` across the wind's eye when she has not the way to
stay: go the long way round, or say in the order's reply that the course lies through the
wind. `verbs._helm` or `hull.heading_error`. **S to M**, with a judgement about when a turn
through the wind is meant. Risk: (b) changes any old save in which a `steer` took her through
the wind at low speed.

---

## D. Getting under way in the schooner

**Claim.** "The schooner's 'get under way' doesn't cast her head onto the ordered tack. She
weighed lying head to wind and gathered sternway, and had to be backed off by hand."

**Verdict.** CONFIRMED.

### The logs

Seconds from "aweigh" to "She has paid off", every `get under way` in the eight sessions
(`cast_timeout_s` is 420):

| Ship | Casts |
|---|---|
| Schooner, session 1 (the owner's scripted merchant passage) | 420 (15,497), 420 (110,180) |
| Schooner, session 4 | 420 (38,157); 1 (256,512, already lying across the wind) |
| Brig, session 2 | 178, 82, 377, 420, 221 |
| Cutter, session 6 | 42 |
| Ship (the frigate's file), session 8 | 75, 1 |

Session 4 after the first: "Under way on the starboard tack, under the topsail and the
mainsail and the jib; ... steering SE by S (146°)" at 38,651, and the officer seven seconds
later: "she hasn't paid off: her head is south-west with the wind 34° on the bow, and she's
gathering sternway." He hauled the jib sheet to windward, let fly the main sheet and backed
the topsail by hand, and she went.

### The script

`GetUnderWayScript`, `scripts.py:4545-4807`; `data/evolutions/get_under_way.yaml`.

- **The timeout says she has cast.** `scripts.py:4731-4733`:
  `if (off >= cast_points and side == self.tack) or self.phase_t >= cast_timeout_s:` and both
  branches write "She has paid off; right the helm, brace round the head yards, set the
  spanker" (`:4760-4763`), fill the head yards and give the helm the course. The completion
  line says "Under way on the {tack} tack" regardless.
- **Square rig** (ship, brig): the after yards braced up for the tack and the head yards abox,
  `targets = [-self.sign * y.brace_limit for y in head] + [self.sign * y.brace_limit for y in
  after]` (`:4657-4662`); the jib at the break-out (`:4699`); the spanker only once she has
  cast (`:4741`). This is Luce's sequence and it is what the package measured, on the frigate
  alone (`TuningNotes.md`, package 35: "paid off seven points at 1261 s").
- **Fore-and-aft** (schooner, cutter; `head_and_after_yards` gives a one-masted set of yards
  as head yards only, `scripts.py:345-355`): the topsail is braced abox, which is right. But:
  1. **The mainsail is set before the anchor is out, flat aft.** `:4656`,
     `_set_fore_and_aft(ship, _boom_mainsails(ship), self.tack)`, which trims the sheet to
     `wanted_sheet_angle("gaff", apparent wind now)` on the lee side of the tack wanted
     (`scripts.py:4533-4542`; `evolutions/trim.py:153-166, 181-184`). At anchor head to wind
     that is the floor, 18 degrees. While the wind is on the wrong bow the boom, if the sheet
     holds it over (`trim.py:403-406`), is aback and helps. Once the wind is on the right bow
     it is an ordinary mainsail sheeted flat: it shakes until the wind is past its luffing
     angle (a fore-and-aft sail with the wind on its lee face "collapses and flogs",
     `physics/sails.py:985-989`) and then it draws, 198 m² eleven metres abaft her middle, and
     brings her head back up. She hangs two or three points off, which is the 34 degrees in
     the log, with the backed topsail giving her sternway.
  2. **The jib is sheeted to leeward of the tack wanted, not held to windward.** `:4699`,
     `_set_fore_and_aft(ship, _jib(ship), self.tack)` hauls the lee sheet to 15 degrees. With
     the wind fine on the right bow a jib sheeted there flogs and does nothing; with the wind
     on the wrong bow it is aback and pushes her head toward the other tack (session 1,
     15,506: "Jib taken aback" nine seconds after it was hoisted). Held to windward it would
     be aback the right way from the first.
  3. **The helm is a-lee for a stern-board and never tended.** `:4700-4701`,
     `dyn.target_rudder = self.sign * units.deg_to_rad(15.0)`. Right with sternway; with
     headway through the water (the mainsail and jib drawing, or a tide past her as she
     breaks out) the same rudder luffs her.
- **Package 32e's headsail sheet held to windward is not used here.** It exists and works:
  `sheets_to(ship, sails, "weather", None)` (`scripts.py:229-236`) is how `heave to` holds the
  fore staysail aback (`:1239`) and how a tack that hangs boxes her head off (`:874-877`,
  with the boom hauled over to windward too). The officer's own order used the same state:
  "Hauled the starboard jib sheet to windward; the jib now 15° off the centreline; aback"
  (session 4, 38,658).

### What decides the tack

`scripts.py:4553, 4581-4588, 4595`: the words of the order (`on the starboard tack`, read by
`_TACK_RE`, `orders/ground_tackle.py:74, 166-170`); else the pilot's `cast` from his port's
file when he is aboard; else `"starboard"`, always. `get_under_way.yaml:43` says "the pilot's,
else the one her head falls off to from the wind"; the code has no such rule, and it does not
look at the course asked either. Session 2, tick 211,328: "She cast the wrong way, sir" after
a bare `get under way`; session 8, tick 121,807: the officer belays his own order because he
named the wrong tack for the course.

### Fix, size, risk

In `GetUnderWayScript`, for a vessel whose yards are on one mast: the mainsail set with its
sheet eased right off (`ease_off_sheets`) or left until she has cast; the jib's sheet on the
weather side of the tack wanted (`sheets_to(..., self.tack, None)`) and let draw when she has
paid off; the rudder by the sign of `dyn.u` as `FillAwayScript` has it. For every rig: the
timeout to say she has not paid off, and not to hand the helm a course. With no tack said and
a course given, take the tack that lays the course. About forty lines in one script: **S to
M**, with a test of the cast per rig, since the tests of this evolution run the frigate only
(`tests/test_ports.py:339-426`). Risk: the merchant passage is the schooner and gets under way
twice, so `GATE_5C_MERCHANT_DIGEST` and its tick constants (`test_known_truths.py:3708-3733`)
are re-pinned; old saves of the schooner and the cutter replay differently from their first
`get under way`. The frigate's and the brig's path need not change.

---

## E. Anchoring in very deep water, and in water shoaler than her draught

**Verdict.** The scope and the cable: WORKS AS DESIGNED. Warnings and a check against her
draught: CONFIRMED absent. A fault in the depth kept over the anchor: found (below).

### How the scope is chosen

`physics/anchor.py:113-120, 132-134`: `RIDING_SCOPE_PER_DEPTH = 5.0` (Luce's "five or even six
times the depth"); `scope_wanted_m` is five times the depth, always. `scripts._scope_wanted`
(`scripts.py:3955-3960`) uses a number of fathoms from the order instead when one is said.
`_veer` caps it at the cable bent to that anchor (`scripts.py:3891-3896`). 46 fathoms gives
230; 30½ gives 152; 3½ gives 17.

### What cable she carries

Every ship file has 240 fathoms on the best bower and 120 on every other anchor
(`data/ships/brig.yaml:1746`, `cutter.yaml:646`, `frigate-36.yaml:2082`,
`topsail-schooner.yaml:789`). It is the generator's one rule: `CABLE_FATHOMS = 120.0`,
`BEST_BOWER_CABLES = 2`, on Falconer's "it is necessary to splice at least two cables
together, in order to double the length when a ship is obliged to anchor in deep water"
(`tools/gen_ships.py:427-433, 465`). So yes, the cables are bent together, by design, on the
85-ton cutter as on the frigate.

### What is refused

Only water deeper than a third of the cable: `scripts.py:3991-3995` and `:4163-4164`, "no
anchoring ground here: …". That is 80 fathoms for a best bower and 40 for any other anchor
(the test says as much, `tests/test_anchor.py:314-330`). Nothing warns. In 46 fathoms she
veers 230 of her 240.

### What a sailor would expect

A word before the anchor goes: that it is deep water, how much cable will be out and how
little left, and that it is most of an hour at the capstan to get it again (the game's own
rate is six fathoms a minute, `weigh_anchor.yaml`; session 4 took 39 minutes to heave 185
fathoms up and down). A scope he can choose: three times the depth in deep water in fine
weather was the old rule the module itself quotes. And a way to heave some in. The officer
planned "three to one, 130 fathoms" (session 4, 532,406), got 230, and had no order to shorten
it: `heave in 70 fathoms` ran as `heave short` (section K, item 5).

`come to an anchor in twelve fathoms` does not do what the primer says. Primer 13, line 71:
"The last is the depth to let go in: she stands on until the lead calls it." The code comes to
at once and uses the number as the scope (`scripts.py:4063`,
`_scope_wanted(ship, self.anchor, depth, self.params.get("fathoms"))`; the parse-only check
gives `params = {'fathoms': 12.0}`). Twelve fathoms of cable in ten of water will not hold.

### Depth against draught

There is no check. `LetGoAnchorScript.check` (`scripts.py:4144-4165`) and
`ComeToAnchorScript.check` (`:3973-3996`) test for no bottom and for too deep, nothing else.
Session 8, tick 121,712: the *Amazon*, drawing 15 ft 1 in (`frigate-36.yaml:23`, 4.6 m), let go
in three fathoms and a half at the top of a tide that falls twenty-five feet. The "dragging"
66 ticks later is the physics as designed: she was let go with her topsails drawing, and an
anchor that comes home for sixty seconds is said to drag (`anchor.DRAG_SAY_S`); it held again
at 121,822.

**No reading gives her draught.** `draught` does not occur in `api/readings.py` or
`data/vocabulary.yaml`. Parse-only: `her draught`, `the draught`, `what does she draw`, `what
is her draught` are each "not an order this ship understands". The library's "the ship" topic
lists parts and no particulars (`agents/tools.py:1255-1262`). The figure exists in the ship
file, in `/api/ship` for the viewer (`api/queries.py:377`), and in the grounding line once she
has struck (`world/chart.py:430-434`).

### Found: the depth over the anchor is read at the wrong place

`core/world.py:578-584`, once a minute:

```python
at = self.origin.advanced(anchor.ground_x, anchor.ground_y)
d = self.chart.depth_at(at) if self.chart is not None else None
if d is not None:
    anchor.depth_m = max(0.0, d + state.height_m)
```

The anchor's place is in the ship's plane metres from the scenario's start. The ship's own
position is advanced a tick at a time, each small run turned into longitude at the latitude
she is then in (`world.py:658-682`; `world/geo.py:72-84`). This line turns the whole voyage's
metres into longitude in one step, at the mean of the start's latitude and the present one.
The two agree on a straight passage and part on a dog-leg. The same arithmetic outside the
game, on straight legs between the ports (the size of the thing, not the sessions' own
tracks, which I do not have):

| Track | The anchor's depth is read |
|---|---|
| Ushant to Falmouth, straight (gate 5b's passage) | at the ship |
| Falmouth to Roscoff, straight | at the ship |
| Plymouth, Roscoff, Scilly (the shape of session 4's) | 1.4 miles west of the ship |
| Falmouth, Roscoff, mid-Channel, Falmouth, Plymouth (the shape of session 2's) | 0.6 mile west of the ship |

After the anchor is let go this line is the only thing that writes `anchor.depth_m`
(`scripts.py:3947` sets it once at the let-go, from the water under the ship). So a depth that
changes by thirty fathoms in twenty minutes with no dragging can only be this place differing
from hers. Two log lines:

- Session 4, Scilly: "The best bower let go in 37 fathoms" (548,569), then "Brought up by the
  best bower in seven fathoms, a hundred and eighty-five fathoms of cable" (549,749). The
  officer took it for "a slip in the book".
- Session 2, Cawsand Bay: "let go in four fathoms" (688,836), then "Brought up by the best
  bower in no water" (689,722): the place read was on the shore, and `fathoms_words(0)` is
  "no water" (`chart.py:190-191`). The model listed this as "apparently a missing depth in the
  text".

It is not only words. `anchor.depth_m` is the depth in the cable's geometry and the anchor's
holding (`anchor.py:175-184, 192`), the target of `heave short`
(`scripts.py:4252-4253`), the up-and-down point and the hoisting time of `weigh`
(`:4321, 4337`). Read too deep, an anchor on a fair scope is past its tripping angle and
drags in a light air; read at nothing, `heave short` heaves the whole cable in. The Harpy's
bower dragging twice in light airs off Roscoff on 14 June (174,157 and 175,482) may be this;
I could not tell from the log.

**Fix.** Take the anchor's place as a short offset from the ship's true position:
`self._position.advanced(anchor.ground_x - self.ship_x, anchor.ground_y - self.ship_y)`. One
line. **S.** The same one-step conversion is in `_coast_of_plane` (`world.py:684-694`) for the
weather's coast. Risk: any passage that anchors after a track that was not straight changes
from the minute after the anchor goes (words, holding, weighing times), so old saves replay
differently there; the pinned passages are close to straight but should be run. No test
anchors after a dog-leg, which is why the suite never saw it.

### Fix for the rest, sizes

A reading `the draught` (**S**: a row in `readings.py`, the words in `vocabulary.yaml`). A
caution in the two checks' replies when the depth is over some thirty fathoms, and when the
cast less the master's own allowance for the tide (he has both: `reckoning._tide_allowance_m`,
`reckoning.py:1295-1325`) leaves less than her draught at low water (**S** each; the second
must use his tide, never the world's). A scope the captain can say on `come to an anchor`, and
`in <n> fathoms` made the depth to let go in as the primer has it (**S to M**:
`orders/ground_tackle.py`, `ComeToAnchorScript`). Risk for all of these: none to the pinned
passages if the default scope is unchanged at the depths they anchor in (14 fathoms at most).

---

## F. The chart's sounding labels read "NaN fm rock and mud"

**Verdict.** CONFIRMED.

`client/map.js:450`:

```js
var fm = s.depth_m === null || s.depth_m === undefined ? "no bottom" : Math.round(s.depth_m / U.FATHOM) + " fm";
```

`client/units.js:8-10` defines `KNOT`, `NAUTICAL_MILE` and `CABLE`, and the export at `:81-101`
has no `FATHOM`. `s.depth_m / undefined` is `NaN`. It is the only use of an undefined member
of `Units` in the client.

The server's side is right. A sounding carries `tick`, `depth_m` (metres, or null for no
bottom), `ground`, `words`, `lat_deg`, `lon_deg` (`world/reckoning.py:540-548`), and the client
reads those names. Casts with no bottom draw correctly as "no bottom"; every cast that found
bottom draws "NaN fm" and its ground.

**Fix.** `var FATHOM = 1.8288;` and `FATHOM: FATHOM` in `client/units.js` (the figure is
`freesail/units.py:28`). Two lines. **S.** Worth doing with it: `Math.round` makes "and a half
four" read "5 fm", and inshore the halves are the point; print to the half fathom under
twenty. No test draws the chart's account (`tests/test_map_view.py` runs only the view's
arithmetic in Node), which is how this passed; a label built in a pure function could be
tested there. No risk to saves or digests.

---

## G. The reckoned track is cleaned up too aggressively

**Verdict.** CONFIRMED. It is a cap on a count, server-side, and the count fills far faster
than its comment supposes.

`world/reckoning.py:283-285`:

```python
# The track by account kept for the chart: the last so many hourly positions (judgement:
# a week of hourly steps, so a long passage's snapshot stays small).
TRACK_KEPT = 168
```

and `:662-664`, in `Reckoning.advance`:

```python
self.track.append((tick, self.lat_deg, self.lon_deg))
if len(self.track) > TRACK_KEPT:
    del self.track[0 : len(self.track) - TRACK_KEPT]
```

`advance` is not hourly. `Navigation.bring_up` calls it, and `bring_up` is called at every
heave of the log (`reckoning.py:1203`), every cast of the lead that finds bottom (`:1261`),
every bearing taken (`:1392`), every transit (`:1443`), the noon, every sight and every course
shaped (`:1526` to `:2046`). At anchor it is worse: "No hours at all (the whole interval hove
to) still steps the board" (`:620`), so a lead going every ten minutes at anchor adds six
copies of the anchorage an hour.

Counted from the logs (ticks with a cast that found bottom, a bearing or a heave of the log;
the noons and sights add a few more): session 1, the owner's merchant passage, made at least
358 points in 39 hours, and the last 168 of them begin at tick 114,000. At the end the chart
held the last seven hours, the Goulet and the Bay of Brest, and the Channel was gone. Session
2 made at least 436 points in eight days, session 4 at least 382.

The pruning is also upside down. The track is capped; `soundings` and `bearings` are never
trimmed (`reckoning.py:1340, 1411`), every one of them is sent in every snapshot (`:836-839`)
and drawn, each bearing as a twenty-mile dashed line from its mark (`client/map.js:432-445`).

Client side there is no thinning: `map.js:408-427` draws every point it is given, and keeps no
track of its own on the chart (`:243-247`); the one-hour buffer `TRACK_SECONDS` is for the
plane only (`:30, 248-251`). The "fit" button's tooltip says "the whole track and the ship"
(`client/index.html:90`) but the view is fitted to the last four points
(`map.js:567`).

**What keeping the whole voyage costs.** A point is about 25 bytes of JSON. Hourly points for
a thirty-day voyage are 720 points, 18 KB, in a snapshot sent about once a second
(`ui/server.py:131-138`) that already carries every sail, spar and line. The track feeds
nothing back into the simulation, so no digest and no replay moves; an old checkpoint loads
with the list it has.

**The simplest good rule.** Keep for ever the points made at a heave of the log, a noon and a
fix; keep every other point (casts, bearings) for the last twelve hours; never append a point
equal to the last. `Reckoning.advance` needs to be told what kind of step it is. **S**
(`reckoning.py`, about fifteen lines; `tests/test_reckoning.py:80` counts points). If the
snapshot's size is ever a care, send the old part once by its own route, as `/api/chart` is.
The soundings and bearings want the opposite treatment: an age, or only the last so many
drawn.

---

## H. The state panel and the controls

**"1x option can be moved from the 'state' section."** The speed buttons 1x, 10x, 60x and 300x
are already beside hold, go and tick 60 (`client/index.html:16-23`). The only thing in the
instruments panel that says 1x is the checkbox "ease to 1x when a station is sampled or
speaks", in the row under "Clock" (`index.html:66`; styled at `client/style.css:212-213`;
wired by its id at `client/app.js:82-83, 360-365`). I take that to be the option meant. Moving
it is the label moved into `<span class="driver">` and two style rules. **S**, under ten
lines; `app.js` finds it by id and needs nothing.

**Anchor facts.** The snapshot has none (`api/queries.py:179-306`). The server has them as
readings (`api/readings.py:1556-1683`):

- `the anchor`: in words, "down, riding by the best bower to the flood, the wind across the
  tide, 62 fathoms out", with "dragging;" and "moored with two anchors;" before it when so;
  or aweigh, catted, at the bows, lost; or "aground, forward on sand". The value carries the
  anchor's id and its whole record (scope, cable's length and size, load, holding, taut,
  dragging, bottom).
- `the cable`: "62 fathoms of the best bower's cable out, bar-taut, the strain 0.01 of the
  rating", and the wear when worn.
- `the ground tackle`: every anchor with its weight, cable and state.

The console's `state` already prints the first two while she is at anchor or aground
(`core/world.py:1198-1203`). Showing them in the browser is two words in the snapshot
(`r.words("anchor")`, `r.words("cable")`) and two rows in `client/instruments.js` and
`index.html`. **S**, about twenty lines and a test. Send the words, not the record:
`holding_kn` and `depth_m` are the physics' numbers, which nobody on the forecastle sees.

---

## I. Charting tools

**What `map.js` offers today.** The wheel zooms about the cursor (`client/map.js:138-149,
173-182`); a drag pans (`:150-169`); "centre" follows the ship and "fit" returns to the
default view (`:193-203`); a graticule and a scale bar at a cable, a mile, five or twenty
miles (`:90-102, 595-615, 690-704`); names when a mile is thirty pixels (`:86-88`); a fixed
north arrow and a wind arrow (`:657-688`). No measuring, no bearing or distance read-out, no
rose, no lines, no marks. The pieces a tool needs are there and pure: `frame.at(x, y)` gives
the latitude and longitude under a pixel and `frame.of(lat, lon)` the reverse (`:264-273`).

**Size.** A movable compass rose (true, and magnetic by `snapshot.reckoning.variation`), ruler
lines that say a bearing in points and a distance in miles and cables, and markers with a
word, kept in the browser's `localStorage` by chart region: about 300 to 400 lines in
`client/map.js` (733 today), tool buttons in `index.html`, a little CSS, and Node tests of the
geometry in `tests/test_map_view.py`. The pointer handling needs modes, since a press is a pan
today. **M**, no server change. If the marks are to be the game's (saved, journaled, seen by
an officer's station or by note 25's chart snapshot), that is an order and a store on the
server: **L**, a design decision first.

**The account, not the truth.** The tools work in the chart's latitude and longitude and from
the hull symbol, which is drawn at the reckoning (`map.js:633-655`), so a line from the ship is
a line from the account and should say "by account". One thing must not be drawn: the
lookout's items in the snapshot carry the true distance of every mark in sight (below). A
"line to the mark" tool that used them would plot the truth.

---

## J. The cutter's square sail in the viewer

**Verdict.** CONFIRMED. The fault is the data, with a tenth more from the drawing.

**The sail.** `data/ships/cutter.yaml:116-125`: `square_sail`, class `square`, on
`square_sail.yard`, 104 m², centre 13.1 m above the water; the comment says "27 ft deep,
four-fifths of the mainsail's fore-leech". It is her course, set flying (alias "the
crossjack"); the `topsail` (56 m²) and `topgallant` (19 m²) are above it. The file gives a sail
an area and a centre and no hoist, head or foot. The yard: `cutter.yaml:81-88`, 14.0 m long,
`height_m: 15.9` above the deck, on a mast 16.1 m above the deck.

**The drawing.** `client/projection.js:692-698`:

```js
var L = Y.half * 2;
var depth = (spec.area_m2 / Math.max(L, 1)) * reefFraction(spec, dyn);
var down = v(0, 0, -depth);
var corners = [Y.a, Y.b, add(Y.b, down), add(Y.a, down)];
```

A square sail is a rectangle the whole length of its yard, as deep as its area over that
length: not the gap to the yard below, not a fixed proportion. For the cutter that is 104 /
14.0 = 7.4 m, from the yard at 15.9 m down to 8.5 m above the deck. The sail covers the upper
half of the mast and stops.

**Why.** `tools/gen_ships.py:3404-3413` hoists the yard to the cap: `sq_yard_h = main_above -
0.5`, 52½ ft above the deck, on Fincham's "the height of the square-sail-yards will be their
diameter above the upper part of the gaff", read as the gaff's peak. `:3433-3438` then makes
the sail by Steel's sloop: `sq_depth = 0.8 * main_hoist`, 27 ft, and `sq_area = round(0.9 *
sq_yard * sq_depth ...)`. A 27 ft sail from a yard 52½ ft up has its foot 25 ft above the deck
in the file itself. Fincham's lofty mast and Steel's sloop's depth do not go together. The
drawing loses another tenth because the area was reckoned on a head nine-tenths of the yard
and is drawn across the whole of it (24 ft against 27).

**Fix.** Drawing only: draw the head at nine-tenths of the yard (`projection.js:695-698`).
**S**, and it gains under a metre; the sail still ends far above the deck. Data: in the
generator, either sling the square-sail yard at the hounds, or make the sail as deep as the
yard's height less the bulwark. **M**: the cutter's file is regenerated, the sail's area and
centre move (so her running before the wind with it set), the yard's and the mast's ratings
are worked from it, and the topsail's depth is defined by the gap to this yard (`:3440`). It is
a light sail and not in "plain sail", so the hierarchy truths 73 and 75 (plain sail) should
not move; `tests/test_view_geometry.py:434-466` pins only the yards' order. Old saves of the
cutter replay differently once the square sail is set.

---

## K. Weighing, heaving to and filling away, from the logs

### 1. The brig hove to goes through the wind, or lies with both topsails aback

What `heave to` does on the brig (`HeaveToScript`, `scripts.py:1135-1280`;
`data/evolutions/heave_to.yaml`):

- backs every yard on the mast with the most square sail (`yards_to_back`, `:368-387`): the
  brig's main, so the main yard, topsail, topgallant and royal yards, to `-sign * brace_limit`
  over 45 seconds (`:1186-1190`);
- hauls up the courses and clews up the light sails forward (`:1195-1197, 1226-1230`);
- keeps the spanker and eases its sheet to the trim of a wind six points on the bow, because
  on a brig the backed yards are on her aftermost mast (`:1205-1212`,
  `HOVE_TO_DRIVER_APPARENT`); on the frigate it is brailed up;
- hauls the head sheets flat aft (`:1256`);
- puts the helm a-lee, 15 degrees of rudder toward the wind, at once, and leaves it there
  (`:1191-1192`).

When the yards are round it writes "Hove to", sets `ship.extra["hove_to"]` and ends
(`:1265-1270`). Nothing keeps her hove to after that. The helm is a fixed rudder angle; no one
tends it or the sheets; the script does not look at whether she lies to. The tuning notes show
how fine the balance is on this hull: with the spanker's sheet for six points she lies 66
degrees off; for five she comes up to 24 and falls off; for eight, 86
(`docs/dev/TuningNotes.md:953`), measured in fifteen knots of wind.

Session 2, hove to for the pilot (order begun 17,674): main topsail and topgallant aback at
17,705; "Hove to" 17,726; then "Fore topsail taken aback" 17,834, "Fore topmast staysail taken
aback" and "Jib taken aback" 17,846, and "Main topgallant filled again", "Main topsail filled
again" 17,855 and 17,857; leeway now to starboard; the log hove at 18,035, a knot and a half.
Her own head went through the wind: on the other tack the yards that were aback are full and
the fore yards and jibs are aback. By the code the only things turning her were the rudder
held a-lee from the first second, with her way still on, and the spanker kept drawing; that
they carried her up and across before the backed topsail stopped her is my reading, not a
measurement. None of the three causes offered did it: no standing order fired in those three
minutes; `keep her full` is refused while she is hove to (`verbs.py:1949-1961`) and the helm
is a held rudder; the log has no wind shift.

The fog (order at 102,690): the main yards aback at 102,752, "Hove to" 102,765, "Fore topsail
taken aback" 102,854 and the main never filled. She came up until the fore topsail, braced
sharp, was aback as well, and lay there with a little sternway, the fore topsail filling and
backing by turns for hours (103,955 to 116,618).

**Fix.** The lee helm put down as her way comes off rather than at the order, and a helm that
is tended while she lies to: eased as she comes within five points, shifted with sternway.
`HeaveToScript` and the helm in `hull.steer`. **M**, with a truth per rig beside truth 12,
which is the frigate's. Risk: every pinned passage heaves to.

### 2. `trim sails` fills a ship that is hove to

`verbs._trim` braces every yard to the apparent wind (`verbs.py:788-815`:
`yards = [y for y in ship.spars.values() if y.is_yard ...]`), the backed ones with the rest.
It is guarded for the anchor and the ground (`:93-99`) and not for `hove_to`, though `steer`
and `keep her full` are (`:1949-1961`). The flag stays set afterward. Session 2: 137,021 "By
standing order 'trim on a shift': trimming sails. Braced eight yards to the wind" and 137,047
"Main topsail filled again"; again at 137,615. Session 4: 162,102 and 193,303, the fore
topsail filled 37 and 39 seconds later. This is the model's note 16, "filled her out of it,
twice". **Fix:** refuse `trim` (or leave the backed yards out of it) while she lies to.
`verbs.py`. **S.**

### 3. "Hove to" outlives the anchor, the weighing and a tack

`ship.extra["hove_to"]` is cleared by `fill away` and `back and fill` and by nothing else
(`scripts.py:1363, 3359`). `come to an anchor`, `let go`, `weigh`, `get under way`, `tack ship`
and `wear ship` neither refuse on it nor clear it. Session 2: hove to at 173,121; anchor let go
173,251; moored, unmoored, under way by Luce's sequence 211,315; tacked 212,315; then at
212,708 `Order not carried out ('steer north east'): She is hove to; fill away before giving
her a course.` Eleven hours and three evolutions later. While the flag stands the master runs no
distance for any time she makes under two knots (`reckoning.py:1021-1024`) and "taken aback"
is never said (`integrate.py:242-245`). **Fix:** clear it where she anchors, gets under way,
tacks or wears. **S.**

### 4. `weigh`, then nothing for seven minutes; `get under way` after `weigh` fails late

`weigh` is crewed `hands: all` to the end of catting and fishing
(`data/evolutions/weigh_anchor.yaml:36`), though the file's comment says "not a manoeuvre,
sail is made meanwhile" (`:34`). Session 4: aweigh at 556,029; `set plain sail` at 556,039
answered "Not hands enough on deck to set the mainsail; the hands are weighing anchor"; the
first sail work began at 556,453, seven minutes on, a mile from the ledges.

Given while a `weigh` is in hand, `get under way` is accepted and queued, because both hold
the ship and a queued evolution's checks wait until it begins (`runner.py:320-331, 690-709`).
When the weigh ends it fails. Session 4: ordered 543,919; "Could not get under way: no anchor
is down: she is under way already, or adrift" at 544,495, nine and a half minutes later, under
bare poles. **Fix:** `weigh` to keep only the forecastle for the cat and fish, or to release
the hands at "aweigh"; `get under way` behind a `weigh` to make sail and cast when its turn
comes, or to be refused at once. `weigh_anchor.yaml`, `GetUnderWayScript.check`. **S to M.**

### 5. `heave in 70 fathoms` is `heave short`, and the number is dropped

"heave in" is a synonym of `heave short` (`vocabulary.yaml:619-622`).
`ground_tackle.execute` reads the fathoms into `params` for any verb
(`orders/ground_tackle.py:138-140`) and `HeaveShortScript` never looks at them
(`scripts.py:4246-4256`); the parse-only check gives `{'fathoms': 70.0}` and the words of
`heave short`. Session 4, 534,281 to 536,457: asked to bring 230 fathoms to 160, she was hove
to "sixty-seven fathoms of cable, the cable a-stay in 45 fathoms" and began to drive. `heave
in 70 fathoms of cable` is refused; without "of cable" it is accepted. There is no order that
shortens the scope to a figure. **Fix:** `heave in <n> fathoms` and `heave in to <n> fathoms`
as the mirror of `veer`. **S.**

### 6. Smaller things met on the way

- `get under way` says "She has paid off" on its timeout, and casts to starboard when no tack
  is said (section D).
- `lay out a kedge` has no need of an anchor down in the code (`scripts.py:5074-5110`); the
  primer says it is refused at sea with none (`primer/14-the-port.md:119`).
- The schooner hove to in a light air made two knots of sternway (session 4, 531,421). Same
  root as item 1: a fixed helm and nothing tended.

---

## The truth on the wire and in the readings (asked with F and G)

The chart's own drawing is clean: the hull, the ellipse, the track, the noons, the soundings'
places and the strangers are all the account's, or a bearing and an estimate from it. What I
found that is worked from `world.position` or the true depth:

| Where | What | Line |
|---|---|---|
| Snapshot, `lookout.items[]` | For every mark, light, danger and piece of land in sight: `distance_m`, the true distance to the metre, and `bearing_deg`, the true bearing to a tenth of a degree, with the feature's id. `_data` removes the distance for a sail only. With the feature's charted place from `/api/chart` this is the true position. The client draws only the words (`map.js:724-727`) | `api/queries.py:206`; `world/lookout.py:423-433, 718-738`; `world/chart.py:384-393` |
| Events on the socket | `lookout.sighting` and `lookout.closing` carry the same `distance_m` in their `data`; every event goes to the browser with its data (`core/events.py:48-58`, `ui/server.py:507-512`) | `lookout.py:330-336, 413-417` |
| Snapshot, `strangers.items[]` | The true bearing to a tenth of a degree and the estimate; by design, and drawn from the account | `lookout.py:560-604`; `map.js:501-535` |
| Snapshot, `reckoning.soundings[]` | The cast's depth and ground are taken at the true position and plotted at the account: an observation, as meant | `reckoning.py:1236-1260, 1338` |
| Reading `the depth of water` (also `the water`) | The chart's depth at the **true** position, at the datum. Not in the snapshot. It is in every agent's sample (`agents/tools.py:153-172` sends every reading in words), at the prompt, and a standing order may test it (`standing/grammar.py:393`; `tests/test_chart.py:440`). A model in session 8 journaled "'depth of water' is the true chart depth, which the master does not see" (tick 21,755) and used it at 121,770: "the chart gives only half a fathom here at the datum" | `api/readings.py:557-566, 1089-1099` |
| Reading `the port` | Bearing and distance of the nearest road from the true position (the lead has this) | `world/ports.py:976-1018` |
| Reading `the anchor` (value) | `depth_m` over the anchor, by the chart and the tide, from the wrong place (section E) | `readings.py:1583-1585`; `core/world.py:578-584` |

Not on the wire: the ship's `x` and `y` are null on the sphere (`queries.py:218-226,
250-251`); the chronometer's block has only what the certificate says; `/api/chart` has no
depth tiles.

Spec §17 says "The true position is not in the snapshot the client receives"
(`TechnicalSpec-M5.md:397`). By the first row it is, for anyone who reads the snapshot and not
the canvas, whenever a charted mark is in sight. The fix is to drop `distance_m` from the
lookout's items for everything, as it is dropped for sails, and to round the bearing to the
point the log gives. **S.** `the depth of water` wants to be the lead's, or the chart's depth
at the account: **S** in code, but a standing order in an old book that reads it would change
meaning.

---

## Where the documents and the code disagree

1. Primer 13, line 42, recommends `at aground then furl all sail`; the order is refused
   aground (`verbs.py:93-99`).
2. `ground.py:12-14` quotes Luce's bracing aback and sending down the upper masts after a
   strike; both are refused aground.
3. `ground.py:26-28` and the package 34 brief give getting off to "a kedge laid out by the
   boat"; the kedge cannot be laid aground (`scripts.py:5084-5085`). Spec §32 says M5 does not
   do the kedge at all; package 35 built it.
4. Primer 13, line 71: `come to an anchor in twelve fathoms` is "the depth to let go in"; the
   code makes it the scope (`scripts.py:4063`).
5. `get_under_way.yaml:43`: the tack is "the pilot's, else the one her head falls off to";
   the code's else is starboard (`scripts.py:4553`).
6. `weigh_anchor.yaml:34`: "sail is made meanwhile"; the evolution holds all hands (`:36`).
7. Primer 14, line 119: `lay out a kedge` is refused at sea with no anchor down; the script
   has no such check.
8. `readings.py:976`: "The ship has no well to sound yet; that reading comes with the world."
   She has a well with water in it that the carpenter reports by the foot.
9. `client/index.html:90`: "fit" is "the whole track and the ship"; it fits the last four
   points (`map.js:567`).
10. Spec §17: no true position in the snapshot; the lookout's items carry it.

## Surprises

1. **The depth over the anchor is read away from the ship** after any passage that was not
   straight (`core/world.py:581`): about a mile and a half on a track shaped like session 4's.
   It is what "brought up in seven fathoms" and "in no water" were, and it reaches the holding,
   the short stay and the weighing. One line to fix.
2. **Twenty-six verbs are refused at anchor and aground**, `furl all sail`, `square the yards`,
   `loose sails to dry` and every bracing order among them (`verbs.py:93-99`). The primer's own
   standing order for a grounding is one of them.
3. **The schooner's cast has timed out every time it was needed**, in the gate's own scripted
   passage as well, and the log said "She has paid off" each time.
4. `the depth of water` is the chart's depth at the true position, in every model's sample.
5. The leak stops when she floats and a second touch lowers it; the strike's speed is through
   the water, so the tide alone gives "half a knot".
