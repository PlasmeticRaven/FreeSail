# Package 127: words and waits on today's ships

The design and report of package 127, the eight faults of `docs/dev/CarriedForward-M7.md`, section 4 (items 1, 3, 4, 5, 7, 8, 9 and 13), in what the log said, or failed to say, on ships already in the game. The log is the game: a line untrue, or a wait unsaid, is a fault of the game. Each was reproduced on a committed ship by a player's orders (seed 7, a steady wind from the north unless said), its cause found, and mended at the cause where the mend changes only what is said. Where a mend would change what a ship does, it was held for the lead's word. The lead ruled item 4 in, and item 5 and the cutter's sternway out.

New truths 7-780 to 7-787 are in `tests/test_words_and_waits.py`, a file of their own so that the three builders of the mending step do not meet in `tests/test_known_truths.py`. Each fails on the trunk (112ff81) and passes with its mend. Item 5 is not pursued, at the lead's ruling. 7-788 is the box-off where the spanker in has not paid her off, beside 7-340 in `tests/test_known_truths.py` (the convoy's truths, below).

## Item 1: a wait behind other work, said in the log

**Seen.** The brig under plain sail: `take in the main topsail`, then `furl the main topsail`. The reply was "Order: furl the main topsail.", and no line of the log said that the furl waited, nor what for, until "Lay aloft and furl the main topsail." two minutes on. A whole-ship order queued behind a manoeuvre said nothing at all: `heave to` (or `tack`, `fill away`, `scud`, `lie a-try`) given while she wears. Neither did the helm's own box-off waiting behind a take-in.

**Cause.** `Runner.start` returns the words "'Furl the main topsail' will follow 'take in the main topsail', which the hands are still at.", and the World leaves the text of an order whose kind is `evolution.started` to the runner, whose line is the work's own started line. The runner wrote a turn-wait as a line only behind the yards a belay handed on, or for a whole lateen aback. A wait for hands was always said; a wait for its turn was not.

**Mend.** The runner says every turn-wait in the log at the order, once (`evolution.waiting`, notable), as it already said the two above. Callers that log the words as a line of their own pass `say_wait=False`: the fight's and the damage orders' `evolution.queued` line, and the forced-round settee and lateen. The order's own line, written when part of an order is not done, drops words the runner said itself (`verbs.unsaid`, the runner's `WAIT_SAID` mark), so that "Shorten sail: 'Reef the fore topsail' will follow ..." is not said twice. Ground tackle keeps its own line, "The weigh waits for the anchor: ...", and says the runner's only where that one does not apply. The mark is in the runner's `__dict__` only while set, so a checkpoint is as it was.

## Item 3: "Filled away" of a ship going astern

**Seen.** The lugger hove to in 15 kn and filled away: "Filled away on the larboard tack; steering ENE (68°)." a second after the order, with a knot and a half of sternway on her (she has headway a minute on). The bilander, likewise at the brace. The cutter in 15 kn, the wind four points on her bow, `lie a-try` and `fill away`: "Filled away ...; braced full and steering ENE (68°)." with two knots of way. She then sags to 39° off the wind and goes astern at 1.15 kn for the hour, with no line. She is not lifting, since she has no headway, and not aback, since no sail is backed and some still draw.

**Cause.** The line is `fill_away`'s `on_complete`, said when the yards are braced full whatever her way, and nothing watched her after.

**Mend, in words.** "Filled away" is said only of a ship with headway. With none, it is "Braced full on the larboard tack; ...; she has no headway on her yet." ("Her sheets drawn ..." where she works no braces), and then, once, "She gathers headway; filled away on the larboard tack." when she has it. If ten minutes pass with none, a line says she has not. A ship filled away with way on her that then loses it and makes sternway is told so once: "Filled away, she has lost her way and makes sternway, under a knot, the wind 38° on the larboard bow." (a knot and more by its knots). With a little way on her, under the half knot that is way, the line says "she has but little way on her yet". The watch is `scripts.watch_filled_away`, run by the runner each tick. Its mark is in `ship.extra` while it watches, and it ends unsaid when she heaves to or a manoeuvre begins. It reads her way and touches nothing. The completion line keeps its kind, `ship.filled_away`, which the captain reads. `FILLED_WATCH_S` (600 s) is JUDGEMENT.

