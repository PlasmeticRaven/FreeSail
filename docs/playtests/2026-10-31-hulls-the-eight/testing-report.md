# The eight hulls: testing report (31 October 2026)

For the owner, in place of your own first look (Build-Ships §5.6, §6). It covers the frigate-36, the brig, the merchant brig, the cutter, the lugger, the smack, the topsail schooner and the privateer schooner on their new drawn hulls, beside the 64 and the razee. Figures are measured at seed 7 on this tree, against 30413223, the tree before the step. The sheets are in `pictures/`, listed in its README.

**Nobody has sailed them in a live page yet.** The sheets are the game's own client drawing the game's own world in a headless browser. What they sail like has not changed: on a clean archive beside this tree, every log line, tick and dynamic of the eight is identical, and all ten polars are the same to the byte. Only the drawing moved, and the guns' height figures that nothing reads until the lee ports come.

You have seen the streams' sheets and called the hull work fantastic, and said the only things you see are from the existing rig not matching it. These sheets are drawn from the final files, after the rulings and the review, so a few things differ from what you saw (first section). The rig has its own section, with every item measured.

## What changed since the sheets you saw

- **The smack's body** now comes from Chapman's plate's own frames, not Steel's sloop. She draws 38 t against her file's 46 t, where she drew 53 t.
- **The schooners** stand on their own plate's lowest sill, 3 ft 1 in, not *Spider*'s 3 ft 5 in of 1835. Everything above the water came down about 9 cm. Her transom is about 38° from the upright; the "45°" was a chord that crosses no drawn line.
- **The cutter's stem head** is square across, where it drew as a pointed fin.
- **The picture's order** is mended: the figure no longer vanishes behind the head's plate, the deck's far edge has no saw-tooth near end on, and the frigate's forecastle bulkhead no longer lies across her deck.

## What you will see, hull by hull

- **Frigate-36** (sheets 10-12). The shared slab is gone. A long frigate's sheer, the waist open between a quarterdeck and a forecastle, a broad black wale down at the water, one quarter gallery, a square stern with two counters and five plain lights, a figure on the head. She is long: drawn 43.74 m at the water.
- **Brig and merchant brig** (20-22, 26). A deep sweep of sheer rising to both ends, flush from taffrail to head, a scroll head, a plain raked transom with no lights, the port band curving with the sheer. The two are one hull but for two of the merchant brig's ports, by your ruling.
- **Cutter** (30-32). Full and round in the bow, the stem head a box standing above the rail, thin rails and a long low band of ports amidships, a flat transom raked about 20° on a rounded tuck.
- **Lugger** (40-42). The one with the most character: high stepped rails at both ends and a low waist, a round stern with no counter, no head at all. Heeled, her full round body shows.
- **Smack** (50-52). Small and full for her length, a strong sheer with two bands of wale, a tall stem head, a small raked stern.
- **Topsail schooner and privateer schooner** (60-62, 66). Long, low and flush, with hardly any sheer: the stem raked hard with a small knee, the post raked, the transom low and raked, the port band reaching most of her length. One hull in two roles, by your ruling.

Sheet 01 has all ten at one scale, 05 under sail, 06 stretched so that only the lines differ, and 07 at the size the page's panel shows them.

## What each is drawn from, and how sure

| Hull | Drawn from | Rung | How sure |
|---|---|---|---|
| Frigate-36 | Her class's own lines: ZAZ2587, the contract draught, and ZAZ2559, *Amazon*'s copy, with frames and inboard profiles | S | Six sheets at about 5.4 px to the foot: a clean line to 0.05-0.1 ft between sheets, ±0.3-0.4 ft where lines cross and at the ends. No sheet marks the load line, so WL1 is a judgement, ±0.15 ft. The lights and the figure are judged, plain shapes |
| Brig, merchant brig | Her class's own lines, ZAZ4491 and ZAZ4492, with two sisters as checks | S | The best of the eight: scans of 100 px to the foot, ±0.05 ft. The load line is WL1, the faint ruled one, by the lead's ruling |
| Cutter | *Sherbourne*'s own draught, ZAZ6381, with ZAZ6382 and the as-built sheets | S | 15.6 px to the foot, 2-3 in. The load line is judged on measures. The as-built sheets are small previews |
| Lugger | Above the water, *Éclair* taken off afloat, ZAZ6306. Below it, *Le Coureur* on ZAZ6170, her type, scaled | S above, S† below | Her rail, plan and stem are her own. No body plan of her exists, so the body is another lugger's, scaled by the beams: drawn 2.53 m deep against the file's 2.1 m. Her line at her sheet's length, 18.33 m, is a departure from the scaling rule, said in her note |
| Smack | Chapman 1768, Pl. LIX No. 3, carried to her file's length and beam; Steel's coasting sloop kept as a check | S† | A type's plate, not her own lines. Her waterline, frames and stern are read off it in Swedish feet, as her note says |
| Both schooners | *Lynx*, by Chapelle 1930 fig. 17 and its plates, carried to the file's length and beam | S† | A later published drawing of her draught; three of her waterlines and the sill line by station |

