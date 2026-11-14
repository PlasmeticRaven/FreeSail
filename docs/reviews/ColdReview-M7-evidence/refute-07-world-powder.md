# Refuter 07: the findings of spec-02 (M5, the world) and spec-04 (M7, powder)

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read whole: `READERS.md`, `REFUTERS.md`,
`spec-02-M5.md`, `spec-04-M7.md`. Read in part: `docs/DesignProposal.md` (§5.1 line 305, §5.2
line 320, the M7 line 553, decisions 39, 44, 49, 56, 64, 66, 67), `docs/TechnicalSpec-M5.md`
(§11 line 315, §17 lines 791 to 802, §23 lines 945 to 955, §33 item 25 lines 1409 to 1411),
`docs/TechnicalSpec-M7.md` (§24, §25, §29, §30). Nothing under `docs/dev`, `docs/design`,
`docs/playtests`, `docs/gates` or the sealed notes was opened. No suite was run. Two world
builds were made (one to recover the position from the log, one under the profiler); scripts
are in the scratchpad, not the tree. Nothing in the tree changed but this file.

| finding | first weight | verdict | my weight |
|---|---|---|---|
| 02-1 the true position reaches the browser in the log's data | high | STANDS IN PART (sent, not shown; no model gets it) | medium |
| 02-2 the captain's chart is the truth; `chart: {year}` read by nothing | high | STANDS IN PART | medium |
| 02-3 the dockyard repairs nothing | medium | STANDS IN PART | low to medium |
| 02-4 the war priced twice | medium | STANDS (tin sure; brandy in part) | low to medium |
| 02-5 the crew pool never refills | medium | STANDS | low |
| 02-6a the map eighty times the plan; "most scenarios use two regions" | medium | STANDS IN PART: the growth is the owner's ruling; the "two regions" falls | low (repository size medium) |
| 02-6b every port loaded, six seconds to build | medium | STANDS IN PART: the ports are a seventh of the build | low |
| 02-9 the document half history | medium | STANDS (not tested further) | medium |
| 04-1 the fine control of the sails not built | high | STANDS IN PART: two of the eight items exist from earlier packages | medium to high |
| 04-2 the gate cannot be run at this commit | high | STANDS IN PART: two items blocked; 7c and 7d not; 7a turns on a reading | medium |
| 04-3 the spec stops at package 101 | high | STANDS IN PART: true, but the gap is three days and part of it is content or M7b's | medium |
| 04-4 §28 kept for Spain, not for the Mediterranean | medium | STANDS IN PART | low to medium |
| 04-5 no collision; grappled hulls overlap | medium | STANDS | medium |
| 04-6 scope past the proposal's first target | medium | REFUTED as a fault (decision 49); stands as a cost | low |
| 04-7 the *Neufchatel* the wrong rig in §27 | medium | REFUTED as to the code: the file follows her sail plan; the spec is stale | low |

---

## spec-02

### 02-1. The true position reaches the browser through the log's data (high; sure)

**What I did.** Read `world/lookout.py:600-670`, `world/chart.py:455-475` (`Sighting.to_dict`),
`ui/server.py:347-353, 538-550, 916-921, 1520-1563`, `core/events.py:190-203`,
`world/knowledge.py:982-993` (`as_the_owner_sees`, which rewrites only the owner's world
orders), `agents/tools.py:183-198` (`log_line`), `agents/journal.py:75-79`, a grep of
`agents/mcp_server.py` for `data`, `to_dict`, `event_dict` (no hit), a grep of `client/` for
`bearing_deg`, `distance_m`, `.data`. Then rebuilt the reader's measurement with the test's
own helper (`tests/test_readings.py:687-708`, a brig at rest at 50.05 N 5.0 W, seed 7,
channel-west, 600 ticks), took each `lookout.*` event through `ui.server.event_dict`, as
`/api/log` sends it, and the feature's position from `api.queries.chart_block`:

