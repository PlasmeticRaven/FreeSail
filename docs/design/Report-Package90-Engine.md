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

## Looking ahead at A2's re-mend: how each step reads A2's new readers, not merged (2026-11-21)

Read for the coordinating session's plan (A2's re-mend on `…/pkg-90` at 7686aec1, with A3), with
`git merge-tree` of each hash against `origin/…/pkg-90` at 7686aec1 and `ruff check` of the
merged `scripts.py`. **Nothing merged and nothing built.** Written now, ahead of A4's section, for
the first item.

1. **A1a-A1b (71ae1aae) and A1c (be2c90fd): a name the merge leaves undefined, with no conflict
   to show it.** `HeaveToScript.check` (A1a, ea1045e) refuses a rig of whole lateens with no head
   sail set and no braced yard by `not has_braced_yards(head, after)`. A2's second pass removes
   `has_braced_yards` (its uses there read `braces_worked`). Git merges the line clean (A1a-A1b's
   conflict is TuningNotes' alone, A1c's none), and the merged file fails `ruff check`:
   `freesail/evolutions/scripts.py:3707:53: F821 Undefined name has_braced_yards` (3714 at A1c).
   Run on a scratch copy of that merge, the xebec's `heave to` with no head sail set fails with
   `NameError: name 'has_braced_yards' is not defined`
   (`tests/test_lateen_whole.py::test_a_rig_of_lateens_with_no_head_sail_set_will_not_lie_to`,
   1 failed).
   The same line stands at A1d, A5-A6 and A4 (3823). **The mend, at A1a-A1b's merge:** the line
   asks whether she has a braced yard at all (A1a's words: "no braced yard"), and names no brace,
   so I would keep its meaning, `not (head or after)`, which is what `has_braced_yards`
   returned. A2's `braces_worked` there differs only for a rig of whole lateens built with head
   yards alone and no square sail set on them: the tartane's file, her topsail furled. That rig
   would be refused "She will not lie to under her lateens: there is no sail to bring her to."
   With the meaning kept she is told "No head sail is set to haul to windward, nor a topsail to
   lay aback.", and she can set it and lay it aback. The xebec probe (no braced yard) and every
   committed file read the same either way. Which of the two is the lead's call.
2. **A1d (e2d6b926): the two conflicts in `scripts.py`.** They are the same, byte for byte, at
   A5-A6 (4ebd88a2) and A4 (b13b8dce): those two add no conflict of their own.
   - **The tack's haul** (`TackScript`, from `mainsail_haul` to `let_go_and_haul`): A1d adds
     the lateens drawn over to `draw` (`lateens_drawn_words`). A2 says "Let go and haul." only
     where she works her braces (`hauled = braces_worked(self.ship)`), else `draw` alone, else
     "Meet her with the helm.". By both rules: A1d's three lines, then A2's test. A rig of whole
     lateens that works no braces says its lateens drawn (after the jib's words where she has a
     head sail) in A2's `elif draw` line. One that works her braces says "Let go and haul." with
     them.
   - **The wear's "Wind aft."** (`WearScript`): A2 names the yards squared by `told_of` and
     `class_word`, and says "hauled out and braced up" by `braces_worked`. A1d puts the lateens
     shifted over (`_lateens_over`) between the sheets and the braces, with A1b's
     `_shift_lateens(new_lee)` after the line. By both rules: A2's four readers, A1d's `over` in
     the line, A1b's call after it. A1d's side's `has_braced_yards` goes, for A2's `worked`.
   - **`tests/test_known_truths.py`**: both sides append at the file's end, package 121's 7-710
     to 7-716 and A1d's 7-670 to 7-672 with their three helpers (`_a1d_probe`, `_a1d_peaks`,
     `_a1d_on_the_bad_hand`). Both are kept whole; they share no name.
3. **A1b's and A1c's other lines** (the lateens' shift and their watch, the box-off's
   interruption "the helm and the yards left as they stand; ...", worded as the settee's line
   beside it, which A2 leaves as it is) name no brace and read none of A2's readers.
4. **A5-A6 as ruled**: they read A2's readers without crossing them. `yard_level` reads a yard's
   place on its mast. A2's `_split_as_built` reads head or after by the mast as she was built.
   Each changes nothing the other reads. The smack is of one mast (`one_masted`) and her topsail
   is a head yard, so by A2 she works her braces only while it is set (`square_set_on`). The cast
   under her plain sail (ruling 3) leaves it furled, so A2's cast lines ("The topsail yard
   abox.", ", brace round the topsail yard") are not said of her, as on `…/pkg-90` now: the two
   rules agree there. With her topsail set by the player she works her braces by A2, and her
   topsail is a topsail by A5: hove to, she has A2's "the braces" (`braces_manned`, one mast) and
   A5's topsail to the mast. That is read from the code, not run. It is for the re-measure at
   the merge (the smack's table, every order, as in A5 and A6's sections).
5. **A4** reads no yard and no brace. Its conflicts are A1d's.

## Step A4 as ruled (nudge 36): the boat in tow, on A5 and A6 as ruled (2026-11-21)

**Built under the lead's ruling on the step's stop (nudge 36):** A4 widened to `world/boats.py`,
`world/dealings.py` and `world/ports.py` for the towed boat alone, and its drag carried by the
trawl's road in `integrate.step`. **Merged first** (nudge 39): **`…/pkg-90-a56` at
4ebd88a**, A5 and A6 as ruled, into `…/pkg-90-engine` by the merge commit **b13b8dc**, so that A4
sits on them; from the package branch, nothing (A2's re-mend is on `…/pkg-90` at 7686aec1, with
A3; the coordinating session merges each step's hash into it in its turn, and none is merged
from it here until it asks). **The base** of every comparison is A5 and A6 as ruled,
**e83f9e7** (the code of `…/pkg-90-a56`; the commit above it adds its report section alone).