The letter is her best source. The `marks` in each file are stricter, a line taking the word of its weakest point, so many of them say `judged` even on an S hull. That table is in Build-Ships §5.7.

## What the sheets disagree with

None of this moved: these are the figures the sailing stands on (§5.0 principle 8). One table of all of them is in `docs/dev/TuningNotes.md`, "The eight hulls", for you and a later package. The ones that matter most:

| | The file | The sheets | |
|---|---|---|---|
| **Brig: weight** | **413 t** | **303 t** | **−27%: the one to look at first** |
| Frigate: weight | 1,270 t | 1,448 t | +14% |
| Smack: weight | 46 t | 38 t | −18% |
| Schooners: weight | 211 t | 198 t | −6% |
| Frigate: keel at the middle | 4.6 m draught | 5.64 m | deeper by 1.04 m |
| Frigate: length at the water | 41.8 m | 43.74 m | |
| Brig: length; drag | 26.8 m; 2 ft | 28.00 m; 3.11 ft | |
| Cutter: length; drag | 15.2 m; 2 ft | 16.50 m; 3 ft | |
| Lugger: length | 16.8 m | 18.33 m | |
| Frigate's fore mast | +14.0 m | +16.59 m | 2.59 m abaft |
| Lugger's fore mast | +6.6 m | +7.90 m | 1.30 m abaft |
| Cutter's mast | +1.5 m | +2.63 m | 1.13 m abaft |
| Brig's fore mast | +8.9 m | +9.62 m | 0.72 m abaft |
| Schooners' rake | 11.3° both | 17.2°, 13.6° to the water | |
| Frigate's guns | 2.75 m apart | 2.97 m apart | up to 4.8 ft off the sheet's ports |
| Cutter's guns | three a side | four ports a side | three guns between four ports |

The guns stay where the file has them and each stands on a port written at its own place; the sheets' real ports are kept in each ship's module for the package that draws ports. The frigate's quarterdeck stays INCORRECT, as you ruled.

## Where the rig no longer sits right

You put your finger on it, and it is measured now. **One cause is under most of it.** The old hull's rail stood at the file's deck height, so the viewer brought every sheet and brace down to half the beam at that height, and they landed on the rail. The new rail is higher and the deck has gone lower: the frigate's rail at the middle went from 1.80 to 3.50 m, the deck at her side to 1.55 m. So the same ends now stop part-way down her side, or off it.

Two kinds, and I have kept them apart. **Viewer:** the drawing's own rule; nothing that sails reads it. **File:** a figure the physics reads, so it waits for a later package with the table above. **Moved by nobody now.** The rings are on sheets 12, 22, 32, 42, 52 and 62.

