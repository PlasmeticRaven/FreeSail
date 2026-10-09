# Milestone 6 work packages

The packages of `docs/TechnicalSpec-M6.md` (§28), briefed in turn for the owner's approval
and launched on his word. The head rules of `M5-WorkPackages.md` hold: the heavy design to
Fable and the standard work to Opus; a scenario's book tuned once and cheaply; the budget
the owner's; nothing under `docs/agents/consent/` or in `docs/agents/ConsentBrief.md`
touched but by the package the specification names for it (42); no model identifier in
any file of the repository; the recorded passages' constants re-pinned only where a change
moves them, with the old figure beside the new and the reason in the tuning notes, and a
passage that moves for a reason the package cannot give a finding, not a pin; the fast
tier run before the report and the slow tests of the passages touched; a section in the
tuning notes and a report to the lead at the end.

## Waves

| Package | Builder | What | State |
|---|---|---|---|
| 38 | Fable | The chart stitched: many regions over the corridor, the queries across edges, the climatology's boxes, the tide's gauges, the recipe form for the blocks | launched 2026-10-09 |
| 39a to 39f | Opus | The six blocks of the voyage to Madeira and the Strait | after 38 |
| 40 | Fable | The ship's company and the rules-based captain in three layers; the captain's station; the officer's reckoning | brief to write |
| 40b | Opus | The lessons in the primer | brief to write |
| 41 | Fable | The wardroom: several doors, the pace rule, the deck's conversation, the master's and the lookout's stations, the stand-by on several conditions | brief to write |
| 42 | Opus | The API door and its security pass; the transcript-driven replay; the consent brief revised once | brief to write |
| 43 | Fable | The crewed promotion, a model captain of another ship, the far-detail guard, the director's seat hook | brief to write |
| 43b | Opus | The lugger and the smack; the world's business | brief to write |
| 44 | Opus | The regatta harness and the parity tests | brief to write |

Package 37m (the helm through the wind) is milestone 5's last, briefed in
`M5-WorkPackages.md`, launched beside 38 on 2026-10-09 and merged after it: 38 moves no
recorded passage, 37m moves several.

## Package 38: the chart stitched (`freesail/world/chart.py` for the chart as the whole manifest, the finest tile under a point across every region and the fall back to the corridor and the world, the features of every region indexed together; `freesail/world/geo.py` if a function needs the sphere beyond one region; `freesail/world/scenarios.py` and `freesail/core/world.py` for `chart:` beside `region:`; `freesail/world/lookout.py`, `ground.py`, `reckoning.py`, `orders/navigation.py`, `api/queries.py` only where a caller assumed one region; `freesail/world/tide.py` and `data/tides/*.yaml` for gauges and streams over a larger table; `freesail/world/weather.py`, `weather_script.py` and `data/weather/climatology.yaml` for the boxes; `tools/build_charts.py` for the corridor, the recipe form and the blocks' checks; `data/charts/` for the corridor's tiles and the manifest; `docs/TechnicalSpec-M6.md` §26 as built; `docs/design/ChartData.md` a note; `docs/references/Charts.md`; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_geo.py`, `test_lookout.py`, `test_tide.py`, `test_weather.py`, `test_scenarios.py`, `tests/test_known_truths.py` only to prove nothing moved)

Spec M6 §26 whole, with the study `docs/design/ChartData.md` §5 and §6 (the levels, the
files, the disk, the build, the queries per tick) and spec M5 §9 to §12 and §16 for what
the chart, the lookout and the tide are today; the owner's chart goal of 2026-10-09
(decision 39, ruling 4 and 5: the Strait as a sixth block, the regions committed whatever
their size). On Fable, since the runtime's one-region assumption runs through the world's
code and the weather's seeding must not move a recorded passage. Launched 2026-10-09
beside 37m; merged first.

What to build:

1. **The chart is the whole manifest.** `load_chart` takes a chart name (`atlantic-east`,
   the manifest's new top-level `charts:` naming the regions it holds and the corridor
   under them) or, as now, a region's name, which is a chart of that one region (every
   scenario and test today keeps working unchanged). A query asks the finest level that has
   a tile under the point across every region of the chart, falls back to the corridor at
   level 1 and the world at level 0 where either is built, and answers None beyond them as
   now. The features of every region are loaded and indexed together, their names unique
   across regions (a clash is an error at load, said in words). `Chart.contains` and
   `bounds_words` speak of the whole. The queries' names and signatures do not change:
   37m's branch, built beside this one, calls them.
2. **No seam.** The lookout, the dangers on a shaped course, the nearest land, the
   grounding, the depth under the keel and the anchor's ground work across a region's edge
   and over the corridor without a seam: a test sails a fake across an edge and over the
   corridor's water and finds no step in the depth, no danger lost and no landfall said
   twice. Where the corridor's 30" cells are the finest, the lookout's words are honest
   about it ("the land" at a headland's scale, no rock by name), by the level's `use`.
3. **The corridor.** Level 1 from GEBCO over 32°N to 51°N and 20°W to 1°W, built by the
   tool (`--corridor`, a region-like recipe with the fetch bounds and the datum, mean sea
   level as the level has it) and **committed** (about 2,300 by 2,300 cells, some 11 MB
   raw; the owner's ruling 5), with the manifest's record of the source, the licence and
   the checksum as for every tile; `.gitignore`'s rule for `tiles/1/` gives way for the
   corridor's tiles alone (name them or move them), the Atlantic beyond it still fetched
   and not committed. The fingerprint of the rules takes the new files as it takes the
   rest.
4. **The weather's boxes.** `data/weather/climatology.yaml` gains boxes: the Channel's as
   it is, unchanged in every figure and in its name, and three more, PROVISIONAL from the
   same kinds of source and marked so (Biscay; the Portuguese coast with the summer
   northerlies, the Portuguese trades; the sea off Madeira with the north-east trade), with
   the sources named or "judgement" per row as the Channel's rows are; a scenario's weather
   is seeded from the box she starts in, and the systems in play blend at a box's edge by
   the study's rule (W §5) or a stated simple one. **Nothing in the Channel moves**: the
   recorded passages and the gate's day replay to their digests, which is the package's
   first test and the merge's condition.
5. **The tide's table over a larger sea.** `constituents.yaml` and `establishments.yaml`
   take gauges and places beyond the Channel as the blocks will add them, the interpolation
   between gauges honest about distance (a position far from every gauge gets the nearest
   with its doubt said in the master's words, not a blend across a coast), and `streams.yaml`
   takes areas by chart; the eleven gauges and their figures unchanged.
6. **The recipe form and the blocks' checks.** `REGIONS` in `tools/build_charts.py` as the
   form each block fills (bounds, fetch, harbours, the sources' names), a `--region` build
   that leaves every other region's tiles untouched, and the checks a block must pass,
   printed by the tool: the allowed-licence test, the shore swept for GEBCO's fill (M5 §33
   item 16), features within the region's bounds and unique across the manifest, every
   feature's source in the references' form, the harbour patches' datum stated. A short
   `docs/dev/ChartBlocks.md` says how a block is built, for the six Opus packages to follow
   (39a to 39f), with the Channel east block's bounds and sources as the worked example.
7. **The ships' plans and the pilots' stations** need nothing new; say so after checking,
   or say what did.

Tests for each; the whole suite's passages unchanged to the digest. Where the corridor's
build cannot be fetched from this machine, say so and leave the recipe and its tests on
a small synthetic corridor, the fetch for the lead or the owner to run; do not commit a
corridor that was not built from the source named in the manifest.