```
true 50° 03' N, 5° 00' W
lookout.sighting the-manacles 263.3 3175  -> 50.04999 -5.0     text: The Manacles bearing W by S, distant two miles: a danger.
lookout.sighting manacle-point 275.8 4168 -> 50.04996 -5.0     text: Manacle Point bearing W by N, distant three miles.
lookout.sighting lowland-point 255.1 5170 -> 50.04996 -5.0
lookout.sighting nare-point 303.5 7392    -> 50.04996 -5.0
lookout.sighting coverack 247.2 7436      -> 50.04993 -4.99998
lookout.sighting penwin-and-vaze 278.1 2378 -> 50.04998 -5.0
```

Every sighting gives the true place to a few metres (a fifth of a second of latitude).

**Weighed exactly, as asked.**

- *Shown or only sent?* Only sent. The words of the line are the point and the eye's
  estimate ("W by S, distant two miles"). `client/log.js` reads `data` only for a roll-up's
  ticks (`log.js:62`), `client/app.js:480` only for the director's lines; `client/map.js`
  draws bearings from the snapshot's reckoning (`map.js:1006-1009`) and strangers from the
  snapshot's estimates (`map.js:1075-1090`), not from the log. A player sees the truth only
  by opening the browser's developer tools or calling `/api/log` by hand.
- *Does it reach a model?* No, by every road I found. `tools.log_line` gives tick, stamp,
  severity, kind, text and `by` (tools.py:183-198); the harness's brief, delta and
  `read the log` go through it (harness.py:1114, 1840, 1963, 5512-5523; tools.py:419); the
  journal's entries carry text only (journal.py:75-79); the MCP server gives "the log's own
  words" and touches no `data`. The `bearing of <mark>` reading a model can ask for gives the
  compass bearing with the compass's error and the lookout's estimate in words
  (`reckoning.Navigation.bearing_reading`, reckoning.py:5517-5536), which is fair.
- *Is a bearing and distance of a landmark by eye fair navigation, and at what precision?*
  Yes: a compass bearing and a distance by estimate or by a vertical angle is how a fix
  was got in sight of land. Fair precision is the compass's (a quarter point to a degree in
  the reading, with the compass's error of two or three degrees on it,
  `COMPASS_ALLOWANCE_DEG = 2.5`, reckoning.py:447) and a distance by eye of a fifth or so,
  or a few per cent by a sextant's vertical angle. The data is true to 0.1 degree with no
  compass error and to the metre. Note that even with `distance_m` struck, two marks' true
  bearings to 0.1 degree cut to a fix of tens of metres: the bearing must be rounded and
  given the compass's error too, as `_data` (lookout.py:654-669) already does for the
  snapshot.
- *Does any test guard this road?* Worse than none: a test pins the truth **into** the
  log's data. `tests/test_lookout.py:103` asserts
  `abs(lizard.data["distance_m"] - 10 * units.NAUTICAL_MILE) < 300.0  # the truth kept`.
  The proof test (`test_readings.py:724`) checks the readings' registry only.
- *Is it known?* Yes, twice in the specification: §17 says "the log's own line of a sighting
  keeps them for the record (`_line_data`), as it did" (TechnicalSpec-M5.md:798-800), and
  §33 item 25 that "if the log's data reaches the browser, it is a road the proof of §15
  does not cover" (1409-1411). The code comment says the log is "the author's and the
  tests'" (lookout.py:636-637); `for_the_record` does not treat it so (events.py:198-203),
  so the comment is false of the code.
- *The strongest defence.* `/api/save` hands the whole truth to the same browser in one
  GET (server.py:1557-1563), and the specification allows the truth in the save (§17). So
  the browser is already a road for a player who goes looking; scrubbing the log alone does
  not shut it. The proposal's words are "no true-position readout", and nothing reads it out.

**Verdict: STANDS IN PART.** The data is there, sent on every websocket line and every
`/api/log`, and recoverable to metres (confirmed). It is not shown, it reaches no model, and
the save is an equal and sanctioned road. **Weight medium**, not high: it does not spoil the
default game for a player who plays it; it breaks the specification's own proof "by any
road", and the one test that touches it holds it the wrong way. Cheap to mend (`_line_data`
to do what `_data` does, or `event_dict` to drop the truth's keys; a test over `/api/log`).

### 02-2. The captain's chart is the truth's; `chart: {year: 1804}` is read by nothing (high; sure)

