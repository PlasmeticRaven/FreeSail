# Gate m6a: the owner's runs (2026-10-11)

The owner's notes on his runs of gate m6a's items, as written (the file `m6a_notes.txt`),
with the saves of each run under `saves/`. The lead's reading of them and the package they
brought (45a and 45b) are in `docs/dev/M6-WorkPackages.md`; the verdict and the rulings in
`docs/gates/gate-m6a.md` and `docs/DesignProposal.md`. The saves are the owner's data files
as he sent them, kept for the record and for replay (`--load`), not read by any test.

## The notes, verbatim

```text
Station test:
1. On first station test, full and by keeps the ship far too close to the wind, loses way, sails aback, boxes off, repeats. Full and by does seem to be trying to steer until the sail lifts, but some part of the bracing or simulation means that whatever sail they are steering by is lifting only when so close to the wind as to already have no way and be forced aback. Some tuning is needed.
1b. After sheets trimmed and trim to the course ran, full and by seemed to work more correctly and keep way on while steering upwind. This could be because initially she was braced sharp up and trying to steer upwind, then after a real trim she was trimmed for the proper full and by steering. What I get from it so far is that with the proper trim order, full and by works well as an "auto" upwind steer, that isn't the absolute best angle but is a good average between speed and pointing angle, and if you sailed "manually" with the bracing sharp up and manual steering, you could get a slightly better angle, but full and by while braced sharp up may not currently function.
2. Chase made until 6:43, station returned to at 6:44 after distance ~three cables and notable brig-sloop of war within hail message
Gale test:
3. Gale test, mizzen storm staysail split and blew out of the bolt-ropes at 10:01.
3b. Taking on water (by damage or by heeling + heavy seas + rain accumulation, foundering, battening down the hatches, pumping, etc.) for Milestone 7.
4. Gale test, ship was driven towards the lee shore, tried to tack away, missed stays each time because the ship went shorten sail for weather and was only under a reefed main topsail and staysails.
4b. Ship wore at the "last moment", 18:04, so to speak, 6 cables from land on the chart "in sight" readings, then was able to make it away from land with the tide drawing the ship away.
4c. There could be some consideration for "weather direction" as the rules-based captain could perceive it, if the weather has features that look like "getting worse", they can be trigger conditions for poor weather behavior, and the inverse as well: if the weather has features that look like "getting better", that can also be part of the trigger conditions for standard/fair weather behavior.
Lee-shore test:
5. Felt like beating off a lee-shore, generally good, mizzen storm staysail split and blew out of the bolt ropes at 10:01 while lying a try
6. Captain continued towards the shore of France and then south, jib and fore topmast staysail split and blew out at 16:48
7. Attempted tacks in the area around the Platresses and La Valbelle after headsails blown out, missed stays
Trade test:
8. Up until the first anchor, mostly good, though with the wind on the beam I would have happily made either balked entrance to Falmouth, and especially the second anchor while happily sailing in on barely closer than a beam reach is not something I would have done or expected. Not sailing in if having to keep full and by, or in a headwind, perhaps, but the wind was only the tiniest bit to the north, if at all, and both entrance attempts were seemingly scrubbed due to that. Not very logical, I think.
9. Ah, thinking about it, if the calculation were being made with an assumption of anchoring near to the Falmouth marker itself, which did lie directly upwind when the second anchor was made, then it's more explicable. I assumed the point that was being aimed for was Carrick Road, north of the anchorages and on a beam reach to a westerly wind, but the westerly wind indeed blocked entrance to the inner Falmouth harbor itself. Perhaps this is OK, the only thing being that the second anchorage might have been close enough to send a boat ashore anyway. A smaller consideration, that a ship that can come to anchor in a road and close enough to trade might simply trade from there. Unreasonable/unrealistic?
10. Third anchor now due to the wind not serving, anchoring in a road and in range may be our best bet for trading, as a baseline. Needs some consideration.
Trade fog test:
11. This one "looked" and "felt" smoother, because it was simpler overall, and I thought the anchor choice was basically at the right time give or take the human judgement factor. I think we'll be able to find a way to enable the smooth and simple in-port behavior that will allow ships going about their business and having a busy port atmosphere which isn't faked. We needn't be able to handle every single edge case, but the basics must function well and reliably.

Wardroom/API/Model Captain testing:
1. ship view and chart reported nonfunctional, showing a white image instead of the actual ship or chart, I suspect either that is actually the case, or the shelve mechanic is messing things up by shelving before the model can report having actually seen the image.
2. Went aground on the Filletes, then the actual land, after the reckoning shifted due to a lead sounding (messing up a reasonable reckoning), and also we ran aground on the Filletes, but the mark on the map and the uncertainty of the reckoning both were not on top of or particularly near the Filletes mark. The pilot recommended that the deeper water was "starboard" of the Filletes, which made the officer think that heading east of the Filletes into the land (as I saw it on the chart) would be the right call.
3. Does the chart show everything that can be visited, or just the current region? It should probably show the entire world charted area, not just one region.
```
