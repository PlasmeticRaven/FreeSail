# Report: package 90, the engine track

The engine track's builder reports here, one section per step, the file pushed last after each
step's commit (and pushed also when a step stops early, with why). Branch
`…/pkg-90-engine`, cut from package 90's stage 0L merged with the trunk, d8857629.

## Step A2: the words of a rig with no yards, mended at their cause (2026-11-20)

**Commit:** **00f0604bca22318016eaca7d92374edbf2dcbcb1** on `…/pkg-90-engine` (parent d8857629). One commit, to be merged alone
before A1a.

**Files (8, each in the engine track's §7.1 row or a pin §10.4 names for A2):**
- `freesail/evolutions/scripts.py`: the mend (two readers, `has_braced_yards` and `braces_manned`,
  and the lines that read them);
- `data/evolutions/tack.yaml`, `heave_to.yaml`, `fill_away.yaml`, `scud.yaml`: their fixed lines
  given a word from the script (`{fell_off}`, `{braces}`, `{braced_full}`);
- `tests/test_rig_words.py`: new (a name §7.1 gives the engine track);
- the moved pins: `tests/test_settee.py`, `tests/test_evolutions.py`,
  `tests/test_rig_geometry.py`, `tests/test_captain_trials.py`, `tests/test_known_truths.py`;
- `docs/dev/TuningNotes.md`: "Package 90, A2", every move old beside new with its reason.

No ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). No class is
added (two functions), so truth 7-606 and the checkpoint's list are not touched. LF only; ruff
clean; no line over 100 characters. Nothing under `docs/agents/consent/`; the primer not edited.

### The cause, and the mend

