# How a chart block is built

For the six packages of milestone 6's chart line (39a to 39f: the Channel east, Biscay
north, Biscay south and Galicia, Portugal and Cadiz, Madeira, the Strait; spec M6 §26),
each a region on the pattern of package 35b (Roscoff's patch, the port file, the tiles
rebuilt) and of package 32 (the Channel west region whole). Package 38 made the chart
the whole manifest, so a block adds a region beside the others and touches nothing of
theirs: its tiles are built alone (`--region`), its features are indexed with every other
region's, its tide and its weather are rows in tables that already reach its water.

## What a block is

1. **The recipe**: an entry in `REGIONS` of `tools/build_charts.py`, the form every key
   of which is read (the comment above `REGIONS` says what each does): `title`, `bounds`
   (the region's box in degrees; the level-2 tiles that meet it are built whole, and the
   block's features must lie within it or within one of its harbour patches' boxes),
   `fetch` (the EMODnet subset: it must cover **the tiles** whole, not the bounds; a
   level-2 tile is 0.43° across, so the tiles reach past the bounds by up to that, and
   the harbour patches' level-3 tiles too: `--check` says whether the box covers them,
   package 39a's first box missed Dartmouth's by a fifth of a degree), `harbours` (the
   level-3 patches as boxes, about 15′ by 15′ each, one per port of the block, named as
   the port file's road and the override name them), `sources` (the ids of `SOURCES` the
   tiles are cut from, in the order they are laid: EMODnet for the depth and the coast,
   GEBCO under it), and `fill_to_chart_datum: true` for every block from 39a on (below,
   "GEBCO's fill"). A source not yet in `SOURCES` (Tofiño's sheets are period data, not a
   source of the tiles; a modern grid beyond EMODnet's reach would be) is added there
   with its licence id, which must be in `ALLOWED_LICENCES`, and the licence text under
   `docs/references/licences/`.
2. **The region in its chart**: the region's name appended to `CHARTS["atlantic-east"]["regions"]`,
   in the order the voyage sails them. The manifest's `charts:` lists the regions that
   are built; a region named and not built is listed under `regions_not_built`.
3. **The features file** `data/charts/features/<region>.yaml`, in the form of
   `channel-west.yaml` (its head says the rules: positions in the modern frame, checked
   against the coast and the shoalest cells; heights for the horizon; a light's `lit`
   dates; `dries_m` for a danger's head; `says` the line the log can say). Every id is
   unique across the manifest (`check_region` refuses a clash), every source in the
   references' form (`docs/references/README.md`: a work and its year, a section and a
   page; or a named modern reference), and the lights dated so that 1805 sees what 1805
   had.
4. **The overrides** under `data/charts/overrides/<region>/`, one file per harbour patch
   read from a period sheet, each stating its `sheet`, its `source`, its `units`
   (fathoms, feet, brasses, metres), its `datum` in words and `datum_above_chart_datum_m`
   (the sheet's low water above the chart's LAT, in metres, from the modern tables or
   marked unverified), its `control_points` with their residuals, and its `patches`
   (depth, drying, land, sea polygons).
5. **The port files** `data/ports/<port>.yaml` on package 35's machinery, with the road,
   the pilot's station, the nation and the port's state (Cadiz blockaded is a state of a
   port, M6 §26); the nations index `data/nations.yaml` where a nation is new (Morocco,
   for Tangier), and every new port in its `ports:` index (`tests/test_nations.py` reads
   the index against the files). **Every spot that names a feature repeats its
   `lat_deg` and `lon_deg`**: a scenario with no `ports:` list (the gate-5b passages)
   loads every port file on its own region's chart, which has not the block's features,
   and a spot with a feature and no position is refused at load. A port of a block is
   loaded into the Channel's recorded passages that way: it moves no digest only while
   it is nowhere nearer to their tracks than the ports they had (the pilot and the
   readings take the nearest port), which a block far down the voyage is, and the
   Channel east was (package 39a). Where no period sheet is read for its harbour the file
   says `datum: unverified` (a top-level key the machinery does not read).
6. **The tide**: the block's gauges in `data/tides/constituents.yaml` (TICON's file,
   `TICON.txt` as package 34 read it, holds the Iberian and the Madeiran gauges by their
   coordinates: which of Vigo, Leixões, Cascais, Lagos, Cadiz, Tarifa and Funchal it
   has is **unverified** here and read when the block is built; the form is the
   eleven's: the record, the mean level above the chart's datum with its source, M2, S2
   and N2) and its
   stream areas in `data/tides/streams.yaml`, each with `chart: <region>` and, for an
   area with no polygon, `bounds:`; the places of the master's epitome in
   `establishments.yaml`, Norie's and Moore's, with `rise_judgement` where the period gives
   no rise. The eleven gauges and their figures do not move. **A new gauge moves every
   Channel position's tide**: the blend is over every gauge within `reach_nm` (400 miles,
   the Channel's whole region), so a twelfth gauge however far changes the tide off
   Falmouth by a little and the recorded passages' digests with it. Package 39a read
   Bournemouth and Portsmouth from TICON and **held** them (`held_gauges:` in the file,
   read by nothing) for the lead's decision; a block in Biscay or beyond is more than
   400 miles from much of the Channel but not from all of it (Brest to the Gironde is
   about 260): measure before adding, or hold. The stream areas go before the open
   Channel's (`mid-channel`, whose bounds hold the Channel east and Biscay's north), in
   water no recorded passage reaches, and `book_limits` grows to take the block's water
   (a single box: 39a took it east to 1 W). `tests/test_tide.py` holds every book
   statement to the period's form (the set to a point, the springs to the half knot, the
   neaps half the springs unless the period gives both rates, `PERIOD_RATES`).