**Carried forward, not this package's** (the lead's ruling): the cutter's hour astern is what she does, every ship's helm kept as for headway while she makes sternway. The case: the cutter, seed 7, 15 kn from north, heading 60, `set plain sail`, 600 s, `set the topsail`, 600 s, `lie a-try`, 900 s, `fill away`. Filled at +1 s with 2.2 kn of way, the helm on a heading for ENE (68°). Her head sags from 57° to 45° off the wind by +120 s with 35° of rudder, her way falling to 1.2 kn. By +300 s she makes 1.04 kn of sternway, 38° off the wind, the rudder at −29° (the heading helm's sign for headway, which with sternway holds her head up). She stays so, 1.15 kn astern, 39° off, −29° of rudder, from +600 s to the end of the hour and beyond. No sail is backed, and the lifting and aback lines do not fire: she has no headway to lift, and some sail draws.

## Item 4: a take-in countermands the setting of its sail (built at the lead's ruling; changes what she does)

**Seen.** The brig in 40 kn: `set plain sail`, then `take in all sail` 300 s on. The main topsail, the topsails' topgallants and the spanker were set after it (635 s to 1013 s) and stood in the gale. Given 30 s on, the whole order was refused, "Nothing done: ... already furled", and every sail was then set.

**Cause.** `verbs._sail_check` refuses a take-in or furl of a furled sail, "already furled", while its set is in hand or waiting. Nothing belays the set, which goes on, and a sail being loosed is taken in only after its set is finished.

**Mend** (`verbs._countermand_the_set`). A `take in` or a `furl` given while the setting of its sail is in hand or waiting belays that setting first, by the captain's own belay (`Runner.belay`). It is said once, in the belay's words: "Belayed setting the fore topsail (the fore topsail left loosed and hanging from the yard), setting the main topsail (not begun, it was waiting for hands), ...". A sail the belay leaves furled is done. One left loosed or half set is taken in from where it is. Where the order then has nothing left to start, the belay is the order's own line and reply (`work.belayed`). Otherwise the belay is a line of its own beside the order's.

**Old beside new**, the brig in 40 kn:
- At 300 s, before: main topsail, fore and main topgallants and spanker set and standing at the end. Now: one belay line; the fore topsail is taken in from where it hung; nothing set at the end.
- At 30 s, before: the order was refused and every sail set. Now: the reply and the line are the belay; nothing set.

**The other way round is unmoved.** A `set the main topsail` given while `take in the main topsail` is in hand is refused, "The main topsail is already set.", and the take-in goes on to its end. The sail ends in its gear, as the take-in said. Nothing is set against an order, so this is not the same fault. The refusal's words are half true while the sail is coming in, and are listed, not mended. It is truth 7-787.

## Item 5: a ship hung in stays cancels the player's take-in (not pursued, at the lead's ruling)

I tried ten ships (brig, frigate, cutter, smack, lugger, merchant brig, bilander, hermaphrodite brig, privateer schooner and topsail schooner) at 8, 15 and 25 kn, from 0.3 to 4 kn of way. In each tack I gave `take in` the mainsail, the spanker, the main topsail or the main topgallant. Every hang came round "Tacked", and every miss fell off on the old tack with the helm on a heading, so the helm's own box-off never fired. Forced (full and by with the wind shifted onto her bow), the box-off waits behind a take-in already in hand and does not cancel it; that wait is now said, by item 1. One given during the box-off is carried out after "Boxed her off". The one road found that cancels waiting work is the game's captain recovering a ship aback with no way (`captains._aback_with_no_way`), which belays every piece of work waiting for hands. An untriggered candidate is a take-in whose sail a box-off hauls up, failing its next step's check, with the box-off then setting the sail again. Nothing is built; the captain's rule is left as it is.

## Item 7: the dire strain warning held back by a lesser one

**Seen.** The frigate under plain sail in 18 kn, the wind rising to 40 over ten minutes. Her jib strains "at the bolt-ropes" at 1641 s and 2241 s, and passes 1.5 of its rating at 2706 s. "Stretched drum-tight" was said only at 2841 s, when the ten minutes from the lesser line were out. A cable's warning (`physics/anchor.py`) had the same rule.

**Cause.** One warning a part in ten minutes, counting every warning alike.

**Mend, one rule for both** (`strain.warning_due`). The old count is kept exactly: one warning a part in ten minutes, moved by every warning the old rule would have said. So every lesser line falls on the tick it fell on before. That matters because the game's captain takes in a head sail on the lesser "bolt-ropes" lines (`captains._head_sails_straining`), and it was the reader's finding on the first build, where a dire line said early let the next lesser line come early too. A dire warning is said whatever lesser one was within the ten minutes, and is itself said once in ten minutes. The dire count is kept on the strain state beside `last_warning_s`, not in it. The jib's dire line now comes at 2707 s. Held over its dire line for an hour, a part says it six times, once in each ten minutes. No lesser line moves. A dire line the old rule said is said on its tick, or up to ten minutes earlier where it had been held back behind a lesser one: moved earlier, then, or added, never later and never lost. No figure of load, strain or damage is read but the ratio's "dire", and none moves.

## Item 8: the smack's cast

**Seen.** The smack at anchor in Carrick Road, `get under way`. Her cast said:
- "send the ready-men aloft";
- "Lay aloft, sail-loosers! Man the topsail sheets and halliards.";
- "Let fall! Sheet home! Hoist away the topsail and the mainsail ...".

Her topsail, not of her plain sail, stayed furled throughout.

**Cause.** Fixed strings in `GetUnderWayScript`.

**Mend.** The words follow what the cast looses. Where nothing of her plain sail is furled aloft:
- "the sails to be got ready for hoisting on deck, no hand aloft";
- "Stations for making sail! Cast off the gaskets of the mainsail; the halliards manned on deck.";
- "Hoist away the mainsail, the main boom steadied over to larboard. Man the bars; heave round!".

The cutter's words, and every ship's that looses a topsail, are as they were.

**Seen and not mended: the smack's fore staysail.** Her cast is meant to make her plain sail. `_plain_sail_topsails` in `freesail/evolutions/scripts.py` (lines 9630 to 9631: "getting under way makes her plain sail"), and the record of the ships' package in `docs/dev/M7-WorkPackages.md` (line 6096: "the cast makes a ship's plain sail"), both say so. Her plain sail is the mainsail, the fore staysail and the jib (`data/ships/smack.yaml`, lines 534 to 537). The cast hoists the jib alone ("Man the jib halliards!", "hoist away the jib"), so her fore staysail stays furled after it. This is a gap between the cast and her plain sail; nothing is mended.

## Item 9: a `set the topsail` waiting for hands

**Seen.** The smack at 09:05, `set plain sail` and two minutes on `set the topsail`. The line was "Not hands enough on deck to set the topsail; the watch is setting the mainsail.". The plain sail was set by +621 s and nothing more was said until the noon relief took it up.

**Cause.** Her larboard watch has two hands fit to go aloft, and the set wants five and begins with half. The other work was never why it waited.

**Mend, in words.** Where the deck is too few for the work even with every hand at other work counted (`hands.too_few_on_deck`), the line says so and what it waits for: "...; the watch on deck has but two hands for it, and it waits for the watch to be relieved or all hands called."

**Held.** Taking it up again, or calling all hands for it, changes what she does.

## Item 13: `clear for action` and the boats

**Seen.** "The boats are out and towing astern; the ship is clear." on every ship. No boat moves: they stay on the booms, where a shot may stave them (`combat.hits`).

**Mend.** "The boats griped fast on the booms; the ship is clear." (Falconer 1780, 'Gripes': the lashings that secure the boats on deck at sea). It says "The boat ..." of one, "towing astern on her painter" of a boat her file tows, and "The ship is clear." of a ship with none.

## Item 1: the callers that say their own wait

These callers pass `say_wait=False`, because each writes the wait as a line of its own:
- `orders/fight.py`, `_start` (`beat to quarters` and the fight's whole-ship work): its reply is the `evolution.queued` line carrying the words, logged by the World. The reply and the log say it once between them.
- `orders/damage.py`, `_start` (the damage orders): the same.
- `evolutions/scripts.py`, the forced-round dip of a settee and shift of a lateen (`dip_settee`, `change_lateen`): their `after` lines log the words as `evolution.queued`.

Two more say it in their own line and take the runner's note back out, rather than pass the keyword. That way stand-in runners in tests, which take the trunk's arguments alone, serve them as before:
- `orders/ground_tackle.py`: "The weigh waits for the anchor: ..." where it applies, in place of the runner's words; elsewhere the runner's, once.
- `orders/signals.py`, `_start_hoist`: the signal's own line (`signal.ordered`) carries the runner's words, its wait with them (the second reader's finding: said twice before this).

Every other caller lets the runner say it. Wherever the order's own line is written, it drops words the runner said (`verbs.unsaid`). A wait that ends says nothing more than the work's own first line.

## Severity of every new or moved line

- A newly said turn-wait carries `turn_wait` in its data (`runner.TURN_WAIT`). It keeps it out of the World's memory of a recurring line's words, so that the lines about it keep the severity they had without it.
- Every turn-wait is routine: behind any work ("'X' will follow 'Y', which the hands are still at."), behind the yards a belay handed on, a whole lateen aback ("The mainsail is aback against the mast; it will not come in till she pays off."), and ground tackle's fallback. Before, the two said were notable; they are now one rule (`runner.TURN_WAIT_SEVERITY`). A routine line eases no compressed passage and wakes no seat. The weigh's "waits for the anchor" line is routine too (notable before).
- "Braced full ... she has no headway on her yet." and "Filled away ..." are notable, as the line always was (`ship.filled_away`).
- "She gathers headway; filled away ..." is notable (`ship.way`), as the "Filled away" line it stands in place of was; pinned (the lead's ruling on the first pass, D2, where this report said routine).
- "Filled away, she has lost her way and makes ... of sternway ..." and "Braced full ten minutes, she has gathered no headway ..." are notable (`ship.way`).
- The dire strain warning is notable, as every strain warning is.
- The waiting line of a watch too few keeps the hands-wait's severity: notable for an order given singly, routine within a group after its first.
- The cast's and the clearing's lines are routine, as their lines were (`evolution.step`, `evolution.started`).
- The countermanding belay (`work.belayed`) is notable, as every belay by order is (`NOTABLE_ORDER_KINDS`).

## Saves

A save written in these windows differs from the trunk's; every one loads either way, each read having a default:
- after a ship's first dire warning: `StrainState.last_dire_s`;
- for up to 600 s after a fill-away: `ship.extra["filled_away_watch"]`;
- between an order that queued work and the next tick: the runner's `wait_said`.

## Moved pins

All of these are old beside new in `docs/dev/TuningNotes.md` under this package.

- **One by item 3's intent:** `test_rig_words`, the lugger's fill-away line.
- **The xebec probe's take-in behind `trim sails`** (`test_lateen_whole`) was first moved here. The trunk has since moved it the same way, and the merge keeps the trunk's.
- **Fourteen recorded passages and captain's trials, by words alone:**
  - their line counts and digests are re-measured;
  - each end state is the same to the bit, and no line the trunk said changes its severity;
  - the lines added are named by kind and count in the notes' table;
  - truth 77 now pins the line count and end state beside each digest.
- **The convoy's three truths, by item 4** (what she does):
  - 7-340 is re-measured to the new day's recovery;
  - its box-off is a case of its own, 7-788, by a one-point header;
  - 7-152's straggler and 7-153's evasion are given their cause in the scenario itself (the lead's ruling E1): `data/scenarios/convoy-six.yaml` places the privateer a cable nearer (49 48.53 N 5 06.61 W, was 49 48.6 N 5 06.5 W), and both truths read the scenario as shipped. The first build's setups in the test (the Friendship lying to five minutes, the schooner moved in the test alone) are gone.
  - A new truth pins the exchange on the shipped day: `test_truth_7_153_the_scenario_as_shipped_shows_the_privateers_exchange_with_the_escort`.
  - 7-153's narrow window (E2) is found and recorded in the notes, not mended; the lead carries it.

The new truths are:
- 7-780 to 7-787, in `tests/test_words_and_waits.py`;
- 7-788, beside 7-340 in `tests/test_known_truths.py`.
