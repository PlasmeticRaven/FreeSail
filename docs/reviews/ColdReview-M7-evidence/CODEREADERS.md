# The code and the data: the task given to each reader of a subsystem

Read `READERS.md` beside this file first and obey it. Then this.

You have a part of the code (and perhaps its data). Read it whole, file by file; where a
file is very long read it in chunks to its end. You may grep the rest of the code, the
data and the tests to see who calls what, but your reading is your part.

The owner asked the review to target "where we've unevenly expanded the scope, missed
testing, implemented a feature inefficiently or multiple times over without integration,
and where we're missing the forest for the trees". Answer, for your part, with file:line
evidence throughout:

1. **What it is.** In a page a newcomer could trust: what this part does in the game,
   its main types and functions, what calls it and what it calls, and what a player would
   see of it. Its size (lines, files) and the size of the data and the tests that belong
   to it (grep tests/ for imports of your modules; name the test files and their lines).
2. **Is it reached?** What in your part is used by the game as played (trace from the
   entry points: `freesail/__main__.py`, `freesail/ui/server.py`, `freesail/ui/console.py`,
   `freesail/core/world.py`'s tick, the orders' `submit`) and what is reached only by
   tests or tools, or by nothing. Dead code, dead data, flags nobody sets, parameters
   always passed the same value. Prove each by grep.
3. **Built more than once.** The same matter handled in two or more places that do not
   know of each other, inside your part or between your part and another: two parsers of
   the same words, two tables of the same facts, two ways of finding a ship or a person,
   two geometries, two copies of a constant, a rule in code and again in data, a function
   re-implemented in a tool or a test helper or the browser's JavaScript. For each: both
   places (file:line), how they differ today (a difference is a bug waiting), and what
   joining them would take.
4. **Size and shape as a hazard.** Very long functions (say the longest ten, with their
   line counts), very long modules, deep nesting, functions with a dozen parameters,
   modules that import half the tree, circular imports dodged by imports inside functions
   (count them), global mutable state, module-level caches, anything that makes a change
   here dangerous. Comments that carry history ("package 37b", "the owner's ruling of...")
   in place of explanation: estimate what share of the lines are comment or docstring and
   whether a newcomer is helped or drowned by them.
5. **Correctness and honesty.** Bugs you can show (a path that cannot work, a unit
   mismatch, an off-by-one, a wrong sign, an exception swallowed, nondeterminism: a set
   iterated, a dict order relied on, wall-clock time or an unseeded random in the
   simulation). Places where the code fakes an outcome rather than simulating it though
   the names say otherwise. Places where a number is said to come from a source and no
   source is given. Check the proposal's hard boundary: the simulation (core, ship,
   physics, crew) must not import from the client or the agents; say whether your part
   keeps it.
6. **Thin or overgrown.** Against the rest of the game as you can see it: is this part
   far more detailed than what it serves, or a thin thing the game leans on? Say which and
   why, concretely.
7. **What is not tested.** Functions and branches in your part that no test calls (grep
   the tests for the names). Behaviour a player meets here that the tests cannot see.

End with `## The ten findings that matter`, ranked, each one or two sentences with its
evidence, weight and confidence; and `## What I did not read`.
