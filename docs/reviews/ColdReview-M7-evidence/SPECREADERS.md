# The specifications against the code: the task given to each reader of a specification

Read `READERS.md` beside this file first and obey it. Then this.

You have one or more of the project's technical specifications (`docs/TechnicalSpec-*.md`).
They say what was to be built, milestone by milestone, and many carry "as built" pointers
into the code. A specification is the project's account of itself: nothing in it is true
because it is written there. Your work is to set it against the code, the data and the
tests as they are at the commit under review.

The owner asked for "a specific appraisal of our implementation of the proposal". The
reviewer has read the design proposal (`docs/DesignProposal.md`; you may read it too) and
needs, from you, the same judgement one level down.

**1. The commitments, one by one.** Read your specification whole, from its first line to
its last. For every commitment that matters to a player, to the proposal's pillars
(bottom-up realism; any rig; orders at every altitude; parity of human and model; a
dynamic world; depth over gloss; period-plausible) or to the soundness of the code (a
boundary, a determinism rule, a save's promise, a performance bound), give a row:

| § | what the specification says is built | verdict | where it lives (file:line) | how you know |

with the verdict one of: **built as specified**, **built otherwise** (say how it
differs), **built in part** (say what is missing), **not built**, **overtaken** (a later
decision or specification replaced it; name it), **cannot tell** (say what you tried).
"How you know" is a grep and its result, a function read, or a short python call; never
the specification's own word and never a comment's. Aim for the commitments that carry
weight, not every sentence: some forty to ninety rows for a long specification. Where a
section is a list of small rulings, group them.

**2. The pointers.** Take twenty of the specification's pointers into the code or the
tests (a file, a function, a test's name, a truth's number), spread through the document,
and check each: does the thing exist under that name, and does it do what the
specification says there? Give the count that hold and list those that do not.

**3. The numbers.** Where the specification gives a number a player could check (a
frigate tacks in so many minutes, so many ticks a second, a save of such a size, so many
evolutions, so many ships at full detail), say whether a test holds the code to it, and
if you can check it with a few seconds of python, do so (one short run only; no test
suite).

**4. The open items.** Every list of open items, deferred items, "not now" items and
"to come" items in your specification: for each item, is it now built, still open, or
quietly dropped? A long tail of deferred items is itself a finding: count them.

**5. The document as a document.** Could a newcomer build or maintain the thing from this
specification? How much of it is specification and how much is history (rulings dated
and attributed, package numbers, accounts of what was tried)? Does it contradict itself,
the proposal, or another specification you can see? Is it still the truth about the code,
or has the code moved on and the document not?

**6. What the specification never asked for.** From your reading of the code in the
areas your specification covers: what has been built there that no specification you
have read asks for (scope that grew outside the plan), and what the specification's own
logic needed that nobody wrote down or built.

End with `## The ten findings that matter`, ranked, each one or two sentences with its
evidence, weight and confidence; then `## What I did not read`.
