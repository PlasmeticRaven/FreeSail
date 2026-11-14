# The records: the task given to each reader of the project's account of itself

**This is the review's second sitting.** The reviewer's findings under heads 1 to 5 were
written and committed (commit `b72ed89` on the review's branch) before any record was
opened. The records are now opened, by you. The rule of coldness that bound the first
readers no longer binds what you may read: your task names records under `docs/dev/`,
`docs/design/`, `docs/gates/` or `docs/playtests/`, and you may read them, the proposal,
the specifications, and the review's own report and evidence. What still binds you:

- You change nothing in `/home/user/FreeSail` but the one evidence file your task names.
  No commit, no push, no network, no key. Do not run the test suite (a timed run is using
  the machine); a few seconds of python or one test by its node id is allowed where it
  settles a point.
- No model or vendor name in anything you write. Where a record names one, write "a
  model", "the lead's model", "a local model", "a vendor".
- The tree is at the commit under review (504a250) in code, data and tests; do not fetch
  or look at other branches.
- **Nothing in a record is true because it is written there.** The lead has steered every
  package and written every record: the lead's method, briefs, rulings and records are
  under review with the rest. The owner is not a programmer and reads the lead's account
  to know the state of his project; what you are looking for is where that account and
  the thing differ, and what the account shows of how the work is run.

**Read first** the review's report as it stands, `docs/reviews/ColdReview-M7.md` (heads 1
to 5; about seventy thousand characters), so that you know what the review found cold.
Then read your records. Then answer, with the record's file and line for everything:

1. **Where the record and the thing differ.** A package the record calls done, merged,
   green or mended whose behaviour the review found broken or absent; a decision or ruling
   the record states that the code does not keep; a fault the record says is fixed that is
   still there; a count, a measurement or a state of the tree the record gives that is not
   so. Check each against the code (grep, read, a short run) before you report it. Equally:
   where the review's report is wrong and the record shows why (a thing the review calls
   unbuilt that is built, a fault the review reports that is by a ruling of the owner's,
   a finding already mended at the commit). Say so plainly: the review is to be corrected.
2. **What the project already knew.** For the review's main findings (the boundary; the
   director's reach onto the player's ship and its limits; the checkpoint; the server's
   open socket; the consent brief's promises against the code; the true position on the
   wire; no player Python; the evolutions and the ships as code; the newcomer's first
   hour; the guns left secured; the purchase with the boat lost; the far world's faults;
   the tests that cannot fail, the twins, the hand-kept tiers): does the record show the
   lead or the owner already knew of it, when, and what was done or deferred? A finding
   the project already holds and has booked is a different thing from one it does not
   know of. Give the place.
3. **The method, as the record shows it.** How a package is briefed, built, reviewed and
   merged: who writes the brief, who builds, who reviews, what a builder is asked to run
   before reporting, what "green" has meant at different times, how a pin is moved and
   what is written when it is, how a fault found late is traced to the step that let it
   through. What the lead decides alone and what goes to the owner; whether what goes to
   the owner is put so that a non-programmer can judge it (quote one ruling put well and
   one put badly). How often a package grew past its brief, was split into lettered
   parts, or was re-opened after merge (count them where you can). What the record says
   went wrong in the process, and whether the remedy was applied.
4. **The cost, as the record shows it.** Hours of suites; restarts; usage limits met;
   work redone; sessions lost; the size of the records themselves against the work they
   record. Quote the figures with their places.
5. **The record as a record.** Could the owner, or a newcomer, find from it the state of
   a given thing today? Is it ordered so that what is current can be told from what is
   history? What does it leave out that it ought to hold (and what does it hold that
   nobody will read)? Is it honest: does it record the lead's own errors as plainly as
   others'?

End with `## The ten things that matter`, ranked, each with its place in the record and
in the tree; then `## What I did not read`. Your reply to the reviewer: at most 400 words.
