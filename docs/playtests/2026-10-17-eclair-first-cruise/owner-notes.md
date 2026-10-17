# The owner's notes on the Éclair's first cruise (2026-10-17)

The owner was captain at the browser; the lead held the officer's station over the tunnel.
The owner's words in play are in the game's log and in `lead-officer-replies.md`'s context;
these are his notes after, verbatim, on the ship and the viewer, with his three pictures
beside them (`pictures/`).

> My notes were mostly on the ship and viewer, besides what I sent in game:
>
> 1. Lug sails and topsails brace at different angles (incorrectly)
> 2. The topsails are modeled as square topsails, they should be lug topsails and handle accordingly
> 3. The lug sails, based on being braced, at least visually, at different and somewhat inverse angles to the square sails (incorrectly for the tack and wind), the sails appear backed visually, filling the wrong direction (as though aback).
> 4. The lugs appear to be centered on the masts, where they should be about 2/3 to windward.
> 5. Note for this, and for other ships: the sails currently block the mast at the wrong aspect, viewed from the front, where they should block the mast it shows, and from behind, the mast is blocked.
>
> Pictures sent for reference, first you can see it mostly looks good except for the lugs being centered clearly, and the topsails being square rather than lug topsails. Second picture shows the disparate trimming, probably a combo of the topsails being square rather than fore and aft, and possibly something in the lug sails themselves, as when trimmed directly to the wind with the trim order they still visualized as aback. The third pic shows the clear centering of the lug sails, whereas they should be about 2/3 to windward on either tack, and also when running.

**The lead's reading, routed to package 57 (the rig through the generator) and the viewer:**

- Items 1 to 3 are one thing: the chasse-marée's topsails are lug topsails set on the
  topmasts above the lower lugs, fore-and-aft sails trimmed with the lugs, not square
  topsails braced by yards; the ship file and the generator give her square topsails, so the
  trim rule braces them as yards while the lugs are sheeted as fore-and-aft sails, and the
  two disagree at every point of sailing. The repeated "taken aback" of the cruise (three
  times on a shift or a turn) is the square topsails' rule catching the wind on the wrong
  side while the lugs were right. The fix is in the ship file and the generator (57: the
  period's shapes), with the trim rule reading a lug topsail as fore-and-aft.
- Item 4: a dipping lug's yard is slung about a third of its length from the fore end, so
  two-thirds of the yard and sail lie abaft the mast, and the sail is set on the lee side of
  the mast (dipped round it at each tack; a standing lug stays on its side). The viewer
  draws the yard centred on the mast and the sail on the mast's line; it should draw the
  yard slung a third from its fore end and the sail on the lee side (the owner's "two-thirds
  to windward" read as the slinging; to be confirmed with him), on either tack and running.
- Item 5: the viewer's draw order is by a fixed list, not by the aspect: from ahead the sail
  before the mast should hide it and from astern the mast should hide the sail; the painter
  orders the parts by their depth from the viewer. With it, the finding of the cruise that
  the view does not show the yards' brace (the lead's journal, 18:29).