**Commits:** **99d164c** on `…/pkg-90-engine` (parent effbaed), A4 alone, one commit; then the
merge **b13b8dc** (parents da88dae, the engine branch's tip, and 4ebd88a). The merge's
conflicts, resolved: `tests/test_yard_level.py` as A5 and A6 as ruled have it (A4 does not touch
it; the two branches carry the same tréou commits under two hashes, restated on `…-a56`);
`docs/dev/TuningNotes.md`, both sides' sections whole, "Package 90, A5 and A6" as ruled and
"Package 90, A4" as built; this report as `…-a56` has it, which holds the engine branch's sections
whole. **The merge brings A4 alone onto A5 and A6 as ruled:** `git diff 4ebd88a b13b8dc` is
`git diff effbaed 99d164c` line for line (nine files, 581 lines in and 40 out, the same lines).
**On origin**, each a branch of its own: `…/pkg-90-a56` at 4ebd88a, its own name (pushed once the
owner allowed the new branch, after the coordinating session's note that it was not there), and
`…/pkg-90-engine` at b13b8dc, then the look-ahead at A2's re-mend (eafd309, the section above)
and this section, each a report commit alone.

**Files** (my row's, and the three the ruling widens it to):
- `freesail/world/boats.py`: `way_on_her(ship_hull, boat)`'s towed branch, `HAUL_ALONGSIDE_WAY_MS`,
  `TOWED_ASTERN_M`; `man_boat`'s place astern and words, `tow_with_boat`'s, `come_alongside`'s and
  `hoist_in`'s words (`_launched`, `_back_aboard`, `_spec_of`); `keep_in_tow`, `_towed_hull`;
- `freesail/world/dealings.py`: `OUT_PHASES`, `_out_phase`; the first phase of the errand,
  `_boat_kept`'s reading of it, the two schedules' times (`boat_out_s`, `boat_in_s`), the two
  "back" lines (`_back_aboard`, `_towed`), the boat's home words, and `keep_in_tow` each tick
  (`_tows_a_boat`);
- `freesail/world/ports.py`: `BOAT_HAUL_ALONGSIDE_S`, `BOAT_VEER_ASTERN_S`, `boat_out_s`,
  `boat_in_s`; `BoatState.words(towed)`;
- `freesail/physics/integrate.py`: `TOW_WAKE_FACTOR` and the drag beside the trawl's, in
  `step`; the hull's equations read, not changed;
- `freesail/evolutions/scripts.py`: `SendBoatScript`'s and `LayOutKedgeScript`'s `towed` (a class
  default, set by `check` only for a towed boat), their times and words (`_boat_out_s`,
  `_boat_in_s`, `_boat_out_words`, `_alongside_phase`);
- `data/evolutions/send_boat.yaml`, `data/evolutions/lay_out_kedge.yaml`: the towed boat's
  paragraph in the served notes, `haul_alongside_s` and `veer_astern_s`, and the log lines'
  `{boat_out}` and `{boat_back}`;
- `tests/test_boat_towed.py` (new); `docs/dev/TuningNotes.md`: "Package 90, A4".

Every changed line stands behind `towed`: a boat's key (stage 0's), read as
`getattr(boat, "towed", False)`, which no committed file carries. **No key is written into a
committed file**, so stage 0's `KEY_CARRIERS["towed"]` stays empty and its row does not move. No
ship file moves (`python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte). No class added
(functions, constants, a module dictionary), so truth 7-606 and the checkpoint's list are not
touched; the key's value is a tuple of `ship.parts.Hull`, a class the list admits already. LF;
ruff check and format clean; no Python line over 100. Nothing under `docs/agents/consent/`.

**A7's use of `world/boats.py` beside A4's**, so that the two do not cross: A7's is the boat
predicates alone (`is_boat`, "her file has oars", and `_oars`), so that a hull with `sweeps:` stays
a ship and not a boat. A4's is `way_on_her`, `man_boat`, `tow_with_boat`, `come_alongside`,
`hoist_in` and the new `_launched`, `_back_aboard`, `_spec_of`, `keep_in_tow` and `_towed_hull`;
it reads no predicate and changes none.

### What was built

TuningNotes has each piece with its words. **Her words**: hauled up alongside by her painter and
manned at the gangway, not hoisted out; back alongside, veered astern on her painter again, not
hoisted in; at home "towing astern on her painter", not "at the booms". **Her place**: manned, she
lies 12 m dead astern on her painter, not 15 m off the lee quarter. **The way rule**: hauled
alongside and manned with up to three knots of way, against a hoisting out's two. **The hauling
times**: a minute each way against five. **Her drag**: while in tow, her own resistance at the
ship's speed times 0.6, on the way ahead alone; gone while she is away or lost.

**JUDGEMENT, each with its reason** (TuningNotes):
1. **The way rule's figure**, 3 knots (`HAUL_ALONGSIDE_WAY_MS`): a boat hauled up alongside on her
   painter may be boarded with a little way on, the ship eased; at more she sheers about and fills
   alongside. No period figure found.
2. **The hauling times**, 60 s each (`BOAT_HAUL_ALONGSIDE_S`, `BOAT_VEER_ASTERN_S`): the painter
   hand over hand and the crew down into her, against the five minutes of the yard and stay
   tackles. No period time found.
3. **Her place astern**, 12 m (`TOWED_ASTERN_M`): a short painter's length, two of her lengths
   and a little, so that she rides clear of the ship's stern.
4. **The wake factor**, 0.6 (`TOW_WAKE_FACTOR`): she rides in the ship's wake, water the ship drags
   along with her, so it meets her slower than the sea meets the ship; a wake fraction of about a
   quarter so near the stern (memory, unverified) gives (1 - 0.25) squared, about 0.6, for a drag
   that goes as the square of the speed. **Not tuned to any band.** For the hulls' truths later:
   they say which state they are measured in, the boat in tow as she ordinarily sails.

### Measured

- **Not one event of the eighteen files' boats moves.** A harness in the session's scratch
  (`a4/boatwork.py`) runs every committed file's boat work, each from a fresh world, seed 7: at
  anchor in Carrick Road, the readings' boat words, `send the boat ashore` to its end and `lay out
  a kedge to the NE` to its end; at rest in a calm off the Lizard, `go to the boat`, two minutes,
  and `come alongside` (hoisting out, manning, hoisting in); `tow her with the boat to the NE`
  twenty minutes and `the boat alongside`; and `go to the boat` with 2.5 knots of way on her (the
  way rule). Each run keeps every event of every hull (tick, kind, text and data), every reply, a
  trace each minute (her heading, way, position, the boat's words and `ship.extra`'s keys) and the
  checkpoint's digest. At e83f9e7 and at the merge: **72 runs, every field the same, 1,070
  events and 2,376 trace rows, every checkpoint digest the same; the two files byte for byte**, as
  at effbaed and 99d164c when first built. (Run first from two worktrees, the digests differed and
  nothing else: a checkpoint holds the build's own stamp, a hash of the source, and each port
  file's path, the tree's own; run from one path with the stamp held the same, they agree.)
- **The eighteen files' sailing**: A2's harness (the going about and its kin, 270 runs) at e83f9e7
  and at the merge: **every tick, kind, trace and line the same** (the two files byte for byte),
  as at effbaed and 99d164c.
- **The tartane probe, her boat in tow** (seed 7; `tests/test_boat_towed.py` pins each): at anchor
  in Carrick Road, `send the boat ashore` takes 4,581 s against 5,040 with her boat on deck (out in
  56 s against 283, home in 58 s against 290); `lay out a kedge to the NE`, her hands short, 739 s
  against 1,399 (out in 82 s against 412, home in 83 s against 413). Manned at rest she lies 12.0 m
  dead astern. With 2.5 knots of way she is manned and the boat on deck is refused; with 3.4 knots
  both are refused, each in its words. At the merge, re-measured: every time the same.
- **Her drag** (plain sail trimmed every two minutes after five, the mean of the last 600 s of
  2,400; the wind from 0°):

  | Wind, her head | Boat on deck | Boat in tow | The boat's drag | The probe's own resistance |
  |---|---|---|---|---|
  | 8 kn, 270° (beam) | 4.34 kn | 4.25 kn | 122 N | 2,633 N |
  | 15 kn, 270° (beam) | 7.23 kn | 7.00 kn | 905 N | 8,855 N |
  | 25 kn, 270° (beam) | 9.52 kn | 9.14 kn | 3,737 N | 21,725 N |
  | 15 kn, 315° (close-hauled) | 3.71 kn | 3.66 kn | 79 N | 1,919 N |
  | 15 kn, 225° (broad) | 6.29 kn | 6.13 kn | 485 N | 6,169 N |

  So she loses 1 to 4 per cent of her way, the most on a fast reach. A checkpoint of her with her
  boat in tow sails on the same. Measured at 99d164c, and again at the merge: every figure the
  same.

### Moved, old beside new, with reason

Nothing moves.

### The test sets run, with counts, and the base comparison

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
each junit kept in the session's scratch. **The base is A5 and A6 as ruled, e83f9e7** (its two
tiers' junits, run for that section), test by test. The first fast run and the slow run are of
a scratch merge, b4c4cb7, whose tree is b13b8dc's but for this report (`git diff b4c4cb7 b13b8dc`:
the report alone); the second fast run is of b13b8dc itself, with nothing else running.

| Run | Base (e83f9e7) | A4 at the merge (b4c4cb7, b13b8dc) |
|---|---|---|
| **Fast tier whole**, `--junitxml`, first run (b4c4cb7) | 8,700: 8,691 passed, 8 skipped, 1 xfailed, 0 failed (1 h 23 min) | 8,729: 8,719 passed, 8 skipped, 1 xfailed, **1 failed** (1 h 17 min). **Test by test: every one of the base's 8,700 the same outcome but one; 29 new, all passed** (`tests/test_boat_towed.py`). The one: `tests/test_replay.py::test_the_fingerprint_is_of_the_code_and_the_data_and_not_of_the_line_endings`, its wall-clock bound, `rules_fingerprint()` in 0.646 s against 0.5 s (0.118 s in the base's run). Run alone, it passed at both trees (0.23 to 0.31 s); `rules_fingerprint()` ten times at each, the median 0.110 s at both |
| **Fast tier whole**, `--junitxml`, second run (b13b8dc, alone on the machine) | the same | 8,729: 8,719 passed, 8 skipped, 1 xfailed, **1 failed** (1 h 20 min). **Test by test: every one of the base's 8,700 the same outcome but one, and not the first run's one; the same 29 new, all passed.** The fingerprint's case passed (0.117 s). The one: `tests/test_known_truths.py::test_truth_7_284_the_blend_adds_a_membership_and_not_a_gauge`, a pace within a quarter (the tide's blend against the eleven gauges alone, the best of five), 0.0220 s against 0.0140 s, 1.57 against 1.25. Run alone ten times: **10 of 10 passed at b13b8dc, 9 of 10 at e83f9e7**, the base's own tree failing it once. Its measure five times over, alone: the ratio 0.92 to 1.83 at b13b8dc, 0.97 to 1.31 at e83f9e7 |
| **Slow tier whole**, `--slow -m "slow and not pace"` (b4c4cb7; the drag in `integrate.step`, so the tier whole) | 568: 557 passed, 11 xfailed, 0 failed (1 h 28 min) | 568: 557 passed, 11 xfailed, 0 failed (1 h 28 min). **Test by test: every one of the base's 568 the same outcome**, none new |

**The two failures** are each a wall-clock bound, each failing in one run and passing in the
other, each passing alone, on a machine of four cores with four workers. **A4 touches neither:**
`git diff e83f9e7 b13b8dc` reaches no line of `freesail/world/tide.py`, `freesail/world/geo.py`,
`tests/test_known_truths.py` or `tests/test_replay.py`, and the fingerprint reads the code and
the data at the same pace at both trees. Neither case is loosened, skipped or marked; each is
reported as it ran.

**The guard set of §10.2**, tallied from each fast tier's junit, base beside new, every case the
same outcome in both runs: the byte test and the golden classing table 96 passed;
`tests/test_schooner_mast.py` 74; `tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py`
21; the lugger's set 58; the settee's 75; the going-about set 261; `test_grammar_book` and truth
7-606 74; `tests/test_lateen_whole.py` 90; all passed at both.

**The generator**, on b13b8dc: `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte with
`data/ships/`. **`ruff check`** and **`ruff format --check`** on b13b8dc: clean (430 files).

### Unsure, and for the lead

1. **`world/movement.py`'s person in the boat at her side** (package 109,
   `_in_the_boat_at_the_side`, l. 494) reads the errand's first phase as `"hoisting out"` alone,
   so a person in a towed boat while she is hauled alongside (her first minute) is not "in the boat
   at the side" and cannot belay her from it. The mend is one line there (`boat.phase not in
   dealings.OUT_PHASES`). My row names `world/movement.py` for A7 alone, and the ruling widened A4
   to three files that are not it, so by the stop rule it is not edited. No committed file meets
   it.
2. **`combat/hits.py`'s "stove on the booms by a shot"** is said of any boat; a towed boat is not
   on the booms. My row names `combat/hits.py` for A3 alone; not edited. For the tartane's file:
   whether a shot reaches her boat astern at all.
3. **The clearing for action** (`action_scripts.py`) gives the boats their share of the clearing
   time and says "The boats are out and towing astern; the ship is clear." of every ship; a ship
   whose boats are all towed already needs no time for them. Left as it is (no row reading asked
   for it, and no committed file tows).
4. **Her drag at speed**: on a fast reach the yawl's file is far past its own hull speed (5.4 kn)
   and the form's wave term rises steeply: 3,737 N at 9.1 kn, a sixth of the probe's own. The
   factor is not tuned for it, as ruled. The tartane's design (§11) has her boat "hoisted in, or
   veered long, in a blow": no order veers the painter long or hoists a towed boat in on passage;
   for the tartane's builder, if her truths want it.
5. **A boat with no file of her own** that is towed puts no drag on the ship (her resistance has no
   form to be read from); no committed file and no probe has one.
6. **The sleeping hull's errand** (`_send_boat_coarse`) takes the towed boat's times; no drag is
   kept on a sleeping hull (its way is the plan's), and the key is kept each tick on every hull
   whose file tows a boat, asleep or awake.
7. **The fast tier's wall-clock bounds** (the fingerprint's 0.5 s, truth 7-284's quarter) each
   failed once here under four workers on four cores and passed alone, the base's tree failing
   7-284 alone once in ten. `tests/conftest.py` keeps such measures out of the tiers by the `pace`
   mark; neither case carries it. Not mine to mark (my row does not name `tests/conftest.py`, and
   no test is loosened); said for the lead, as `docs/dev/ContinuationProposal.md`'s "Timing tests
   out of the ordinary tiers" says of others.

**The look-ahead's item 1, ruled** (the lead's nudge 43, trunk d6159090): (a), A1a's meaning kept,
`not (head or after)`, a question of what she carries and not of what is set. The coordinating
session makes the one-line mend at A1a-A1b's merge into `…/pkg-90`; A1c and the later steps carry
the line unchanged and merge onto it. When A1d, A5-A6 and A4 are resolved against it, by both
rules, each hash's report says which lines were resolved by hand, and `ruff check` runs on each
merged tree before its tiers.

Stopped after A4 and the A5-A6 section, as briefed: waiting for the coordinating session's message.

## For the coordinating session: held on nudge 46's item 6, a file outside my row (2026-11-21)

**Where nudge 46 stands.** `…/pkg-90-a1ab` is cut locally from 0d5d2c56; nothing is pushed to it
yet. Items 1 to 5, 7 and 8 are built there, uncommitted, and the lugger's bow watch is declared in
TuningNotes, old beside new. Each item has a proof in `tests/test_lateen_whole.py`, and each proof
fails when its mend is undone (thirteen mutations, each failing its pins). The base tiers on
0d5d2c56 are running.

**Held on item 6.** The lead asks that "no whole lateen aboard" be served only where she carries
a whole lateen, and kept out of the samples. A station's sample is drawn in
`freesail/agents/harness.py`'s `_sample_readings`: `agents/tools.readings_words` less
`api/action_readings.py`'s `idle_rows`. My §7.1 row names only `api/readings.py`'s practice row,
and no field of a `Reading` (`where`, `absent`, `none_words`, `per_asker`) keeps a row out of a
sample. By the stop rule I have not edited either file.

**The smallest mend:** `idle_lateen_rows(world)` in `api/readings.py`, naming the practice's row
where she carries no whole lateen, and read by `idle_rows` in `api/action_readings.py`. That is two
lines there, as `idle_practice_rows` is read now, with a test that the row is in no sample of the
eighteen and is in the xebec probe's. The readings tool itself keeps every row:
`tests/test_grammar_book.py` asks every reading to be named in the primer, and the tool's own tests
read every registry row. That is the rule of the readings that wants every row on every ship.

**The question:** may I edit `api/action_readings.py` for those two lines? Until I hear, item 6
stays stopped and the hash is built without it.

**And the new branch:** pushing `…/pkg-90-a1ab` may need the owner's allowance, as `…-a56` did; I
will ask the owner when the hash is ready.

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

## The second pass merged into the engine track, under A1c, A1d, A5-A6 and A4 (nudge 46, 2026-11-22)

**The merge:** **4a4e1c6** on `…/pkg-90-engine`, parents **db715d8** (the engine branch's tip)
and **2e1e19b** (`…/pkg-90-a1ab`'s tip, the hash above). It brings onto the engine's steps both
the second pass and what lay under it at 0d5d2c56: A2's re-mend and A3, and the package's other
commits since the engine last took it: 71 commits in all, the second pass's three among them. The
code and data take 29 files, 1,066 lines in and 173 out; the tests take seven files, 1,845 in and
67 out. Git finds two merge bases, 033f42b7 and 71ae1aae, a criss-cross (each branch has merged a
commit of the other's), and merges against the two together.

**Which lines were resolved by hand** (five files conflicted; every other file merged clean):
1. **`freesail/evolutions/scripts.py`, the tack's haul** (`TackScript`, at "let go and haul"),
   by both rules, as the look-ahead set out. Kept from the engine: A1d's three lines,
   `if left:`, `on = lateens_drawn_words(self.ship, left)` and `draw = ...`. Dropped from the
   engine: its `if self.head:`. Taken from the package: A2's five-line comment,
   `hauled = braces_worked(self.ship)` and `if self.head and hauled:`. So a rig of whole
   lateens that works no braces says its lateens drawn over in A2's `elif draw` line.
2. **`freesail/evolutions/scripts.py`, the wear's "Wind aft."** (`WearScript`), by both rules.
   Taken from the package: A2's comment and its readers, `worked = braces_worked(self.ship)`,
   `swung = told_of(...)`, `yards = ...`, `squared = ...` and `braced = ...`. Dropped from the
   engine: its `squared = ...` and its `braced = ...`, the one that read `has_braced_yards`.
   Kept from the engine, and written in by hand: A1d's
   `over = self._lateens_over(new_lee, wind)  # package 90, A1d`, and the line
   `self.note(f"Wind aft. {squared} over the sheets{over}{braced}." + dipped)`, which is A2's
   line with A1d's `{over}` in it. A1b's `self._shift_lateens(new_lee)` after it merged as it
   stood. No `has_braced_yards` is left in the tree; 0d5d2c56's hand-resolved
   `not (head or after)` came over clean.
3. **`tests/test_lateen_whole.py`**: the engine's file whole (A1a to A1d, 48 tests), with the
   second pass's own diff from 0d5d2c56 applied to it: the two pins moved, `NOT_HERS`, and its
   section appended after A1d's. The import block is united: the engine's, with
   `brig_with_settee_doc`, `tartane_probe_doc`, `LUG_AGAINST_MAST_AREA`, `against_the_mast`,
   `compute_sail_forces`, `LineState` and `contrary`. No name is shared: 65 tests, the engine's 48
   and the second pass's 17.
4. **`tests/test_known_truths.py`**: both appended sections kept whole, A1d's 7-670 to 7-672
   with their three helpers first, then the package's (package 121's 7-710 and on); they share no
   name.
5. **`docs/dev/TuningNotes.md`**: both sides' sections whole. The package's sections that the
   engine lacked come in whole: 465 lines, A2's re-mend among them. The engine's sections from A1c
   to A4 (190 lines) are followed by the second pass's (34). Three lines of A2's own first-pass
   section are as A2's re-mend rewrote them on the package (7686aec1). Git merged those without
   a conflict, and no line of the engine's own sections is lost.
6. **This report**: the engine's whole. Every line of the package's copy, A2's and A1a-A1b's
   sections, is in it already. The second pass's section is appended, as above.

**Checked on the merged tree:**
- No conflict marker is left anywhere. `ruff check` and `ruff format --check` are clean: 431
  files, run before the tiers.
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.
- The code, tests and data are byte for byte those of a dry run of the same merge, made in the
  session's scratch from 75abacd. The commits after 75abacd change TuningNotes and the report
  alone.
- On that dry run, with `-n 2`:
  - `test_lateen_whole`: 147 passed;
  - the lens of `test_rig_words`, `test_probes_90`, `test_settee`, `test_lug`, `test_yard_level`,
    `test_pole_mast`, `test_boat_towed`, `test_helm_kind`, `test_held_work`, `test_catalogue`,
    `test_captains` and `test_bilander`: 553 passed;
  - both sides' new truths (7-67x, 7-68x, 7-69x, 7-71x): 10 passed.

**The tiers of 4a4e1c6** are running (fast, then slow, from 03:36 UTC). Each case will be set
beside its outcome on the engine at db715d8 (A4's merge, b13b8dc's code, whose tiers were run for
A4's section), with the cases that A2's re-mend, A3 and the package bring named by their file.
They follow in a section of their own when done.

**For the coordinating session:** `…/pkg-90-a1ab` at **2e1e19b** is the hash for the gate (its
section above); the engine branch now carries it, at 4a4e1c6.

## For the coordinating session: the merge's slow tier, and a question on nudge 48's item 3 (2026-11-22)

**The merge's tiers (4a4e1c6), both done.** Set beside the engine at db715d8 (A4's merge,
b13b8dc's code, its tiers run for A4's section), test by test, with the xdist group's `@...`
stripped from each id:
- **Fast tier whole:** 8,843 cases, 8,834 passed, 8 skipped, 1 xfailed, 0 failed (58 min). Every
  one of the engine's 8,729 has the same outcome but these:
  - truth 7-284's wall-clock bound failed there under load and passes here;
  - five cases are gone: the heave-to pin renamed by the second pass, and four
    `tests/test_rig_words.py` cases that A2's re-mend renamed on the package, none of them at
    0d5d2c56 either;
  - 119 are new, all passed, each also in the a1ab hash's tier (48 of the second pass's lateen
    cases, 33 of A2's `test_rig_words`, 12 of `test_mends_120`, 7 of the package's truths, and
    their renamed kin).

  The guard set is the same, all passed; `test_lateen_whole` went from 90 cases to 147.
