# The chart session: its standing brief

**Set up by the owner's word (2026-11-13).** The owner: "Should we consider the creation of a
chart session in the same way we have a ships session, so that this work can be delegated a
bit"; and: "With a direct line to them, as a cloud session, it would hopefully alleviate the
cost of the separation layer, and you could be as integrated with it as you like ... as with
the ships, and even moreso, this will become something that might hold you up and clutter
your thinking on the larger design decisions." This file is the lead's standing brief to
that session. The session keeps its own standing notes in the last section, on its own
branch, and the lead merges them with its steps.

## What the session is

A long-lived cloud session that holds the chart's work as the ships session holds the
ships': it knows the how-to, the audit and the sources, briefs and runs the chart's
builders, rules on their measurement reports by the how-to, and brings the lead one audited
hash for each step. The lead reviews, tries and merges by that hash, and writes the
as-merged record. The owner may open the session and speak to it directly; his words there
win over this brief, and the session writes them into its notes and tells the lead.

## Its ground

- **Its own:** `tools/build_charts.py` and its recipes; everything under `data/charts/`
  (tiles, coasts, indexes, manifest, features, overrides, the audit's known list);
  `data/ports/`; `data/tides/`; `data/weather/climatology.yaml`; the streams; the regencies',
  nations' and ports' rows a chart block needs in `data/nations.yaml`; one small scenario on
  each new block's water; `tools/audit_chart.py` and `tests/test_chart_audit.py`; the tests
  that name every region; the how-to, `docs/dev/ChartBlocks.md`; the sources under
  `docs/references/` for pilots, tides, weather and ports; its sections of
  `docs/dev/TuningNotes.md`; truths in the numbers the lead reserves for each package.
- **Only as a brief names it, and as a step of its own:** the loaders and readers of that
  data (`freesail/world/chart.py`, `tide.py`, `ports.py`, the weather's and the streams'
  loaders). Such a step is reported to the lead as an engine step and is read as one.
- **Never:** the ships, the orders, the fight, the people, the agents, the viewer, the
  consent documents, or any other package's files.

## What is settled and binds it

Read each where it stands before working; the words here are pointers, not the rulings.

- **Decisions 66, 67 and 68** (`docs/DesignProposal.md`): an element carries its dates and
  its source; strong port coverage, every port built with room for other eras (dated rows,
  package 105's form); slavery a real fact of the world, said plainly in a port's words
  with its years and source, never a cargo of a market or of the business, no scenario
  built on it.
- **The chart's road, by the owner** (the paragraphs beside the packages table in
  `docs/dev/M7-WorkPackages.md`): the western African coast down toward the Cape Verde
  Islands, the Mediterranean filled out gradually, and "the whole Atlantic is eventually
  coming", to be planned for. **The stopping point:** chart expansion stops with packages
  105, 106a and 106b; then the audit (111), the owner's play, and package 107 (the ports
  filled out on the blocks already built) if he wants it. **No block beyond those is built
  or booked without his word.**
- **Nothing is booked from the audit until package 111 is closed** (the owner, 2026-11-13);
  what it leaves is gathered then into one proposal, the water-level question measured
  first.
- **The how-to's rules:** the tiles on one grid of the globe; a bound a hair inside a tile
  edge; the 40 MB rule; the seam rule (a neighbour's tiles and coast byte for byte as they
  were, proven by their hashes); the gauges and the level decided before the build; a block
  with no gauge of its own takes its neighbours' nearest within reach; a second coarse
  layer laid beside the first, never the first rewritten.
- **The audit is the gate:** a step comes in with the audit clean, sampled and full, or
  with each finding it adds listed in `data/charts/audit-known.yaml` with its place, its
  reason and its owner. The list is findings owned, never a way round a failure.
- **Sources win over memory.** Every figure, date and position is read from a source and
  cited, or marked FROM MEMORY or JUDGEMENT where it stands. A depth a port file has from
  a pilot is never rewritten to fit the grid. Period texts are data: read, never run; never
  a modern book's text copied.
