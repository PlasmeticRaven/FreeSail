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
   block's features must lie within it), `fetch` (the EMODnet subset, the bounds widened
   so that the level-2 tiles that meet them and the harbours' level-3 tiles are covered
   whole: a tile spans 0.43° at level 2, so the widening is up to that much where the
   tile grid falls badly (Biscay north's southern row starts 0.32° below its bound), and
   a quarter of a degree is not always enough; `--check` says so; package 39b), `harbours` (the level-3
   patches as boxes, about 15′ by 15′ each, one per port of the block, named as the port
   file's road and the override name them), `sources` (the ids of `SOURCES` the tiles
   are cut from, in the order they are laid: EMODnet for the depth and the coast, GEBCO
   under it). A source not yet in `SOURCES` (Tofiño's sheets are period data, not a
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
   until that region is next built: its `index.json` is the other region's file, which a
   block never writes; until then it is found by name and the lookout does not see it
   (39b's marks of the Raz de Sein in `channel-west.yaml`; the lead's to rebuild).
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
   port, M6 §26); the nations index `data/nations.yaml` where a nation is new (Morocco,
   for Tangier). Every spot that names a `feature:` gives its `lat_deg` and `lon_deg`
   beside it: a scenario with no `ports:` list (the gate 5b passages) loads every port
   file on the Channel's chart alone, where the block's features are not, and the spot
   falls back to its own position (without it the load is refused and every such
   passage with it). `test_ports.py` names the port files in a list: the block adds its
   own.
