# Notes for milestone 7: details the owner wants kept

Design details noted during milestone 6 for the milestones that follow, each with its
date and its ground, so that the specification of M7 (powder) and M7b (the director) can
pick them up. Not open items of M6: nothing here waits on a package of this milestone.

## Sail handling at fine control (M7, a "fine-control" sub-module)

The owner, 2026-10-10, on the aquatint of the Nimble cutter in chase
(`docs/references/images/cutter-nimble-in-chace-aquatint.webp`) and in conversation with
the lead:

1. **Settling the halyards.** The nearer cutter's topgallant yard is run down with the
   sail left set and billowing: the squall's first order in Luce 1866 ch. XXVI, "settle
   down the top-gallant sails and royals, or clew them up". The game has the yard's hoist
   as a transient of `set`, `take in`, `reef` and `shake out` (the `hoist`, `settle
   halyards` and `clew down` steps; the yard on the cap during a reef; drawn at its hoist
   since 37n) and no held state: an order `settle the topgallant halyards` (a mast's by
   name; `settle the topgallants` for all; the cutter's one), the yard on the cap with the
   sail set and sheeted, a `settled` sail state with its drive and its load cut to a
   fraction (judgement, Luce as the source, the strain truth the check), `hoist the
   topgallant yards` or `sway up` to restore; the books' storm lines using it as the step
   before clewing up. Left out of 37p by the owner's word; a detail for M7.
2. **Fine control of the sails for speed and spill.** The vangs eased or set up to control
   how a gaff sail spills; a sail kept shivering by command ("keep the mizzen topsail
   shivering", as Luce's tacking has it for the main and mizzen topsails); the sheets
   checked or flattened by so much; the weather braces checked a little in a puff. The
   `keep <x> <state>` prefix struck from 37o (decision 39's playtest notes) may return
   here, confined to a fine-control sub-module where a held intention for a sail or a
   yard is the thing wanted, with the helm's `full and by` as its model (an intention the
   crew keeps, logged when it changes something and not every tick).

The measure for both, when they come: the strain truths (a sail settled or shivering
carries less than one drawing), the speed truths (a sail spilled slows her by what it
should), and the gale trials of package 40c under 37p's trim.