**What I did.** `grep -rn "year: 1804" data/scenarios` (44 files, plus 1807 and 1808 once
each). Traced `papers:` through `world/scenarios.py:546-627`: the epitome and the
chronometer are taken out, the rest kept as `sc.papers` (line 627). Every reader of
`scenario.papers` or `world.papers` (`dealings.py:193`, `service.py:130`, `flags.py:533`,
`signals.py:1449, 1477`, `combat/marks.py:387`, `agents/tools.py:2835`) reads
`price_lists`, `service`, `private_signals`, `signal_books`; none reads `chart`. The
`Papers` class (`world/places.py:689`) has no mention of a chart or a year. The lead's cast
compares against `world.chart.depth_at(world.position)` (reckoning.py:2955-2958), the
truth tiles.

**Verdict: STANDS IN PART.** Confirmed: the year is accepted and ignored, and the chart the
master works by and the browser draws is the modern survey (spec M5 §11 line 315 and §17
line 793 promise "a separate product ... degraded", "a longitude error of the period's
chart"). What falls is "half of 'the two positions kept apart' is missing": the account and
the truth are kept apart, and a ship gets lost by her reckoning's errors as the proposal
asks (§5.2). The proposal itself does not ask for an erring chart; the specification does.
**Weight medium**: a specification's commitment not built and a scenario key silently
ignored in 46 files, with no word in the code that it is ignored.

### 02-3. The dockyard repairs nothing (medium; sure)

**What I did.** Read `dealings.py:2529-2560` (`demand`); counted the yard items in all port
files (`grep -rhn "item: " data/ports`: cordage 124, provisions 124, water 124, topmast 123,
yard 69, topgallant mast 52, suit of sails 47; no lower mast, no hull work); grepped
`freesail/` for repair, refit, careen, caulk: only the crew's evolutions
(`evolutions/repair_scripts.py`: plug, caulk, fother, fish, jury mast) and the rule
captain's choosing of them. Read the commitment itself: "the **dockyard** (repairs and stores
by the part graph: a spar, a suit of sails, cordage, water and provisions, with time and
cost ...)" (TechnicalSpec-M5.md:949-951).

**Verdict: STANDS IN PART.** The specification's own colon defines "repairs and stores" as a
spar, a suit of sails, cordage, water and provisions; that is what is built, and the crew
fits the spars. What stands: no yard hand touches the hull, and no port supplies a lower
mast, so a ship that loses a lower mast in action (M7) carries a jury mast for the rest of
the game and a shot hole stays a plug. That is M7's consequence more than M5's. **Weight low
to medium.**

### 02-4. The war is counted twice in the prices (medium; sure)

**What I did.** Read `ports.py:330-345, 400-453` (`WAR_FACTOR = 1.5` multiplied in
`Market.factors` whenever the good's origin is at war with the port's nation) and the rows:
`brest.yaml:70` tin 180, "English tin, scarce under the blockade"; `falmouth.yaml:98` brandy
200, "a smuggler's price while France is at war with us"; `falmouth.yaml:90` tin 120;
`brest.yaml:66` brandy 110. The arithmetic gives the reader's figures (180 x 1.5 = 270 at
Brest, 200 x 1.5 = 300 at Falmouth, season and supply at 1).

**Verdict: STANDS** for the tin, whose note gives the war as the reason for its price, then
multiplied for the war again. For the brandy it stands **in part**: a smuggler's price in
Cornwall had the peace-time duty behind it as well as the war, so part of the 200 is not the
war's. A British ship cannot trade at Brest (stance hostile), so the round trip is a
neutral's; the business's traders (`business.transact`) will run it. **Weight low to
medium**: two rows of data and a note per row to mend, but it is the kind of thing that
makes the market's one obvious trade wrong.

### 02-5. The crew pool never refills (medium; sure)

**What I did.** Read `dealings.py:2612-2665`: `pool["hands"] = have - taken` (2658); grepped
`freesail/` for other writers of `crew_pool` (only the read at 2635 and the loader,
`ports.py:718, 828`, dated rows); no impressment verb found in `orders/`. Falmouth's pool is
4 able, 8 ordinary, 12 landsmen (`falmouth.yaml:131-133`).

**Verdict: STANDS.** Nothing but a dated row in the file restores a pool. **Weight low** at
this milestone: the game's scenarios are passages and actions of days; it bites in a career
(M8) and when the business's ships are ever made to recruit.

