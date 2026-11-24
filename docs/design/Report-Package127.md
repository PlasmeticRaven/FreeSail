# Package 127: words and waits on today's ships

The design and report of package 127, the eight faults of `docs/dev/CarriedForward-M7.md`, section 4 (items 1, 3, 4, 5, 7, 8, 9 and 13), in what the log said, or failed to say, on ships already in the game. The log is the game: a line untrue, or a wait unsaid, is a fault of the game. Each was reproduced on a committed ship by a player's orders (seed 7, a steady wind from the north unless said), its cause found, and mended at the cause where the mend changes only what is said. Where a mend would change what a ship does, it is held for the lead's word.

New truths 7-780 to 7-786 are in `tests/test_words_and_waits.py`, a file of their own so that the three builders of the mending step do not meet in `tests/test_known_truths.py`. Each fails on the trunk (112ff81) and passes with its mend. 7-787 and 7-788 are kept for items 4 and 5, if the lead rules them in.

## Item 1: a wait behind other work, said in the log

**Seen.** The brig under plain sail: `take in the main topsail`, then `furl the main topsail`. The reply was "Order: furl the main topsail.", and no line of the log said that the furl waited, nor what for, until "Lay aloft and furl the main topsail." two minutes on. A whole-ship order queued behind a manoeuvre said nothing at all: `heave to` (or `tack`, `fill away`, `scud`, `lie a-try`) given while she wears. Neither did the helm's own box-off waiting behind a take-in.

**Cause.** `Runner.start` returns the words "'Furl the main topsail' will follow 'take in the main topsail', which the hands are still at.", and the World leaves the text of an order whose kind is `evolution.started` to the runner, whose line is the work's own started line. The runner wrote a turn-wait as a line only behind the yards a belay handed on, or for a whole lateen aback. A wait for hands was always said; a wait for its turn was not.

**Mend.** The runner says every turn-wait in the log at the order, once (`evolution.waiting`, notable), as it already said the two above. Callers that log the words as a line of their own pass `say_wait=False`: the fight's and the damage orders' `evolution.queued` line, and the forced-round settee and lateen. The order's own line, written when part of an order is not done, drops words the runner said itself (`verbs.unsaid`, the runner's `WAIT_SAID` mark), so that "Shorten sail: 'Reef the fore topsail' will follow ..." is not said twice. Ground tackle keeps its own line, "The weigh waits for the anchor: ...", and says the runner's only where that one does not apply. The mark is in the runner's `__dict__` only while set, so a checkpoint is as it was.

## Item 3: "Filled away" of a ship going astern

**Seen.** The lugger hove to in 15 kn and filled away: "Filled away on the larboard tack; steering ENE (68°)." a second after the order, with a knot and a half of sternway on her (she has headway a minute on). The bilander, likewise at the brace. The cutter in 15 kn, the wind four points on her bow, `lie a-try` and `fill away`: "Filled away ...; braced full and steering ENE (68°)." with two knots of way. She then sags to 39° off the wind and goes astern at 1.15 kn for the hour, with no line. She is not lifting, since she has no headway, and not aback, since no sail is backed and some still draw.

**Cause.** The line is `fill_away`'s `on_complete`, said when the yards are braced full whatever her way, and nothing watched her after.

**Mend, in words.** "Filled away" is said only of a ship with headway. With none, it is "Braced full on the larboard tack; ...; she has no headway on her yet." ("Her sheets drawn ..." where she works no braces), and then, once, "She gathers headway; filled away on the larboard tack." when she has it. If ten minutes pass with none, a line says she has not. A ship filled away with way on her that then loses it and makes sternway is told so once: "Filled away, she has lost her way and makes a knot of sternway, the wind 38° on the larboard bow." The watch is `scripts.watch_filled_away`, run by the runner each tick. Its mark is in `ship.extra` while it watches, and it ends unsaid when she heaves to or a manoeuvre begins. It reads her way and touches nothing. The completion line keeps its kind, `ship.filled_away`, which the captain reads. `FILLED_WATCH_S` (600 s) is JUDGEMENT.

