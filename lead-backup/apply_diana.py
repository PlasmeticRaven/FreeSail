import sys
merge, stamp, run = sys.argv[1], sys.argv[2], sys.argv[3]
p='docs/dev/M7-WorkPackages.md'
s=open(p).read()
anchor="## Package 70: the combat core ("
assert s.count(anchor)==1
record=f"""### Package 90, the *Diana*: a light frigate kept as a corvette, as merged (2026-11-27)

**Merged at {merge} by the hash the ships' session reported, 504c520d, with her report on top of it (2651a882).** The first new ship of package 90, and the game's fourteenth vessel: `data/ships/corvette-20.yaml`, her people `data/people/corvette-20.yaml`, made whole by the generator (`tools/ships/diana.py`; nineteen files of nineteen byte for byte from the generator, the other eighteen unmoved). By the owner's word of 24 November, with her faults told to him: "Agreed on joining her now."

**What she is.** The *Diana*, a light frigate of the Danish navy built at Copenhagen in 1804, taken by Spain at Cartagena in September 1809 and kept as a corvette to 1832 (Winfield and others 2023, p. 930; Roos 1957); her hull and profile measured on the Spanish navy's plan of her of 1809 to 1810, her displacement her own plan's, her masts' rakes from the plan (the owner, of her preview: "I quite like the mixed rake of her masts, especially so if that comes from the source directly"); flush-decked, eleven ports a side, 167 men. Her spanker is the 95 square metres her boom by Luce's chain gives, with Steel's longer boom recorded and not used, by the owner's choice "(a)". Her rudder is traced from her plan and is the least of any ship's in the game against her lateral plane.

**How she sails, as her truths pin it** (`tests/test_diana.py`; her particulars 7-660, her speed, her stiffness, her helm, her tacks, her midship lee port):
- Close-hauled her helm is within half a degree of amidships; with the wind abeam she carries one to three degrees of weather helm.
- **Under all plain sail she stays in a working breeze and is slack in stays in a fresh one:** in 12 and 15 knots she stays three times of three; in 8 knots once of three; in 20 and 25 knots she misses stays. She wears in 15 knots in about eight minutes.
- **Shortened by the game's own order she stays in 20 knots, three of three.** In 25 knots the shortening takes in her jib, and without it she gripes past what her small rudder holds, thirty to sixty degrees off at under two and a half knots: she stays once of three; **`set the jib` again and she bears away, gathers way and stays, three of three.**
- So a captain of her keeps her jib on her in a fresh breeze, and wears where she will not stay.

**How she was gated.** The hash before her last commit (608830d) was read whole by the lead's independent reader on 24 November and passed: the eighteen other ships with no difference, her truths cell for cell, twelve mutants of twelve caught; the cloud's run 168 was green on that tree. Her last commit is words alone (her reading no longer opens "a a light frigate", pinned, with a test of every ship's reading for a doubled article; her row and section in the primer's chapter 28; "a Spanish ship sloop" now read as a corvette; one line of her tacks' truth), read by the lead. Staged on the trunk with packages 127 and 126's part one in it, the cloud's run {run} was green on the tree that merged, and her own tests and the primer's, 1,167, pass.

**Owed, and by whom:**
- **With package 125** (at the lead's gate): the moment of her "mainsail haul". Hauled with the wind ahead she stayed thirteen times of fifteen under plain sail where she now stays seven; by the lead's ruling that moment is a habit of the ship said in her file, and **the ships' session sets it for her through the generator when 125 is on the trunk**, with her helm and `clr_x_m` measured again, her tacks' counts, and her topgallant yards in a rising wind.
- No block of orders for her in the primer (`tests/test_primer.py` has no row for her): for the ships' session, with that.
- Found by her builder in other ships' words and carried (`docs/dev/CarriedForward-M7.md`, fault 24): the razee, the 64 and the 74 read "hMS ..." in their class words, and the smack "a Navy's smack".

"""
s=s.replace(anchor, record+anchor)
row="truths 7-660 to 7-699 and 7-720 to 7-749 |"
assert s.count(row)==1
s=s.replace(row, f"truths 7-660 to 7-699 and 7-720 to 7-749. **THE *DIANA* MERGED 2026-11-27 at {merge}** by the hash 504c520d (the cloud's run {run} green; her reader's pass of 24 November; the owner's \"Agreed on joining her now.\"); the record is \"Package 90, the *Diana*\"; the lateen hulls' third pass and then the tartane next |")
assert "(nudge 83)" in s
s=s.rstrip('\n')+f"""

**{stamp} (nudge 84): THE DIANA IS ON THE TRUNK ({merge}), by your hash 504c520d with her report.** The cloud's run {run} was green on the merged tree; nineteen files of nineteen from the generator. Well built. Three things follow, none urgent: (1) **package 125 is at my gate with a ruling that touches her:** the moment of the tack's "mainsail haul" becomes a habit of the ship, a key of her file read through the schema (default: hauled at the point, as now; set: hauled with the wind ahead when her way is gone). No ship of today's sets it. When 125 is on the trunk I will give you the key's name: set it for her through the generator and measure again what you hold owed (her helm and `clr_x_m`, truth D to its first band if she holds it, truth E's counts, her topgallant yards in a rising wind). (2) Your two notes are taken: no block of orders for her in the primer (yours, with (1), if you judge she wants one); and "hMS ..." in the class words of the razee, the 64 and the 74 and "a Navy's smack" are written down as fault 24 of the carried list: **mend them with your third pass if they are the generator's or the reading's few lines, declared as words alone; say if not.** (3) Your pace figures are noted; the cloud's pace job is the measure and it passed. **The third pass of the lateen list is awaited on one reported hash**, holding the trunk as it then is.
"""
open(p,'w').write(s)
p='docs/dev/ShipsNudge.md'
s=open(p).read()
i=s.index("Latest note:")
s=s[:i]+f"Latest note: {stamp} (THE DIANA IS ON THE TRUNK at {merge}; package 125's ruling will give her a key of her file for the moment of the haul: its name follows when 125 merges; fault 24, the class words \"hMS ...\" and \"a Navy's smack\", may ride with your third pass as words alone; THE THIRD PASS is awaited on one reported hash). Nudge number: 84.\n"
open(p,'w').write(s)
p='docs/TheGameAsBuilt.md'
s=open(p).read()
a="- **Thirteen vessels and five boats:** the cutter, the smack, the lugger, the bilander, the brig, the merchant brig, the hermaphrodite brig, the topsail schooner, the privateer schooner, the frigate of 36, the razee of 44, the 64 and the 74."
assert s.count(a)==1
s=s.replace(a,"- **Fourteen vessels and five boats:** the cutter, the smack, the lugger, the bilander, the brig, the merchant brig, the hermaphrodite brig, the topsail schooner, the privateer schooner, the corvette *Diana* (joined 27 November, after the gate), the frigate of 36, the razee of 44, the 64 and the 74.")
open(p,'w').write(s)
p='docs/dev/CarriedForward-M7.md'
s=open(p).read()
a="a third pass of five is owed before the tartane's file. Then the corvette *Diana*, by the owner's word \"Join now\": a light ship with a small rudder, slack in stays in a breeze under all plain sail, who wants her jib; her helm and her tacks are measured again when package 125 lands. Then the tartane, the polacre, the xebec and the three-decker."
assert s.count(a)==1
s=s.replace(a, f"a third pass of five is owed before the tartane's file. **The corvette *Diana* joined on 27 November at {merge}**, by the owner's word \"Join now\": a light ship with a small rudder, slack in stays in a fresh breeze under all plain sail, who wants her jib; her helm and her tacks are measured again, and the moment of her haul set in her file, when package 125 lands. Then the tartane, the polacre, the xebec and the three-decker.")
i=s.index("23. The box off's own line can name the wrong tack"); j=s.index("\n", i)+1
s=s[:j]+"\n24. Words of three ships' class and one's: the razee, the 64 and the 74 read \"hMS as razeed, 1795\", \"hMS as built, a 64-gun ship ...\" and \"hMS a 74-gun ship ...\" where a leading capital is made small; the smack reads \"a Navy's smack\" (found by the *Diana*'s builder, 27 November; for the ships' session with its third pass).\n"+s[j:]
b="19, 20, 21, 22 and 23 are not yet placed"
assert s.count(b)==1
s=s.replace(b,"19, 20, 21, 22 and 23 are not yet placed; 24 is the ships' session's")
open(p,'w').write(s)
print("applied")
