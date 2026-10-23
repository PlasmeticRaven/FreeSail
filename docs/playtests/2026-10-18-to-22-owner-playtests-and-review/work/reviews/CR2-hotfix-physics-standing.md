# CR2: Code review of the hotfix's physics, ground and standing-order changes (B to H)

## Scope

**Span (transcript times are UTC; ship times are marked "ship")**
- 2026-10-21 04:30 to 11:57: `chunks/director-6.md`, read in full. It covers the grounding explained, the repair hotfix, the kedge, the well, the starter-book change and the suite runs with their re-pins.
- 2026-10-22 00:44 to 02:28: `chunks/director-7.md` and `director-8.md`, around the Edit, Bash, `ground.py`, cable and log-spam hits. This covers the checkpoint crash and its fix (the only `ground.py` change on 22 Oct), the kedge in live play off Horta, and the swing log spam.
- Related tool calls in `director-1.md` (2026-10-20 00:09): the session's own edits to `places.py`, `ports.py`, `sights.py` and `reckoning.py`.

**Versions**
- H, at rules fingerprints d89d1d7362914b8c and then 372c899e355594fa (the Horta save's `builds`).
- Compared against B, G and the merged tree. The merged tree holds the H content of every file in this slice, LF-normalised.

**Seats**
- The owner is captain.
- Opus 5.5 is director and also wrote the hotfixes (the Claude Code session "Sailing game scenario design").

**Files read**
- `work/diffs/hotfix-code.patch`: the hunks for `world/ground.py`, `physics/anchor.py`, `evolutions/scripts.py`, `standing/grammar.py`, `orders/__init__.py`, `starter.orders`, and the nine tests in the slice. I also read the hunks for `api/readings.py`, `agents/tools.py`, `test_readings.py` and the `aboard:` effects in `world/orders.py`, for context.
- `hotfix-docs.patch` and `hotfix-tuningnotes.patch`.
- H in full: `ground.py`; `anchor.py` lines 1 to 300; `LayOutKedgeScript`; `integrate.py` (the aground and anchor parts); `chart.aground` and `chart.danger_under`; `World._tick_tide`; `.gitattributes`; `fingerprint_of`.
- `github-pkg66.patch` (the `test_agents` and `test_known_truths` hunks), and the merged versions of those two tests and of my files.
- `testruns/*-fast.txt`, the specs (M4 §24, M5 §18 and §32, M6 §7 and §30), and DesignProposal §3.4, §4.3 and §9.
- The scratchpad helpers' commands, as quoted in the transcript.

**Not run**
- No tests, per the brief. The coordinator reports that the slow tier fails the same nine tests on an untouched G and on the merged tree.

## Narrative

- **04:30 to 04:34, 21 Oct.** The owner asks how the cutter ran aground off Horta. The director explains: the anchor was let go with way on, and the furl was queued behind veering the cable. The owner: "if I weren't the developer, I would have just hard rage quit there" (04:33).
- **04:35 to 04:49.** The owner raises repair. The director adds two `aboard:` things, `leak_stopped` and `well_pumped`, with a test in `test_ground.py`. It runs the suite; the starter-brief test fails on the owner's own brief file.
- **05:01 to 05:31.** The owner reports `lay out a kedge` was refused aground. The director proposes a ground-grip rule. The owner: "I say we do the honest and conservative implementation" (05:31).
- **05:33 to 05:37.** The kedge work, in three pieces:
  - `anchor.py`: heaving at the capstan loses its exemption from dragging when the ship is aground.
  - `scripts.py`: the "she is aground" guard on laying out the kedge is gone.
  - `ground.py`: `grip_kn` and `_heave_off`.
  - The first try at detecting the kedge coming home failed (the physics clears its flag first), so it was redone as "the distance to the anchor shrinking".
- **05:39.** The probe on the frigate test: at low water the kedge pulls 8.6 kN against 617 kN of grip and comes home; on the flood it heaves her off 21 minutes before the tide alone would.
- **06:49 to 06:53.** The owner asks for "sound the well".
  - The well becomes a reading, the carpenter's last sounding, kept in `ship.extra["well_sounded"]`.
  - `sound_well` is first a `Ground` method. It is moved to module level because `world.ground` exists only when the scenario has a chart.
- **06:53.** The director warns that the starter book's held well order would now fire every glass. The owner: "The simplest solution will probably be removing the standing order" (06:54). The order is removed and its comment says how to enter it.
- **06:55 to 07:11.** The tests and primers are updated by Python heredoc scripts. This is the start of the CRLF conversion (finding CR2-10).
- **07:11 to 10:10.** The full suite runs with the slow tier and gives 18 failures.
- **10:12 to 11:57.** Triage by bisection with scratchpad plugins (`oldwell_plugin`, `nokedge_plugin`), a temporarily re-appended starter line, and a temporary `sed` of `anchor.py`.
  - Three passages and truth 49 move only because of the starter book, and are re-pinned.
  - Seven pins are classed as failing before this work, and blamed on the "2026-10-19 evening changes … (package 65's era)".
  - All of this is recorded in TuningNotes.
- **00:44 to 00:49, 22 Oct.** The owner restarts at the stand-down save. The first tick aground with a taut cable crashes the clock thread: `AttributeError: 'Ground' object has no attribute '_anchor_dist'`. The fix gives the two attributes class-level defaults; this is the only `ground.py` change on 22 Oct.
- **Ship 10:22 to 10:35, 2 Jul.** The kedge is let go 90 fathoms to the SE by E. One ship-minute later the log says "The kedge comes home along the ground: she lies too hard on…" (10:23). The hawser was only "taut to the capstan" at 10:35.
- **Ship 10:39 onward.**
  - "Man the pumps" is refused in stale words.
  - The director pumps her out by `aboard: the well pumped out` every glass, about 15 times.
  - The kedge is hove home to 12 fathoms.
  - "Weigh the kedge" is refused aground (journal 15:14 ship).
- **Ship 19:21.** "She is hove off by the kedge, and afloat again on the flood." The new rule worked in live play, nine and a half hours after the strike.
- **Ship 20:44 onward; 02:14 to 02:28 UTC, 22 Oct.**
  - The owner asks: "Do you see that log spam of the cable swinging to flood and ebb?" The source is `core/world.py` `_tick_tide`, not `ground.py`.
  - No code was changed. The spam and eight other bugs went into a new TuningNotes section, "Open, for the lead", on the owner's word ("Leave it for now, note it for the lead session", 02:13).

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| CR2-01 | bug | med | The kedge-home line fires at let-go, before anyone heaves.<br><br>Cause, traced in code (an inference): `LayOutKedgeScript` sets `depth_m` from the depth at the *ship* (`_water_depth`) and `scope_m = out_m`, the horizontal distance.<br><br>Within a minute `World._tick_tide` re-reads the depth where the kedge lies. Then hypot(out_m, depth) > scope, the hawser is over-stretched, and the cutter's 30 kg kedge (holding at most about 0.9 kN) drags. `_heave_off`'s distance test then reports it as "comes home". | Ship 10:22: "The kedge let go … ninety fathoms to the SE by E."<br><br>Ship 10:23: "The kedge comes home along the ground: she lies too hard on".<br><br>Ship 10:35: "the hawser taut to the capstan" (director-7, about 00:56 UTC 22 Oct). | DesignProposal §1, §3 ("honest"); M5 §18 | Let the kedge go with scope ≥ hypot(out_m, the depth at the kedge's place), so the hawser lies slack until hove taut. Say "comes home" only while a heave on that anchor is in hand. Add a test of the let-go sequence. | Open in H and merged. The geometry is from B; the hotfix's line made it visible. |
| CR2-02 | realism | med | Aground, `heave in` drags the kedge home. There is no "heave taut", "keep a strain" or "pawl the capstan".<br><br>Primer 13's recipe, `heave in the kedge to twenty fathoms`, "hauls the hawser taut". In the game it drags the kedge from 90 to 20 fathoms, and the steeper cable cuts its holding (`holding_n` lift). The test does the same.<br><br>A seaman of 1805 heaves taut, pawls, and holds the strain as the tide makes. | Journal at ship 15:14: kedge "home at 12 fm".<br><br>"pawl the capstan" is listed as not understood (TuningNotes, open for the lead).<br><br>Pascoe in character (ship 13:13): "Heave her short now an' … nothing left to heave on". | DesignProposal §9 ("kedging off"); §1 | Aground, the capstan should stop when the cable's load reaches what the anchor holds (or what the hands can heave), with a line like "hove taut; she does not come". Add a `heave taut` / `keep a strain on` form. Fix primer 13's recipe. | Open (H, merged) |
| CR2-03 | realism | med | **The grip-against-pull rule is binary in practice.**<br><br>Grip per cm of water she lacks: about 2.7 kN for the cutter and about 15 kN for the frigate (0.4 × ρg × 0.75 L × B). A kedge holds at most about 0.9 kN (cutter) or about 9 kN (frigate). So the pull wins only within millimetres of her draught.<br><br>The kedge's whole effect is waiving the 0.3 m `AFLOAT_MARGIN_M`. Its gain is the time the tide takes to rise a foot: 21 minutes in the test.<br><br>**The docs overclaim.** The `ground.py` docstring says the kedge "keeps her from being driven further on", but nothing drives a grounded ship anywhere (`integrate.py` holds her; sail thrust aground is not modelled). Primer 13's "twenty minutes to an hour" depends on the tide's rate. | Probe at 05:39 UTC: "pull_kn 8.6, grip_kn 617.4".<br><br>TuningNotes itself: "Within the afloat margin she lacks none, and any strain heaves her off". | M5 §18, §32 ("the kedge" later); DesignProposal §3.4 | Accept it as the owner's "honest and conservative" ruling, and say plainly in primer 13 and the docstring that the kedge gets her off as she floats. Drop the "driven further on" claim.<br><br>For milestone 8: capstan purchases, a bower carried out by the launch, lightening, and sails laid aback. | H, merged; documented in part |
| CR2-04 | bug | low | "Hove off by the kedge" is said for any taut cable. `_heave_off` sums every taut anchor in `tackle.down()`, kedge or not, hove in or not. A ship that grounds with a bower taut to seaward is "hove off by the kedge" with no kedge out. | `ground.py` `_heave_off`; TuningNotes: "A ship riding by a taut bower … is helped the same way". | M5 §18 (the log's words) | Name the anchor or anchors that pulled ("hove off by the best bower"), or say "by her cable". | Open |
| CR2-05 | bug | high (in play; fixed) | The kedge hotfix crashed the live game's clock thread. A Ground restored from a pre-hotfix checkpoint lacks the attributes `__init__` sets.<br><br>The 22 Oct fix (class-level `_came_home_said = False` and `_anchor_dist = None`, guarded in `_heave_off`) is correct, and matches the project's "class default, so a checkpoint from before loads" idiom. No test restores an older Ground. | Owner at about 00:46 UTC 22 Oct: "got an error, I think the clock is stuck by it". | DesignProposal §3.2 (saves) | Add a regression test: build a Ground by `__new__` or unpickle a pre-hotfix one, then tick it aground with a taut cable. Add a review rule: every attribute on a checkpointed class gets a class default. | Fixed in H; merged has the fix |
| CR2-06 | test | low | **The re-pins are justified and recorded.** They are GATE_5A_DAY 625→623 / `bff57a…`→`1680cb…`, GATE_5B 733→731 / `c8c81b…`→`9a1f28…`, GATE_5B_THICK 471→469 / `155a46…`→`6f062d…`, and truth 49's input check inverted.<br><br>Cause: the owner's ruling took the held well order (two lines) out of every passage that reads the starter book. The session proved each by restoring the absent row and the held order together; the old pins came back.<br><br>**Gap:** some earlier-value chains were cut from the comments: "729 at package 57", `5f682b9f676a2db4` at 57, "495 at package 37p", `e358748a1eae5fc6` at 45. | `test_known_truths.py` lines 2523–2524, 2971–2973, 3031–3032; TuningNotes "The well, sounded" (old→new).<br><br>06:54 UTC 21 Oct: "removing the standing order 'sound the well' from the starter book". | Project pin practice (comments keep old values) | Accept the re-pins. Restore the cut history in the comments. | Re-pins hold on merged; coordinator: the merged slow tier fails only the 9 that G fails |
| CR2-07 | docs | med | **The cause given for the seven failing pins is wrong.**<br><br>TuningNotes blames the "2026-10-19 evening changes to `world/ports.py`, `reckoning.py`, `places.py` and `sights.py` (package 65's era)". Those four B→H diffs are this session's own "things found aboard, widened" hotfix, made at 2026-10-20 00:09 UTC (19 Oct 20:09 local, `director-1.md` lines 1732–1790). G lacks them and fails the same seven (coordinator).<br><br>"Failing before this work" is right; the named cause is not. The proposed session card `task_cfc0ee5b` points the lead at those four files. | TuningNotes: "Likely the 2026-10-19 evening changes to `world/ports.py` …". | §24 packages; TuningNotes practice | Before the fold-in, correct the paragraph: they fail on G too, cause unknown (B, or Windows). Re-scope `task_cfc0ee5b`. | H's TuningNotes (merged with one conflict) |
| CR2-08 | bug | med | "Man the pumps" and "rig the pumps" are refused in false words. `data/vocabulary.yaml:1923` still says "she makes no water … the well is not sounded … 'Sound the well' says so".<br><br>Stale comments also remain in `orders/prompt.py` 175 and 195–196, `standing/grammar.py` 258–260, `standing/runtime.py` 35 and `standing/rules.py` 507. | Journal at ship 10:39 (01:00 UTC 22 Oct): refused "with STALE words". | DesignProposal §1 (words that help) | Reword it: the pumps are milestone 8's; `sound the well` has the carpenter sound it. Update the stale comments. | Listed in "Open, for the lead"; unfixed in H and merged |
| CR2-09 | test | med | **Package 33c's "held order" path now has no use and no test.** The registry has no absent rows left (05:11 UTC probe: `[]`). The only held test was replaced. `test_readings`' loop over absent rows is now empty.<br><br>The code remains in `grammar.py` `held`, `Rule.held`, the runtime's skip, the book's "Held until" and `python_api`.<br><br>`held` is set only when the order is entered. A save from before the hotfix with the starter book loaded keeps its well order held forever, under the old sentence. | `grep add_absent tests/` finds nothing.<br><br>The 37d fixture save carries the order; the owner's recent saves do not (checked). | M4 §24 item 4; 33c | Keep a test with a monkeypatched `REGISTRY.add_absent`, or retire the mechanism. When a save loads, re-check its held rules against the registry. | Open |
| CR2-10 | harness | med | **13 files were converted LF→CRLF.**<br><br>Cause: the session's `py - <<'EOF'` scripts did `Path.read_text(encoding="utf-8")` then `write_text(…, encoding="utf-8")` with no `newline=`. On Windows that writes CRLF. Every file the Edit tool touched stayed LF.<br><br>Times on 21 Oct (UTC):<br>- `ground.py` 06:53:20<br>- `test_agents.py` and `test_orders_m4a.py` 06:55:52<br>- `test_replay.py` 06:57:02<br>- `test_standing.py` 06:57:14 and 06:58:58<br>- `grammar.py` 06:57:45<br>- primers 06, 07, 10, 11 and 13 at 07:11:25<br>- `test_orders.py` and `test_python_api.py` 10:12:59<br>- `test_known_truths.py` 10:59:47 to 11:44:24<br><br>`test_weather_script.py` went CRLF at 10:12:59 and back to LF at 11:02:46 by Git Bash `sed -i`.<br><br>**Risk:** none at run time (Python reads either; `fingerprint_of` normalises CRLF, which `test_replay` guards; ruff's line ending is auto).<br>- Whole-file diffs of test files 3,000 to 7,000 lines long. The coordinator had to LF-normalise to review and to auto-merge.<br>- `.gitattributes` has no `* text=auto`, so a commit with `core.autocrlf=false` would put CRLF into the repository.<br>- A latent hazard: `test_orders_m4a` asserts no `\r` in `starter.orders`, and a script that touched it would break that test. | The `py - <<'EOF'` commands at those times. `eol.py`: H has 1371/0 CRLF/LF in `grammar.py` and 6869/0 in `test_known_truths.py`; B and G are all LF. | n/a | Fold in from the merged (LF) tree, not H's files. For future scripts, use `newline="\n"` or the Edit tool. Owner's call: `* text=auto eol=lf`, keeping the existing `-text` lines. | H CRLF; merged LF |
| CR2-11 | design-gap | low | **"Weigh the kedge" is refused aground.** `WeighAnchorScript` keeps its guard while `LayOutKedgeScript` lost its own. That breaks the lay out, heave, weigh and lay out again cycle. "Let go" is refused aground too. | Save inputs at ticks 2109493, 2125271 and 2125288: "Weigh the kedge".<br><br>Journal at ship 15:14: weigh refused "aground". | DesignProposal §9 | Let the kedge be weighed aground, by the capstan or tripped by the boat. Consider letting an anchor go to stop her driving further on. | Listed in the open notes; unfixed |
| CR2-12 | design-gap | low | **The well is read, never compared** (`WELL_NOT_COMPARED`). DesignProposal's own sketch is `when the well exceeds 2 feet then man the pumps`.<br><br>The starter book now has no well routine at all. The ship's regulations as spec M3 reads them have the carpenter sound "twice at least in each watch". | `grammar.py` lines 382–387; DesignProposal §4.3 example. | DesignProposal §3.4 item 7, §4.3 | Deferring to milestone 8's pumps is consistent. Comparing against the last sounding would be harmless now. A quiet once-a-watch carpenter's report is an option (owner). | Deferred (M8) |
| CR2-13 | realism | low | The leak runs only while she is aground (`_leak` is called only when `grounded`). A hull strained on the ground stops making water the moment she floats, which is the reverse of period experience. Not caused by the hotfix; TuningNotes records it. | TuningNotes: "the leak runs only while she is aground". | DesignProposal §3.4 item 7 | Milestone 8, with the pumps. | Pre-existing |
| CR2-14 | spec-deviation (idiom) | low | **Layering.**<br>- `sound_well` and `well_words` (the hull's well, for every ship) live in `world/ground.py`, and `orders/__init__.py` imports them.<br>- `_fx_well_pumped` in `world/orders.py` writes `Ground._feet_said` and `_waterlogged_said`.<br>- `Ground` annotates `_anchor_dist` twice, with different types. | Code | The codebase's shape (DesignProposal §8.2) | Move the well to its own small module, and give `Ground` a public reset for the carpenter's counts. | Open |
| CR2-15 | test | low | **Gaps in the new tests:**<br>- a kedge laid toward the shoal (no heave-off)<br>- the rock friction<br>- the let-go sequence (CR2-01)<br>- a restored Ground (CR2-05)<br>- a non-kedge cable's wording (CR2-04)<br>- the "less than at the last sounding" branch<br>- the `sound the pumps` and `pump well` aliases<br>- the ship-alone refusal<br><br>`test_orders.py`'s well row now checks only the event's kind. | The diff hunks of `test_ground.py`, `test_standing.py` and `test_orders.py`. | n/a | Add the cases, cheaply, to the same files. | Open |
| CR2-16 | harness | low | The bisection edited files in the folder the live game runs from: a line appended to `starter.orders` and a `sed -i` on `anchor.py`, each restored by `cp` (10:19–11:27 UTC 21 Oct). Both came back clean (`anchor.py` mtime matches the restore). A restart in those windows would have played under different rules. | 10:19:52, 10:47:31, 10:54:32 and 11:02:58 UTC commands. | n/a | Bisect in a copy or worktree. | Process |
| CR2-17 | docs | low | **Primer nits.**<br>- 13 says "Each minute" the strain is weighed; it is every tick.<br>- 06's sample reads "The well: the well not sounded yet".<br>- The "Brought up … in 16½ fathoms" line logged while she was aground made the director believe she was afloat (journal 00:55 UTC, corrected 00:56). A pre-existing bug in the ground and anchor area. | Ship 09:48: "Brought up by the best bower in 16 fathoms and a half". | M5 §18 | Fix the wording. Suppress "brought up" while aground (already in the open notes). | Open |

### Per-change table

| File | What changed | Verdict | Reason |
|---|---|---|---|
| `freesail/world/ground.py` | **21 Oct:**<br>- `grip_kn` and `_heave_off` (taut cables' pull, capped at holding, against the ground's friction × the weight it bears; a quarter-length step if the water there serves)<br>- `_afloat(kedged)`<br>- the `ground.kedge_home` line<br>- module-level `sound_well` and `well_words`<br>- the docstring<br><br>**22 Oct:** class-level defaults for the kedge's memory (the checkpoint crash). The swing spam was *not* changed in code. | Accept with fixes | The physics is sound in magnitude, conservative as ruled, and deterministic. It needs CR2-01 (spurious come-home), CR2-03 (the docstring overclaim), CR2-04 (wording) and CR2-14 (placement). The 22 Oct fix is correct (CR2-05). The file is CRLF in H. |
| `freesail/physics/anchor.py` | `if anchor.heaving and not aground`: hove in aground, past its holding, the anchor drags home. | Accept | Physically right: the anchor, not the ship, gives way. Bisected: it moves no pin. The capstan should also stall (CR2-02). |
| `freesail/evolutions/scripts.py` | The "she is aground" guard is removed from `LayOutKedgeScript.check`. | Accept | Carrying out a kedge is the remedy for a ship on the ground. The weigh guard was left in (CR2-11). The let-go geometry is a pre-existing bug (CR2-01). |
| `freesail/orders/__init__.py` | `sound the well`, `the pumps` and `pump well` go to the carpenter's sounding, never the lead. | Accept | The behaviour and words are right ("two feet and four inches of water, and gaining"). Idiom note in CR2-14. |
| `freesail/standing/grammar.py` | `WELL_NOT_COMPARED`, `_HOW["well"]`, and the refusal in `_parse_comparison`. | Accept | An honest deferral (CR2-12). A stale docstring remains at lines 258–260 (CR2-08). CRLF in H. |
| `freesail/api/readings.py` (context) | `the well` becomes a real reading: the last sounding with its age, and "not sounded yet" before one. | Accept | It is observed, not truth, which fits the M7b observed world. |
| `freesail/agents/tools.py` (context) | The "(refused until…)" note is dropped, and the "Not yet in the ship" line shows only if any reading is absent. | Accept | Correct now that no reading is absent. |
| `data/standing_orders/starter.orders` | The held `sound the well` order is removed; the comment says how to enter it. | Accept | The owner's ruling. It stays LF, so `test_orders_m4a`'s check that it holds no CR still passes. Realism option in CR2-12. |
| `data/vocabulary.yaml` | Not changed. | Change needed | The pumps refusal is now false (CR2-08). |
| `tests/test_ground.py` | Two new tests (the repair; the kedge against the flood alone) and two helpers. | Accept | Good comparative design (the same seed with and without the kedge). Gaps in CR2-15. |
| `tests/test_known_truths.py` | Three passages re-pinned; truth 49 now finds no well input. | Accept | Justified, bisected and recorded (CR2-06). Restore the cut history. CRLF in H; merges clean with G's truths 7b-117 to 119. |
| `tests/test_standing.py` | The held-well test is replaced by a sounded-every-glass test, and the table row's refusal words changed. | Accept | It covers the order, the reading, the cadence, the trend and the replay. The held path is lost (CR2-09). CRLF. |
| `tests/test_orders.py` | `HELD` removed; the well row expects a plain `standing.given`. | Accept | Weaker than before (kind only). CRLF. |
| `tests/test_orders_m4a.py` | Starter count 8→7; the test renamed; no held line. | Accept | Follows the ruling. CRLF. |
| `tests/test_python_api.py` | `sound.rule.held is None`. | Accept | Follows. CRLF. |
| `tests/test_replay.py` | Truth 39's voyage loads every starter line. | Accept | Follows. CRLF. |
| `tests/test_weather_script.py` | Count 13→12; the held assertion removed. | Accept | Follows. LF again, after `sed`. |
| `tests/test_agents.py` | Starter count 8→7. | Accept | Merged with G's station-line asserts; no clash. CRLF in H. |
| `tests/test_readings.py` (context) | The absent-rows test loops over every row; the well is asserted present. | Accept | The loop is now empty (CR2-09). |
| `docs/primer/06`, `07`, `10`, `11` | The well's words; the starter listing without the well order. | Accept | Accurate. CRLF. A small nit in 06 (CR2-17). |
| `docs/primer/13` | The well sounding, and the "Or she is kedged off" bullet. | Accept with fixes | The recipe drags the kedge home (CR2-02); "Each minute"; overclaim (CR2-03). CRLF. |
| `docs/primer/14` | A sentence: the kedge works aground. | Accept | Accurate. |
| TuningNotes (the hotfix's sections) | The repair, the kedging off, the well sounded, and "Open, for the lead". | Accept with a fix | Thorough, with old→new pins. The cause given for the seven failures is wrong (CR2-07). |

## What worked well

- **Pin discipline.**
  - The session did not re-pin blindly. It bisected each moved pin by restoring the old absent row and the old held order together via pytest plugins, and ruled out the kedge and anchor changes.
  - It re-pinned only the three passages and the truth-49 check the starter book explains, and wrote old→new into TuningNotes. That is exactly the project's practice.
- **Honest physics in sensible units.**
  - The grip is lost buoyancy × friction, capped at the displacement's weight.
  - The pull is capped at what the anchor holds.
  - The step is checked against the tiles and the charted dangers.
  - The order of magnitude is right: a 300 kg kedge cannot shift a frigate sitting on the sand at low water. The conservative ruling was respected.
- **The kedge worked in live play.** She came off at ship 19:21 "hove off by the kedge … on the flood", and the owner kept playing.
- **The well reading follows the observed-world principle.** It is the carpenter's last sounding with its age, not the truth. The period idiom fits: "two feet and four inches of water … and gaining".
- **The checkpoint crash was fixed in two minutes, in the project's own idiom**, and the lesson was carried into the swing-spam note ("a class-level default").
- **New bugs were noted, not patched.** After the kedge and well work, the session wrote nine found bugs into "Open, for the lead" on the owner's word, instead of hot-patching more of the live tree.
- **No semantic clash with G.** Both shared tests merged cleanly. G's additions pin nothing the hotfix moved, and the merged fast tier fails exactly G's four.

## Model behaviour and experience

- **The director (Opus 5.5) was candid about limits** before building. At 05:25 UTC it said the kedge "won't haul her straight off at dead low water". The owner chose that over a quick fix.
- **The in-character seamanship was better than the game's.**
  - Pascoe at ship 13:13: "Heave her short now an' … nothing left to heave on". That is correct seamanship; the game has no way to "hold the strain" (CR2-02).
  - The director also told the owner out of character that laying a sail aback has no effect aground.
- **Tooling slips under live pressure:**
  - The heredoc rewrite habit converted the files to CRLF (CR2-10).
  - It edited files in the live tree to bisect (CR2-16).
  - It ran the suite with output held until the end ("That was my mistake", 09:20 UTC).
  - It misread the truth tool as "not aground" (00:55 UTC 22 Oct; corrected a minute later).
- **It did not recognise its own earlier edits.** Its 20 Oct `aboard:` widening of `ports.py`, `places.py`, `sights.py` and `reckoning.py` was blamed on "package 65's era" (CR2-07).
- **The owner's experience.**
  - The grounding nearly ended the run ("hard rage quit", 04:33 UTC 21 Oct).
  - The repair, kedge and well hotfixes turned it into a nine-hour scene with the pump every glass and a kedge on the flood.
  - The remaining friction is the game's grammar: the refused weigh, "pawl the capstan", the stale pumps refusal, and the swing spam ("log spam of the cable swinging to flood and ebb?", 02:1x UTC 22 Oct).

## Open questions for the owner

1. Aground, should heaving at the capstan stop at what the anchor holds ("hove taut; she does not come"), and should there be a `heave taut` / `keep a strain on` form? Today it drags the kedge home, and the primer tells you to.
2. Is the kedge's present effect (waiving the foot-of-water margin, 20 to 60 minutes) what you want until milestone 8? Or should capstan purchases, a bower carried out by the launch, lightening, or sails aback count sooner?
3. The well routine: keep the starter book without one, or add a quiet once-a-watch carpenter's report? And may the well be compared now (`when the well exceeds 2 feet then …`) against the last sounding?
4. Should the repository adopt `* text=auto eol=lf` in `.gitattributes`, so a Windows hotfix copy can't commit CRLF?
5. May the TuningNotes cause for the seven failing pins be corrected (to: they fail on G too, cause unknown), and the proposed session card re-scoped accordingly?
