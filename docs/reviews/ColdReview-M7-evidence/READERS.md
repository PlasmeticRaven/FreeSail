# The cold review of milestone 7: the rules every reader works under

This file is the standing instruction given to each reader working under the reviewer of
package 114. It is kept with the evidence so that the method can be checked.

**What this is.** FreeSail is a text-first age-of-sail simulation in Python. The whole
project is under a cold, critical review for its owner, who is not a programmer. You are
one reader among several; you have a part of the tree and a question. The reviewer joins
the parts.

**The tree.** `/home/user/FreeSail`, checked out at the commit under review
(504a25066c6995ce9829a19ffc597feb510a1870). Do not fetch, pull, switch branch or look at
any other branch.

**Cold means these, without exception:**

- Do NOT open, grep, list the contents of or read anything under `docs/dev/`.
- Do NOT open `docs/reviews/ColdReview-M7-SealedNotes.md`.
- Do NOT open anything under `docs/design/` or `docs/playtests/` or `docs/gates/`, unless
  your task names a file there. (They are the project's account of itself and are read
  later, by the reviewer.)
- When you search (grep, glob), restrict the search to the code, the data and the tests
  (`freesail/ client/ tools/ data/ tests/ .github/ pyproject.toml README.md`) so that the
  records do not come back in your results.
- Comments and docstrings in the code are the project's account of itself too. Read them,
  but do not take one as true: say what the code does, and where a comment and the code
  differ, that is a finding.

**You change nothing.** No file of the code, the data or the tests is edited, moved,
deleted or created in `/home/user/FreeSail`, with one exception: the single evidence file
your task names, under `docs/reviews/ColdReview-M7-evidence/`. No git commit, no push.
No model or vendor name in anything you write. No network, no key, no paid call. Do not
install anything.

**Do not run the test suite or any long command** unless your task says to: a timed
suite is running on this machine's four cores and you would spoil its timings. Short
commands (grep, wc, a few seconds of python to import a module and call one function) are
fine.

**How a finding stands.** Each with its evidence (a file and line, or a command and its
output), its weight (what it costs if left: high, medium, low) and your confidence (sure,
likely, a suspicion). None from memory or from what such projects usually do. Say plainly
what you did not look at. Criticism is the purpose: do not soften a finding and do not pad
the list. Where the thing is sound, say so in one line and move on. Do not praise.

**Your return.** Write your full findings to the evidence file your task names (Markdown,
plain words, UK spelling, no em-dashes used as flourishes, file:line references), then
reply with a summary of at most 400 words: the five or so findings that matter most, and
what you did not read. Read the files whole, not by excerpt, unless told otherwise; if you
run short of room, say exactly which files you did not finish rather than guessing at them.
