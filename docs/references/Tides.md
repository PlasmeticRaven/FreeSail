# The tide data's sources

What `data/tides/` is built from (spec M5 §16; the study `docs/design/Tides1805.md`;
package 34), source by source: what was taken from each, under what licence, and where
the licence text is kept. The rule is the charts' (`Charts.md`): **the facts are not
licensed, the files are**; the constants are copied as numbers with the dataset's
citation, and the period's figures are read from the books and cited by page.

## The world's tide: the harmonic constants

| Source | Taken | Licence | Text |
|---|---|---|---|
| **TICON** (Piccioni, Dettmering, Bosch and Seitz, "TICON: TIdal CONstants based on GESLA sea-level records from globally distributed tide gauges", Geoscience Data Journal 6, 2019; the data file PANGAEA doi:10.1594/PANGAEA.896587) | The M2, S2 and N2 amplitudes and Greenwich phase lags of the eleven gauges of `data/tides/constituents.yaml` (Newlyn, Devonport, Weymouth, Dover, St Mary's, Brest, Le Conquet, Roscoff, Saint-Malo, St Helier, Cherbourg), read from the dataset's own `TICON.txt` (the zip at doi.pangaea.de, fetched 2026-10-01), the stations found by their coordinates. The nodal corrections are the game's own (Schureman's f and u). | Creative Commons Attribution 4.0 International, as PANGAEA states for the dataset. | `licences/cc-by-4.0.txt` |
| **SHOM, Références Altimétriques Maritimes (RAM)** | The mean level above the chart datum (the ZH, lowest astronomical tide) of the French ports, which TICON's amplitudes about the gauge's mean level want to sit on the chart's datum: Brest, Le Conquet, Roscoff, Saint-Malo, Cherbourg. The British ports' offsets are from the study's figures and the UKHO's published datum differences (`constituents.yaml` says which are UNVERIFIED). | Licence Ouverte 2.0 (Etalab), as data.gouv.fr states for SHOM's RAM. | `licences/licence-ouverte-2.0.md` |
| **EMODnet Bathymetry DTM 2024** | Nothing new: the chart's datum, lowest astronomical tide, which the tide's heights are above (`Charts.md`). | CC BY 4.0 | `licences/cc-by-4.0.txt` |

The streams (`data/tides/streams.yaml`) are rates and directions by area, each entry with
its `source`: the headland table of Bowditch 1802 ('Of the Tides', the rates off the
Lizard, the Start and Scilly), the pilots' words (White 1835, Imray 1874, Faden 1793 for
the Four and the Fromveur), and modern summaries of the Admiralty tidal stream atlases
(NP250, NP255, NP257) as published on eoceanic.com, visitmyharbour.com and
figaronautisme.com with Ifremer's figures for the Iroise, read 2026-10-01; the atlases
themselves were NOT READ, and the file says so where a timing rests on a summary alone.
No image, table or text of any of these is copied: the figures are the facts.

## The captain's tide: the establishments

`data/tides/establishments.yaml` has two tables. `norie` is the establishment of the
ports as Dessiou's figures (with Daussy's for the French coast) stand in Whewell 1833,
"Essay towards a first approximation to a map of cotidal lines", Philosophical
Transactions 123, the table of pp. 147 to 236 (the Falmouth 5h 15m, Plymouth 5h 33m,
Brest 3h 48m, St Malo 6h 00m of the period's epitomes, Norie's among them: the Epitome
itself was not read, and the file says so). `moore` is the older table in points of the
moon's bearing (SW by W at Brest, W at Plymouth: Moore, *The Practical Navigator*, 1799,
'Of the Tides', forty-five minutes a point), and `minutes_per_day_of_age: 48` is Moore's
rule, "multiply the moon's age by 48 minutes". Both are facts of the period, cited by
work and page in the file, and nothing of either book is copied.

## What is not here

The UKHO's tide tables and the Admiralty tidal stream atlases are Crown copyright and
were not read; the SHOM atlas of the Iroise (the Fromveur's seven knots) was not read,
and the Fromveur's timing is from a summary and so marked. The study's open item 3
(spec M5 §33), the datum offsets of four British ports, is still open: `constituents.yaml`
carries the judgement figures with UNVERIFIED on each.