- **All of them: no shrouds, backstays, chains, deadeyes or channels are drawn at all**, and no bare stay; a stay shows only as the luff of a sail on it. The files carry these lines and the sheets show them. So nothing stands wrong against a channel yet, but whoever draws them must take the masts first: the sheets' channels stand to the sheets' masts. Viewer.
- **Frigate.** The spanker's boom runs straight through her stern, 1.83 m under the taffrail (ring 3): file. The mizzen yards' braces stop in the air under her counter, 2 m out from her rail (1), the courses' sheets 1.7-3.2 m down her side (2), and the fore course's weather sheet in the air past the stem (9): viewer. The fore mast 2.59 m abaft the sheet's place (5), and the main in the waist 0.44 m forward of the quarterdeck's break, where the sheet has it through the quarterdeck (4): file. Bowsprit 16.9° against the sheet's 19.5° (7), old 32.7°: the end's height is the file's, the heel the viewer's.
- **Brig and merchant brig.** The boom through the transom, 0.38 m under the taffrail (3): file. The main yards' braces stop 0.5-0.8 m off her side with no mast aft to lead to (1), the sheets 1.1-1.5 m down her side (2, 5): viewer. Fore mast 0.72 m abaft (4): file. Bowsprit 17.5° against 15.7° (6), old 32.0°, with the jib-boom steeper still at 19.0°.
- **Cutter.** The bowsprit runs dead level from the top of her stem head (3), since the file's end is lower than that; the sheet has it lower, at 5°, and your picture of the kit has it beside the stem. File and viewer. The mast 1.13 m abaft (2): file. The fore staysail's foot drops behind the rail and shows as a pale tab to leeward (4), braces and sheets 0.6-0.7 m down her side (1, 5): viewer. Her boom clears the taffrail: right.
- **Lugger.** Her raised rails stand over the lugs' feet: 0.67 m at the bow (5), 0.41 m aft (1): file. The mizen's sheet ends in the air 4.22 m past her stern (2), no outrigger being filed, and lowered the mizen yard comes out through her stern (8): viewer on the file's corners. The jib's tack is inside her bow, not on the bowsprit (7): viewer. Bowsprit level from the rail at the stem (6). Fore mast 1.30 m abaft, main 0.64 m forward: file.
- **Smack.** Bowsprit level from the top of her stem head, 0.85 m above the file's end (3). The staysail's and jib's tacks are 1.29 m under the rail at the stem, their feet showing over her side to leeward (2): viewer. Boom 0.11 m under her taffrail (4): file. Her mast is right.
- **Schooners.** The short bowsprit at 20° with the jib-boom at 8° makes an elbow (4), against the plate's one spar at about 10°, old 56°. The boom just lies on her taffrail, 0.02 m under (3): file. Staysail and jib tacks 0.86 m under the rail, showing as a tab (5), sheets 1.0-1.4 m down her side (1, 2, 6): viewer. Her masts rake 11.3° against the plate's 17.2° and 13.6° (7): file.

**What I would do, if you and the lead agree:** a small viewer step, reading the drawn rail and the stem head in place of the old deck height and half-beam for those three rules. It moves no file and no pin, and it mends the most of what you see. The boom heights, masts and rakes wait for the later package. I have not done it: this step moved no code for the rig.

## For your eye

None is a test failure. Tell me which matter:

1. The rig above: is the small viewer step wanted before the next ship? My pick is yes.
2. The three level bowsprits on the cutter, lugger and smack: my pick is to root them at the sheet's height with the small viewer step, not at the top of the stem head.
3. The far quarter gallery stands proud of the hull by up to 1.1 m on the frigate, and 1.2-1.3 m on the 64 and razee, seen from 150-172° off the bow. It is the plain box's width on a wide quarter.
4. A pale streak of deck under the schooners' transom, seen from 150° at about 8° of heel. No painter's order cures it.
5. Do the cutter and the smack read as two hulls to you? They are the closest pair the check found, 6.0 px apart on a 100-px drawing, the next the brig and the schooners at 6.5. The 4 px line is a judgement, to be re-set after your first sheet.
6. The lugs' feet to leeward come nearly to the water when she heels 12° (sheet 42). That is the old drawing's sag, not new, but her lower lee side shows it more.
7. The frigate's five lights and figure, and every gallery, are plain and judged.

Later, for your test when the lee ports come (L2): the cutter's sills at 1.00-1.23 m shut her lowest port at 14.5°, against the old 24.3°. A cutter's low freeboard may well be the truth of it. The schooners' lowest shut at 10.5°, and the privateer heels 8.5° in the check's lee broadside.

## What has not been done

- **Nobody has sailed them live**, and nothing here tests how they feel, since nothing about how they sail moved.
- **The ports are not drawn** (package 81); the bands stay plain.
- **The lee ports are not wired** (L2, L3): the sills are in the files, and nothing reads them yet. They are recorded port by port in the tuning notes.
- **The disagreements are not moved**, by ruling.
- **"Sixteen ports a side"** stays in the brig's description; her sheet has ten. It waits for SW-4, because digests and the primer carry the words.
- **The lugger's bowsprit** stays at 21.8 kN, where the rule's words give 37.4 kN. It waits for a tuning pass.
- **Not reached:** the frigate's deck sheets, the cutter's manuscript CHN0105, the brig's contracts. Sharper scans of the 1280-px sheets would be a licence from Greenwich; the drawing does not need them.
- **The trunk** has not been brought in again; that, and the final fast tier around it, come with the merge.

## Tests

