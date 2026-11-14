# Records 03: the work-package records of milestones 5, 6 and 7b, with the close-outs of 4, 5b and 5c

The reader's evidence for the second sitting (`RECORDREADERS.md`). The tree is at 504a250. Nothing was changed but this file. No suite was run; the code was read and grepped to check what the records claim.

**Read:** `docs/reviews/ColdReview-M7.md` whole (466 lines). `docs/dev/M7b-WorkPackages.md` whole (1–1764). `docs/dev/M6-WorkPackages.md` whole (1–1980). `docs/dev/M5-WorkPackages.md`: 1–83 (the head and the waves table), 665–703 (package 32c, the split of the suite into tiers), 2676–3275 (the last 600 lines whole), and the headings of the rest. `M5-CloseOut-5b.md`, `M5-CloseOut-5c.md` and `M4-CloseOut.md` whole. To check claims I also read `docs/gates/gate-m6c.md` whole, decisions 50 and 51 in `docs/DesignProposal.md`, `docs/TechnicalSpec-M7b.md` 2240–2292, and parts of the review of 2026-10-22 (`docs/playtests/2026-10-18-to-22-owner-playtests-and-review/FreeSail-M7b-Playtest-and-Hotfix-Review.md` 181, 396, 537–577, 620–640, 653–659, 788–810).

Model and vendor names in the records are written here as "the larger model" (the records' builder for heavy design), "the standard model" (the records' builder for standard work), "a model", "a vendor".

---

## 1. Where the record and the thing differ

**1.1 The director's hard limits. The record says the channel enforces them, and it does not. The record's own first entry already said so.**
- The brief for package 50 (M7b:281–287): "the limits enforced by the channel, not trusted to the model". Decision 50 (DesignProposal:655): "The brief's hard limits (the player's own: no gale above such a force, nobody dies) stay refusals."
- The record of package 50 as merged (M7b:321–322): "`nobody_dies` and `the_chart_as_it_is` are declared in the brief's limits and read to the director in words, with nothing yet for them to refuse." No later package in M7b closes this.
- In the code, `nobody_dies` refuses only an `aboard:` entry whose `harm` is `deadly` (`agents/director.py:338-341`). `data/director/aboard.yaml` holds 35 `harm:` entries: 29 `none`, 5 `hurt`, and none `deadly`. So the limit cannot refuse anything. That is the review's finding, and the record has carried the gap as an open item since 2026-10-17.
- The cold review of 2026-10-22 got this wrong. Its §6.1 (line 629) says "The limits held where they were tested: ... nobody died". Nobody died because nobody was killed, not because anything was refused. The project's own independent reading misread the gap that package 50's record had named.
- The brig limit, R-38, is recorded as mended by package 68 (M7b:1507–1508, with "a test per starter brief's limit"). In the code it ranks only words it knows (`director.py:398-420`, `size_rank_of`). The review's "a line-of-battle ship" passing is the case those tests did not try.

**1.2 The rule of reach: the record covers the hand and the voice, and never mentions the `captain:` channel.**
- Package 62 as merged (M7b:683–684): "the rule of reach refuses it where a model or the player holds her captain and for the player's own ship by name or 'the ship'". That is true of the `ship "X": order` form (`world/orders.py:1439-1460`).
- `apply()` sends `captain:` to `_captain()` before the reach check is reached (`world/orders.py:272-273`; the check is at 300-303). `_captain()` sets the intent of the player's own rules captain with no reach check (390-417). The code's own comment calls this channel "the director's seam" (`orders.py:120`, `384`).
- No line in M7b, M6, the spec's director sections, or the 10-22 review discusses `captain:` as a road open to the director. My greps for "captain: intent" in `docs/dev/*.md` and `docs/TechnicalSpec-M7b.md` found nothing. The project did not know of this road.
- The director's fixed brief (`director.py:1319-1321`) and its module head (`director.py:7`) still promise "nor any of the player's own ship".

