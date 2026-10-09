# The chart data's sources

What `data/charts/` is built from (spec M5 §10; the study `docs/design/ChartData.md`;
package 32), source by source: what was taken from each, under what licence, and where
the licence text is kept. The manifest (`data/charts/manifest.yaml`, written by
`tools/build_charts.py`) carries the same per source with the URL, the retrieval date and
the checksum of every file fetched, and the attribution block the game shows. The rule
throughout is the study's: **the image is licensed; the facts on it are not.** The modern
grids are resampled into the tiles under licences that allow it; the period charts and
pilots are read, by hand, into `features/` and `overrides/` files that cite the sheet or
the page, and no scan is committed.

## The modern grids in the tiles

| Source | Taken | Licence | Text |
|---|---|---|---|
| **GEBCO_2025 Grid** (GEBCO Compilation Group, 2025; doi:10.5285/37c52e96-24ea-67ce-e063-7086abc05f29) | Level 0, the world at 2.5′, from the eight global GeoTIFF tiles at CEDA decimated by ten (the block mean, the land clipped at fifty metres above the sea), and level 1, the Atlantic at 30″: both built by the tool (`--world`, `--atlantic`) on the developer's machine and not committed (spec M5 §10); and, in the committed tiles, the land under level 2 where EMODnet has nothing. Elevation relative to mean sea level. The region's own extract (47.65 to 51.35 N, 7.4 to 2.4 W at 15″) from GEBCO's grid subsetting application. **The corridor** (package 38; spec M6 §26): level 1 at 30″ over 32 N to 51 N and 20 W to 1 W, from a second extract of the same application (31.9 to 51.1 N, 20.1 to 0.9 W at 15″, ESRI ASCII in a zip of 114 MB, retrieved 2026-10-09, its SHA-256 in the manifest beside each tile's), sampled at the level's cell centres (the mean of the four 15″ cells each sits on), with a distance-to-shore field over the block; 30 tiles, 5.9 MB compressed, **committed** under `tiles/1/atlantic-corridor/` by the owner's ruling 5, so that a clone plays the voyage. Elevation relative to mean sea level, the level's datum. | Public domain: "placed in the public domain and may be used free of charge", with the acknowledgement of the source, no suggestion of official status, and "should NOT be used for navigation". | `licences/gebco-terms-of-use.md` |
| **EMODnet Bathymetry DTM 2024** (EMODnet Bathymetry Consortium, 2024; doi:10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1) | Level 2, the region at 3″, and level 3, the four harbour patches at 0.5″, sampled bilinearly from the 1/16′ grid; the coast, as the zero contour of the level-2 elevation; the per-tile shoalest sounding from the grid's own per-cell maximum. Elevation relative to lowest astronomical tide, which is the chart datum of levels 2 and 3. Fetched as classic netCDF subsets from EMODnet's ERDDAP service (`bathymetry_dtm_2024`). | Creative Commons Attribution 4.0 International, with the constraint DO NOT USE FOR NAVIGATION. | `licences/cc-by-4.0.txt` |
| **SHOM MNT bathymétrique de façade Atlantique** (projet HOMONIM, 100 m) | Nothing in this build. The French cross-check the study asks for was not made: the grid is published as 7z archives and the build machine has no reader for them, and the rule that the tool adds no dependency beyond numpy and pyyaml holds. The manifest says so; the recipe is in `data/charts/unverified-checks.yaml`. | Licence Ouverte 2.0 (Etalab), as data.gouv.fr states. | `licences/licence-ouverte-2.0.md` |
| **SHOM-IGN Histolitt coastline** (the French shoreline) | Nothing in this build: the data.gouv.fr record found is a regional republication with no licence stated, and SHOM's own diffusion is behind a form. The French shore is EMODnet's. | SHOM–IGN's own conditions, to be copied verbatim when fetched. | `licences/shom-ign-histolitt.md` |
| **UKHO** | Nothing. The INSPIRE layers are under the Open Government Licence and are not needed; the survey bathymetry's licence was not read (the unverified list), and EMODnet carries the surveys. | OGL v3.0 for the INSPIRE layers. | `licences/ogl-3.0.md` |
| **OpenStreetMap** | Nothing, on purpose: ODbL is not in the allowed list (C §2). | | |

The allowed-licence list the tool refuses against is `ALLOWED_LICENCES` in
`tools/build_charts.py`: public domain, CC BY 4.0, Licence Ouverte 2.0, OGL 3.0, LGPL 3.0
and the named per-source permission of Histolitt. The test
`tests/test_chart.py::test_every_source_in_the_manifest_has_an_allowed_licence_with_its_text_kept`
reads the manifest against it.