The whole fast tier before the last mends: 5,750 passed, 1 failed, 2 skipped, 44:38. The failure was the work's: a test that asked the merchant brig's hull to equal the brig's to the byte, which your two-roles ruling makes untrue in her two ports alone; it was mended, the difference pinned. After the mends: the mended files with the slow tests, 1,129 passed; the guard sets 9, 265, 146, 68 and 184 passed; the picture tests in a real browser, 2 passed, thresholds unmoved. **Three captain's trials fail on this machine with or without this work,** the known difference from the build machine, and their figures are in the tuning notes once. One truth's band moved, by the lead's ruling: the brig's lowest sill, from Steel's 1.22-1.52 m to her sheet's 1.555-1.585 m.

## The figures

**Weight and depth** (drawn by the hull's own reckoning; file figures unmoved)

| | Drawn weight | The file | Off | Drawn depth, greatest section | File's draught | Rail at the middle, old then new | Deck at side, the middle |
|---|---|---|---|---|---|---|---|
| Frigate-36 | 1,448 t | 1,270 t | +14% | 5.05 m | 4.6 m | 1.80, 3.50 m | 1.55 m |
| Brig, merchant brig | 303 t | 413 t | −27% | 2.87 m | 3.5 m | 1.50, 2.54 m | 1.15 m |
| Cutter | 105 t | 106 t | −1% | 2.29 m | 2.6 m | 0.92, 1.58 m | 0.66 m |
| Lugger | 101 t | 101 t | 0% | 2.53 m | 2.1 m | 1.00, 1.50 m | 0.74 m |
| Smack | 38 t | 46 t | −18% | 1.45 m | 1.9 m | 0.76, 1.44 m | 1.00 m |
| Both schooners | 198 t | 211 t | −6% | 3.10 m | 3.3 m | 0.90, 1.87 m | 0.82 m |

**The lowest ports** (the heel that shuts them by the owner's rule, on heel alone)

| | Old sill, shut | New lowest sill | Shut | Lowest with a gun in it |
|---|---|---|---|---|
| Frigate-36 | 2.40 m, 21.0° | 2.19 m | 19.7° | the same |
| Brig | 2.10 m, 24.7° | 1.57 m | 17.5° | the same |
| Merchant brig | 2.10 m, 24.7° | 1.57 m | 17.5° | 1.62 m, 18.2° |
| Cutter | 1.50 m, 24.3° | 1.00 m | 14.5° | 1.03 m, 14.7° |
| Schooners | 1.00 m, 11.0° | 0.95 m | 10.6° | 0.96 m, 10.5° |

**The bowsprit's rise** (from the stem head to the file's end, then the jib-boom)

| | Old | New | Jib-boom | The sheet |
|---|---|---|---|---|
| Frigate-36 | 32.7° | 16.9° | 13.8° | 19.5° to K |
| Brig | 32.0° | 17.5° | 19.0° | 15.7° to WL1 |
| Cutter | 7.2° | level | none | 5.1° to the line |
| Lugger | 9.6° | level | none | 5.5° to the page |
| Smack | 9.1° | level | none | a spar about 2.37 m at the post |
| Schooners | 56.4° | 20.0° | 7.9° | 9.2-10.5° to the water |

**Where the lines end, against the rail** (plain sail; metres under the rail, and off the side at that height)

| | Courses' and fore-and-aft sheets | Braces with no mast aft | Head sails' sheets, on the side |
|---|---|---|---|
| Frigate-36 | 1.74-3.18, 0.14-0.51 | 3.54-3.67, in the air under the counter | 2.29 |
| Brig, merchant brig | 1.07-1.46, 0.07-0.77 | 1.31-1.46, 0.53-0.77 | 1.35 |
| Cutter | (main sheet to the taffrail) | 0.62-0.65, 0.14-0.38 | 0.69 |
| Lugger | 0.52, 0.07 (fore lug); main and mizen past the stern | none | 1.07 |
| Smack | (main sheet to the taffrail) | 0.66-0.68, 0.11-0.17 | 0.73 |
| Schooners | 0.97-1.40, 0.06-1.15 | none | 1.20 |

**The boom against the stern** (on the centre line; a minus is under)

| | Boom's height | Over the taffrail | Past the taffrail |
|---|---|---|---|
| Frigate-36 | 4.20 m | −1.83 m | 4.32 m |
| Brig, merchant brig | 3.30 m | −0.38 m | 4.36 m |
| Cutter | 2.40 m | +0.45 m | 3.63 m |
| Smack | 1.95 m | −0.11 m | 1.86 m |
| Schooners | 2.40 m | −0.02 m | 5.68 m |
| The razee, for comparison | 7.16 m | +0.01 m | 8.94 m |
