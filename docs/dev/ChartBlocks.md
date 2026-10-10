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
   level-2 tile is 0.43° across, so the tiles reach past the bounds by up to that where
   the tile grid falls badly, and the harbour patches' level-3 tiles too: a quarter of a
   degree is not always enough, and `--check` says whether the box covers them; package
   39a's first box missed Dartmouth's by a fifth of a degree, and Biscay north's southern
   row starts 0.32° below its bound, package 39b), `harbours` (the level-3 patches as
   boxes, about 15′ by 15′ each, one per port of the block, named as the port file's road
   and the override name them), `sources` (the ids of `SOURCES` the tiles are cut from,
   in the order they are laid: EMODnet for the depth and the coast, GEBCO under it), and
   `fill_to_chart_datum: true` for every block from 39a on (below, "GEBCO's fill"; Biscay
   north, package 39b, was built beside 39a and without it, and wants a rebuild with it);
   with it, `fill_mean_level_m` where the block's gauges are held (package 39d: the
   world's mean level over a held block is a far gauge's, Le Conquet's 4 m over Portugal
   against the coast's 2, and raising by it turned the estuaries EMODnet lacks, the
   Guadalquivir to Bonanza, the Odiel, the Arade, into ground above low water; the
   figure is the block's own from its sources, said in the recipe's comment); and
   `skip_dry_tiles` where half the block is inland (package 39d: Portugal's 72 level-2
   tiles of Iberian land, 7.6 MB of its 21.7, have no water and are computed for the
   field and not written; the corridor answers there). The units of an override are
   `UNIT_M`'s; Tofiño's Spanish sheets are in `brazas` (six pies de Castilla, 1.6718 m,
   package 39d).
   A source not yet in `SOURCES` (Tofiño's sheets are period data, not a
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
   had. A danger's `extent_m` is a radius within which its head stands solid
   (`Chart.danger_under`: a ship within it with less water over the head than she draws
   is aground), so it is kept under a kilometre and laid over the foul ground itself, not
   over the water beside it (the Channel's largest is the Seven Stones' 1,500 m; package
   39b's first draft gave the Four of the Croisic five kilometres and the Boyart four,
   which closed the channel all ships take into the road of Aix). A mark that lies in
   another region's bounds goes in that region's features file, and is **not indexed**
   until that region's `index.json` is rebuilt from its file: the index is the other
   region's, which a block's build never writes; until then the mark is found by name
   and the lookout does not see it (39a's marks of Morlaix and 39b's of the Raz de Sein
   in `channel-west.yaml`; the lead rebuilt its index from the file at their merges,
   `build_index` over its features, and its counts in the manifest, no tile or coast
   touched).
4. **The overrides** under `data/charts/overrides/<region>/`, one file per harbour patch
   read from a period sheet, each stating its `sheet`, its `source`, its `units`
   (fathoms, feet, brasses, metres), its `datum` in words and `datum_above_chart_datum_m`
   (the sheet's low water above the chart's LAT, in metres, from the modern tables: a
   number, which the check refuses when it is absent, since package 39b; before, a
   missing key was read as nought and passed), its `control_points` with their residuals,
   and its `patches` (depth, drying, land, sea polygons). Where the datum's height cannot
   be read, there is no patch: the port file says `datum: unverified` instead. SHOM's
   Références Altimétriques Maritimes are readable from the build network as the WFS
   layer `RAM_BDD_WLD_WGS84G_WFS:ram_3857` of `services.data.shom.fr/INSPIRE/wfs`
   (GeoJSON, every station's NM, PMVE, BMVE; Licence Ouverte 2.0): the French and
   Biscay datums are read from it, not from memory.
5. **The port files** `data/ports/<port>.yaml` on package 35's machinery, with the road,
   the pilot's station, the nation and the port's state (Cadiz blockaded is a state of a
   port, M6 §26: `state: blockaded` with `blockade: by:`, `station:`, `since:` and
   `source:`, package 39d, closed to the blockaders' enemies, listed by
   `Ports.blockades()` for 6c's world's business; a scenario's `ports:` entry lays or
   lifts one); the nations index `data/nations.yaml` where a nation is new (Morocco,
   for Tangier). **Every spot that names a `feature:` repeats its `lat_deg` and
   `lon_deg` beside it**: a scenario with no `ports:` list (the gate-5b passages) loads
   every port file on the Channel's chart alone, where the block's features are not, and
   the spot falls back to its own position (without it the load is refused, and every
   such passage with it). A port of a block is loaded into the Channel's recorded
   passages that way: it moves no digest only while it is nowhere nearer to their tracks
   than the ports they had (the pilot and the readings take the nearest port), which a
   block far down the voyage is, and the Channel east was (package 39a). Where no period
   sheet is read for its harbour the file says `datum: unverified` (a top-level key the
   machinery does not read). The port is entered in the ports' index of
   `data/nations.yaml` (`ports:`, which `tests/test_nations.py` holds equal to the
   files), and `tests/test_ports.py` names the port files in a list: the block adds its
   own to both. Every road, anchorage and mooring has a note of the bottom (an anchorage
   or a bottom feature with `bottom:`) within three kilometres (`test_tackle_orders.py`,
   on the whole chart), and every book the game ships names places of the whole chart
   (`test_log_lines.py`).
6. **The tide**: the block's gauges read from TICON's file (`TICON.txt` in the zip at
   doi.pangaea.de, as package 34 read it, by their coordinates; which of Vigo and
   Tarifa it has is **unverified** here and read when the block is built (package 39d
   read Cascais, Lagos, Huelva, Bonanza and Cadiz, and found no Leixões, Lisbon or
   Setúbal; package 39e Funchal, Ponta Delgada, Angra, Horta and Santa Cruz das Flores);
   the form is the eleven's: the record, the mean level above the
   chart's datum with its source, M2, S2 and N2), **held** under `held_gauges:` in
   `data/tides/constituents.yaml` and not in `gauges:`, each block's after the last
   (package 39a's Bournemouth and Portsmouth, package 39b's nine of Biscay north, package
   39e's five of the islands, which no Channel position's reach meets). **A new
   gauge moves every Channel position's tide**: the interpolation blends every gauge
   within `reach_nm` (400 miles, the Channel's whole region) of a position, so a gauge
   added to `gauges:`, however far, enters the blend at Falmouth and moves every recorded
   passage's digest (Brest to the Gironde is about 260 miles); until the engine gives a
   gauge its own water (a reach or a chart of its own: the lead's decision, the finding
   of 39a and of 39b), the block's gauges wait there, read and verified, and the world's
   tide over the block is the eleven's blend, which over Biscay is the Channel's tide and
   wrong. The stream areas in `data/tides/streams.yaml`, each with `chart: <region>` (and,
   for an area with no polygon, `bounds:`) and its `book:` in the period's form
   (`tests/test_tide.py` holds every statement to it: the set to a point, the springs to
   the half knot, the neaps half the springs unless the period gives both rates,
   `PERIOD_RATES`), are looked up first-match: an area within another's polygon goes
   before it (the Raz before the Iroise), and the block's areas go before `mid-channel`,
   whose statement in the directions has no polygon and answers within its own
   `bounds:` (package 39d; it had answered for every position within the limits).
   `book_limits` is a list of boxes since package 39d, each block appending its own (39a
   took the first box east to 1 W, 39b south to 45.9 N and east to 0.9 W; one box over
   the Channel and Portugal would have taken in the Western Approaches west of 7 W and
   Biscay south between): give the block an area over its whole box (Portugal's
   `portuguese-coast`, after its bars and rivers) so that no position of the box is
   without a statement. Keep the polygons off the water
   the recorded passages' other sail use (the naval cruise's Diamond within eight miles
   of 48 N 4 55 W and Harpy within ten of 47 50 N 6 W; the merchant passage's Palinure
   from the Raz and Hirondelle from Sein), or their digests move with them. The places
   of the master's epitome in `establishments.yaml`, Norie's and Moore's, with
   `rise_judgement` where the period gives no rise: such a rise is the world's spring
   range at the place to the foot (`test_tide.py` holds it), which over a block whose
   gauges are held is the Channel's blend and not the place's own. The eleven gauges and
   their figures do not move.
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
   corridor and the sources' earlier fetches carried over as they were (since 39a and
   39b each source's records of the files this run did not fetch are kept before this
   run's: a `--region` build had dropped the corridor's GEBCO extract and the other
   regions' subsets, the Channel's GEBCO extract among them). **The seam** (below): a
   tile another region of the manifest lists is that region's, and the build neither
   writes it again, lists it nor draws its coast (`tiles_listed_elsewhere`). After the build
   `git status` shows no change to any tile, coast or index file another region lists.
   The tiles are committed (the owner's ruling 5; a region is about 12 to 18 MB, but a
   region that is mostly open sea costs more: the Azores' 153 level-2 tiles are 40 MB,
   package 39e, below). **Every tile is written by `save_tile`** (package 39e), its zip
   entries dated alike, so that the same arrays give the same bytes: from 39e on a
   rebuild's byte-identity means array-identity, and a tile that changed in its bytes
   changed in its arrays. The tiles written before it keep their bytes (numpy's
   `savez_compressed` dated each entry with the clock) until they are rebuilt.
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
  `datum_above_chart_datum_m`, a number (since package 39b: before, a missing key was
  read as nought and passed);
- **the fetch box covers the tiles whole** (packages 39a and 39b): every level-2 tile
  that meets the bounds, the seam's included, and every harbour's level-3 tile lies
  within `fetch`;
- **the tiles another region lists** (packages 39a and 39b): how many of the block's
  tiles another region of the manifest lists, which stay that region's, not written and
  not listed (`tiles another region lists: n kept`, at the check by level and again at
  the build);
- **the shore swept for GEBCO's fill** (spec M5 §33 item 16): at the build, the cells
  where EMODnet has nothing and GEBCO's fill reads water shallower than three metres,
  clustered and printed largest first, for the block to patch (a town, an islet) or to
  say are water. With the fill raised to the datum (below) what is left is mostly real
  water EMODnet lacks: the Channel east's ten largest were Poole, Christchurch,
  Portsmouth and Langstone harbours, the Fleet behind the Chesil Beach, and the foot of
  Sark's western cliffs. On a low coast it finds the marshes and the lakes behind the
  shore (Biscay north: the Brière, the lake of Grand-Lieu, the Marais poitevin), closed
  from the sea and left as water, said in the notes; Biscay north, built without the
  raise, also shows the fault the raise mends: GEBCO's land, its heights above mean sea
  level read as above LAT, stands as ground that dries, and at high water springs the
  model floods the marsh behind a dyke.

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
Biscay north's recipe (package 39b, built beside 39a) has not the key either: its
sweep found 34,053 cells in 267 places, the marshes behind its dykes among them, which
flood at high water springs; the rebuild with the key is the lead's to order.

**Blocks built at once (packages 39c to 39f).** The neighbours' seams fall inside a
row of tiles: Portugal's northern row (41.84 to 42.27 N) and southern row (36.29 to
36.72 N) straddle Biscay south's 42 N and the Strait's 36.4 N. Built in parallel, neither
neighbour is in the manifest, so each block writes the row's tiles and lists them (four of
them both Portugal's and a neighbour's: `2/150624_-32064` and `-33600` with Biscay south,
`2/130656_-22848` and `-24384` with the Strait); at the merge the
lead keeps one listing (the seam rule makes the first region in the manifest the owner),
and the files of the other block's copy of those tiles are dropped. The copies differ
only by each block's distance field, its patches and its fill level. A mark across a
neighbour's bound goes in the report for the lead, not in a file that does not exist yet
(Portugal's Sancti Petri, Cape Roche and Trafalgar are the Strait's).