- **Slow tier whole:** 569 cases, 558 passed, 11 xfailed (1 h 5 min). Every one of the engine's
  568 has the same outcome, and one is new, A2's, passed. Against the a1ab hash's slow tier,
  every one of 569 is the same.

**Nudge 48 is read, and the third pass is begun** on `…/pkg-90-a1ab` above 2e1e19b, with no
merge.

**A question on item 3, the count of the rows not to be had.** The "... and 18 more" is counted
by `freesail/world/knowledge.py`'s `rows_elsewhere(senses)`. That function has the senses alone,
and they hold the hull by its name, not the ship, so it cannot tell whether she carries a whole
lateen. The smallest mend:
- `rows_elsewhere(senses, world=None)`, leaving out `readings.idle_lateen_rows(world)` when a
  world is given;
- and its two callers passing the world they already have, one argument each:
  `freesail/agents/harness.py`'s `_readings_elsewhere` (the stations' line) and
  `freesail/api/queries.py`'s rows elsewhere (the player's).

So the line is the trunk's to the byte on the eighteen, at both doors. **May I make those two
one-argument edits beside `knowledge.py`?** Until I hear, item 3 is held and the rest goes on.

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

## The third pass merged into the engine track (nudge 48, 2026-11-22)

**The merge:** **0d639a6** on `…/pkg-90-engine`, parents **e1b5671** (the engine branch's tip)
and **7173281** (`…/pkg-90-a1ab`'s tip: the third pass, 1458b0e, and its report's tiers). It
brings two commits onto the engine. The code and data take seven files, 335 lines in and 61 out.
The tests take one file, `tests/test_lateen_whole.py`, 417 in and 22 out. Git finds one merge
base, 2e1e19b: the engine took the second pass at 4a4e1c6, and this is the same merge again.

**Which lines were resolved by hand** (four files conflicted; every other file merged clean):
1. **`freesail/evolutions/runner.py`, `_start_waiting`**, by both rules. Kept from the engine:
   A1d's `if busy or lateen_take_in_waits(ship, inst.evo.verb, inst.subject):` and its
   `continue  # a whole lateen aback in a strong wind waits too (package 90, A1d)`. Dropped from
   the engine: its `reason = self._failing_condition(ship, inst, inst.evo.preconditions +
   inst.evo.requires)`. Taken from the third pass: its comment `# work a belay handed on is begun
   already: its beginning's conditions are not read`, `conditions = [] if
   inst.params.get(HANDED_ON) else inst.evo.preconditions` and `reason =
   self._failing_condition(ship, inst, conditions + inst.evo.requires)`. Dropped from the third
   pass: its plain `if busy:` and `continue`. So the work handed on skips its preconditions, and
   the take-in waits as A1d had it.
2. **`freesail/evolutions/scripts.py`, the tack's haul** (`TackScript`, at "let go and haul"), by
   both rules. Taken from the third pass: `draw = " Draw jib; trim aft the head sheets." if
   self._jibs() else ""`, then `if self.heads and not draw:`, its comment `# the fore lateen alone
   drawn on the new board (package 90, nudge 48)` and `draw = f" Draw the
   {self._boom_names(self.heads)}; trim aft its sheet."`. Dropped from the engine: its
   `draw = ... if self.heads else ""`. Kept from the engine, after them: A1d's `if left:`,
   `on = lateens_drawn_words(self.ship, left)` and `draw = f"{draw[:-1]}; {on}." if draw else
   ...`. So the fore lateen's own line comes first, and A1d's lateens drawn over are joined to it.
3. **`tests/test_lateen_whole.py`, the import block**: the engine's four lines, from
   `from freesail.evolutions import trim as yard_trim` to the `freesail.physics.sails` line, with
   `LUG_AGAINST_MAST_AREA` dropped from that line as the third pass dropped it. Its one use, the
   two-thirds pin, is against `2.0 / 3.0` now (item 6), and ruff would flag the name unused. The
   rest of the file merged clean: the engine's 147 cases and the third pass's 44, 191.
4. **This report**: both sides' sections whole, the engine's first (the second pass's merge and
   the question on item 3), then the third pass's section with its tiers.

`docs/dev/TuningNotes.md` merged clean: the engine's 171 sections whole, and the third pass's
appended after the second pass's, 172. No line of either side's is lost.

**Checked on the merged tree:**
- No conflict marker is left anywhere. `ruff check` and `ruff format --check` are clean: 431
  files, run before the tiers.
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.
- The code, tests and data are byte for byte those of a dry run of the same merge, made in the
  session's scratch from 1458b0e. 7173281 changes this report alone.
- The lens, `-n 4`, on the merged tree (0d639a6): 2,068 passed, 1 skipped, 1 xfailed, 0 failed;
  `test_lateen_whole`'s 191 among them, all passed. It ran over `test_lateen_whole`,
  `test_settee`, `test_bilander`, `test_lug`, `test_hull_lugger`, `test_standing`, `test_orders`,
  `test_held_work`, `test_evolutions`, `test_catalogue`, `test_probes_90`, `test_grammar_book`,
  `test_practice_orders`, `test_mends_75`, `test_lateen`, `test_agents`, `test_practice`,
  `test_knowledge`, `test_agent_api`, `test_readings`, `test_checkpoint`, `test_tow`,
  `test_yard_level`, `test_pole_mast` and `test_rig_words`.

**The tiers** run whole on the commit that adds this section, which touches this report alone.
Each case will be set beside its outcome at 4a4e1c6 (the engine's last tiers, above) and at
1458b0e (the third pass's). They follow in a section of their own when done.

**For the coordinating session:** `…/pkg-90-a1ab` at **7173281** is the hash for the gate (1458b0e
tiered, the commit after it the report alone). The engine branch now carries it, at 0d639a6.

## For the coordinating session: the third pass's merge, its tiers (nudge 48, 2026-11-22)

**The tiered hash is b764b06**, the commit that adds the merge's section above (its code, tests
and data are 0d639a6's, the merge). This commit, which writes the results, touches this report
alone.

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
on b764b06's own worktree, each junit kept in the session's scratch. Set beside the engine's last
tiers, those of **4a4e1c6** (the second pass's merge), and beside the third pass's, those of
**1458b0e**, test by test, with the xdist group's `@...` stripped from each id:

| Run | b764b06 | Against the engine (4a4e1c6) | Against the third pass (1458b0e) |
|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,887: 8,878 passed, 8 skipped, 1 xfailed, 0 failed (59 min 36 s) | **Every one of the 8,843 the same outcome**, none gone; **44 new, all passed**, the third pass's, every one in `tests/test_lateen_whole.py` | **Every one of the 8,766 the same outcome**, none gone; **121 new, all passed**, the engine's own steps': `test_yard_level` 34, `test_boat_towed` 29, `test_pole_mast` 28, `test_lateen_whole` 27 (A1c's and A1d's) and `test_known_truths` 3 |
| **Slow tier whole**, `--slow -m "slow and not pace"` | 569: 558 passed, 11 xfailed, 0 failed (1 h 11 min) | **Every one of the 569 the same outcome**, none new | **Every one of the 569 the same outcome**, none new |

**The guard set of §10.2**, tallied from the fast tier's junit, the same at 4a4e1c6: the byte
test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed.
`tests/test_lateen_whole.py`: 147 at 4a4e1c6, 191 now, all passed.

**The hashes for the gate:** `…/pkg-90-a1ab` at **7173281** (1458b0e tiered, the commit after it
the report alone); `…/pkg-90-engine` at this commit (b764b06 tiered, this commit the report
alone).

**Next:** nothing more on nudge 48. I wait for the coordinating session's word here.

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

## A1c's hash merged into the engine track (nudge 49, 2026-11-22)

**The merge:** **b3c2dee** on `…/pkg-90-engine`, parents **68d74c1** (the engine branch's tip)
and **ee66c4a** (`…/pkg-90-a1c`'s tip: A1c's hash with the five, 2f3285c, and its tiers). It
brings 23 commits onto the engine: the five and their tiers, and `…/pkg-90` as cut at b3c68af4
(its merges of A1c, A3 and A3's two lists, and of the three A1a-A1b passes, and the trunk to
7a1bd65e). The code and data take seven files, 146 lines in and 40 out. The tests take two,
`tests/test_helm_kind.py` (A3's lists) and `tests/test_lateen_whole.py`, 515 in. Git finds two
merge bases, 7173281 and be2c90f. The engine took the third pass from `…/pkg-90-a1ab`, and
`…/pkg-90` took it again at 5e42ed2f.

**Which lines were resolved by hand** (four files conflicted; every other file merged clean,
`freesail/evolutions/scripts.py` among them):
1. **`freesail/evolutions/runner.py`, `_start_waiting`**, by both rules:
   - Kept from the engine: A1d's `if busy or lateen_take_in_waits(ship, inst.evo.verb,
     inst.subject):` and its `continue  # a whole lateen aback in a strong wind waits too
     (package 90, A1d)`.
   - Dropped from the engine: the third pass's three lines, `# work a belay handed on is begun
     already: its beginning's conditions are not read`, `conditions = [] if
     inst.params.get(HANDED_ON) else inst.evo.preconditions` and `reason =
     self._failing_condition(ship, inst, conditions + inst.evo.requires)`. Nudge 49's item 3
     takes them out.
   - Taken from A1c's hash: `reason = self._failing_condition(ship, inst,
     inst.evo.preconditions + inst.evo.requires)`, as on the trunk before the third pass.
   - Dropped from A1c's hash: its plain `if busy:` and `continue`.

   So the take-in waits as A1d had it, and the work handed on, never waiting, reads its
   conditions as any work. `HANDED_ON`'s import went out clean, and no use of it is left in the
   file.
2. **`tests/test_lateen_whole.py`**, three hunks:
   - The import block: the engine's three lines, `from freesail.evolutions import trim as
     yard_trim`, `from freesail.orders import navigation` and `from freesail.physics import
     sails as P`. A1c's hash had `navigation` alone, so none of its lines is lost.
   - The engine's A1d section (169 lines, from its heading "Taken aback, and the bad hand, in a
     breeze (A1d)"), set against nothing: kept whole.
   - The five's section (353 lines, "The five that ride A1c's hash"), set against nothing: kept
     whole, at the file's end.

   The file is the engine's 191 cases and the five's 22: 213.
3. **`docs/dev/TuningNotes.md`**, three hunks, each side's sections whole:
   - A1c's hash has the lead's nudge-43 paragraph, "**At its merge into `claude/pkg-90`, by hand
     (the lead's nudge 43).** ...", at the end of A1b's section, before A1c's. The engine has
     nothing there. Taken: the paragraph and its blank line, in A1b's section, where the lead
     wrote it.
   - The engine's A1d, A5-A6 and A4 sections (171 lines), set against nothing: kept whole, but
     for their last two lines. Those are a blank and a second copy of that same paragraph, word
     for word, after A4's "Not built, for the lead". Left out, so the paragraph stands once.
   - The five's section (34 lines), set against nothing: kept whole.

   173 sections. Against 68d74c1 the file loses those two lines alone. Against ee66c4a it loses
   none.
4. **This report**, two hunks, both sides' sections whole:
   - The engine's eight sections from A1d to "held on nudge 46's item 6" (867 lines), set against
     nothing: kept.
   - The engine's last two (the third pass's merge and its tiers, 86 lines), set against A1c's
     hash's section with its tiers (201 lines): the engine's first, a blank, then A1c's hash's.

   17 sections before this one.

**Checked on the merged tree, before the tiers:**
- No conflict marker is left anywhere. `ruff check` and `ruff format --check` are clean, 431
  files.
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.
- The code, tests and data are byte for byte those of a dry run of the same merge, made in the
  session's scratch from 2f3285c. ee66c4a changes this report alone.
- The lens, `-n 4`, on b3c2dee: 2,476 passed, 1 skipped, 1 xfailed, 0 failed (7 min 37 s);
  `test_lateen_whole`'s 213 among them, all passed. It ran over the 32 files of A1c's hash's
  lens, and `test_tow`, `test_boat_towed`, `test_yard_level`, `test_pole_mast` and
  `test_rig_words`.

**The tiers** run whole on the commit that adds this section, which touches this report alone.
Each case will be set beside its outcome at b764b06 (the engine's last tiers) and at 2f3285c (A1c's
hash). They follow in a section of their own.

**For the coordinating session:** nudge 50 received. `…/pkg-90-a1d` is cut and merged next, its
tiers held until A1c's verdict, and its section follows on that branch.

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

## A1d's hash merged into the engine track (nudge 51, 2026-11-23)

**The merge:** **64efd89** on `…/pkg-90-engine`, parents **95a58e9** (the engine branch's tip)
and **32c9448** (`…/pkg-90-a1d`'s tip: A1d's hash with the five, 71febde, and its tiers). It
brings eight commits onto the engine. Four are `…/pkg-90-a1d`'s: its two merges of `…/pkg-90`
(4fcd224 at ee66c4a8, cde50e7 at a13fb0fe), the five (71febde) and their tiers (32c9448). Four are
`…/pkg-90`'s since ee66c4a8: the lead's nudge 50 (3a59376), the trunk's merge of A1c (85266ea6),
its record (25ccf84) and `…/pkg-90`'s merge of the trunk (a13fb0fe). A1d's own code was on the
engine already (e2d6b92), and the trunk's four carry no code. So the code takes three files, the
five's: `freesail/evolutions/runner.py`, `freesail/evolutions/scripts.py` and
`freesail/orders/crew.py`, 87 lines in and 10 out. The tests take one, `tests/test_lateen_whole.py`,
282 in. The docs take the trunk's `docs/dev/M7-WorkPackages.md` and `docs/dev/ShipsNudge.md`, as
the trunk has them. Git finds two merge bases, ee66c4a and e2d6b92.

**Which lines were resolved by hand** (three files conflicted; every other file merged clean, the
five's three code files among them):
1. **`tests/test_lateen_whole.py`**, one hunk: the five's section (282 lines, from its heading
   "The five that ride A1d's hash (the lead's nudge 51)"), set against nothing: kept whole, at the
   file's end. The file is then `…/pkg-90-a1d`'s byte for byte: the engine's 213 cases and the
   five's 14, 227.
2. **`docs/dev/TuningNotes.md`**, two hunks, each side's sections whole:
   - The engine's A5-A6 and A4 sections (104 lines, from "## Package 90, A5 and A6: a yard's level
     from its order on its mast" to A4's "Not built, for the lead"), set against nothing: kept
     whole, where they stood.
   - The five's section (31 lines, "Package 90, the five that ride A1d's hash"), set against
     nothing: kept whole, at the file's end.

   174 sections. Against 95a58e9 the file loses no line; against 32c9448 none.
3. **This report**, two hunks, both sides' sections whole:
   - The engine's seven sections from "Step A4: the boat in tow" to "held on nudge 46's item 6"
     (752 lines), set against nothing: kept.
   - The engine's last section (A1c's hash merged, nudge 49; 76 lines), set against
     `…/pkg-90-a1d`'s two (A1d on A1c's hash, and A1d's hash with the five and its tiers; 310
     lines): the engine's first, then `…/pkg-90-a1d`'s. **One line added by hand:** a blank line
     between them, as each side's hunk began at its heading, the blank before it standing outside
     the hunk.

   20 sections before this one. Against 95a58e9 the file loses no line; against 32c9448 none.

**Checked on the merged tree, before the tiers:**
- No conflict marker is left anywhere. `ruff check` and `ruff format --check` are clean, 431
  files. No carriage return in the merge's diff.
- `python tools/gen_ships.py <scratch>`: 18 of 18 byte for byte.
- The code, tests and data are byte for byte those of a dry run of the same merge, made in the
  session's scratch from 71febde. 32c9448 changes `…/pkg-90-a1d`'s report alone.
- The lens, `-n 4`, on 64efd89: 3,699 passed, 1 skipped, 1 xfailed, 0 failed (31 min 37 s);
  `test_lateen_whole`'s 227 among them, all passed. It ran over the 52 files of A1d's hash's lens, and
  `test_tow`, `test_boat_towed`, `test_yard_level` and `test_pole_mast`.

**The tiers** run whole on the commit that adds this section, which touches this report alone.
Each case will be set beside its outcome at b764b06 (the engine's last tiers) and at 71febde
(A1d's hash). They follow in a section of their own.

**The engine's tiers on 95a58e9 (nudge 49's merge) did not finish.** A restart of the session's
machine stopped them at 14% of the fast tier, and they were not run again: 95a58e9 is under this
merge, whose tiers are measured against both b764b06 and 71febde. The record has no tiers of
95a58e9 itself.

**For the coordinating session:** nudge 52 received. A5 and A6's own hash is **b40ffa3** on
`…/pkg-90-a56` (its section there, 695331e, names the lines resolved by hand and sets the smack
beside the trunk), its tiers held until A1d's verdict. If that verdict comes while this merge's
tiers run, A5 and A6's take the machine first, and this section's results say where these stopped.

## A1d's hash merged into the engine track: the tiers on df84c25 (nudge 51, 2026-11-23)

**The tiered hash is df84c25**, the commit that adds the merge's section above; it differs from the
merge, 64efd89, in this report alone. The commit after it, which writes these results, touches this
report alone.

All from the tree's root, `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"`,
on a worktree of its own, each junit kept in the session's scratch. Compared test by test by the
test's id, with the xdist group's `@...` stripped, beside **b764b06** (the engine's last tiers, the
third pass merged) and **71febde** (A1d's hash with the five, its tiers in `…/pkg-90-a1d`'s
section).

| Run | df84c25 | Against b764b06 | Against 71febde |
|---|---|---|---|
| **Fast tier whole**, `--junitxml` | 8,931: 8,922 passed, 8 skipped, 1 xfailed, 0 failed (58 min 35 s) | b764b06's 8,887 (8,878 passed, 8 skipped, 1 xfailed): **every one the same outcome**, none gone; **44 new, all passed**: 36 in `tests/test_lateen_whole.py` (A1c's five's 22 and A1d's five's 14) and 8 in `tests/test_helm_kind.py` (A3's lists) | 71febde's 8,840: **every one the same outcome but one**, none gone; **91 new, all passed**, the engine's own: `tests/test_yard_level.py` 34, `tests/test_boat_towed.py` 29 and `tests/test_pole_mast.py` 28. **The one**: `tests/test_harbour.py::test_in_the_browser_the_stations_are_one_table_and_a_planned_door_is_offered`, failed at 71febde, passed here: the harbour's race, the lead's to mend (nudge 52), the code the same at both |
| **Slow tier whole**, `--slow -m "slow and not pace"` | 569: 558 passed, 11 xfailed, 0 failed (1 h 6 min 52 s) | b764b06's 569 (558 passed, 11 xfailed): **every one the same outcome**, none gone, none new | 71febde's 569 (558 passed, 11 xfailed): **every one the same outcome**, none gone, none new |

**The guard set of §10.2**, tallied from the fast tier's junit, every case the same outcome as at
b764b06: the byte test and the golden classing table 96 passed; `tests/test_schooner_mast.py` 74;
`tests/test_probes_90.py` 89; `tests/test_check_viewer_guns.py` 21; the lugger's set 58; the
settee's 75; the going-about set 261; `test_grammar_book` and truth 7-606 74; all passed.
`tests/test_lateen_whole.py`: 191 at b764b06, 227 now, all passed.

**95a58e9** (nudge 49's merge), whose own tiers a restart of the machine stopped, is under this
hash: these tiers stand for it, as the merge's section says.

**Next:** A5 and A6's tiers on b40ffa3 at A1d's verdict, as the lead's nudge 52 asks; the engine
track holds.