**1.3 The strike of the player's ship is a form the project designed. The review should say so.**
- The director's forms reference lists `ship "the ship": struck to the Harpy` as a verified example: "a ship struck to another and possessed, the player's own by her name or 'the ship' ... doubted after the first minute" (`director.py:986-993`; package 74, M7's).
- Under decision 50 a doubt can be re-entered with a reason and is then performed. So the review's strike is not a hole in the code. It is a designed form that only doubt guards, and that no hard limit or rule of reach covers.
- The finding stands as a contradiction between the design and the brief's promise. It is not a bug a builder slipped in. **The review's decision 14 note should be corrected to say this.**

**1.4 The truth on the wire against M5's promise.**
- Package 37j's brief (M5:3073–3075): "The snapshot to the browser no longer carries the true distance and bearing of the landmarks in sight. A test proves no reading gives the true position by any road."
- The 5b close-out (5b:28) and the 5c close-out (5c:30–33) record the rule as checked in the code.
- The log line's data keeps a mark's true distance "for the record (the log is the author's and the tests')" by design (`world/lookout.py:634-650`). `tests/test_lookout.py:103` asserts "the truth kept". The test 37j promised covers readings and the snapshot, not the log events the browser receives.
- So the record's claim is true as worded and false in effect. The review's finding stands, and it is a decision taken in the code, not an oversight.

**1.5 Gate 6c: the README says it passed.**
- `README.md:5` says "gate m6c passed". The gate's own verdict (`gate-m6c.md:3`) says "run in part ... items 1 to 3, 5 and 8 run, the rest deferred to the director's milestone's gate by decision 50".
- Never run: item 4 (the pictures through a door), 6 (the chart whole and the owner's own passage), 7 (Funchal to Angra), 9 (a model captain of another ship), 10 (the world's business), 11 (the lugger and the smack), 12 (the regatta with a model) and 13 (the seat hook). That is 8 of 13 (`gate-m6c.md:68-99`).
- They went to "Gate 7b after 55, carrying gate 6c's untested items" (TechnicalSpec-M7b:2285). Decision 51 deferred package 55 and gate 7b (M7b:47, 188–192). The 10-22 review's §6.2 also found the local-model directed passage unplayed (line 633).
- The review is right. This confirms its "to be checked" in §1.3, row 11, and in §5.4.

**1.6 The gate 6c findings briefed for package 58 were dropped between the spec and the brief.**
- The lead read the 6c notes (M6:1974–1980), and spec M7b §24 (2243–2249) gives package 58 these items: the offing by the account and not its doubt; the guard against land ahead; a bearing taken when the doubt is wide; the headsail shifted; the trim's cadence; Bertheaume's track; "all sail in a chase"; the station's regain against the wearing order; the lay line and the sea-route mark; Roscoff's and St Mary's tracks.
- The brief for 58b as approved (M7b:1303–1356) holds none of these except the gale book. "Kept out of 58" names "the lay line (43b's open item, 61)" (M7b:1361).
- Checked in the code:
  - The King's ship's `chasing` book makes no sail beyond `give chase` and the trims (`data/captains/kings-ship.yaml:215-219`).
  - Nothing in `freesail/world/` names a lay line.
  - "Wear at the hour" keeps its old form (`kings-ship.yaml:222`).
  - Roscoff's track to sea still crosses the land at far detail (`world/business.py:617-620`).
- The record never says these items were dropped. The spec's list and the brief simply differ.

**1.7 The rules captain's "perception on the player's terms".**
- The brief for package 40 (M6:159–161): "nothing in `captains.py` reads the world's truth, and a test proves it".
- Package 43 put the far brain, which by its brief perceives "from the vessel's own truth", in a separate module so that the proof would keep passing: "The brain on the far body lives in `freesail/world/brains.py` (the truth-road proof on `captains.py` must keep holding; the shared judgement is a mixin)" (M6:1508–1511).
- The proof is a grep of eleven strings in one file's source, plus one comparison of two worlds (`tests/test_captains.py:275-296`). `captains.py:4326-4337` reaches a crewed body's sailors by `crew_world.ship`, a road the list does not name.
- The record presents a module boundary drawn around a string test as perception kept honest. The review's decision 40 note is right. It should add that the far brain's knowledge of the truth is by brief (M6:1346–1349), not by drift.

