# Milestone 5c close-out: what landed before gate 5c, and the compliance review

A record for the owner and the lead of the packages that landed between gate 5b
(passed 2026-10-01) and the cut of gate 5c (2026-10-02), what the lead changed between
them, the review of the build against the M5 specification whole, and what is handed on.
In the form of `M5-CloseOut-5b.md`; the specification keeps its pointer here.

## What landed

| Package | Builder | What | Where the record is |
|---|---|---|---|
| 33b | Fable | The moon (Meeus, checked against Horizons), the chronometer and the time sight, the lunar drawn and not computed, the amplitude and the azimuth for the variation; the chart in the captain's hands (a bearing and a distance by account, the dangers, a shaped course warning of a danger); the lookout's estimate held, dangers first, the lights by their range; Nare Point; truths 60 and 61 | the tuning notes "the chronometer, the moon, the lunar and the azimuth" |
| 33c | Opus | The readings asked at the prompt; the aliases; a mark by any of its words; belay by the order's words; the whole-ship groups; the article and the manoeuvre in hand in the dialect; the conflict rule's grain and the held lines once a watch (open item 15); the well held; the starter book a choice with primer chapter 11 and the forms tables | the tuning notes "the passage's words" |
| 33d | Opus | Completion under the browser's order line; the library and the ship's papers in a pane; the clock eased on a station; zoom and pan on the chart | `docs/design/Presentation.md`'s item built |
| 32c | Opus | The suite in two tiers (`--slow`), the days built once a run (`--dist loadgroup`), the fast tier on Linux and Windows in CI, the whole suite in the release workflow | the tuning notes "the suite in two tiers" |
| 34 | Fable | The world's tide (M2, S2, N2 at eleven gauges, the streams by area), the captain's tide by Moore's rule, grounding's consequences, anchoring as Luce has it with the ground tackle as parts; the passages ending at anchor; truths 62 to 64 and 66 | the tuning notes "the tide, the grounding and the anchor"; `docs/references/Tides.md` |
| 35 | Fable | Places, people, the papers by handle through the library to every station, Falmouth, Plymouth and Brest with the pilot from the cutter, the boat, the market, the yard, the crew pool and the stance, the nations table, `get under way`, `moor`, the kedge; truths 68 to 70; a determinism fault in the tide's shared table found and fixed | the tuning notes "places, people, papers, the ports and the nations" |
| 35b | Opus | St Mary's and Roscoff as port files; Roscoff's harbour patch from Bellin 1764, the region's tiles rebuilt | `docs/references/Charts.md`; `data/charts/unverified-checks.yaml` |
| 36 | Fable | Other sail at far detail on a polar from the file with the level-of-detail switch; the lookout sighting sail and making her out; the chase; the world-order channel journaled and replayed; the merchant passage and the naval cruise; the brig's two descriptions; the pilot's boat from the port's file; truths 67, 71, 72 | the tuning notes "other sail"; `data/scenarios/merchant-passage.yaml`, `naval-cruise.yaml` |
| 37 | Fable | The officer of the watch: the domain per order, standing orders by rank, the welfare detector for a station with authority, stand by with a wake condition, the handover note, the reseating once, the consent brief and the re-ask rule, the fitness drill, the identity header | the tuning notes "the officer of the watch"; `docs/agents/Harness.md` §13 |

Between them, the lead: the library's chapter list (chapter 10 was missed); the empty
later-events clause; a second `heave to` refused at the order; a yard's purchase at a
port without the item refused in the yard's words; the pilot's tide in his own words;
the two scenario fixtures in the slow tier; the suite's baseline count corrected (2089,
not 2097, at the 5b cut); the three passages re-pinned at each merge with the reasons.

## The compliance review against spec M5

The two rules of the chapter, checked in the code: **the world keeps the truth and the
captain keeps his account**: no reading gives a position, the tide's hour or another
vessel's place; the chart draws the account, the ellipse and each sighting by bearing
and estimate (`client/map.js`); the pilot's word on his port's tide is the one place the
world's tide reaches the captain, through a person, to the quarter hour. **Everything
inward reachable by an order or a reading; everything outward through something the
ship models**: a sail through the lookout, a letter by the boat, the gangway, the
messenger and the door, the news by the pilot, a world order never a line from nowhere
(truths 68 and 71).

| Spec | State at the cut |
|---|---|
| §9 to §13 | Built (32, 33a), as at 5b |
| §14 the sights | Built (33a, 33b): the noon latitude, the time sight, the lunar drawn, the amplitude and the azimuth; double altitudes not built |
| §15 orders and readings | Built; `come to an anchor` and `weigh` by 34; the readings at the prompt by 33c |
| §16 the tide | Built (34): three constituents at eleven gauges, the streams by area, the captain's tide by Moore's rule; the datum offsets at three ports still judgement (open item 3) |
| §17 the captain's chart | Built; `--casual` not built |
| §18 grounding and anchoring | Built (34); mooring with two anchors (35); the kedge by the boat (35); the hawse fouled not built |
| §19 truths | 58 to 72 pass; 73 to 76 as at 5b; the seven expected failures the owner's rulings |
| §22 places and people | Built (35): a name and a description, a person in one; the papers by handle |
| §23 ports | Built (35, 35b): five ports as files on one machinery; the pilot's vessel from the port's file (36) |
| §24 nations | Built (35): the table with the wars from memory, said so |
| §25 other sail | Built (36) at far detail with the promotion point; the crewed promotion M6's |
| §26 the world-order channel | Built (36): five channels, journaled and replayed, refused at the prompt |
| §27 scenarios | Built (36): the file whole; the merchant passage and the naval cruise |
| §29 the officer's watch | Built (37); the lead's watch and the verdict to come |
| §30 performance | The pace truth holds with the dozen ships on the sea (about three times the floor) |

