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

## Sails and yards as the files have them (package 37n)

**The square sail's cut.** The viewer cuts every square sail as its ship file's note says
the generator worked it (`tools/gen_ships.py`): between its yard and the yardarms below,
the clews at nine-tenths of the yard below, the head what the area leaves over the depth
between the yards; a sail with no yard below (a course, the cutter's square sail) as broad
as nine-tenths of its own yard, head and foot, and as deep as its area over that; the
schooner's topsail, whose bare fore yard the file does not carry, down to where that yard
is, its centre midway as the generator puts it. Before, the viewer drew every square sail
the whole yard broad and its area over the whole yard deep: the cutter's square sail 24 ft
deep where Steel's is 27 (the owner's note of 2026-10-09), every course a tenth short, and
the topgallants and royals overlapping the yard below by a sixth. The files' figures were
right; the drawing was not.

**A yard at its hoist.** The simulation hoists a topsail yard as the last step of setting
the sail, settles it to reef and to take the sail in, and strikes topmasts with their
yards "lowered on the caps". The viewer draws a yard on an upper mast where that work has
put it, from the snapshot as it was (the sail's state and the step in hand; no field
added): at the file's height with the sail set, lower by the depth of each reef, on the cap
of the mast below while the sail is not set, halfway while a hoist or a settling of the
halyards is in hand. A struck topmast is housed, its head just above the lower cap, its
yard on that cap; the light yards and masts sent down are on deck and not drawn, as
before. The lower yards hang in their slings and do not move, and so does the cutter's
square-sail yard, which the file crosses as a yard and to which her topsail sheets. The
view's scale is the full rig at its hoists, whatever is lowered.

## The captain's chart and its tools (package 37n)

The chart draws the account and never the truth (spec M5 §17): the reckoned position and
its ellipse, the track by account, the noons, the bearings taken, the soundings, the sail
in sight by bearing and estimate. Three things were added from the owner's notes of
2026-10-09.

**The rose.** A protractor rose the player drags by its centre and turns by its rim
(`r`, or the button). Its outer ring is true degrees, north up; its inner ring the
thirty-two points of the compass turned by the variation the master allows (the
account's, the chart of 1794's until he observes his own); its index runs through the
centre right across the chart, and its bearing is written under it, true and by the
compass, so a course or a bearing between two points is read by laying the centre on one
and the index through the other. Where it stands and how it is turned are kept in the
browser only.

**The pencil.** A line between two clicks (with its bearing and length as it is laid), a
ring about a point (its radius typed in miles or given by a second click), a note at a
point; listed in a small pane over the chart, each to be rubbed out, all at once if
wished. They are kept with the game: the server holds them on the World, every save and
checkpoint carries them, and a save taken up by the browser's server brings them back.
They are the player's pencil and nothing else reads them: not the reckoning, not the
standing orders, not the log or the readings, not a station's door. A later image of the
chart for an image-capable door (the owner's note 7, M6 §13) may draw them.

**The bearings cleaned.** A bearing taken is drawn full for a glass, fades to a ghost over
the rest of the watch, and is gone after the watch, or at once when a later bearing of the
same mark replaces it. The snapshot keeps every bearing; only the drawing is cleaned. The
noons and the player's own marks are not.

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
