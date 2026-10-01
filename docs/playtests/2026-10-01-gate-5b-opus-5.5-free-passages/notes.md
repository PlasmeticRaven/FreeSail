# Playtest 13: gate 5b, two free passages, the cutter and the brig (Opus 5.5 through Claude Desktop)

Two passages the owner sailed without a scenario's book, in the gate-m5b build, with Opus 5.5 at the watcher's station through Claude Desktop (the consent record of 2026-09-29): the cutter *Sherbourne* on "An October day" (the climatology's weather, seed 7) from off Ushant to off St Anthony's Head, fourteen hours; and the brig *Harpy* on "A July day" (seed 7) from off Brittany in fog to off the Start, a night hove to between, thirty-seven hours. The owner's notes are below as written; the watcher's post-session notes are `post-session-notes-cutter.md` and `post-session-notes-brig.md`, its journals `journal-cutter.md` and `journal-brig.md`, all verbatim; the saves are `cutter-save.json` (tick 49921) and `brig-save.json` (tick 133945) with their checkpoints. The refused orders of each, replayed by the lead, are in `refused.md`.

## 1. The scenario, the seed and the build

Free passages: the ship, the climatology's weather for the month, seed 7, the `gate-m5b` build, the browser, the watcher through Claude Desktop. The cutter: 118 orders at the prompt, no preset book (the owner wrote six standing orders on the way, a timed lead among them). The brig: 151 orders, a book written on the way ("Lie Off", "Night Sails", a blind lead every ten minutes, "Lye off" under twenty fathoms).

## 2. What happened, in the owner's and the watcher's words

The cutter: reefed before setting anything on a lee shore in 22 knots, two reefs in the main, staysail and jib, north at seven to eight knots; squalls every half hour veering and blowing 28 to 35; a cross-bearing fix off the Lizard, Black Head and the Beast at 15:12 found her six miles west of the reckoning; hauled to NNE outside the Manacles; a tack off St Anthony's Head in the dark at 17:44, "a proper escape"; hove to in seven fathoms for want of an anchor. The brig: all sail and the lee studding sails in fog off Brittany, steered across the Channel on the watcher's advice rather than up the French coast; the fog lifted at noon, a bearing moved the reckoning ten miles west; a night hove to twenty miles south of the Start in thirty-seven fathoms; fog again in the forenoon with the blind lead going; the Start at noon; becalmed six miles NE of the Start with all sail in, the glass 30.32, "uncompromising realism".

## 3. The owner's notes (verbatim)

> 1. Cutter trysail and storm jib are the same as the jib and mainsail in the viewer? Should be different sizes/positions, surely? Same for the brig storm trysail
> 2. Cutter bowsprit doesn't move in the viewer when run-in or run-out.
> 3. Cutter heave to a bit uncertain, needs some more testing and perhaps tuning, but also might have been the exact situation and my seamanship. Something to consider.
> 4. Brig heave to came all the way through the wind before going back through again and settling on the original tack, hove to. Worked out, but felt a bit wrong. Just one instance, so again, more testing probably needed before making any decisions.

## 4. What the owner wished to say and could not

`refused.md`. From the watcher's notes: `scandalise the driver` refused with an honest reason (no state for a dropped peak yet); `clew up the driver` corrected to `brail up`; `reef the mainsail, N reefs` takes N more, not to N; "daylight is night" accepted in one standing order and "the daylight is night" refused in another.

## 5. What the watcher said

The cutter: the lee shore at the start, the fix, the Manacles, the escape; its own mistake, reading the helm as weather helm all day when the reading gives no side (at 17:06 it was lee helm). The brig: the French coast in fog, the lie-off order, the blind lead. Both stood by by the bells and the events throughout and opted out at the owner's word.

## 6. How the day felt at each compression

The brig: "taken aback" as an urgent line every few minutes in a calm dropped the compression to 1x each time.

## 7. Any number a sailor would call wrong

From the watcher: the log over-reads by about fifteen per cent (both passages, the noon fix); the brig held three knots through the water for forty minutes in two knots of wind; the lookout's distances wander (the Start at four miles, then four leagues, then three leagues, while she made half a knot); "making sternway" shown at four knots; "a heavy sea getting up / going down" chattered through the squalls; the Manacles, the Old Wall and the Black Rock never sighted from the cutter passing two to three miles off; one mark at five miles in the list and three by the bearing taken.

## 8. How the setup went

As at gate 5a.

## 9. What to keep from the model's own account

The cutter, in the watcher's order of weight: no lights at night (the Lizard's lights seen by day as a mark and not after dark; the lead's note: the night rule bounds a light by the weather's visibility, which the squalls' rain had at a few miles, so the rule and the words of the visibility are both to look at); lead orders conditioned on "land in sight" going dead at dark; emergency handling (the tack queued behind the lead, "avast that" belaying the tack and not the lead, the tack refused until close-hauled); "trim sails" bracing the furled square yards first and starving the mainsail's trim and once the lead; reefs additive, a reef standing order stacking to four; "shoal water" heaving her to in seven fathoms in an entrance. The brig: "taken aback" urgent in a calm; way coming off too slowly in a calm; "trim sails" chasing flaws (the instant wind, not the mean); the lookout's wandering distances; no reading for being hove to (`if she is not hove to`); the daylight parse; the chart's edge north of the Start. Both: the helm reading's side. Preferences, kept as such: the officer-of-the-watch station, an action. Politeness: the rest.

## 10. Follow-ups

The lead's sorting of this and playtest 12 is in `docs/dev/M5-WorkPackages.md`, "Follow-ups from gate 5b's playtests", and decision 30.
