# Package 127: words and waits on today's ships

You are the builder of one package of FreeSail (a deterministic, ticked, text-first age-of-sail simulation in Python 3.11). The repository is checked out at the trunk, `claude/dreamy-darwin-d77nty`. You work on the branch `claude/pkg-127` and push only there. The lead (`session_01DTAvj6mwzAZMm2fER1Bi3U`) gates what you report. The owner approved this package on 2026-11-24 ("125, 126, and 127 are approved to launch"): it is part of the mending step that opens milestone 8.

## What this is

Eight faults in what the log says, or fails to say, on ships already in the game. Each was found in passing by a builder or a reader of the ships' package while proving that the eighteen ship files had not moved; none has been looked into, and what is written here is what was seen, not a diagnosis. They are listed in `docs/dev/CarriedForward-M7.md`, section 4 (the numbers below are that list's). **The log is the game:** a player reads nothing else, so a line that is untrue, or a wait that is not said, is a fault of the game and not of its wording.

1. **(1) An order made to wait behind other work says so in its reply alone, never in the log.** Seen on the brig: `furl the main topsail` given behind `take in the main topsail` answers "Order: furl the main topsail." and no line of the log says it waits or when it begins. A whole-ship order made to wait says nothing at all. (For a whole lateen, which no ship in the game carries, the ships' package made such a wait a line of the log at the order: see `freesail/evolutions/runner.py` and the reports of package 90's engine in `docs/design/Report-Package90-Engine.md`; the same should hold for every ship.)
2. **(3) "Filled away" is said of a ship then going astern:** the bilander and the lugger; the cutter, and the smack with her topsail set, after `lie a-try` and `fill away` ("Filled away ..." and she goes astern for an hour). See `freesail/evolutions/scripts.py` about lines 4527 and 11041.
3. **(4) Plain-sail work sets a topsail in a gale after `take in all sail`.**
4. **(5) A ship hung in stays cancels the player's take-in when she boxes herself off.**
5. **(7) The dire strain warning of a part can be held back ten minutes by a lesser warning of the same part** (`freesail/physics/strain.py`, `_warn`, `WARNING_INTERVAL_S`): a part warned as working and then loaded to where it will carry away says nothing more until the ten minutes are out, on every ship. The words and the counting of warnings may change; no figure of load, strain or damage may.
6. **(8) The smack's cast says "Hoist away the topsail and the mainsail" while her topsail stays furled.**
7. **(9) A `set the topsail` waiting for hands is not taken up again after the work it waited on is done, and nothing says so.**
8. **(13) `clear for action` says "The boats are out and towing astern; the ship is clear."** (`freesail/evolutions/action_scripts.py`, about line 134) of a boat that is on the booms.

## Your scope, and it does not grow