## The period charts and pilots in the hand-made files

Read into `data/charts/features/channel-west.yaml` (206 entries) and the five overrides of
`data/charts/overrides/channel-west/` (the fifth, Roscoff's, package 35b's), each entry
citing the work and the page in the form
of `docs/references/README.md`. The scans and the OCR texts are cached outside the
repository and never committed.

| Work | Where read | What was taken |
|---|---|---|
| Faden, *Le Petit Neptune François; or, French Coasting Pilot*, 1793 | Internet Archive `lepetitneptunefr00fade`, the OCR text, pp. 53 to 62 | The Four, the Passage du Four, the Platresses, La Valbelle and Le Tendéoc, La Helle, Conquet and the Vinotière, Blanc Sablon, St Matthew's Point and the Monks, the Black Rocks (Noires, Bossevins), Béniguet and the isles, Ushant and Keller, the Cock, the Buzec and its marks, Bertheaume road, the Bay of Brest with the Fillettes and the Mingan and their marks, the castle of Brest, Camaret road, Toulinguet and the Bellen, the Parquette, the Gouemont and the Vandrée, the Basses du Lis and the Menjan, the Pezeaux and the hay-ricks, the Bec de la Chèvre, the Iroise with its bottom, the tides of the Four, the Raz and the rade, and the soundings south-west of Ushant with their grounds. In his translation's fathoms. |
| Martin White, *Sailing Directions for the English Channel*, 1835 | Internet Archive `sailingdirectio00whitgoog`, the OCR text, pp. 13 to 35 | Scilly: St Agnes light at five leagues, the daymark, the Crim, the Bishop, the Bishop's Ridge and the Shovel, the Nun Deeps, the Poll Bank, the Gilstone, Crow Bar by the hour of tide and the Crow Rock's three heads, St Mary's Road and its berth, St Mary's Sound's leading mark, the Woolpack and the Spanish and Bartholomew ledges, Broad Sound and the Old Wreck, the North Channel, Spence's chart "minutely correct", the Seven Stones with the Pollard's position; the Lizard and its lights, the Stags, the Craggan, the Rose, the Spanam, the Beast; the Manacles, the Penwin and the Vaze and Mawnan church's mark; Falmouth's two channels and their leading marks, St Just Pool, the Gray, the Deadman, Gribbin Head; the Eddystone's stream and its oozy ground, the Hand Deeps, the East Rutts, the Gregory rock; Plymouth Sound's channels, marks and anchorage, Cawsand Bay, the Dragstone, the Knap, the Panther; the Start. |
| James F. Imray, *Sailing Directions for the English Channel*, part I, 1874 | Internet Archive `sailingdirection00unse_0`, the OCR text, pp. 75 to 108. The study called this item Imray 1848 from its catalogue date; its title page reads 1874 and its variation note 1873, and it is cited as 1874. | Falmouth: the entrance, the Black Rock, the Old Wall, the Lugo rock, St Mawes and Falmouth banks, the Governor, Carrick Road, Cross Road and St Just Pool with their depths, the outer road, the inner harbour's depths before the dredging, the docks then building, the tides; the coast to Plymouth (the Nare, the Gull rock, the Bizzies, Gwineas, Mevagissey, Fowey, the Udder rock, Looe Island); Mount's Bay (the Gear, Gwavas Lake, the Low Lee, Mousehole, the Runnelstone); the Land's End, the Longships, the Brisons, Cape Cornwall; the Seven Stones' light-vessel; Plymouth's Hamoaze. |
| Stephenson and Burn, *The Channel Pilot*, 1795 | Internet Archive `bim_eighteenth-century_the-channel-pilot-compr_stephenson-john_1795`, the OCR text | Nothing cited: the ECCO microfilm's OCR is illegible past the title page. In period exactly, and the first thing to read from the page images. |
| Serres, *The Little Sea Torch*, 1801, plate 13 | Rumsey, Internet Archive `dr_plate-13-...-11197022`, the display image | The coastal views named in `view` for the Lizard (three bearings), the Land's End, Pendennis, St Mawes, the Dodman, the Manacles and Rame Head. |
| Mackenzie senior, *A Treatise of Maritim Surveying*, 1774 | Internet Archive `bim_eighteenth-century_a-treatise-of-maritim-su_mackenzie-murdoch-fr_1774`, the OCR text, part II p. 15 | The datum statement: depths "such only as are taken at low Water in ordinary Spring-tides", and the allowances by the hour of tide. |
| Mackenzie junior, *A survey of the south coast of England from Plymouth to the Lizard*, 1773, Hurd 1809 | RMG G223:2/42, the museum's display image (1,077 by 1,280 pixels) | The Fowey inset's legend ("The Soundings are at low water Spring-tides. Tides rise 15 feet at springs. Neaps 7 or 8. Variation 22° 30′ W", 1774) and its soundings, legible; the Sound and the coast not legible at that size. The Plymouth override names it. |
| Dummer, *The harbour of Falmouth*, 1698 | RMG P/34A(37), the museum's display image (817 by 1,280 pixels) | The Roads' shape before any works; no sounding legible. The Falmouth override names it. |
| Spence, the Scilly Islands, 1792, on Hurd's sheet of 1808 | RMG rmgc-object-540451 | Not read: no display image on the museum's page. White's word for it stands. |
| Bellin, *5e carte particulière des costes de Bretagne*, 1773 | Rumsey, Internet Archive `dr_5e-carte-particuliere-des-costes-de-bretagne-12066036`, the display image (1,536 by 975 pixels) | The coast's shape and the larger names; the soundings in brasses and the legend not legible at that size; the full-resolution JPEG 2000 (14.7 MB, CC BY-NC-SA) cached and not transcribed. |
| Beautemps-Beaupré, *Le Pilote français*, I, 1822 | Défense digital library | Not opened: the site refused every connection from the build network. |
| Bellin, *Carte de l'entrée des rivières de Morlaix, de St Paul de Léon, et Isle de Bas, avec les roches, basses, et isles*, *Petit Atlas Maritime* t. V no. 51, 1764 (package 35b) | Rumsey 6903.538, Internet Archive `dr_carte-de-ientree-des-rivieres-de-morlaix-de-st-paul-de-leon-et-isle-de-ba-6903538`; read 2026-10-02 at full resolution (11,336 by 6,959 pixels) through the Rumsey collection's IIIF server, the crops cached outside the repository (CC BY-NC-SA 3.0) and none committed | Engraved south up. The town of Roscou with its church and its harbour (stippled, dry), the Chenal de Bas and its soundings in brasses (½ twice in the narrows by Roscoff, 2 and 1 east of them, 3 twice south of the island's middle, 6 off the Roche Croix, 10 and 15 at the western entrance, 12 at the Pierre Blanche), the Petite and Grande Lavandière, the Isle Verte, the Isle Ledanet and le Loup, Pointe de Pergueridre, Bloscou, the churches of N.D. de St Paul and N.D. de Bon Secours on the island, le Taureau; the scale, 1,800 toises to 1,330 pixels. No legend for the soundings: brasses at low water of springs, unverified for Bellin. Georeferenced by six control points (residuals 70 to 230 m); the Roscoff override names it and carries the road (3 brasses), the channel west of it (6), the harbour drying, the town and the Isle Verte as land. |
| Beautemps-Beaupré, *Le Pilote français*, the north coast (surveyed 1837 to 1838) (package 35b) | Gallica; the Défense digital library | Not reached: gallica.bnf.fr answered 403 to every request from the build network on 2026-10-02, and the Défense library reset the connection. Later than the period in any case; the Roscoff patch rests on Bellin's sheet and the pilots' words, as it says. |
| Faden 1793, 'Isle de Bas' and the tides of the north coast (package 35b) | the same OCR text, pp. 44 to 48 | Roscoff's free port for the rum "sold to our smugglers"; the eastern passage "at low tide no passing at all" and to be taken with a pilot; the western passage by the Lavandière and the Couillon, a man on the mizzen yard; the anchorage over against the island's great cove "in 4 fathoms at low water"; the tides W ¼ S and E ¼ N; high water at the Isle of Bas with a W by S moon. |
| La Barre, *The French Coasting Pilot*, 1825; Norie, *The New British Channel Pilot*, 1839 (package 35b) | Internet Archive `frenchcoastingp00barrgoog` (the OCR's running heads partly illegible, pp. 39 to 40) and `newbritishchann00norigoog`, p. 148 | La Barre: "Roscoff Harbour or Toum, a place well known to the English smugglers", the island road in three to four fathoms on sand; Norie: "frequented only by smugglers and fishermen", the tide till a quarter past five at full and change. |
| Imray 1874, 'Roscoff', 'Ile de Bas', and 'Scilly Islands' (package 35b) | the same OCR text, pp. 104 to 108 and 211 to 212 | Roscoff "dry at low water", the Isle de Bas's high water 4h 49m at full and change and its springs' rise of 23 feet; St Mary's Road "capable of containing a fleet of 200 sail", St Mary's Pool "where small craft anchor opposite the town", St Mary's Sound "by far the best and safest channel", the fresh water and provisions. |
| *Arrest du Conseil d'État du Roi* of 3 September 1769, on the entrepôt of tafias at Roscoff (package 35b) | Internet Archive `arrestduconsei00fran_32` (the Newberry's French pamphlets), the OCR text | The colonies' rum allowed to lie a year in bond at Roscoff for export abroad: the market file's note on the rum. |
| The French encyclopaedia's pages for Roscoff's marks (package 35b) | fr.wikipedia.org, read 2026-10-02 (the API; several requests refused for their rate) | The positions of the church of Roscoff (built 1522 to 1545, its openwork belfry since 1585), the chapel of Sainte-Anne on the Isle of Bas (the ruins of the old church of Saint-Paul-Aurélien, the sheet's St Paul), the bourg of the island and Pointe de Perharidy: the override's control points. |
| Trinity House, the lighthouse pages; the encyclopaedias' pages for the French lights | trinityhouse.co.uk; en. and fr.wikipedia.org, read 2026-09-30 | The lights' dates: the Lizard 1752, the Eddystone 1698, 1709, 1759 and 1882, the Longships 1795, St Agnes 1680 to 1911, the Bishop 1858, the Wolf 1870 (a daymark 1795), St Anthony 1835, the Start 1836, Godrevy 1859, Trevose 1847, Round Island 1887; the Stiff 1699, Saint-Mathieu 1692 and 1835, Créac'h 1863, the Pierres Noires 1872, Kermorvan 1849, the Four 1874, the Petit Minou and Portzic 1848, Sein 1839, Ar Men 1881, the Île Vierge 1845, Batz 1836, the Sept-Îles 1835, the Triagoz 1864. |

The positions of the features are the modern chart's, checked against the EMODnet coast
and moved by the rule the features file's head states; the doubtful ones say so in `fix`.
The five overrides each name their sheet, their unit, their datum, the datum correction
applied (from memory of the modern tide tables, marked unverified; Roscoff's 1.30 m is
SHOM's BMVE as the tide study quotes the RAM) and their control points.

**The rebuild of 2026-10-02 (package 35b).** The Roscoff override and its harbour group
(`roscoff` in the tool's `REGIONS`, 48.71 to 48.76 N, 4.07 to 3.95 W) were rasterised by
`python tools/build_charts.py --skip-fetch` from the sources cached on 2026-09-30 (their
checksums the manifest's, unchanged). One level-2 tile changed (`175200_-15168`, the north
coast of Léon) and four level-3 tiles were added under Roscoff; every other tile came out
byte for byte as before, the coast moved only at Roscoff, and the manifest's build hash
moved with the hand-made files and the tool's recipe. A rebuild with the same files gives
the same tiles: the tool's output is a function of its inputs.

## The unverified list, checked

Each item of the study's §7 was checked from the build network on 2026-09-30 and the
finding recorded in `data/charts/unverified-checks.yaml`, which the tool copies into the
manifest's `notes`. In short: Mackenzie's datum, the GEBCO_2025 file size and Le Créac'h's
date are verified; the Défense library and Gallica still refuse the build network (the
Commons copies stand, and Chapman's 1809 survey of Plymouth Sound is there to read); SHOM's
two licence statements are still in conflict and no image of theirs is used; the UKHO
bathymetry licence is still unread and unneeded; GSHHG's tolerances, the datum offsets at
the four ports, the brasse on the French sheets and the Seven Stones light-vessel's year
stay unverified and are marked so where they are used.

## The recipe for the rest

`python tools/build_charts.py` fetches the region's sources into `.cache/charts/` (or
`--cache DIR`), builds the region and writes the manifest; that is what the repository
carries. The world and the Atlantic are built on the owner's machine and never committed
(spec M5 §10): `--world` fetches GEBCO's global GeoTIFF zip (4.2 GB) and writes level 0
into `tiles/0/` (150 tiles, 26.5 MB, twelve minutes), `--atlantic` level 1 into `tiles/1/`;
git ignores both folders, the manifest lists their tiles only when the build made them,
and the runtime reads whichever are present. `--reuse-world` keeps a built world level as
the last manifest lists it after a change of the hand-made files; `--skip-fetch` refuses
the network. A new region is a recipe in `REGIONS`, a features
file and its overrides, and the same run (C §5.2: "adding a region later is adding tiles
and a features file, nothing else").