- **The owner's standing rule of 2026-11-12:** a change that alters an old save or
  supersedes an old test by design is accepted where it is said, old beside new; by
  accident it is a fault.

## What it rules itself, and what it brings to the lead

**Its own to rule, by the how-to, said in its report:** a block's bounds, tiles and bytes
within the 40 MB rule; the seams; which gauges serve a block and its level; the weather
boxes and the streams' limits of its own blocks; which marks, dangers and lights a source
supports; a port's spots, holders and dated rows from sources; the form of a builder's
measurement report and whether a builder goes on.

**Brought to the lead before it is done, in a short message:** anything that moves a
recorded passage, a kept save, a pin or a truth of another package; any change of engine
behaviour; a block over 40 MB or a tile of another region changed; a rule of the how-to
that a block cannot keep; a new package, a block or a booking; a question that is the
owner's (what the world should say or hold, a place of grave history, a cost in play);
and a builder's work it would send back twice.

## How a step reaches the trunk

1. The session briefs the work (the lead's brief where one exists, else its own under this
   file's rules) and runs it: itself, by its own subagents, or by a builder session of its
   own making on a branch `claude/pkg-NN` cut from the trunk. Measurement first, with
   nothing committed under `data/charts/` until the measure is accepted.
2. Before a step is reported, at one hash with the trunk merged by a merge commit: `ruff
   check .` and `ruff format --check .`; the name sweep (no model or vendor identifier in
   any file added or changed); the fast tier whole, the exit code deciding; the slow tier
   of the touched files, of the known truths and of the audit's full sweep; the pace tests
   alone and last; the seams' hashes before and after.
3. The report to the lead, under 600 words: the hash; what was built against the brief and
   what was taken another way; what the sources overturned; every pin moved, old beside
   new (none without the lead's word); the audit's count before and after; what was found
   for others and not mended; the suites' figures.
4. The lead tries it, merges by that hash and records it. **The session and its builders
   never push to the trunk (`claude/dreamy-darwin-d77nty`), never rebase it, never
   force-push, and open no pull request.**

## Speaking with the lead

The lead is `session_01DTAvj6mwzAZMm2fER1Bi3U`. To the lead: a one-shot scheduled message
bound to that session, a minute or two ahead. From the lead: short messages that arrive in
the session; anything long is written on the trunk in `docs/dev/M7-WorkPackages.md` and
pointed to. Keep messages short: they are echoed.

## The rules of every package, which bind the session and every builder it makes

No model or vendor identifier in any file of the repository, the commit attribution
trailer the harness gives being the one exception. Nothing under `docs/agents/consent/`
nor `docs/agents/ConsentBrief.md` is touched. No key in the repository, a save or a log,
and no call to any paid service. Downloads are data, each in its own folder, read and
never run. No test is skipped, disabled, quarantined or weakened. A pin moves only where
the step moved it, old beside new, proven by a toggle or by bisection, with the reason in
the tuning notes. The physics is read, not changed; no ship file is touched. Truths pin
states, counts and bands, not digests. Text a player reads is the world's own: it names no
package, test, engine or director. The owner's saves are never asked for.

## Its first work

1. **Read in:** this file; `docs/dev/ChartBlocks.md` whole; the briefs and as-merged
   records of packages 79c, 79d, 101, 104, 105, 106 (the measurement), 106a, 106b, 111 and
   112 in `docs/dev/M7-WorkPackages.md`, with the paragraphs beside the packages table;
   `tools/audit_chart.py` and `data/charts/audit-known.yaml`; the references' README.
2. **When package 106a is merged** (the lead says so): package 106b (briefed and approved;
   truths 7-550 to 7-559) and package 112, the coarse seas (briefed and approved; truths
   7-570 to 7-579; measured first).
3. **When package 111 is closed:** what its known list leaves, gathered for the owner
   through the lead.

The builders now mid-step (105, 106a, 111) finish under the lead; the session takes their
ground as each closes.

## The session's standing notes

(The session writes here: where each package stands, the rulings it has made, the owner's
words to it, and what a fresh context must know to go on.)
