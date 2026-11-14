# The second reader: the task given to each refuter

Read `READERS.md` beside this file first and obey it (what may not be opened; nothing
changed but your one evidence file; no test suite run, though you may run a single test
by its node id, or a few seconds of python, where that settles a point).

**What this is.** A first reader has read a part of the code and written findings. The
review's rule is that no finding is kept until a second reader, told to refute it, has
tried and failed. You are that second reader. Your task names one or two evidence files.
For each finding in their `## The ten findings that matter` sections (and any other
finding in the body marked high or medium that you judge the owner would act on), do
your honest best to show that it is **wrong**, **overstated**, **already handled
elsewhere**, or **of no consequence to a player or a maintainer**:

- Open the code at the lines cited. Does it say what the reader says it says? Read
  around it: is there a guard a few lines up, a caller that never passes that case, a
  test the reader did not find, a second code path that does the thing properly?
- Where the reader says "nothing reads this", "no test covers this", "is never called":
  search for yourself, with other spellings, through `getattr`, string keys, YAML keys,
  the JavaScript.
- Where the reader says a thing happens in play, make it happen if a few seconds of
  python can (build a world as the tests do: look at a test's helper for the shortest
  road), or show the road by which play cannot reach it.
- Where the finding is a judgement (too large, built twice, overgrown), ask what the
  strongest defence of the code as it stands would be, and say whether it holds.
- Check the weight: what does it cost the owner if left exactly as it is?

For each finding write: the finding in one line (with the first reader's weight and
confidence); what you did to refute it (the command, the lines read); and your verdict,
one of **STANDS** (you tried and could not refute it; say what you confirmed),
**STANDS IN PART** (say which part falls and which stands), **REFUTED** (give the
counter-evidence), **NOT TRIED** (say why); and the weight you would give it.

Do not be kind to the first reader and do not be kind to the code. A refuter who finds
every finding sound has probably not tried; one who refutes by quibbling has not helped
either. If, in refuting, you come on something worse that the first reader missed, add it
at the end under `## Found on the way`, with its evidence.

Head your evidence file with a table: the finding in a few words, the first reader's
weight, your verdict, your weight. Your reply to the reviewer: at most 300 words: which
findings fell, which stand firmest, and anything found on the way.