7. **The weather**: nothing, unless the block's water lies in no box of
   `data/weather/climatology.yaml` (the four boxes cover the corridor whole); a block
   that reads a printed climatic table replaces a PROVISIONAL row and says so in the
   row's `note`.
8. **A scenario** `data/scenarios/<block>.yaml` that sails the block's stretch (a free
   passage, not a gate's), with `chart: atlantic-east` and a position in the region.
9. **The build**: `python tools/build_charts.py --region <region>` fetches the sources
   into `.cache/charts` (the network through the proxy reaches GEBCO's and EMODnet's
   services), builds the region's tiles at levels 2 and 3 and its coast and index,
   prints the checks (below), and writes the manifest with every other region, the
   corridor and the sources' earlier fetches carried over as they were. The tiles are
   committed (the owner's ruling 5; a region is about 18 MB).
10. **The tuning notes' section** and the report to the lead, as every package.

## The checks a block must pass

Printed by `python tools/build_charts.py --check <region>` without fetching (and at
every build of the region), each line saying what passed and `FAILED:` what did not,
the tool refusing to build on a failure:

- **the allowed-licence test**: every source the recipe names is in `SOURCES` with a
  licence in `ALLOWED_LICENCES` (public domain, CC BY 4.0, Licence Ouverte 2.0, OGL 3.0,
  LGPL 3.0, the named Histolitt permission; never ODbL);
- **features within the region's bounds**: every feature's position inside `bounds`;
- **ids unique across the manifest**: no feature id of the block is in any other
  region's file;
- **every feature's source in the references' form**: a work and its year, or a named
  reference (Trinity House, an encyclopaedia page with its date read, the modern chart,
  the study, an RMG or SHOM record);
- **the harbour patches' datum stated**: every override has `datum` and
  `datum_above_chart_datum_m`;
- **the fetch box covers the tiles whole** (package 39a): the level-2 tiles that meet
  the bounds and the harbours' level-3 tiles, the seam's column included;
- **the seam** (package 39a; at the build): `tiles another region lists: n kept`, the
  tiles of the block's lists that another region of the manifest lists, which stay that
  region's;
- **the shore swept for GEBCO's fill** (spec M5 §33 item 16): at the build, the cells
  where EMODnet has nothing and GEBCO's fill reads water shallower than three metres,
  clustered and printed largest first, for the block to patch (a town, an islet) or to
  say are water (with the fill raised to the datum, below, what is left is mostly real
  water EMODnet lacks: the Channel east's ten largest were Poole, Christchurch,
  Portsmouth and Langstone harbours, the Fleet behind the Chesil Beach, and the foot of
  Sark's western cliffs).

## The seam, and GEBCO's fill (package 39a)

**The seam.** The level-2 tiles are on one grid for every region (a tile's corner is a
whole multiple of 1,536″ from 90 S and 180 W), so a region's edge column may meet its
neighbour's bounds too: channel-west's easternmost column runs from 3.36 W to 2.93 W.
A tile another region of the manifest lists is that region's: the block's build computes
it with its own block (so that the distance field knows the shore across the seam:
Lyme's cliffs lie in channel-west's column, a cable from channel-mid's first) but
neither writes it, lists it nor draws its coast (`tiles_listed_elsewhere`, where the
region's tile lists are made; `_build_level`'s `taken`). The neighbour's tiles and its
manifest entry are not touched, and `git status` shows it: nothing of channel-west's
changed when channel-mid was built. The other side of the seam is the neighbour's: its
field knows only its own block, so within a cable or two of the seam it may give a
shore farther than the true one, until the neighbour is rebuilt (a finding, not a fix).
Abut the bounds on the neighbour's (3 W, 48 N) rather than overlapping them: the
features of the two then never share a box, and a query takes the one tile there is.

**GEBCO's fill.** Where EMODnet has no value (the land, mostly, and some harbours and
lagoons it does not survey) the tiles take GEBCO's height, which is about mean sea level,
while the levels are about LAT. Read against LAT that height is low by mean sea level's
height above LAT: at St Malo, where that is 6.8 m, the low land behind the town and the
marshes of the Cotentin read as drying ground under three metres, and were covered at
high water. A recipe with `fill_to_chart_datum: true` raises the fill by the world's own
mean level there (`mean_level_grid`: the tide table's gauges blended as the tide blends
them), so that a low shore stands as high above the world's high water as it does above
the sea's; the sweep's suspects fell from 37,348 cells to 2,772. Channel-west's recipe
has not the key, so its tiles, if rebuilt, come out as before (the Roscoff town patch
was the same fault mended by hand). Every block on a coast of large tides sets it.

A block's test file asserts the same of its own files through `tests/test_chart.py`'s
helpers (the manifest's licences, the sources cited), and adds the block's own truths:
a landfall on its coast by day and by night, a depth in its road, a tide at its gauge
within the atlas's figure, the scenario sailed to a digest.

## The worked example: the Channel east block (`channel-mid`, package 39a, as built)

The recipe as built (the outline in spec M6 §26 had the west bound at 4 W, overlapping
channel-west by a degree, and the south at 49 N, leaving St Malo out; the brief abutted
the block on channel-west at 3 W and the build lowered the south to 48.5 N):

```python
"channel-mid": {
    "title": "The Channel east, Lyme Bay to the Needles, the Channel Islands and St Malo",
    "bounds": {"south": 48.5, "north": 51.0, "west": -3.0, "east": -1.0},
    "fetch": {"south": 48.15, "north": 51.30, "west": -3.70, "east": -0.70},
    "harbours": {
        "dartmouth-torbay": {"south": 50.30, "north": 50.50, "west": -3.62, "east": -3.47},
        "portland-weymouth": {"south": 50.50, "north": 50.64, "west": -2.50, "east": -2.38},
        "guernsey": {"south": 49.40, "north": 49.52, "west": -2.60, "east": -2.42},
        "jersey": {"south": 49.15, "north": 49.23, "west": -2.22, "east": -2.05},
        "alderney": {"south": 49.68, "north": 49.75, "west": -2.28, "east": -2.15},
        "st-malo": {"south": 48.60, "north": 48.70, "west": -2.12, "east": -1.98},
    },
    "sources": ["emodnet_dtm_2024", "gebco_2025"],
    "fill_to_chart_datum": True,
},
```

**A neighbour's water.** Dartmouth and Torbay (3.5 W) and Morlaix (3.83 W) lie in
channel-west's bounds. Where channel-west lists no level-3 tile the block may patch the
harbour and keep its marks in its own features file (the bounds' check takes a harbour
patch's box as the block's): Dartmouth and Torbay are channel-mid's, their marks never
read by a scenario on channel-west's chart alone, which keeps the recorded passages'
digests safe. Where the block patches nothing (Morlaix) the marks go in the
neighbour's features file, which is data and no tile; but **the neighbour's index**
(`features/<region>.index.json`) is then stale, and the runtime reads the index when it
is present (`Chart.__init__`): the marks are found by id (a port's spots) and not by the
lookout until the index is rebuilt. The brief forbade touching channel-west's index, so
package 39a left it and reported it: a decision for the lead (rebuild the index, one
file, which moves no digest while the marks are out of every recorded passage's sight;
or make the runtime index a feature its region's index lacks).

**The period data, as read.** Bellin's 'St Malo et environs' (Petit Atlas Maritime t. V
no. 44, Rumsey 6903.531) at full resolution through the IIIF server: a harbour plan,
georeferenced by five control points (residuals 71 to 102 m), the road and the Rance's
mouth patched at his soundings; his sheets of the islands (t. V nos. 39 and 40, Rumsey
6903.526 and .527) are coastal charts at four common leagues to the scale, with no plan
of a road, and no patch rests on them. Mackenzie's survey of the coast east of Plymouth
was not found from this machine (the RMG's collection search answered the keywords
with unrelated objects); Dartmouth's patch rests on Imray 1874's depths in the Dart,
which EMODnet's grid smooths to two or three metres. The directions are Faden 1793 (in
period exactly, with Captain Dobree's directions for the islands), White 1835 (his own
survey of the islands from 1813) and Imray 1874; the lights' dates from Trinity House's
pages and the French encyclopaedia's (the Casquets 30 October 1724, Portland 1716, the
Needles' cliff-top tower 29 September 1786, Hurst 29 September 1786, Barfleur November
1775, Fréhel November 1702; the Start 1836, Berry Head 1906, St Catherine's 1838, Anvil
Point 1881, Alderney 1912 not yet). EMODnet's grid has no breakwater at Portland, Braye
or St Peter Port and no barrage across the Rance: at its sixteenth of a minute the
modern works are not in it, so the 1805 roads need no patch to remove them; what a
patch is for here is a depth the grid smooths (the Dart) or that has changed (the
Rance's mouth, four metres deeper in Bellin's day).

**The tide, as read.** TICON's file holds, in the block's water, Weymouth, St Helier,
Saint-Malo and Cherbourg (four of the eleven, their figures again to the centimetre) and
Bournemouth and Portsmouth (held, above); no gauge at St Peter Port, Dartmouth or
Portland. The streams of the Race and the Swinge are White's own (half-ebb to half-flood
south-westward, seven knots and more at springs); the Russels' hour Faden's; Portland's
hour Bowditch's; the rest judgement, marked.

What the block need not do: nothing of `freesail/` changes for a block, unless its
water wants a rule the engine lacks, which is a finding for the tuning notes and the
lead, not a patch in the block.
