# The owner's first action (2026-10-24): package 70 as merged, played to the strike and the repairs

The owner played `data/scenarios/first-action.yaml` from the harbour at the captain's
station with no input until the enemy struck, then worked the repairs himself as far as
the game allows today. The save is `save/m7-first-action.json` (the fighting book loaded
beside the starter's; the King's cutter with her carronades; seed 7); the lead replayed it
to the end tick and read the log (570 lines, digest `353377dd3ef7d292`).

## The owner's words

"Overall, not bad at all for a start. It's missing a bit of the visible pageantry, but that
can come with time. Something like showing the gun ports and guns in the viewer with some
basic movement, and some firing effects (smoke plumes/muzzle flash over a few seconds when
each gun actually fires) and basic smoke lingering to sell it. Otherwise, functionally, it
seemed quite good, damage came to the rigging, shots were missing and hitting on both
sides, both ships kept up the fight, though it was basically just a single loop around a
circle, through the wind, at least as it appeared at first glance. That's fine for the
first action, anyway, with no player or model input."

## The action as the log has it

The privateer cutter opens fire at five cables at 781 (13 minutes in); the book's "return
her fire" answers at once. In two hours the King's cutter fires 51 times (three or four
carronades a time as they bear) and the enemy's shot strikes her 18 times, all in the
rigging and the sails (the topsail sheet, a brace, the square sail yard in the slings, the
main topgallant mast, the larboard main shrouds, the staysail halyard, both jib sheets, a
backstay, the trysail outhaul; shot through the topsail, the jib and the mainsail; two
shot across the deck, nobody hurt). The enemy strikes at 7560 (12:06); the book ceases
firing, the captain secures the guns and shapes a course for his cruising ground.

**The circle through the wind (the owner's note), confirmed.** The rules captain's engaging
helm steers each minute "to keep the enemy on the engaged beam" by the enemy's bearing
alone: 76, 61, 45, 3, 351, 340, 328, 316, 304, 291, **278 ("lies in the wind's eye from her
head; she will be taken aback")**, 264, 246, 226 ... 113, 97, 86, 68, 78, 67, 53, 31, 21: a
full turn to larboard in two hours, through the wind's eye at 2940 to 3107 with the head
sails aback and no way on, the carronades silent from 2160 to 4320 (the enemy on the other
beam, the engaged side never shifted). The law has no regard for the wind: it should
never order a course within the close-hauled angle, should shift the engaged battery when
the enemy passes through the eye, and should keep or take the gage by the doctrine. **For
the next captain's pass (booked with 71's brief, the captain's helm in action).**

## The owner's repairs, and what the game answered

Worked: `the glass on her`, `the damage report` (and `damage report`, `the damage`), `reeve
the jib sheets`, `reeve the staysail halyard`, `send down the topgallant yard`, `set the
jib`, `cut away the wreck of the main topgallant mast`, `send down the square sail yard`,
`shift the square sail yard`, `trim the square sail yard`, `reeve the starboard topsail
sheet`, `take a fix`, `set the topsail` (once its sheet was rove), `trim the sails`, `set
the staysail`, `reeve the storm trysail outhaul`, `steer east`, `trim for a run`, `pipe
down`.

Refused, and what each wants:

- `reeve new lines`, `reeve a new line`: the game wants the line named. A reading of the
  parted lines (`the parted lines`, `the lines`, `the halyards`, `the sheets`, `the
  braces` were all tried and refused as not orders) would let the player find them; **the
  damage report should list the parted lines by name**, and `reeve new lines` could rove
  every parted running line in turn as a standing evolution. 73's damage control.
- `reeve new larboard shrouds`, `reeve the starboard main topmast backstay`: standing
  rigging is set up, not rove; "nothing here sets it up" is honest and is 73's (knotting
  and setting up shrouds and backstays under fire, the preventer backstays before it).
- `shift the main topgallant mast`: no spare aboard a cutter; right by the file, and the
  spares are 77's catalogue. `shift the topgallant yard` waits on the mast: right.
- `reeve new square sail braces`, `reeve the larboard topgallant yard brace`: went with
  their spars; the game says to clear the wreck and shift the spar first: right.
- `raise the topsail`, `raise the topsail yard`: not the dialect's words (`set the topsail`
  is), and `set the topsail` then said the sheet must be rove first: the right road, found.
- `trim the square sail`: unbent after the yard was shifted; right.
- `the surgeon`, `where is the surgeon`: nobody hurt and no surgeon's reading; 73's.
- `gybe the mainsail`: "wear ship" understood and "the mainsail" not; a cutter's boomed
  mainsail gybes of itself when the helm carries the wind across (58b), and the answer
  should say so: 78's gybe as an evolution, and its words now.
- `captain: carry on`: a world order's form at the ship's prompt, refused as such; the
  owner meant the captain's `carry on` after standing him aside (`the glass on her` struck
  his book). The two forms collide for a player: a note for the harbour's second pass.

## Found in the replay and fixed by the lead (2026-10-24)

**Two of the fighting book's seven orders were refused at the load** ("'at quarters' names
no event the ship knows; did you mean at quarters?"): the event was registered under the
words "at quarters" while the grammar looks up the words after `at`. Registered as
`quarters` (and `the beat to quarters`); the book loads whole (eleven orders with the
starter's). **The book-conflict line** ("the book holds one of that name already (the
captain's); the book's is kept") read both ways; it now says the held order stands and the
book's is not loaded. The five such lines at 540 are the rules captain's engaging book
meeting the player's fighting book of the same names, which is by design (the player's
stands).

## Booked

- The viewer's pageantry (the owner): the gun ports and guns drawn with some movement, a
  muzzle flash and a smoke plume over a few seconds at each gun's firing, smoke lingering
  to leeward: package 81 in `docs/dev/M7-WorkPackages.md`.
- The engaging helm: with 71's brief.
- The damage report naming the parted lines, `reeve new lines`: 73's.
