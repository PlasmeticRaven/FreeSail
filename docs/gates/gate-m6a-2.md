# Gate M6a-2: the fixes from the owner's first runs

**Verdict:** not cut. The owner's word of 2026-10-15: the gate is folded into the milestone's
last (gate 6c, at the end of M6's work), his runs of 2026-10-13 to 15 on package 45's build
(`docs/playtests/2026-10-13-gate-m6a-2-owner-runs/`) standing as its runs. The document stays
as drafted for that gate's items. It was to be a small gate on gate m6a's document carrying the
fixes the owner's runs of 2026-10-11 brought
(`docs/playtests/2026-10-11-gate-m6a-owner-runs/`; package 45 in
`docs/dev/M6-WorkPackages.md`). The verdict of m6a and of this gate are the owner's
together: m6a's items stand as run, and the items below are the runs that prove the
fixes.

**What changed since `m6a`** (package 45; the detail in its merge record and its section
of `docs/dev/TuningNotes.md`):

- The pictures reach the model and are not blank: the chart and the ship's view drawn on
  fixed offscreen canvases with their own backgrounds; `chart` takes a span (harbour,
  coast, passage, whole), centred on the account; a shelved picture's stub says it was
  shown and put back.
- The chart whole in play: a scenario's `region:` is the region she starts in on the whole
  `atlantic-east` chart; the browser's chart and the picture show every block as built and
  the Western Islands; the map culls and decimates its coast so the page stays quick.
- Courses and intents by way of marks: `shape a course for Lisbon via Ushant and
  Finisterre`, and an intent's `via`.
- The helm full and by with the yards braced sharp up keeps her way; the pilot aboard
  fixes her by his marks, names the hand and the mark, and takes the conn on `let the pilot
  take her in`; the merchant captain goes in as far as the wind serves and does his
  business from the road; tack or wear by the state of her sail; sail made again after the
  gale; the glass as a stimulus; the storm sails stand their gale. *(The items of Part B as
  merged are listed in the merge record; any left undone is named there.)*

## What you need

As gate m6a: Python 3.11 or newer (`py`), the gate zip from the release `gate-m6a-2`
extracted to a fresh folder (or the branch `gates/m6a-2`), and Claude Desktop or the API
door for the wardroom items.

## Setup

```
py -m pip install -e ".[dev,server,agents]"
py -m pytest -n 4
```
*The fast tier; the count is the merge record's ("Package 45, as merged").*

## Items

Each on the playtest form in `docs/playtests/README.md`, every surprise written down
whether or not it is a fault.

- [ ] **1. The helm full and by, both ways.** On any trial or the merchant passage: `brace
  sharp up` then `keep her full and by`, a quarter hour; then `trim sails` and the same.
  *She keeps her way braced sharp up (four knots and more in fifteen) and is never aback;
  after `trim sails` she lies as 37p measured her, six points off and a little slower.*
  The owner's note 1 and 1b.
- [ ] **2. The gale and the lee shore again** (`trial-station-gale`, `trial-station-lee-shore`).
  *No storm sail blown out through the gale; where she must go about under short sail she
  wears, the log saying the choice and why; after the gale she makes sail again whatever
  her state and bends new headsails where the old blew out; never aground.* Notes 3 to 7.
- [ ] **3. The merchant's business** (`trial-trade-stranger`, `trial-trade-thick`,
  `merchant-intent`). *One anchor where the wind serves no further, and the boat does the
  business from the road; the entrance made when the wind is on the beam.* Notes 8 to 11.
- [ ] **4. The pictures.** The wardroom game through Claude Desktop or the API door with the
  browser's page open: `chart` at each span and `ship_view` from two facings, asked by the
  model and read by you in the same page. *The model describes what the picture shows and
  the picture is what you see; shelved, its stub says it was shown; asked again, it comes
  again.* The wardroom note 1.
- [ ] **5. Brest with the pilot given the conn.** `merchant-passage` to the Goulet:
  `let the pilot take her in` at the pilot's boarding, and watch. *The pilot's fixes by his
  marks in the log, his warnings naming the hand and the mark, his conn through the Goulet
  to the anchorage; `I have the conn` takes her back.* The wardroom note 2.
- [ ] **6. The chart whole, and a passage of your own.** Any scenario: the browser's chart
  zoomed out to the whole, every block and the islands drawn, and in to a harbour. Then a
  passage of your own from Falmouth into Biscay or to Lisbon, by `via` marks or your own
  courses, the chart followed the whole way across the seams. *Nothing odd at 48 N or
  45.9 N; the pilot, the market and the anchorage at the far end as at Falmouth.* The
  wardroom note 3, and the question of every charted place (the answer in §26's "the
  chart in play" note and the merge record).
- [ ] **7. Funchal to Angra**, if the evening allows (`data/scenarios/azores.yaml`): the
  frigate across the widened corridor by the log and the noon sight. *The landfall on
  St Michael's, the Peak of Pico raised at thirty leagues or more in clear weather, the
  anchor in Angra Road.*

## The report

The verdict and the rulings go in this document and in `docs/DesignProposal.md`; the
playtest records under `docs/playtests/`.

## What this gate does not do

Nothing new of the milestone: packages 43, 43b and 44 wait on this gate as they waited on
m6a. The land-avoiding route for the planner, the blend of the held gauges and the deep-sea
tiles' rule are open items of the chart line, not this gate's.
