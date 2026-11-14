# The test suite's audit: the task given to each reader of the tests

Read `READERS.md` beside this file first and obey it. Then this.

The owner asked for "an audit of the current test suite for tests no longer testing
relevant features, tests which are built not to fail, tests which might be consolidated,
and general suggestions for improvements to the general test procedure." Every test file
is read whole and none is sampled away. You have a list of files; read each from its first
line to its last (in chunks if it is long), and the code a test calls where you need it to
judge the test.

For **each file** in your list, write a section in your evidence file with:

1. **Count and kind.** How many tests; how many are parametrised and into how many cases;
   which module-scoped or session-scoped fixtures it builds and roughly what they cost (a
   day sailed, a server started, a browser); in one or two lines, what behaviour of the
   game the file proves.
2. **(a) Tests of what is no longer there or no longer matters.** A feature removed,
   replaced or superseded whose tests remain; a test whose name or docstring promises one
   thing and whose body now asserts another or nothing; tests kept alive by edits that
   emptied them (an assertion commented out, a body reduced to `assert True`, a
   comparison against a value read from the code under test). Check against the code:
   grep for the thing the test names before you call it gone.
3. **(b) Tests built not to fail.** An assertion of what the test itself set up; a band
   wide enough for any answer (say the band and what the code gives); a monkeypatch, a
   fake, a toggle or a flag that steps round the very thing tested; a digest, hash, count
   or golden text pinned to whatever the code now does with no reason a reader can check
   (say how many such pins the file holds); an `xfail`, `skip` or `skipif` and whether
   anybody could expect it mended; a `try/except` that swallows; a loop over an empty or
   possibly empty collection; `assert x or True`-shaped logic; a test that would pass if
   the function under test returned early.
4. **(c) Tests that might be one.** The same behaviour proved in several tests or several
   files (name the others where you know them); the same scenario sailed again and again
   for one assertion each; families that want one table-driven test.
5. **Anything else** a critical reader would tell the owner about this file: a test that
   is a good one and proves something hard (one line, no praise beyond the fact), a test
   whose failure message would not tell a builder what broke, a file that tests a tool or
   a document rather than the game.

Give line numbers. Be concrete: "test_x (line 210) asserts `len(lines) >= 0`" is a
finding; "some assertions look weak" is not.

**Fault-planting candidates.** At the end of your evidence file, under the heading
`## Faults to plant`, nominate up to six of your strongest claims under (b), each as: the
test (file::name), the fault to plant in the code under test (the file, the line, the
exact edit: for example "in freesail/physics/hull.py line 212 change `* 0.5` to `* 0.6`",
or "make function f return its input unchanged"), what the test's name says it should
catch, and your prediction (passes although the game is broken, or fails as it should).
Choose faults a builder could really make, which really break the behaviour the test
names. Also nominate up to three faults in behaviour that you believe NO test in your
files would catch though a player would. The reviewer plants them in a scratch copy and
runs the tests; you do not.

**At the head of your evidence file**, a table with one row per file: file, lines, tests
(cases), fixtures of weight, and your verdict in a few words (sound / pins much, proves
little / duplicates X / dead in part / …).

Your reply to the reviewer: at most 400 words, the findings that matter most.