### 02-6a. The chart eighty times the "modest sea", while most scenarios use two regions (medium; sure)

**What I did.** Read the proposal: "the first map is one modest sea area ... roughly a hundred
by a hundred miles" and, in the same sentence's heading, "build the world's mechanisms ...
and **grow the map**" (DesignProposal.md:305). Decision 39 commits the chart line to Madeira
and the Strait "whatever their size"; decision 44 launches the four last blocks and the
Azores; decision 49 calls the rest "mostly content, ships and charted area"; decision 67 asks
for "a very strong coverage as far as ports go". Then: `chart_holding`
(chart.py:911-925), called by `World.__init__` (core/world.py:775), turns `region:
channel-west` into the first chart of the manifest's `charts:` that holds it, which is
`atlantic-east`, all twenty regions (manifest `charts:`). Counted scenarios:
`find data/scenarios -name "*.yaml" | wc -l` gives 52 (not 69); 36 say `region:
channel-west`, 14 `chart: atlantic-east`. `git count-objects -vH`: size-pack 427.44 MiB;
`du -sh data/charts`: 359M.

**Verdict: STANDS IN PART.** The size is as measured, but it is the owner's ruling, four
times over, not a builder's overreach; "outgrown the plan" is true only of the first map.
"Most scenarios use two regions" is **refuted**: every scenario with a chart plays on the
whole twenty-region chart, because a region names where she starts on it. What stands is the
cost: a 427 MiB repository and 359 MB of tiles to clone for a maintainer. **Weight low** as a
fault of scope; **medium** as a maintenance cost the owner may not have priced.

### 02-6b. A Channel world loads all 121 ports and takes about six seconds to build (medium; sure)

**What I did.** Read `ports.py:1213-1225`: with no `ports:` in the scenario and a chart, every
file of `data/ports/` is loaded (121 files). Timed one build (the test's helper, brig,
seed 7, channel-west, a timed suite on the machine, load average about 4): **11.1 s**. Then
one build under `cProfile` (26.9 s profiled), whose cumulative times are: YAML parsing 26.0
of it in all; `chart.load_manifest` 6.2 (called **twice** per build: `load_chart`,
chart.py:901, and `chart_holding`, chart.py:919); `tide.load_tide` 6.7; `chart.load_chart`
8.8; `Ports.__init__` 4.1. `yaml.__with_libyaml__` is False: the pure-Python parser.

**Verdict: STANDS IN PART.** Every port is loaded, as the reader says; that follows from the
one whole chart above, and a channel-west world is in truth an atlantic-east world, in which
Algiers belongs. The build's time is not the ports' but the YAML parser's: the ports are about
a seventh of it, the manifest (398 KB, parsed twice) and the tide tables more. The chart is
cached per process (`_CHARTS`, chart.py:890-902), so the cost is paid at start and once per
test process. **Weight low** for a player (a start of ten seconds); a maintainer's suite pays
it per process.

### 02-9. The document is half history (medium; sure)

**Not tested further** than to confirm the two sentences quoted (§17's "as it did" over a
road §33 says is open; §31's promise against eighteen as-built paragraphs, which I did not
recount). **STANDS** on the reader's count; weight medium.

---

## spec-04

### 04-1. The fine control of the sails, named in the proposal's M7 line, is not built (high; sure)