For each of the eight: reproduce it on a committed ship by the orders a player gives; find the cause; mend it at the cause, so that the log says what happened, when it happened, once. Where the mend is a line of the log, it is in the words of the deck. Where two of the eight prove to be one cause, say so and mend it once. **Not in scope:** how ships go about (a tack that fails logged "Tacked" is package 125's, with the moment of the haul); the harbour, fog and the game's captain replacing spars (package 126); any ship's file; any lateen hull; the physics' figures.

## The steps

**Step 0, a ground report in ONE message.** For each of the eight: the exact orders and the ship that reproduce it on the trunk, with the lines of the log as they came; the cause as you read it; the mend you propose; how many pinned tests it would move. One you cannot reproduce is reported so, with what you tried. **Then go on and build, unless** more than twenty pinned results would move in all, or a recorded passage, or a mend would change what a ship does and not only what is said: in any of those, wait for the lead's word.

**Step 1, the build, reported as ONE hash.** New truths are numbered **7-780 to 7-788**; use no other number. Each truth fails with its mend taken out.

## How you work

- Lint: `ruff check .` and `ruff format --check .`. The fast tier: `python3 -m pytest -n 4 -q -p no:cacheprovider`. The slow tier adds `--slow -m "not pace"`.
- **Before you report a hash, run the fast tier WHOLE on that hash:** 65 to 95 minutes on four workers, as a tracked background task with a limit of hours (three is safe), never with a limit it cannot meet, never as `cmd &`. A time limit you set yourself is not a limit of your container. Beside it, the slow tier of every test file you touched and of every file that reads what you changed (by grep), and `python3 -m pytest tests/test_api_door.py -q -p no:cacheprovider`. The whole slow tier is the cloud's, run by the lead on the hash you report.
- **Merge the trunk in before you report** (`git fetch origin claude/dreamy-darwin-d77nty && git merge --no-edit FETCH_HEAD`; never a rebase). Other work is landing on it this week: the ships' package (a list of mends for lateen hulls, then a new ship, the corvette *Diana*), and packages 125, 126 and 127, which are three builders at once, of whom you are one. They touch `freesail/evolutions/scripts.py`, `freesail/physics/strain.py`, `freesail/world/captains.py`, `tests/test_known_truths.py` and `docs/dev/TuningNotes.md`. If the merge conflicts in a file you did not mean to change, keep both sides' sections whole and check for conflict markers before you commit (`grep -n '^<<<<<<<\|^>>>>>>>' -r docs tests freesail`). A generated file is regenerated by its tool, never merged by hand.
- **This package changes what ships already in the game do. Its gate is of today's ships:** for everything that moves, the old beside the new, measured, with the reason; for everything else, proof that it does not move (the same orders run on the trunk and on your hash, the logs and the ships' states compared). The lead's own reader will run the eighteen ship files old beside new in gales, through the orders and through games left to the game's own captain, and will list every line of what a player or a model's seat is served that differs. Declare every such difference yourself first, in your report: an undeclared one holds the hash.
- Any subagent you use to read or review your work runs on the stronger tier offered to you on the Agent tool (the lead's launch message names it). Every pin you move is passed by a reader other than you, told to check that nothing was weakened and that each new truth fails with the mend taken out: say who read each.
- Every moved pin old beside new, with the reason, in `docs/dev/TuningNotes.md` under your package's heading. Your design and report go in `docs/design/` as `Report-Package127.md`. Do not edit `docs/dev/M7-WorkPackages.md` (the lead writes the record), `docs/dev/ShipsNudge.md`, `docs/dev/CarriedForward-M7.md`, `docs/DesignProposal.md`, or anything under `docs/agents/consent/` or `docs/agents/ConsentBrief.md`.
- Text the game serves is in the world's own words, as a seaman of 1800 would say or be told it: no package numbers, no design talk, nothing a player could not have been told on a quarterdeck. Period sources are cited by author, year and page; their text is not copied. A figure with no source is marked JUDGEMENT where it is defined, with its ground.

## How you report

Report to the lead by `create_trigger` (persistent_session_id `session_01DTAvj6mwzAZMm2fER1Bi3U`, initiation `human_request`, a short name, **your whole message as the trigger's own prompt**, beginning "From package 127:" with your number) and then `fire_trigger` on the id it returns. If `create_trigger` fails once with a passing error, try it again.

Each report is one message. A build report gives ONE hash with: what you built and why; the counts and the time of the fast tier whole on that hash; the slow files run and their counts; every pin that moved, old beside new, and who read it; every difference in what a player or a seat is served; what you found and did not mend. **The lead gates the hash you have reported, never one you have merely pushed.** A few passes are fine where the work needs them; each is one gathered list from the lead. Your own estimates of time are not deadlines. The lead's rulings come to you as a message in this session; where a choice is the owner's, the lead takes it to him.

## The rules that hold whatever else (not for bargaining)

- No model identifier (no model's or maker's name or version) in any file you write or change: code, tests, data, documents, commit bodies. The one exception is your own commit attribution lines. Do not set a commit's author by hand.
- Never skip, disable, quarantine or weaken a test. A pin is re-measured only where it moved, old beside new, with the reason in `docs/dev/TuningNotes.md`, and is passed by someone other than the one who moved it.
- Physics equations are read, not changed. Ship files only through `tools/gen_ships.py` (run without `-P`). A generated file is regenerated by its tool, never edited by hand.
- Truths pin states, counts and bands, not digests of worlds.
- API keys never in the repository, a save or a log. You seat and question no real model: a held station is the scripted fake's.
- Push only to your own branch. Never push to the trunk or another session's branch, never force-push, never rebase a pushed branch. Do not open a pull request.
- If something outside this scope blocks you, or the scope proves larger than it reads, stop and report it: do not rule on it yourself.
