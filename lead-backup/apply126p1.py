import sys
merge = sys.argv[1]
p='docs/dev/M7-WorkPackages.md'
s=open(p).read()
anchor="## Package 70: the combat core ("
assert s.count(anchor)==1
record=f"""### Package 126, part one: a game ended from the harbour, and fog that comes on and clears, as merged (2026-11-27)

**Merged at {merge} by the hash its builder reported, afb5a998.** Package 126 was split by the lead after its second pass: two of the owner's three notes are in this part; **the third, the game's own captain replacing a spar carried away, is held for part two** (below). The part's tree was run whole by the cloud's run 175 (45977895973, green). No physics, no ship file, and none of the captain's or the runner's code: `freesail/world/captains.py` and `freesail/evolutions/runner.py` are the trunk's byte for byte. The builder's report is `docs/design/Report-Package126.md`; the truths are 7-770 to 7-775.

**What changed for a player:**
- **A game can be ended from the harbour** (the owner's note 2): the harbour's page has "end the game"; it is refused with no game in play; with play not saved it says what would be lost and from when ("This game was last saved at Morning watch (05:02), 5 June 1805; what has passed since, to ..., is lost if it is ended.") and ends on the second word; a game saved, by the desk or by the download, ends at once; the models' doors the harbour started are stopped; nothing saved is touched, and another game begins from the same harbour. The stations' table no longer keeps one game's choice of doors into the next (older fault 6). The primer's first chapter and the README each say it in a sentence.
- **Fog comes on and clears over a time, and is said as it does** (his note 3): the air a fog lies in comes and goes by degrees in time and at its edge, and the sight closes and opens a step at a time ("A fog is settling in.", "The fog is thickening.", "The fog has shut in thick.", "The fog is thinning.", "The fog seems to be clearing.", "The fog lifted."), notable where the sight a ship is handled by changes (shut in thick; first opening), routine between; a turn of the fog is not said within ten minutes of the turn before, and is said after if it has held.

**How it was gated.** The second pass, which held these two mends with the captain's work, was read whole by the lead's independent reader: the harbour against a live game and in a browser; 78 fogs minute by minute on both trees (the same fogs; steps of two rungs of sight within a fog 164 on the trunk, none now; no fog line outside a fog, none lost; about three notable lines a fog, never more than two in an hour); a checkpoint of the trunk taken mid-fog loads and goes on; what a model's seat is served differs by the primer's sentence alone; 16 of 18 mutants killed in the fast tier and one in the slow. For this part the lead checked that everything but three small mends is that pass's code with the captain's work taken out, read the three (a game saved by the download counts as saved; the end's words give the date; the lock), and ran the reader's batch himself against the trunk: **102 cases; the 84 with no fog in them identical in every line, state hash and end; the 18 fog cruises the same until their first fog line.** The harbour's and the fog's tests, 53 with the slow ones, pass.

**Today's ships otherwise unmoved; no pin moved.** A June day in fog ends up to six cables from where the trunk's did, by the fog's own lines and what a captain does on them.

**Held for part two** (the builder has the list; on the trunk as it now is): the captain's spar work must be the last claimant of her hands (in the reader's 56 passages with a spar carried away, about twenty showed hands held from trimming, reefing or heaving to by the spar's work; the bilander in a rising wind made 1.6 miles where the trunk's captain made 12.9, and drove astern for ninety minutes); the `lie a-try` mend must act only where a topsail can never be set (it reached five more ships undeclared, and left the cutter never brought to in a gale from the start); the order of the wreck's clearing pinned. **Found and not mended:** the saves a stand-down writes are named by seed and tick, and two at one tick overwrite one another.

"""
s=s.replace(anchor, record+anchor)
row="branch `claude/pkg-126`; truths 7-770 to 7-779; milestone 8's mending step |"
assert s.count(row)==1
s=s.replace(row, f"branch `claude/pkg-126`; truths 7-770 to 7-779; milestone 8's mending step. **PART ONE MERGED 2026-11-27 at {merge}** by the hash afb5a998 (the harbour's end and the fog; the cloud's run 175 green); **part two, the captain's spar work and `lie a-try`, HELD for a third pass** after two reads not passed; the record is \"Package 126, part one\" |")
open(p,'w').write(s)
p='docs/dev/CarriedForward-M7.md'
s=open(p).read()
a="2. **A game can be ended from the harbour**, without stopping the harbour or beginning another."
b="3. **Fog comes on and clears over a time**, and is said as it does (\"the fog seems to be clearing\", \"a fog is settling in\"), as far as the weather's simulation allows."
c="4. **The game's own captain replaces a spar carried away.**"
for x in (a,b,c): assert s.count(x)==1, x
s=s.replace(a, a+f" **Mended: package 126, part one, merged 27 November at {merge}.**")
s=s.replace(b, b+f" **Mended: package 126, part one, merged 27 November at {merge}.**")
i=s.index(c); j=s.index("\n", i)
s=s[:j]+" **Built and held: package 126's part two, after two reads not passed (the spar's work took the hands that work her); a third pass is in hand.**"+s[j:]
d="package 126 takes 6 and 12;"
assert s.count(d)==1
s=s.replace(d, f"package 126 mended 6 in its part one (merged 27 November at {merge}) and holds 12 for its part two;")
e="19 and 20 are not yet placed."
assert s.count(e)==1
s=s.replace(e, "19 and 20 are not yet placed.\n\n21. The saves a stand-down writes are named by seed and tick, and two written at one tick overwrite one another (found by package 126's builder; the desk's naming, older than the package).")
open(p,'w').write(s)
print("applied")
