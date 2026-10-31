# The pictures of the eight hulls' testing report

Every sheet is drawn by the game's own client (`client/projection.js`, `client/shipview.js`, `client/style.css`) in a headless browser. The sailing states come from the game's own world at seed 7: 15 knots from the north, heading east, "set plain sail" and "brace sharp up on the larboard tack", 500 ticks on (3,600 for the merchant brig, whose few hands take longer). **Old** is the file and the viewer at 30413223, the tree before the hull step. **New** is the file and the viewer as they went into the step's one commit. The hull-alone cells are the same files with only the hull's figures drawn.

No Greenwich image and no picture of the owner's is on any sheet, nor any crop of one. The sheets they are measured from are cited by number in `docs/design/ships-design/`.

The bright orange lines are lines being worked at that moment, the braces in the trim; at rest they are the faint grey ones. Each cell's head gives its scale in pixels a metre. The red rings on the close sheets are laid over the drawing afterwards and are not the game's.

## All ten at one scale

| Sheet | What it shows |
|---|---|
| `01-all-ten-hulls-abeam-one-scale.png` | The ten hulls alone, abeam, at 14 px a metre, each with the rung of her lines under her name: the sheer, the ends and the wales |
| `02-all-ten-hulls-quarter-one-scale.png` | The same on the quarter at 135°: the sterns' shapes and the quarter galleries |
| `03-all-ten-hulls-ahead-astern-one-scale.png` | The same ahead and astern at 17 px a metre: the sections, the tumblehome, the transoms and lights |
| `04-all-ten-hulls-heeled-one-scale.png` | The same heeled 10° and seen from windward, what heel lifts out of the water |
| `05-all-ten-plain-sail-one-scale.png` | All ten whole under plain sail, abeam to leeward, at 7.2 px a metre |
| `06-all-ten-hulls-normalised.png` | The ten stretched to one length, beam and freeboard at the middle, so that only the lines differ: abeam, ahead, astern. The brig and merchant brig, and the two schooners, are the same hull by your ruling |
| `07-all-ten-in-the-pages-panel.png` | All ten in the page's panel at the built-in 800 × 600 window, 418 × 169 px at actual size, furled and under plain sail: what shows in play |

## Hull by hull, old beside new

The hull sheet has the hull alone abeam, on the quarter, ahead, astern, and heeled 10° from windward. The plain-sail sheet has her whole abeam, on the quarter, ahead and astern. Each row is at one scale. The brig's hull sheet stands for the merchant brig and the topsail schooner's for the privateer: one class in two roles, and only two of the merchant brig's ports differ.

| Sheet | What it shows |
|---|---|
| `10-frigate-36-hull-old-new.png` | The frigate alone, the shared hull beside the *Amazon* class's lines: open waist, quarterdeck and forecastle, one gallery, five plain lights, the figure |
| `11-frigate-36-plain-sail-old-new.png` | The frigate under plain sail, old beside new |
| `20-brig-hull-old-new.png` | The brig alone, the shared hull beside the *Diligence* class's lines: a long sweep of sheer, the scroll head, a raked plain transom |
| `21-brig-plain-sail-old-new.png` | The brig under plain sail, old beside new |
| `26-merchant-brig-plain-sail-old-new.png` | The merchant brig under plain sail, old beside new: the brig's hull |
| `30-cutter-hull-old-new.png` | The cutter alone, the shared hull beside *Sherbourne*'s own draught: the full round bow, the stem head a box above the rail, the flat transom raked about 20° |
| `31-cutter-plain-sail-old-new.png` | The cutter under plain sail, old beside new |
| `40-lugger-hull-old-new.png` | The lugger alone, the shared hull beside *Éclair*'s sheet: the stepped rail, the round stern, no head |
| `41-lugger-plain-sail-old-new.png` | The lugger under plain sail, old beside new |
| `50-smack-hull-old-new.png` | The smack alone, the shared hull beside Chapman's plate: the high stem head, two bands of wale, the raked rounded stern |
| `51-smack-plain-sail-old-new.png` | The smack under plain sail, old beside new |
| `60-topsail-schooner-hull-old-new.png` | The schooner alone, the shared hull beside *Lynx*'s plate: long, low and flush, the stem raked hard, the transom raked about 38° |
| `61-topsail-schooner-plain-sail-old-new.png` | The topsail schooner under plain sail, old beside new |
| `66-privateer-schooner-plain-sail-old-new.png` | The privateer schooner under plain sail, old beside new: the schooner's hull |

## Where the rig no longer sits right, close

New file on the new viewer only. Each sheet has six cells; a ring marks a place measured. **V** is the viewer's own rule, **F** a file figure the physics reads. The figures are in the report and in `docs/dev/TuningNotes.md`, "The eight hulls".

| Sheet | The rings |
|---|---|
| `12-frigate-36-rig-close.png` | 1 the mizzen yards' braces ending in the air under her counter (V). 2 the courses' sheets ending part-way down her side (V). 3 the spanker's boom through her quarter and taffrail (F). 4 the main mast in the waist, forward of the quarterdeck's break (F). 5 the fore mast, 2.59 m abaft the sheet's place (F). 6 the jib sheets' end on her side (V). 7 the bowsprit's rise, at the stem head and on the spar (F and V). 8 a fore lower studding-sail boom, low against the rail (F and V). 9 the fore course's weather sheet ending past the stem, in the air (V) |
| `22-brig-rig-close.png` | 1 the main yards' braces ending off her side (V). 2 a course's sheet (V). 3 the boom through her transom, under the taffrail (F). 4 the fore mast, 0.72 m abaft the sheet's place (F). 5 the jib sheets' end (V). 6 the bowsprit's rise (F and V). 7 a fore lower studding-sail boom (F and V). 8 the fore course's weather sheet past the stem (V) |
| `32-cutter-rig-close.png` | 1 the braces' ends (V). 2 the mast, 1.13 m abaft the sheet's place (F). 3 the bowsprit level from the top of the stem head (F and V). 4 the fore staysail's foot under the rail (V). 5 the staysail and jib sheets' end (V). The furled cell shows her boom clear of the taffrail: that one sits right |
| `42-lugger-rig-close.png` | 1 the main lug's foot under the raised after rail (F). 2 the mizen lug's sheet ending 4.22 m past her stern, in the air (V on F). 3 the main lug's sheet (V). 4 the mizen mast's foot, abaft her deck's end (V). 5 the fore lug's foot under the raised bow rail (F). 6 the bowsprit level from the rail at the stem (F and V). 7 the jib's tack inside her bow (V). 8 the lowered mizen yard through her stern, furled (V on F) |
| `52-smack-rig-close.png` | 1 the yards' braces' ends, faint (V). 2 the staysail and jib tacks under the rail at the stem (V). 3 the bowsprit level from the top of her stem head (F and V). 4 the boom under her taffrail (F). 5 the head sails' sheets' end (V) |
| `62-topsail-schooner-rig-close.png` | 1 the fore sail's two sheets' ends (V). 2 the fore topsail's sheets' ends (V). 3 the boom at her taffrail (F). 4 the bowsprit at about 20° and its elbow at the jib-boom (F and V). 5 the staysail and jib tacks under the rail (V). 6 their sheets' end (V). 7 the fore mast's rake (F) |