**What I did.** Read §24 (TechnicalSpec-M7.md:1118-1127) and the proposal's M7 line
(DesignProposal.md:553: "settling the halyards, the vangs, a sail kept shivering by
command"). Grepped `freesail/orders` and `tests` for settle, sway up, shiver, spill,
flatten, check, ease, gybe, a `keep` prefix. Found:

- *the sheets checked or flattened by so much*: **built** before M7. `ease the spanker sheet
  two fathoms` (tests/test_staying.py:269), `ease the jib sheet` (test_lying_to.py:708);
  `verbs.py:1698-1746, 1849-1870` haul or ease a fathom of the fall, "a little",
  "handsomely"; `check` is a verb of a line (verbs.py:1746).
- *the yards by hand*: `brace the fore yards in a point`, held until the next trim, "the log
  says what shivers or fills" (verbs.py:850-858, package 37p). A yard can be braced to
  shiver and kept so; there is no order that names the shiver.
- *settle the topgallant halyards*, *sway up* (of a sail), a `settled` state: **not built**
  (`_settle_call` in verbs.py is the watch call's, not a halyard's; the only `sway_up` file is
  `sway_up_topgallant_masts.yaml`, the spar).
- *the vangs eased to spill a gaff sail*: **not built** (vangs exist for lateen and settee
  yards' trim, verbs.py:1582-1587).
- *the weather braces checked in a puff*, the `keep <x> <state>` prefix: **not built**.
- *the gybe as an evolution*: **not built**; the gybe is by the helm (navigation.py:449-611;
  grammar.py:253-260 makes "gybe the mainsail" a wear and refuses it in words).

**Verdict: STANDS IN PART.** Two of the eight items exist in a form from earlier packages;
the three the proposal's own line names (halyards settled, vangs, a shiver by command) do
not. M7 is open and iterative (decision 49) and its gate has not been passed, so "not built
yet" rather than "skipped". **Weight medium to high**: it is the only part of the proposal's
M7 line that is absent, and the specification has no word on when.

### 04-2. The gate as the specification writes it cannot be run at this commit (high; sure)

**What I did.** Read §29 and §30 (TechnicalSpec-M7.md:1256-1307), `world/seats.py:76`
(`ADVERSARIAL_SEATS_CONSENTED = False`), `world/prizes.py:1115-1160`
(`adversarial_seat_why`: a model at the captain's station of a hull at war with the nation of
the player's hull, or of the hull his person is on, is refused; the player's own hull is
skipped), `world/ships.py:2156-2182` (`Vessels.in_sight`: a sail is in sight if within the
horizon, the visibility and the night limit; no test of the land between). Grepped
`data/scenarios` for razee, seventy-four, hermaphrodite: none (eleven test files use them).

**Verdict: STANDS IN PART.**
- *The player struck to a model's ship*: blocked, confirmed, by a deliberate flag waiting on
  the consent revision (package 55).
- *7b's lugger behind the headland unseen*: blocked, confirmed: no sight across land at all.
- *7a*: "against a French frigate or a privateer under a model captain" can be read as the
  model in the *Indefatigable* (allowed: her own hull is skipped at prizes.py:1151-1152) or in
  the enemy (refused). Not decidable from the text; the reader took the stricter reading.
  "No scenario uses the *Indefatigable*" is true, but a scenario is a data file of minutes'
  work, not a missing build.
- *7c, 7d*: nothing found that stops them; the sub-gates "may pass separately" (§30).

So two of five items cannot run, one may not, two can. The blocks are known (§29 says so;
§5 says sight across land is 78's). **Weight medium**: the owner should know the gate's
"player struck" and 7b need two packages not yet run (55, 78), and that the spec says nothing
of an interim gate.

### 04-3. The specification stops at package 101; merged work runs past it (high; sure)

**What I did.** Packages named in commit subjects: 100, 101, 102, 104, 105, 106b, 109, 110,
111, 112, 114 (and 103, 103a, 106, 106a, 107 in bodies); in the specification: 101 only of
those over 100. `test_truth_7_` tests: 298, the highest 7-584. Merge subjects of 102 to 112
are dated 2026-11-13 and 2026-11-14: 102 the nations' days, 105 Sicily and Malta, 106a the
Canaries, 109 the director's dry run and the view, 111 "the audit's mends", 112 "the layers'
order".

**Verdict: STANDS IN PART.** True: the specification does not describe the last ten
packages or some 150 truths. But the gap is the last three days' work; much of it is chart
and port content (decisions 49 and 67 call that content) and 109 is the director's (M7b),
not this specification's. The worse part is that §32 forbids a new chart block "before the
gate's scenarios choose one", and the code and the owner's decision 67 have overrun that
sentence without the sentence being struck. **Weight medium**.

### 04-4. §28's rule kept for Spain and not for the Mediterranean states (medium; sure)

**What I did.** Read decision 64 (DesignProposal.md:877-887). Listed the nation keys of the
sampled tables by python: `hail.yaml` `navy`, `ports`, `lies` hold batavian-republic,
britain, denmark, france, morocco, portugal, spain, united-states; `parole` britain,
default, france, spain; `business.yaml` `prize_courts` britain, default, france, spain;
`marines.yaml` kits british, french, basic. `nations.yaml` has sixteen nations, eight of
them Mediterranean states; Spain's `marines: {kit: basic}` (line 159) has no source or note.
Read `world/hail.py:484-500`: no `ports` row gives "the port"; a lying ship with no `lies`
row is the "Nancy"; no `navy` row gives "the {kind} {name}". Business traders sail under
their port's nation (business.py:460), and Messina, Syracuse and Catania are Naples's,
Porto Farina Tunis's, so a Neapolitan or Tunisian hail is likely in play (not run).

**Verdict: STANDS IN PART.** The decision's firm duty is Spain's row "with its source or ...
in the tuning notes"; the Mediterranean factions are "where it can" and "the relevant".
Spain's marines on basic with no note in the data is a breach on the face of the file (the
tuning notes, which may record the search, I may not read). For the Mediterranean, the
prize-court `default` is an honest foundation; the hail table's gaps are the part a player
will meet: a Neapolitan answering from "the port", and lying as the English "Nancy".
**Weight low to medium.**

### 04-5. Collision is not built; grappled ships overlap (medium; sure)

**What I did.** Read `combat/boarding.py:1-11`; grepped `freesail/` for collision, collide,
stove, run aboard, fall aboard, fouled: only the boats stove by shot (`combat/hits.py:102-237`)
and two comments. No code judges two hulls meeting.

**Verdict: STANDS.** Two hulls pass through each other on the chart, grappled or not, and
the specification's §25 (built "even if the tuning nearly removes it from play", the
owner) has not begun. **Weight medium**: visible in the viewer at every boarding.

### 04-6. Scope run past the proposal's first target (medium; sure)

**Verdict: REFUTED as a fault.** Decision 49 makes M7 iterative, "M7 will expand as it goes";
the reader's own table shows nearly every item asked by the specification. It **stands as a
cost** to maintain. **Weight low**.

### 04-7. §27 has no as-built and calls the *Neufchatel* a schooner (medium; sure)

**What I did.** Read `data/ships/hermaphrodite-brig.yaml:1-25`: built from her lines and sail
plan at Greenwich (RMG ZAZ6177, ZAZ6179) and Winfield, "a brig's square foremast and a
schooner's main".

**Verdict: REFUTED as to the code**: the file follows the sources; the specification's word
is the stale one. The missing as-built and package 90's absent hulls stand. **Weight low**.

---

## Found on the way

1. **A second log line carries the truth.** `lookout.closing` builds its data from
   `s.to_dict()` raw (lookout.py:623), the true bearing to 0.1 degree and the distance to the
   metre, for every land, light or danger closing; the reader cited only `_line_data`. Any
   mend of 02-1 must cover both.
2. **A test pins the leak.** `tests/test_lookout.py:103` asserts the true distance is in the
   sighting's data ("the truth kept"). A mend will break it; it should be turned into the
   guard (nothing in `/api/log`'s data within a cable of the truth).
3. **Ships are seen through the land.** `Vessels.in_sight` (ships.py:2156-2182) tests the
   horizon, the visibility and the night limit only; a sail behind a headland or an island is
   hailed by the lookout through it. This is more than 7b's lugger: it is in every coastal
   game now.
4. **The build's time is the pure-Python YAML parser**, with the 398 KB manifest parsed twice
   per build (chart.py:901 and 919) and libyaml absent. A cache of the parsed manifest, or the
   C loader where present, would take seconds off every start and every test process.
5. **`region:` does not mean a region.** `region: channel-west` gives the whole twenty-region
   chart (chart.py:911-925, core/world.py:775), so the scenarios' key misleads a reader of the
   data, as it misled the first reader.

## What I did not do

Run any test; build more than two worlds; read `world/reckoning.py`, `world/lookout.py`,
`world/dealings.py` or `world/ports.py` whole; check the amplitude and azimuth road (02-8),
the levels of detail (02-7) or the open-item counts (02-9, 04-9); look at the tuning notes
the §28 rule names (forbidden); play a hail to a Neapolitan ship.