**The sources' reach from the build network (package 39d).** Wikimedia's API refuses
the build network for its rate (429, minutes at a time) when several packages ask at
once; the encyclopaedia's pages were read one by one through the session's own web
reader instead. The Internet Archive serves Tofiño's *Derrotero* (1789) in three OCR'd
copies and his *Atlas Marítimo* (the Universidad de Sevilla's copy, `A062039040`,
Public Domain Mark) at full resolution through its IIIF service
(`iiif.archive.org/iiif/<item>$<page>/<x,y,w,h>/<width>,/0/default.jpg`, the v3 path
answering 404). Puertos del Estado's REDMAR reports (`bancodatos.puertos.es/BD/informes/
globales/GLOB_2_3_<station>.pdf`, the stations' codes in `INT_3.pdf`) give a Spanish
gauge's mean level and LAT above its zero: the datum's height for a Spanish patch.

A block's test file asserts the same of its own files through `tests/test_chart.py`'s
helpers (the manifest's licences, the sources cited), and adds the block's own truths:
a landfall on its coast by day and by night, a depth in its road, a tide at its gauge
within the atlas's figure (once its gauges are blended), the scenario sailed. Several
tests of the whole chart were written when it held the Channel alone (its regions, its
features, the seam off Penmarch over the corridor, the directions' limits, the stream
areas' chart, the port files' list): a block updates them to hold its region beside the
others, as 39b did.

The recorded passages are the proof that a block moved nothing of the Channel: run
`python -m pytest tests/test_known_truths.py --slow -n 4` whole. A `-k "gate_5b or
gate_5c"` selects the tests by their names and not by their fixtures, and so runs one
test of the passages' many (39b found it so).

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

