# Gate M6c: Other ships with captains, the regatta, and the fixes of m6a-2 (the milestone's last)

**Verdict:** open. The build `m6c`, to be cut at package 42b's merge, the milestone's last
(branch `gates/m6c`, tag `gate-m6c`, the release's zip), after packages 45 and 45c (the
fixes from the owner's runs of m6a), 43 (other ships with captains), 43b (the lugger and
the smack, the world's business, the ports' faults), 44 (the regatta, the trims by a point
of sail, the parity tests) and 42b (the consent brief revised for 6c). Gate m6a-2 was not
cut (the owner, 2026-10-15): its items are here, the owner's runs of 2026-10-13 to 15
(`docs/playtests/2026-10-13-gate-m6a-2-owner-runs/`) standing for those of them he has
already run. The verdicts of m6a, m6a-2 and this gate are the owner's together, and the
milestone closes on them; the director's milestone (`docs/TechnicalSpec-M7b.md`) follows.

**What this gate proves** (spec M6 §18, §25): a ship beside the player's is the same ship,
crewed, commanded by the rules or by a model, sailed under the same physics; the world
peoples itself with business; and the game measures its players, rules, local, hosted and
human, on one course.

**What changed since `m6a`**, in short (the detail in each package's merge record in
`docs/dev/M6-WorkPackages.md` and its section of `docs/dev/TuningNotes.md`): the pictures
drawn right and put back only by the model's hand; the chart whole in play; `via` marks; the
helm braced sharp up; the pilot who fixes her, names the hand and takes the conn; the
merchant's entry and his business from the road; tack or wear; sail after the gale by
steps; the glass as a stimulus; the storm sails; the naval cruise restored and the chase
rule mended; the Goulet's track; the ghosted boat and `--load --until`; the world orders
kept for the record only; the stations keyed to the person; the far-detail brain and the
crewed promotion with the cap of three; a station on another ship across the switch; the
seat hook and the live world order `world: ...`; the lugger and the smack; the world's
business and the quay's rumours; the regatta with its first table; the trims by a point of
sail; the parity tests.

## What you need

Python 3.11 or newer (`py`), the gate zip from the release `gate-m6c` extracted to a fresh
folder (or the branch `gates/m6c`), Claude Desktop or the API door for the model items, a
local runner for the regatta's local agent if you have one, and the re-asks run after 42b's
revision before any model is seated.

## Setup

```
py -m pip install -e ".[dev,server,agents]"
py -m pytest -n 4
```
*The fast tier; the count is the merge record's ("Package 43b, as merged": 3,293).*

```
py -m pytest tests/test_captain_trials.py tests/test_known_truths.py --slow -n 4
```
*The trials and the known truths; every pin as the merge records have them; the expected
failures the rulings' and the lead's.*

## Items

Each on the playtest form in `docs/playtests/README.md`, every surprise written down whether
or not it is a fault. Items 1 to 7 are gate m6a-2's; the owner's runs of October stand for
those he has run, and he says which.

- [ ] **1. The helm full and by, both ways.** `brace sharp up` then `keep her full and by`;
  then `trim sails` and the same; then `trim for close hauled` and the same. *She keeps her
  way braced sharp up; after `trim sails` she lies six points off; the point's trim gets her
  on course without going aback, and `trim sails` finishes the job.*
- [ ] **2. The gale and the lee shore again** (`trial-station-gale`, `trial-station-lee-shore`).
  *No storm sail blown out; wearing under short sail with the reason said; sail made again
  by steps after the gale; never aground.*
- [ ] **3. The merchant's business** (`trial-trade-stranger`, `trial-trade-thick`,
  `merchant-intent`). *One anchor where the wind serves no further, the boat from the road;
  the let-go stood back from too little water.*
- [ ] **4. The pictures.** The wardroom through Claude Desktop or the API door with the
  page open: `chart` at each span and `ship_view` from two facings. *The picture is what you
  see; put back only by the model's hand with its note; asked again, it comes again.*
- [ ] **5. Brest with the pilot given the conn.** `merchant-passage`, or the wardroom save
  of m6a loaded `--until 113000`: `let the pilot take her in`. *His fixes by his marks, his
  warnings naming the hand, his conn through the Goulet with the set allowed for, the berth
  in the Bay; `I have the conn` takes her back.*
- [ ] **6. The chart whole, and a passage of your own** across the seams, by `via` marks or
  your own courses. *Nothing odd at the seams; the pilot, the market and the anchorage at
  the far end as at Falmouth.*
- [ ] **7. Funchal to Angra**, if the evening allows (`azores.yaml`).
- [ ] **8. The Palinure with a brain** (`trial-station-stranger`, and the naval cruise). *She
  investigates, is made out, finds herself overmatched and evades; the frigate gives up a
  stale chase and returns to her station; the cruise meets the cutter, reads the letter and
  speaks the brig.* Then `world: ship "Palinure": intent run home to Brest` typed at the
  prompt, and what she does.
- [ ] **9. A model captain of another ship.** `--station captain --ship Palinure` on the
  naval cruise through a door, the model's consent on record. *Her brief and her readings
  her own; the station kept across the switch, the sample saying which shape; the player's
  lookout seeing her as a sail.*
- [ ] **10. The world's business.** `merchant-cutter` (or any of the four free merchant
  scenarios) for a day and a night. *The sails sighted and made out are the business's
  traders, fishermen and cruisers under their flags; the quay's rumours when the boat
  returns; a ship into port and a fisherman home.*
- [ ] **11. The lugger and the smack.** Each sailed for a watch: the dipping lug in a tack,
  `dip the foresail`, heaving to under the lugs; the smack on the cutter's orders.
- [ ] **12. The regatta.** `py tools/regatta.py data/regatta/ushant-to-falmouth.yaml` with
  `--agent rules`, `--agent fake`, and a model through a door once the re-asks are run; the
  table read. *A model refused before the gun without its record; the table's columns.*
- [ ] **13. The seat hook.** A scenario with a `director:` grant: `world: seat <model> as
  captain of Palinure for 20 samples`, then `world: unseat Palinure`. *Refused without a
  record or a grant; stood down when the budget is spent.*

## The report

The verdict and the rulings go in this document and in `docs/DesignProposal.md`; the
playtest records under `docs/playtests/`.

## What this gate does not do

The director (M7b): the observed world with no player's ship, the director's voice, people
in places, needs. The open items of the milestone, carried to its close in
`docs/TechnicalSpec-M7b.md` §26: the planner across the land, the lugger's beating on the
regatta's crossing (a lay-line rule), Roscoff's and St Mary's tracks at far detail, Brest's
reach from the Bay, the held gauges' blend, the deep-sea tiles' rule, the orders review
(deferred to a cold review).