**1.8 Other points where the review should be corrected or sharpened.**
- Decision 17(a), the station's brief sent as the system message: the lead's own brief for package 42 specifies it ("the brief as the system prompt; a sample as a user message", M6:735–736). It was designed, not drift.
- Parity tested only at the captain's station: that was the brief's scope ("the captain's station's observation surface is the player's", M6:1665–1672). The record of 44 counts "78 readings, 302 verbs, 21 console commands, 17 snapshot blocks and 16 tools" and lists the exceptions as "by design" (M6:1477–1480). The review's finding stands. It is a scope the lead chose, not a test that failed to see.
- The python sandbox: see 2.4. The review's "Specification M4 put the sandbox in milestone 6; no later specification mentions it" is confirmed. Two further facts: the 5c close-out handed "officers writing Python rules" to milestone 6 (5c:119–120), and no line of `M6-WorkPackages.md` mentions Python rules or a sandbox.

---

## 2. What the project already knew

| Review finding | Known? | Where, and what was done |
|---|---|---|
| The director's limits | **Yes**, the `nobody_dies` gap from 2026-10-17 | M7b:321–322, carried and never closed; the brig limit found at 10-22 (R-38), "mended" by 68 (M7b:1507); 1.1 above |
| The director's reach onto the player's ship by `captain:` and `follow` | **No** | Nothing in M5, M6, M7b or the 10-22 review; 62's record claims reach for "the player's own ship" by the hand only |
| The strike | Designed | `director.py:986-993` (M7's package 74) |
| The server's open socket | **Yes**, 2026-10-18 | 59's "lead's note, an open item": the harbour's writing routes "answer any client the game's server answers ... behind a tunnel ... anyone with the URL ... recorded and not mended here; a token for the harbour, or a flag that closes it, when the tunnel is a practice rather than a test" (M7b:748–755) |
| The consent brief's promises | **Yes**, in part | "To come": the captain's debrief of 10-18 and R-51, booked to 55 (M7b:141–142, 231–232), which decision 51 deferred; `ConsentBrief.md:13` still says it. The system-message road was the lead's own design (M6:735–736) |
| The true position on the wire | Decided, not known as a leak | 1.4 |
| No player Python | **Yes**, and dropped | M4 spec §24 item 1 and 5c:119–120 hand it to M6; M6 never briefs it |
| Ships as code | **Yes**, by rule | "The ship files are generated: every change goes through `tools/gen_ships.py` ... never by hand" (M7b:1038) |
| The newcomer's first hour | **Yes**, 2026-10-18 | The owner: the harbour "would not be clear at all to a newcomer" (M7b:76–78); package 64 struck 2026-11-06 into M7's 96 (M7b:40, 71–74) |
| Guns secured under the player's hand | The mechanism by ruling | Decision 41: the player's direct order makes the captain stand aside (M6:454–457); the consequence (nothing tells the player the guns are his) is not recorded |
| The purchase with the boat lost | Near it | 53b, "not fixed, carried: the market's `buy` checks the hold's room without goods still in the boat" (M7b:659–660) |
| The far fisherman's haul from the player's hold | Probably the cause | 56: "one catch function for the player's ship, a crewed fisherman and the far body" (M7b:788–789); the fault is not recorded |
| Tests that cannot fail; hand-kept tiers | **Yes**, in part | 32c's rule: slow "applied from `tests/conftest.py` ... never by editing the test files" (M5:679–680); 58a found truth 88 "marked `pace` by hand and not recognised by the conftest's name rule" (M7b:507–509, 537); 50 found a slow test failing on the main line "since `b9052c5`" unseen (M7b:333–335); 58b: "the station gale's pin was stale before this package (the non-strict xfail hid it)" (M7b:443–445) |
| The far world's faults | In part | Roscoff's and St Mary's tracks (M6:1446, `gate-m6c.md:111`); "ships seen through the land" not recorded |
| Gates not held | **Yes**, by the owner's rulings | 1.5; §3.2 below |

---

## 3. The method, as the record shows it

**3.1 The head rules for builders, quoted.**

**M3, M4 and M5 (to 2026-10-01):** "run the whole suite and read the summary line yourself, report in the set order" (M5:10–11; M4-WorkPackages:3). M3 states the rule in full: "the full `python -m pytest` clean (the suite takes two to three minutes; run it whole, and read the summary line, do not pipe it through anything that can hide a failure)" (M3-WorkPackages:15). M5 added five rules (M5:15–41): the truth kept from the captain; unverified study figures marked; parity structural; "a scenario's book is tuned once and cheaply ... A builder that finds itself on its tenth whole-passage run is to say so"; and the heavy design to the larger model, the standard work to the standard model.

**The split of the suite.** Package 32c (2026-10-01), from the cold review of 2026-09-30, which gave the build machine's figures as "eleven minutes alone, seventeen on four workers" (M5:667–691). From the K batch (2026-10-08): "The fast tier is run before the report and the slow tests of the passages the package touches; the whole suite is the lead's at the merge" (M5:2939–2941).

**M6:** "the fast tier run before the report and the slow tests of the passages touched; a section in the tuning notes and a report to the lead" (M6:10–12). The lead's whole suite at the merge is no longer written.

**M7b:** "the fast tier and the slow tier of the files touched before the report, the whole slow tier once at the end" (M7b:11–12). Also from 2026-10-17: "The lead plays ... a merged package gets a short run by the lead at a station ... before its record closes" (M7b:14–21).

**Moving a pin.**
- In M5 and M6 (M5:2936–2939; M6:8–10): "re-pinned where a change moves them, with the old figure beside the new and the reason in the package's section of `docs/dev/TuningNotes.md`; a passage that moves for a reason the package cannot give is a finding, not a pin".
- M7b's own wording (M7b:9–11) keeps the old figure and the reason and does not repeat "a finding, not a pin". It does say M6's rules hold.
- In practice the whole suite is run, and the pins are written to what failed:
  - "the slow tier whole 3,479 passed, 12 expected failures, the 6 failures the pins then written in" (45, M6:1188–1189);
  - "the 13 failures its pins then written in" (45c, M6:1577–1578);
  - "the four pins then written in" (43b, M6:1440);
  - "the 10 moved pins then written in" (44, M6:1482).
- Bisection to prove that a moved pin is the package's appears from 58a (M7b:532–534) and 68 (M7b:559).
- The 57 rule, "an expected failure on a trial is a debt, not a pin: 58 lifts it, and nothing else may be marked so" (M7b:858–860), was broken six days later in the same milestone. 68 marked the two Goulet cases strict expected failures (M7b:569–571). 58b left the gale trials as expected failures "with the new figures" (M7b:441–443, 1366–1369). They were lifted only at M7's package 88 (`tests/test_captain_trials.py:145`).
- A test was changed to fit the merge: truth 90's regatta finish failed on the merged tree, "so the course's radius was made the game's own reach" (M7b:406–413).

**What "green" has meant.**
- To 2026-10-01: the whole suite, run by the builder.
- After that: the fast tier, plus the slow tests the builder judged touched, with the whole suite by the lead.
- By M7b: one whole suite for a wave, "at the owner's word: one suite for the three" (M7b:404). Examples:
  - 53b with 66 (M7b:588);
  - 59 with 62 (M7b:673–674);
  - 68, 58a, 67 and 58b: "3,914 passed, 12 expected failures, 2 skipped, one failed" (M7b:404–406).
- Some packages were reported with their whole slow tier incomplete:
  - 59's builder's whole slow tier was "cut off at 24% by a container restart" (M7b:720);
  - 53's builder's rerun was cut off by the restart (M7b:882–884);
  - 58b's builder's "whole slow tier was stopped at the lead's stand-down and not run by the builder" (M7b:415–416);
  - 54's whole slow tier ran "under the other packages' load" (M7b:918).
- Pace tests "passing once in three runs" were accepted as "the floor within its noise" (68, M7b:550–552).

**3.2 When the gates stopped.**
- "Gates lag the work" (decision 29, 2026-09-30; M5:75–79) first meant a package is launched before the earlier gate is run, and each gate is still cut and run.
- 2026-10-11: package 45 was "merged ... as committed so far (the owner's word, to play it)" (M6:28).
- 2026-10-15: gate m6a-2 was "not cut ... folded into the milestone's last gate" (M6:1819–1820). This is the first gate not held.
- 2026-10-17: gate 6c was "run in part" (decision 50).
- 2026-10-23: gate 7b was not run, and M7b was "frozen open" (decision 51; M7b:188–192).
- So "no gate" began on 2026-10-15. Since then no gate has been passed whole.

**3.3 Lettered packages** (counted from the headings and the waves tables; earlier milestones not read).
- M4 already had 29b and 29c (M4-CloseOut:31, 71).
- M5: 30b, 31b, 31c, 32b to 32f, 33a to 33d, 35b and 37b to 37n, so **26**.
- M6: 37p, 39a to 39f, 40b, 40c, 42a, 42b, 43b and 45c, so **13**. Package 45 was two packages joined into one (M6:939–941).
- M7b: 53b, 58a and 58b, so **3**. 51, 60, 63 and 64 were taken into or replaced by M7's packages 82, 96 and "60 (from M7b)" (M7b:31, 36, 39, 40).

**Re-opened after merge or amended by a later package.**
- 45, merged in part on 10-11 and whole on 10-15 (M6:1161).
- 37e and 37f, amended by 37j and 37k (M5:3026, 3085).
- 45's regressions, which became 45c (M6:1192–1219).
- 57, mended by the lead after the owner's test (M7b:868–873).
- 68's item 19, which became 58b's item 6 (M7b:569–571, 1342).

**Packages that grew past their brief.**
- 52 extended the rule of reach (M7b:347–350).
- 66 was "wider than asked" twice (M7b:593, 595).
- 40 was briefed "to go beyond the letter" (M6:106–110).

**3.4 Independent readings.**
- The first in these records is "the cold review of 2026-09-30" (`docs/design/ColdReview-2026-09-30.md`; M5:667; 5b:7).
- Then the gate 5c review and audit (`report-2.md`, parts M and N; 5c:69–72; M5:2925–2928).
- Then the cold review of 2026-10-22, with 63 findings (M7b:114–116, 1474–1479).
- The orders system's review was "deferred to a cold review by a [larger-model] subagent" (M6:1722, 1822–1824) and then dropped from the gate (M7b:164–166).

**3.5 Who decides.**
- The lead decides much alone, and the owner's assent is taken by silence:
  - "Taken another way, accepted by the lead, for the owner's overrule if he wants it" (M7b:345);
  - "the four 'taken another way' choices above stand unless he says otherwise" (M7b:576–577).
- Lead's rulings at merges: 56's pins (M7b:794–802); 39e's widened corridor, which the lead held for the owner (M6:857–868).
- A ruling put to the owner well, in plain terms and with its consequence, at 57 (M7b:852–860): "**The gale trial now grounds** ... the owner saw this very grounding in his own gale run at gate 6c ... so the fault is the captain's handling, already 58's first item; but an expected failure on a trial is a debt, not a pin: 58 lifts it, and nothing else may be marked so."
- One put badly, at 66 (M7b:613–617). It gives five questions in a clause, with no consequence and no advice: "**Decisions for the owner:** a day as the bound of a hold until an event; 'heard by' naming the people within hearing as well as the stations (four named at most, the rest counted) or the stations only; an order out of turn opening the turn while merely waiting; the deck passing to someone when the captain lands; a status line in the browser ..." The same is true of 67's (M7b:495–498).

**3.6 What the record says went wrong, and the remedy.**
- A slow test failed on the main line unseen (M7b:333–335). The remedy was one assertion mended. No rule changed.
- A stale pin was hidden by a non-strict expected failure (M7b:443–445). No rule followed.
- The lead's errors are written plainly:
  - 'the lead did not think of the master and spared the acts' (M7b:214–215);
  - 45c found that the lead's suspicion of the cruise's drift was wrong ("not the helm rules at all", M6:1550);
  - 53b found that "the test's finding 8 was this, not the scenario's people" (M7b:655–656).

---

## 4. The cost, as the record shows it

**Usage.**
- "the gate 5c verdict waits on the allowance's reset" (M5:36–37).
- "the builder had not the budget to find which of the three" (45; M6:1197–1198).
- "the test battery stays as it is, the usage eaten" (M6:1819).
- "while the lead's usage is near its limit" (M7b:63).
- "[the larger model]'s usage kept for M7" and "the design runs ... wait for the new week's budget" (M7b:117–118, 194–196).

**Machines and suites.**
- "the machine had carried four suites at once at a load of twenty-five, so the builders stood theirs down" (M7b:504–505).
- Builders ran under loads of 17 to 25 (M7b:413–414, 462).
- 68 ran "nineteen commits ... across two container restarts" (M7b:545–546).
- There were three more restarts that cut suites (3.1).
- Truth 90: "the week would cost a quarter of an hour a brief" (M7b:329–330).
- 32c's reason was the suite's eleven to seventeen minutes (M5:689–690).

**Tokens.**
- 58a: a day's samples went from 1,371,847 to 1,038,872 characters (M7b:527–529).
- 67: 4.11M against 4.70M tokens over 132 glasses (M7b:486–488).
- The 10-22 review's R-34: about 16.3M prompt tokens in two hours, and a vendor's credit run out (review of 10-22, line 561).

**Work redone.**
- 37e, 37f and 45 were redone by 37j, 37k and 45c.
- Every passage was re-pinned at 37p, 45, 45c, 57 and 68.

**The records' size.**
- M5: 277,685 characters; M6: 176,154; M7b: 158,508; the three close-outs: about 30,000.
- M7b records 14 built packages, about 11,000 characters each, before the tuning notes.

---

## 5. The record as a record

**Finding the state of a thing.** The waves table is the only current view, and each row packs a whole history into one cell (M7b:27–47). Under it the order is neither by date nor by number:
- M7b gives 50's brief, then 50's and 52's records, then 52's brief, then records of 58b, 67, 58a, 68, 66, 53b, 62, 59, 56, 57, 53 and 54 (newest first, broken), then the briefs.
- M6 interleaves the records of 39d, 39e, 39c, 39f, 45, 42b, 43b, 44, 43 and 45c among the briefs.
- A newcomer cannot tell what is current from what is history without reading the whole.

**Facts that are only in the records.** These carried items are the state of the game, and they live in records nobody will reread:
- the director seated in a ship, not built (M7b:691);
- `news:` not a channel (M7b:319–320; still absent from `CHANNELS`, `world/orders.py:125-149`);
- no Fowey port (M7b:743–746; `data/ports/` has none).

**What the record leaves out.**
- A register of the open items. The same item is carried from package to package in prose.
- Any statement when a spec's list for a package is cut at briefing (1.6).
- The README's status, kept true to the gate (1.5).

**Honesty.** The record is plain about builders' faults and about many of the lead's own (3.6). It is not plain about its own claims of enforcement. "The limits enforced by the channel" and "the rule of reach ... for the player's own ship" stand in briefs and records beside an open item that contradicts the first, and a channel the second never names.

**Deferred items, checked in the code (eight).**
1. M4 to M5: "the night's end constant split from the broken-sleep hour" (M4-CloseOut:110). **Not done**: one `NIGHT_ENDS_HOUR = 4` still serves both (`crew/routine.py:67-70`, `world/needs.py:82`).
2. M5 §17's `--casual`, "not built" (5b:41; 5c:46). **Still not built**: no flag in `freesail/`.
3. Double altitudes, "not built" (5c:43). **Not built** (`world/sights.py:16`).
4. "The hawse fouled not built" (5c:47). **Not built**: no fouled hawse in the code.
5. To milestone 6: "officers writing Python rules" (5c:119–120), with the sandbox (TechnicalSpec-M4:111, 261). **Never briefed**: `standing/python_api.py:28-29, 44` still says "milestone 6's sandbox".
6. The gate 6c findings for 58: "all sail in a chase", the lay line, Roscoff's tracks. **Not done** (1.6).
7. 50's `news:` channel and 59's Fowey port. **Not done**.
8. Taken up: 32f, the launcher, became 59, the harbour (M7b:35). M4's fitness drill was built by 37 (5c:20). 61's simple half and 63's small items went into 68 (M7b:146–150).

**What remains unbuilt of M7b** (M7b:31–47, 154–162):
- 51, the director's chart and focus, with its heart moved to M7's 82;
- 55, the solo director, the consent revision and the gate;
- 61's planner proper;
- 65, the place's knowledge, never briefed;
- 69, the Windows pins, booked;
- the director seated in a ship;
- a letter to another ship's captain (M7b:706–708);
- the drink sequence (M7b:943–954).

Why the milestone was frozen open: the owner wanted it closed efficiently, with the larger model's usage kept for M7's combat and signalling, "which the play made him want most" (M7b:117–119). The consent re-brief was to wait "until testing is to begin in earnest" (M7b:188–192; decision 51).

---

## The ten things that matter

1. **The director's hard limits do not refuse, and the record has said so since its first day.** Since 2026-10-17 the record says `nobody_dies` has "nothing yet ... to refuse" (M7b:321–322). Decision 50 still calls the limits refusals, and the 10-22 review misread the limit as holding (review of 10-22, line 629). No `aboard:` entry is deadly (`data/director/aboard.yaml`; `agents/director.py:338-341`).
2. **The director's reach onto the player's ship through `captain:` was never seen by the project.** 62's record claims reach for the player's ship through the hand only (M7b:683–684). `captain:` is dispatched before the reach check (`world/orders.py:272-273` against `300-303`), and the code calls it "the director's seam" (`orders.py:120`).
3. **No gate has been passed whole since 2026-10-15.** m6a-2 was not cut (M6:1819). 6c ran 5 of 13 items (`gate-m6c.md:3`). 7b was frozen unrun (M7b:188–192). The README says "gate m6c passed" (`README.md:5`).
4. **Spec items are silently cut at briefing.** Gate 6c's ten findings for 58 (TechnicalSpec-M7b:2243–2249) are absent from 58b's brief (M7b:1303–1361). "All sail in a chase" is not in the King's ship's book (`kings-ship.yaml:215-219`).
5. **Player Python was handed on and dropped.** The 5c close-out (5c:119–120) and M4 spec §24 hand it to M6, and nothing in M6 picks it up. `standing/python_api.py:28-29, 44` still promises it.
6. **"Green" has thinned.** It went from the builder's whole suite (M3-WorkPackages:15) to the fast tier and the touched files (M6:10–12), then to one suite per wave "at the owner's word" (M7b:404), with suites cut by restarts (M7b:720, 882–884, 415–416). The pins are written in after the run fails (M6:1188–1189, 1577–1578).
7. **The "perception on the player's terms" test is a string grep, and the code was arranged to keep it passing.** The far brain was put in `brains.py` "so that the truth-road proof on `captains.py` must keep holding" (M6:1508–1511; `tests/test_captains.py:275-296`; `captains.py:4326-4337`).
8. **The truth on the wire was kept by a decision while the record promised the opposite.** M5:3073–3075 against `world/lookout.py:634-650` and `tests/test_lookout.py:103`.
9. **The project knew and booked several of the review's findings.** The harbour open to any client of a tunnel (M7b:748–755); the consent brief's "to come" (M7b:141–142, 231–232); the newcomer's harbour (M7b:76–78, struck into 96); the station's brief as the system prompt, by the lead's own brief (M6:735–736); the hand-kept tiers (M7b:507–509).
10. **The project makes its own rule against expected failures and breaks it.** "An expected failure on a trial is a debt, not a pin ... nothing else may be marked so" (M7b:858–860) was broken by 68 and 58b in the same week (M7b:569–571, 1366–1369). A test's radius was changed to make the merged tree pass (M7b:406–413).

## What I did not read

- `docs/dev/M5-WorkPackages.md` lines **84–664** and **704–2675**. That is packages 30 to 32b, 32d to 37g, the follow-ups of gates 5b and 5c, and the M5 records in that span, read by their headings only.
- `M3-WorkPackages.md`, `M3b-` and `M4-WorkPackages.md`, beyond one line each for the head rule.
- `docs/dev/TuningNotes.md`, which the records cite as the full account of every pin.
- `docs/design/ColdReview-2026-09-30.md` and the gate 5c `report-2.md`.
- The 10-22 review beyond the lines named at the head of this file.
- `M7-WorkPackages.md`.
- The gate documents other than `gate-m6c.md`.