## Out in the ocean: the islands and the corridor (package 39e)

Madeira and the Western Islands are two regions with no neighbour (`madeira`, `azores`),
so the seam rule keeps nothing (`tiles another region lists: 0 kept`); what they found:

- **Widening the corridor rewrites it.** The corridor is whole tiles on the level-1 grid,
  but a tile reaches past its fetch box, and the cells beyond are `NODATA`: the old west
  column ran from 22.13 W with nothing west of 20.1 W. Moving the west bound to 32 W fills
  those cells, the distance field changes wherever new land is the nearest (the Azores,
  up to 613 cells in that column), and the bilinear sample at a new origin breaks the
  half-metre ties the other way (±1 m in a few hundred to two thousand cells of every
  tile, a land cell or eleven turning to sea). So a corridor's widening changes every
  existing tile in its arrays as well as its bytes. No recorded passage or trial reads
  the corridor (they are `region: channel-west`, whose chart has no corridor); the
  widening to 32 W is built and held for the owner's word (package 39e's report). A
  rebuild from the same cache is now byte-identical (`save_tile`).
- **A peak is seen beyond the search's reach.** `Chart.in_sight` searched the index
  only as far as the horizon of an object of 300 m, and the weather's clearest
  visibility is twelve miles: the Peak of Pico (2,351 m, seen thirty leagues off by the
  directions) could not be seen at forty. A feature taller than `chart.SEARCH_HEIGHT_M`
  is now looked for wherever she is, and in the clearest weather
  (`chart.CLEAR_VISIBILITY_NM`, the weather's "the horizon") seen to its own geographic
  horizon; no feature of the Channel is so tall, so nothing its lookout sees moves.
- **EMODnet does not hold every islet.** The Formigas, the Cabras off Angra, the islets
  of Vila Franca, the Mosteiros and the Magdalena are water in the grid (the Formigas'
  place has 66 m, nothing under 34 m within eight kilometres). An islet the grid lacks is
  the feature's alone: a rock with a height and an `extent_m` grounds a ship
  (`danger_under`), an island is a mark; check every islet against the tiles.
- **A block's gauges beyond every Channel position's reach** (the islands' are a thousand
  miles from Brest) would move no Channel tide if blended, but they want a mean level
  each, which no open source gave here: they are held as the brief has them, and the
  world's tide over the islands is the nearest of the eleven alone (Le Conquet's, four
  times the islands' range). The fill raise (`fill_to_chart_datum`) follows that tide.
- **The directions' limits were one box over the coast**, and within it the open
  Channel's statement answered where no area did; a block far out in the ocean puts its
  water in a box of its own in `book_limits` (package 39d's list of boxes, the open
  Channel's statement of its own bounds) rather than widening one box over the sea
  between.
- **Open sea is dear.** 131 of the Azores' 153 level-2 tiles hold no land and lie more
  than three miles from it, and the multibeam relief compresses badly (260 KB a tile,
  against Madeira's 107): 40 MB. Writing only the tiles within ten miles of land would be
  33 tiles and 10 MB, the corridor answering the rest at 30″ (a recipe rule for the
  lead, which wants the corridor widened first).
- **Tofiño's bearings are true**: the Punta Delgada to the Galera, "S 75 E seven miles
  and a half", fits the grid's points within five degrees and a mile, where a magnetic
  bearing would be twenty degrees out.
- **Norie's Table XLI** (1805), whose columns the OCR loses, is legible in the page
  images through the Internet Archive's IIIF server
  (`https://iiif.archive.org/iiif/<item>$<leaf>/full/900,/0/default.jpg`, the leaf from
  the archive's full-text search); the encyclopaedia's pages serve where its API refuses
  for its rate.
