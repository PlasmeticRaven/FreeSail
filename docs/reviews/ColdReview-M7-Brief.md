# The cold review of milestone 7: the reviewer's brief (package 114)

This file is the reviewer's whole brief, set apart so that the reviewer need not open the
project's records to read it. It is the text of "## Package 114" in
`docs/dev/M7-WorkPackages.md` as the owner approved it, with two changes made at the launch
(2026-11-14) for the review's coldness, by the owner's word to the lead ("do a double check
that you're happy with the 'coldness' of the initial context for the reviewer"): **the
lead's own examples of where to look are taken out** (a parenthesis under head 4 and a
clause in the test suite's sub-review), and they stand, with the lead's running list of
what he has himself found, in `docs/reviews/ColdReview-M7-SealedNotes.md`.

**The order of reading, which is part of the brief:**

1. This file.
2. The thing itself, as "Cold means this" below sets out: the proposal and the
   specifications, the code, the data, the tests, the game played.
3. Your own findings under heads 1 to 5 written down and committed on your branch.
4. Only then the records (`docs/dev/`, the design notes' histories, the playtests' notes)
   **and the sealed notes.** When you open the sealed notes, say in the report which of
   the lead's items you had found yourself, which you had missed and now confirm, and
   which you dispute. An item of the lead's is a claim to be tried like any other.

The tree under review is the trunk at the commit named in your launch message. Work that
is in flight on other branches is named there too; it is not on the trunk and is not under
review, except as the records speak of it.

---

## Package 114: the cold review of the whole (`docs/reviews/ColdReview-M7.md` new, with its evidence beside it; no code, no data, no test)

**BRIEFED 2026-11-13; APPROVED by the owner the same day ("114 is approved by the brief"; to run on Fable, as the packages table names it); not launched: it begins when the work
in flight has settled, at a commit of the trunk the lead names, on the owner's word.** The
reviewer is a new session that has built none of this, on the model the owner has named,
with readers of its own under it. The owner (2026-11-13): "general coverage of the project's current shape as
a cold and critical review, targeting where we've unevenly expanded the scope, missed
testing, implemented a feature inefficiently or multiple times over without integration,
and where we're 'missing the forest for the trees' in our development in general. It should
include a specific appraisal of our implementation of the proposal, as well as proposal(s)
for continuation, refinement of existing systems, integration of disparate elements
covering similar ground, and hazards to avoid, this review being along with the currently
planned more specific reviews."

**Cold means this.** The reviewer forms its own picture of the project from the thing
itself before it reads the project's account of itself. **First** the proposal
(`docs/DesignProposal.md`, every decision, and the technical specifications), the code, the
data, the tests, and the game played: a scenario begun and sailed through the game's own
doors as a player would, by the probe and the harness with the rules' seats alone (no key,
no paid call). **Only then** the records: `docs/dev/M7-WorkPackages.md` and its
predecessors, the tuning notes, the design notes, the playtests' notes; and where the
record and the thing differ, that difference is a finding. The lead has steered every
package and written every record: **the lead's method, briefs, rulings and records are
under review with the rest,** and nothing in them is to be taken as true because it is
written there.

**What it answers, in the owner's order.**

1. **The proposal as implemented.** Decision by decision: built as decided, built
   otherwise, built in part, not built, or overtaken; each with where it lives and how the
   reviewer knows. The proposal's own aims weighed against what a player can do today from
   the harbour page to the end of a passage, a fight and a port.
2. **Where the scope has grown unevenly.** The subsystems measured against one another (the
   code, the data, the tests and the research each holds) and against the weight the
   proposal gives them: where detail has run far ahead of the game around it, and where a
   thing the game leans on is thin.
3. **What is not tested, and what the testing costs.** What the suites prove and what
   they only pin; behaviour with no test; truths that would pass on a broken game (a sample
   proved by planting faults and seeing whether anything fails); tests that test the same
   thing; the hours the suites take and what that has cost the work; what would make them
   cheaper without making them weaker.
4. **What is built inefficiently, or more than once.** The same matter handled in two or
   more places that do not know of each other (the lead's own examples are withheld: see the head of this file), each with what joining them would take. Code and data whose size or
   shape is itself the hazard.
5. **The forest.** What the project is now, said in a page a newcomer could trust. Whether
   the order of work has served the proposal's ends or the builders' momentum. What a
   player meets that the tests do not see. What the project believes of itself that is not
   so.
6. **What to do.** A continuation proposed in order, with what each step buys; the
   refinements existing systems want before more is laid on them; the integrations of (4)
   ranked; **the hazards to avoid,** in the code, the data, the repository, the process and
   the cost of the work; and what to stop doing.

**A sub-reviewer for the test suite, of its own (the owner, 2026-11-13):** "one
sub-reviewer that focuses on an audit of the current test suite for tests no longer testing
relevant features, tests which are built not to fail, tests which might be consolidated,
and general suggestions for improvements to the general test procedure." A reader under
the reviewer whose whole work is the tests, every test file read and none sampled away:
(a) **tests of what is no longer there or no longer matters:** a feature removed, replaced
or superseded whose tests remain, and tests kept alive by edits that emptied them; (b)
**tests built not to fail:** an assertion of what the test itself set up, a band wide
enough for any answer, a patch or a toggle that steps round the thing tested, a digest or
a count re-pinned to whatever the code now does with no reason a reader can check, an
expected failure that nobody expects to mend; each such claim proved on a sample by
planting the fault the test names and seeing whether it fails; (c) **tests that might be
one:** the same behaviour proved in several files, the same scenario sailed again and
again for one line each, families that want a table; with the seconds each costs, from
the suites' own timings; (d) **the procedure:** what the tiers hold and why, what runs on
the builder's machine, the lead's and the cloud's, what a step is asked to run before it
reports and what that lets through, how pins are moved and recorded, the pace tests on a shared machine, and
what would make an hour's fast tier shorter without making it weaker. Its return is a
table by test file (the tests, their seconds, its verdicts) in the evidence, and its
proposals ranked by what each saves and what each risks, under head 3 of the report. **It
changes no test:** the rule that no test is skipped, disabled or weakened binds the review
as it binds a builder; a test it would remove or join is proposed in words for the owner.

**How a finding stands.** Each with its evidence (a file and line, a command and its
output, a scenario and what happened), its weight (what it costs if left) and the
reviewer's confidence; each tried against a second reader told to refute it before it is
kept; none from memory; what was not looked at said plainly. Criticism is the purpose: no
finding is softened, and none is padded.

**The report.** First two pages for the owner, who is not a programmer, in plain words:
what the project is, the ten things that matter most, and what to do first. Then the body
by the six heads. Then the evidence. One document under `docs/reviews/`, the evidence in
files beside it.

**How it sits with the other reviews** (proposed with this brief; the owner's to settle):
it comes first and alone; packages 103, 96 and 92 follow it, each amended by what it
finds.

**The rules that bind it:** it changes no file of the code, the data or the tests, and
proposes changes in words; no model or vendor identifier in any file; nothing under
`docs/agents/consent/` nor `docs/agents/ConsentBrief.md` is edited (they may be read and
reviewed); no key, no paid call; downloads are data, never run; the owner's saves are not
given to it; it works on `claude/pkg-114`, never pushes to the trunk, never force-pushes,
opens no pull request. It may run the suites and its own probes as it needs. It reports to
the owner; the lead merges its document unedited and may answer it in a document of its
own beside it, never in it.