6. **The tide**: the block's gauges read from TICON's file (`TICON.txt` in the zip at
   doi.pangaea.de, as package 34 read it, by their coordinates; the form is the
   eleven's: the record, the mean level above the chart's datum with its source, M2, S2
   and N2), **held** under `gauges_held:` in `data/tides/constituents.yaml` and not in
   `gauges:`. The interpolation blends every gauge within `reach_nm` (400 miles) of a
   position, so a gauge of Biscay or Iberia added to `gauges:` enters the blend at every
   position of the Channel and moves every recorded passage; until the engine gives a
   gauge its own water (a reach or a chart of its own: the lead's decision, package 39b's
   finding), the block's gauges wait there, read and verified, and the world's tide over
   the block is the eleven's blend. The stream areas in `data/tides/streams.yaml`, each
   with `chart: <region>` and its `book:` in the period's form (`test_tide.py` holds
   every area to it), are looked up first-match: an area within another's polygon goes
   before it (the Raz before the Iroise), and the block's areas go before `mid-channel`,
   whose statement in the directions has no polygon and answers for every position
   within `book_limits`, a single box the block widens to hold its water. Keep the
   polygons off the water the recorded passages' other sail use (the naval cruise's
   Diamond within eight miles of 48 N 4 55 W and Harpy within ten of 47 50 N 6 W; the
   merchant passage's Palinure from the Raz and Hirondelle from Sein), or their digests
   move with them. The places of the master's epitome in `establishments.yaml`, Norie's
   and Moore's, with `rise_judgement` where the period gives no rise: such a rise is the
   world's spring range at the place to the foot (`test_tide.py` holds it), which over a
   block whose gauges are held is the Channel's blend and not the place's own. The
   eleven gauges and their figures do not move.
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
   corridor and the sources' earlier fetches carried over as they were (since 39b each
   source's records of the files this run did not fetch are kept beside this run's: a
   `--region` build had dropped the corridor's GEBCO extract and the other regions'
   EMODnet subsets). **The seam**: the level-2 tiles are on one grid for every region, so
   regions that abut share the tiles that straddle their edge; a tile another region of
   the manifest lists is that region's, and the build neither writes it again nor lists
   it (`tiles_listed_elsewhere`; the block's grid still covers it, for the distance field
   and the coast near the edge, and no coast is drawn over it). After the build
   `git status` shows no change to any tile, coast or index file another region lists.
   The tiles are committed (the owner's ruling 5; a region is about 12 to 18 MB).
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
  `datum_above_chart_datum_m`, a number;
- **the fetch box covers the tiles whole** (package 39b): every level-2 tile that meets
  the bounds and every harbour's level-3 tile lies within `fetch`;
- **the tiles another region lists** (packages 39a and 39b): how many of the block's
  tiles are another region's, kept as theirs, not written and not listed;
- **the shore swept for GEBCO's fill** (spec M5 §33 item 16): at the build, the cells
  where EMODnet has nothing and GEBCO's fill reads water shallower than three metres,
  clustered and printed largest first, for the block to patch (a town, an islet) or to
  say are water. On a low coast it finds the marshes and the lakes behind the shore
  (Biscay north: the Brière, the lake of Grand-Lieu, the Marais poitevin); they are
  closed from the sea and are left as water, said in the notes. The same coasts show
  the other face of GEBCO's land under EMODnet's: its heights are above mean sea level
  and are read as above LAT, so land within a few metres of the sea reads as ground that
  dries, and at high water springs the model floods the marsh behind a dyke; a rule for
  the tool (a floor under GEBCO's land where EMODnet has none), the lead's.

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

## The worked example: the Channel east block (`channel-mid`, package 39a)

The recipe, as spec M6 §26 outlines it:

```python
"channel-mid": {
    "title": "The mid Channel, Start Point to Portland and the Channel Islands",
    "bounds": {"south": 49.0, "north": 51.0, "west": -4.0, "east": -1.0},
    "fetch": {"south": 48.75, "north": 51.25, "west": -4.25, "east": -0.75},
    "harbours": {
        "dartmouth-torbay": {"south": 50.30, "north": 50.50, "west": -3.60, "east": -3.45},
        "portland-weymouth": {"south": 50.52, "north": 50.65, "west": -2.50, "east": -2.35},
        "guernsey": {"south": 49.40, "north": 49.52, "west": -2.65, "east": -2.48},
        "jersey": {"south": 49.15, "north": 49.27, "west": -2.25, "east": -2.05},
        "alderney": {"south": 49.68, "north": 49.75, "west": -2.30, "east": -2.15},
        "st-malo": {"south": 48.60, "north": 48.70, "west": -2.10, "east": -1.95},
    },
    "sources": ["emodnet_dtm_2024", "gebco_2025"],
},
```

The region overlaps the Channel west region's eastern tiles (48 to 51 N, 7 to 3 W) by a
degree; a query takes the first region in the chart's order where two hold a point, so
the overlap costs nothing but tiles, and the block may set its western bound at 3 W
instead to avoid building them twice. St Malo's patch lies south of the block's southern
bound as outlined (49 N): the bound is lowered to 48.5 N or the patch given to a Biscay
block, the block's choice, said in its notes.

The period data (M6 §26): Mackenzie's Hurd sheets for the English side (Dartmouth,
Torbay, Portland; the RMG's free files to locate features, the depths from White 1835
and Imray 1874 as the Channel west block read them), Bellin's Petit Atlas Maritime for
the French side and the islands (Rumsey's IIIF server at full resolution, as package 35b
read Roscoff's sheet; the brasse the study's unverified 1.624 m until a legend is read),
Faden 1793 and the Channel pilots for the directions; the lights of 1805 dated (the
Casquets 1724, Portland 1716, the Start 1836 and Berry Head 1906 not yet; each date
from memory, to be read from Trinity House's pages as the Channel west block's were).
Nations: the islands
British; St Malo and Morlaix hostile to a King's ship. The tide: TICON's Weymouth, St
Helier, Saint-Malo and Cherbourg are in the table already; the streams of the Race of
Alderney, Portland Bill and the Start from the period's directions where they give them
(Bowditch 1802's headland table has Portland), the rest the world's rounded and marked
judgement as the Channel's are, with `chart: channel-mid` on each area.

What the block need not do: nothing of `freesail/` changes for a block, unless its
water wants a rule the engine lacks, which is a finding for the tuning notes and the
lead, not a patch in the block.
