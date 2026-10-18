# The owner's chart checks (2026-10-18)

The owner, after the Éclair's first cruise: a quick check of the in-game chart at the
harbour span for places that appear closed off by the drawn land where they should not be,
"places to look at at least for the drawn chart so that they show the actual charted
bounds accurately enough for the close-in navigation necessary". Three pictures:

- `santona-closed.png`: the road of Santoña drawn inside a land polygon that closes the
  harbour's entrance from the sea.
- `passages-broken.png`: the harbour of Passages drawn as detached contour fragments, the
  inlet's sides not joined to the coast on either hand, the mouth of Passages a cable
  north of a closed shape.
- `roscoff-channel-pinched.png`: the channel of Bas with the island's and the mainland's
  contours all but touching at the eastern narrows (the lead's measurement: 92 m), where
  the keel read six fathoms.

**The lead's reading** (spec M7b §26, "The chart's drawn coast at the harbours"): the drawn
coast is the region's level-2 contour of the depth grid (cells of about 115 m); a channel or
an inlet narrower than two or three cells closes or breaks in it, while the harbour patch
under the keel holds the water. The fix is one for all three: draw the coast, and read the
nearest land, from the finest level wherever a harbour patch exists (or from the French and
Spanish shoreline data where the repository may carry them), so that the picture, the lookout
and the keel agree. The Passages fragments are the contour cut at the patch's edge and not
rejoined: the same fix, with the patch's contour stitched to the region's at its boundary.
Booked ahead of 61; the owner's three places are its test cases, with the eastern narrows
of Bas, the Goulet and Carrick Road.
