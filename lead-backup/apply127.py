import sys
merge, stamp = sys.argv[1], sys.argv[2]   # the merge's short hash; "2026-11-27, HH:MM UTC"
p='docs/dev/M7-WorkPackages.md'
s=open(p).read()
anchor="## Package 70: the combat core ("
assert s.count(anchor)==1
record=f"""### Package 127: words and waits on today's ships, as merged (2026-11-27)

**Merged at {merge} by the hash its builder reported, 523f01ee, in two passes.** The first hash (abba31bc) was run whole by the cloud's run 172 (green) and not passed by the lead's independent reader; the second was run whole by run 174 (45949027944, green) and passed by the same reader in a narrow read. The physics' diff was read by the lead (the counting of the strain's warnings and the cable's, `strain.warning_due`; no figure of load, strain or damage read differently). The builder's report is `docs/design/Report-Package127.md`; its truths are 7-780 to 7-788.

**What changed for a player, on every ship already in the game:**
- **An order made to wait is said in the log, once, routine:** "'X' will follow 'Y', which the hands are still at"; behind the same work, "will follow the same work"; a group of orders says one line ("Shortening sail: some of it waits its turn, behind ..."). A wait for want of hands keeps its notable line; the weigh's "waits for the anchor" is routine where it was notable.
- **"Filled away" is said only with headway.** Without it: "Braced full" (or "Her sheets drawn") "... she has no headway on her yet" or "but little way on her yet"; then "She gathers headway; filled away on the X tack." (notable), or after ten minutes that she has gathered none, or that she has lost her way and makes sternway ("under a knot" said so).
- **A take-in or a furl countermands a setting still in hand or waiting for the same sail** (the lead's ruling; the one change in what a ship does): said once, notable ("Belayed setting ..."), by whatever order made it, alone or inside `shorten sail`. Of the builder's 130 runs 24 end differently, all by this; of the reader's 234 runs of the rule, 165.
- **The dire warning of a part is said when it comes,** whatever lesser warning of it was said within the ten minutes (33 dire lines became 147 in the reader's 78 gale runs; none later, none lost; the lesser warnings the same, 567 beside 567).
- The smack's cast names the sail she casts under; a set waiting for hands on a watch too few for it is said; `clear for action` says where the boats are ("The boats griped fast on the booms; the ship is clear."; a boat's own, "The boat is clear.").
- **The convoy of six** (`data/scenarios/convoy-six.yaml`): the privateer placed a cable nearer, so that the day a player opens shows the straggler signalled and the privateer's whole exchange again, which the countermand's change to the commodore's first tack had taken from it. Truths 7-152 and 7-153 read the scenario as shipped.

**The reader's measure.** 574 cases on thirteen vessels and five boats, old beside new, twice: no line undeclared on the second pass; every end state that differs is the countermand's; the state hashes of the two passes the same in 574 of 574 (the second pass changed words alone). Fourteen recorded passages and trials moved by words alone, each end state the same to the bit. Four checkpoints of the trunk load and go on. The first pass's findings (a countermand inside `shorten sail` said routine, and on the bilander nowhere; a signal's wait for hands losing its notable line; "She gathers headway" declared routine and logged notable; a fifth of the wait lines naming one work twice) are mended and pinned.

**Pins moved** (old beside new in the tuning notes, "Package 127"): the lugger's fill-away line; the fourteen passages' and trials' counts and digests; 7-340 re-measured and renamed; 7-152 and 7-153 by the scenario's move; 7-788 new (the box off where the spanker taken in has not paid her off).

**Carried** (`docs/dev/CarriedForward-M7.md`, section 4): the privateer of the convoy's day evades by one number (fault 19); four small things of the new words (fault 20). Saves gain three fields, each defaulted on loading.

"""
s=s.replace(anchor, record+anchor)
row="branch `claude/pkg-127`; truths 7-780 to 7-788; milestone 8's mending step |"
assert s.count(row)==1
s=s.replace(row, f"branch `claude/pkg-127`; truths 7-780 to 7-788; milestone 8's mending step. **MERGED 2026-11-27 at {merge}** by the hash 523f01ee, in two passes (the cloud's runs 172 and 174 green; the lead's reader not passing the first and passing the second); the record is \"Package 127: words and waits on today's ships, as merged\" |")
assert s.rstrip().endswith("it does not wait on 127.")
s=s.rstrip('\n')+f"""

**{stamp} (nudge 83): package 127 is ON THE TRUNK ({merge}); the third pass can come, whole, on one reported hash.** Merge the trunk first. What it brings that your third pass meets: a wait said in the log once and routine (its mark is `TURN_WAIT`; signals and ground tackle take back only marked notes); a take-in or furl countermanding a setting in hand, said notable, alone or in `shorten sail`; the dire warning said when it comes (`strain.warning_due`, `last_dire_s`): your item 2, a spar lost while its shift waits, takes that rule; and the boats' line of `clear for action`: "The boats griped fast on the booms; the ship is clear." for a ship, "The boat is clear." for a boat, so the lost boat's clause follows those words. The convoy of six's privateer lies a cable nearer. Package 126 is split: its harbour and fog come next to the gate, its captain's spar work later; neither waits on you. **The Diana's one commit of words (nudge 78) is still awaited.**
"""
open(p,'w').write(s)
p='docs/dev/ShipsNudge.md'
s=open(p).read()
i=s.index("Latest note:")
s=s[:i]+f"Latest note: {stamp} (PACKAGE 127 IS ON THE TRUNK at {merge}: THE THIRD PASS CAN COME, whole, on one reported hash, the trunk merged first; the boats line is now \"The boats griped fast on the booms; the ship is clear.\"; THE DIANA's ONE COMMIT OF WORDS (nudge 78) is still awaited). Nudge number: 83.\n"
open(p,'w').write(s)
p='docs/dev/CarriedForward-M7.md'
s=open(p).read()
a="Of these, package 127 (launched 24 November) takes 1, 3, 4, 7, 8, 9 and 13;"
assert s.count(a)==1
s=s.replace(a, f"Of these, package 127 (**merged 27 November at {merge}**) mended 1, 3, 4, 7, 8, 9 and 13;")
b="18. **A ship made a King's ship in the harbour carries no private signals**"
assert s.count(b)==1
i=s.index(b); j=s.index("\n", i)+1
add="""
19. **A privateer made a crewed ship never closes a stranger she is looking at** (found by package 127's builder and the lead's reader, 27 November). Fully crewed, the convoy's privateer keeps about 2.1 miles from the stranger she investigates and takes up evading only at 1.94 to 2.00 miles; the builder reads the cause as her near lookout making out colours at two miles without the glass where her far captain used three with it (`captains._keep_stranger`); the reader saw the distances and could not confirm the glass. So the convoy of six's day turns on where she is placed: a cable farther and nothing happens, a cable nearer and she is judged an enemy but no straggler is signalled; with other seeds the exchange comes later. Truth 7-153 pins the day as shipped, at one seed.

20. Small things of package 127's new words, left as found by the lead's reader: "will follow the same work" said of a signal waiting behind a different signal; "some of it waits its turn" where all of it waits; an order's wait logged a tick after a line of the same moment that belays what it waited for; and a wait said for a `weigh` that will be refused, there being no anchor down.
"""
s=s[:j]+add+s[j:]
c="16, 17 and 18 are the lead's proposed package 129, not launched."
assert s.count(c)==1
s=s.replace(c, "16, 17 and 18 are the lead's proposed package 129, not launched; 19 and 20 are not yet placed.")
open(p,'w').write(s)
print("applied")