## Findings of the cut, and where each went

- **A shared table's cached value depended on its first asker** (35's finding in 34's tide): fixed by evaluating at the cell's centre; the replay contract's one hole of the milestone.
- **A station's orders are not journaled** (37): they replay from the station's transcript, as the watcher's replies do, else a replay would give them twice.
- **The consent brief changed** (37): the re-ask rule names the sections; the owner runs the re-asks before any model is seated with authority.
- **A far-detail vessel sails over land between waypoints** (36): a bound to add before a scenario sails one along a shore (a ruling asked at the gate).
- **Open items added**: 16 (the GEBCO fill over the shore); 3 narrowed (the tide's constituents verified, three datum offsets not).

## The fold-in of m5c-c (2026-10-08)

Between the cut and the verdict the owner played ten games on the gate's build and, at
his word of 5 October, had the findings built locally in a copy of the gate with no
commits (`CHANGES-m5c-c.md`, the record of each package; decision 35). The review of
those games and the audit of the build are
`docs/playtests/2026-10-05-gate-5c-review/report-2.md` (its parts M and N are the
audit). The folder was taken whole on 2026-10-08 as the merge of a branch made at the
gate's commit, so that git carried the four commits made after the cut across it; the
games under `saves/` and the owner's notes stayed out.

| Package | What | Record |
|---|---|---|
| 37b, 37c | A session may come back to its station (decision 34); the wind-shift and taken-aback lines | `CHANGES-m5c-c.md`; the review's F1 |
| 37d | The build's stamp on a save and its checkpoint, the load's rule and `--replay-anyway`, three playtest checkpoints kept as tests; the lookout's distance judged afresh, the shore always a sighting, `take a fix` | the tuning notes "the saves, and the sight of land"; the review's F3 |
| 37e | The account: one rule by which an observation is believed, the doubt, the fix's choice of marks, the master's tide in the traverse, a course shaped to make good | the tuning notes "the account"; F4 |
| 37f | A ship hove to stays hove to; the anchors by name, the dragging line, the ground's words; the log's lines | the tuning notes "lying to, and the ground"; F5 |
| 37g | A key to each seating; the turn's budget in two counts; the stand-by's wakes; the two detectors; the deck to and fro; the general grant and its held-back list; the three ways of leaving; the consent brief revised once and leaner (decisions 36 and 37) | the tuning notes "the station's safety"; F6; `docs/agents/Harness.md` §13 |

What the lead changed at the fold-in, on the owner's seven rulings (decision 38):
`.gitignore` lets `tests/fixtures/saves/` through the `saves/` rule; `BUILD_NAME` is
`m5c-c` and the nine test lines that spelt the build's name read the constant; the
*Palinure* is put at 48 32 N 5 23 W, five leagues on the frigate's bow at seven, as the
audit tried it; the cruise's book makes a sighted sail out and lets the made-out line
give chase, where two chases in one second had made the second wear fail; and the
handling fault under the cruise's lost chase is mended in `_course_not_laid`: a chase or
a shaped course whose shorter turn passes through the wind's wake is a wear and she is
worn for it, as she already was for a turn through the eye (the tuning notes "the
fold-in of m5c-c"). A plain `steer` through the wind is left as the helm has always had
it, and is put to the owner: refused in words that name the wear, or worn without a
word.

The whole suite on this machine after the fold-in: 2984 passed, 8 expected failures
(seven rulings and the schooner's pilot); the fast tier 2733. Two of the recorded
passages pinned on the owner's Windows machine by 37d to 37f came out a tick or two
apart on Linux (the merchant passage and the 5b schooner, the frigate's agreeing): the
pins stand as Linux measures them, where the releases run, the difference is spec M5
§33's item 24, and `ci.yml` gained a manual run of the whole suite on both platforms so
the two can be compared without a gate.

Left as the audit found them, for packages after the fold-in (the review's part K): the
local runner's five faults (the reply cut off while thinking, tokens counted by the
server's figure, the handover reserve as a share, the oversize request trimmed, the
replay's line at a stand-down by the door); the amendments to 37e (the cast not beyond
doubt, the tide's height for the lead, the account worked at each board, the doubt on
one hand) and to 37f; the half-point course; 37h, the pilot; `the port` and `the depth
of water` still read from the truth; a far-detail vessel's leg across the coast (the
gate's ruling never given); the schooner's pilot and the lost beat it marks.

## What is handed on

To the gate's verdict: the owner's run and the lead's officer's watch (§29), the consent
question put to the lead's weights first. To milestone 6: the crewed promotion of a
far-detail ship and a rules-based captain, officers writing Python rules, the captain's
station, the officer bound to a person beyond the name. To milestone 7: colours as
deception, the private signal, prizes and convoys, the chase to windward, the smuggler's
run. To the launcher and installer line (decision 31): 32d, 32f, packaging at M8. The
open items of spec M5 §33 stand as numbered.
