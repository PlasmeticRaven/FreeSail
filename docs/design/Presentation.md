# Design note: presentation

From the owner's general notes of 2026-09-29, sorted with the lead the same day. A note
for the viewer, sound and interface work of milestones 5 to 8; not itself a
specification. Text and data remain the baseline: nothing here may be the only way to
know something, because a language model at a station reads the same log and readings
the human does.

## Rig motion

**The boom that jumps.** Seen by the owner in a wear: the boom was on one side and then
the other. It is the model, not the viewer. A fore-and-aft sail's sheet angle is unsigned
and the sail is taken to lie on the lee side, so when the wind crosses the stern the lee
side flips in one tick and the viewer, which draws the boom at the sail's sheet angle,
follows. There is no gybe in the physics. The wear script already says "the boom will
come over". The work: a signed sheet angle; the boom coming over on a timeline during a
wear or a gybe (eased across under the sheet, or all standing with the strain that costs,
which the strain model can price); the log saying it; the viewer following the number as
it does now. A physics and evolutions item for the rig-geometry follow-ups.

**Dipping lugs and lateens.** No vessel carries them yet. When the tartane comes
(decision 11), the dip is an evolution with steps like any other, and the viewer shows
the yard where the steps put it: the pleasing motion the owner asks for comes from the
model doing the work in stages, at the same rate as everything else on the page, not from
animation. The lug and lateen classes exist in the projection already.

## Crew figures

Who is aloft and where is already in the data: every evolution's assignment names its
hands and whether they are aloft, and the runner knows the subject's mast and yard. Simple
figures at those positions (on the ratlines going aloft, on the footropes of the yard
being worked, at the braces or the capstan on deck, a lookout at the masthead) are cheap
to draw from it, a few hundred marks at the viewer's refresh. Not before milestone 5's
first wave; a viewer package with the layering fix.

## Layering

Known faults, deferred by the owner (2026-09-29), addressable later. The viewer sorts
whole figures far to near and breaks ties by sail class, so a square sail draws behind
its mast from most facings and a staysail in the centreline plane can draw in front of a
topsail it should be behind. The fix is per-figure depth from the sail's belly, and
square sails cut at the mast plane as they are already cut where a stay crosses them.

## Completion in the browser

The console completes a line as it is typed and the owner finds it useful. The server has
no route for it. A small route on the same completer, and a hint under the order line in
the client. Goes with milestone 5's interface work.

## Sound

Feasible and worth doing, as an option, comfortable rather than loud. Not FMOD, which is
commercial C++ middleware and sits badly with a Python game in a browser. The browser's
own audio synthesises from the readings the log already carries: wind noise shaped by
the wind's speed and its gusts, rigging creak by strain, the sea by the sea state when
milestone 5 has one, the crew by the hands at work and a call for all hands, alarms by the
log's urgent mark. Because every sound derives from a reading or a log line, parity with
the text is free. Instruments, generated music and public-domain shanties are a line here
for when the world has objects and evenings; nothing more now.

## Special ships

A galleon, a steam-and-sail ship, a clipper to test the limits: a line in the vessel
library's list for after the current plan, as the owner says, and no more before the
baseline is built.
