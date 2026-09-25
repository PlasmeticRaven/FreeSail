# Reference texts

Public-domain seamanship sources kept in the repository so that ship data, the evolution catalogue and the in-game reference library can cite them by chapter and section, and so that LLM officers can be pointed at the same passage a human would read.

All five are optical-character-recognition (OCR) text dumps from Internet Archive scans. They are readable and searchable but not clean: expect occasional garbled words, stray characters from the scanner's language detection, and broken tables. Use them for research and citation, and check anything numeric against the page image (the PDF link in each item) before it becomes a game constant.

| File | Work | Source item | Notes |
|---|---|---|---|
| `luce/luce-1884-textbook-of-seamanship-ocr.txt` | S. B. Luce, ed. Aaron Ward, *Text-Book of Seamanship: The Equipping and Handling of Vessels under Sail or Steam*, 1884 | https://archive.org/details/isbn_9781296549435 | The edition the 1891 revision on maritime.org descends from. 37 chapters plus appendices. Steam chapters (XV, XXXV) are out of scope. Chapter list is at line 184 of the file. |
| `luce/luce-1866-seamanship-1877-printing-ocr.txt` | S. B. Luce, *Seamanship, compiled from various authorities*, 1866 (1877 printing) | https://archive.org/details/seamanshipcompf00lucegoog | Earlier and closer to sail-only practice. Its table of contents lists the sub-topics of every chapter, which the 1884 scan does not; use it to find things, then read the passage in either edition. |
| `lever/lever-1827-young-sea-officers-sheet-anchor-ocr.txt` | Darcy Lever, *The Young Sea Officer's Sheet Anchor*, 1827 printing (first published 1808) | https://archive.org/details/youngseaofficers00leve_0 | Squarely in the game's period. Organised as numbered figures; the text refers constantly to plates that are not in the OCR, so read alongside the scan when the geometry matters. |
| `chapelle/chapelle-1930-the-baltimore-clipper-ocr.txt` | Howard I. Chapelle, *The Baltimore Clipper: Its Origin and Development*, 1930 | https://archive.org/details/baltimoreclipper00howa | Published in the United States in 1930 and in the public domain there from 2026. The standard work on the type: plans, dimensions and spar tables for named Baltimore-built schooners of 1790 to 1820, the source for the reference schooner's particulars. |
| `falconer/falconer-1780-universal-dictionary-of-the-marine-ocr.txt` | William Falconer, *An Universal Dictionary of the Marine*, 1780 edition (first published 1769) | https://archive.org/details/universaldiction00falc | Glossary source for part names and period usage. The 1815 Burney revision would be the ideal edition; substitute it if a clean scan is found. |

A cleaner human-readable transcription of Luce's 1891 edition is at https://maritime.org/doc/luce/index.php. It sits behind a browser check that automated fetching does not pass, so it is not mirrored here; it is the better text to read in a browser.

## How to cite in data files

Cite the work, chapter and sub-heading, not a line number in the OCR (line numbers change if the text is ever cleaned). Example, in an evolution file:

```
source: "Luce 1866, ch. XXIV Working to Windward, 'Tacking'"
```

`LuceChapterMap.md` in this folder maps the chapters to the game systems they feed.