**Held.** The cutter's hour astern is what she does: the heading helm holds 29° of rudder the wrong way for sternway. That is not mended here.

## Item 4: plain-sail work sets a topsail in a gale after `take in all sail` (held)

**Seen.** The brig in 40 kn: `set plain sail`, then `take in all sail` 300 s on. The main topsail, the topgallants and the spanker are set after it and stand in the gale. Given 30 s on, the whole order is refused, "Nothing done: ... already furled", and every sail is then set.

**Cause.** `verbs._sail_check` refuses a take-in or furl of a furled sail, "already furled", while its set is in hand or waiting. Nothing belays the set.

**Proposed, not built.** The take-in belays the set (`Runner.belay`, said "Belayed setting the main topsail"). It changes what the ship does, so it waits for the lead's word.

## Item 5: a ship hung in stays cancels the player's take-in (not reproduced; held)

**Tried.** Ten ships at 8, 15 and 25 kn, with 0.3 to 4 kn of way, and a take-in given in the tack. Every hang came round, and every miss fell off with the helm on a heading. The helm's box-off, forced, waits behind a take-in (now said, by item 1) and does not cancel it.

**Candidates.**
- The game's captain (`captains._aback_with_no_way`), which belays every piece of work waiting for hands when she is aback with no way.
- A take-in whose sail a box-off hauls up, failing its next step's check, the box-off then setting the sail again.

Either mend changes what a ship does, so both are held.

## Item 7: the dire strain warning held back by a lesser one

**Seen.** The frigate under plain sail in 18 kn, the wind rising to 40 over ten minutes. Her jib strains "at the bolt-ropes" at 1641 s and 2241 s, and passes 1.5 of its rating at 2706 s. "Stretched drum-tight" was said only at 2841 s, when the ten minutes from the lesser line were out. A cable's warning (`physics/anchor.py`) had the same rule.

**Cause.** One warning a part in ten minutes, counting every warning alike.

**Mend, one rule for both** (`strain.warning_due`). The lesser warnings keep their count, one in ten minutes, on the ticks they had. A dire warning is said whatever lesser one was within the ten minutes, and is itself said once in ten minutes. The dire count is kept on the strain state beside `last_warning_s`, not in it. The jib's dire line now comes at 2707 s. No figure of load, strain or damage is read but the ratio's "dire", and none moves. The captain's head-sail rule reads only the lesser "bolt-ropes" lines, which are unmoved.

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

**Seen and not mended.** The smack's fore staysail, of her plain sail, is still furled after the cast.

## Item 9: a `set the topsail` waiting for hands

**Seen.** The smack at 09:05, `set plain sail` and two minutes on `set the topsail`. The line was "Not hands enough on deck to set the topsail; the watch is setting the mainsail.". The plain sail was set by +621 s and nothing more was said until the noon relief took it up.

**Cause.** Her larboard watch has two hands fit to go aloft, and the set wants five and begins with half. The other work was never why it waited.

**Mend, in words.** Where the deck is too few for the work even with every hand at other work counted (`hands.too_few_on_deck`), the line says so and what it waits for: "...; the watch on deck has but two hands for it, and it waits for the watch to be relieved or all hands called."

**Held.** Taking it up again, or calling all hands for it, changes what she does.

## Item 13: `clear for action` and the boats

**Seen.** "The boats are out and towing astern; the ship is clear." on every ship. No boat moves: they stay on the booms, where a shot may stave them (`combat.hits`).

**Mend.** "The boats griped fast on the booms; the ship is clear." (Falconer 1780, 'Gripes': the lashings that secure the boats on deck at sea). It says "The boat ..." of one, "towing astern on her painter" of a boat her file tows, and "The ship is clear." of a ship with none.

## Moved pins

Two pins move, both by a mend's own intent, old beside new in `docs/dev/TuningNotes.md` under this package:
- `test_lateen_whole`'s take-in behind `trim sails` (item 1);
- `test_rig_words`'s lugger fill-away line (item 3).
