# Milestone 5b close-out: what landed before gate 5b, and the compliance review

A record for the owner and the lead of the packages that landed between gate 5a and
the cut of gate 5b (2026-09-30), what the lead changed between them, the review of the
build against the M5 specification as far as 5b's first half (decision 29), and what is
handed on. Written in the form of `M4-CloseOut.md`; the specification keeps its pointer
here rather than growing "as built" paragraphs (the cold review's process point, adopted).

## What landed

| Package | Builder | What | Where the record is |
|---|---|---|---|
| 31b | Fable | All hands manned in parallel with a party bound on any one job; the heavy-weather routine's order of work (the close reef first; the day under systems loses nothing); parted running rigging rove afresh or spliced; the brace line with yards on deck; chapter 9 free of the gate's day; the pinned form under the air-mass rule with the milestone 2 draws retired | `docs/dev/TuningNotes.md` "all hands in parallel"; spec M5 §3 |
| 31c | Opus | A sample carries only what changed (the gate's day's samples 105,000 to 44,000 tokens, the digest unchanged); the Desktop door's wait at 200 s; six weather events to stand by for; `tell`/`ask` a station inside a standing order; the journal while standing by; a bell in flight; the release line; the unattended wait in ten real minutes only, on every driver's clock (the cold review's one bug); the candour sentence | `docs/agents/Harness.md`, `ConsentBrief.md` (its hash moved to `e99d6bbb4f9771cf`) |
| 32 | Fable | Latitude and longitude as the world frame with the plane kept; the chart data of the western Channel (the region's tiles committed, 17 MB; the world and the Atlantic built by the tool); the four period patches and the feature list of two hundred entries; the build tool with its licence check; depth, aground, the coast and what is in sight; the sea breeze and coastal fog wired; the lookout's hails; the chart in the browser; truth 65 | `docs/references/Charts.md`; `data/charts/manifest.yaml`; the tuning notes' M5b section |
| 32b | Fable | The cutter *Sherbourne* and the brig *Harpy* as ship files from Fincham's and Steel's rules; the running bowsprit; the orders' grammar swept across four ships (the brig's wear and heave-to fixed in the scripts by place, `reef the bowsprit` by spar class, a part's name in the dialect followed by its comparison); truths 73 to 76 | `docs/design/VesselCandidates.md`; the tuning notes "where the four ships stand" |
| 32e | Fable | Yaw that scales with the vessel and the rudder's lift by its blade; Luce's recovery when she hangs in stays and the squaring as a brace; the headsail sheets held to windward; the sheet holds the trim, the free tending retired into evolutions with a tending routine in the starter book; a course refused while hove to; turning circles and the small vessels' tacks as truths | the tuning notes "staying and sheets"; `tests/test_staying.py` |
| 33a | Fable | The reckoning with its covariance and the study's error terms; soundings, bearings and the noon sight as lines and points; the master as the first named person; the readings and log lines of the study; the captain's chart with the truth gone from the snapshot; the checkpoint save proven against the replay (a load in a twentieth of a second against a sixteen-second replay); the passages of gate 5b; truths 58 and 59 | the tuning notes "the reckoning"; `data/scenarios/gate-5b-passage*.yaml` |

Between them, the lead: the dialect reading `the land` and `the depth of water` (32's two hunks, after 31c landed); the four cutter and brig order-table rows after 31b's wording; `tools/chart_manifest.py` (spec §20's tool); truth 73's test as the owner reworded it; a standing order's firing on a cadence as a routine line (32e's tending routine had put fifty-seven notable lines in a day); a course refused while a heave-to is in hand as well as after it (the starter's "keep her full" fired in the twenty seconds between the order and the yards aback, on every passage); the events `tacked` and `wore`; the passage's book amended (the lead every ten minutes closing the land, the ship wearing at the outer road to lie to on the seaward tack, the thick passage standing off from the land close aboard); the passages' constants re-pinned after 32e's physics. Packages 32c (the suite in two tiers, a Windows job) and 32d (the `freesail` command and the setup step) are written for the owner's local sessions and are not in this cut.

## The suite

At the cut: see the gate report's setup line. Truths 1 to 59, 65 and 73 to 76 pass; the seven expected failures are the owner's rulings (truths 3, 11, 18, 24, 26, 28, 31), unchanged since milestone 3b. Truths 60 to 64 and 66 (the chronometer, the lunar, the tide, the grounding by account) are gate 5c's set with 33b and 34; 67 to 72 are 5c's.

## The compliance review against spec M5

The two rules of the chapter, checked in the code: **the world keeps the truth and the captain keeps his account**: the snapshot the browser receives carries the reckoning and its ellipse and no `position` (`api/queries.py`; `client/map.js` draws only the account); the truth is read by the tests from the world and by `tools/day_log.py --reckoning` as the author's view; no reading gives it (`the reckoning` says "by account"). **Everything inward reachable by an order or a reading; everything outward through something the ship models**: the lookout's hails, the lead's cast, the noon sight and the bearing are the outward arrivals of this gate, each a log line and a reading.

| Spec | State at the cut |
|---|---|
| §2 systems, §3 gusts and squalls, §4 the sea and the motion, §5 the readings (5a) | Built (30, 31), the gate 5a rulings built by 31b: the pinned form under the air-mass rule, the sea's cost answered by the hands. Open: the frontal trough (§33 item 9), the wave-growth sources (item 8) |
| §9 the frame | Built (32): `Position` on the sphere whose minute is the mile; the plane kept for the scenarios without a position |
| §10 the chart data | Built (32): the region's tiles, coast, features and overrides committed; the world and the Atlantic by the tool, as the spec says; every source's licence in the manifest; the study's unverified list checked and recorded. HOMONIM not cross-checked, Histolitt not used (the manifest says so). The scans read at display size only: every override says what it rests on |
| §11 queries | Built: depth, aground (the tile's minimum short-circuit; `tide_m` 0 until 34), the coast and its name, in sight of what; the coast hook wired for the sea breeze and the fog |
| §12 the lookout | Built: the hails, the readings, the events; a station for it is §33 item 6 |
| §13 two positions | Built (33a): the covariance, the error terms named with their sources, the observations as lines and points; tuned to the study's 30 to 50 miles after four days (39 × 9) |
| §14 the sights | The noon latitude built; the chronometer, the moon and the lunar are 33b's (gate 5c's set by decision 29) |
| §15 orders and readings | Built but for `come to an anchor` and `weigh` (34) and the chronometer's and lunar's readings (33b); the standing dialect reads the new rows for nothing |
| §16 the tide | 34 (gate 5c's set) |
| §17 the captain's chart | Built: the reckoned position, the ellipse, the track by account, the noon positions, the bearings, the soundings; the truth gone from the snapshot; `--casual` not built |
| §18 grounding and anchoring | Taking the ground is an urgent line and a stop (32); consequences and the anchor are 34's |
| §19 truths | 58, 59, 65 pass; 73 to 76 pass (73 as reworded); 60 to 64 and 66 wait on 33b and 34 |
| §20 gate 5b | The passages as revised: clear and thick in the frigate, the schooner, the cutter and the brig through the same orders; the chart in the browser; the manifest tool; the checkpoint; `--load` and the climatology days carried; the numbers pinned |
| §23 the cutter, §25 the brig | The files built (32b), pulled forward; their use by the pilot and at far detail is 35's and 36's |
| §30 performance | The pace truth holds on the passage with the region loaded (the queries cost nothing the measure can separate from noise) |

## Findings of the cut, and where each went

- **A ship hove to forereaches on to the land.** On every passage the ship, hove to on the tack she arrived on at the first shoal cast, forereached on to the Roads' banks (the frigate in four minutes, the schooner in an hour). The true answer is the anchor (34). Until then the passage's book wears her at the outer road and heaves her to on the seaward tack, and the gate report asks the owner to rule on that ending. The events `tacked` and `wore` were added so the book can wait for the wear.
- **A course order in the heave-to's window.** The starter's "keep her full" fired between "heave to" and the yards aback, on every passage; the refusal 32e built for a ship lying to now holds while the manoeuvre is in hand too.
- **The conflict rule's grain.** `heave the lead` and `wear ship` are logged as "contrary orders on the ship" by the standing runtime's conflict rule, which treats every ship-subject evolution as one part; the lines are routine and the lead still goes. An open item for the standing runtime (spec M5 §33, item 15).
- **The `at a sounding, if ...` rule's held lines.** Every cast after the deep-sea one logs a routine "not carried out" line for the fill-away rule whose if-clause fails; the log's routine tier carries them. Open item 15 with the above.
- **Cadence firings.** A standing order's firing on `every` is now a routine line; the 5a day's digest moved with it, re-pinned.
- **The variation is provisional** (§33 item 14); an azimuth is put to the owner at the gate.

## What is handed on

To 33b: the chronometer, the moon and the lunar; the readings and the log lines of §15 they carry; truths 60 and 61. To 34: the tide and the set it gives the reckoning (`SET_DOUBT_*` become the world's stream against the captain's allowance), grounding's consequences, anchoring and weighing, the port's mooring; truths 62 to 64 and 66. To 35: the pilot boarding from the cutter, the places and people whole. To 36: the brig at far detail. The open items of spec M5 §33 stand as numbered, 15 added here.
