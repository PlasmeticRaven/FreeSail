# Design study: chart data for a real sea

From the owner's ruling 1 of 2026-09-29 on the milestone 5 scoping draft: the map is a
real sea, the western English Channel and the Western Approaches, Falmouth to Ushant and
Brest, about a hundred miles square; older coast and depth data are wanted wherever they
can be had, since dredging, training walls and shifting banks have changed the harbours
and approaches; and the data model and the pipeline are to be built so the map can grow
toward the whole Atlantic and, as a long-term dream, the world. A study for the M5b
chart section of the specification; not itself a specification.

Reads with: `docs/TechnicalSpec-M5.md` §3 (5b), §4; `docs/design/InwardAndOutward.md`
(the chart is a reading; a grounding arrives through the lead and the hull);
`docs/design/Papers-and-Books.md` (a chart and a pilot are ship's papers);
`docs/references/README.md` (how sources are cited). The sister studies
`Navigation1805.md` and `Tides1805.md` take the reckoning and the tide; this one stops at
the data under the keel and the shape of the shore.

Everything below was checked on 2026-09-29 against the pages named. Where a page could
not be opened from the build network, or a claim rests on memory, it is marked
**unverified**. Nothing numeric here should become a game constant without being read
again from the source when the feature is built.

## 1. What the map has to answer

Four questions, each cheap, each many times a second: *how deep is it here* (for the
lead, the grounding and the anchor), *how far and which way is the nearest shore* (for
the lookout and the log's "the land bearing north-east, distant four leagues"), *what is
in sight* (headlands, lights, marks, other things a lookout names), and *is she aground*.
Behind them a fifth, asked once per passage: *what does the captain's chart say*, which
is not the truth and is the subject of 5b's two positions.

The area is bounded, for the purpose of this study, by 48°N to 51°N and 7°W to 3°W:
about 335 km north to south and 290 km east to west at that latitude, covering Falmouth,
Plymouth, the Lizard, Land's End and the Scillies on the English side, Ushant, the Iroise,
Brest and the Chenal du Four on the French, and the open Channel between. A frigate draws
about 5 m and a schooner about 3; the game needs the ten-fathom line honest, the
five-fathom line honest, and the rocks and drying banks of the approaches exactly where
the period put them.

## 2. Modern open coast and bathymetry

What each gives, what it costs, and whether its terms let it be redistributed inside an
MIT-licensed game. "Redistributable" below means the *derived tiles* the game ships can
carry it; attribution text lives in the manifest (§5).

| Source | Coverage and resolution | Format | Licence | Redistributable |
|---|---|---|---|---|
| **GEBCO_2025 Grid** ([gebco.net](https://www.gebco.net/gebco2025-grid), [terms](https://www.gebco.net/data-products/gridded-bathymetry/terms-of-use)) | Global, 15 arc-seconds (43,200 × 86,400 cells; about 460 m at the equator, 300 m east-west at 49°N). Land and sea in one grid. | netCDF (global file, about 4 GB compressed and 7 GB open, the figures GEBCO gives for its 2026 release and the same order for 2025, **unverified** for 2025 exactly); netCDF, GeoTIFF or ESRI ASCII for a user-drawn area from the download app; a cloud-optimised GeoTIFF mirror of about 3.3 GB exists. | "The GEBCO Grid is placed in the public domain and may be used free of charge": copy, publish, distribute, adapt and commercially exploit, with an acknowledgement of the source, no suggestion of official status, and the note that it is not for navigation. | Yes, with the acknowledgement. |
| **EMODnet Bathymetry DTM 2024** ([release page](https://emodnet.ec.europa.eu/en/emodnet-bathymetry-dtm-2024-release), [product record](https://emodnet.ec.europa.eu/geonetwork/srv/api/records/cf51df64-56f9-4a99-b1aa-36b8d7b743a1), [a tile record](https://sextant.ifremer.fr/record/36276c23-a660-435f-802b-4c755b536985)) | All European seas, 1/16 × 1/16 arc-minute (about 115 m north-south, 75 m east-west at 49°N). Built from 22,032 surveys and composite DTMs from 66 providers; SHOM and the UKHO both contribute, so this is the best open modern grid for the whole M5 area. Supplied in 59 tiles; the tile or tiles covering 48–51°N, 7–3°W are picked in the download portal (the tile letters were not confirmed from here). | ESRI ASCII, XYZ, CSV, netCDF (CF), GeoTIFF, SD; also WMS/WCS. | Creative Commons Attribution 4.0 International, with "DO NOT USE FOR NAVIGATION". Citation: EMODnet Bathymetry Consortium (2024), EMODnet Digital Bathymetry (DTM 2024), DOI 10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1. | Yes, with the citation. |
| **SHOM MNT bathymétrique de façade Atlantique (HOMONIM)** ([data.gouv.fr](https://www.data.gouv.fr/en/datasets/mnt-bathymetrique-de-facade-atlantique-projet-homonim-1), [SHOM record](https://services.data.shom.fr/geonetwork/1/api/records/MNT_ATL100m_HOMONIM_WGS84.xml)) | North Sea, Channel and Bay of Biscay out past the shelf to about 4,800 m; 0.001° (about 111 m). Two vertical references offered: lowest astronomical tide (the French chart datum) or mean sea level. | ArcGIS grid, WMS, direct HTTP. | Licence Ouverte / Open Licence 2.0 (Etalab): free reuse, commercial included, with attribution. | Yes, with attribution. |
| **SHOM Litto3D Bretagne 2018–2021** (SHOM catalogue; found through [Sextant](https://sextant.ifremer.fr/geonetwork/srv/api/records/4c54ac5e-9b83-42ad-b10e-e0769d6a1cd3)) | Airborne topo-bathymetric lidar of the Breton shore and islands, 1 m, land and sea in one surface; Finistère included. | Point clouds and DTM. | Licence Ouverte 2.0, credit "Shom - IGN". | Yes; far finer than the game needs, useful for the Brest and Iroise harbour patches only. |
| **SHOM–IGN Histolitt coastline** ([data.gouv.fr](https://www.data.gouv.fr/fr/datasets/shom-ign-trait-de-cote-histolitt-r)) | The French shoreline as 2-D polylines at the level of highest astronomical tide. | Vector. | Free reuse with "© IGN-Shom 2009" and their conditions (logos and links when shown on a website). | Yes, with the credit; the conditions are SHOM–IGN's own, not Etalab's, so they go in the manifest verbatim. |
| **UKHO ADMIRALTY Marine Data Portal and Seabed Mapping Service** ([portal](https://datahub.admiralty.co.uk/portal/apps/sites/#/marine-data-portal), [gov.uk guidance](https://www.gov.uk/guidance/inspire-portal-and-medin-bathymetry-data-archive-centre), [licensing](https://copyright.ukho.gov.uk/)) | UK EEZ. The INSPIRE layers (limits, routeing, wrecks) are under the Open Government Licence. Bathymetric surveys from the MEDIN archive (about 4,000 surfaces, 1970 to date) are downloadable free, gridded at 2 m and 4 m where a modern survey exists, as BAG or CSV, under a "UKHO Bathymetry Data Licence" that third parties describe as OGL-like; UKHO's own licensing site describes purpose-based routes (free non-commercial and low-value commercial for one year, with acknowledgement). | BAG, CSV; OGL layers as shapefile or services. | OGL for the INSPIRE layers. The bathymetry licence text itself was not read from here: **unverified** whether it permits redistribution of a derived grid inside a game whose own licence allows commercial use. | OGL layers yes. Survey bathymetry: not until the licence is read; it is not needed, since EMODnet already carries the UKHO surveys at 115 m. |
| **GSHHG 2.3.7** ([soest.hawaii.edu](https://www.soest.hawaii.edu/wessel/gshhg/)) | Global shoreline polygons in five resolutions (full, high, intermediate, low, crude, each about a fifth the size of the last), from the World Vector Shoreline at nominal 1:250,000 plus WDBII lakes; the maintainers warn it can be mis-registered against recent imagery when zoomed close. The Douglas-Peucker tolerances usually quoted (0.2, 1, 5, 25 km) are from memory, **unverified**. | Native binary, ESRI shapefile, netCDF-4. | GNU Lesser General Public License (since 2.2.2; LGPL v3 in current packaging). | Yes; LGPL on a data file is an odd fit but permits redistribution with the licence text. Good for the Atlantic and world tiers, too coarse for a harbour. |
| **Natural Earth 1:10m coastline** | Global, 1:10,000,000. | Shapefile. | Public domain. | Yes, but it is a world-map coastline: useful only as the crude fallback for the world tier's picture, never for depth or hazards. |
| **OpenStreetMap coastline** ([osmdata.openstreetmap.de](https://osmdata.openstreetmap.de/data/coast.html)) | Global, the finest open shoreline; land polygons, coastline strings and water polygons, split into chunks. | Shapefile, WGS84 or Mercator. | ODbL: attribution and **share-alike on any derived database**. | Not into an MIT-licensed data set without making the chart data ODbL. Use it, if at all, only for rendering in the viewer with attribution, never merged into the tiles. The lead recommends not using it for M5 at all: EMODnet, Histolitt and the period charts give the shore. |
| **NOAA ENC** ([chart downloader](https://charts.noaa.gov/ENCs/ENCs.shtml)) | United States waters only, S-57 vector charts with soundings, public domain, updated weekly. | S-57. | US Government work, public domain. | Yes, but irrelevant to M5; the model for what an Atlantic tier wants on the American side later (Des Barres's coast). |

Two remarks. First, EMODnet alone would do for open water and most of the coast at the
scale the owner named; SHOM's HOMONIM is a second opinion on the French side with the
chart datum stated, and GEBCO is what the Atlantic and world tiers are cut from. Second,
none of the modern grids is the 1805 sea in the harbours: EMODnet's Falmouth shows the
dredged channel of 1860, its Plymouth shows a breakwater, its Brest shows the naval and
commercial ports. That is the whole reason for §3.

## 3. Historical charts and surveys of the area

### 3.1 The surveys

- **Murdoch Mackenzie junior** (1743–1829), Admiralty Surveyor from 24 May 1771 in
  succession to his uncle, ordered to survey the coast of the British Isles from the
  Bristol Channel anticlockwise: Cornwall in 1772–73, the coast of Kent in 1775, the south
  coast of Devon in 1779, and so on until his sight failed and he gave up the office in
  1788, with **Graeme Spence** (c. 1758–1812) as his assistant and successor. His
  surveys of this coast that were later engraved: *A survey of the south coast of England
  from Plymouth to the Lizard, 1773*, with an inset plan of Fowey 1774, published by
  Hurd as an Admiralty chart in 1809 at about 1:90,000 (National Maritime Museum
  [G223:2/42](https://www.rmg.co.uk/collections/objects/rmgc-object-544536)); and *the
  coast of Cornwall from the Lizard Point to St Agnes Head, 1772*, published with
  Spence's Scilly of 1792 by Hurd in 1808 ([RMG record](https://www.rmg.co.uk/collections/objects/rmgc-object-540451)).
  The Falmouth survey the M5 area most wants (Mackenzie surveyed the harbour in 1774–75,
  **unverified**; the RMG record found under "harbour of Falmouth" is Dummer's manuscript
  of 1698, [P/34A(37)](https://www.rmg.co.uk/collections/archive/rmgc-object-541407), a
  century too early but a check on what the Roads were before anyone touched them) is
  in the UKHO Archive at Taunton or, for pre-1826 material, in transfer to The National
  Archives as class ADM 352 ([gov.uk](https://gov.uk/guidance/the-ukho-archive)); neither
  is online.
- **Graeme Spence** surveyed the Scilly Isles 1789–92 and wrote a *Nautical description
  and survey of the Scilly Isles*, 158 folios with tides and tide tables, delivered to
  the Admiralty in 1797 (manuscript at Cambridge University Library,
  [catalogue](https://archivesearch.lib.cam.ac.uk/repositories/2/resources/6421); not
  digitised). His chart of the islands was engraved on the 1808 Hurd sheet above.
- **Mackenzie senior's** *Treatise of Maritim Surveying* (1774) is on the Internet
  Archive as an ECCO microfilm scan
  ([bim_eighteenth-century_a-treatise-of-maritim-su_mackenzie-murdoch-fr_1774](https://archive.org/details/bim_eighteenth-century_a-treatise-of-maritim-su_mackenzie-murdoch-fr_1774)).
  It is the statement of method for every British survey in the area: triangulation from
  a measured base, soundings by boat on compass lines, reduced to low water. What datum
  exactly he reduced to must be read from the text (**unverified**; the general practice
  of British charts before the twentieth century was a spring low water, and modern
  Admiralty datum is approximately lowest astronomical tide).
- **The Hydrographic Office** was created by Order in Council in 1795 with Dalrymple as
  Hydrographer; it printed its first chart in 1800 (an anchorage in Quiberon Bay) and
  under Hurd from 1808 engraved the Mackenzie and Spence surveys above. So in 1805 the
  King's ships on this coast sailed by private charts (Steel, Heather, Faden, Laurie and
  Whittle) and by manuscript copies; the Admiralty charts of the area are 1808–09
  engravings of 1772–92 surveys, which is exactly the depth data the game wants.
- **The French side.** The *Neptune François* of 1693 (Pène, Sauveur and the Académie),
  its 1773 re-issue by Bellin with the *5e carte particulière des costes de Bretagne*
  covering the environs of Brest, Bellin's *Carte réduite de la Manche* (1763) and his
  *Petit Atlas Maritime* sheets of the Breton coast (1764) are the printed French
  hydrography a captain of 1805 could own. **Beautemps-Beaupré** began the resurvey of
  France in 1816; *Le Pilote français, première partie: environs de Brest* appeared in
  1822, with a table of the tides observed at Brest in 1816; the north coast from Ushant
  to the Île de Batz was surveyed 1837–38; the work closed in 1844. Later than 1805 but
  the first French survey to modern standard of a coast that had not yet been dredged;
  for the Goulet, the Iroise and the Chenal du Four it is the best depth source there is.
- **Des Barres's *Atlantic Neptune*** (1774–1800) is the American shore, not this one;
  it matters for the Atlantic tier (§6).

### 3.2 Where the scans are and what they may be used for

| Holder | What (verified items) | Image terms |
|---|---|---|
| **Royal Museums Greenwich** | The Hurd 1808 and 1809 Admiralty sheets from Mackenzie and Spence; Dummer 1698; many later Admiralty surveys of Plymouth and Falmouth. | Images © Crown copyright / NMM. Free 72-dpi files (1,280 px long side, up to 15 per project) under CC BY-NC-ND for non-commercial use; anything larger is licensed through RMG Images. A 1,280-px scan of a 1:90,000 sheet is about 100 m per pixel: enough to place named rocks, not to read soundings. |
| **David Rumsey Map Collection** (davidrumsey.com, mirrored item by item on the Internet Archive as `dr_…`) | *Le Neptune François* 1693 (Mortier, Amsterdam) and the 1773 Bellin edition, including the [Brest sheet](https://archive.org/details/dr_5e-carte-particuliere-des-costes-de-bretagne-12066036); Bellin's [*Carte réduite de la Manche* 1763](https://archive.org/details/dr_carte-reduite-de-la-manche-12059030) and *Petit Atlas Maritime* Bretagne sheets 1764; *The English Pilot for the Southern Navigation* 1752 (Mount and Page) with [Halley's chart of the Channel](https://archive.org/details/dr_a-new-chart-of-british-channel-extending-from-north-foreland-to-scilly-isl-13251034) and the text pages of *Directions between Plymouth and Falmouth*; Serres's *Little Sea Torch* 1801 with its [coastal views of the Lizard, Pendennis, St Mawes, the Dodman and the Manacles](https://archive.org/details/dr_plate-13-1-lizard-nw-2-lizard-ne-3-lands-ens-4-lizard-nnw-5-11197022). Full-resolution JPEG 2000 files, 8 to 37 MB each. | CC BY-NC-SA 3.0, credit "David Rumsey Map Collection, David Rumsey Map Center, Stanford Libraries"; commercial use by arrangement. |
| **Bibliothèque nationale de France, Gallica** (its catalogue did not answer from here; the items were confirmed through the public-domain copies on Wikimedia Commons, which record the Gallica ark) | Bellin, *Plan de l'Isle d'Ouessant* 1764 (ark `btv1b8591931r`); *New chart of the Plymouth Sound* after Halley (ark `btv1b53010480b`); *Carte réduite des passages de l'Iroise, du Four et du Raz* (Dépôt de la Marine); Commons holds 250-odd files from the *Neptune François* and Bellin. | Gallica: non-commercial reuse free with the source named; commercial reuse under a paid licence. Commons treats faithful scans of public-domain charts as public domain. |
| **Library of Congress** | [The Atlantic Neptune collection](https://www.loc.gov/collections/the-atlantic-neptune-collection/about-this-collection/), some twenty-six volumes and sheets. | "Free to use and reuse" unless a rights advisory says otherwise. |
| **National Library of Scotland** | Mackenzie senior's *Maritime Survey of Ireland and the West of Great Britain* 1776 (for example [rec/833](https://maps.nls.uk/rec/833)); *Admiralty Charts of Scotland, 1795–1904*. Nothing for the Channel. | Per image, shown in the viewer: CC BY for most, CC BY-NC-SA for some; credit line required. The Atlantic tier's Irish and Hebridean coasts. |
| **SHOM, *Cartes marines anciennes (archives)*** ([data.gouv.fr](https://www.data.gouv.fr/datasets/cartes-marines-anciennes-archives)) | The ARCHIPEL digitisation of 2016: about 3,300 charts published from the late eighteenth century on and 6,700 survey plans from the early nineteenth, as JPEG 2000 with XML metadata and GML footprints, through data.shom.fr and diffusion.shom.fr. This should include the printed *Pilote français* sheets of 1822 onward and possibly the survey minutes; not confirmed from here. | data.gouv.fr states Licence Ouverte; SHOM's own catalogue record for the same series says "Copyright SHOM 2017 – reproduction interdite". **Conflict, unverified**: ask SHOM before redistributing any image, though transcribed soundings are another matter (below). |
| **Bibliothèques numériques de la Défense** (bibliotheques-numeriques.defense.gouv.fr) | Search results show it holds *Le Pilote français* 1822, Heather's *New British Channel Pilot* 4th ed. 1807, editions of *The English Pilot*, Faden's *Petit Neptune François*, and the Admiralty *Channel Pilot* of 1859, 1863 and 1869. The site refused every connection from the build network, so none of these records was opened. **Unverified**; to be checked from a browser. | Unknown; the ministry's site terms say Licence Ouverte except where third-party rights are stated, which for digitised public-domain books is likely but not confirmed. |

The licence table matters less than it looks, because of one distinction the pipeline
must keep: **the image is licensed; the facts on it are not.** A sounding of seven
fathoms off Black Rock in 1774, the outline of a bank, the name of a ledge, are
public-domain facts that anyone may read off a scan and write into a data file, whatever
the scan's terms. What the game must not do is ship the scan itself, or a raster derived
pixel by pixel from it, under a licence the holder did not give. So: the period charts
are *read*, by hand or by a tool, into `features` and `overrides` files that cite the
sheet; the scans stay in a cache and are never committed. The only exceptions worth
making are public-domain copies (LoC, Commons) if the viewer ever wants a period chart
as a picture on the captain's table.

### 3.3 Reading a period sounding

- **Units.** Fathoms of six feet (1.829 m) everywhere British and in Faden; French charts
  of the Dépôt in *brasses* (about 1.62 m, five *pieds du roi*; **unverified** as to
  which brasse each sheet uses, and the sheet's own legend must be read) until the metre.
- **Datum.** British soundings reduced to a low water of spring tides; Beautemps-Beaupré
  to a very low spring low water that became the French *zéro hydrographique*. The modern
  datum on both sides is approximately lowest astronomical tide, which lies below a mean
  spring low water by an amount that varies by port and is of the order of half a metre
  to a metre in this area (from modern tide tables; **unverified** figures, to be read
  from the current tables for Falmouth, Plymouth, Scilly and Brest when the overrides are
  built). The correction is small against a frigate's five metres and the game's honesty
  about depth; it is applied once in the pipeline and recorded per override.
- **Position.** A Mackenzie or Beautemps-Beaupré survey is internally good to tens of
  metres in a harbour, but its graticule may be minutes of longitude off. Georeference a
  sheet by control points that have not moved (rock heads, headlands, church towers,
  castles) against the modern coastline, never by its own longitude scale; then read
  features off it in the modern frame.
- **What has changed, and what the period data are for.** Verified where marked:
  *Plymouth Sound*: no breakwater until the works of 1812–41 (foundation stone 8 August
  1812, completed 1841); Cawsand Bay was the fleet's anchorage before it, where the
  blockading squadrons off Brest assembled; the Sound was open to southerly swell and the
  dockyard water was the Hamoaze. *Falmouth*: Carrick Roads deep by nature (the docks'
  histories call it the deepest natural harbour in western Europe), but the inner
  harbour and the Penryn river shallow and silting, and a 300-foot dredged channel to
  the docks only from about 1860; so the 1805 anchorage is the Roads and the shore off
  St Mawes, not the modern inner harbour. *Scilly*: rock unchanged, the sand between the
  islands not; in 1805 one light, St Agnes (1680), and none on the Bishop (1858), the
  Wolf (1869) or the Seven Stones (a lightvessel from the 1840s, **unverified**), which
  makes a night landfall what it was. *Brest*: the Goulet and the Iroise passages are
  rock and unchanged; the naval port and the commercial reclamation are not the 1805
  shore; Ushant had the Stiff light (1699), Saint-Mathieu its abbey tower light (1692);
  Le Créac'h (1863) did not exist (**unverified** date). The open western Channel has
  few sandbanks, so modern bathymetry is safe there; the differences are the harbours,
  the approaches and the works of man on the shoreline.

The method that follows: **modern grids for open water and the general coast; period
charts for the harbours, the approaches, the named hazards and the shoreline works;
every feature and every override carrying its source.** In practice the M5 area needs
four period patches (Falmouth and the Helford, Plymouth Sound and Cawsand, the Scillies,
Brest and the Iroise) and a feature list for the coast between.

## 4. Period sailing directions and pilots

What a pilot book gives that no grid can: the leading marks and transits by which a
harbour was entered ("bring St Anthony's Head open of Pendennis Point"), the dangers
named as a captain named them (the Manacles, the Bizzies, the Shovel, the Basse Royale),
the anchorages in words (depth, bottom, shelter by wind, which berth for a ship of war),
the hour of high water at full and change and the set of the streams, the soundings and
bottom used to make a landfall ("in eighty fathoms, fine grey sand, you are to the
westward of Scilly"), and the coastal views that let a lookout recognise a headland. For
the game these are the text of the `features` file, the vocabulary of the log, the
reference a language-model officer is pointed at, and, under `Papers-and-Books.md`, the
in-world book a captain may or may not own. Verified online, oldest first:

| Work | Where | Notes |
|---|---|---|
| *The English Pilot for the Southern Navigation*, Mount and Page, 1752 | Rumsey via Internet Archive (`dr_…13251…` items; CC BY-NC-SA images) | The text pages of *Directions between Plymouth and Falmouth* and *A description of the Coast of France* are there as images; editions ran to 1803. |
| Du Bocage, *Le Petit Neptune François: or, the French Coasting Pilot*, trans. Jefferys, 1761 | [archive.org](https://archive.org/details/bim_eighteenth-century_le-petit-neptune-franoi_du-bocage-georges-boiss_1761) (ECCO microfilm) | The French coast in English, with Bellin's improvements. |
| Bougard, *Le petit flambeau de la mer*, 1785 edition | [archive.org](https://archive.org/details/bub_gb_JQs1rDxYZcIC) | The French coasting pilot the two above descend from. |
| Faden, *Le Petit Neptune François; or, French Coasting Pilot*, 1793 | [archive.org](https://archive.org/details/lepetitneptunefr00fade), a second copy `lepetitneptunef00neptgoog` | Compiled for the Navy at the outbreak of war: 39 sheets of the French coast, three of coastal profiles, and directions for Brest, Ushant and the passages. The single most useful period text for the French half of the area; public domain. |
| Stephenson and Burn, *The Channel Pilot, comprehending the harbours, bays and roads in the British Channel*, 1795 | [archive.org](https://archive.org/details/bim_eighteenth-century_the-channel-pilot-compr_stephenson-john_1795) (ECCO microfilm, 170 MB PDF) | In period exactly, for the English side. |
| Serres, *The Little Sea Torch*, 1801 | Rumsey via Internet Archive (`dr_…11197…`), plate 13 for the Lizard to Rame Head | Coastal views: what a headland looks like from seaward at a stated bearing, which is what the lookout's "in sight of what" should be checked against. |
| Heather, *The New British Channel Pilot*, 4th ed. 1807 | Défense digital library (record found, **not opened**) | Heather's 1801 *Marine Atlas* and his Channel pilot were what a merchant master bought in Leadenhall Street. |
| Steel | Nothing open found. Penelope Steel's 1804 chart of the Channel from John Steel's 1802 chronometer survey survives with dealers; David Steel's firm published *Steel's Navigation Warehouse* charts from 1782. **Unverified** whether any library has scanned them. |
| Beautemps-Beaupré, *Le Pilote français*, I: *Environs de Brest*, 1822 | Défense digital library (record found, **not opened**); the printed sheets should be in SHOM's archive dataset | The French directions and tides for the Goulet and the Iroise, surveyed 1816–19. |
| La Barre, *The French Coasting Pilot*, 1825 | [archive.org](https://archive.org/details/frenchcoastingp00barrgoog) | An English rendering of the new French surveys. |
| Martin White, *Sailing Directions for the English Channel*, Hydrographic Office, 1835 | [archive.org](https://archive.org/details/sailingdirectio00whitgoog) | White surveyed the Channel for the Admiralty from 1810 into the 1830s; the first official directions, thirty years after the game's date but before most of the harbour works. |
| Norie, *The New British Channel Pilot*, 1839 (editions from the 1810s) | [archive.org](https://archive.org/details/newbritishchann00norigoog) | The commercial standard; earlier editions (1822, 1824) exist in libraries, none found scanned. |
| Walker, *Sailing Directions for the English Channel and Coast of France*, 1844 | [archive.org](https://archive.org/details/sailingdirectio01walkgoog) | |
| Imray, *Sailing Directions for the English Channel, the Bristol Channel and the South Coast of Ireland, with the Coast of France from Calais to Brest, including the Scilly Islands*, 1848 | [archive.org](https://archive.org/details/sailingdirection00unse_0) (Peabody Essex) | Its title page says it is compiled from Hurd, White and Denham "with those of Messrs. MacKenzie, Spence, Owen": the period surveys in a later, cleaner text, covering the whole M5 area in one volume. |
| Admiralty, *The Channel Pilot*, part I, 1859; 2nd ed. 1863 | 1863 at [archive.org](https://archive.org/details/channelpilotptn02changoog); 1859 at the Défense library (**not opened**) | The official directions, for checking the transits and the bottom notes. |

The lead's reading order for the feature list: Faden 1793 and Stephenson 1795 for the
words of the time; Imray 1848 and White 1835 for the completeness and the transits;
Serres 1801 for the views. Spence's Scilly description, if the manuscript is ever
photographed, would be the best thing of all for the islands.

## 5. Data model and pipeline

### 5.1 Coordinates

The game's plane is metres; a real sea is degrees. The chart layer should keep
geographic coordinates (WGS 84 latitude and longitude) as the world frame, because every
source is in them and because the Atlantic tier makes any local projection wrong
somewhere. The ship's motion each tick stays in metres and is converted at the end of
the tick (dφ = dy / R, dλ = dx / (R cos φ)); at 48–51°N the error of treating a
hundred-mile box as flat is a scale change of a few per cent between its north and south
edges, which is why the conversion is per tick and not per region. The viewer projects
for drawing. The one number the game has today for latitude (the sun) becomes the ship's
position.

### 5.2 Files

```
data/charts/
  manifest.yaml            regions, levels, every source with its licence text,
                           attribution line, URL, retrieval date and checksum; the
                           build's own version hash
  tiles/<level>/<lat>_<lon>.npz
                           depth raster tiles: int16 decimetres relative to chart
                           datum (approximately LAT), negative below, positive land,
                           nodata sentinel; plus a uint16 distance-to-shore field in
                           cells for the two finer levels; zlib-compressed numpy
  coast/<region>.geojson   the shoreline as polylines at each level's tolerance, each
                           piece tagged with its source and, where a period chart
                           overrides the modern shore, the sheet
  features/<region>.yaml   named things: hazards (rock, ledge, bank, drying), marks
                           (headland, tower, castle, church, beacon), lights (with
                           their date, so 1805 sees St Agnes and not the Bishop),
                           places (ports, anchorages, roads), transits and leading
                           lines (two marks and the bearing that clears a danger),
                           bottom notes; each with position, extent, height or
                           drying height, the period name and the modern one, a
                           source citation in the README's form, and a line the log
                           can say
  overrides/<region>/*.yaml
                           period depth and shore patches: polygons with a depth or a
                           drying height in the sheet's own units and datum, the
                           sheet, the control points used to georeference it, and
                           the datum correction applied; rasterised over the modern
                           grid by the build
```

Levels, in geographic cells so the same code serves every tier:

| Level | Cell | About | Use |
|---|---|---|---|
| 0 | 2.5′ | 4.6 km N–S | The world's picture and coarse depth |
| 1 | 30″ | 0.93 km N–S | The Atlantic: passages, landfalls at a headland's scale |
| 2 | 3″ | 93 m N–S, 60 m E–W at 49°N | A region: the M5 area whole, coast and approaches |
| 3 | 0.5″ | 15 m N–S | Harbour patches: Falmouth, Plymouth, Scilly, Brest |

A tile is 512 × 512 cells at its level; a region is whichever tiles exist at levels 2
and 3. A query asks the finest level that has a tile under the point and falls back to
the next. Adding a region later is adding tiles and a features file, nothing else.

*Note (package 38, 2026-10-09; spec M6 §26).* The runtime held one region until
milestone 6's first package: the manifest now has `charts:` (a chart names the regions
it holds and the corridor under them) and `corridors:` (level 1 over the voyage's water,
32 N to 51 N and 20 W to 1 W, from GEBCO at 30″, committed, with the distance field the
table above gave the two finer levels alone, so that a landfall over the corridor is a
landfall at a headland's scale), and a query asks the finest level across every region
of the chart before the corridor. "Adding a region later" is now exactly that, plus a
line in the chart's list; `docs/dev/ChartBlocks.md` says how. Two things the study did
not foresee: the levels' datums differ at a region's edge (LAT within, mean sea level
over the corridor: a step of a metre or two in deep water, said in the tuning notes), and
a region's distance field knows only its own block's shores, so the query reads the
corridor's field too where the region's tiles end within the distance it gives.

### 5.3 Disk

Raw int16, before compression; compressed sizes are a guess at a factor of two to four
(land tiles and flat deep water compress well, shelf edges do not):

- **M5 area at level 2** (3°×4° at 3″): 3,600 × 4,800 = 17 M cells, 35 MB raw, ten to
  fifteen compressed; with the distance field, about half again. Four harbour patches
  at level 3 of 15′ × 15′ each: 3.2 M cells and 6.5 MB raw apiece. The whole region
  under 60 MB raw, under 25 MB compressed: small enough to commit, and the lead
  recommends committing it so a clone plays.
- **The Atlantic at level 1** (100°W–20°E, 60°S–70°N at 30″): 14,400 × 15,600 = 225 M
  cells, 450 MB raw; land tiles dropped and the rest compressed, of the order of 150 MB.
  Not committed: fetched and built by the tool, or published as a release asset.
- **The world at level 0** (2.5′): 8,640 × 4,320 = 37 M cells, 75 MB raw, about 25 MB
  compressed. Also a candidate for committing, since it is the picture of the globe and
  the fallback under every other level.
- For scale: GEBCO's native 15″ world is 3.7 G cells and 7 GB; the game never carries it.

### 5.4 The build

`tools/build_charts.py`, run by a developer, not by the game:

1. **Fetch** each source named in a region's recipe into a cache outside the repository
   (GEBCO area extract, the EMODnet tile or tiles, HOMONIM, Histolitt, GSHHG), recording
   URL, date and checksum, and refusing any source whose licence is not in the allowed
   list (public domain, CC BY, Licence Ouverte, OGL, LGPL, and named per-source
   permissions); ODbL is not in the list.
2. **Resample** to the level grids (numpy; GDAL or rasterio may be used in the tool if
   installed, but the game's runtime dependencies stay `numpy` and `pyyaml`). EMODnet
   for level 2 and the coast, HOMONIM as a check on the French side, GEBCO for levels
   0 and 1, all converted to decimetres below chart datum with the datum shift each
   source states.
3. **Overrides**: rasterise each period polygon at levels 2 and 3 with its converted
   depth, and splice the period shoreline into the coast where an override says so
   (Plymouth without the breakwater; Falmouth without the docks). Where an override
   and the modern grid disagree in open water by more than a stated tolerance, the tool
   prints the place, because that is either a real change or a misread fathom.
4. **Derive**: the distance-to-shore field by a distance transform of the land mask at
   levels 2 and 3; a per-tile minimum depth; a spatial index of features by 0.25° cell.
5. **Write** tiles, coast, the manifest with the attribution block the game shows in
   its about text, and a report. A test checks that every feature and override cites a
   source and that every source in the manifest has a licence in the allowed list.

What is hand-made: the `features` files (read from the pilots and the sheets, in the
period's words, a few hundred entries for the M5 area) and the `overrides` (polygons
traced from the georeferenced sheets for the four harbours, a few dozen). What is
derived: everything else.

### 5.5 Queries per tick

- **Depth here.** Tile lookup by integer arithmetic on the position, nearest cell or
  bilinear between four; the current tile and its eight neighbours held in a small
  cache. Under a microsecond in numpy on one point; the lead reads it once when
  ordered, the grounding check reads it every tick.
- **Aground.** Each tick: if the tile's minimum depth exceeds the ship's draught plus
  the highest tide plus a margin, nothing more is done (the open-sea case, almost every
  tick). Otherwise depth at the keel's cells (bow and stern, since she may take the
  ground by the forefoot) against draught, heel and the tide's height from
  `Tides1805.md`; touching becomes an event with speed and bottom type, and the
  consequences are the hull's and the log's.
- **Nearest coast.** The distance field gives how far in one read; the direction from
  its gradient across the neighbouring cells, or, when the log wants a name, the
  nearest tagged coast piece from the features index. Read when the lookout is asked or
  on the roll-up's cadence, not every tick.
- **In sight of what.** Once a game minute: the features within the geographic horizon
  from the masthead (d in nautical miles about 2.08 (√h_eye + √h_object) with heights in
  metres), filtered by the 0.25° index, then by visibility and daylight from 5a and by
  the feature's own rules (a light at night, a castle by day, a view plate's bearing
  when the game has one). The result is the lookout's reading and the material for
  "take a bearing of".
- **The captain's chart.** A separate product built from the same features and coast,
  degraded as 5b decides (a chart of 1804 with its longitude error, a pilot's words
  instead of a grid), which is what the viewer draws. The truth tiles are never drawn.

## 6. Recommendation

1. **Sources for the M5 area.** EMODnet DTM 2024 (CC BY 4.0) for the level-2 depth and
   the general coast; SHOM HOMONIM (Licence Ouverte) as the French cross-check with its
   stated datum; GEBCO_2025 (public domain) for levels 0 and 1 and as the fallback under
   everything; Histolitt (SHOM–IGN credit) for the French shoreline where EMODnet's
   coast is coarse. No OSM in the tiles; no UKHO survey bathymetry until its licence is
   read, and probably never, since EMODnet carries it.
2. **Period data for the four patches.** Falmouth and Plymouth from the Hurd engravings
   of Mackenzie (RMG's free files to locate features; higher resolution by licence if
   soundings are to be read from them, or from a library copy), checked against Dummer
   1698 and White 1835; Scilly from the 1808 Hurd sheet of Spence; Brest and the Iroise
   from Bellin's 1773 Brest sheet and Ushant plan (Rumsey, Gallica) for the names and
   from the *Pilote français* of 1822 (SHOM archive, Défense library) for the depths.
   Facts transcribed, images never shipped.
3. **The feature list** from Faden 1793, Stephenson 1795, Imray 1848 and White 1835,
   with Serres 1801 for the views and the lights table dated so 1805 shows what 1805
   had. Each entry cites work and section in the README's form.
4. **The pipeline** as §5.4: one tool, a manifest with licences, an allowed-licence test,
   the region committed (under 25 MB), the Atlantic and world tiers fetched.
5. **Hand-made against derived.** Hand: features (some hundreds of lines of YAML) and
   overrides (a few dozen polygons). Derived: every tile, the distance fields, the
   coast outside the overrides, the indices. Estimated effort: the pipeline is a
   package of ordinary size; the four patches and the feature list are a week of
   reading and tracing that cannot be delegated to a grid, and are the "cool obscure"
   pillar made concrete.
6. **The path to the Atlantic.** No new code: GEBCO already covers it at level 1, GSHHG
   or Natural Earth give the world's coast at levels 0 and 1, and each new region of
   play is tiles at levels 2 and 3 plus a features file, built from EMODnet where Europe
   reaches, from NOAA's public-domain ENCs and Des Barres (LoC, free to reuse) on the
   American shore, and from NLS's Mackenzie 1776 for Ireland and the Hebrides. The cost
   is disk (about 150 MB compressed for the Atlantic tier, not committed) and, for each
   region that is to be sailed into rather than across, the same week of hand work the
   Channel needs. The world at level 0 costs 25 MB and comes for free with GEBCO; it is
   the dream's floor, not its ceiling.

## 7. What was not verified, gathered

The Défense library's records (Heather 1807, *Pilote français* 1822, *Channel Pilot*
1859) and Gallica's own catalogue answered nothing from the build network; SHOM's two
statements of the archive charts' licence conflict; the UKHO bathymetry licence text was
not read; GSHHG's tolerances, the GEBCO_2025 file size, the datum offsets between spring
low water and LAT at the four ports, Mackenzie's own datum statement, the *brasse* on
each French sheet, and the dates of the Seven Stones lightvessel and Le Créac'h are from
memory or secondary pages. Each is a morning's check from a browser when the M5b section
is written; none changes the recommendation.
