import sys
merge, run = sys.argv[1], sys.argv[2]
p='docs/dev/M7-WorkPackages.md'
s=open(p).read()
anchor="## Package 70: the combat core ("
assert s.count(anchor)==1
record=f"""### Package 126, part two: the game's own captain and a spar carried away, as merged (2026-11-27)

**Merged at {merge} by the hash its builder reported, cf6730aa, in its fourth pass, over the reader's "not pass" on one finding the lead judged acceptable (below).** The owner's note 4 from his play of the gate: "I noticed she did not attempt to replace the topgallant mast or yard." The cloud's run {run} was green on the tree that merged. No physics, no ship file. The builder's report is `docs/design/Report-Package126.md`, sections 7 to 13; the truths are 7-776 to 7-779 with their lettered parts.

**What the captain now does.**
- **A wreck is cut away as soon as there are hands for it,** the spar that keeps her manageable first and a light spar last; then the spare is shifted, and the sails that were set are bent and set again. Where she carries no spare he says so: the Renard, a cutter, clears the wreck of her topgallant mast and says "There is no spare topgallant mast aboard."
- **The spar's work is the last claimant of her hands.** Work on her sails, her braces, a reef, the lead or bringing her to that would be short of hands takes them ("Belayed clearing away the wreck of the fore topmast: hands to brace the fore yard."), and the spar's work is taken up again after five quiet minutes with nothing waiting. If a wreck has hung an hour with the watch never free, in settled weather, he calls all hands for it and pipes down after.
- **In heavy or worsening weather he does no work on a spar at all** (at or above his shortening line, the glass falling fast, or the wind risen a force within the hour) **unless she is lying to**; work in hand is held "for the weather". Lying to, he clears the wreck.
- **Bringing her to in a gale:** what she can lie a-try under is a fact of her sail (a stout topsail, bent and standing, that reefs or is of her plain sail); a ship with none is given `heave to`, her light square canvas taken in first; an order to bring her to that is refused or fails is given again after ten minutes, twice.
- **The same holds for a player's own orders:** his `clear away the wreck` gives way to a later order of his that is short of hands, and is taken up again after (the primer's chapter 3 says so).

**The rulings it was built to** (the owner: "your rulings stand", 27 November): a captain clears a wreck as a seaman would, though the game's physics makes a hanging wreck help some hulls (fault 22); so his work is judged, passage by passage and seed by seed, against the trunk's captain who does nothing where clearing is no loss, and against the wreck cleared at once and for nothing where clearing is itself the loss; and wherever the trunk's captain brings her to in a gale, his does.

**How it was gated: four passes, four reads by the lead's reader.** The first three were not passed (hands taken from handling her; a ship worse off in a rising wind; rules not pinned; the smack's topsail blown out). On the fourth: the reader's thirteen mutants and the builder's eleven all caught by tests of each rule; no line anywhere in which work is short of hands for the spar's work; no spar order begun in heavy weather; 37 passages of the reader's own judged by seed, four outside the rule and all four declared; every bringing-to of the trunk's kept, the latest 142 seconds later; the worst cases of the earlier reads now the trunk's or within the rule (the bilander in 25 knots: 15.9 miles made good against the trunk's 16.1, where the second pass's captain drove her astern); nineteen ship files in two gales from the start with no sail lost that the trunk keeps; 40 of 65 other cases identical in every line and state, the first action line for line, the corvette untouched where no spar is lost. Of the builder's own 140 passages, 121 are inside the rule and 19 declared with their causes.

**The finding the lead judged, and merged over.** In a steady westerly gale from the start the cutter is brought to nineteen minutes after the trunk's captain brings her to, where the lead's rule allowed five. The trunk's cutter lies a-try under her light topsail, which strains for an hour and blows out, and she ends sailing on; this one takes that topsail in first, heaves to under her fore-and-aft canvas, and lies so to the end with the sail whole. She is later and better found; it is of the kind the builder declares for her and was not in his table for that wind. **Told to the owner, and his to overturn.**

**Declared, and carried** (`docs/dev/CarriedForward-M7.md`, section 4): a topsail schooner that has lost her fore topmast will not always heave to in a rising gale, and after two failures her captain is silent for an hour and a half (fault 25; giving her a course again was tried and did not restore her); the smack's heave-to fails in a gusty gale and takes two and a half hours to hold (fault 26); the cutter in a rising gale heaves to where the trunk's sailed on; nine passages where the wreck's windage, gone, costs her (fault 22), one of which, the 74 in a rising gale, is four miles behind even the wreck cleared at once, its cause only partly shown. **One pin moved:** the primer's third chapter is longer by a paragraph (about 11,330 tokens to about 11,480).

"""
s=s.replace(anchor, record+anchor)
row="**part two, the captain's spar work and `lie a-try`, HELD for a third pass** after two reads not passed; the record is \"Package 126, part one\" |"
assert s.count(row)==1, s.count(row)
s=s.replace(row, f"**PART TWO MERGED 2026-11-27 at {merge}** by the hash cf6730aa, its fourth pass (the cloud's run {run} green; the lead's reader not passing it on one finding the lead judged acceptable and told the owner); the records are \"Package 126, part one\" and \"part two\" |")
open(p,'w').write(s)
p='docs/dev/CarriedForward-M7.md'
s=open(p).read()
a=" **Built and held: package 126's part two, after two reads not passed (the spar's work took the hands that work her); a third pass is in hand.**"
assert s.count(a)==1
s=s.replace(a, f" **Mended: package 126, part two, merged 27 November at {merge}, in four passes.**")
b="holds 12 for its part two;"
assert s.count(b)==1
s=s.replace(b, f"mended 12 in its part two (merged 27 November at {merge});")
c=" and where a ship with no topsail to lie under will not heave to in a gale after two tries, he gives her her course again as the trunk's captain does (package 126's part two)."
assert s.count(c)==1
s=s.replace(c, "; a ship with no topsail to lie under is given `heave to` (package 126's part two). Giving her her course again after two failed tries was built and did not restore her, so it was left out and the case is carried (fault 25).")
i=s.index("24. Words of three ships' class and one's"); j=s.index("\n", i)+1
add="""
25. **A topsail schooner without her fore topmast will not always heave to in a rising gale, and her captain then falls silent** (package 126's part two, declared; the lead's reader, 27 November). With no topsail to lie under she is given `heave to`; in 38 knots it can fail ("she would not lie to on the larboard tack; the helm amidships"), is given again and fails again, and for about an hour and a half he gives no order while she neither lies to nor sails her course (15.9 miles made good in three hours where the trunk's, refused `lie a-try` once, sailed on and made 27.1). On another seed she heaves to and lies so.

26. The smack's heave-to in a gusty gale from the start fails three times and holds only after two and a half hours; in a steady gale she is never brought to, as before (the lead's reader of package 126's part two; she keeps her topsail now).
"""
s=s[:j]+add+s[j:]
d="24 is the ships' session's"
assert s.count(d)==1
s=s.replace(d,"24 is the ships' session's; 25 and 26 are for a later package of the captain's")
e="- A player's own spar work gives way to a later order of his that is short of hands, and is taken up again after (package 126's part two)."
assert s.count(e)==1
s=s.replace(e, e+"\n- Package 126's part two was merged over its reader's \"not pass\" on one finding: the cutter, in a steady gale from the start, is brought to nineteen minutes later than the trunk's, having first taken in the light topsail the trunk's cutter lay under and lost; she ends hove to with her sail whole where the trunk's ends sailing on.")
open(p,'w').write(s)
print("applied")