The going-about evolutions and their kin named braced yards and braces without reading whether
she has them. A lugger's and a boat's lug yards are no braced yards, and the cutter, the smack and
the two schooners have head yards alone. **Mended where the words are made, for every rig:** a line
that names a braced yard or its braces is said only where she has one, read from the yards the
evolution itself swings (`head_and_after_yards`; `working_yards` for the scud and the anchor), so a
ship whose yards are shot away is not told to brace them either. The new words are JUDGEMENT:
"full and by" (or "trimmed" before a course's clause) for "braced up"/"braced sharp up"; "head
braces" or "sheets" for "after braces"; "Right the helm." for "Braced the yards full."; the braced
or squared clause dropped elsewhere. The table of every line, old beside new, with the rigs it
moves on, is in `docs/dev/TuningNotes.md`, "Package 90, A2".

**The lines mended (16, in 10 evolutions):** the tack's end, its luff up for a course and its
fallen-off line after a miss; the wear's up-helm line (both branches), its wind-aft line and its
end; the heave-to's and the fill-away's first lines; the fill-away's falling-off line and its end;
the box-haul's, wear short round's and box her off's wind-aft line; the scud's two first lines;
the come-to-anchor's brought-up line; and get under way's two topsail-yard phrases on a boat at her
grapnel.

### The proof that every tick is the same

The session's scratch harness (`a2/harness.py`, `a2/compare.py`): all eighteen files from four
starts (the lugger transcripts' settle, seed 7, 15 kn; off the wind; the same settle in 5 kn; the
anchor's road in Carrick Road; and off Falmouth in three fathoms and a half, where a boat lies to
her grapnel), each order run from a copy of the settled world: tack, wear, heave to and fill away
(by the wind and for a course), box haul, wear short round, box her off, scud, back and fill, lie
a-try, a course across the eye and across the stern, a tack in 5 kn, come to an anchor and get
under way. For each run every event (tick, kind, text) and a 10-second trace of heading, speed and
position, at the base and on the mended tree.

**270 runs: in every one the ticks, the event kinds, the orders' answers and the trace are
identical. 88 lines move, in 51 runs, all words, all on the ten rigs the table names (the lugger
18, the cutter 9, each schooner 9, the smack 8, each boat 7); not one line moves on the eight rigs
with after yards.** The ground report's 18 lines in 11 runs are among them, line for line. The two
digests' passages (below) agree: every tick and kind the same, only those words.

### Each moved test, old beside new, with its reason (the reason of all: the words of a rig with no yards, at their cause)

| Test | Old | New |
|---|---|---|
| `tests/test_settee.py::test_the_luggers_tack_and_wear_are_as_they_were[tack ship-lines0]` | 180 s: "Tacked; braced up on the larboard tack, heading ENE (68°)." | "Tacked; full and by on the larboard tack, heading ENE (68°)." |
| the same, `[wear ship-lines1]` | 1 s: "Stand by to wear ship. Up helm; brace in the after yards."; 36 s: "Wind aft. Shifted over the sheets; hauled out and braced up. Lowered the foresail and the mainsail to dip them."; 171 s: "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)." | "Stand by to wear ship. Up helm."; "Wind aft. Shifted over the sheets. Lowered the foresail and the mainsail to dip them."; "Wore ship; full and by on the larboard tack, heading ENE (68°)." |
| `tests/test_evolutions.py::test_with_no_head_yards_the_wear_squares_none[the lugger]` | "Wind aft. Shifted over the sheets; hauled out and braced up." | "Wind aft. Shifted over the sheets." |
| `tests/test_rig_geometry.py::test_going_about_lets_the_bowlines_go_and_steadies_them_out_again[wear-schooner]` | "Stand by to wear ship. Up helm; clear away the bowlines; brace in the after yards." | "Stand by to wear ship. Up helm; clear away the bowlines." |
| `tests/test_captain_trials.py::test_the_merchant_hauls_off_from_a_privateer_and_waits_in_the_road_for_a_wind` (slow): `TRIAL_TRADE_STRANGER_DIGEST` | 48c8948f87088a76 | 323b8966ceab6857: seven lines' words of 1,594, the schooner's "Hands to the head braces; heave to." (11094, 34488, 66601), "Fill away; man the head braces." (12493, 35890, 67820) and "Stand by to wear ship. Up helm." (34201); the states as pinned |
| `tests/test_known_truths.py::test_truth_77_...` (slow): `GATE_5C_MERCHANT_DIGEST` | 16272dee77120779 | 8259996fb122428e: five lines' words of 3,096, the same words (17461, 18301, 89192, 90359, 90475); the cruise's digest holds |

**Four digests more, moved by the wider reach** (found by the slow tier whole; each passes at the
base; every tick and kind the same, line for line, traced at both): the schooner's "Hands to the
head braces; heave to." and "Fill away; man the head braces.", and in two of them her wear's first
line, "Stand by to wear ship. Up helm.":

| Test (slow) | Constant | Old | New | Lines moved |
|---|---|---|---|---|
| `tests/test_known_truths.py::test_the_schooner_sails_the_passage_with_her_octant_and_the_log_every_two_hours` | `GATE_5B_SCHOONER_DIGEST` | be166d89d06a1992 | 0fef1c52128ce9b2 | 3 of 766 (28741, 30178, 56925) |
| `tests/test_known_truths.py::test_the_schooner_on_an_intent_alone_at_seed_7_has_its_own_constants` | `GATE_6A_INTENT_DIGEST` | 5d3cbbc5f4d33b84 | 7239b1a1ed45736f | 11 of 2,079 (ten heave-to and fill-away lines; the wear's at 88141) |
| `tests/test_known_truths.py::test_truth_78_...` | `GATE_6A_FAKE_CAPTAIN_DIGEST` | f47f7bc0daabc950 | 50529f09d4de955e | 5 of 3,108 (the merchant passage's five) |
| `tests/test_captain_trials.py::test_in_thick_weather_near_the_land_the_merchant_runs_for_the_road_and_waits` | `TRIAL_TRADE_THICK_DIGEST` | 506bf46eaa6d66fe | f2f52d500f050950 | 2 of 426 (3901, 5323) |

**These four are not among the pins the card names.** I moved them as "what the wider reach moves"
(nudge 22's own category), because they move by the head-braces words alone (and the card's own
"both schooners' wear's first line"); but they are my reading, and a reader may hold them a stop.
See "Unsure" item 2.

Nothing else moved: no fast test, and no slow test but these six digests (below).

**Not moved, as the card asked:** the primer. Its lines A2 makes untrue, old beside new from the
harness's run of the topsail schooner (seed 7, 15 kn), for A1b's edit of chapter 5 and for the lead
on chapter 7, which no step names:
- `docs/primer/05-going-about.md:357`, the schooner's wear: "Stand by to wear ship. Up helm; brace
  in the after yards." -> "Stand by to wear ship. Up helm." (Its line 359 stands: true of her; it
  lacks "shifted over the sheets" already, older than A2.)
- `docs/primer/07-a-first-passage.md:339`, the *Speedwell* hove to: "Hands to the after braces;
  heave to." -> "Hands to the head braces; heave to." (her own line before it: "braced the fore
  topsail aback").
- `docs/primer/07-a-first-passage.md:349`, her fill away: "Fill away; man the after braces." ->
  "Fill away; man the head braces."

Every other primer line holding these words is the frigate's or the brig's, and stands.

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is d8857629**, a worktree beside the mended
tree; nothing was merged into the branch (see below).

| Run | Base (d8857629) | Mended tree |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,471: 8,462 passed, 8 skipped, 1 xfailed, 0 failed (1 h 34 min, the box loaded by the measures) | 8,500: 8,491 passed, 8 skipped, 1 xfailed, 0 failed (1 h 18 min). **Test by test: every one of the base's 8,471 the same outcome; 29 new, all `tests/test_rig_words.py`, passed** |
| **Fast tier whole again, after the mend of the four digests** (the session's rule: the mended tests, then the fast tier with its junit) | as above | 8,500: 8,491 passed, 8 skipped, 1 xfailed, 0 failed (1 h 26 min), on the committed tree. **Test by test: every one of the base's 8,471 the same outcome; the same 29 new passed** |
| **Slow tier whole**, `--slow -m "slow and not pace"` | the five below re-run: 5 passed | 568: 552 passed, 11 xfailed, 5 failed (1 h 31 min): the four digests above, and the browser round-trip (`tests/test_harbour.py::test_in_the_browser_a_game_is_started_and_the_four_scenarios_round_trip`, "assert 'schooner' in ''": the page read before it was written, under the tier's load; **it passes alone on this tree**, 53 s, and at the base) |
| **The six moved digest tests**, after their pins moved | the two named pass at the base with the old digests (measured) | 6 passed (17 min) |

**The guard set of §10.2 at A2**, tallied from the fast tier's junits, base beside mended, every
case the same outcome: the byte test and the golden classing table (`tests/test_ship_particulars.py`,
`tests/test_rig_classing.py`, truth 7-185) 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 86; `tests/test_check_viewer_guns.py` 21; the lugger's set (`tests/test_lug.py`,
truth 7b-111, `tests/test_captains.py`'s and `tests/test_view_geometry.py`'s lug cases) 58; the
settee's, `tests/test_settee.py`, 75; the going-about set (`test_gale`, `test_rig_geometry`,
`test_staying`, `test_lying_to`, `test_evolutions`, `test_captain_trials`, `test_catalogue`) 261; all
passed, at both. Their slow cases are in the slow tier whole above (their only failure
`trade_thick`'s digest, moved and passing since). The lens of a trace of the lugger's and the
frigate's tack, wear and heave-to at seed 7 before and after is the harness's (identical).

**The slow tier of the files touched** is inside the slow tier whole: `test_settee`,
`test_evolutions`, `test_rig_geometry` and `test_rig_words` (no slow case) all passed;
`test_captain_trials` and `test_known_truths` failed only the four digests, passing since.

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 files byte for byte with
`data/ships/`; no new ship file, so no `load_ship` or viewer-guns check of one.

**The package branch moved while A2 ran** (`…/pkg-90` at 8b8a982: package 119, the
merchant brig's watches, and N1 to N3). A2 needed nothing of it, so **nothing was merged into this
branch**; the base of every comparison here is d8857629. Checked for the merge: A2's diff applied
on 8b8a982 in a scratch worktree, the only conflict `docs/dev/TuningNotes.md` (both append at its
end; resolved there by keeping both sections whole, A2's after package 119's). There,
`test_rig_words`, `test_settee`, `test_evolutions`, `test_rig_geometry`, `test_lying_to` and
`test_hands` passed (333), and the six moved digest tests passed (6): package 119's `too_few` on
the heave-to and the fill-away, in the same two evolution files, sits on other lines and moves
none of A2's figures.

### Where else the cause was looked for

By the cause, not the examples: every string of `freesail/` naming a brace, a braced yard, the
after or head yards or squaring (parsed, all modules), and every base line of the harness's 270
runs on a rig with no braced yard naming a brace, a yard or squaring, and on a rig with head yards
alone naming after yards or after braces. Every such line is mended or found true of every rig that
reaches it:
- **mended**: the lines of the table (the ground report's four, the card's wider reach, and found
  beyond it: the tack's luff up and its fallen-off line, the scud's two lines, the come-to-anchor's
  "square the yards", the cutter's and the schooners' heave-to and fill-away "after braces", and the
  boats' get-under-way "The topsail yard abox." and "brace round the topsail yard");
- **left, keyed already** (earlier mends of the same cause): "Mainsail haul" on after yards, "Let
  go and haul" and "the head yards aback to box her off" on head yards, the urgent missed-stays
  line's "square the yards", the wear's "Squared the head yards";
- **left, true where reached**: "Haul taut the lifts and weather braces. Steady out the bowlines."
  (only with a bowline steadied out; a bowline is a square sail's, and no yardless file carries one);
  the box-haul family's other lines and back and fill and lie a-try (each refused without the yards
  it works); the heave-to's "Braced the ... aback" (on the yards laid aback); get under way's ship's
  road (two masts with yards); `_brace_up_for_the_helm` (a square sail set);
- **outside the engine track's files**, read and found keyed: `physics/integrate.py`'s "the yards
  are not trimmed" (a square sail set), `orders/navigation.py`'s across-the-stern line (yards
  aback), `orders/verbs.py`'s brace order (refused, "This ship has no yards to brace.");
  `world/captains.py` holds none of the words. **No file outside the row was needed.**

### Unsure, and for the lead

1. **The two digests' premise.** The card has them "in tests already failing at the base ... their
   outcome does not change". At this base, d8857629, both **pass** (their digests are their pins;
   the ground report's 5067945e failed both). So A2 must move them or turn them red. They are named
   in §10.4's A2 row, so I moved them, old beside new with every line traced; if the lead would
   rather they were ruled first, it is these two constants alone.
2. **The wider reach on rigs with head yards alone.** "Hands to the after braces" and "man the after
   braces" on the cutter, the smack and the two schooners: no example of the card's names them; I
   took them as the same cause ("after" braces where she has no after yards), and the schooners'
   own primer log shows it ("braced the fore topsail aback", then "Hands to the after braces"). They
   move four digests the card does not name (gate 5b's, gate 6a's intent's, truth 78's and
   `trade_thick`'s), and add six lines to the two it does. "head braces" is JUDGEMENT; the engine
   already calls these yards her head yards ("Squared the head yards", "Brace abox the head
   yards!"). **Were it ruled no part of the cause,** it is `braces_manned`'s middle branch alone:
   gate 5b's and `trade_thick`'s digests go back to their old figures, and the other four move
   still, by the wear's first line, which the card names.
3. **The words chosen** (all JUDGEMENT): "full and by" and "trimmed" (the ground report's
   candidate's); "sheets" for a yardless rig's heave-to and fill-away (Luce's fore-and-after heaves
   to by her sheets); "Right the helm." where a yarded ship "Braced the yards full."
4. **Found on the way, not built** (another cause, which no step names): a boat's anchor work is
   said in a ship's words (the messenger, the bars and the capstan, sail-loosers aloft, a topsail and
   a jib she has not, "Hook the cat", "under the jib"), and the lugger and the boats brought up are
   told to "brail up the spanker". Only the two yard phrases of that road are A2's, and they are
   mended.
5. **Two new tests near the slow tier's line.** Under the measures' load,
   `test_the_lugger_brought_up_squares_no_yards` and `test_a_ship_with_after_yards_says_them_as_before`
   took 5 to 8 s (the conftest's line is 5 s); `tests/conftest.py`'s slow list is not in my row, so
   neither is marked slow. Measured alone on the quiet box: 6.05 s (of it about 4 s the Channel's chart,
   loaded once a process: 2.2 s with it loaded) and 5.47 s. Left in the fast tier rather than
   trimmed and the tier run a third time; if the lead wants them in `SLOW_TESTS`, that is
   `tests/conftest.py`'s line.

Stopped after A2, as briefed: waiting for the coordinating session's message before A1a.

## Steps A1a and A1b: the whole lateen's side, its routing and its going about with the yard's change (2026-11-20)

**Merged first:** `origin/…/pkg-90` at **00382c4** (A2's merge), into this branch by
fast-forward, before A1a; nothing merged since. Every comparison here is against a worktree of
00382c4.

**Commits** on `…/pkg-90-engine`, three, one merge (plan §6, §9.1: "A1a-A1b"):
- **ea1045e** A1a: the side, the shift by itself (`change_lateen`), its routing, the stern and
  bow watches, the heave-to refused;
- **4e6df32** A1b: `LateenChange` woven into the going about, the clause, the practice and its
  reading, the primer, and truth 7-606's list written again for A1a's script;
- **1b0f12c** A1b, a mend found before the tiers: the practice given in a standing order.

**Files** (each in the engine track's §7.1 row, or named by the card or the coordinating
session):
- `freesail/evolutions/scripts.py`, `runner.py`; `freesail/orders/verbs.py`, `grammar.py`,
  `vocabulary.py`, `navigation.py`; `freesail/api/readings.py` (the practice's row);
- `data/evolutions/change_lateen.yaml` (new), `set_lateen.yaml`, `tack.yaml`, `wear.yaml`
  (their last lines' `{lateens_said}`; no timing moved); `data/vocabulary.yaml`;
- `docs/primer/05-going-about.md` (the new section, and A2's line at :357, "Up helm.", from a
  run); `docs/dev/TuningNotes.md` ("Package 90, A1a", "Package 90, A1b");
- `freesail/core/checkpoint_names.py`, **written by its tool** (`python tools/checkpoint_names.py
  --write --jobs 4`, the brief's checkpoint rule), the diff one name (below);
- `tests/test_lateen_whole.py` (new), `tests/test_agents.py` (A1a's count).

No ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). LF; ruff
check and format clean; no line over 100. Nothing under `docs/agents/consent/`. Chapter 7's lines
(:339, :349) untouched. No truth added: none of 7-670 to 7-679 is used (every behaviour is pinned
in `tests/test_lateen_whole.py`, at the door it is met at, on the probes, since no committed file
carries a whole lateen).

### What was built

TuningNotes has each piece with its reason and its words; in short:
- **A1a.** The side found once at the set (`set_lateen`'s nought-second step) and kept brailed
  and furled; the lug's two-thirds on the bad hand; `shift`, `change` and `dip` of a whole lateen
  routed to `change_lateen` (peaked, the car abaft, 14.6 s a metre by itself, one able hand for
  2½ m and at least four, all hands), "for" keeping the sail room's; the whole lateens held by
  every manoeuvre that holds a settee; the stern watch and the new bow watch (a lugger's lugs at
  the same cause); the heave-to refused in the xebec's words.
- **A1b.** `LateenChange`, a plain class, built only when a lateen is to be shifted: 8.7 s a
  metre (read from `change_lateen.yaml`'s own `timing`, the tack's and the wear's untouched),
  together where her hands serve every party, else one after another, the main first. Woven in at
  the holds, the tack (through the wind), the wear (wind aft), the fill away, the hove-to watch's
  forced round, the box-haul, the wear short round and box her off; she is tacked or worn when it
  is done; the mizen hauled and eased; a lateen rig's tack waits to pay off. Which yards: the
  clause (`tack ship and leave the mizen`), else the practice (`leave the lateens in stays` and
  its kin, a new verb `leave` and the occasion), answered and read (`the lateen practice`); the
  plan read again as the change begins.

### The probes, old beside new

The three probes of `tests/rig_fixtures.py` with `dipping` on each whole lateen (`a1/goabout.py`
in the session's scratch: seed 7, 15 kn steady from the north, the starboard tack 67.5° off, plain
sail trimmed, settled 1,800 s, then the order and 900 s; "lost" is the ground she would have made
to windward in 900 s at her settled rate, less what she made). Base 00382c4; A1a the yards left
(A1a's commit, ea1045e); A1b the yards changed by the default practice, at the probes' own yards.

| Probe | Tack: base -> A1a -> A1b | Wear: base -> A1a -> A1b | After, kn |
|---|---|---|---|
| Tartane | 89 s, 29 m -> 157 s, 128 m -> **262 s, 193 m** | 487 s, 353 m -> 480 s, 517 m -> **480 s, 490 m** | 6.17 -> 5.83 -> 6.05 |
| Polacre | 164 s, 102 m -> 165 s, 128 m -> **292 s, 154 m** | 464 s, 455 m -> 462 s, 500 m -> **461 s, 472 m** | 4.84 -> 4.65 -> 4.76 |
| Xebec | 100 s, 51 m -> 100 s, 156 m -> **344 s, 318 m** | 255 s, 367 m -> 294 s, 459 m -> **308 s, 460 m** | 5.14 -> 4.60 -> 5.00 |

A1a's differences from the base are Eng §2.2a's "yard left" to the metre (+99, +27, +105 in
stays). A1b's (+164, +53, +266 in stays; +137, +18, +93 in the wear) are under §2.2a's at the
hulls' own seconds (+294, +69, +295; +250, +77, +122): the probes' yards are shorter (the tartane
probe's main 16.0 m), the change begins after "let go and haul" and not as her head passes the
wind, and each yard's sheet is drawn as it is set. The xebec's tack ends at the tack's own 300-s
timeout: with all three yards in their gear she pays off well past full and by (127° off at the
most) and comes back up slowly. The bare xebec (head sails furled) waits 31 s past it for her head
to pay off, the ruling's case.

**The eighteen files**: A2's harness (`a2/harness_v2.py`: each file settled 2,400 s, then her
tack, wear, heave-to and fill-away, box-haul and the rest, every event and a trace every 10 s) at
00382c4 and at A1b: **270 runs, every tick, kind, trace and line the same**.

### Moved, old beside new, with reason

1. `tests/test_agents.py::test_the_contents_says_what_each_topic_costs_measured_from_the_text_served`
   (A1a): "110 evolutions" -> "111 evolutions", `change_lateen.yaml`, the card's.
2. `freesail/core/checkpoint_names.py` (A1b's commit, for A1a's class): truth 7-606's `kin` case
   failed, `('freesail.evolutions.scripts', 'ChangeLateenScript')` lacking. Every script class is
   kin to the scripts the list admits, and A1a's `change_lateen` has its own. The list written
   again by its tool (`python tools/checkpoint_names.py --write --jobs 4`, 11 min), **the diff
   that one name**, as the brief's checkpoint rule asks. **A1a's commit alone (ea1045e) fails
   truth 7-606**; the merge, one, carries both. The plan held 7-606 unmoved by construction at
   A1b: true of `LateenChange` (no name, built only when needed), not of A1a's script.
3. `tests/test_lateen_whole.py`, A1a's own: four tests put the yards on the bad hand with a plain
   `tack ship`, which did nothing to them before A1b; given `tack ship and leave the lateens`
   (the first renamed for it). Same merge, same file.
4. `docs/primer/05-going-about.md:357`: "Stand by to wear ship. Up helm; brace in the after
   yards." -> "... Up helm." (A2's, from a run: the topsail schooner worn under plain sail, seed 7,
   12 kn, at 00382c4 and at A1b alike). The next line, "Wind aft. Squared the head yards; hauled
   out and braced up.", runs today as "... shifted over the sheets; hauled out and braced up." at
   the base too (B3.4b's words, before A2): not in my brief, so not edited.

No other pin moves (the tiers below).

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is 00382c4**, a worktree of the merged hash.

| Run | Base (00382c4) | A1a-A1b (1b0f12c) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,509: 8,500 passed, 8 skipped, 1 xfailed, 0 failed (1 h 45 min, the box loaded by the measures) | 8,572: 8,563 passed, 8 skipped, 1 xfailed, 0 failed (1 h 15 min). **Test by test: every one of the base's 8,509 the same outcome; 63 new, all `tests/test_lateen_whole.py`, passed** |
| **The touched files' slow cases**, `--slow -m slow` (`tests/test_agents.py`, `tests/test_lateen_whole.py`, which has none) | | 15 passed |
| **The guard files whole with their slow cases**, `--slow`: `test_settee`, `test_catalogue`, `test_held_work`, `test_agents`, `test_readings`, `test_lateen`, `test_lug`, `test_evolutions`, `test_orders`, `test_grammar_book`, `test_staying`, `test_lying_to`, truths 7-606 and 7b-111 | | on the tree before the list and the mend: 1,313 passed, 2 xfailed, **1 failed, truth 7-606's `kin`** (A1a's script, above); then truth 7-606 whole and `test_lateen_whole` after the list: 127 passed. The mend after touches the practice's words alone |

**The guard set of §10.2 at A1a-A1b**, tallied from the two fast tiers' junits, base beside new,
every case the same outcome: the byte test and the golden classing table
(`tests/test_ship_particulars.py`, `tests/test_rig_classing.py`, truth 7-185) 96 passed;
`tests/test_schooner_mast.py` 74; `tests/test_probes_90.py` 88; `tests/test_check_viewer_guns.py` 21;
the lugger's set (`tests/test_lug.py`, truth 7b-111, `tests/test_captains.py`'s and
`tests/test_view_geometry.py`'s lug cases) 58; the settee's, `tests/test_settee.py`, 75; the
going-about set (`test_gale`, `test_rig_geometry`, `test_staying`, `test_lying_to`,
`test_evolutions`, `test_captain_trials`, `test_catalogue`) 261; A1b's own, `test_grammar_book` and
truth 7-606, 74; all passed at both. **The settee's and the lugger's guard sets held unmoved**, and
`tests/test_catalogue.py` with them. The probes' going about re-measured above; the eighteen files'
by the harness, every run the same.

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`. **The checkpoint's list:** written by its tool, one name (above).

### Unsure, and for the lead

1. **The rate by itself** (`change_lateen`, `shift the mainsail` with no manoeuvre): 14.6 s a
   metre, the lugger's `dip_lug` by itself, the lean put to the lead and **not ruled**; now in
   `change_lateen.yaml`'s `timing` beside the ruled 8.7 in a manoeuvre ("the change's own file",
   Eng §2.3 item 4, read literally: `tests/test_catalogue.py` pins milestone 2's timings alone).
2. **`hands: all` with no party named** on `change_lateen`, the party and its numbers term the
   script's: the numbered party with `too_few`, a named party, or `requires`, each moved a guard
   pin (TuningNotes, A1a). The lateen's own evolutions are not given `too_few` for the same
   reason.
3. **A checkpoint while a `LateenChange` is in hand is refused** on loading
   (`CheckpointRefused`), as one while a `SetteeChange` is in hand always was: neither is
   admitted. By the plan's construction (no name added at A1b). A lateen hull's first scenario
   would need it admitted.
4. **"The lateens" by itself** (`shift the lateens` with no occasion) rests on the hull's file
   naming the group (Eng §2.3 item 3a); the probes have none, and answer "There is no such part as
   the lateens". The practice and the clause read "the lateens" whatever the file.
5. **The practice is the lateens' together**: one per occasion, as the plan's dict has it; a
   practice for one yard is refused in words, and one going about names one by the clause.
6. **The readings row is in every station's readings**, "no whole lateen aboard" on any other
   hull (the row's words for its None). Its one phrase, "the lateen practice", was chosen because
   "the practice of the lateens" became the cutter's nearest hint for "and leave the lateens" in
   place of "the lanterns".
7. **The new verb `leave` is every hull's**: a line beginning "leave" other than "leave the
   pumps" was "not an order this ship understands" and is now answered by the verb ("She carries
   no whole lateen; ..." or "no such part"). The clause and the occasion are read on a lateen hull
   alone.
8. **The words** (JUDGEMENT): the change's ("Shift ...: ease the parrel(s), cast off the runners,
   peak up the yard(s) and pass the car(s) round.", "Shifted the mizen; it stands to leeward of
   the mast."), the plan's ("the lateens to be shifted in stays", "... left on their masts"), the
   end's (", the mizen on the mast", ", but she has not paid off: ..."), the practice's ("Her
   practice: ...") and the refusals'. `LATEEN_PAID_OFF_DEG` (10°) is JUDGEMENT.
9. **Found and mended before the tiers**: a standing order of the practice was refused as the
   book read it whole (`orders.read_whole` seeks the object as a part); "the lateens" is now a
   mark, the object empty (third commit, 1b0f12c).

Stopped after A1a and A1b, as briefed: waiting for the coordinating session's message.

## Step A1c: the rules captain and `put her about` with a whole lateen (2026-11-20)

**Merged first:** `origin/…/pkg-90` at **033f42b7** (A3 merged, and stage 0's guards as one
table), into this branch by a merge commit, **686557d**, its message reworded before it was
pushed so that it names no branch. The one conflict, `docs/dev/TuningNotes.md`, both appending
at its end: kept both whole, the package branch's stage-0 section first and A1a's and A1b's after
it. Every comparison here is against a worktree of 686557d.

**Commit:** **0c98ff8** on `…/pkg-90-engine` (parent 686557d), one commit, merged alone.

**Files** (each in the engine track's §7.1 row for A1c):
- `freesail/orders/navigation.py`: `LATEEN_TACK_KN` and its words beside `WEAR_WIND_KN`; the
  readings' mean true wind as one reader (`mean_true_wind_kn`, `lateen_strong_wind_kn`);
  `put_about_choice`'s reason; `judge_course`'s eye branch;
- `freesail/orders/verbs.py`: the ordered tack's warning (`_warn_lateen_in_stays`);
- `freesail/world/captains.py`: `LATEEN_LEAVE_KN`, `BAD_HAND_S`; `Captain._lateen_work` in
  `_work`; `_across_the_stern`'s lateens and the bow's event (`_across_the_bow`,
  `_shift_lateens_left`). Not near A3's lines in `Captain._repairs`, nor package 121's l. 1080;
- `freesail/evolutions/scripts.py`: `lateens_on_their_masts`, read by the going about's last line
  as before and by the captain;
- `tests/test_lateen_whole.py`: A1c's part; `docs/dev/TuningNotes.md`: "Package 90, A1c".

No ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). No class
added, so truth 7-606 and the checkpoint's list are not touched (truth 7-606 in the fast tier
below). LF; ruff check and format clean; no Python line over 100. Nothing under
`docs/agents/consent/`. No book written: neither key is in any file of `data/captains/` (a test
says so of each). No truth added: none of 7-670 to 7-679 used.

### What was built

TuningNotes has each piece with its words; in short:
- **`put her about`** wears a vessel with a whole lateen set over 22 kn (the readings' mean true
  wind, as the gale's 30 kn is read), for every voice: "Put about: wearing, the wind 25 knots: a
  lateen is not put in stays in a strong wind." The tack regardless with the land to leeward, or
  no room to wear, stands before it.
- **The course's judgement** (`steer`, `shape a course`, the captains' hourly leg) wears her for a
  course across the wind's eye in the same wind and words, and tacks her regardless where there
  is no room to wear, saying so.
- **An ordered `tack ship`** there is obeyed, warned once in words (a note, `ship.tack_warned`:
  "The wind 25 knots: a lateen is not put in stays in a strong wind; she is put in stays as
  ordered."), never turned into a wear.
- **The rules captain**: the practice in stays by the wind at 12 kn, once at each crossing; a
  yard left on the bad hand shifted as the wind rises over 12 kn or after a board of 1,800 s;
  each lateen the stern's or the bow's line names shifted, as a lug is dipped. Nothing on a hull
  with no whole lateen, and nothing kept in his business there.

### Measured

- The xebec probe in 25 kn (seed 7, the starboard tack 67.5° off, plain sail trimmed, settled
  900 s): `put her about` wears her, the reason said; `tack ship` tacks her, warned; `steer 45`
  wears her for the larboard tack, full and by. In 18 kn all three tack her as before.
- The tartane probe under the rules captain (seed 7, 14 kn and 9 kn from 260°, her head 90°, a
  passage to the eastward): his first course carries the wind across her stern, the deck says the
  mainsail lies on the mast, and his next order is "shifting the mainsail (the wind across the
  stern)"; in 9 kn his first judgement leaves the lateens in stays.
- **The eighteen files**: A2's harness at 686557d and at 0c98ff8: **270 runs, every tick, kind, trace and line the same** (the two files byte for byte).

### Moved, old beside new, with reason

Nothing moves (the tiers below).

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is 686557d**, a worktree of the merge.

| Run | Base (686557d) | A1c (0c98ff8) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,608: 8,599 passed, 8 skipped, 1 xfailed, 0 failed (1 h 29 min, the box loaded by the measures) | 8,627: 8,618 passed, 8 skipped, 1 xfailed, 0 failed (1 h 15 min). **Test by test: every one of the base's 8,608 the same outcome; 19 new, all `tests/test_lateen_whole.py`, passed** |
| **The lens with its slow cases**, `--slow`: `test_captains`, `test_captain_trials`, `test_captain_rules`, `test_subtypes`, `test_held_hulls`, `test_rig_words`, `test_ships`, `test_signals`, `test_settee`, `test_lug`, `test_orders`, `test_brains` | | 1,029 passed (16 min), on the tree as committed |
| **The touched files' slow cases**, `--slow -m slow` (`test_lateen_whole`, which has none, `test_captains`, `test_captain_trials`, `test_captain_rules`) | | 5 passed |

**The guard set of §10.2**, tallied from the two fast tiers' junits, base beside new, every case
the same outcome: the byte test and the golden classing table (`tests/test_ship_particulars.py`,
`tests/test_rig_classing.py`, truth 7-185) 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89 (stage 0's table, from the merge); `tests/test_check_viewer_guns.py`
21; the lugger's set 58; the settee's 75; the going-about set 261; `test_grammar_book` and truth
7-606 74; all passed at both. `tests/test_subtypes.py`'s pairs of books pass (no key written).

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`.

### Unsure, and for the lead

1. **The bow's lugs.** A1a's bow line names the lugger's dipping lugs too; the captain's answer
   to it is built for whole lateens alone. Dipping the lugger's lugs on it would move her
   captained runs, which no row of the card names. The deck says them, as before.
2. **The warning's place and words** (JUDGEMENT): a note of the ship's, after the tack's first
   line, kind `ship.tack_warned`; not given for a tack of the course's judgement, whose own words
   say why, nor for `put her about`'s tack regardless, whose note says why too (that tack is
   warned: it goes by `tack ship`).
3. **The captain's figures** (JUDGEMENT, ruled as defaults): his practice set at the first
   judgement where the practice differs from the wind's (a crossing from no reading), then once
   at each crossing; the board's timer runs while a yard is on the bad hand with no manoeuvre in
   hand, and starts again after any; his why's words ("the wind under 12 knots", "30 minutes on
   the bad hand", "the wind round ahead through the bow").
4. **Hove to for weather** the captain still sets the practice by the wind, but gives no shift
   while a manoeuvre ("hove to") is in hand: the hove-to watch's forced round (A1b) shifts them.

Stopped after A1c, as briefed: waiting for the coordinating session's message.

## Step A1d: a whole lateen aback, and on the bad hand, in a breeze (2026-11-20)

**Merged first:** nothing new. The package branch's A2 mended hash had not landed when A1d was
built (the coordinating session's word: merge it when it is said to have landed); the branch
stands on 686557d (the package branch at 033f42b7) and A1c. The base of every comparison here is
A1c, **0c98ff8** (a worktree; `be2c90f` above it adds the report alone).

**Commit:** **8dce637** on `…/pkg-90-engine` (parent be2c90f), one commit, merged alone.

**Files** (each in the engine track's §7.1 row for A1d, or A1b's places):
- `freesail/physics/sails.py`: `LATEEN_ABACK_LOAD`, `LATEEN_BAD_HAND_LOAD` beside
  `LUG_AGAINST_MAST_AREA`; `_carried_over_abaft_the_beam` in `_read_rig`; `lateen_load_factor` in
  `_apply_loads`, on the spars alone;
- `freesail/evolutions/trim.py`: `keeps_its_side`; `read_sheet`'s cloth on its yard's side;
  `set_sheet_angle` keeping a whole lateen's drawn side, the lee included;
- `freesail/evolutions/scripts.py` (A1b's places): the draw at "let go and haul"
  (`TackScript._draw_lateens_over`), the hang's eased mizen, the wear's "wind aft"
  (`WearScript._lateens_over`), `ease_off_sheets`' side, the take-in's test
  (`lateen_aback`, `lateen_take_in_waits`) and their words;
- `freesail/evolutions/runner.py`: the take-in's wait, at the start and in `_start_waiting`;
- `freesail/orders/navigation.py`: the bow watch's words for a lateen held aback;
- `tests/test_lateen_whole.py`: A1d's part, and A1a's bow line moved;
  `tests/test_known_truths.py`: truths 7-670, 7-671 and 7-672;
- `docs/dev/TuningNotes.md`: "Package 90, A1d".

No ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). No class added
(functions and constants only), so truth 7-606 and the checkpoint's list are not touched.
`physics/strain.py` is not touched. LF; ruff check and format clean; no Python line over 100.
Nothing under `docs/agents/consent/`.

### What was built

TuningNotes has each piece with its words. **The rule**: a whole lateen's cloth lies on its
yard's side, kept by its mast, and its sheet keeps the side it is drawn to; the wind come round
ahead onto that side holds it aback against its mast (the plate `_plate_force` makes, unchanged);
in the luffing band it shakes as before; with the wind abaft the beam on it the cloth goes over to
leeward, the bad hand. **The strain**: its pull on its yard and its mast (and any spar beneath)
times 2.5 held aback and 2.5 on the bad hand, its cloth and lines the plain pull; the strain model
as it is. **The evolution's part**: every lateen drawn over to the new lee at "let go and haul"
and at "wind aft", those left said; the aftermost eased in stays and in the wear as A1b eases it;
the bow's line "aback against the mast"; a take-in of a lateen aback over 22 kn waits till it
fills or is drawn over.

### Measured

- **The bands** (truths 7-670 to 7-672; the probes' lateen yards and masts rated by the
  generator's rule, the design's figures to the decimal): taken aback by a shift, the tartane's
  great yard 0.94 of its rating in 28 kn, 1.26 in 31, 1.46 in 34, 1.71 in 37, so it **strains from
  about 29 kn and may carry away from about 34½** (the polacre's fore yard 30 and 36½); her main
  mast, carrying more, from about 40. On the bad hand the polacre's fore yard 0.95 in 42 kn, 1.37
  in 46, 1.59 in 50: **from about 42½ and 48½**. The rules captain's board on the bad hand in 12
  kn for 1,800 s: the yards at 0.08 to 0.12 of their ratings, **under a fifth**, no condition lost.
  The lead's figures (28 and 35; 40 and 49) stand.
- **The probes' going about** in 15 and 25 kn, old (A1c) beside new: **−34 to +18 m**. The tack
  and the wear with the yards changed (A1b's figures) within 2 per cent but for the polacre's
  25-kn tack, +17.5 m, 5 per cent: her fore lateen stands aback 28 s across the main yard's swing,
  paying her head off, as the design means it to. With the lateens left the wear loses 5 to 20 m
  the less (its left lateens now drawn for the wind she comes to at "wind aft") and the polacre's
  25-kn tack 34 m the less (the design's own case, 76 m). The table is TuningNotes'. No "taken
  aback" line is said in any run.
- **The eighteen files**: A2's harness at 0c98ff8 and at 8dce637: **270 runs, every tick, kind,
  trace and line the same** (the two files byte for byte).

### Moved, old beside new, with reason

1. `tests/test_lateen_whole.py::test_the_bow_watch_says_a_lateen_left_on_its_mast_by_a_shift_of_wind_through_the_bow`
   (A1a's own): "... the foresail and the mizen and the mainsail lie on their masts; shift them
   when you will." -> "... are aback against their masts; shift them when you will.", the
   design's words (§2.4.3a) for the lateens A1d holds aback there.

`tests/test_strain.py`, `tests/test_lateen.py` and `tests/test_settee.py` as they are.

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is A1c, 0c98ff8** (its fast tier's junit, run
for A1c's report on the same code as `be2c90f`).

| Run | Base (0c98ff8) | A1d (8dce637) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,627: 8,618 passed, 8 skipped, 1 xfailed, 0 failed (1 h 15 min) | 8,638: 8,629 passed, 8 skipped, 1 xfailed, 0 failed (1 h 16 min). **Test by test: every one of the base's 8,627 the same outcome; 11 new, all passed** (eight of `tests/test_lateen_whole.py`, truths 7-670 to 7-672) |
| **Slow tier whole**, `--slow -m "slow and not pace"` (a new rule of force in `physics/sails.py`, so the tier whole and not the touched files' alone) | | 568: 557 passed, 11 xfailed, 0 failed (1 h 26 min). The same 568 cases as A2's slow tier (`a2`'s run on its own tree) and the same eleven xfailed; A2's five failures there (its four digests, moved since, and the browser's flake) pass |
| **The guard and physics files with their slow cases**, `--slow`: `test_strain`, `test_lateen`, `test_settee`, `test_lug`, `test_sails`, `test_trim_order`, `test_evolutions`, `test_staying`, `test_lying_to`, `test_gale`, `test_rig_geometry`, `test_catalogue`, `test_captains`, `test_captain_trials`, `test_rig_words`, `test_held_work`, truth 7b-111 | | 590 passed, 1 xfailed (16 min), on the tree as committed |

**The guard set of §10.2**, tallied from the two fast tiers' junits, base beside new, every case
the same outcome: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py`
74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed at both.
`tests/test_strain.py`, `tests/test_lateen.py` and `tests/test_settee.py` as they are.

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`.

### Unsure, and for the lead

1. **The change in stays begins where A1b put it**, at the head yards' swing's end, "changed
   last, as the settee"; the design's §2.4.3a has it begin at "let go and haul". So that no lateen
   stands aback through the swing, every lateen still set is drawn over at "let go and haul" and
   the one to be changed fills on the bad hand until its change begins. On the probes the swing
   is short or none; on a hull with long head yards it is the swing's seconds on the bad hand.
2. **The aftermost lateen in the wear** is eased at "up helm" and hauled aft only as she comes to
   steady (A1b); at "wind aft" A1d takes it over to the new lee still eased. Drawn there at once,
   as the first draft did, the wear with the lateens left lost 53 to 132 m less than A1c: a change
   of A1b's act, not the rule's, so not built.
3. **The tartane probe on the bad hand from 34 kn**, and in a 12-kn wind's top gust of 15.6 kn,
   luffs and is taken aback by her own lateens, so her figures there are aback's; the bad hand's
   band is the polacre's. Her own file measures her (Tar-D T-9).
4. **The take-in's wait** is the runner's (no step of an evolution file can wait, and
   `registry.py` is not in my row): a take-in of a whole lateen held aback over 22 kn waits at its
   start and when its turn comes; its words are said once, at the order.
5. **Truths 7-670 to 7-672** take about 3 s each (the probes tick at about a millisecond), so they
   stand in the fast tier.

Stopped after A1d, as briefed: waiting for the coordinating session's message.

## Step A4: the boat in tow, stopped by the stop rule (2026-11-21)

**Stopped before building; nothing committed for it.** The branch stands at e2d6b92, A1d's report.
A4 needs three files that my §7.1 row and the card do not name for it, so by the brief's stop rule
it stops here, and none of them is edited.

**What A4 needs, and why** (read: every road by which a boat leaves and comes back to her ship):
1. **`freesail/world/boats.py`**, which my row names for A7 alone ("only so that the boat
   predicates stay a boat's"). The boat manned as a hull is hoisted out here and nowhere else:
   `man_boat` ("hoisted out and manned: her coxswain and N oarsmen in her, lying off the lee
   quarter", placed off the lee quarter, refused under way by `way_on_her`, "heave to or come to
   an anchor before the boat is hoisted out"), `tow_with_boat` ("hoisted out and manned for the
   tow"), and `hoist_in` and `come_alongside` ("alongside and hoisted in"). A towed boat is
   hauled up alongside from astern and manned, and veered astern again after, so each of these
   wants the boat's `towed` read: its words, its place (astern on her painter, not off the lee
   quarter), and whether the way rule, which guards a hoisting out, applies (JUDGEMENT: hauled
   alongside she can be manned with a little way on).
2. **`freesail/world/dealings.py`**, not named in my row. The boat's state on an errand says
   "hoisting out" (`phase="hoisting out"`, l. 2760) and the errand's schedule counts the hoisting
   out and in (`BOAT_HOIST_OUT_S`, `BOAT_HOIST_IN_S`, l. 2785-2786 and 3383-3384, the boat's
   other roads to the quay and to another ship); its words are the errand's (`boat_phase`).
3. **`freesail/world/ports.py`**, not named. The two times themselves (`BOAT_HOIST_OUT_S`,
   `BOAT_HOIST_IN_S`, 300 s each, l. 308-309).

In my row, and ready to take the same reading once the three are given: the errands' scripts
(`evolutions/scripts.py`: `SendBoatScript`'s and `LayOutKedgeScript`'s "hoist_out" and "hoist_in"
phases, 300 s each, and `send_boat.yaml`'s "Away {boat}'s crew! Hoist out {boat}." and "{boat_cap}
hoisted in."), and the clearing for action's "boats hoisted out to tow astern"
(`evolutions/action_scripts.py`, l. 103-134). Built in those alone, `send the boat ashore` would
say "hauled alongside" while `man the boat` still said "hoisted out" of a boat already in the
water: a mend at two places of one cause, not at the cause.

**Measured, for the drag** (A4's JUDGEMENT "left out as small beside the hull's, measured against
the trawl's form"), run in scratch with nothing changed: the engine's own resistance
(`physics/hull.resistance`, the form the trawl's drag rides beside in `integrate.step`) of the
16-ft yawl (`data/ships/boat-yawl-16.yaml`, the nearest committed boat to the tartane's 4.5 m)
beside the tartane probe's hull, upright:

| Her way | The yawl | The tartane probe | The boat's share | The trawl, for scale (`TRAWL_DRAG` u²) |
|---|---|---|---|---|
| 2 kn | 33 N | 561 N | 6 per cent | 1,270 N |
| 4 kn | 168 N | 2,308 N | 7 per cent | 5,081 N |
| 6 kn | 734 N | 5,836 N | 13 per cent | 11,433 N |
| 8 kn | 3,009 N | 13,453 N | 22 per cent | 20,325 N |

So the boat's drag is small at a towing pace and in light airs, but at the tartane's sailing
speeds (6 to 8 kn, the A1b probe's 6 kn close-hauled and 8.5 kn in 25 kn) it is an eighth to a
fifth of her hull's by the engine's form, well past the boat's own hull speed. **For the lead**:
whether it is left out, as the plan has it, or carried as a drag like the trawl's (veered long in
a blow, or hoisted in, by the tartane's design §11), the figure being the boat's resistance at her
speed. JUDGEMENT either way; the boat towed in the wake of a ship rides lighter than the bare form.

**Pins:** none moved; nothing built. **Stage 0's table** (`KEY_CARRIERS["towed"]`) stays empty: no
committed file tows a boat.

Going on to A5 and A6 meanwhile, as briefed; they touch none of these files.

## Steps A5 and A6: a yard's level from its order on its mast, and the pole mast's quick handing (2026-11-21)

**Merged first:** nothing new (the package branch's A2 mended hash has not been said to have
landed). **The base** of every comparison is A1d, **8dce637** (`e2d6b92` and `a7f8298` above it add
reports alone).

**Commit:** **effbaed** on `…/pkg-90-engine` (parent a7f8298), one commit for the two, as the plan's
§9.1 merges them.

**Files** (each in the engine track's §7.1 row):
- `freesail/ship/graph.py`: `Ship.yard_level`, `YARD_LEVEL_SPARS`, `_find_yard_levels` and its
  memo `_YARD_LEVELS` (a weak dictionary, never pickled); `Ship.is_pole_mast`, `Ship.on_pole`;
- `freesail/evolutions/scripts.py`: the level read at `lowest_square_sails`,
  `light_sails_forward_of`, `_topsails_on`, `_is_upper_square`, `_topsails`; lie a-try's refusal
  ("close-reefed" only of a topsail with reef bands); `mast_inventory` naming the pole;
- `freesail/evolutions/trim.py`: `_level` (and through it `stagger`, `by_level`, `eased_lowest`,
  `heavy_weather_trim`);
- `freesail/orders/verbs.py`: `_take_in_kind`, `_level_rank`, `evolution_key(..., ship)`'s
  `pole`, the pole sail's refusal of "haul up";
- `freesail/physics/sails.py`: `_yard_level` (the helm's mark) and `studding_level`, by
  `yard_level`;
- `data/vocabulary.yaml`: `take in` and `furl`'s `pole`, `take_in_words`' `pole: [lower, clew up]`;
  `data/evolutions/take_in_pole.yaml`, `data/evolutions/furl_pole.yaml` (new);
- `tests/test_yard_level.py`, `tests/test_pole_mast.py` (new); `tests/test_agents.py` (the pin
  below); `docs/dev/TuningNotes.md`: "Package 90, A5 and A6".

No ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). No class added
(methods, functions, constants and a module dictionary), so truth 7-606 and the checkpoint's list
are not touched; a test shows a checkpoint the same bytes whether the levels have been read or
not. No key written into a committed file: stage 0's `KEY_CARRIERS` does not move. LF; ruff check
and format clean; no Python line over 100. Nothing under `docs/agents/consent/`.

### What was built

TuningNotes has each piece with its words. **A5**: a braced yard's level is the level of the spar
it hangs on and one more for each braced yard on the same spar below it by height; a square yard
on a lower mast with no braced yard below it and a whole lateen's yard below it counts the
lateen's (the lead's lean, ruled); read at the twelve places in place of the parent spar's class.
A pure rank by height (the plan's first wording) was measured and not built: it made three
committed files' topsails courses. **A6**: the pole, read from the parts as filed with no key: a
lower mast with a braced yard above its lowest on the mast itself and no topmast; its upper square
sails taken in by the halyards let go, lowered onto the yard below and clewed up there
(`take_in_pole`, 60 s), and furled from the yard below (`furl_pole`, the lowering and a 120-s
furl), "lower" its word and "haul up" refused in its own words; the topmast evolutions refused in
words naming the pole. **Not built, as ruled:** `reef_pole`. The two new files' served notes are
the ship's work and its sources alone (a test says so).

### Measured

- **The guard over every file's yard levels** (`tests/test_yard_level.py`), old beside new: every
  braced yard of the eighteen files at the level its spar's class gave it, but the smack's
  `topsail.yard`, 0 -> 1. Of the committed files the smack's main alone is a pole, her topsail
  alone on it (`tests/test_pole_mast.py`).
- **The smack** (seed 7, her head 292.5°, the topsail set over plain sail and settled 900 s):
  hove to in 15 kn, her topsail now laid to the mast as a fore-and-after's ("Hove to on the
  starboard tack, topsail to the mast, helm a-lee."), 50.5° off at 2.87 kn by +900 s, where before
  it was hauled up as a course and she lay 47.3° off at 2.61 kn; in 30 kn she lies a-try under the
  topsail and the foresail, 49.3° off at 3.64 kn by +1,800 s, where before she was refused ("She has
  no topsail to lie a-try under."). Her topsail taken in 88 s from the order's start line, against
  154 s; furled 300 s against 350. The table is TuningNotes'.
- **The eighteen files**: A2's harness at 8dce637 and at effbaed, **270 runs: 267 the same in
  every tick, kind, trace and line; the smack's three move**, none of them pinned:
  1. `lie_a_try` (her plain sail, the topsail not set): the refusal's words, "She has no topsail to
     lie a-try under." -> "The topsail is not set; set it to lie a-try under it." (A5: she has a
     topsail now; the lie a-try's refusal mended at its cause for a topsail with no reef bands).
  2. `anchor` and `shoal_anchor` (come to an anchor, then get under way): getting under way now
     looses and sets her topsail before she casts, where it stayed furled; her cast's "She has
     paid off ..." 2 s earlier (3,603 s against 3,605; 3,115 against 3,117), the trace parting
     from +3,170 s in the one and +2,740 s in the other, and at the run's end, +3,900 s, she lies
     51 m and 63 m from where she lay before; in `shoal_anchor` her under-way line names the
     topsail. The cause: the cast looses and sets every topsail (`scripts._topsails`, one of the
     twelve places), and hers is one now. Each run, old beside new, is in the section for the
     lead's reader below. *Corrected (nudge 38)*: this item as first pushed (58b28ab) said "every
     line the same words", "34 to 39 m" (the two components of her end place's move in the one
     run, not its distance) and a cause in the trim's stagger; measured again, as here.

### Moved, old beside new, with reason

1. `tests/test_agents.py::test_the_contents_says_what_each_topic_costs_measured_from_the_text_served`:
   "111 evolutions" -> "113 evolutions": `take_in_pole.yaml` and `furl_pole.yaml` (the ground
   report's row 12, measured 110 -> 112 before A1a's `change_lateen`).

**The ground report's rows 13 to 16 do not move**: no `reef_pole` (13), and
`tests/test_held_work.py`'s two sweeps (14, 15) and `tests/test_in_world.py`'s catalogue case (16)
pass as they are (in the lens below and the fast tier).

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is A1d, 8dce637** (its two tiers' junits, run
for A1d's report).

| Run | Base (8dce637) | A5-A6 (effbaed) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,638: 8,629 passed, 8 skipped, 1 xfailed, 0 failed (1 h 16 min) | 8,689: 8,680 passed, 8 skipped, 1 xfailed, 0 failed (1 h 27 min). **Test by test: every one of the base's 8,638 the same outcome; 51 new, all passed** (27 of `tests/test_pole_mast.py`, 24 of `tests/test_yard_level.py`); the moved pin's case passed at both |
| **Slow tier whole**, `--slow -m "slow and not pace"` (a level read in `physics/sails.py` and the trim's, so the tier whole) | 568: 557 passed, 11 xfailed, 0 failed (1 h 26 min) | 568: 557 passed, 11 xfailed, 0 failed (1 h 25 min). **Test by test: every one of the base's 568 the same outcome**, none new |
| **The lens with its slow cases**, `--slow`, `-n 3`: `test_yard_level`, `test_pole_mast`, `test_lateen_whole`, `test_settee`, `test_lug`, `test_evolutions`, `test_staying`, `test_lying_to`, `test_gale`, `test_rig_geometry`, `test_catalogue`, `test_captain_trials`, `test_held_work`, `test_agents`, `test_in_world`, `test_rig_classing`, `test_schooner_mast`, `test_fishing`, `test_sails`, `test_trim_order`, `test_orders`, truth 7b-111 | | 1,703 passed, 2 xfailed (11 min), on the tree as committed |

**The guard set of §10.2**, tallied from the two fast tiers' junits, base beside new, every case
the same outcome: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py`
74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74;
`tests/test_lateen_whole.py` 90; all passed at both.

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`.

### For the lead's reader at the gate (nudge 38)

**1. What "only the smack moves: her topsail becomes level 1, on a pole" changes in play.** Her
topsail's yard crosses her main's own head, the main's lowest braced yard there, so the engine
read it as a course; it is now a topsail, on a pole main. Her plain sail sets no topsail, so a
player who never sets it meets the change in three places: `get under way` looses and sets her
topsail with the mainsail and the jib before she casts, and she stands out under it ("Under way on
the starboard tack, under the topsail and the mainsail and the jib; ...", where it was "under the
mainsail and the jib"); `lie a-try` with it furled is refused in other words ("The topsail is not
set; set it to lie a-try under it.", where it was "She has no topsail to lie a-try under."); and
`strike the topmasts` (and `send down the topgallant masts`, `fid the topmast`) names her main a
pole ("... her masts are the main mast (a pole, the mast and topmast in one stick)."). With it set
(`set the topsail`), measured from one settled world, each order from a copy of it (seed 7, 15 kn
from 0°, her head 292.5° at 5 kn, plain sail and then the topsail set, trimmed every two minutes
after five, 1,320 s, as `tests/test_pole_mast.py`'s `_smack`; `a5/play.py` in the session's
scratch, at 8dce637 and at effbaed), times from the order:

| Order | Before (A1d) | Now (A5 and A6) |
|---|---|---|
| `heave to` | "Hauled up the courses."; "Hove to on the starboard tack, under her fore-and-aft canvas, foresail sheet to windward, helm a-lee." at +214 s; at +600 s 47.3° off at 2.61 kn, the topsail hanging in the gear | no course hauled up; "...; braced the topsail aback; helm a-lee."; "Hove to on the starboard tack, topsail to the mast, helm a-lee." at +202 s; at +600 s 50.5° off at 2.87 kn, the topsail set and to the mast |
| `lie a-try` | refused: "Could not bring her to: She has no topsail to lie a-try under." | "All hands! Shorten sail and bring her to under the topsail."; the jib taken in; "Lying a-try under the topsail and the foresail, helm a-lee." at +348 s; at +600 s 43.3° off at 1.06 kn. In 30 kn: lying a-try at +808 s, 49.3° off at 3.64 kn by +1,800 s, where it was refused at +386 s |
| `back and fill` | "Hauled up the topsail."; "Backed the square sail; her way checked." and "Filled the square sail; she forereaches." at +50, +223, +401 and +574 s; at +600 s her head 297.3° at 4.14 kn | the topsail kept: "Backed the topsail; her way checked." and "Filled the topsail; she forereaches." at +50, +224, +400 and +573 s; at +600 s her head 229.0° at 3.27 kn |
| `take in the topsail`, `clew up the topsail` | "Hands to the topsail clewlines and buntlines."; "Clewed up the topsail." at +138 s; "Took in the topsail; hanging in the gear." at +204 s: **154 s** from the start line at +50 s (her watch at the sheets first) | "Let go the topsail halyards; hands to the clewlines and buntlines."; "Lowered the topsail down onto the yard below and clewed it up there." and "Took in the topsail; lowered on the yard below, hanging in the gear." at +138 s: **88 s** |
| `lower the topsail` | refused: "A course is hauled up, not lowered; say 'haul up the topsail' or 'take in the topsail'." | obeyed, as take in |
| `haul up the topsail` | obeyed, as take in | refused: "A topsail or light sail on a pole mast is lowered, not hauled up; say 'lower the topsail' or 'take in the topsail'." |
| `furl the topsail` | "Lay aloft and furl the topsail."; "Clewed up the topsail." at +150 s; "Furled the topsail." at +400 s: **350 s** from the start line | "Lay out on the yard below and furl the topsail."; "Lowered the topsail down onto the yard below and clewed it up there." at +150 s; "Furled the topsail on the yard below." at +350 s: **300 s** |
| `take in all sail` | the topsail's lines and time as take in; the jib, last, hauled down at +412 s | the topsail's as take in now; the jib at +350 s |
| `get under way` (in Carrick Road, 12 kn from 225°, the topsail furled by `come to an anchor`) | the topsail furled through it | the topsail loosed and set with the mainsail; "She has paid off ..." 2 s sooner; at +1,500 s her head 136.2° at 3.78 kn against 125.3° at 4.19 kn |

The same line for line and tick for tick: `tack ship`, `wear ship`, `box haul`, `scud`, `shorten
sail`, `set the topsail`, `trim sails`, `square the yards`, `brace sharp up on the larboard tack`,
and `come to an anchor` with the topsail set.

**2. The three harness runs that move.** A2's harness (`a2/harness_v2.py` in the session's
scratch): each start settled once and each run from a copy of it (the checkpoint's own pickling),
every event and a trace every 10 s; A1d (8dce637) beside A5 and A6 (effbaed).

| Run | Seed and start | What moves | What parts, old beside new |
|---|---|---|---|
| `lie_a_try` | seed 7; at sea, 15 kn from 0°, her head 292.5° at 5 kn, plain sail braced sharp up on the starboard tack and trimmed every two minutes after five, 2,400 s; then `lie a-try`, 600 s | **a word** | the refusal alone: "Order not carried out ('lie a-try'): She has no topsail to lie a-try under." -> "Order not carried out ('lie a-try'): The topsail is not set; set it to lie a-try under it."; every tick and trace row the same |
| `anchor` | seed 7; Carrick Road (50.160° N, 5.034° W), 10:00 on 10 June 1805, 12 kn from 225°, her head 335° at 3 kn, plain sail set, 240 s; then `come to an anchor`, 2,400 s, and `get under way`, 1,500 s | **how she sails**, and the ticks with it | the same to +3,165 s, where getting under way looses her topsail (furled throughout before; set at +3,444 s); the trace parts from +3,170 s; "She has paid off; right the helm, draw the jib, haul aft the main sheet, brace round the topsail yard." at +3,603 s against +3,605; the helm's "Steady, full and by, the wind 68° on the starboard bow." at +3,706 s against "... 73° ..." at +3,815; the lookout's sighting of the pilot's cutter and his glass on her at +3,780 s against +3,720, the same words; his "made out" line on her, at +3,900 s before, past the run's end now. At +3,900 s her head 136.2° at 3.78 kn against 125.3° at 4.19 kn, 51 m apart (53 m at the most) |
| `shoal_anchor` | seed 7; off Falmouth in three fathoms and a half (50.152° N, 5.040° W), the same hour, 8 kn from 225°, her head 335° at 2 kn, plain sail and `set the lug`, 60 s; then `come to an anchor`, 2,400 s, and `get under way`, 1,500 s | **a word, the ticks and how she sails** | the same to +2,740 s, where her topsail is loosed (set at +3,000 s) and the trace parts; "She has paid off ..." at +3,115 s against +3,117; the helm's "... the wind 69° ..." at +3,212 s against "... 71° ..." at +3,527; "Under way on the starboard tack, under the topsail and the mainsail and the jib; the best bower catted and fished; full and by." at +3,437 s against "..., under the mainsail and the jib; ..." at +3,434; the pilot's cutter, which closes a ship in her cruising ground (`world/ships.py`), read "under way on the larboard tack, with the wind on the quarter" at +3,300 s where she was "running before it" (so read at +3,600 now); "St Anthony's Head ... closing" at +3,840 s against +3,900. At +3,900 s her head 135.0° at 2.54 kn against 127.6° at 2.88 kn, 63 m apart (110 m at the most) |

The cause in the two anchor runs, measured (`a5/cast.py`): at A1d her topsail stays furled through
both casts; at A5 and A6 it is loosed at +3,165 s and +2,740 s, where the traces part.

**3. The tartane's tréou** (Tar-D §5.1a and §15 risk 5; the lead's question 5). **A new case on the
tartane probe, not her file**, which is not on this branch:
`tests/test_yard_level.py::test_the_tartanes_topsail_is_a_topsail_whether_the_treous_yard_is_crossed_or_not`
(commit **109ee87**, above A4). The probe is `rig_fixtures.tartane_probe_doc()` with her pole main
as Tar-D §4.1 files it: no topmast, the topsail yard on the main's own head at 15.6 m, the jib's
stay to the lower mast. Her great lateen's yard crosses at 10 m, and the tréou's yard (the
cutter's square sail and its gear, renamed `main.treou`) is crossed on the main or not:

| The tréou's yard | Her topsail's level | The tréou's yard's level | The courses; the topsails | The pole |
|---|---|---|---|---|
| not crossed (her plain sail, decision 9) | **1**, by the great lateen's yard below it (the ruled clause) | none crossed | none; the topsail | the main a pole; the topsail on it, taken in and furled by the pole's way |
| crossed at 8 m, below the great lateen's yard | **1**, by the braced yard below it | 0, the course | the tréou; the topsail | the same; the tréou a course |
| crossed at 13 m, above the great lateen's yard | **1** | **1** | none; the topsail and the tréou | the same, and the tréou on it as well |
| **at her file's heights** (nudge 38's second case): crossed at 8.31 m, **the same height as the great lateen's yard**, the topsail's yard at 15.78 m; filed after the lateen's yard, as her file has it, or before it | **1** | **0**, the course, in either order | the tréou; the topsail | the same; the tréou a course |

So **her topsail reads the same whether the tréou's yard is crossed or not**, at either height.

**The tie, as `Ship._find_yard_levels` reads it.** Her file (her branch's `data/ships/tartane.yaml`)
crosses the great lateen's yard and the tréou's both at the main's hounds, 8.31 m, and the topsail's
yard at 15.78 m. The clause counts a lateen yard **only strictly below** a square yard
(`lat.height_m < sp.height_m`). At the tie the great lateen's yard is not below the tréou's, so
the tréou's yard is the main's lowest braced yard with no lateen yard below it: **level 0, the
course**. Her topsail is 1 by the braced yard below it. **The order of the spars in the file
cannot change it.** The file's order breaks a tie between two braced yards on one spar alone
(`(height, order)` in the count below), and the lateen clause compares heights alone. Pinned
both ways (commit **c6018aa**, the case's rows `her-files-tie` and
`her-files-tie-the-treou-filed-first`). Measured on the probe: 0 at 8.30 m and at 8.31 m, **1 at
8.32 m**, either order, so a centimetre above the great lateen's yard decides. Her own file loaded
on this tree in the session's scratch, not committed, reads the same: `main.treou.yard` 0,
`main.topsail.yard` 1, her main a pole, the courses the tréou. Pinned as it is; the clause is the
lead's to rule, not changed.
The case pins each row's levels, courses and topsails and her topsail's pole (five rows with the
tie's two below, passed; 56 passed with `tests/test_pole_mast.py`, `--slow`); the tréou's own pole, the last column, is the scratch
measure's (`treou/probe.py`). Once both are on `…/pkg-90`, the coordinating session checks the
same on her file.

**For the lead** (the third row; not built, the clause being ruled): the tréou's yard is the
main's lowest braced yard, so crossed above the great lateen's yard's crossing it takes the ruled
clause too and is read a topsail beside her topsail: taken in by the pole's way and not hauled up
as a course, and no course in her heave-to. Tar-D gives no height for either crossing. Two readings:
her file crosses the tréou's yard below the great lateen's yard's crossing, and the rule reads it
the course as it stands; or the clause is narrowed to a square sail set over the lateen and not one
set below it (the tréou's foot reaches near the deck, the topsail's does not). And **for her
builder**: with no tréou's yard crossed, her topsail's pole words say "Lowered the topsail down onto
the yard below and clewed it up there." and "Furled the topsail on the yard below.", the yard below
then being her great lateen's (measured on the probe, `treou/takein.py` in the session's scratch).

### Unsure, and for the lead

1. **The smack's getting under way under her topsail**, her cast 2 s earlier and her place 51 m
   and 63 m off at the harness's end: no truth or pin of hers reads it (the tiers), and it is the
   rule's own reach (her topsail a topsail, and the cast loosing every topsail). Said here rather
   than left to be found; whether a smack casts under her topsail, as a cutter does, is the
   lead's.
2. **The lateen-below clause** (the lead's lean) reaches no committed file: the tartane's topsail
   over her great lateen and the polacre's mizen topsail meet it with their files; the probes show
   it (`tests/test_yard_level.py`).
3. **The pole's times** are JUDGEMENT (no period time found): the brig's clew-up less its settling
   on the cap for the take-in, the square sail's furl less the climb for the furl.

## Steps A5 and A6 as ruled (nudge 39): the tréou her course, the pole's words at the hounds, the cast under her plain sail (2026-11-21)

**Their own hash, for the gate** (the lead's ruling 4): branch **`…/pkg-90-a56`**, cut from
**effbaed** (A5 and A6 as first built), A4 not in it. Its code is **e83f9e7**; the commit above it
adds this section alone. Brought across from `…/pkg-90-engine` by cherry-pick, in order:
58b28ab (this report's A5 and A6 section) as ca9d96b, 109ee87 (the tréou case) as e37fd53,
ca72113 (the section for the lead's reader) as 4aac105, c6018aa (the tie pinned) as ea24aa1,
da88dae (its report) as fcfc97a; then e83f9e7, the three rulings built. **Merged first:**
nothing new (A2's mended hash has not been said to have landed). **The base** of every
comparison is A1d, **8dce637**, as for A5 and A6's first section; where said, effbaed.

**Files** (each in the engine track's §7.1 row):
- `freesail/ship/graph.py`: the clause narrowed in `_find_yard_levels`; `_square_foot_m`;
- `freesail/evolutions/scripts.py`: `_plain_sail_topsails`, read at the cast's two places
  (`GetUnderWayScript._begin_loose` and its `loose` phase); `pole_words` and its two tables,
  `POLE_WORDS_ON_THE_YARD_BELOW` and `POLE_WORDS_AT_THE_HOUNDS`;
- `freesail/evolutions/runner.py`: the pole's words filled for `take_in_pole` and `furl_pole`;
- `data/evolutions/take_in_pole.yaml`, `data/evolutions/furl_pole.yaml`: their log lines' words in
  braces (`{pole_lowered}`, `{pole_hanging}`, `{pole_furl_from}`, `{pole_furled_on}`), and a
  sentence of the served notes for the hounds;
- `tests/test_yard_level.py` (the tréou case restated, the clause's narrowing, the pole's words
  by her case); `tests/test_pole_mast.py` (the smack's cast); `docs/dev/TuningNotes.md`, "Package
  90, A5 and A6" restated as ruled.

No ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). No class added
(functions, constants and a function inside one), so truth 7-606 and the checkpoint's list are not
touched. No key written into a committed file: stage 0's `KEY_CARRIERS` does not move. LF; ruff
check and format clean; no Python line over 100. Nothing under `docs/agents/consent/`.

### The three rulings, built

1. **The tréou is her course, wherever its yard crosses.** The clause is narrowed as ruled: a
   square sail is a topsail by the lateen's yard below it only where it is set over the lateen,
   its foot clear above the lateen's yard, and not where its foot comes down past that yard toward
   the deck. The foot is read from the cut as her file gives it, its head on its yard and its
   centre (`centre_height_m`) midway between head and foot: twice the centre less the yard's
   height (`graph._square_foot_m`). The yard below the square yard, and its sail a whole lateen on
   the same mast, are as before. A bare yard, with no sail to be set over the lateen, is not
   raised by it. **JUDGEMENT** on the foot: exact for a sail cut square; for a topsail cut wider
   at its foot its centre lies lower than midway, so the foot is read lower than it is and the
   clause errs toward the course. On her file the margin is 1.11 m: her topsail's foot 9.42 m,
   the great lateen's yard 8.31 m.
2. **The pole's words where the yard below is not a square yard.** `take_in_pole` and
   `furl_pole` take their words from the yard below (`scripts.pole_words`). Where a braced yard
   is crossed below the pole sail on its mast, the words are as before (the smack's, unchanged):
   "Lowered the topsail down onto the yard below and clewed it up there.", "Took in the topsail;
   lowered on the yard below, hanging in the gear.", "Lay out on the yard below and furl the
   topsail.", "Furled the topsail on the yard below.". Where none is, the pole's own: "Lowered the
   topsail down to the hounds and clewed it up there.", "Took in the topsail; lowered to the
   hounds, hanging in the gear.", "Lay aloft to the hounds and furl the topsail.", "Furled the
   topsail on its own yard, lowered to the hounds.". A yard whose sail is set flying and furled is
   not crossed: package 57's flying sail is sent down on deck with its yard, as her file's tréou
   is (`flying: true`) in her plain sail. So her topsail takes the hounds' words in her plain
   sail, and the yard below's words with her tréou set. The served notes say both. The times as
   before: **JUDGEMENT**, 60 s to lower and clew up and a 120-s furl (no period time found).
3. **Getting under way makes her plain sail.** The cast looses and sets the topsails of her plain
   sail alone (`scripts._plain_sail_topsails`), ruled by the plain sail and not by the vessel. A
   file with no plain sail group would have every topsail, as before; every committed file has
   one. Of the eighteen files the smack's topsail alone is not of her plain sail: every other
   file's topsails are (measured, each file's `_topsails` against its `plain sail`).

### Measured

- **A2's harness** (the going about and its kin, 270 runs; `a2/harness_v2.py` in the session's
  scratch) at 8dce637 and at e83f9e7: **269 the same in every tick, kind, trace and line.** The
  one that moves is the smack's `lie_a_try`, in its refusal's words alone: "She has no topsail to
  lie a-try under." -> "The topsail is not set; set it to lie a-try under it.". Her trace is the
  same. So **the cutter, every ship and the other files do not move by a line or a tick**:
  `cutter`'s fifteen runs, `seventy-four`'s, `frigate-36`'s and every other file's, all the same.
  Against A5 and A6 as first built (effbaed), the two that move back are the smack's `anchor` and
  `shoal_anchor`.
- **The smack's two anchor runs against the trunk** (f264f89, its harness run in a scratch
  worktree for the smack and the cutter): `anchor` and `shoal_anchor` the same as the trunk's,
  line for line and tick for tick, for both. She casts under her mainsail and her jib, her
  topsail furled throughout ("Under way on the starboard tack, under the mainsail and the jib;
  ...", +3,434 s in `shoal_anchor`). The two hulls' other runs that differ from the trunk differ
  in the same lines at A1d, the base: A2's going-about words ("Hands to the after braces; heave
  to." where the trunk has "head braces", the after yards' clauses), every tick and trace the
  same.
- **Every order of the smack's table** (`a5/play.py`, the first section's measure, at 8dce637,
  effbaed and e83f9e7). Everything listed there stands, being her topsail read as a topsail when
  the player has set it, but the cast:

  | Order, her topsail set over plain sail | At e83f9e7, as ruled |
  |---|---|
  | `heave to` | as first built: "...; braced the topsail aback; helm a-lee."; "Hove to on the starboard tack, topsail to the mast, helm a-lee." at +202 s; 50.5° off at 2.87 kn at +600 s (A1d: "Hauled up the courses.", under her fore-and-aft canvas, 47.3° off at 2.61 kn) |
  | `lie a-try` | as first built: lying a-try under the topsail and the foresail at +348 s in 15 kn and at +808 s in 30 kn (A1d: refused, "She has no topsail to lie a-try under.") |
  | `back and fill` | as first built: "Backed the topsail; her way checked." and "Filled the topsail; she forereaches." (A1d: "Hauled up the topsail." and "Backed the square sail ...") |
  | `take in the topsail`, `clew up the topsail` | as first built, the pole's way, in the yard below's words: 88 s from the start line (A1d: clewed up as a course, 154 s). **JUDGEMENT** |
  | `lower the topsail` | as first built: obeyed (A1d: refused, "A course is hauled up, not lowered; ...") |
  | `haul up the topsail` | as first built: refused, "A topsail or light sail on a pole mast is lowered, not hauled up; say 'lower the topsail' or 'take in the topsail'." (A1d: obeyed) |
  | `furl the topsail` | as first built, from the yard below: 300 s from the start line (A1d: "Lay aloft and furl the topsail.", 350 s). **JUDGEMENT** |
  | `take in all sail` | as first built: the topsail as take in; the jib, last, at +350 s (A1d: +412 s) |
  | `strike the topmasts` (and `send down the topgallant masts`, `fid the topmast`) | as first built: "... her masts are the main mast (a pole, the mast and topmast in one stick)." (A1d: "... her masts are the main mast.") |
  | **`get under way`** (Carrick Road, her topsail furled by `come to an anchor`) | **as A1d, line for line and tick for tick**: the topsail furled through the cast (first built: loosed and set, she paid off 2 s sooner and lay at +1,500 s 136.2° at 3.78 kn against 125.3° at 4.19 kn) |
  | `tack ship`, `wear ship`, `box haul`, `scud`, `shorten sail`, `set the topsail`, `trim sails`, `square the yards`, `brace sharp up on the larboard tack`, `come to an anchor` | as A1d, line for line and tick for tick |

  With her topsail never set, a player meets two changes: `lie a-try`'s refusal in other words,
  and the topmasts' orders naming the pole.
- **`lie a-try` on the trunk's cutter** (f264f89; `a56m/try.py`, settled as the harness's at-sea
  start, seed 7, the wind from 0°, her head 292.5°, plain sail braced sharp up on the starboard
  tack and trimmed, 2,400 s). Her plain sail sets her topsail. She is brought to: "All hands!
  Shorten sail and bring her to under the topsail.", then "Lying a-try under the topsail and the
  foresail, helm a-lee." at +296 s in 15 kn (36.5° off at 1.30 kn at +1,800 s) and at +420 s in
  30 kn (41.6° off at 1.72 kn). With her topsail furled first she is refused: "The topsail is not
  set; set it, close-reefed, to lie a-try under it.". **The smack follows the cutter, no
  further.** Her topsail set, the same order brings her to in the same words: lying a-try at
  +298 s in 15 kn (43.1° off at 0.97 kn) and at +546 s in 30 kn (49.4° off at 3.68 kn). Her
  topsail not set, as in her plain sail, she is refused in the cutter's words less "close-reefed"
  ("The topsail is not set; set it to lie a-try under it."), her topsail having no reef bands.
  The head's cutter is the trunk's in every line, tick and figure here. Whether a one-masted
  vessel lies a-try under a square topsail at all is the lead's look at the heavy-weather book,
  not settled here.
- **The tréou** (`tests/test_yard_level.py`, the tartane probe with her pole main; her own file is
  not on this branch). Each sail's cut moves with its yard (the cutter's cut), or her file's cut
  is given (her topsail's centre 12.6 m, its foot 9.42 m; her tréou's centre 5.8 m, its foot
  3.29 m):

  | The tréou's yard | Her topsail's level | The tréou's level | The courses; the topsails |
  |---|---|---|---|
  | not filed, at the probe's heights (the great lateen's yard 10 m, the topsail's 15.6 m, its foot 12.0 m) | 1, set over the lateen | none | none; the topsail |
  | not filed, at her file's heights and cut (8.31 m; 15.78 m, foot 9.42 m) | 1, set over the lateen | none | none; the topsail |
  | crossed at 8 m, below the great lateen's yard | 1 | **0, the course** | the tréou; the topsail |
  | crossed at **13 m**, above it (its foot 7.4 m) | 1 | **0, the course** (first ruled: 1) | the tréou; the topsail |
  | crossed at **8.31 m, with the great lateen's yard (the tie)**, her file's heights and cuts, filed after it as her file has it | 1 | **0, the course** | the tréou; the topsail |
  | the same, the tréou's yard filed before the great lateen's | 1 | **0, the course** | the tréou; the topsail |

  **The answer hangs on the sail's cut, not on the two yards' heights**: the clause compares the
  sail's foot with the lateen's yard, and the file's order breaks ties between braced yards
  alone. Beside it, the narrowing itself on the probe's topsail, its yard at 15.5 m with no
  braced yard below: cut down to near the deck (its foot 1.0 m), the course; its foot at the
  great lateen's yard's own height (10.0 m), the course, not clear above it; its foot at
  10.25 m, a topsail. The heights are exact in binary, so the tie is a tie. Her own file, read
  on this tree in the session's scratch and not committed: `main.topsail.yard` 1,
  `main.treou.yard` 0, the courses the tréou, her main a pole.
- **The pole's words, her case** (`tests/test_yard_level.py`, the probe at her file's heights and
  cuts, seed 7, 15 kn, plain sail set, then `take in the topsail` and `furl the topsail`). With no
  tréou's yard filed, and with her tréou set flying and furled as her file has it, the hounds'
  words. With the tréou's yard crossed (the cutter's square sail, not set flying), the yard
  below's. The smack's words are the yard below's, as `tests/test_pole_mast.py` pins them.

### Moved, old beside new, with reason

1. `tests/test_yard_level.py::test_the_tartanes_topsail_is_a_topsail_whether_the_treous_yard_is_crossed_or_not[above]`:
   the tréou's yard crossed at 13 m, its level **1 -> 0** (ruling 1). Its topsails were the
   topsail and the tréou, and are now the topsail alone; its courses were none, and are now the
   tréou. The case's probe moves each sail's cut with its yard (`_cut_moved`). Before, the sails'
   centres stayed where the cutter files them as their yards moved: the topsail's centre stood
   19.5 m high over its yard at 15.6 m.
2. The same case's two tie rows (c6018aa), **0 -> 0**, now by the cut and not by the clause
   counting a lateen yard strictly below. They now take her file's cuts.
3. `tests/test_yard_level.py::test_a_square_yard_over_a_whole_lateen_counts_the_lateen_yard_below_it`:
   its probe's topsail cut moved with its yard (its foot 12.0 m); every assertion as it was.

New: `tests/test_yard_level.py`'s `her-file-not-crossed` row,
`test_a_square_sail_whose_foot_comes_below_the_lateens_yard_is_the_course` and
`test_the_tartanes_topsail_on_her_pole_comes_down_to_the_hounds_where_no_yard_is_below` (three
rows); `tests/test_pole_mast.py::test_the_smack_gets_under_way_under_her_plain_sail_her_topsail_left_furled`.
No other pin moves (the tiers).

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is A1d, 8dce637** (its two tiers' junits, run
for A1d's report), test by test.

| Run | Base (8dce637) | A5-A6 as ruled (e83f9e7) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,638: 8,629 passed, 8 skipped, 1 xfailed, 0 failed (1 h 16 min) | 8,700: 8,691 passed, 8 skipped, 1 xfailed, 0 failed (1 h 23 min). **Test by test: every one of the base's 8,638 the same outcome; 62 new, all passed** (28 of `tests/test_pole_mast.py`, 34 of `tests/test_yard_level.py`); the moved pins' cases passed. Against effbaed's fast tier: every one of its 8,689 the same outcome, 11 new |
| **Slow tier whole**, `--slow -m "slow and not pace"` (the level read in `physics/sails.py` and the trim's, and the cast, so the tier whole) | 568: 557 passed, 11 xfailed, 0 failed (1 h 26 min) | 568: 557 passed, 11 xfailed, 0 failed (1 h 28 min). **Test by test: every one of the base's 568 the same outcome**, none new |
| **The lens with its slow cases**, `--slow`, `-n 3`: A5 and A6's lens (their first section) and `test_anchor`, `test_neufchatel`, `test_ships` | | 1,833 passed, 2 xfailed (10 min), on the tree as committed |

**The guard set of §10.2**, tallied from the two fast tiers' junits, base beside new, every case
the same outcome: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py`
74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74;
`tests/test_lateen_whole.py` 90; all passed at both.

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`.

### Unsure, and for the lead

1. **The foot read from the centre** (JUDGEMENT, above): a builder who files a square sail's
   centre by its area, for a topsail cut wider below, gives a foot lower than its cut's. The
   clause then reads it the course sooner. Her file's margin is 1.11 m. The polacre's mizen
   topsail, over her lateen mizen, is the other sail the clause is for. Her file is not on this
   branch: the polacre's builder reads its foot against her mizen's lateen yard.
2. **The pole's words read the yard below as it is, crossed or sent down**, at the line's own
   tick. The level of each yard is read from the parts as filed, so the tréou's level and her
   topsail's do not hang on whether the tréou is set (ruling 1).
3. **The earlier sections' words on the cast** (A5 and A6's "Measured" item 2, "Unsure" item 1,
   and the lead's reader's item 1 and its `get under way` row) describe A5 and A6 as first built,
   effbaed. They stand as the record of that hash. This section supersedes them for the gate.

Stopped after A5 and A6 as ruled, as briefed: A4's section follows on `…/pkg-90-engine`, on this
tree merged.

## Steps A1a and A1b's second pass (nudge 46): what befalls the yard, the belay, and the words (2026-11-22)

**Merged first:** nothing. `…/pkg-90-a1ab` is cut from **0d5d2c56**, the package's A1a-A1b merge
(A2's re-mend and A3 under it, no A1c), as the coordinating session asked. **The base** of every
comparison is 0d5d2c56, and "old" before A1a-A1b is 2a19e8f, its first parent.

**Commits:** **75abacd** on `…/pkg-90-a1ab` (parent 0d5d2c56), the eight items in one commit;
**c8787cb**, TuningNotes alone, one count corrected (item 5's: 1,512 pairs and 560 moved, where
75abacd gave 756 and 280); then this report's commit. The tiers ran on 75abacd's tree: the two
commits after it change TuningNotes and this report alone, which no test reads. **On origin:**
`…/pkg-90-a1ab`, pushed once the owner allowed the new branch.

**Which lines were resolved or changed by hand:** no merge is made in this hash, so no line is
resolved by hand. The one hand-resolved line under it stands as resolved: 0d5d2c56's
`not (head or after)` in `HeaveToScript.check`, the coordinating session's at A1a-A1b's merge
(nudge 43). This pass adds `and not head_sails_carried(self.ship)` beside it (item 3) and pins
the two both ways. Every other changed line is this pass's own, in the files below.

**Files** (my row's, and one widened):
- `freesail/evolutions/scripts.py`: `lateen_shift_befallen`; `ChangeLateenScript.tick`;
  `LateenChange.advance`, `_begun`, `_waiting`, `belay_words`, `belay`; `Script.belayed`,
  `Script.changes_left_words`; `FillAwayScript.left_words`; `head_sails_carried` and
  `HeaveToScript.check`; `TackScript._not_paid_off_words` and `TackScript.words`;
  `lateen_plan_words` (and its two callers); the party's comment;
- `freesail/evolutions/runner.py`: the belay line's words for a ship (`_left_words`);
- `freesail/orders/grammar.py`: `LATEEN_ONLY_VERBS`, `_unknown_verb`, `_names_a_whole_lateen`,
  `_the_practice_said`, `_match_verb`'s `hidden`; the sail room's mark in `_parse`;
- `freesail/api/readings.py`: `idle_lateen_rows`;
- **`freesail/api/action_readings.py`, widened by nudge 46's item 6, for its two lines alone**
  (`idle_rows` reading `idle_lateen_rows`; held at the stop rule and allowed by the coordinating
  session, db715d8's section);
- `tests/test_lateen_whole.py` ("The second pass", and the two pins below);
  `docs/dev/TuningNotes.md`: "Package 90, A1a and A1b's second pass".

No class added (functions and methods), so truth 7-606 and the checkpoint's list are not
touched. No key written into a committed file. No ship file moves (`python tools/gen_ships.py
<scratch>`: 18 of 18 byte for byte). LF; `ruff check` and `ruff format --check` clean; no Python
line over 100. Nothing under `docs/agents/consent/`.

### The eight items, each with its proof

Each proof is in `tests/test_lateen_whole.py`, entered by the door the lead's reader met it at,
and each fails when its mend is undone: the session's scratch `n46/mutate.py`, fourteen mutations
(the three of item 3 among them, and the lead's two of item 8), each failing its pins.

1. **What befalls the sail while its yard is shifted** (`lateen_shift_befallen`): blown out, its
   yard or mast carried away, or its jeers parted. **By itself**, each ends the work in its own
   words, the sail as the casualty left it, on its old side: "Could not shift the mainsail: the
   main lateen yard jeers parted while it was being shifted; the yard came down and the sail
   hangs in its gear." (and "it blew out of the bolt-ropes while it was being shifted", "the main
   lateen yard was carried away ...", "the main mast was carried away ..."). Before, all four
   ended "Shifted the mainsail; it stands to leeward of the mast." set and drawing. **In stays**,
   the yard is let be and said in the same words, the foresail and the mizen shifted and she
   tacked; before, the jeers parted ended "Shifted the mainsail" and set. Proofs:
   `test_a_casualty_while_the_shift_by_itself_is_in_hand_ends_it_in_true_words` (four),
   `test_a_casualty_in_stays_lets_the_yard_be_as_it_left_it_and_says_so` (two).
2. **A going about belayed while the lateens are being shifted**: each yard whose change is begun
   is finished to the side it was going, and each waiting its turn is left set on its mast; both
   are named in the belay's line. The xebec probe, seed 7: "Belayed tacking ship; the helm and
   the yards left as they stand at steady; the mainsail and the foresail and the mizen, their
   change begun, shifted round to the starboard side." (the wear the same at "come to"; the
   polacre's box-haul at "come to", "the foresail and the mizen"). Ten minutes on, all three set
   and drawing, 67° off at 4.3 kn after the tack and 101° off at 2.1 kn after the wear. With
   twelve hands to give (the main first): "...; the mainsail, its change begun, shifted round to
   the starboard side; the foresail and the mizen left on their masts, not yet shifted." The fill
   away the same as she lies (before, "... the foresail in its gear, not yet shifted round the
   mast", and left so). Before: "Belayed tacking ship; the helm and the yards left as they stand
   at steady.", and she lay 107° off at 2 kn under three lateens in their gear. Proofs: three
   tests named for it, five cases.
   - **The bilander's settee at the same belay, on the trunk (c91e7cad):** the same silence. Her
     tack belayed with the settee lowered on deck: "Belayed tacking ship; the helm and the yards
     left as they stand at steady.", the settee in its gear on deck ten minutes on, she 68° off at
     4.1 kn; her wear at "bear away" the same, she dead before the wind at 3.3 kn with it down.
     **Mended at the one cause** (the belay's words, `Script.changes_left_words`, one rule for
     both): "...; the mainsail lowered on deck, not yet dipped." (the fill away's own words since
     package 75's B3.3b), the settee left on deck as before. **Declared as a move on a
     committed ship:** the bilander's belay line alone, when a tack or a wear is belayed while
     her settee is lowered. Proof, on the settee brig:
     `test_a_going_about_belayed_while_the_settee_is_lowered_says_it_is_on_deck`.
   - **Listed, older code, not mended:** the lugger's lugs at the same belay have the same
     silence: "Belayed tacking ship; the helm and the yards left as they stand at helm down.",
     her fore and main lugs in their gear ten minutes on (the wear the same at "come to"). Her
     `LugDip` is another field; naming it would move her, and no one has asked for it.
3. **The heave-to's refusal**: the lateens' words only where she carries neither a head sail nor
   a braced yard. A head sail carried is one she can still set, not blown out, unbent or carried
   away, as a yard sent down or wrecked is none of `working_yards` (JUDGEMENT). The xebec with
   her jibs furled: "No head sail is set to haul to windward, nor a topsail to lay aback."
   (before, "She will not lie to under her lateens: there is no sail to bring her to."). **Pinned
   both ways in this hash**, on the probes: the xebec with her jibs furled and with them blown
   out; the tartane with her jibs blown out, her topsail furled, and with its yard sent down.
   With the yards' check read of what is set, or dropped, or the head sails read of what is set,
   the pin fails:
   `test_a_rig_of_lateens_with_a_head_sail_or_a_yard_not_set_is_told_what_is_not_set`.
4. **`leave` on today's ships**: an order only on a hull with a whole lateen, and only in the
   practice's forms ("the lateens" after it, an occasion said, or a whole lateen of hers named).
   On every other hull it is neither matched nor hinted. Old beside new, 2a19e8f against the
   mended tree: nine forms of `leave` and four near spellings on each of the eighteen files, every
   answer the same ("'leave port' is not an order this ship understands. ..."). At 0d5d2c56:
   "There is no such part as the  in this ship.", "... as the ship in this ship.", "Leave what?
   ...", and "leav port" hinted "did you mean 'leave'?" on all eighteen. On the probes the other
   forms answer as at the trunk, and no answer anywhere carries an empty name. Proofs: one test
   for each of the eighteen files, and one on the xebec.
5. **The standing orders' contraries**: the sail room's mark is kept only when `shift` names a
   whole lateen of a hull with one. Old beside new on the cutter, and on every ship: 1,512 pairs
   of sail orders (84 on each file), every answer and every manner the same as at 2a19e8f. At
   0d5d2c56, 560 had moved on thirteen ships, 280 of them in the contrary itself, among them the
   cutter's "shift the jib" beside "shift the jib for a new one" (and "bend the jib" likewise), a
   contrary on the jib where it was a repetition. On the xebec probe the whole lateen's two
   shifts stay contrary, two works on one sail.
6. **The practice's row in the samples**: left out of the sample where she carries no whole
   lateen (`idle_lateen_rows`, read by `idle_rows`, the sample's own road); on the xebec probe it
   rides. **The rule of the readings that wants every row on every ship**, the lead's "say which":
   the readings tool's. It keeps the row on every ship, as every reading is named in the primer
   (`tests/test_grammar_book.py`) and the tool's own tests read every registry row. Proofs: one
   test for each of the eighteen files, and the xebec's.
7. **The words**: the bare tartane probe tacked (her topsail and head sails furled at once, seed
   7): "Tacked; through the wind on the larboard tack, heading NE by N (38°), but she has not
   paid off: she lies 38° off the wind with a knot of sternway." (before, "Tacked; full and by
   ... with no way of way.", she going astern at up to 1.4 kn); "with no way on her" under half a
   knot either way. `tack ship and leave the mizen` with the mizen taken in: "...; the foresail and
   the mainsail to be shifted in stays; the mizen, ordered left, is not set." ("the lateens" said
   only of all she carries); before, "...; the lateens to be shifted in stays." and the clause
   dropped. The comment's "six for 16 m" is seven. JUDGEMENT on the words.
8. **The pins the tests lacked**: the two-thirds on the bad hand, at the door it is met at (tacked
   with the lateens left, each draws two-thirds of the cloth it draws with its yard to leeward;
   made to draw fully, the pin fails); the least party of four, at the tartane's mizen (its 7-m
   yard takes three by the yard and four by the rule; shifted by itself with two hands to give,
   7 m at 14.6 s a metre times four over two; made one, the pin fails); and item 3's line.

### Ruled, declared: the lugger's bow watch

A move on a committed ship, allowed by the lead and declared here and in TuningNotes. The
session's scratch `n46/windshift.py`: each of the eighteen files settled as A2's harness settles
her (seed 7, 15 kn, plain sail braced sharp up, 2,400 s) on each tack, then the wind shifted at
a stroke toward her bow by 4, 8 and 10 points, the last two through it; every event of 600 s
kept, with a trace every 10 s, 108 runs. **2a19e8f beside 0d5d2c56: 104 the same in every event
and trace; the lugger's four through her bow move, by one line alone, her trace the same at every
tick.** With the wind through her starboard bow she now hears, at +3 s, "The wind has come round
ahead to the larboard bow: the foresail and the mainsail are against their masts; dip them when
you will." (on the larboard tack, "... to the starboard bow ..."), where before nothing was said.
**0d5d2c56 beside the mended tree: all 108 the same.** A2's harness (A1a and A1b's 270 runs) never
brought the wind through her bow, so "nothing moves" there was not so.

### Measured: today's ships, base beside the mended tree

- **A2's harness** (the going about and its kin, 270 runs on the eighteen files, A1a and A1b's own
  measure) at 0d5d2c56 and at the mended tree: **every tick, kind, trace and line the same**,
  3,205 events and 32,940 trace rows, the two files byte for byte.
- **The wind through the bow** (`n46/windshift.py`, above): 108 runs, the same at both.
- **`leave` and its near spellings**: 162 answers (nine forms on each of the eighteen files) and
  72 more (four near spellings on each), every one as at 2a19e8f, the trunk's.
- **The contraries**: 1,512 pairs, every answer and every manner as at 2a19e8f.
- **The probes** (seed 7, from the settle of `tests/test_lateen_whole.py`), each item's runs as
  set out above. Their going about with nothing befallen and nothing belayed is A1a-A1b's, none
  of its lines moved: the lateen file's 32 tests before this pass (63 cases) pass as they were,
  but for the two pins below.

### Moved, old beside new, with reason

1. `tests/test_lateen_whole.py::test_a_rig_of_lateens_with_no_head_sail_set_will_not_lie_to`
   -> `...with_no_head_sail_nor_braced_yard_aboard_will_not_lie_to` (item 3): the xebec with her
   jibs furled was refused in the lateens' words; it is her jibs blown out now. Furled, she is told
   what is not set, the new test beside it.
2. `tests/test_lateen_whole.py::test_a_hull_with_no_whole_lateen_answers_every_word_as_before`
   (item 4): the cutter's "leave the mainsail" was "She carries no whole lateen; ..." and "leave
   the mainsail in stays" "... but not 'stays'"; both now get the trunk's answer, "'leave the
   mainsail' is not an order this ship understands. ..." and the same for its own words.

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is 0d5d2c56**, its two tiers run here for
this hash (its own worktree, its own junits), test by test. The mended hash's are of 75abacd's
tree (the two commits after it change TuningNotes and this report alone). Compared by the test's
id with the xdist group's `@...` stripped: the new module fixtures regroup the lateen file's
cases, so their ids carry another group.

| Run | Base (0d5d2c56) | The second pass (75abacd) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,665: 8,656 passed, 8 skipped, 1 xfailed, 0 failed (1 h 11 min) | 8,722: 8,713 passed, 8 skipped, 1 xfailed, 0 failed (56 min). **Test by test: every one of the base's 8,665 the same outcome but the pin renamed** (`test_a_rig_of_lateens_with_no_head_sail_set_will_not_lie_to`, now `...with_no_head_sail_nor_braced_yard_aboard_...`, passed); **58 new, all passed**, every one in `tests/test_lateen_whole.py` (57 new cases and the renamed one) |
| **Slow tier whole**, `--slow -m "slow and not pace"` (the runner, the readings' samples and the grammar touched, so the tier whole) | 569: 558 passed, 11 xfailed, 0 failed (1 h 8 min) | 569: 558 passed, 11 xfailed, 0 failed (1 h 5 min). **Test by test: every one of the base's 569 the same outcome**, none new |

**The guard set of §10.2**, tallied from the two fast tiers' junits, base beside new, every case
the same outcome: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py`
74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed at both.
`tests/test_lateen_whole.py`: 63 at the base, 120 now, all passed.

**The lens of the touched files**, before the commit (`-n 2`): `test_lateen_whole`, `test_settee`,
`test_bilander`, `test_lug`, `test_hull_lugger`, `test_standing`, `test_orders`, `test_held_work`,
`test_evolutions`, `test_catalogue`, `test_probes_90`, `test_grammar_book`,
`test_practice_orders`, `test_mends_75` and `test_lateen`: 1,652 passed, 1 skipped; then, with
item 6 in, `test_agents`, `test_practice`, `test_practice_orders`, `test_knowledge`,
`test_agent_api`, `test_grammar_book` and `test_readings`: 238 passed, 1 xfailed.

**The generator:** `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`. **`ruff check`** and **`ruff format --check`**: clean.

### Unsure, and for the lead

1. **The yard begun is finished at the belay itself** (item 2), and its seconds left are not
   kept: a belay given just after a change begins finishes the yard for nothing (the xebec's
   19-m main, 165 s at 8.7 s a metre). The other road would hand the rest of the change on as
   the yard's own shift by itself, its time kept, and its line said when it is done. For the
   lead.
2. **The shift by itself belayed** is left in its gear and said, as A1a built it ("the mainsail
   in its gear, its yard not yet shifted round the mast"). Item 2's rule is said of a going about,
   and finishing this one at a belay would make the belay a free shift. For the lead.
3. **Two lines for one casualty in stays** where the casualty says its own: a sail blown out by a
   shot has its own line, and the change's "Could not shift the mainsail: it blew out of the
   bolt-ropes while it was being shifted." follows it.
4. **The lugger's belay mid-dip** (item 2's listed case): the same silence, older code, not
   mended.

**Next:** this hash goes back to the gate. Then `…/pkg-90-a1ab` is merged into `…/pkg-90-engine`
by a merge commit, so that A1c, A1d, A5-A6 and A4 sit on the mends. A dry run shows its
conflicts: `scripts.py`'s two (the tack's haul and the wear's "Wind aft.", A1d's against A2's
readers, as the look-ahead set out), `tests/test_known_truths.py`, `tests/test_lateen_whole.py`
and TuningNotes (each both sides' sections appended, kept whole). Each will be resolved by both
rules and named line by line in that merge's section, with `ruff check` before its tiers.

Stopped after the second pass, as briefed: the merge into the engine follows.

## Steps A1a and A1b's third pass (nudge 48): the yard finished in its time, and the end that says what she is (2026-11-22)

**Merged first:** nothing. On `…/pkg-90-a1ab` above **2e1e19b**, with no merge, as the
coordinating session asked. **The base** of the tiers' comparison is 0d5d2c56, as for the second
pass (its two tiers' junits), and 2e1e19b's tiers (75abacd's tree) are set beside it. "Old" in
the words below is the second pass unless said.

**Commits:** this pass is one commit, which carries this section with its code. **The fast and
the slow tier run on that exact commit**, whose hash is the one sent. Their results follow in a
commit after it that touches this report alone, as the lead's reminder allows when it is said
plainly. It is said plainly here.

**Which lines were resolved or changed by hand:** no merge is made in this pass, so no line is
resolved by hand. Every changed line is this pass's own, in the files below.

**Files** (my row's, and three widened):
- `freesail/evolutions/scripts.py`:
  - `_how_it_went` and `lateen_shift_befallen` (the mast named, "shot away", a sheet or a tack
    parted);
  - `LateenChange`'s `factor`, `handed`, `belay_words` and `belay`;
  - `Script.handed_on`, and `changes_left_words` with the lugger's lugs;
  - `HANDED_ON`;
  - `ChangeLateenScript`'s handed-on work (`handed`, `said_id`, `holds`, `begin`, `_tick_handed`,
    `_set_on_its_side`, `_lies`, `remaining_s`, `left_words`, `words`);
  - `lateen_plan_words` (the clause's lateens not set, "the lateens"), and the clause said with
    every lateen taken in, in the tack and the wear;
  - `TackScript._how_she_lies_words`, `_not_paid_off_words`'s `how`, `_jibs` and `_boom_names`,
    and the tack's head-sheet words;
- `freesail/evolutions/runner.py`: `_hand_on`; the belay's hand-on; `_begin` with no first line
  for work handed on; `_start_waiting` reading no beginning's conditions for it;
- `freesail/orders/grammar.py`: `_no_sail_before_the_occasion`;
- `data/evolutions/change_lateen.yaml`: its last line, `{it_stands}`;
- **`freesail/world/knowledge.py`'s `rows_elsewhere(senses, world=None)`, and its two callers,
  `freesail/agents/harness.py`'s `_readings_elsewhere` and `freesail/api/queries.py`'s
  `knowledge_block`, one argument each: the three widened by nudge 48's item 3** (allowed by the
  coordinating session, its answer to e1b5671's question);
- `tests/test_lateen_whole.py` ("The third pass", and the second pass's tests where the rule
  moved); `docs/dev/TuningNotes.md`: "Package 90, A1a and A1b's third pass".

**Form:**
- No class is added (methods, functions and a constant), so truth 7-606 and the checkpoint's
  list are not touched.
- The new fields are plain dicts and floats, with class defaults on `ChangeLateenScript`, so a
  save from before loads.
- No key is written into a committed file, and no ship file moves (`python tools/gen_ships.py
  <scratch>`: 18 of 18 byte for byte).
- LF; `ruff check` and `ruff format --check` clean; no Python line over 100. Nothing under
  `docs/agents/consent/`.

### The six items, each with its proof

Each proof is in `tests/test_lateen_whole.py`. Each fails when its mend is undone: the session's
scratch `n46/mutate48.py`, sixteen mutations, each failing its pins, among them the lead's two
survivors ("no way of way", the two-thirds made 0.9). The second pass's thirteen
(`n46/mutate.py`), run again on this tree, each still fail theirs.

1. **A yard begun is finished in its time.**
   - At the belay the manoeuvre ends as before. Each yard whose change is begun goes on as work in
     hand: one `change_lateen`, its subject the longest yard.
   - The runner begins it without the preconditions of its beginning, the yards being in their
     gear, and without its first line.
   - It is worked for the seconds each yard had left, at no lighter a rate than the manoeuvre's own
     at the belay (the runner's factor for it then). Each yard is said when it is set.
   - The yards waiting are left on their masts and said, as before.
   - The belay's line: "...; the mainsail and the foresail and the mizen, their change begun, still
     being shifted round to the starboard side."
   - Belayed in its turn, the work handed on is a shift by itself, "... in their gear, their yards
     not yet shifted round their masts" (allowed as built).

   Measured, seed 7, the seconds from the order until every lateen draws on its new side, plain
   beside belayed as the change begins: the xebec's tack 248 beside 248 (the second pass, 44); the
   tartane's 262 beside 263 (80); the polacre's 292 beside 292 (105); her box-haul 435 beside 436
   (246); the xebec's wear 258 beside 259 (55); the polacre's fill away 187 beside 190 (1). At
   0d5d2c56 none of the six belayed drew in 2,400 s. **Pinned:** a belayed going about is never
   sooner on the new hand than the plain one, on all six; and again with the handed-on work's own
   hands made to work at half the manoeuvre's factor, which only the rate holds.

   A floor in seconds was built beside the rate first. The mutations showed it to be the rate's
   twin: undoing either alone, the other held. It is gone, and the rate alone keeps the time.
2. **A sheet or a tack parted mid-shift:** "Could not shift the mainsail: the main lateen sheet
   parted while it was being shifted; the sail hangs in its gear, not set, till its sheet is rove
   afresh." (the tack's alike), by itself and in stays. Before, it ended "Shifted ..." set and
   drawing fully. Proofs: the casualty tests, two cases each more.
3. **The rows not to be had**, counted where they are hers. On the eighteen, from six places, at
   both doors (the stations' line and the player's `knowledge_block`), 2a19e8f beside the mended
   tree: all 216 lines the same, byte for byte. At 0d5d2c56, 180 had read "19 more" for "18
   more". On the xebec probe the row is still counted. Proofs: one test for each of the eighteen,
   and the probe's.
4. **`leave` on a lateen hull:** "leave in stays" and "leave port in stays" are answered "Leave
   what in stays? Her practice is said of the lateens together: 'leave the lateens in stays'."
   ("Shift what in wearing? ..." alike). Before, "There is no such part as the in stays in this
   ship; did you mean the main staysail ...".
5. **The words:**
   - With every lateen taken in, the clause is said ("...; the mizen is not set and is let be.";
     "the lateens are not set and are let be"), in the tack and the wear.
   - "ordered shifted, is not set" is now "is not set and is let be".
   - **The end's line says what she is**, on any hull with a whole lateen:
     - the polacre with her jibs furled: "Tacked; braced up on the larboard tack, heading NE
       (46°), but she has not paid off: she lies 46° off the wind with a knot of sternway.";
     - the tartane with hers furled, the same at 39°;
     - the xebec with her mizen furled: "Tacked; through the wind on the larboard tack, heading
       E (95°), but she has fallen off: she lies 95° off the wind with three knots of way." (it
       was "full and by").
   - **The mast named where it went**, "carried away" or "shot away" as the strain's own line has
     it.
   - **"Draw jib" with the jibs furled is the lateens' road** and is mended, not listed: the
     polacre's fore lateen was counted among the head sheets (A1b). It is now "ease off the
     foresail sheet" and "Draw the foresail; trim aft its sheet."; on today's ships the head sheets
     are the set jibs alone, as at the trunk.
6. **Two pins:** "with no way on her", at the words' own door; and the two-thirds against
   `2.0 / 3.0` itself.

### Ruled, declared

- **The bilander's belay line:** its true extent, by the lead's reader, is all sixty runs with the
  settee lowered at the belay (the tack, putting her about, the wear, the wear short round, the
  box-haul, boxing her off), each differing by that suffix alone.
- **The lugger's lugs at the same belay**, the third move on a committed ship, declared:
  - old, "Belayed tacking ship; the helm and the yards left as they stand at helm down.";
  - new, "...; the foresail and the mainsail lowered, not yet dipped." (the wear alike, at "come
    to");
  - words alone: her lugs are in their gear ten minutes on at both.
- **"lateen practice" typed on a ship with none** answers "The lateen practice: no whole lateen
  aboard.", declared: 36 answers in the reader's sweep, the only one on the eighteen that differs.
- **Unsure 3** (two lines for one casualty in stays): allowed.
- **The lugger's bow watch**, by the reader: 72 of 672 wind-shift runs, hers alone, the line 3 s
  after the shift, her trace identical.

### Measured: today's ships

- **A2's harness** (270 runs) on this tree: byte for byte as at 0d5d2c56.
- **The wind-shift runs** (`n46/windshift.py`, 108): byte for byte as at 0d5d2c56.
- **The lens of the touched files**, `-n 2`: 1,906 passed, 1 skipped, 1 xfailed. It ran over
  `test_lateen_whole`, `test_settee`, `test_bilander`, `test_lug`, `test_hull_lugger`,
  `test_standing`, `test_orders`, `test_held_work`, `test_evolutions`, `test_catalogue`,
  `test_probes_90`, `test_grammar_book`, `test_practice_orders`, `test_mends_75`, `test_lateen`,
  `test_agents`, `test_practice`, `test_knowledge`, `test_agent_api`, `test_readings` and
  `test_checkpoint`.

### Moved, old beside new, with reason

The second pass's own pins, where the rule moved:
1. Its three belay tests: from "..., their change begun, shifted round to the starboard side.",
   every yard set at the belay, to "..., still being shifted round ...", the yards set and said in
   their time.
2. `test_the_clause_names_a_lateen_not_set_and_the_lateens_are_all_she_carries`: "the mizen,
   ordered left, is not set." to "the mizen is not set and is let be.".
3. `test_a_whole_lateen_on_the_bad_hand_draws_two_thirds_of_its_cloth`: from the constant to
   `2.0 / 3.0`.

`change_lateen.yaml`'s last line reads "Shifted the {sail}; {it_stands}.", the same words where it
stands to leeward.

### The test sets run, with counts, and the base comparison

**The tiered hash is 1458b0e**, the third pass's commit itself. The commit after it, which
writes these results, touches this report alone.

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch, on 1458b0e's own worktree. Compared test by test with
the two junits of the second pass's section: **the base, 0d5d2c56**, and **the second pass,
75abacd** (2e1e19b's tree), by the test's id with the xdist group's `@...` stripped.

| Run | 1458b0e | Against the base (0d5d2c56) | Against the second pass (75abacd) |
|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,766: 8,757 passed, 8 skipped, 1 xfailed, 0 failed (58 min 40 s) | **Every one of the base's 8,665 the same outcome but the pin the second pass renamed** (its new name passed); **102 new, all passed**, every one in `tests/test_lateen_whole.py` | **Every one of the 8,722 the same outcome**, none gone; **44 new, all passed**, every one in `tests/test_lateen_whole.py` |
| **Slow tier whole**, `--slow -m "slow and not pace"` (the runner, the readings' samples and the grammar touched, so the tier whole) | 569: 558 passed, 11 xfailed, 0 failed (1 h 6 min) | **Every one of the 569 the same outcome**, none new | **Every one of the 569 the same outcome**, none new |

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at
both: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed.
`tests/test_lateen_whole.py`: 63 at the base, 120 at the second pass, 164 now, all passed.

**On 1458b0e's tree:** `python tools/gen_ships.py <scratch>`, 18 of 18 byte for byte with
`data/ships/`; **`ruff check`** and **`ruff format --check`**, clean.

### Unsure, and for the lead

1. **The work handed on calls all hands** ("All hands! (to shift the foresail)") where the
   manoeuvre had the watch (the fill away): it is the shift by itself's own file (`hands: all`),
   and its rate is never lighter than the manoeuvre's.
2. **A save taken while the work handed on is in hand** loads: the work is a `change_lateen` with
   plain fields. A save while the manoeuvre's change is in hand is refused, as the second pass had
   it.

**Next:** `…/pkg-90-a1ab` merged again into `…/pkg-90-engine`, as before.

## A1c's hash (nudge 49): the five that ride it, the work handed on in its place and on its hands, and the end where a course was given (2026-11-22)

**Merged first:** nothing. `…/pkg-90-a1c` is cut from `…/pkg-90` at **b3c68af4**: A1c and A3's
lists on the third pass, the trunk at 7a1bd65e merged in, and 7173281 (the third pass's tiers)
with them. No merge is made on it, so **no line is resolved by hand**. Every changed line is this
pass's own, in the files below. **The base** of the tiers' comparison is b3c68af4, its two tiers
run here on its own worktree. "Old" in the words below is b3c68af4.

**Commits:** this pass is one commit, which carries this section with its code. **The fast and
the slow tier run on that exact commit**, whose hash is the one sent. Their results follow in a
commit after it that touches this report alone. It is said plainly here.

**Files** (my row's; none widened):
- `freesail/evolutions/runner.py`:
  - `_hand_on`: the manoeuvre's place (`order`, `given`) and its hands (`assignment`, its hands'
    `at`, `want`, `all_hands`, `held_up`), the work begun at once;
  - the belay's hand-on before the manoeuvre is removed;
  - `_begin` and `_start_waiting`: the third pass's two skips for work handed on taken out, each
    line as on the trunk before it;
  - `_describe`: the parts a script names (`Script.parts_named`);
  - `HANDED_ON` no longer imported.
- `freesail/evolutions/scripts.py`:
  - `Script.parts_named`, and `ChangeLateenScript.parts_named` (the yards handed on);
  - `TackScript._how_she_lies_words(wind, aim, to_it)`, read in `_to_the_course` and at
    `_pay_off`'s end, and `words` leaving out the course's clause where she lies otherwise.
- `tests/test_lateen_whole.py`: "The five that ride A1c's hash", 22 cases; no pin of before moved.
- `docs/dev/TuningNotes.md`: "Package 90, the five that ride A1c's hash".

**Form:**
- No class and no field is added: a method on `Script`, one on `ChangeLateenScript`, and a
  parameter. So truth 7-606 and the checkpoint's list are not touched, and a save from before
  loads.
- No key is written into a committed file, and no ship file moves (`python tools/gen_ships.py
  <scratch>`: 18 of 18 byte for byte).
- LF; `ruff check` and `ruff format --check` clean; no Python line over 100. Nothing under
  `docs/agents/consent/`.

### The five, each with its proof

Each proof is in `tests/test_lateen_whole.py`. Each fails when its mend is undone: the session's
scratch `n49/mutate49.py`, ten mutations, each failing its pins.

1. **An order waiting behind a manoeuvre waits behind the work handed on.** The work keeps the
   manoeuvre's place in the order of work. Measured on the xebec probe, seed 7, the order given
   mid-change in a tack and then "belay tacking ship":
   - "take in the mainsail": old, "The mainsail is in the gear; there is nothing to take in." the
     next tick, the take in dropped and all three lateens set; new, it waits and "Took in the
     mainsail; brailed up to its yard." follows the last shift, as after a plain tack.
   - "take in all sail": old, the three lateens' take in dropped alike; new, the five sails taken
     in after the shift.
   - "shift the mainsail": old, "Could not shift the mainsail: The mainsail is in the gear; ...";
     new, "The mainsail lies to leeward of its mast already.", as after a plain tack.

   Proof: `test_an_order_waiting_behind_a_belayed_manoeuvre_waits_behind_the_work_handed_on`,
   the three orders (a later number given back, the three fail).
2. **The end's line where a course was given** is held to her state as the plain order's is, on
   any hull that carries a whole lateen. "Full and by" is read against her close-hauled angle,
   "the course ordered" against the course, and "trimmed for the course ordered" against the
   course she paid off to, each within 10°. Where she lies otherwise the course's clause is not
   said, and the line says how she lies. Measured, seed 7 (`n49/r2.py`), old and new:
   - the polacre probe, her jibs furled, `steer north-east`: old "Tacked; braced up on the
     larboard tack, heading NE (49°), full and by."; new "..., heading NE (49°), but she has not
     paid off: she lies 49° off the wind with no way on her.";
   - the same, `steer east-north-east`: old "..., the course ordered.", 19° short of it; new as
     above;
   - the same, `steer east`: old "Tacked; braced up for the course ordered on the larboard tack,
     heading NE (49°)." with 0.9 kn of sternway; new "..., but she has not paid off to it: she
     lies 49° off the wind with a knot of sternway.";
   - the xebec probe, her mizen furled, `steer north-east` and `steer east-north-east`: old
     "Tacked; trimmed on the larboard tack, heading E (94°), full and by." and "..., the course
     ordered."; new "..., but she has fallen off: she lies 94° off the wind with three knots of
     way.";
   - the same, `steer east`, on her course: "Tacked; trimmed for the course ordered on the
     larboard tack, heading E (93°).", old and new.

   Proofs: `test_the_tacks_end_where_a_course_was_given_says_how_she_lies` (the five above),
   `test_the_tacks_end_on_the_course_ordered_is_said_as_before`, and
   `test_the_course_ordered_is_read_against_the_course_not_full_and_by`. The last is at the
   tack's own door. No end in play lies between the two measures of a course steered as she
   lies (within half a point of close-hauled), and the mutation "read against full and by"
   passed every test in play. Her head 12° past full and by is 7° past a course 5° free of it,
   and is on it.
3. **Three rules no test held, each pinned:**
   - **A casualty in the work handed on:** `test_a_casualty_in_the_work_handed_on_ends_it_in_true_words`
     (the mainsail, the last yard, blown out, its jeers, sheet or tack parted, its yard carried
     away: the work ends in the file's words, the others finished) and
     `test_a_casualty_to_a_yard_not_the_last_is_said_and_the_rest_are_finished` (the mizen blown
     out, said, the foresail and the mainsail finished).
   - **The side's words where a yard ends to windward,** with the ruling:
     `test_a_wear_belayed_with_the_wind_aft_finishes_its_yards_and_says_where_they_lie`. Brought
     back to her old tack (`steer west-north-west`), each yard is finished to the side it was going,
     now the weather side: "Shifted the mainsail; it lies on the mast, to windward.". Left to go
     on, each stands to leeward.
   - **The work handed on made to wait: the branch is taken out.** With item 4 the work takes
     the manoeuvre's hands and begins at once, so nothing reaches it. `_start_waiting`'s skip of
     its preconditions and `_begin`'s skip of its first line are gone, each line as on the trunk
     before the third pass. On the trunk at 55b9658e, too, the work asked for all hands just after
     the belay had let the manoeuvre's go, and an all-hands request is too few only with no idle
     hand in its pool. The pin (item 4's test): it is never waiting, in the manoeuvre's place, on
     the very hands the manoeuvre had. Given its own request again, the pin fails.
4. **The work handed on takes the hands the manoeuvre had,** with its request and its call, and
   is named of every yard it still shifts ("shifting the mainsail and the foresail and the
   mizen").
   - On the polacre probe's fill away from hove to, her fore lateen to windward, belayed
     mid-change: old, "All hands! (to shift the foresail)" at the belay, and 70 hands; new, the
     fill away's twelve and no call, the foresail set at the same tick, 1489.
   - On the xebec's tack: the tack's 92 hands, all hands, piped down as the last yard is set.
     "take in the jib" given then waits with "...; the watch is shifting the mainsail and the
     foresail and the mizen.".
   - The six probes' times from the order until the lateens draw on the new side, plain and
     belayed (`n46/r48b.py`), are the third pass's, each to the second, old and new: the xebec's
     tack 248 and 248, the tartane's 262 and 263, the polacre's 292 and 292, her box-haul 435 and
     436, the xebec's wear 258 and 259, the polacre's fill away 187 and 190.

   Proof: `test_the_work_handed_on_takes_the_manoeuvres_hands_and_is_named_of_its_yards`, the
   tack and the fill away. Given its own request, or named of one yard, it fails.
5. **Read, not reached: `_try_resume` fails held work without handing on.** It is not reached by
   a manoeuvre with a change in hand, and so is left as it stands.
   - Work is held only by a manoeuvre's belay of the step-list work in hand (scripted work is not
     held: `_call_all_hands`) and by a post's leaving work they hold (`_post_off`).
   - No post is counted a hand of a manoeuvre, nor of any work while one is in hand
     (`_working_posts`). Every manoeuvre that makes a lateen change is a helm manoeuvre: the tack,
     the wear, the fill away, the box-haul and boxing her off.
   - A save is refused while a manoeuvre's change is in hand (the second pass's pin,
     `test_the_change_is_built_only_when_a_lateen_is_to_be_shifted`), so none comes back held.

   Proof: `test_no_post_is_counted_for_a_manoeuvre_so_none_with_a_change_is_held`. The polacre's
   master heads the watch on deck, and the watch is counted too few. The master is counted for a
   numbered take in, but not for the fill away nor while it is in hand. Gone below mid-change, the
   fill away goes on, never held, and its yard is shifted. With the manoeuvre rule undone in
   `_working_posts`, it fails.

### Ruled, nothing to build

- **The lugger's lugs at the belay**, the third declared line: its extent as measured by the
  lead's reader is written into TuningNotes. It is 180 of 1,420 belays (the tack 68, putting her
  about 68, the wear 44), at steady 92, come to 44, helm down 32 and mainsail haul 12.
- A wear belayed with the wind aft and brought back to her old tack, its yards finished to
  windward and said: allowed as built, pinned under item 3.
- The second pass's unsure 2 (saves): allowed as built. The readings tool's full list: allowed.

### Measured: today's ships

- **A2's harness** (270 runs) on this tree: byte for byte as at b3c68af4.
- **The wind-shift runs** (`n46/windshift.py`, 108): byte for byte as at b3c68af4.
- Every changed road is read only on a hull that carries a whole lateen, or only by the work a
  belay hands on, which only a whole lateen's change makes.

### The test sets run, with counts, and the base comparison

**The tiered hash is 2f3285c**, this pass's commit itself. The commit after it, which writes these
results, touches this report alone.

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base, b3c68af4**, ran here the same way on its own
worktree, and 2f3285c on its own. Compared test by test by the test's id, with the xdist group's
`@...` stripped.

| Run | b3c68af4 (the base) | 2f3285c | Against the base |
|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,793: 8,784 passed, 8 skipped, 1 xfailed, 0 failed (1 h 22 min, the lens and the harness running beside it) | 8,815: 8,806 passed, 8 skipped, 1 xfailed, 0 failed (58 min 39 s) | **Every one of the base's 8,793 the same outcome**, none gone; **22 new, all passed**, every one in `tests/test_lateen_whole.py` |
| **Slow tier whole**, `--slow -m "slow and not pace"` (the runner, the scripts and the words touched, so the tier whole) | 569: 558 passed, 11 xfailed, 0 failed (1 h 6 min) | 569: 558 passed, 11 xfailed, 0 failed (1 h 8 min) | **Every one of the 569 the same outcome**, none gone, none new |

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at
the base: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed.
`tests/test_lateen_whole.py`: 183 at the base, 205 now, all passed.

**The lens of the touched files**, `-n 2`, run on the working tree beside the commit: 2,305 passed,
1 skipped, 1 xfailed, 0 failed (18 min); the fast tier above holds each of its files on the exact
hash. It ran over `test_lateen_whole`, `test_settee`, `test_bilander`, `test_lug`,
`test_hull_lugger`, `test_standing`, `test_orders`, `test_held_work`, `test_evolutions`,
`test_catalogue`, `test_probes_90`, `test_grammar_book`, `test_practice_orders`, `test_mends_75`,
`test_lateen`, `test_agents`, `test_practice`, `test_knowledge`, `test_agent_api`, `test_readings`,
`test_checkpoint`, `test_hands`, `test_captains`, `test_crews`, `test_helm_kind`, `test_lying_to`,
`test_tackle_orders`, `test_found_on_the_way_85`, `test_mends_109`, `test_held_hulls`, `test_driver`
and `test_replay`.

**The coordinating session's tiers on 5e42ed2f**, quoted only as a cross-check. 5e42ed2f is
b3c68af4's first parent, and differs from it only in `docs/dev/M7-WorkPackages.md` and
`docs/dev/ShipsNudge.md`. Its fast tier: 8,793 (8,779 passed, 13 skipped, 1 xfailed, 0 failed), the
same count of cases as the base here. Its slow tier: 534 passed, 14 skipped, 11 xfailed, 10 failed,
the ten known to fail on that machine. Its pace tier: 11 passed, 4 under truth 51's floor. The
cloud's base above is the comparison.

**On 2f3285c's tree:** `python tools/gen_ships.py <scratch>`, 18 of 18 byte for byte with
`data/ships/`; **`ruff check`** and **`ruff format --check`**, clean.

### Unsure, and for the lead

1. **"belay that" just after a manoeuvre is belayed** now finds what was given after it, before
   the work handed on, because the work keeps the manoeuvre's place. With nothing given after,
   it finds the work handed on, as before.
2. **The belay of the work handed on** names every yard it still shifts, so its line says them
   twice. On the xebec, 120 s after the tack is belayed with the mizen shifted: "Belayed shifting
   the mainsail and the foresail; the mainsail and the foresail in their gear, their yards not yet
   shifted round their masts." (old, "Belayed shifting the mainsail; ..."). It is true, and the
   work's one name, but long.

**Next:** `…/pkg-90-a1c` merged into `…/pkg-90-engine`, as before.

## A1d on A1c's hash (nudges 50 and 51): `…/pkg-90` merged, the lines resolved by hand (2026-11-22)

**The branch:** `…/pkg-90-a1d`, cut from A1d's hash **e2d6b926** (A1d's code, 8dce6372, and its
report, on A1c as first built, be2c90fd), with no A5-A6 and no A4. Allowed by the owner, who has
since given a standing allowance to push my own branches as needed.

**The merges:**
- **4fcd224**, parents e2d6b92 and **ee66c4a** (`…/pkg-90` then: A1c's hash with the five, A3's
  lists, the three A1a-A1b passes and the trunk to 7a1bd65e). Git finds one merge base, be2c90fd.
  It brings 96 commits. The code and data take 35 files, 1,477 lines in and 204 out, and the tests
  take 8, 2,755 in and 67 out. Five files conflicted; every other merged clean,
  `freesail/evolutions/runner.py` among them.
- **cde50e7**, parents 4fcd224 and **a13fb0f** (`…/pkg-90` now: ee66c4a with the trunk at
  25ccf840 merged in). It touches `docs/dev/M7-WorkPackages.md` and `docs/dev/ShipsNudge.md`
  alone, and merged clean.

**Which lines were resolved by hand** (4fcd224; both rules):
1. **`freesail/evolutions/scripts.py`, the tack's haul** (`TackScript`, at "let go and haul"):
   - Taken from the package: `draw = " Draw jib; trim aft the head sheets." if self._jibs() else
     ""`, `if self.heads and not draw:`, its comment `# the fore lateen alone drawn on the new
     board (package 90, nudge 48)` and `draw = f" Draw the {self._boom_names(self.heads)}; trim
     aft its sheet."`.
   - Dropped from A1d: its `draw = " Draw jib; trim aft the head sheets." if self.heads else ""`.
   - Kept from A1d, after them: `if left:`, `on = lateens_drawn_words(self.ship, left)` and `draw
     = f"{draw[:-1]}; {on}." if draw else f" {on[0].upper()}{on[1:]}."`.
   - Taken from the package, after those: its five comment lines from `# her head yards hauled in
     words only where she works her braces; ...`, then `hauled = braces_worked(self.ship)` and
     `if self.head and hauled:`.
   - Dropped from A1d: its `if self.head:`.

   So the fore lateen's own line comes first and A1d's lateens drawn over are joined to it, as the
   engine's merge at 0d639a6 has them, line for line.
2. **`freesail/evolutions/scripts.py`, the wear's "Wind aft."** (`WearScript`):
   - Taken from the package: its comment's line `# A2: "hauled out and braced up" before it,
     whatever she had); and where she` and the six after it (A2's second pass, `braces_worked` and
     the yards' class word), then `worked = braces_worked(self.ship)`, `swung =
     told_of(self.ship, self.head)`, `yards = f"{class_word(self.ship, swung)}yards"`, `squared =
     f"Squared the {yards}; shifted" if swung and worked else "Shifted"` and `braced = "; hauled
     out and braced up" if worked else ""`.
   - Dropped from A1d: `# A2: "hauled out and braced up" before it, whatever she had)`, `squared =
     "Squared the head yards; shifted" if self.head else "Shifted"`, and the three lines of
     `braced = (` ... `has_braced_yards(self.head, self.after)` ... `)`. `has_braced_yards` is gone
     since A2's second pass.
   - Kept from A1d: `over = self._lateens_over(new_lee, wind)  # package 90, A1d` and its note,
     `self.note(f"Wind aft. {squared} over the sheets{over}{braced}." + dipped)`.
   - Dropped from the package: its note without `{over}`.

   The engine's merge has the same lines.
3. **`tests/test_known_truths.py`**, one hunk at the file's end: A1d's section (truths 7-670 to
   7-672, 145 lines) against the package's (package 121's truths 7-710 to 7-716, 302 lines). Both
   kept whole, A1d's first, with two blank lines between. The file is byte for byte the
   engine's.
4. **`tests/test_lateen_whole.py`**, two hunks:
   - The import block: A1d's `from freesail.physics import sails as P` and the package's `from
     freesail.physics.sails import against_the_mast, compute_sail_forces`, both.
   - A1d's section ("Taken aback, and the bad hand, in a breeze (A1d)", 166 lines) against the
     package's three ("The second pass", "The third pass", "The five that ride A1c's hash", 1,171
     lines). Both kept whole, A1d's first, with two blank lines and the rule line between.

   The file is byte for byte the engine's (95a58e9's).
5. **`docs/dev/TuningNotes.md`**, one hunk: A1d's section (64 lines) against the package's three
   (the second pass, the third pass, the five; 114 lines). Both kept whole, A1d's first, with a
   blank line between. The lead's nudge-43 paragraph merged clean, once, in A1b's section. That
   makes 171 sections: the engine's file less its A5-A6 and A4 sections.
6. **This report**, three hunks. Git set A1d's section against the second pass's, the two sharing
   lines ("### The test sets run, with counts, and the base comparison", the guard set's
   sentence), so its hunks cut across both. The file is built from both sides whole: the common
   head (A2, A1a-A1b and A1c, 469 lines), then A1d's section as at e2d6b926, a blank, then the
   package's three sections as at ee66c4a. Every line of each side is kept in its order, and
   every line git merged clean is in it (both checked).

**Checked on 4fcd224, before the five:**
- No conflict marker anywhere. `ruff check` and `ruff format --check` are clean, 428 files.
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.
- The tree differs from the engine's (95a58e9) only in A5-A6's and A4's files: the pole's two
  files and its lines in the vocabulary and the runner, the towed boat's two files, `trim.py`,
  `verbs.py`, `integrate.py`, `sails.py`, `graph.py`, `boats.py`, `dealings.py`, `ports.py`,
  `scripts.py`'s A5-A6 and A4 lines, `test_agents.py`, and `test_boat_towed.py`,
  `test_pole_mast.py` and `test_yard_level.py`.
- The merge's own lens was cut at 48% by the machine's restart, with no failure to then. The
  lens below is run on the five's tree.

## A1d's hash (nudge 51): the five that ride it, the manoeuvre behind the work handed on, who has the work, her head, missed stays and the captain's road (2026-11-22)

**On `…/pkg-90-a1d` at cde50e7** (above). Every changed line is this pass's own, in the files
below. "Old" in the words below is cde50e7 (A1d on A1c's hash, before the five). **The base** of
the tiers' comparison is `…/pkg-90` at **a13fb0f**, its two tiers run here on its own worktree.

**Commits:** this pass is one commit, which carries this section with its code and the merge's
section above. **The fast and the slow tier run on that exact commit**, whose hash is the one
sent. Their results follow in a commit after it that touches this report alone.

**Files** (my row's; none widened):
- `freesail/evolutions/scripts.py`:
  - `ChangeLateenScript.holds`: the work handed on holds the ship;
  - `Script.lateen_way` and its three overrides (the tack, the wear, the box-haul), passed at the
    hand-on as `way`, read by `ChangeLateenScript._handed_awa` as each yard is set;
  - `TackScript.words`: her head where the line says she lies otherwise;
  - the tack's end: missed stays read there on a hull with a whole lateen, and
    `TackScript._miss_stays` saying her lateens where they lie.
- `freesail/evolutions/runner.py`: `start`, the waiting line said where work handed on keeps a
  whole-ship order waiting; `HANDED_ON` imported again.
- `freesail/orders/crew.py`: `all_hands_work` reads the work's own request.
- `tests/test_lateen_whole.py`: "The five that ride A1d's hash", 14 cases; no pin of before
  moved.
- `docs/dev/TuningNotes.md`: "Package 90, the five that ride A1d's hash".

**Form:** no class and no field is added: a method on `Script` with three overrides, a key in the
work handed on's params (read only where present, so that a save from before keeps the deck's
reading), and a parameter. So truth 7-606 and the checkpoint's list are not touched, and a save from
before loads. No ship file and no committed book moves (`python tools/gen_ships.py <scratch>`: 18 of
18 byte for byte). LF; `ruff check` and `ruff format --check` clean; no Python line over 100.
Nothing under `docs/agents/consent/`.

### The five, each with its proof

Each proof is in `tests/test_lateen_whole.py`, "The five that ride A1d's hash". Each fails when its
mend is undone: the session's scratch `n51/mutate51.py`, fourteen mutations, each failing its pins.

1. **No manoeuvre begins while a lateen of hers is in its gear in work handed on.** The work a
   belay hands on holds the ship, as the manoeuvre it stands for held her
   (`ChangeLateenScript.holds`). A manoeuvre ordered then waits behind it, and the runner says so
   at the order ("'Fill away' will follow 'shift the foresail', which the hands are still at.").
   A whole-ship order's line is the runner's started line, and this one would go unsaid
   (`Runner.start`, the lines for the lead below). It begins when the yard is set.

   The ground came from a second cause, found by the pin: the work handed on drew each yard's
   sheet for the wind on deck as it was set. The manoeuvre draws it close-hauled on the way it
   reckons with (`full_and_by_apparent`: the tack's way at "helm's a-lee", the wear's and the
   box-haul's before the helm, the fill away's her way as she has it). The manoeuvre now hands
   on that way (`Script.lateen_way`), and the work draws each yard as the manoeuvre would.

   Measured, seed 7, from hove to, the fore lateen on her weather side, `fill away`, `belay that`
   a second into the change, `fill away` again (`n51/r1e.py`), old and new:

   | | Plain: "Filled away", to windward in 30 min | Given again, old | Given again, new |
   |---|---|---|---|
   | The polacre | 187 s, 650.9 m | 190 s, 1,194.5 m (+543.6) | 190 s, 624.8 m (−26.1) |
   | The xebec | 185 s, 1,333.7 m | 187 s, 1,388.7 m (+55.0) | 186 s, 1,333.2 m (−0.5) |

   (The table's times are the yard's, drawing on the new side. "Filled away" itself is said at
   254 s plain and 265 s given again on the polacre, and at 196 and 198 s on the xebec; old, 49
   and 14 s.)

   Each yard handed on is now set with its sheet as the plain manoeuvre sets it, to the fourth
   place, in all six of nudge 48's cases. Old, the xebec's tack belayed set her three lateens'
   sheets at 0.0, 0.0 and 0.11 against 0.81, 0.80 and 0.83, and the fill away's at 0.997 against
   0.58. The ground, belayed as the change begins against plain, in half an hour: the xebec's tack
   −1,538.9 m old, −0.8 m new; the tartane's −108.2 and −0.8; the polacre's −88.8 and 0.0; her
   box-haul −95.1 and −35.9; the xebec's wear −832.3 and −1.4. The time until her lateens draw on
   the new side is nudge 48's in every case, to the second, but the xebec's wear belayed, 260 s
   against 259 (plain 258).

   Proofs: `test_a_fill_away_belayed_and_given_again_waits_behind_the_work_handed_on_and_gains_nothing`
   (the polacre and the xebec: "Filled away" no sooner, no more ground in half an hour, the
   waiting line said, the second begun after the yard is set), and
   `test_each_yard_handed_on_is_set_with_its_sheet_as_the_manoeuvre_sets_it` (the six).
2. **Who has the work, at `pipe down`.** `all_hands_work` (`orders/crew.py`) read the work's file
   (`change_lateen.yaml`'s `hands: all`) beside its own state. It now reads the work's own request
   wherever it has one, and the file only for work that has none (no company, a save from before
   it). With a crew a request is always made from the file's line (an all-hands line stays all
   hands whatever selector is given: `Runner._crew_line`), so no other work's answer moves. The
   work handed on carries the manoeuvre's request.
   - A fill away by twelve of the starboard watch, belayed: old "All hands are still at work
     (shifting the foresail); pipe down when it is done.", no hand called; new "Nobody is turned
     up; the starboard watch has the deck.", the line any ship gives while her watch has work in
     hand. The yard is shifted by them in its time.
   - A tack by all hands, belayed: refused as before, truly.

   Proof: `test_pipe_down_after_the_watchs_work_is_belayed_says_who_has_it`.
3. **Her head where she has not paid off to the course** (`TackScript.words`). Wherever the line
   says she lies otherwise than it claims (`not_paid_off`, said only on a hull with a whole
   lateen), the heading in it is her head and not the course. No probe end in play reaches it:
   the sweep of the three probes over eight courses each (`n51/r3.py`, 48 ends) has none, and the
   helm alone pays her off when her head sails are taken from her. So it is pinned at the tack's
   own door: a tack for E by N ended on its last trim lying 44° off the wind with a knot of
   sternway. Old "heading E by N (79°), but she has not paid off to it: she lies 44° off the
   wind ..."; new her head, NE (44°).

   Proof: `test_where_she_has_not_paid_off_to_the_course_the_line_gives_her_head`.
4. **Missed stays, not "Tacked".** On a hull with a whole lateen, a tack that ends with the wind
   on her old side by more than two points has not come round. It has missed stays, read as the
   hung tack's miss reads it ("she fell off on the old tack"), and is told so in the game's own
   words. The urgent line says her lateens where they lie as she misses. It is read where the
   tack ends, so that a tack fallen back that comes round before its end is a tack, as it was.
   The polacre probe, her foresail taken in, tacked, her mizen shifted in stays:
   - old "Tacked; braced up on the starboard tack, heading SW by S (217°), the mizen on the mast,
     but she has not paid off: she lies 143° off the wind with no way on her.";
   - new "Missed stays: she fell off on the old tack, the mizen on the mast. Up helm; square the
     yards; flatten in the head sheets; ease off the mizen sheet.", then "Squared the yards; she
     fell off on the starboard tack, to try again or to wear.".

   Over the polacre's 25 tacks of `n51/r4.py` (five winds, five sail plans), that end alone moves.
   Read at the moment she fell back instead, eight tacks at 20 and 24 knots that come round by
   their end were called missed (the mutation "read as she falls back").

   Proofs: `test_a_tack_that_falls_back_on_her_old_tack_has_missed_stays` and
   `test_a_tack_fallen_back_that_comes_round_before_its_end_is_a_tack` (the polacre at 20 knots:
   her head through, back on her old side 84° with two knots of sternway, round on the new tack by
   the end, "Tacked; braced up on the larboard tack, heading ENE (68°).", old and new).
5. **The captain's wiring, through his own road.** His work (`_work`) calls the lateens' work and
   reads the bow's line. Two tests drive `_work` itself, a sailing state set and his orders
   recorded:
   - the practice set as the wind falls under his book's 12 knots, and each yard shifted after a
     board of 30 minutes on the bad hand;
   - each lateen the bow's line named shifted.

   With either call taken out of `_work`, its test fails.

   Proofs: `test_the_rules_captains_own_work_sets_the_practice_and_shifts_the_yards_on_the_bad_hand`
   and `test_the_rules_captains_own_work_shifts_the_lateens_the_bow_left_on_their_masts`.

### Ruled, nothing to build

- Unsure 1 (`belay that` twice finds the newest order first) and unsure 2 (the long belay line of
  the work handed on) of A1c's hash: allowed as built.
- Listed, not asked: the places' "the tiller is" credited to Falconer's QUARTER-DECK, to be worded
  when that file is next touched (not in my row); "full and by" at 66° with sternway by the angle's
  rule, the trunk's.

### Measured: today's ships

- **A2's harness** (270 runs) on this tree: byte for byte as at a13fb0f (the base) and as at
  cde50e7 (old).
- **The wind-shift runs** (`n46/windshift.py`, 108): byte for byte as at a13fb0f and at cde50e7.
- Every changed road is read only on a hull that carries a whole lateen, or only by the work a
  belay hands on, which only a whole lateen's change makes, but one: `all_hands_work`, which reads
  for every other work the same flag as before (item 2).

### The test sets run, with counts, and the base comparison

**The tiered hash is 71febde**, this pass's commit itself. The commit after it, which writes these
results, touches this report alone.

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base, a13fb0f**, ran here the same way on its own
worktree, and 71febde on its own, after it. Compared test by test by the test's id, with the xdist
group's `@...` stripped.

| Run | a13fb0f (the base) | 71febde | Against the base |
|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,815: 8,806 passed, 8 skipped, 1 xfailed, 0 failed (1 h 37 min, the lens and the harness running beside it) | 8,840: 8,830 passed, 8 skipped, 1 xfailed, **1 failed** (57 min) | **Every one of the base's 8,815 the same outcome but one**, none gone; **25 new, all passed**: 22 in `tests/test_lateen_whole.py` (A1d's own 8 and the five's 14) and A1d's truths 7-670 to 7-672 in `tests/test_known_truths.py`. **The one**: `tests/test_harbour.py::test_in_the_browser_the_stations_are_one_table_and_a_planned_door_is_offered`, passed at the base, failed here: a race in the harbour's start, the base's code, below |
| **Slow tier whole**, `--slow -m "slow and not pace"` (a rule of force and the runner touched, so the tier whole) | 569: 558 passed, 11 xfailed, 0 failed (1 h 6 min) | 569: 558 passed, 11 xfailed, 0 failed (1 h 6 min) | **Every one of the 569 the same outcome**, none gone, none new |

**The one failure, read to its cause; not this hash's.** The stations table's first row for the
officer read `''` where the scenario gives the station to a model (`'a model'`). In
`freesail/ui/harbour.py` the game's start sets `self.started = True` under the harbour's lock, and
then reads and parses the scenario file for its plan (`self.plan(scenario)`) while it builds
`self.game`. `game_state` reads both under the driver's lock, not the harbour's. So a page's poll
that falls between them sees a game started with no plan, and the table is drawn without it;
under the tier's load the test read that first drawing. None of the files the test runs is
touched: `freesail/ui/`, `client/` and `tests/test_harbour.py` are a13fb0f's byte for byte.
- In the session's scratch, the window widened (a sleep of 1.5 s at `plan`'s head): the test
  fails twice in two, with the tier's very assertion. With the plan read before the lock and
  `self.started` set after `self.game`, the sleep still in place: passes twice in two. Restored.
- The test alone on 71febde: three passes in three; on a13fb0f: three in three.
  `tests/test_harbour.py` whole on 71febde: 42 passed (2 min 31 s).
- In the twelve fast tiers' junits kept in this session's scratch, this is its one failure.

Not mended: `freesail/ui/harbour.py` is in no row of mine. It is for the lead, below.

**The guard set of §10.2**, tallied from the two fast tiers' junits, every case the same outcome
at both: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed.
`tests/test_lateen_whole.py`: 205 at the base, 227 now (A1d's own 8 and the five's 14), all
passed.

**The lens of the touched files**, `-n 2`, on the working tree as committed (only this report and
the notes changed after it began): 3,603 passed, 1 skipped, 1 xfailed, 0 failed (1 h 5 min); the
fast tier above holds each of its files on the exact hash. Its 52 files (the session's scratch,
`n51/lens_files.txt`): `test_agent_api`, `test_agents`, `test_bellerophon`, `test_bilander`,
`test_captain`, `test_captain_rules`, `test_captain_trials`, `test_captains`, `test_catalogue`,
`test_checkpoint`, `test_company_moved`, `test_crew_orders`, `test_crews`, `test_damage_control`,
`test_driver`, `test_evolutions`, `test_found_on_the_way_85`, `test_gale`, `test_grammar_book`,
`test_hands`, `test_held_hulls`, `test_held_work`, `test_helm_kind`, `test_hull_lugger`,
`test_indefatigable`, `test_knowledge`, `test_known_truths`, `test_lateen`, `test_lateen_whole`,
`test_lug`, `test_lying_to`, `test_mends_109`, `test_mends_75`, `test_neufchatel`, `test_officer`,
`test_orders`, `test_practice`, `test_practice_orders`, `test_probes_90`, `test_readings`,
`test_replay`, `test_rig_geometry`, `test_rig_words`, `test_sails`, `test_schooner_mast`,
`test_settee`, `test_ships`, `test_standing`, `test_staying`, `test_strain`, `test_studding` and
`test_tackle_orders`.

**On 71febde's tree:** `python tools/gen_ships.py <scratch>`, 18 of 18 byte for byte with
`data/ships/`; **`ruff check`** and **`ruff format --check`**, clean.

### For the lead

1. **A whole-ship order made to wait is said by no line, on any ship.** `_ship_evolution`
   (`orders/verbs.py`) returns the runner's "'Tack ship' will follow '...', which the hands are
   still at." as `evolution.started`, and the world drops that kind's text, since the runner writes
   its own started line. So a manoeuvre ordered behind work that holds the ship (another
   manoeuvre, sending down the topgallant masts, furling all, the anchor's work) waits unsaid.
   `orders/fight.py` and `orders/damage.py` name theirs `evolution.queued`. Mended at its cause it
   would move today's ships' lines, so it is not built: a stop. The work handed on's wait is said
   by the runner itself (item 1), as A1d's take-in wait is.
2. **A tack missed on a hull with no whole lateen** is read as before: package 75's B3.4b names
   the tack she lies on ("Tacked; braced up on the starboard tack ..." of a ship fallen back), and
   no other ship's end moves.
3. **A race in the harbour's start** (`freesail/ui/harbour.py`, `start` and `game_state`; in no
   row of mine). `self.started` is set before `self.game` is built, and the scenario's plan is
   read between the two, while `game_state` reads both under the driver's lock and not the
   harbour's. A page's poll that falls between them draws the stations table with no plan. It
   failed `test_harbour`'s stations test once, in the fast tier on 71febde (above, with its proof).
   The mend, tried in scratch only: read the plan before the lock, and set `self.started` after
   `self.game`. As the lead's nudge 32 asked, said: a harbour test of the base failing once on a
   tree with my files.

**Next:** `…/pkg-90-a1d` merged into `…/pkg-90-engine`, as before; then A5 and A6 as their own
hash, on the lead's word.

## A5 and A6 as their own hash (nudge 52): `…/pkg-90` merged at 32c9448, the lines resolved by hand (2026-11-23)

**The merge:** **b40ffa3** on `…/pkg-90-a56`, parents **4ebd88a** (A5 and A6 as ruled, nudge 39,
on A1a-A1b as first built, no A4) and **32c9448** (`…/pkg-90`'s tip: A1d's hash and its tiers, on
A1c, the three A1a-A1b passes, A3's lists, A2 and the trunk), as the lead's nudge 52 asks. It
brings 104 commits; one merge base, e2d6b92. Over 4ebd88a the code, data and tests take 47 files,
4,650 lines in and 299 out, all the trunk's.

**What the merge adds over `…/pkg-90`** (non-docs, against 32c9448): A5 and A6's own lines and no
other, twelve files, 922 lines in and 50 out. Each file's added and removed lines are those of A5
and A6's own commits (e2d6b92 to 4ebd88a), line for line: `data/evolutions/furl_pole.yaml`,
`data/evolutions/take_in_pole.yaml`, `data/vocabulary.yaml`, `freesail/evolutions/runner.py`,
`freesail/evolutions/scripts.py`, `freesail/evolutions/trim.py`, `freesail/orders/verbs.py`,
`freesail/physics/sails.py`, `freesail/ship/graph.py`, `tests/test_agents.py`,
`tests/test_pole_mast.py` and `tests/test_yard_level.py`. The code merged clean, `runner.py`,
`scripts.py` and `vocabulary.yaml` among it. And the merged tree is the engine branch's
(`…/pkg-90-engine` at 64efd89, the same trunk with A5 and A6 and A4) less A4's own commit, 99d164c,
line for line in each of its eight files: no line of A4 here, and no other.

**Which lines were resolved by hand** (two files conflicted, both docs):
1. **This report.** Git matched the two sides' like sub-headings ("### The test sets run, with
   counts, and the base comparison", the guard set's lines) across different sections, and split
   them into three hunks, each side's sections interleaved. Resolved by section, against the
   merge base e2d6b92:
   - The four sections both sides have (A2, A1a and A1b, A1c and A1d, as first built): the same
     on each side, kept.
   - This branch's three, whole, in their order after A1d's: "Step A4: the boat in tow, stopped
     by the stop rule" (57 lines), "Steps A5 and A6" (213) and "Steps A5 and A6 as ruled (nudge
     39)" (197).
   - `…/pkg-90`'s five, whole, in their order after them: the second pass (223 lines), the third
     pass (188), A1c's hash (202), A1d on A1c's hash (82) and A1d's hash (228).
   - **One line added by hand:** a blank line between the last line of "Steps A5 and A6 as
     ruled" and the second pass's heading, which stood next to no section of this branch's.

   12 sections before this one. Against 4ebd88a the file loses no line; against 32c9448 none.
2. **`docs/dev/TuningNotes.md`**, one hunk. Git set this branch's A5 and A6 section, less its last
   two lines, against `…/pkg-90`'s four newest sections, matching the section's closing "Built by
   the engine track's builder; ..." with the same line closing A1d's five. Resolved by section:
   - "Package 90, A5 and A6: a yard's level from its order on its mast, and the pole mast's quick
     handing" (53 lines), whole, after A1d's section, where it stood.
   - Then `…/pkg-90`'s four, whole, in their order: the second pass (35 lines), the third pass
     (46), the five that ride A1c's hash (34) and the five that ride A1d's (30).
   - **One line added by hand:** a blank line before the second pass's heading.
   - Every other section as git merged it, clean: the trunk's edits to four sections of before
     (A0, A3, A2 and A1b, four lines out and their lines in), and its packages 120, 121 and
     121's follow-up, in their places.

   173 sections. Against 4ebd88a the file loses only the trunk's own four lines; against
   32c9448 none. Set beside git's own resolution of the hunk (ours, then theirs), the file
   differs only in A5 and A6's two closing lines kept with their section, and the blank.

**Checked on the merged tree:** no conflict marker is left anywhere; `ruff check` and `ruff
format --check` are clean, 430 files; no carriage return in the merge's diff; `python
tools/gen_ships.py <scratch>`, 18 of 18 byte for byte.

**The tiers are held until A1d's verdict**, as the lead asks. If A1d passes as it stands, the fast
and the slow tier whole run on b40ffa3, the merge's exact hash; the commits after it touch this
report alone. If it comes back with a list, its mend comes onto `…/pkg-90` first, it is merged in
here, and the mended hash is tiered.

### The smack, old beside new, against the trunk as it will stand

Measured as at nudge 39, each order from one settled world (`a5/play.py` in the session's
scratch: seed 7, 15 kn from 0°, her head 292.5° at 5 kn, plain sail and then the topsail set,
trimmed every two minutes after five, 1,320 s; in Carrick Road, 12 kn from 225°). **Old is the
trunk as it will stand**, `…/pkg-90` at 32c9448; **new is b40ffa3**. Times from the order.

| Order, her topsail set over plain sail | The trunk (32c9448) | A5 and A6 (b40ffa3) |
|---|---|---|
| `heave to` | "Hauled up the courses."; "Hauled flat aft the mainsail sheet; the foresail sheet to windward; helm a-lee."; "Hands to the sheets; heave to."; "Hove to on the starboard tack, under her fore-and-aft canvas, foresail sheet to windward, helm a-lee." at +214 s; at +600 s 47.3° off at 2.61 kn, the topsail hanging in the gear | no course hauled up; "...; braced the topsail aback; helm a-lee."; "Hands to the braces; heave to."; "Hove to on the starboard tack, topsail to the mast, helm a-lee." at +202 s; at +600 s 50.5° off at 2.87 kn, the topsail set and to the mast. In 30 kn the same two lines, at +386 s |
| `lie a-try` | refused: "Could not bring her to: She has no topsail to lie a-try under." (in 30 kn at +386 s) | "All hands! Shorten sail and bring her to under the topsail."; the jib taken in; "Lying a-try under the topsail and the foresail, helm a-lee." at +348 s; at +600 s 43.3° off at 1.06 kn. In 30 kn: lying a-try at +808 s, 49.3° off at 3.64 kn by +1,800 s |
| `back and fill` | "Hauled up the topsail."; "Backed the square sail; her way checked." and "Filled the square sail; she forereaches." at +50, +223, +401 and +574 s; at +600 s her head 297.3° at 4.14 kn | the topsail kept: "Backed the topsail; her way checked." and "Filled the topsail; she forereaches." at +50, +224, +400 and +573 s; at +600 s her head 229.0° at 3.27 kn |
| `take in the topsail`, `clew up the topsail` | "Hands to the topsail clewlines and buntlines."; "Clewed up the topsail." at +138 s; "Took in the topsail; hanging in the gear." at +204 s: 154 s from the start line | "Let go the topsail halyards; hands to the clewlines and buntlines."; "Lowered the topsail down onto the yard below and clewed it up there." and "Took in the topsail; lowered on the yard below, hanging in the gear." at +138 s: 88 s. **JUDGEMENT**, as ruled |
| `lower the topsail` | refused: "A course is hauled up, not lowered; say 'haul up the topsail' or 'take in the topsail'." | obeyed, as take in |
| `haul up the topsail` | obeyed, as take in | refused: "A topsail or light sail on a pole mast is lowered, not hauled up; say 'lower the topsail' or 'take in the topsail'." |
| `furl the topsail` | "Lay aloft and furl the topsail."; "Clewed up the topsail." at +150 s; "Furled the topsail." at +400 s: 350 s | "Lay out on the yard below and furl the topsail."; "Lowered the topsail down onto the yard below and clewed it up there." at +150 s; "Furled the topsail on the yard below." at +350 s: 300 s. **JUDGEMENT**, as ruled |
| `take in all sail` | the topsail as take in; the jib, last, hauled down at +412 s | the topsail as take in now; the jib at +350 s |
| `strike the topmasts` (and `send down the topgallant masts`, `fid the topmast`) | "She has no topmasts to strike; her masts are the main mast." | "... her masts are the main mast (a pole, the mast and topmast in one stick)." |
| **Every refusal that lists her masts** (`mast_inventory`; written out at the lead's nudge 56, ruled allowed): 62 phrases of the vocabulary, each given to her at sea. The twenty catharpin orders (`swifter in`, `ease`, `cast off` and `catharpin in`, eight of the fore mast and twelve of the mizzen); crossing the topgallant and royal yards (7) and sending them down (6); sending down or striking the topgallant masts (9) and swaying them up or fidding them (9); fidding or swaying up the topmasts (6) and striking or housing them (5) | "She has no fore mast; her masts are the main mast.", "She has no topgallant and royal yards to cross; her masts are the main mast." and their kin | every one the same but the note: "... her masts are the main mast (a pole, the mast and topmast in one stick)." |
| `heave to` in 30 kn, held 1,800 s (nudge 56, ruled allowed) | "Could not heave to: she would not lie to on the starboard tack; the helm amidships." at +986 s; 59.4° off at 7.48 kn at +1,200 s | "Could not heave to: she would not lie to on the starboard tack, the wind on the starboard bow; the topsail left aback and the helm amidships." at +986 s; "Jib taken aback." at +1,178 s; she pays off before the wind with it aback, 149.7° off at 6.02 kn at +1,200 s |
| `heave to`, then `tack ship` at +600 s with the topsail to the mast (nudge 56, ruled allowed) | tacked at +116 s of the order (+120 s after 300 s hove to) | "Missed stays: she hung in stays and would not come round. ..." at +541 s of the order (the same after 300 s and 900 s hove to). The cutter hove to with her topsail to the mast refuses that tack on both sides: "She has not way enough on her to stay: 2.0 kn through the water." |
| `back and fill`, held 1,800 s (nudge 56, ruled allowed) | "Backed and filled; lying to with the square sail to the mast." at +836 s; "She has filled and gathers way, the wind on the starboard bow: hove to no longer." at +948 s | "Backed and filled; lying to with the topsail to the mast." at +833 s; "She has fallen off, the wind on the starboard quarter, abaft the beam, and the helm and the sheets will not bring her to: hove to no longer." at +1,125 s |
| `get under way` (Carrick Road, her topsail furled by `come to an anchor`) | | **the trunk's, line for line and tick for tick**: her topsail furled through the cast; at +1,500 s her head 125.3° at 4.19 kn |
| `tack ship`, `wear ship`, `box haul`, `scud`, `shorten sail`, `set the topsail`, `trim sails`, `square the yards`, `brace sharp up on the larboard tack`, `come to an anchor` | | the trunk's, line for line and tick for tick |

**Set beside nudge 39's table** (A1d, 8dce637, beside A5 and A6 as ruled, e83f9e7; its two runs
kept in the scratch), A5 and A6's change to each order is the same, line for line and figure for
figure, **but one line, in both `heave to` runs: its start.** Then, at A1d and as ruled alike,
"Hands to the head braces; heave to.". Since then the trunk's words of a rig with no yards (A2's
re-mend) say "Hands to the sheets; heave to." of her read with no braced yard to back, and with
A5 and A6, her topsail read as a topsail and braced aback in the line before, "Hands to the
braces; heave to.": the trunk's cutter's line in the same harness, word for word. The rest moves
with the trunk alike on both sides (the box-haul's, the wear's and the get-under-way's words).

With her topsail never set, a player meets two changes: `lie a-try`'s refusal in other words, and
the topmasts' orders naming the pole.

**The three harness runs**, and the harness whole (A2's, `a2/harness.py` in the session's scratch:
each start settled once and each run from a copy of it, every event and a trace every 10 s), on
b40ffa3 beside the trunk's (its run on 71febde's tree for nudge 51, whose code is 32c9448's, file
for file): **270 runs, 269 the same in every tick, kind, trace and line.**

| Run | Seed and start | b40ffa3 against the trunk |
|---|---|---|
| `lie_a_try` | seed 7; at sea, 15 kn from 0°, her head 292.5° at 5 kn, plain sail braced sharp up on the starboard tack and trimmed every two minutes after five, 2,400 s; then `lie a-try`, 600 s | **a word**: the refusal alone, "Order not carried out ('lie a-try'): She has no topsail to lie a-try under." -> "Order not carried out ('lie a-try'): The topsail is not set; set it to lie a-try under it."; her trace the same, 60 rows |
| `anchor` | seed 7; Carrick Road, 10:00 on 10 June 1805, 12 kn from 225°, her head 335° at 3 kn, plain sail, 240 s; then `come to an anchor`, 2,400 s, and `get under way`, 1,500 s | **the same**, line for line and tick for tick: 34 events, 390 trace rows |
| `shoal_anchor` | seed 7; off Falmouth in three fathoms and a half, the same hour, 8 kn from 225°, her head 335° at 2 kn, plain sail and `set the lug`, 60 s; then `come to an anchor`, 2,400 s, and `get under way`, 1,500 s | **the same**, line for line and tick for tick: 33 events, 390 trace rows; "Under way on the starboard tack, under the mainsail and the jib; the best bower catted and fished; full and by." at +3,434 s |

The smack's twelve other runs, the cutter's fifteen and every other file's: the same in every
tick, kind, trace and line. The runs' files are kept in the scratch (`n52/`).

**For the coordinating session:** A5 and A6's hash is **b40ffa3** on `…/pkg-90-a56`, pushed, its
tiers held. The engine track's merge of A1d's hash (64efd89) is tiered meanwhile on its own
branch, as before.

## A5 and A6's hash tiered (nudges 53 and 54): `…/pkg-90` merged at efc5d779 and at 40561a76, the tiers on 3d4a468 (2026-11-23)

**The first merge (nudge 53):** **50bb169** on `…/pkg-90-a56`, parents **695331e** (A5 and A6's
hash, b40ffa3, and its section above) and **efc5d779** (`…/pkg-90`'s tip: 32c9448 with the trunk at
e3026cdb merged in, A1d merged there at 793adc04 by 71febde6), as nudge 53 and the coordinating
session ask. It brings four commits, the trunk's 71b89f8, 793adc0 and e3026cd and `…/pkg-90`'s
efc5d77, and two files, both docs: `docs/dev/M7-WorkPackages.md` (41 lines in, 1 out) and
`docs/dev/ShipsNudge.md` (1 in, 1 out), as the trunk has them. It merged clean: **no line resolved
by hand.** Its code, data, tests and tools are b40ffa3's byte for byte; and efc5d779's are 32c9448's
and 71febde's (`freesail/`, `data/`, `tests/` and `tools/` the same trees), so the base's tiers are
71febde's.

**Checked on the merged tree:** no conflict marker; `ruff check` and `ruff format --check` clean;
no carriage return in the merge's diff; `python tools/gen_ships.py <scratch>`, 18 of 18 byte for
byte.

**The second merge (nudge 54):** **3d4a468** on `…/pkg-90-a56`, parents **50bb169** and
**40561a76** (`…/pkg-90`'s tip: efc5d779 with the trunk at 8f9a4b45 merged in, the harbour's start
race mended there by the lead at ecfacf09), as the lead asks before the next hash is sent. It brings
three commits, the trunk's ecfacf0 and 8f9a4b4 and `…/pkg-90`'s 40561a7, and four files:
`freesail/ui/harbour.py` (13 lines in, 6 out), `tests/test_harbour.py` (72 in), and two docs,
`docs/dev/M7-WorkPackages.md` and `docs/dev/ShipsNudge.md`, as the trunk has them. It merged clean:
**no line resolved by hand.** Its code over 40561a76 is A5 and A6's own lines, the twelve files of
the section above, line for line as over efc5d779. Checked as the first: no conflict marker; ruff
clean; no carriage return; the generator 18 of 18 byte for byte.

**The tiered hash is 3d4a468**; the commit after it, which writes these results, touches this
report alone. The tiers of 50bb169, run before nudge 54 came, are kept below as measured: that
hash is not to be sent, but its run is the record of A5 and A6 beside efc5d779.

**The tiers of 50bb169** (nudge 53's merge; begun before nudge 54, and finished). All from the
tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`, on a
worktree of its own, each junit kept in the session's scratch, compared test by test by the
test's id (the xdist group's `@...` stripped) beside `…/pkg-90` at efc5d779: its tiers are those
of 71febde, the same code tree (in `…/pkg-90-a1d`'s section).

| Run | 50bb169 | Against efc5d779 (71febde's tiers) |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,902: 8,892 passed, 8 skipped, 1 xfailed, 1 failed (58 min 45 s) | efc5d779's 8,840 (8,830 passed, 8 skipped, 1 xfailed, 1 failed): **every one the same outcome**, none gone; **62 new, all passed**, A5 and A6's own: `tests/test_yard_level.py` 34 and `tests/test_pole_mast.py` 28. **The one failed, at both:** `tests/test_harbour.py::test_in_the_browser_the_stations_are_one_table_and_a_planned_door_is_offered`, with the same message at both ("At index 3 diff: '' != 'a model'": the planned door's cell empty), the harbour's race in its start (the lead's to mend, nudge 52), `freesail/ui/` and `client/` the same at both. Run alone on 50bb169 three times, in its own worktree: passed three times |
| **Slow tier whole**, `--slow -m "slow and not pace"` | 569: 558 passed, 11 xfailed, 0 failed (1 h 9 min 17 s) | efc5d779's 569 (558 passed, 11 xfailed): **every one the same outcome**, none gone, none new |

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at
efc5d779: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74;
`tests/test_lateen_whole.py` 227; all passed.

### The smack, and the three harness runs, against efc5d779

Run again on 50bb169 and on efc5d779 (each from its own worktree; `a5/play.py` and `a2/harness.py`
in the session's scratch, as in the section above):
- **The smack's table:** each side's run is byte for byte nudge 52's (32c9448's and b40ffa3's), so
  the table above stands as it is, old (efc5d779) beside new (50bb169), line for line and figure
  for figure.
- **The harness whole:** 270 runs, **269 the same in every tick, kind, trace and line**. The one:
  the smack's `lie_a_try`, in its refusal's words alone ("Order not carried out ('lie a-try'): She
  has no topsail to lie a-try under." -> "Order not carried out ('lie a-try'): The topsail is not
  set; set it to lie a-try under it."), her trace the same, 60 rows. Her `anchor` (34 events, 390
  trace rows) and `shoal_anchor` (33 events, 390 rows) the same, line for line and tick for tick.
  Each side's file is byte for byte its run for nudge 52 (new) and for nudge 51 (old: 71febde's).

### The tiers of 3d4a468 (nudge 54), test by test

Run as the first, on a worktree of its own, then `…/pkg-90` at 40561a76 tiered whole on another
(none of its tiers was to hand, and the harbour's file is reached through `freesail/ui/server.py`
by every page's test), each case set beside its outcome there and at 50bb169.

| Run | 3d4a468 | Against 40561a76 | Against 50bb169 |
|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,903: 8,894 passed, 8 skipped, 1 xfailed, 0 failed (54 min 27 s) | 40561a76's 8,841 (8,832 passed, 8 skipped, 1 xfailed, 0 failed; 59 min 42 s): **every one the same outcome**, none gone; **62 new, all passed**, A5 and A6's own: `tests/test_yard_level.py` 34 and `tests/test_pole_mast.py` 28. The harbour's browser test and the trunk's new one passed at both | 50bb169's 8,902 (8,892 passed, 8 skipped, 1 xfailed, 1 failed): **every one the same outcome but one**, none gone; **1 new, passed**, the trunk's: `tests/test_harbour.py::test_a_page_that_asks_while_a_game_starts_finds_one_whole_game`. **The one:** `tests/test_harbour.py::test_in_the_browser_the_stations_are_one_table_and_a_planned_door_is_offered`, failed at 50bb169, passed here: the harbour's start, as mended on the trunk at ecfacf09 |
| **Slow tier whole**, `--slow -m "slow and not pace"` | 569: 558 passed, 11 xfailed, 0 failed (1 h 5 min 51 s) | 40561a76's 569 (558 passed, 11 xfailed, 0 failed; 1 h 12 min 1 s): **every one the same outcome**, none gone, none new | 50bb169's 569 (558 passed, 11 xfailed): **every one the same outcome**, none gone, none new |

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at
40561a76 and at 50bb169: the byte test and the golden classing table 96 passed;
`tests/test_schooner_mast.py` 74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py`
21; the lugger's set 58; the settee's 75; the going-about set 261; `test_grammar_book` and truth
7-606 74; `tests/test_lateen_whole.py` 227; all passed.

**The smack's table and the three harness runs** are not run again: nudge 54's merge brings no
file they read (the harbour's two and two docs alone), and they are measured above against
efc5d779, whose code is 40561a76's but for `freesail/ui/harbour.py`. The coordinating session
allows it.

**For the coordinating session:** A5 and A6's hash is **3d4a468** on `…/pkg-90-a56`, pushed and
tiered; the commit after it touches this report alone. The lateen hulls' list rides A4's hash, as
the lead confirms: five of its seven are built on `…/pkg-90-lateen` (b3cd1eb, cut from 50bb169;
its section there), items 1 and 3's strain line stopped on `physics/strain.py` (the row's "not
touched", the mend proposed), item 7 asked. That branch takes the trunk before A4's hash is
reported, as nudge 54 asks, and its tiers run on that hash. **Next:** A4, on the lead's word.

## The lateen hulls' list (nudge 53): five built on their own branch, two for the lead (2026-11-23)

**The branch:** `…/pkg-90-lateen`, a branch of its own, as the coordinating session asked (its
name is mine; it was given none). Cut from **50bb169**, A5 and A6's hash, since the lead's "with
the engine's next hash" reads, to the coordinating session, as the hash after A5 and A6's (the
lead to confirm). Its code: **f0914df** (items 2, 3's bow line, 4 and 6) and **1767018** (item 5),
four files: `freesail/evolutions/runner.py`, `freesail/evolutions/scripts.py`,
`freesail/orders/navigation.py` and `tests/test_lateen_whole.py`, all in the plan's §7.1 row.

**Each item, old (50bb169) beside new**, the measures in `docs/dev/TuningNotes.md` ("Package 90, the
lateen hulls' list"):
1. **The dire warning missed: not built, a stop.** `physics/strain.py`'s rule; the row says
   "`physics/strain.py` is not touched". The mend proposed at its cause is in the notes.
2. **The take-in's wait: built.** Said at the order whatever work is before it, and when its turn
   comes if its lateen came aback meanwhile; once.
3. **The warnings that point the wrong way: the bow's line built**, "...; let fly its sheet, shift
   it or box her off" (JUDGEMENT on the words; why not "bear away", in the notes). **"If sail is
   not shortened" is `physics/strain.py`'s: a stop**, with item 1.
4. **Clearing for action: built.** It begins at once beside the work handed on, short ("Only 102
   hands to clear for action; the rest are shifting the foresail and the mizen."), the yards
   keeping their parties; `let go the anchor` there is answered as on the trunk. A manoeuvre still
   waits behind the yards.
5. **The aftermost lateen in stays: put back.** The reasoning for A1d's ease was its own judgement
   (that a whole lateen cannot be hauled over its mast as a boom is), with no source. Measured over
   1,536 probe tacks, the 22 that hang in stays, all the polacre's, all miss eased and all come
   round hauled, the yard well under its rating either way: it cost her stays for nothing.
   Hauled to windward again, and said as the mizen course and the settee are, with no boom.
   `docs/design/Design-Package90-Engine.md` §2.4.3a still says "eased": the design is not this
   row's to edit, and the notes and the code's comment say why it moved.
6. **Said twice: both built**, the polacre's foresail at "let go and haul" and the bow's two
   "when you will".
7. **Ratings: asked.** The probe files are stage 0's (`tests/rig_fixtures.py`); a hull's own file
   is the generator's and carries its ratings, and her gate is her builder's. What is the engine's
   part?

**The proofs** (`tests/test_lateen_whole.py`, "The lateen hulls' list (the lead's nudge 53)"):
eight new cases and two pins moved, each failing with its mend undone (run so, the code put back to
50bb169's or to A1d's ease, the tests as they are now):
- new: the take-in at the order, and when its turn comes; clearing for action; the anchor; the
  foresail named once; the bow's two lines; the polacre's hung tacks, seeds 24 in 12 kn and 36 in
  20 kn, coming round;
- moved, old beside new: the bow watch's line ("shift them when you will" -> "let fly their
  sheets, shift them or box her off"); the hang's (`..._eased_and_not_hauled_over` ->
  `..._hauled_to_windward_with_the_booms`, "the mizen sheet eased" -> "the mizen hauled over to
  windward").

**Checked on 1767018:** `ruff check` and `ruff format --check` clean; no carriage return in the
branch's diff; `python tools/gen_ships.py <scratch>`, 18 of 18 byte for byte (no ship file
touched); `tests/test_lateen_whole.py`, `test_probes_90.py`, `test_lateen.py` and
`test_rig_words.py`, 431 passed (the fast tier's set; `test_lateen_whole` 235 of them); and the
harness whole (A2's, every ship, 270 runs, `a2/harness.py` in the session's scratch) **byte for byte
50bb169's**: no committed ship's line, tick or trace moves.

**Not run:** the tiers of this branch, held until the lead says where these ride, A5 and A6's
taking the machine first.

## A4's hash (nudge 55): A4 brought onto `…/pkg-90` at d83a9b26 with the lateen hulls' list, items 1 and 3's strain line; the tiers held (2026-11-23)

**The branch:** `…/pkg-90-a4`, cut from **99d164c** (A4 alone on effbaed), as the lead's nudge 55 asks.

**The first merge:** **b288bb4**, parents 99d164c and **d83a9b26**. d83a9b26 is `…/pkg-90`'s tip: A5 and A6's hash 3d4a468 and its tiers (2447e57), on A1d, A1c, A1a-A1b, A2, A3 and the trunk at 8f9a4b45, with the design's §2.4.3a corrected to the build by the coordinating session. One merge base, effbaed.

Over d83a9b26 the merge adds A4's own lines and no other: nine files, 581 lines in and 40 out, each file's lines those of 99d164c over effbaed, line for line. They are `data/evolutions/lay_out_kedge.yaml`, `data/evolutions/send_boat.yaml`, `freesail/evolutions/scripts.py`, `freesail/physics/integrate.py`, `freesail/world/boats.py`, `freesail/world/dealings.py`, `freesail/world/ports.py`, `tests/test_boat_towed.py` and A4's section of `docs/dev/TuningNotes.md`. `scripts.py` merged clean.

**Which lines were resolved by hand** (one file conflicted): `docs/dev/TuningNotes.md`, one hunk.
- Git set A4's section ("Package 90, A4: the boat in tow", 49 lines, the end of 99d164c's file) against `…/pkg-90`'s four sections after A5 and A6's: the second pass (35 lines), the third pass (46), the five that ride A1c's hash (34) and the five that ride A1d's (30).
- Resolved by section: A4's section whole after A5 and A6's, where it stood (as on `…/pkg-90-engine`), then the four whole, in their order.
- **One line added by hand:** a blank line after A4's section, which closed its file and now stands before the second pass's heading.
- Against d83a9b26 the file loses no line. Against 99d164c it loses only the lines that the trunk and `…/pkg-90` changed in sections both sides had: A5 and A6's, as ruled, and the trunk's edits to A0, A3, A2 and A1b.

**The second merge:** **2853b46**, parents b288bb4 and **b3cd1eb** (`…/pkg-90-lateen`: the five of the lateen hulls' list, its notes and its section in this report, cut from 50bb169). One merge base, 50bb169. Over b288bb4 it adds that branch's own lines and no other, line for line: `freesail/evolutions/runner.py`, `freesail/evolutions/scripts.py`, `freesail/orders/navigation.py`, `tests/test_lateen_whole.py` and its notes' section. `scripts.py` and the notes merged clean.

**Which lines were resolved by hand:** this report, one hunk.
- Git set "A5 and A6's hash tiered (nudges 53 and 54)" (89 lines, `…/pkg-90`'s) against "The lateen hulls' list (nudge 53)" (55 lines, `…/pkg-90-lateen`'s).
- Resolved: each whole, the first then the second.
- **One line added by hand:** a blank line before the second's heading.
- Against either side the file loses no line.

**Checked on each merged tree:**
- no conflict marker;
- `ruff check` and `ruff format --check` clean;
- no carriage return in the merge's diff;
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.

The lens on 2853b46 passed, 394 tests: `test_lateen_whole`, `test_boat_towed`, `test_yard_level`, `test_pole_mast`, `test_strain`, `test_gale` and `test_tow`.

### Items 1 and 3: the strain's line, within the widening

**2df9bcc**, on the lead's widening: the warning's words and what the ten minutes' rate is counted against. No figure of load, strain or damage moves, and nothing of the rule moves on a ship with no whole lateen. Untouched:
- `LATEEN_ABACK_LOAD` and `LATEEN_BAD_HAND_LOAD`;
- every ratio, the wear, the chance and the certain failure;
- `WARNING_INTERVAL_S`;
- the plain words.

The change has three parts:
- **The cause is marked where A1d's factor is applied.** `physics/sails.py`, `lateen_pressed`, says what presses a whole lateen on its mast: aback, or the bad hand. `lateen_load_factor` reads its factor from it, the same figures. `_apply_loads` marks each spar of the lateen's chain under `strain.LATEEN_PRESSED`, beside its load, and `_reset_loads` clears the mark with the loads each substep. `physics/sails.py` is A1d's file. This is a mark, no figure; the notes I proposed at b3cd1eb put it there.
- **The rate is counted against the part and its cause.** In `physics/strain.py`, `_warn` keys a pressed part as `"<cause>:<part>"`, as the anchor keys its cable `"cable:<id>"`. A lateen coming aback or onto the bad hand is warned for as it comes, whatever was said before. Within a cause it is still one warning a part in ten minutes, and that warning stamps the part's own key too.
- **The words name the cause and the relief** (`_pressed_words`; JUDGEMENT on the words, in the anchor's form, the reliefs the lead's):
  - aback: "the mainsail aback against the mast: let fly its sheet, shift it or box her off";
  - on the bad hand: "the mainsail lying on the mast; she will carry it away: let fly its sheet or shift it", with no "box her off", since paying off leaves the yard on the bad hand.

The proofs are in `tests/test_lateen_whole.py`, "The strain's line", and each of the first two fails with the mend undone:
- **Item 1:** the xebec probe generator-rated in 57 kn, put on the bad hand. Each yard is warned "bending like a whip" at once, with its cause and relief, before any of them carries away.
- **Item 3:** the xebec in 25 kn, aback. "Main lateen yard working under the press of sail, the mainsail aback against the mast: let fly its sheet, shift it or box her off.", once in ten minutes.
- **The guard:** all eighteen files, plain sail struck by 50 kn. No part is ever marked, and every warning key is a part or a cable.

The file holds 255 cases.

| Item 1, the xebec probe in 57 kn, the lateens put on the bad hand at 600 s | Old (d83a9b26) | New (2df9bcc) |
|---|---|---|
| On the good hand | the mizzen mast and yard, the fore yard and the main yard "working under the press of sail." at 252, 442 and 451 s | the same |
| On the bad hand, before a loss | nothing | at 601 s, each "bending like a whip(s), the ... lying on the mast; she will carry it (them) away: let fly its sheet or shift it." (1.63 to 1.88) |
| The losses | the mizzen lateen yard at 756 s, the fore at 805 and the main at 1,156; the main's "bending like a whip; she will carry it away if sail is not shortened." at 1,051 | the same three at the same seconds; no other line |

**For the lead: within a cause, the older rule still stands.** A yard first warned "working" in its cause that rises past one and a half within the ten minutes is warned "bending like a whip" only when they are out, as any spar of a committed ship is in a rising wind. Measured: the xebec generator-rated on the bad hand in 52 kn, the main yard at 1.31 at +1 s and "bending like a whip" at +601, nothing lost between. In the bands nothing carried away unwarned, aback in 33, 35 and 37 kn or on the bad hand in 45, 49 and 52. Counting the rate against the dire step too, for pressed parts alone, would be inside the widening's words. It is not built, since the lead named the cause as the mend.

### The eighteen in gales, old beside new

Every committed ship file was run through 35 and 50 kn gusting (`n55/gales.py` in the session's scratch). Each is settled once:
- seed 7, 15 kn from the north with the scenario's gusts and shifts (0.3 and 0.3);
- her head 292.5 degrees at 5 kn;
- `set plain sail` and `brace sharp up on the starboard tack`, trimmed every two minutes after five, 900 s.

Each of ten runs is made from a copy of that world. The gale strikes (the mean raised at a stroke), the order is given, and the run lasts 900 s:
- `trim sails` close-hauled;
- `steer 270`, a reach;
- `steer 180`, running;
- `tack ship`;
- `wear ship`;
- `heave to`;
- caught aback, the wind eight points through her bow;
- `shorten sail`;
- `take in all sail`;
- `scud`.

Each run records:
- every event, with its second, kind, severity, subject, text and data;
- every part's load, condition, state and wreck each five seconds;
- her heading, speed and place each ten seconds.

**Old is `…/pkg-90` at d83a9b26** (the trunk as it will stand with A5 and A6); **new is 2df9bcc**, whose code is this hash's.

| | Old beside new |
|---|---|
| Runs | **360, the same in every event, tick, part sample and trace**; the two files byte for byte |
| Events | 6,101, every strain warning line and its tick among them |
| Strain warnings | 1,766 |
| Sails blown out | 417 |
| Spars carried away | 49 |
| Lines parted | 4 |
| Part samples | 64,800 |

**The harness catches a warning moved:** with `WARNING_INTERVAL_S` cut from 600 to 540 in a scratch tree, the cutter's, the brig's, the frigate's and the lugger's 80 runs gave 53 runs and 254 event rows different.

**Against the trunk itself**, beeb4149 (A5 and A6 staged at the gate, not yet on it), the same 360 runs are byte for byte the same file. The smack's topsail, A5 and A6's one mover, is not of her plain sail and is never set in these runs.

### Item 7: which truths re-rate the probes' yards, and why

Truths 7-670, 7-671 and 7-672 (`tests/test_known_truths.py`, `_a1d_probe`) re-rate the probes' lateen yards and masts by the generator's rule before they measure: a lower yard for its own sail, a lower mast for every sail on it (`tools/gen_ships.py`, `design_kn` in `DESIGN_WIND_KN["lower"]`). This hash's item 1 proof does the same (`_rated_by_the_generator`).

**Why:** the bands the lead ruled are figures for spars rated as every committed hull's are, by the generator: aback from about 28 and 35 kn, the bad hand from about 40 and 49. The probes were filed by hand at stage 0, for other ends. Filed against the generator's rule:
- below it: the tartane probe's great yard (44.1 kN against 59.5), the xebec's main yard (56.0 against 77.3), and the polacre's and the xebec's fore yards (56.0 against 61.1). So as filed the tartane's great yard strains aback from about 23 kn and risks it from about 29, as the lead's reader found.
- about it: the tartane's mizzen yard, 11.0 against 11.2.
- above it: the polacre's and the xebec's mizzen yards (56.0 against 21.7) and every lateen mast, the generator's rating 0.27 to 0.63 of the filed.

The probes stay as stage 0 wrote them. A hull's own file carries the generator's ratings, and her builder measures her own yards against A1d's bands at her gate.

### The five, read with this hash

As built on `…/pkg-90-lateen` and set out in its section above: items 2, 3's bow line, 4, 5 (put back) and 6. They come through both merges line for line, and their proofs pass on this hash. Items 1 and 3's strain line are above, and item 7 is said.

**The tiers are held until A5 and A6's verdict.** If A5 and A6 pass as they stand, the fast and the slow tier whole run on this hash, the commit that adds this section. Its code is 2df9bcc's; it adds this section and the notes' alone. If the verdict comes back with a list, its mend comes onto `…/pkg-90` first, is merged in here, and the mended hash is tiered.

**For the coordinating session:** A4's hash is this section's commit on `…/pkg-90-a4`, pushed, its tiers held. A4's own part is inert (no committed file tows a boat), and the eighteen's warnings in gales are the trunk's, as set out above.

## A5 and A6 held for two pins (nudge 56): the yard levels in a table and the smack's `lie a-try`, tests alone; what moves on her written out (2026-11-23)

**The commit:** on `…/pkg-90-a56` at 2447e57 (A5 and A6's hash 3d4a468 and its tiers), as the lead asks: one commit of tests alone, with this report and the notes. It touches no code, data or tools, only `tests/test_yard_level.py` and these two records. There is no merge, so no line was resolved by hand.

**Pin 1: every committed yard's level in a table.** `COMMITTED_YARD_LEVELS` in `tests/test_yard_level.py` lists the eighteen files' 91 braced yards, each at its level as the files stand. Files with no braced yard (the five boats and the lugger) have empty rows. It is held both ways, as stage 0's `KEY_CARRIERS` is:
- `test_the_table_of_yard_levels_has_a_row_for_every_committed_file_and_no_other`: a row for every file and no other, 91 yards.
- `test_each_committed_files_yards_are_the_yards_of_its_row_at_their_levels`, file by file: a yard in the file and not in its row fails, a row's yard the file does not have fails, and a level moved fails.

Measured, as the lead asks, with a change to a ship's file where both sides move together: the cutter's topgallant mast filed as a royal mast. The guard working the old formula again passes it, and the table fails it. (Her topgallant yard filed on the topmast is caught by both.)

**Pin 2: the smack's `lie a-try`** (ruling 3: she follows the cutter, no further). `test_the_smacks_lie_a_try_is_refused_furled_in_her_topsails_words_and_set_she_lies_a_try`:
- with her topsail furled, "Order not carried out ('lie a-try'): The topsail is not set; set it to lie a-try under it." at the order;
- with it set, "Lying a-try under the topsail and the foresail, helm a-lee." at +348 s, the table's figure.

Both start from `_smack_with_her_topsail` with 300 s more, the trims done. On the settle alone the order waits behind the trims: furled, it is refused at +65 s in the same words; set, she lies a-try at +648 s. The trunk's words put back in `LieATryScript.check` ("set it, close-reefed, to lie a-try under it.") fail it. The file holds 54 cases, all passed.

**What moves on her, written into the table** (the section "A5 and A6 as their own hash (nudge 52)", "The smack, old beside new", and the notes' A6 table). Each was measured, old `…/pkg-90` at 40561a76, whose code is the trunk's, against 3d4a468:
- **Every refusal that lists her masts** (`mast_inventory`). Every phrase of the vocabulary, 1,949, was given to her at sea: 62 answers list her masts, on both sides, and every one differs by the pole's note alone. Of the 62:
  - 20 are the catharpin orders, 8 of the fore mast and 12 of the mizzen;
  - 7 cross the topgallant and royal yards, and 6 send them down;
  - 9 send down or strike the topgallant masts, and 9 sway them up or fid them;
  - 6 fid or sway up the topmasts, and 5 strike or house them.
- **Heaving to in 30 kn, held 1,800 s.** It fails at +986 s on both sides. Now: "...; the topsail left aback and the helm amidships." She pays off before the wind with it aback, 149.7° off at 6.02 kn at +1,200 s, where the trunk's smack lay 59.4° off at 7.48 kn.
- **A tack ordered from hove to,** 600 s after `heave to`, the topsail to the mast. She misses stays at +541 s of the order (the same after 300 s and 900 s hove to), where the trunk's tacked at +116 s. The cutter, hove to so, refuses it on both sides: "She has not way enough on her to stay: 2.0 kn through the water."
- **Backing and filling, held 1,800 s.** She falls off to the quarter, "hove to no longer", at +1,125 s, where the trunk's filled at +948 s. The lead's reader gave +1,237 and +1,061 s: 112 and 113 s later, from a settle of their own.

**The tiers:** the fast tier whole runs on this commit's hash, test by test against 3d4a468's. The slow tier is the same code, since this commit adds tests and records alone, and is not run again. The results follow in a section of their own.

**For the coordinating session:** the pins' commit is this section's, on `…/pkg-90-a56`, pushed, its fast tier running. Next, A4's: the pole's marks glossed in the catalogue, this commit merged into `…/pkg-90-a4`, and A4's tiers on that exact hash.

## A4's hash at nudge 56: A5 and A6's pins merged, the pole's marks glossed; the tiers on this hash (2026-11-23)

**The lead's choice: A4 is left as built.** Within one cause the ten minutes' rule stands for a lateen's parts, as for every spar of every ship. Whether the dire step should be counted apart goes to the owner with the other older things. Nothing of the strain's line changes.

**The pole's marks, glossed** (**4e7ebe1**). The catalogue glosses `{sail}` alone, and `take_in_pole` and `furl_pole` (A6's) serve marks of their own, `{pole_lowered}`, `{pole_hanging}`, `{pole_furl_from}` and `{pole_furled_on}`.
- Each file's served notes now end with a paragraph that glosses them in the words the game fills them with (`scripts.pole_words`), the yard below's and the hounds': "In its words the game fills {pole_lowered} with "down onto the yard below" and {pole_hanging} with "lowered on the yard below"; where no square yard is crossed below it, with "down to the hounds" and "lowered to the hounds"." (`take_in_pole`; `furl_pole` the like for its three).
- The gloss is in the files' comments alone, A6's own files. No line of code moves, and nothing she does or says.
- `tests/test_pole_mast.py`, `test_the_pole_evolutions_marks_are_glossed_where_they_are_served`, ties each gloss to `POLE_WORDS_ON_THE_YARD_BELOW` and `POLE_WORDS_AT_THE_HOUNDS`. It fails with the gloss undone.
- The catalogue's readers (`test_agents`, `test_in_world`, `test_held_work`, `test_evolutions`): 331 passed, 1 xfailed.

**The merge:** **0e66d03**, parents 4e7ebe1 and **6dcfe40** (`…/pkg-90-a56`'s two pins on 2447e57, as the lead asks). One merge base, 2447e57. Over 4e7ebe1 it adds the pins' lines and no other, line for line:
- `tests/test_yard_level.py`;
- `docs/dev/TuningNotes.md`: the A6 table's rows and the pins' paragraph, in A5 and A6's section;
- this report's table rows (the section "A5 and A6 as their own hash (nudge 52)").

**Which lines were resolved by hand:** this report, one hunk.
- Git set this branch's two sections ("The lateen hulls' list (nudge 53)", 56 lines; "A4's hash (nudge 55)", 118) against `…/pkg-90-a56`'s "A5 and A6 held for two pins (nudge 56)" (29 lines).
- Resolved: each whole, this branch's first.
- **One line added by hand:** a blank line before the pins' heading.
- Against either side the file loses no line.

**Checked on the merged tree:**
- no conflict marker;
- `ruff check` and `ruff format --check` clean;
- no carriage return;
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.

The pinned files on it, `tests/test_yard_level.py` and `tests/test_pole_mast.py`: 83 passed.

**The tiers:** the fast and the slow tier whole run on this hash, the commit that adds this section, test by test against 3d4a468's (A5 and A6's hash, the code A4 stands on) and against the pins' 6dcfe40. As the lead says, they need not wait for the merge of A5 and A6. The results follow in a section of their own.

**For the coordinating session:** A4's hash is now this section's commit on `…/pkg-90-a4`, pushed; its tiers run after the pins' fast tier, so that the two do not share the machine.

## The pins' fast tier (nudge 56): 6dcfe40 test by test against 3d4a468 (2026-11-23)

**The tiered hash is 6dcfe40**, the pins' commit in the section above. The commit after it, which writes these results, touches this report alone. Run as before: from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`, on a worktree of its own, with the junit kept in the session's scratch and compared test by test by the test's id (the xdist group's `@...` stripped).

| Run | 6dcfe40 | Against 3d4a468 |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,923: 8,914 passed, 8 skipped, 1 xfailed, 0 failed (1 h 36 min 8 s) | 3d4a468's 8,903 (8,894 passed, 8 skipped, 1 xfailed, 0 failed; 54 min 27 s): **every one the same outcome**, none gone, the 8 skipped and the 1 xfailed the same cases at both. **20 new, all passed**, the pins' own, all in `tests/test_yard_level.py` (34 cases to 54): the table's row test 1, its file-by-file test 18 (one for each committed file), the smack's `lie a-try` 1 |
| **Slow tier** | not run again | The same code: this commit adds `tests/test_yard_level.py`'s cases, none marked slow, and two records alone. 3d4a468's slow tier stands as measured above (569: 558 passed, 11 xfailed, 0 failed) |

**The time:** the 20 new cases took 7.6 s between them. The 8,903 cases at both took 1.77 times as long summed (12,881 s at 3d4a468, 22,774 s here), and every group of cases over 20 s at 3d4a468 ran 1.16 to 3.34 times as long (median 1.74). The slowing is the machine's across the run, not this commit's: the session's machine restarted at 12:35 UTC, before this run began at 12:48.

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at 3d4a468: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; `tests/test_lateen_whole.py` 227; all passed.

**For the coordinating session:** the pins' commit is **6dcfe40** on `…/pkg-90-a56`, pushed and tiered; the commit after it touches this report alone. It is merged into `…/pkg-90-a4` at 0e66d03 (A4's hash ee1b856, its section there), and A4's fast and slow tiers run on ee1b856 now.

## A4's hash at nudge 57: the trunk merged through `…/pkg-90` at 7405febf, the lines resolved by hand; the tiers on ee1b856 stopped, restarted on this hash (2026-11-23)

**The merge:** **40a532e** on `…/pkg-90-a4`, parents **ee1b856** (A4's hash at nudge 56) and **7405febf** (`…/pkg-90`'s tip: b6c7b5b2 with the trunk at 9c95644b merged in, A5 and A6 merged there at 214e70db by 6dcfe408), as the lead asks before A4's hash. Two merge bases, 6dcfe40 and d83a9b26; the merge took 6dcfe40. Over ee1b856 it brings three docs and no other file:
- `docs/dev/M7-WorkPackages.md` (53 lines in, 1 out) and `docs/dev/ShipsNudge.md` (1 in, 1 out), as the trunk has them;
- this report's section "The pins' fast tier (nudge 56)" (07e5411's, 14 lines).

No code, data, test or tool moves: `freesail/`, `data/`, `tests/` and `tools/` are ee1b856's trees. And 7405febf's are d83a9b26's and the trunk 9c95644b's, the same trees, so the trunk's code is the old side of every measure below, as it was at nudge 55.

**Which lines were resolved by hand:** this report, one hunk.
- Git set this branch's "A4's hash at nudge 56" (32 lines) against `…/pkg-90`'s "The pins' fast tier (nudge 56)" (14 lines).
- Resolved by section, each whole: this branch's first, then the pins' tier.
- **One line added by hand:** a blank line before the pins' tier's heading.
- Against either side the file loses no line.

**Checked on the merged tree:**
- no conflict marker;
- `ruff check` and `ruff format --check` clean;
- no carriage return in the merge's diff;
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.

**The tiers on ee1b856, stopped.** They began at 14:25, after the pins' fast tier, and were stopped at 16:06 when nudge 57 came: the hash sent is the hash tiered. Kept as measured, not as the hash's record:
- **The fast tier finished:** 8,981, of which 8,971 passed, 8 skipped, 1 xfailed and **1 failed** (1 h 34 min 51 s).
  - Against 6dcfe40, every other case had the same outcome, and none was gone but the one renamed at nudge 53 (`..._eased_and_not_hauled_over` -> `..._hauled_to_windward_with_the_booms`, in the lateen hulls' list above).
  - There were 59 new cases, all passed: `tests/test_boat_towed.py` 29, `tests/test_lateen_whole.py` 29 and `tests/test_pole_mast.py` 1.
- **The one failed:** `tests/test_known_truths.py::test_truth_7_284_the_blend_adds_a_membership_and_not_a_gauge`, package 89's measure of the tide's pace. A fresh cell's work with the blocks must stay within a quarter of the eleven gauges' alone, the best of five timed runs each. It gave 0.0226 s against 0.0116. It passed at 3d4a468 and at 6dcfe40.
  - The modules it loads are `freesail/world/tide.py`, `geo.py`, `units.py` and `core/moon.py`. None of them moves between 6dcfe40 and ee1b856, nor does the data they read.
  - Run alone six times on each hash, alternating, while the slow tier held the machine: it **failed once on ee1b856** (0.0145 against 0.0116) and **three times on 6dcfe40** (0.0200 against 0.0125, 0.0149 against 0.0119, and 0.0174 against 0.0118).
  - It is a measure of time on a loaded machine. The machine has run 1.77 times slower since its restart at 12:35 (the pins' tier, above). The test is not touched.
- **The slow tier** was stopped six minutes in; no result is kept.

**The tiers on this hash** (40a532e), running from 16:08 on a worktree of their own, one after the other:
1. the fast tier whole, test by test against 3d4a468, 6dcfe40 and ee1b856;
2. the slow tier whole, against 3d4a468 (6dcfe40's slow tier is 3d4a468's, the same code);
3. the eighteen in gales on this hash, against the trunk's code (d83a9b26's run at nudge 55) and against beeb4149's;
4. truth 7-284 alone on the idle machine, ten times on this hash and ten on 6dcfe40, alternating.

The results follow in a section of their own, with the seven of the lateen hulls' list read item by item. The commits after 40a532e touch this report alone.

**For the coordinating session:** A4's hash is **40a532e** on `…/pkg-90-a4`, pushed, its tiers running.

## A4's hash tiered (nudge 57): 40a532e test by test against 3d4a468, 6dcfe40 and ee1b856; the eighteen in gales; the seven read item by item (2026-11-23)

**The tiered hash is 40a532e**, the merge in the section above. The commits after it, d2e2f0f and this one, touch this report alone. All runs are from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`, on a worktree of its own, one after the other. Each junit is kept in the session's scratch and compared test by test by the test's id (the xdist group's `@...` stripped).

| Run | 40a532e | Against 3d4a468 | Against 6dcfe40 | Against ee1b856 |
|---|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,981: 8,972 passed, 8 skipped, 1 xfailed, **0 failed** (1 h 30 min 23 s) | 8,903 (8,894 passed, 8 skipped, 1 xfailed): **every one the same outcome**; gone only the one renamed at nudge 53 (`..._eased_and_not_hauled_over`, now `..._hauled_to_windward_with_the_booms`); **79 new, all passed**: `tests/test_boat_towed.py` 29, `tests/test_lateen_whole.py` 29, `tests/test_yard_level.py` 20 (the pins), `tests/test_pole_mast.py` 1 | 8,923 (8,914 passed, 8 skipped, 1 xfailed): **every one the same outcome**; gone only the renamed one; **59 new, all passed**, the same less the pins | 8,981 (its run above, stopped before the slow): **every one the same outcome but one**, none gone, none new. **The one:** truth 7-284, failed there, passed here, the same code |
| **Slow tier whole**, `--slow -m "slow and not pace"` | 569: 558 passed, 11 xfailed, **0 failed** (1 h 36 min 18 s) | 569 (558 passed, 11 xfailed): **every one the same outcome**, none gone, none new | 6dcfe40's slow tier is 3d4a468's, the same code (the pins' section) | not run to its end |

The 8 skipped and the 1 xfailed of the fast tier, and the 11 xfailed of the slow, are the same cases at every hash.

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at 3d4a468 and 6dcfe40: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; `tests/test_lateen_whole.py` 255; all passed.

**Truth 7-284 alone, on the idle machine** after the tiers, ten times on this hash and ten on 6dcfe40, alternating (`pytest -q` on the one case, from each worktree):
- **40a532e: 10 of 10 passed.**
- **6dcfe40: 9 of 10 passed**, one failed: 0.0226 s against 0.0121 s.

It fails at times on the hash whose tier it passed, the same code. It is a measure of time on this machine, not of A4, and stands as package 89 wrote it.

### The eighteen in gales on this hash, old beside new

`n55/gales.py` in the session's scratch, run from this hash's tree, as set out in "A4's hash (nudge 55)": every committed ship file, 35 and 50 kn gusting, the ten orders, 900 s each.

The old side is **the trunk's code**. `freesail/`, `data/` and `tools/` are the same trees at d83a9b26, at `…/pkg-90`'s 7405febf and at the trunk's 9c95644b, so d83a9b26's run at nudge 55 is theirs.

| | Old beside new (40a532e) |
|---|---|
| Against the trunk's code (d83a9b26's run) | **360 runs, the same in every event, tick, part sample and trace; the two files byte for byte** |
| Against beeb4149's run (the trunk at nudge 55) | 360 the same |
| Against 2df9bcc's run (the strain's line, at nudge 55) | 360 the same |
| Events | 6,101, of 39 kinds, every strain warning line and its tick among them |
| Strain warnings | 1,766 |
| Sails blown out | 417 |
| Spars carried away | 49 |
| Lines parted | 4 |
| Part samples | 64,800 |

So on the eighteen files, every warning line and its tick is the trunk's. The strain's line moves only what a whole lateen presses, and no committed file carries one. The guard in `tests/test_lateen_whole.py` holds it for all eighteen, 18 passed on this hash.

### The seven of the lateen hulls' list, read item by item on this hash

Each item's proofs are in `tests/test_lateen_whole.py`, and every one passed in this hash's fast tier.

1. **The dire warning missed: mended** (2df9bcc, `physics/strain.py` within the lead's widening). A lateen coming aback or onto the bad hand is warned for as it comes, keyed by its cause.
   - Proof: `test_a_lateen_come_onto_the_bad_hand_in_a_gale_is_warned_for_at_once_before_it_goes`. The xebec, generator-rated, in 57 kn: each yard warned "bending like a whip" at once, before any carries away. It fails with the mend undone.
   - The guard: `test_no_part_of_a_committed_ship_is_pressed_by_a_lateen_and_her_warnings_keep_their_rule`, 18 passed; and the gales above.
   - Left as built, the lead's choice at nudge 56: within one cause the ten minutes' rule stands, as for every spar.
2. **The take-in's wait: built** (f0914df). It is said at the order whatever work is before it, and again when its turn comes if its lateen came aback meanwhile; once.
   - Proofs: `test_a_take_in_behind_other_work_says_the_lateens_wait_at_the_order` and `test_a_take_in_whose_lateen_comes_aback_behind_other_work_says_so_when_its_turn_comes`.
3. **The warnings that point the wrong way: both mended.**
   - The bow's line (f0914df): "...; let fly its sheet, shift it or box her off". Proof: `test_the_bows_line_names_what_eases_a_lateen_aback_and_says_when_you_will_once`.
   - The strain's words (2df9bcc): the cause and what eases it, in place of "if sail is not shortened" for a pressed lateen. Proof: `test_a_lateen_held_aback_is_warned_for_with_its_cause_and_what_eases_it`, the xebec in 25 kn, once in ten minutes.
4. **Clearing for action: built** (f0914df). It begins at once beside the work handed on, short of hands and said so, the yards keeping their parties; `let go the anchor` there is answered as on the trunk.
   - Proofs: `test_clearing_for_action_begins_at_once_beside_the_work_handed_on` and `test_letting_go_the_anchor_beside_the_work_handed_on_is_answered_as_on_the_trunk`.
5. **The aftermost lateen in stays: put back** (1767018), hauled to windward with the booms. The design's §2.4.3a was corrected to it on `…/pkg-90` at d83a9b26.
   - Proofs: `test_hung_in_stays_the_aftermost_lateen_is_hauled_to_windward_with_the_booms` (the pin moved, old beside new, at nudge 53) and `test_the_polacre_hung_in_stays_comes_round_with_her_mizen_hauled_to_windward`, seeds 24 and 36, 2 passed.
6. **Said twice: both mended** (f0914df). The polacre's foresail is named once at "let go and haul", and the bow's "when you will" is said once.
   - Proofs: `test_with_jibs_or_none_the_foresail_drawn_with_the_head_sheets_is_named_once` and the bow's line in 3.
7. **Ratings: said, no line moves** ("A4's hash (nudge 55)", item 7). Truths 7-670, 7-671 and 7-672 re-rate the probes' lateen spars by the generator's rule before they measure, since the lead's bands are for spars rated as every committed hull's are. The probes stay as stage 0 filed them, and a hull's builder measures her own yards against A1d's bands at her gate.
   - The three truths: 3 passed.

**For the coordinating session:** A4's hash is **40a532e** on `…/pkg-90-a4`, pushed and tiered whole: the fast tier and the slow, 0 failed. The commits after it touch this report alone. Every warning line and tick of the eighteen in gales is the trunk's, and the seven are read above. **Next:** the Diana, then the tartane, whose gate begins with the lateen hulls' list, on the lead's word.

## A4's one commit (nudge 60): the boat entries' marks glossed where they are served, pinned against the game's words; what is served, old beside new (2026-11-23)

**The commit:** on `…/pkg-90-a4` at 329648e (A4's hash 40a532e and its two report commits), as the lead asks, and nothing else in it: two entries' served notes, one test, and this section. No line of code moves, and nothing she does or says. There is no merge, so no line was resolved by hand.

**The gloss.** `send_boat` and `lay_out_kedge` serve `{boat_out}`, and `send_boat` also `{boat_back}`, where the trunk's served the words. Each entry's served notes now end with a line as the two pole entries carry, in the words the game fills them with:
- `send_boat`: "In its words the game fills {boat_out} with "Hoist out {boat}" and {boat_back} with "hoisted in"; for a boat towed astern, with "Haul {boat} up alongside" and "veered astern on her painter again"."
- `lay_out_kedge`: "In its words the game fills {boat_out} with "Hoist out {boat}"; for a boat towed astern, with "Haul {boat} up alongside"." It serves `{boat_out}` alone; its line when done names the boat by `{boat}`, as on the trunk.

**Where the game takes the words:** `freesail/evolutions/scripts.py`, `_boat_out_words` for both entries' `{boat_out}`, and `SendBoatScript.words` for `{boat_back}`. These are the words `world/boats.py` and `world/dealings.py` (`_back_aboard`) give the boat's own lines. `{boat}` and `{boat_cap}`, the boat's name, were served on the trunk and are as they were.

**The pin:** `tests/test_boat_towed.py`, `test_the_boats_evolutions_marks_are_glossed_in_the_words_the_game_fills_them_with`, one case for each entry.
- Every mark of the entry's logged lines but the boat's name is glossed, of a boat on deck and of one towed astern.
- On the tartane probe, with her boat on deck and with it towed, at anchor in Carrick Road, the order is given, and the running script's own words are the gloss's.
- The line logged at the start is the entry's, filled with them.

It was tried against six faults, and each fails it:
- the gloss's "hoisted in" changed;
- the kedge's towed words in the gloss changed;
- the gloss taken out of `send_boat`;
- the game's "Haul {boat} up alongside" changed (both cases fail);
- the game's "veered astern on her painter again" changed;
- the kedge's start line put back to the trunk's "Hoist out {boat}".

The catalogue's readers (`test_agents`, `test_in_world`, `test_held_work`, `test_evolutions`), with `test_boat_towed`, `test_pole_mast` and `test_ports`: 441 passed, 1 xfailed.

**What is served, old beside new: every entry of the catalogue.** The trunk at 27e97e4 (its code 9c95644b's) beside this commit, each of the 113 entries' served text (`agents/tools._evolution_text`) compared whole: **109 the same, word for word. Four differ**, all of A4's hash:

| Entry | The trunk serves | This hash serves |
|---|---|---|
| `take_in_pole` (A6's) | `{pole_lowered}` and `{pole_hanging}`, not glossed | the same, and the gloss line (4e7ebe1, nudge 56): "...fills {pole_lowered} with "down onto the yard below" and {pole_hanging} with "lowered on the yard below"; where no square yard is crossed below it, with "down to the hounds" and "lowered to the hounds"." |
| `furl_pole` (A6's) | `{pole_lowered}`, `{pole_furl_from}` and `{pole_furled_on}`, not glossed | the same, and the gloss line (4e7ebe1), the yard below's three and the hounds' three |
| `send_boat` | at the start "Away {boat}'s crew! Hoist out {boat}."; when done "{boat_cap} hoisted in."; timing `hoist_out_s` 300, `hoist_in_s` 300, `boat_pace_kn` 4 | at the start "Away {boat}'s crew! {boat_out}."; when done "{boat_cap} {boat_back}."; the towed boat's paragraph; timing with `haul_alongside_s` 60 and `veer_astern_s` 60 beside the rest; and the gloss line (this commit) |
| `lay_out_kedge` | at the start "Hoist out {boat}; the kedge and a hawser into her."; timing `hoist_out_s`, `sling_s`, `boat_pace_kn`, `hoist_in_s`, `hawser_fraction` | at the start "{boat_out}; the kedge and a hawser into her."; the towed boat's paragraph; timing with `haul_alongside_s` 60 and `veer_astern_s` 60; and the gloss line (this commit) |

On every committed ship no boat is towed, so the game fills `{boat_out}` with "Hoist out {boat}" and `{boat_back}` with "hoisted in". Her logged lines are the trunk's word for word, as the lead's reader found in 130 runs of the boats' work. The gloss tells a seat so where it is served.

**Checked on this commit:**
- `ruff check` and `ruff format --check` clean;
- no line over 100 characters;
- no carriage return;
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte (no ship file touched).

**The tiers:** the fast tier whole runs on this commit's hash, test by test against 40a532e's. The results follow in a section of their own; the commit after this one touches the report alone.

**For the coordinating session:** A4's one commit is this section's, on `…/pkg-90-a4`, pushed, its fast tier running. Next, the lateen hulls' list as it stands (nudge 60's eight), on `…/pkg-90-lateen` once A4 is on `…/pkg-90`.

## A4's one commit tiered (nudge 60): 0040fda's fast tier whole, test by test against 40a532e (2026-11-23)

**The tiered hash is 0040fda**, the one commit in the section above. The commit after it, which writes these results, touches this report alone. Run as before: from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`, on a worktree of its own, with the junit kept in the session's scratch and compared test by test by the test's id (the xdist group's `@...` stripped).

| Run | 0040fda | Against 40a532e |
|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,983: 8,974 passed, 8 skipped, 1 xfailed, **0 failed** (1 h 13 min 35 s) | 40a532e's 8,981 (8,972 passed, 8 skipped, 1 xfailed): **every one the same outcome**, none gone; **2 new, both passed**, the pin's two cases in `tests/test_boat_towed.py` (`send_boat` and `lay_out_kedge`). The 8 skipped and the 1 xfailed are the same cases at both |

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at 40a532e: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; `tests/test_lateen_whole.py` 255; all passed.

The slow tier is not asked for this commit and was not run. It is 40a532e's code with two entries' comments and one test added, and 40a532e's slow tier stands (569: 558 passed, 11 xfailed, 0 failed).

**For the coordinating session:** A4's one commit is **0040fda** on `…/pkg-90-a4`, pushed, and its fast tier is whole with 0 failed. The commit after it touches this report alone. **Next:** the lateen hulls' list as it stands (nudge 60's eight), on `…/pkg-90-lateen` once A4 is on `…/pkg-90`.

## The lateen hulls' list as it stands (nudge 60): the eight on `…/pkg-90-lateen`, each with its proof; nothing moves on today's ships (2026-11-24)

**The branch:** `…/pkg-90-lateen`, brought to `…/pkg-90` at **3d3841f2** (A4 merged there) first, as the coordinating session asks. b3cd1eb, the branch's tip, is in 3d3841f2's history, so it came as a fast-forward: **no merge commit and no line resolved by hand.** The work is four commits of code and tests and this one of the notes and report:
- **cd4c76b**, item 7;
- **002fb54**, items 1 and 3;
- **13330c7**, items 2 and 6;
- **ac7ed13**, item 8.

They touch:
- `freesail/physics/strain.py` and `sails.py` (the strain's line, the widened words and what the rate is counted against);
- `freesail/orders/navigation.py`;
- `freesail/evolutions/runner.py` and `scripts.py`;
- `freesail/world/boats.py`, `dealings.py` and `ports.py`, and `freesail/physics/integrate.py` (a comment only);
- `tests/test_lateen_whole.py`, `tests/test_boat_towed.py` and `tests/test_known_truths.py` (7-672).

**The equations are read, not changed:** no load, ratio, factor, rate, timing or drag figure moves. The measures, old beside new, are in `docs/dev/TuningNotes.md`, "Package 90, the lateen hulls' list as it stands: the eight of nudge 60".

Each item and its proof (every pin fails with its mend undone, run so):
1. **The dire warning missed: mended for a cause that ends and comes again.** A part pressed by a cause it was not pressed by at the last tick has that cause's ten minutes begun afresh (`strain._causes_come`).
   - Proof: `test_a_cause_that_ends_and_comes_again_within_ten_minutes_is_warned_for_as_it_comes`, the xebec in 40 kn. She is aback and warned at 601 s, the cause ends, and she is aback again at 701. Old was silent at 701 at 1.15; new warns at 701.
   - **The mast's key with two lateens: mended.** It is marked for the lateen that pulls hardest, not the last in the ship's order of sails. Proof: `test_a_spar_two_lateens_press_is_warned_for_the_one_that_pulls_it_hardest`.
   - **Seen and left, as the lead chose at nudge 56:** within one cause the ten minutes' rule stands. The reader's run, reproduced as nearly as written, kept the xebec's mizzen yard on the bad hand from 613 s to its loss at 1,081 s. It was warned "working" at 1.05 and carried away at 1.86 with no second line, on both sides alike.
2. **The three waits: said.**
   - A furl of a set lateen held aback now waits as a take-in does, since it brails it up first (`LATEEN_BRAILED_FIRST_VERBS`), and says so at the order.
   - A furl behind `trim sails` says it there too.
   - An order to a whole lateen waiting behind other work says what it follows, at the order.
   - Proofs: `test_a_furl_of_a_lateen_held_aback_waits_as_a_take_in_does_and_says_so`, `test_a_furl_behind_trim_sails_of_a_lateen_held_aback_says_its_wait_at_the_order` and `test_an_order_to_a_lateen_waiting_behind_other_work_says_so_at_the_order`.
   - One pin moved, old beside new: nudge 53's take-in behind `trim sails` now says the "will follow" line at the order as well.
3. **The advice: only orders she will take that are measured to bring the load down** (`strain.pressed_reliefs`, said by the strain's line and by the bow's). The three probes were generator-rated, held aback in 30 and 40 kn and on the bad hand in 40 and 50, and each order was set against the same run with no order.
   - **Named:**
     - shift it, both causes: under half the load within a second;
     - box her off, held aback, where she has head yards to brace abox and is not hove to: the polacre and the tartane, under half within a second;
     - take it in, on the bad hand: under half 152 to 170 s on, where with no order it never falls.
   - **Not named:**
     - let fly its sheet: it raises the load on the bad hand (the xebec in 40 kn, her main yard 0.93 to 1.11), and held aback it eases it no more than doing nothing;
     - box her off on the bad hand: the polacre's yards then rise past their load at the order, to 1.28 to 2.10;
     - a take-in held aback;
     - ease off, and the helm's orders.
   - The words, old beside new: aback "let fly its sheet, shift it or box her off" became "shift it" (the xebec, which refuses the box) or "shift it or box her off"; on the bad hand "let fly its sheet or shift it" became "shift it or take it in".
   - Proofs: `test_held_aback_a_lateen_is_eased_by_each_order_its_warning_names` (four cases), `test_on_the_bad_hand_a_lateen_is_eased_by_each_order_its_warning_names` (two) and `test_on_the_bad_hand_the_sheet_let_fly_raises_the_load_and_is_not_named`. Each gives the order and reads the load falling, or rising.
   - Four pins of the old words moved, old beside new.
   - **"0.86 to 0.08"** is nudge 53's own figure ("my reader measured the yard from 0.86 of its rating to 0.08 at once"), which the bow's line's comment quoted. This report never gave a case for it. The nearest measured here is the xebec in 30 kn aback, her fore yard at 0.86: its sheet let fly, 0.52 at 30 s and 0.41 at a minute, as with no order by then; shifted, under half within the second. The comment now gives the measured reliefs.
4. **Clearing for action:** as mended at nudge 53, untouched.
5. **The aftermost lateen in stays, owed in measurement:** 300 tacks a side close-hauled, old the trunk's tip b49ed33d (A1d's ease), new this branch.
   - The polacre in 20 kn: 4 hang, old all miss stays, new all come round.
   - The polacre in 25 kn: 116 hang, old all miss, new all come round.
   - The xebec and the tartane in 12, 16, 20 and 25 kn: never hang, 2,400 tacks the same tick for tick.
   - **None lost against the trunk at any wind**, and the greatest lateen loads are the same both sides.
6. **The haul line names every sail hauled or left, once.** The polacre with her jibs set, `tack ship and leave the lateens`: "Draw jib; trim aft the head sheets and the foresail sheet; draw the mizen on the mast.", where before the foresail was drawn and not named. The pin that held it so moved, old beside new. The lugger's line is as it was.
7. **Truth 7-672's upper band:** under 0.15 of the rating. Measured at the bad-hand factor 2.5, 3.0 and 4.0, the tartane's great yard reaches 0.121, 0.145 and 0.193, so 4.0 now fails where a fifth alone passed it.
8. **The boat in tow:**
   - A boat towed past her own hull speed is said to sheer and ship water, once as she passes it, and her reading says so: "The boat towing too fast for her, sheering about astern on her painter and shipping water; shorten sail to ease her." (JUDGEMENT on the words).
   - The drag figure past hull speed is marked as having no ground, and not changed.
   - Now held by cases: no drag making sternway, and the two timings against `ports.BOAT_HAUL_ALONGSIDE_S` and `BOAT_VEER_ASTERN_S`.
   - Run: clearing for action and anchoring with her boat towed, each as with it on deck.
   - Proofs: `test_a_boat_towed_faster_than_her_hull_speed_is_said_to_sheer_and_ship_water`, `test_making_sternway_her_boat_in_tow_drags_nothing` (two) and `test_a_towed_boats_two_timings_are_the_ports_figures` (two).

**Nothing moves on today's ships:** no committed file has a whole lateen or a towed boat, and every change is keyed to one or the other. Measured before this commit, on 002fb54 to ac7ed13's code:
- the eighteen in gales on items 1 and 3, byte for byte the trunk's run (360 runs, 6,101 events, 1,766 strain warnings);
- A2's harness, 270 runs over every committed ship, byte for byte 0040fda's (3d3841f2's code).

Both run again on this commit's hash with its tiers.

**For the lead:**
- Within one cause, the dire step is still not counted apart (item 1). It is the lead's choice of nudge 56, and is seen again in the reader's run.
- `docs/design/Design-Package90-Engine.md` still quotes the strain's old words ("let fly its sheet or shift it", "let fly its sheet, shift it or box her off"). The design is not this row's to edit.
- Two older things on the trunk:
  - the clear-for-action line says "The boats are out and towing astern" of a boat at the booms, nothing moving her;
  - an order to any other sail waiting behind work is said in its reply alone, never in the log. It is mended here for whole lateens only, so that no committed ship's line moves.

**Checked on this commit:**
- `ruff check` and `ruff format --check` clean;
- no carriage return;
- no new line over 100 characters;
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.

**The tiers:** the fast and the slow tier whole run on this commit's hash, test by test against 3d3841f2. Its code is 0040fda's: the fast tier is 0040fda's run, and the slow is 40a532e's, which runs the same slow tests on the same code but two entries' comments. The eighteen in gales and A2's harness run again on this hash. The results follow in a section of their own; the commit after this one touches this report alone.

**For the coordinating session:** the eight are this section's commit on `…/pkg-90-lateen`, pushed, its tiers running.

## The lateen hulls' list, its second pass (nudge 76): on `…/pkg-90-lateen2`, items 1 to 4 built and pinned, item 5 waiting for package 127 (2026-11-24)

**The branch:** `…/pkg-90-lateen2`, cut from `…/pkg-90` at **b35aaaba** (the list of eight merged on the trunk at da356b76, by 111b1b5), as the coordinating session asks.
- `…/pkg-90` is still at b35aaaba, and the trunk at 41d1d1bc. Packages 125 to 127 have not landed, so there is nothing more to merge before this hash, and **no line was resolved by hand.**
- The work is one commit of code and tests, **5a467fe**, and this one of the notes and report.
- Its files:
  - `freesail/physics/strain.py` (the widened words);
  - `freesail/orders/navigation.py` (the bow's line);
  - `freesail/combat/hits.py` (the engine track's file, A3's);
  - `freesail/world/boats.py` and `dealings.py`;
  - `tests/test_lateen_whole.py` and `tests/test_boat_towed.py`.

**The equations are read, not changed:** no load, ratio, factor, rate, timing or draw moves. The measures, old beside new, are in `docs/dev/TuningNotes.md`, "Package 90, the lateen hulls' list, its second pass".

1. **"Take it in" is not named on the bad hand:** it eases nothing for two minutes and more (the xebec in 50 kn, her main yard at 1.57 to 1.60 for 169 s). The dire line names only what eases at once.
   - Old "shift it or take it in"; new "shift the mainsail".
   - Proof: `test_on_the_bad_hand_a_lateen_is_eased_at_once_only_by_the_order_its_warning_names`. The shift eases at once and is named; the take-in holds the yard over 1.5 for two minutes and is not named. It is the old pin moved, old beside new.
2. **The reliefs are orders she takes word for word.** They were "shift it" and "shift them", which she refused ("There is no such part as the them"). Now they are "shift the mainsail", "shift the mizen or box her off", and in the bow's line "shift the foresail and the mizen and the mainsail".
   - **A lateen warned while its own shift waits for hands** is told so, and what the hands are at: "...: its shift waits its turn, the hands shifting the mainsail.", the xebec's mizen at 1.65 behind her foresail's and mainsail's shifts. Before, "shift it or take it in".
   - Proof: `test_a_lateen_whose_shift_waits_for_hands_is_told_so_not_to_shift_it`. The old words' pins moved, old beside new: five tests, eight cases (the bow watch's line, the bow's line, the gale's bad hand, the breeze's aback, and the four reliefs aback).
3. **A boat towed astern stove by a shot is cut adrift,** in tow no longer, her drag gone, and her reading says so: "The boat is stove by a shot as she tows astern; she fills, and her painter is cut.". The draw is as it was, and a boat on the booms is stove there as before.
   - Proof: `test_a_boat_towed_astern_stove_by_a_shot_is_cut_adrift_not_on_the_booms`, through `hits._deck_hit` itself.
4. **The three pins:**
   - the hunt scenario (aback to the bad hand to aback, never without a cause between: warned at 601, 611 and 641 s), `test_a_cause_that_turns_to_another_and_back_is_warned_for_each_time_it_comes`;
   - boxing off not offered hove to, `test_hove_to_she_is_not_offered_boxing_off`;
   - the towed boat's line at its two figures and her hull speed, `test_a_boat_towed_too_fast_is_said_at_her_hull_speed_and_again_only_under_nine_tenths`.
5. **The dire step within one cause waits for package 127's rule,** as the lead asks; not built here. It does not hold items 1 to 4.

**Each pin fails with its mend undone**, run so, seven faults:
- the reset only from no cause;
- the box offered hove to;
- the re-arming at eight tenths;
- the stove words as before;
- the stove boat kept in tow;
- the waiting shift unsaid;
- the take-in named again.

The lens (`test_lateen_whole`, `test_boat_towed`, `test_knowledge`, `test_strain`, the combat and action files, `test_probes_90`, `test_rig_words`, `test_settee`, `test_evolutions`, `test_lateen`): 727 passed.

**For the lead, beyond this row:**
- "shift the lateens" wants a `lateens` group in a lateen hull's own file, as "the jibs" is (`groups:`, the generator's).
- A list with commas is the order parser's, for every order on every ship.
- The runner's in-turn line, "Shifting the fore lateen, main lateen and mizzen lateen: not hands enough for all at once; the watch takes the sails in turn.", names the parts where the warnings name the sails, and is every ship's line. It is left as it is.

**Checked on this commit:**
- `ruff check` and `ruff format --check` clean;
- no carriage return;
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.

**The tiers:** the fast and the slow tier whole run on this commit's hash, test by test against b35aaaba's code, which is 111b1b5's: its fast tier is the l72t run of 111b1b5 and its slow likewise. The eighteen in gales and A2's harness run on it too, since `strain.py` moves. The results follow in a section of their own; the commit after this one touches this report alone.

**For the coordinating session:** the branch to watch is **`…/pkg-90-lateen2`**, this section's commit, pushed, its tiers running.
